import uuid
from datetime import UTC, datetime

import pytest

from app.telemetry.intake import intake_calls

START = datetime(2026, 11, 14, 9, tzinfo=UTC).isoformat()


def entry(**kw):
    return {"model": "google/gemini-3.8-flash", "provider": "openrouter", "locality": "cloud",
            "kind": "analyze", "started_at": START, "latency_ms": 900,
            "usage": {"input_tokens": 1200, "output_tokens": 300}, "cost_usd": 0.002,
            "cost_source": "provider", "cost_estimate_usd": None, "error": None,
            "attempt_id": str(uuid.uuid4())} | kw


def test_provider_cost_entry():
    [call] = intake_calls([entry()])
    assert (call.process, call.provider, call.cost_usd, call.cost_source) == ("intake", "openrouter", 0.002, "provider")
    assert (call.input_tokens, call.output_tokens, call.detail["kind"]) == (1200, 300, "analyze")


def test_intake_call_without_cost_uses_estimate_or_unknown():
    estimated, unknown, local = intake_calls([
        entry(cost_usd=None, cost_source="estimate", cost_estimate_usd=0.0015),
        entry(cost_usd=None, cost_source="unknown"),
        entry(cost_usd=None, cost_source="local", locality="local", provider="ollama"),
    ])
    assert (estimated.cost_usd, estimated.cost_source) == (0.0015, "estimate")
    assert (unknown.cost_usd, unknown.cost_source) == (0.0, "unknown")
    assert (local.cost_usd, local.cost_source) == (0.0, "local")


def test_errors_rejections_and_legacy_entries():
    failed, rejected = intake_calls([entry(error="TimeoutError", usage=None, cost_usd=None,
                                           cost_source="unknown"),
                                     entry(rejected=True, error="InvalidEvidence")])
    assert failed.status == "error" and failed.error == "TimeoutError"
    assert rejected.detail["rejected"] is True
    assert intake_calls([{"model": "m", "latency_ms": 1}]) == []  # entries from before this change


@pytest.mark.integration
def test_submission_links_intake_calls():
    from sqlalchemy import select

    from app.config import Settings
    from app.customers.repository import ensure_customers
    from app.db.models import RunRow, TicketRow
    from app.db.session import make_engine, make_sessionmaker, reset_db
    from app.intake.db_models import IntakeSessionRow
    from app.telemetry.db_models import AiCallRow
    from app.telemetry.intake import add_intake_calls, link_intake_calls

    engine = make_engine(Settings(_env_file=None).test_database_url)
    reset_db(engine)
    sf = make_sessionmaker(engine)
    phone = "07701234567"
    with sf() as session:
        ensure_customers(session, [phone])
        intake = IntakeSessionRow(token_hash="0" * 64, customer_phone=phone, state={})
        session.add(intake)
        session.flush()
        add_intake_calls(session, intake.id, [entry()])
        ticket = TicketRow(external_id=f"INTAKE-{intake.id.hex}", channel="app", customer_phone=phone,
                           text="x", received_at=datetime.now(UTC), source="intake")
        run = RunRow(mode="jev", prompt_version="v1", model_ids={}, status="running")
        session.add_all([ticket, run])
        session.flush()
        link_intake_calls(session, intake.id, run_id=run.id, ticket_id=ticket.id)
        session.commit()
        [row] = session.scalars(select(AiCallRow)).all()
        assert (row.run_id, row.ticket_id, row.intake_session_id) == (run.id, ticket.id, intake.id)
    engine.dispose()


async def test_model_trace_entries_carry_identity_and_cost():
    from langchain_core.messages import AIMessage

    from app.config import Settings
    from app.intake.contracts import Analysis
    from app.intake.model import IntakeModel, ModelBudget
    from tests.intake.helpers import context, message

    class Runnable:
        async def ainvoke(self, messages):
            raw = AIMessage(content='ok', usage_metadata={'input_tokens': 10, 'output_tokens': 5,
                                                          'total_tokens': 15})
            parsed = Analysis(language='en', category='general_inquiry', updates=[],
                              additional_issues=[], suggested_question=None, additional_needed=[],
                              reinspect_images=[])
            return {'raw': raw, 'parsed': parsed, 'parsing_error': None}

    model = IntakeModel(Settings(_env_file=None), runnable_factory=lambda schema: Runnable())
    call = await model.analyze(context([message('hello', language='en')]), [], ModelBudget(60, 3))
    [item] = call.trace
    assert item['kind'] == 'analyze' and item['locality'] in {'cloud', 'local'}
    assert item['provider'] and item['started_at'] and item['cost_source'] in {
        'estimate', 'unknown', 'local'}
    [recorded] = intake_calls(call.trace)
    assert (recorded.input_tokens, recorded.output_tokens) == (10, 5)
