from datetime import UTC, datetime

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import select

from app.config import Settings
from app.db.models import TicketResultRow
from app.db.session import make_engine, make_sessionmaker, reset_db
from app.main import create_app
from app.pipeline.graph import PipelineDeps, build_graph, run_batch
from app.pipeline.stage4_lookup.lookup import InMemoryTransactionRepo
from app.taxonomy import load_taxonomy
from app.telemetry.db_models import AiCallRow
from tests.fakes import make_output
from tests.helpers import make_ticket
from tests.telemetry.fakes import RecordingClassifier

PHONE = "07701234567"
SETTINGS = Settings(_env_file=None, openrouter_api_key="", typesafe_api_key="")


def graph(fail_for=()):
    return build_graph(PipelineDeps(
        taxonomy=load_taxonomy(SETTINGS.taxonomy_path), txn_repo=InMemoryTransactionRepo([]),
        jev=RecordingClassifier(make_output("general_inquiry", priority="P4"), fail_for=fail_for)))


async def test_run_batch_attaches_each_tickets_calls():
    tickets = [make_ticket("سؤال", external_id="a", id=1), make_ticket("سؤال", external_id="fail", id=2)]
    outcomes, _ = await run_batch(graph(fail_for={"fail"}), tickets, concurrency=2)
    assert [len(o.ai_calls) for o in outcomes] == [1, 1]
    assert outcomes[1].status == "failed"


@pytest.fixture
def client():
    engine = make_engine(SETTINGS.test_database_url)
    reset_db(engine)
    sf = make_sessionmaker(engine)
    with TestClient(create_app(SETTINGS, session_factory=sf,
                               pipeline_builder=lambda *_: graph(fail_for={"fail"}))) as test_client:
        yield test_client, sf
    engine.dispose()


def start(client, ids):
    response = client.post("/api/runs", json={"tickets": [
        {"external_id": i, "text": "شكد عمولة التحويل؟", "customer_phone": PHONE,
         "received_at": datetime.now(UTC).isoformat()} for i in ids]})
    assert response.status_code == 202, response.text
    return response.json()["id"]


@pytest.mark.integration
def test_batch_writes_calls_with_run_and_ticket(client):
    test_client, sf = client
    run_id = start(test_client, ["ok-1"])
    with sf() as session:
        [row] = session.scalars(select(AiCallRow)).all()
        result = session.scalars(select(TicketResultRow)).one()
        assert (row.run_id, row.ticket_id, row.process) == (run_id, result.ticket_id, "classify")
        assert result.processed_at is not None


@pytest.mark.integration
def test_failed_ticket_keeps_its_calls(client):
    test_client, sf = client
    run_id = start(test_client, ["fail"])
    with sf() as session:
        result = session.scalars(select(TicketResultRow)).one()
        assert result.status == "failed"
        [row] = session.scalars(select(AiCallRow).where(AiCallRow.run_id == run_id)).all()
        assert row.ticket_id == result.ticket_id


@pytest.mark.integration
def test_ledger_failure_does_not_fail_the_result(client, monkeypatch):
    test_client, sf = client
    import app.telemetry.store as store

    def broken_rows(*args, **kwargs):
        return [AiCallRow(started_at=datetime.now(UTC), process="classify", provider="typesafe",
                          model="m", locality="cloud", latency_ms=1, cost_usd=0.0,
                          cost_source="estimate", status="ok", attempt=1, ticket_id=999_999, detail={})]

    monkeypatch.setattr(store, "call_rows", broken_rows)
    start(test_client, ["ok-2"])
    with sf() as session:
        assert session.scalars(select(TicketResultRow)).one().status != "failed"
        assert session.scalars(select(AiCallRow)).all() == []
