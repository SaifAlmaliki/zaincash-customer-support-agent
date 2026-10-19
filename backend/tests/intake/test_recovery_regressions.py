from uuid import uuid4

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import select
from sqlalchemy.exc import OperationalError

from app.intake.contracts import TurnResult
from app.intake.db_models import IntakeOperationRow
from app.intake.errors import ModelUnavailable, RevisionConflict
from app.main import create_app


def create(client):
    result = client.post("/api/intake/sessions", json={"language": "en"}).json()
    return result["session"]["id"], {"Authorization": f"Bearer {result['credentials']['token']}"}


def command(text, revision=0):
    return {"request_id": str(uuid4()), "expected_revision": revision, "text": text, "language": "en", "attachment_ids": []}


def test_original_payload_identity_survives_sanitization(intake_client):
    sid, headers = create(intake_client)
    intake_client.model.analyses = [ModelUnavailable()]
    body = command("My card number is 1234567890123456")
    first = intake_client.post(f"/api/intake/sessions/{sid}/messages", headers=headers, json=body)
    assert first.status_code == 200
    assert "1234567890123456" not in first.text
    changed = intake_client.post(f"/api/intake/sessions/{sid}/messages", headers=headers,
                                 json=body | {"text": "My card number is 9999999999993456"})
    assert changed.status_code == 409
    assert changed.json()["detail"]["code"] == "operation_conflict"


def test_receipt_reference_is_preserved(intake_client):
    sid, headers = create(intake_client)
    response = intake_client.post(f"/api/intake/sessions/{sid}/messages", headers=headers,
                                  json=command("Receipt reference 1234567890123456 failed"))
    assert "1234567890123456" in response.json()["messages"][0]["text"]


def test_superseded_failed_operation_cannot_be_retried(intake_client):
    sid, headers = create(intake_client)
    intake_client.model.analyses = [ModelUnavailable()]
    body = command("First message")
    old = intake_client.post(f"/api/intake/sessions/{sid}/messages", headers=headers, json=body).json()
    latest = intake_client.post(f"/api/intake/sessions/{sid}/messages", headers=headers,
                               json=command("What is the fee?", old["revision"])).json()
    retry = intake_client.post(f"/api/intake/sessions/{sid}/operations/{body['request_id']}/retry", headers=headers,
                              json={"expected_revision": latest["revision"]})
    assert retry.status_code == 409


def test_failed_review_retry_cannot_reopen_submitted_session(intake_client, reviewed):
    sid, headers, view = reviewed["sid"], reviewed["headers"], reviewed["view"]
    intake_client.model.reviews = [ModelUnavailable()]
    request = str(uuid4())
    failed = intake_client.post(f"/api/intake/sessions/{sid}/review", headers=headers, json={
        "request_id": request, "expected_revision": view["revision"], "allow_partial": True, "language": "ar",
    }).json()
    fresh = intake_client.post(f"/api/intake/sessions/{sid}/review", headers=headers, json={
        "request_id": str(uuid4()), "expected_revision": failed["revision"], "allow_partial": True, "language": "en",
    }).json()
    submitted = intake_client.post(f"/api/intake/sessions/{sid}/submit", headers=headers, json={
        "request_id": str(uuid4()), "expected_revision": fresh["revision"], "review_id": fresh["review"]["id"], "confirmed": True,
    })
    assert submitted.status_code == 200
    retry = intake_client.post(f"/api/intake/sessions/{sid}/operations/{request}/retry", headers=headers,
                              json={"expected_revision": fresh["revision"]})
    assert retry.status_code == 409
    assert intake_client.get(f"/api/intake/sessions/{sid}", headers=headers).json()["phase"] == "submitted"


def test_publication_failure_is_retryable_without_restart(intake_client, monkeypatch):
    sid, headers = create(intake_client)
    turns = intake_client.app.state.intake.turns
    original = turns.finish

    def fail_once(*args):
        monkeypatch.setattr(turns, "finish", original)
        raise OperationalError("commit", {}, RuntimeError("temporary"))

    monkeypatch.setattr(turns, "finish", fail_once)
    body = command("What is the fee?")
    response = intake_client.post(f"/api/intake/sessions/{sid}/messages", headers=headers, json=body)
    assert response.status_code == 200
    assert response.json()["turn_status"] == "retryable_failure"
    retried = intake_client.post(f"/api/intake/sessions/{sid}/operations/{body['request_id']}/retry", headers=headers,
                                json={"expected_revision": response.json()["revision"]})
    assert retried.json()["turn_status"] == "idle"
    assert len([m for m in retried.json()["messages"] if m["role"] == "user"]) == 1


def test_actual_app_restart_reconciles_failed_placeholder(intake_client, reviewed):
    view = reviewed["view"]
    intake_client.post(f"/api/intake/sessions/{reviewed['sid']}/submit", headers=reviewed["headers"], json={
        "request_id": str(uuid4()), "expected_revision": view["revision"], "review_id": view["review"]["id"], "confirmed": True,
    })
    app = create_app(intake_client.app.state.settings, session_factory=intake_client.factory)
    with TestClient(app) as restarted:
        result = restarted.get("/api/results").json()["items"][0]
        run = restarted.get(f"/api/runs/{result['run_id']}").json()
        assert result["status"] == "failed"
        assert run["processed"] == run["counts"]["total"] == 1
        assert run["counts"]["by_status"] == {"failed": 1}


def test_stale_attempt_audit_is_retained_once_with_attempt_identity(intake_client):
    repo, turns = intake_client.app.state.intake.repo, intake_client.app.state.intake.turns
    owner, view = repo.create("en")
    claim = turns.claim(owner, "message", uuid4(), view.revision, command("What is the fee?"))
    turns.recover_interrupted()
    fresh = turns.retry(owner, claim.request_id, repo.get(owner).revision)
    with pytest.raises(RevisionConflict):
        turns.finish(claim, TurnResult(claim.context.state, "old", None, [{"cost_usd": 0.01}]))
    turns.finish(fresh, TurnResult(fresh.context.state, "new", None, [{"cost_usd": 0.02}]))
    with intake_client.factory() as session:
        operation = session.scalar(select(IntakeOperationRow).where(IntakeOperationRow.request_id == claim.request_id))
        assert [item["attempt_id"] for item in operation.usage] == [str(claim.attempt_id), str(fresh.attempt_id)]
        assert sum(item["cost_usd"] for item in operation.usage) == 0.03
