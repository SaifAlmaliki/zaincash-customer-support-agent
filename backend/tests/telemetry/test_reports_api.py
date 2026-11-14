from datetime import UTC, datetime, timedelta

import pytest
from fastapi.testclient import TestClient

from app.config import Settings
from app.customers.repository import ensure_customers
from app.db.models import RunRow, TicketResultRow, TicketRow
from app.db.session import make_engine, make_sessionmaker, reset_db
from app.main import create_app
from app.telemetry.db_models import AiCallRow

pytestmark = pytest.mark.integration
NOW = datetime.now(UTC).replace(microsecond=0)
PHONE = "07701234567"


def call(process, model, cost, latency, *, run=None, ticket=None, status="ok", source="provider",
         provider="openrouter", locality="cloud", when=NOW - timedelta(hours=1)):
    return AiCallRow(started_at=when, process=process, provider=provider, model=model, locality=locality,
                     latency_ms=latency, input_tokens=100, output_tokens=10, cost_usd=cost,
                     cost_source=source, status=status, error=None if status == "ok" else "TimeoutError",
                     attempt=1, run_id=run, ticket_id=ticket, detail={})


@pytest.fixture
def seeded():
    settings = Settings(_env_file=None, openrouter_api_key="", typesafe_api_key="")
    engine = make_engine(settings.test_database_url)
    reset_db(engine)
    sf = make_sessionmaker(engine)
    with sf() as s:
        ensure_customers(s, [PHONE])
        run = RunRow(mode="jev", prompt_version="v1", model_ids={}, status="completed", started_at=NOW - timedelta(hours=2))
        s.add(run)
        s.flush()
        tickets = [TicketRow(external_id=f"T-{i}", channel="app", customer_phone=PHONE, text="x",
                             received_at=NOW - timedelta(hours=2), source="upload") for i in range(3)]
        s.add_all(tickets)
        s.flush()
        draft = [{"kind": "draft", "duration_ms": 1500.0}]
        results = [
            TicketResultRow(run_id=run.id, ticket_id=tickets[0].id, status="pending_review", category="failed_transfer",
                            category_probs={}, flags={}, extracted={}, escalation_reasons=[], citations=[],
                            agent_trace=draft, escalated=False, latency_ms=2000, cost_usd=0.012,
                            processed_at=NOW - timedelta(hours=1)),
            TicketResultRow(run_id=run.id, ticket_id=tickets[1].id, status="escalated", category="fraud_report",
                            category_probs={}, flags={}, extracted={}, escalation_reasons=[], citations=[],
                            agent_trace=[], escalated=True, latency_ms=6000, cost_usd=0.002,
                            processed_at=NOW - timedelta(hours=1)),
            TicketResultRow(run_id=run.id, ticket_id=tickets[2].id, status="pending_review", category="other",
                            category_probs={}, flags={}, extracted={}, escalation_reasons=[], citations=[],
                            agent_trace=[], escalated=False, latency_ms=1000, cost_usd=0.5,
                            processed_at=None),  # old result: no ledger rows, falls back to run start
        ]
        s.add_all(results)
        s.flush()
        t0, t1 = tickets[0].id, tickets[1].id
        s.add_all([
            call("intake", "google/gemini-3.8-flash", 0.004, 800, run=run.id, ticket=t0),
            call("classify", "jev-1.13.0", 0.0001, 900, run=run.id, ticket=t0, provider="typesafe", source="estimate"),
            call("draft", "anthropic/claude-sonnet-5.5", 0.010, 1200, run=run.id, ticket=t0),
            call("classify", "jev-1.13.0", 0.0001, 950, run=run.id, ticket=t1, provider="typesafe", source="estimate"),
            call("extract", "qwen3:4b", 0.0, 4000, run=run.id, ticket=t1, provider="ollama", locality="local",
                 source="local", status="error"),
            call("kb_index", "openai/text-embedding-3-small", 0.0002, 300),
            call("probe", "x/y", 0.0, 100, source="unknown"),
            call("classify", "jev-1.13.0", 9.0, 1, when=NOW - timedelta(days=30)),  # outside 7 days
        ])
        s.commit()
        ids = {"run": run.id, "results": [r.id for r in results]}
    client = TestClient(create_app(settings, session_factory=sf, pipeline_builder=lambda *a, **k: None))
    with client:
        yield client, ids
    engine.dispose()


def test_summary_totals_and_groups(seeded):
    client, _ = seeded
    data = client.get("/api/ai-usage/summary").json()
    t = data["totals"]
    assert t["calls"] == 7 and t["errors"] == 1
    assert t["cost_usd"] == pytest.approx(0.004 + 0.0001 + 0.010 + 0.0001 + 0.0002)
    assert t["unknown_cost_calls"] == 1
    assert t["tickets"] == 3
    assert t["ai_time_p50_ms"] == pytest.approx(2000)
    assert t["draft_time_p50_ms"] == pytest.approx(1500)
    processes = {g["process"]: g for g in data["by_process"]}
    assert processes["classify"]["calls"] == 2 and processes["extract"]["error_rate"] == 1.0
    assert processes["classify"]["cost_sources"] == {"estimate": 2}
    models = {g["key"]: g for g in data["by_model"]}
    assert models["ollama:qwen3:4b"]["locality"] == "local"
    assert models["typesafe:jev-1.13.0"]["processes"] == ["classify"]
    assert data["unattributed"]["calls"] == 2
    assert {g["process"] for g in data["unattributed"]["by_process"]} == {"kb_index", "probe"}
    assert sum(d["calls"] for d in data["daily"]) == 7


def test_filters(seeded):
    client, ids = seeded
    only = client.get("/api/ai-usage/summary", params={"process": "classify"}).json()
    assert only["totals"]["calls"] == 2
    local = client.get("/api/ai-usage/summary", params={"model": "ollama:qwen3:4b"}).json()
    assert local["totals"]["calls"] == 1
    run = client.get("/api/ai-usage/summary", params={"run_id": ids["run"]}).json()
    assert run["totals"]["calls"] == 5
    assert client.get("/api/ai-usage/summary", params={"process": "bogus"}).status_code == 422
    assert client.get("/api/ai-usage/summary", params={"model": "no-provider"}).status_code == 422


def test_ticket_rows_include_intake_cost(seeded):
    client, ids = seeded
    page = client.get("/api/ai-usage/tickets", params={"sort": "cost"}).json()
    assert page["total"] == 3
    first = page["items"][0]
    assert first["result_id"] == ids["results"][2] and first["detail_recorded"] is False
    t0 = next(i for i in page["items"] if i["result_id"] == ids["results"][0])
    assert t0["intake_cost_usd"] == pytest.approx(0.004)
    assert t0["total_cost_usd"] == pytest.approx(0.016)
    assert t0["cost_by_process"] == pytest.approx({"intake": 0.004, "classify": 0.0001, "draft": 0.010})
    assert (t0["ai_time_ms"], t0["draft_time_ms"], t0["intake_time_ms"]) == (2000, 1500, 800)
    by_time = client.get("/api/ai-usage/tickets", params={"sort": "time", "limit": 1}).json()
    assert by_time["items"][0]["ai_time_ms"] == 6000 and by_time["total"] == 3
    filtered = client.get("/api/ai-usage/tickets", params={"model": "ollama:qwen3:4b"}).json()
    assert [i["result_id"] for i in filtered["items"]] == [ids["results"][1]]


def test_ticket_timeline(seeded):
    client, ids = seeded
    data = client.get(f"/api/ai-usage/tickets/{ids['results'][0]}/calls").json()
    assert [c["process"] for c in data["calls"]] == ["intake", "classify", "draft"]
    assert data["result"]["external_id"] == "T-0"
    assert client.get("/api/ai-usage/tickets/999999/calls").status_code == 404


def test_empty_period_returns_empty_report(seeded):
    client, _ = seeded
    params = {"from": (NOW + timedelta(days=1)).isoformat(), "to": (NOW + timedelta(days=2)).isoformat()}
    data = client.get("/api/ai-usage/summary", params=params).json()
    assert data["totals"]["calls"] == 0 and data["totals"]["ai_time_p50_ms"] is None
    assert data["by_process"] == [] and data["daily"] == []
    assert client.get("/api/ai-usage/tickets", params=params).json() == {"items": [], "total": 0}


def test_health_reports_the_capability(seeded):
    client, _ = seeded
    assert client.get("/api/health").json()["capabilities"]["evaluation"] is True
