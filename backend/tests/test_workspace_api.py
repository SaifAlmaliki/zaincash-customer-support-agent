"""HTTP boundary tests use the real graph and test database; only model calls are faked."""
from datetime import UTC, datetime

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.engine import make_url

from app.config import Settings
from app.db.session import make_engine, make_sessionmaker, reset_db
from app.main import create_app
from app.pipeline.graph import PipelineDeps, build_graph
from app.pipeline.stage4_lookup.lookup import InMemoryTransactionRepo
from app.taxonomy import load_taxonomy
from tests.fakes import FakeClassifier, make_output

pytestmark = pytest.mark.integration


@pytest.fixture
def client():
    settings = Settings(_env_file=None, openrouter_api_key="", typesafe_api_key="")
    assert make_url(settings.test_database_url).database == "support_test"
    engine = make_engine(settings.test_database_url)
    reset_db(engine)

    def pipeline(_settings, _mode, _repo):
        return build_graph(PipelineDeps(
            taxonomy=load_taxonomy(settings.taxonomy_path),
            txn_repo=InMemoryTransactionRepo([]),
            jev=FakeClassifier(make_output("general_inquiry", priority="P4"), fail_for={"fail"}),
        ))

    with TestClient(create_app(settings, session_factory=make_sessionmaker(engine),
                               pipeline_builder=pipeline)) as test_client:
        yield test_client
    engine.dispose()


def start_run(client, tickets=None):
    response = client.post("/api/runs", json={"tickets": tickets or [
        {"external_id": "case-1", "text": "شكد عمولة التحويل؟",
         "received_at": datetime.now(UTC).isoformat()},
    ]})
    assert response.status_code == 202, response.text
    return response.json()["id"]


def test_batch_and_queue_expose_real_results(client):
    run_id = start_run(client)
    run = client.get(f"/api/runs/{run_id}").json()
    assert run["status"] == "completed"
    assert run["mode"] == "jev"
    assert run["processed"] == run["total"] == 1
    result = client.get("/api/results").json()["items"][0]
    assert result["category"] == "general_inquiry"
    assert result["category_confidence"] == 0.9
    assert result["draft_text"] is None
    detail = client.get(f"/api/results/{result['id']}").json()
    assert detail["ticket"]["text"] == "شكد عمولة التحويل؟"
    assert any(event["node"] == "prepare" for event in detail["agent_trace"])
    assert client.get("/api/results/99999").status_code == 404


def test_result_list_paginates_filters_and_run_id(client):
    first_run = start_run(client, [
        {"external_id": "needle-a", "text": "needle alpha"},
        {"external_id": "needle-b", "text": "needle beta"},
        {"external_id": "other", "text": "unrelated"},
    ])
    second_run = start_run(client, [{"external_id": "second-run", "text": "needle second"}])
    assert second_run != first_run
    query = (
        f"/api/results?run_id={first_run}&status=pending_review&team=General%20Care"
        "&category=general_inquiry&priority=P4&q=needle&offset=1&limit=1"
    )
    page = client.get(query).json()
    assert page["total"] == 2
    assert len(page["items"]) == 1
    assert page["items"][0]["run_id"] == first_run
    assert "needle" in page["items"][0]["ticket"]["text"]
    empty = client.get(query.replace("offset=1", "offset=99")).json()
    assert empty == {"items": [], "total": 2}


def test_result_list_uses_count_page_and_no_intake_query(client):
    from sqlalchemy import event

    start_run(client)
    engine = client.app.state.session_factory.kw["bind"]
    statements = []

    def observe(_conn, _cursor, statement, _parameters, _context, _many):
        statements.append(statement)

    event.listen(engine, "before_cursor_execute", observe)
    try:
        response = client.get("/api/results?offset=0&limit=1")
        assert response.status_code == 200, response.text
    finally:
        event.remove(engine, "before_cursor_execute", observe)
    assert len([sql for sql in statements if "ticket_results" in sql]) == 2
    assert not [sql for sql in statements if "intake_submissions" in sql]


def test_review_requires_text_and_rejects_stale_updates(client):
    start_run(client)
    result = client.get("/api/results").json()["items"][0]
    url = f"/api/results/{result['id']}/reviews"
    request = {"action": "approve", "reviewer": "Reviewer", "final_text": "  ",
               "expected_updated_at": result["updated_at"]}
    assert client.post(url, json=request).status_code == 422
    request["final_text"] = "هلا بيك، نراجع استفسارك ونرجعلك بالتفاصيل."
    saved = client.post(url, json=request)
    assert saved.status_code == 200, saved.text
    assert saved.json()["status"] == "approved"
    assert saved.json()["final_text"] == request["final_text"]
    assert saved.json()["draft_text"] is None
    assert len(saved.json()["reviews"]) == 1
    assert client.post(url, json=request).status_code == 409


def review_payload(result, **updates):
    payload = {
        "action": "approve",
        "reviewer": "Reviewer",
        "final_text": "هلا بيك، نراجع استفسارك.",
        "expected_updated_at": result["updated_at"],
    }
    payload.update(updates)
    return payload


def test_review_missing_stale_and_team_errors_keep_http_contract(client):
    missing = {
        "action": "approve", "reviewer": "Reviewer", "final_text": "رد",
        "expected_updated_at": datetime.now(UTC).isoformat(),
    }
    response = client.post("/api/results/99999/reviews", json=missing)
    assert response.status_code == 404
    assert response.json()["detail"] == "Ticket result not found."

    start_run(client)
    result = client.get("/api/results").json()["items"][0]
    url = f"/api/results/{result['id']}/reviews"
    stale = review_payload(result, expected_updated_at="2000-01-01T00:00:00+00:00")
    response = client.post(url, json=stale)
    assert response.status_code == 409
    assert response.json()["detail"] == "This ticket was updated by another reviewer. Refresh before saving."

    invalid_team = review_payload(result, action="reassign", team="Not a team", final_text=None)
    response = client.post(url, json=invalid_team)
    assert response.status_code == 422
    assert response.json()["detail"] == "Select a valid support team."


@pytest.mark.parametrize("status,message", [
    ("processing", "This ticket is still processing."),
    ("failed", "Processing failed. Run the ticket again before reviewing it."),
])
def test_review_state_errors_keep_http_contract(client, status, message):
    from app.db.models import TicketResultRow

    start_run(client)
    result = client.get("/api/results").json()["items"][0]
    with client.app.state.session_factory.begin() as session:
        session.get(TicketResultRow, result["id"]).status = status
    current = client.get(f"/api/results/{result['id']}").json()
    response = client.post(f"/api/results/{result['id']}/reviews", json=review_payload(current))
    assert response.status_code == 409
    assert response.json()["detail"] == message


def test_batch_failure_is_isolated_and_conflicting_ids_rejected(client):
    run_id = start_run(client, [{"external_id": "ok", "text": "مرحبا"},
                                {"external_id": "fail", "text": "سؤال"}])
    run = client.get(f"/api/runs/{run_id}").json()
    assert run["status"] == "completed_with_errors"
    assert run["processed"] == 2
    assert run["counts"]["by_status"]["failed"] == 1
    response = client.post("/api/runs", json={"mode": "jev", "tickets": [
        {"external_id": "ok", "text": "different content"},
    ]})
    assert response.status_code == 409


def test_health_does_not_expose_secrets_and_empty_batch_is_rejected(client):
    health = client.get("/api/health")
    assert health.status_code == 200
    assert "openrouter_api_key" not in health.json()
    assert health.json()["capabilities"]["drafting"] is False
    assert client.post("/api/runs", json={"mode": "jev", "tickets": []}).status_code == 422


def test_documents_are_stored_once_and_not_claimed_indexed(client):
    file = {"file": ("policy.md", b"# Fictional support policy\nContact support.", "text/markdown")}
    first = client.post("/api/knowledge", files=file)
    assert first.status_code == 200, first.text
    assert first.json()["status"] == "awaiting_indexing"
    second = client.post("/api/knowledge", files=file)
    assert second.json()["id"] == first.json()["id"]
    assert len(client.get("/api/knowledge").json()) == 1
    assert client.post("/api/knowledge", files={"file": ("bad.exe", b"binary")}).status_code == 422
    doc_id = first.json()["id"]
    assert client.get(f"/api/knowledge/{doc_id}/download").content.startswith(b"# Fictional")
    assert client.delete(f"/api/knowledge/{doc_id}").status_code == 204
    assert client.get("/api/knowledge").json() == []


def test_concurrent_conflicting_insert_is_rechecked_after_upsert(client, monkeypatch):
    from dataclasses import replace

    from app.api import runs
    from app.db.repository import upsert_tickets

    def racing_upsert(session, tickets, **kwargs):
        # Another request commits between this request's initial SELECT and INSERT.
        with client.app.state.session_factory() as competitor:
            upsert_tickets(competitor, [replace(tickets[0], text="Different winning message")], source="upload")
            competitor.commit()
        return upsert_tickets(session, tickets, **kwargs)

    monkeypatch.setattr(runs, "upsert_tickets", racing_upsert)
    response = client.post("/api/runs", json={"mode": "jev", "tickets": [
        {"external_id": "race-id", "text": "Original losing message"},
    ]})
    assert response.status_code == 409
    assert client.get("/api/runs").json() == []


def test_progress_counts_only_durable_results_after_save_failure(client, monkeypatch):
    from app.services import batch_jobs

    save_outcomes = batch_jobs.save_outcomes

    def fail_one_save(session, run_id, outcomes):
        if outcomes[0].ticket.external_id == "db-fail":
            raise RuntimeError("Simulated persistence failure")
        return save_outcomes(session, run_id, outcomes)

    monkeypatch.setattr(batch_jobs, "save_outcomes", fail_one_save)
    run_id = start_run(client, [{"external_id": "db-fail", "text": "رسالة أولى"},
                                {"external_id": "durable", "text": "رسالة ثانية"}])
    run = client.get(f"/api/runs/{run_id}").json()
    assert run["status"] == "failed"
    assert run["processed"] == run["counts"]["total"] == 1
    assert sum(run["counts"]["by_status"].values()) == 1
    assert run["total"] == 2


def test_only_jev_mode_is_configured_and_retired_modes_are_rejected(client):
    client.app.state.settings = Settings(_env_file=None, openrouter_api_key="test-router-secret",
                                         typesafe_api_key="test-jev-secret")
    client.app.state.testing_pipeline = False
    health = client.get("/api/health")
    assert health.json()["configured_modes"] == ["jev"]
    assert "test-router-secret" not in health.text and "test-jev-secret" not in health.text
    response = client.post("/api/runs", json={"mode": "gemini", "tickets": [
        {"external_id": "retired-mode", "text": "شكد عمولة التحويل؟"},
    ]})
    assert response.status_code == 422


def test_api_reports_missing_typesafe_key(client):
    client.app.state.testing_pipeline = False
    response = client.post("/api/runs", json={"mode": "jev", "tickets": [
        {"external_id": "missing-key", "text": "مرحبا"},
    ]})
    assert response.status_code == 503
    assert "TYPESAFE_API_KEY" in response.json()["detail"]
