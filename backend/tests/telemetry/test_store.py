import logging
from datetime import UTC, datetime

import pytest
from sqlalchemy import select

from app.config import Settings
from app.db.models import RunRow
from app.db.session import make_engine, make_sessionmaker, reset_db
from app.telemetry.calls import AiCall
from app.telemetry.db_models import AiCallRow
from app.telemetry.store import add_calls, call_rows, persist_calls

NOW = datetime(2026, 11, 14, 9, tzinfo=UTC)
CALL = AiCall("kb_index", "openrouter", "openai/text-embedding-3-small", "cloud", NOW, 40,
              input_tokens=120, cost_usd=0.0000024, cost_source="provider", detail={"batch": 1})


def test_call_rows_copy_links_and_fields():
    [row] = call_rows([CALL], document_id=5)
    assert (row.process, row.document_id, row.input_tokens, row.cost_source) == ("kb_index", 5, 120, "provider")
    assert row.detail == {"batch": 1} and row.run_id is None


@pytest.fixture
def sf():
    engine = make_engine(Settings(_env_file=None).test_database_url)
    reset_db(engine)
    yield make_sessionmaker(engine)
    engine.dispose()


@pytest.mark.integration
def test_add_calls_inside_owner_transaction(sf):
    with sf() as session:
        run = RunRow(mode="jev", prompt_version="v1", model_ids={}, status="running")
        session.add(run)
        session.flush()
        add_calls(session, [CALL], run_id=run.id)
        session.commit()
        [row] = session.scalars(select(AiCallRow)).all()
        assert row.run_id == run.id and row.started_at == NOW


@pytest.mark.integration
def test_add_calls_failure_keeps_the_owner_transaction(sf, caplog):
    with sf() as session:
        run = RunRow(mode="jev", prompt_version="v1", model_ids={}, status="running")
        session.add(run)
        session.flush()
        with caplog.at_level(logging.WARNING):
            add_calls(session, [CALL], run_id=run.id, ticket_id=999_999)  # FK violation
        session.commit()
        assert session.get(RunRow, run.id) is not None
        assert session.scalars(select(AiCallRow)).all() == []
    assert "AI call recording failed" in caplog.text


@pytest.mark.integration
def test_add_calls_surfaces_the_owners_own_flush_failure(sf, caplog):
    from sqlalchemy.exc import IntegrityError

    with sf() as session:
        session.add(AiCallRow(started_at=NOW, process="kb_index", provider="p", model="m", locality="cloud",
                              latency_ms=1, cost_usd=0.0, cost_source="unknown", status="ok", attempt=1,
                              ticket_id=999_999, detail={}))  # the owner's pending FK violation
        with caplog.at_level(logging.WARNING), pytest.raises(IntegrityError):
            add_calls(session, [CALL])
    assert "AI call recording failed" not in caplog.text


@pytest.mark.integration
def test_persist_calls_own_transaction_and_swallow_errors(sf, caplog):
    persist_calls(sf, [CALL])
    with sf() as session:
        assert len(session.scalars(select(AiCallRow)).all()) == 1

    def broken():
        raise RuntimeError("db down")

    with caplog.at_level(logging.WARNING):
        persist_calls(broken, [CALL])
    assert "AI call recording failed" in caplog.text
