"""Guided interview over the real intake API with the scripted model."""
from __future__ import annotations

from uuid import uuid4

import pytest

from app.intake.contracts import Analysis, QuestionRecord
from tests.intake.helpers import fact

pytestmark = pytest.mark.integration

VAGUE = "حولت فلوس وما وصلت"


def user_message(turn):
    return next(item for item in reversed(turn.messages) if item.role == "user")


def opening(turn):
    source = user_message(turn)
    return Analysis(language="ar", category="failed_transfer", updates=[
        fact("issue", source.text, source),
        fact("recipient_outcome", "ما وصلت", source, normalized="no"),
    ])


def start(client, text=VAGUE):
    created = client.post("/api/intake/sessions", json={"language": "ar", "customer_phone": "07809876543"}).json()
    case = {
        "sid": created["credentials"]["session_id"],
        "headers": {"Authorization": f"Bearer {created['credentials']['token']}"},
        "view": created["session"],
    }
    send(client, case, text)
    return case


def send(client, case, text, answer_to=None, status=200):
    body = {
        "request_id": str(uuid4()), "expected_revision": case["view"]["revision"],
        "text": text, "language": "ar", "attachment_ids": [],
    }
    if answer_to is not None:
        body["answer_to"] = answer_to
    response = client.post(f"/api/intake/sessions/{case['sid']}/messages", headers=case["headers"], json=body)
    assert response.status_code == status, response.text
    if status == 200:
        case["view"] = response.json()
    return response


def analyze_calls(client):
    return sum(1 for call in client.model.calls if call[0] == "analyze")


def test_new_session_has_no_question_or_progress(intake_client):
    created = intake_client.post("/api/intake/sessions", json={"language": "ar", "customer_phone": "07809876543"}).json()
    assert created["session"]["pending_question"] is None
    assert created["session"]["progress"] == []


def test_session_exposes_the_pending_question_and_progress(intake_client):
    intake_client.model.analyses = [opening]
    view = start(intake_client)["view"]
    pending = view["pending_question"]
    assert pending == {
        "key": "amount", "message_id": view["messages"][-1]["id"], "text": "شكد المبلغ؟",
        "reason": "يساعدنا نلگه العملية.", "answer_kind": "amount", "choices": ["unknown"], "attempt": 1,
    }
    assert view["readiness"]["next_key"] == "amount"
    progress = {item["key"]: item for item in view["progress"]}
    assert list(progress) == [
        "issue", "amount", "date", "debited", "recipient_outcome", "recipient_phone", "recipient_name", "txn_ref",
    ]
    assert progress["issue"] == {"key": "issue", "tier": "required", "status": "known", "display": VAGUE}
    assert progress["recipient_outcome"]["display"] == "no"
    assert progress["amount"] == {"key": "amount", "tier": "required", "status": "missing", "display": None}
    assert progress["txn_ref"]["tier"] == "ask_once"


def test_review_has_no_pending_question(reviewed):
    assert reviewed["view"]["pending_question"] is None


def test_records_from_before_question_metadata_still_load():
    record = QuestionRecord.model_validate(
        {"key": "amount", "basis_revision": 1, "message_id": str(uuid4()), "outcome": "asked"}
    )
    assert record.reason == "" and record.attempt == 1


def opening_with_amount(turn):
    source = user_message(turn)
    return Analysis(language="ar", category="failed_transfer", updates=[
        fact("issue", source.text, source),
        fact("amount", "50000", source),
        fact("date", "2026-10-06", source),
        fact("recipient_outcome", "ما وصلت", source, normalized="no"),
    ])


def test_quick_reply_is_recorded_without_the_model(intake_client):
    intake_client.model.analyses = [opening_with_amount]
    case = start(intake_client, "حولت 50000 بتاريخ 2026-10-06 وما وصلت")
    pending = case["view"]["pending_question"]
    assert pending["key"] == "debited"
    before = analyze_calls(intake_client)
    send(intake_client, case, "اي", answer_to={"message_id": pending["message_id"], "key": "debited", "choice": "yes"})
    assert analyze_calls(intake_client) == before
    progress = {item["key"]: item for item in case["view"]["progress"]}
    assert progress["debited"]["status"] == "known"
    assert progress["debited"]["display"] == "yes"
    assert case["view"]["messages"][-2]["text"] == "اي"
    assert case["view"]["pending_question"]["key"] == "recipient_phone"


def test_quick_unknown_marks_the_detail_unknown(intake_client):
    intake_client.model.analyses = [opening]
    case = start(intake_client)
    pending = case["view"]["pending_question"]
    send(intake_client, case, "ما أعرف", answer_to={"message_id": pending["message_id"], "key": "amount", "choice": "unknown"})
    progress = {item["key"]: item for item in case["view"]["progress"]}
    assert progress["amount"]["status"] == "unknown"
    assert case["view"]["pending_question"]["key"] == "date"


def test_quick_reply_for_another_question_is_rejected(intake_client):
    intake_client.model.analyses = [opening]
    case = start(intake_client)
    pending = case["view"]["pending_question"]
    messages = len(case["view"]["messages"])
    response = send(intake_client, case, "اي", answer_to={
        "message_id": pending["message_id"], "key": "debited", "choice": "yes",
    }, status=409)
    assert response.json()["detail"]["code"] == "revision_conflict"
    stale = send(intake_client, case, "ما أعرف", answer_to={
        "message_id": str(uuid4()), "key": "amount", "choice": "unknown",
    }, status=409)
    assert stale.json()["detail"]["code"] == "revision_conflict"
    current = intake_client.get(f"/api/intake/sessions/{case['sid']}", headers=case["headers"]).json()
    assert len(current["messages"]) == messages


def test_attach_is_not_a_message_answer(intake_client):
    intake_client.model.analyses = [opening]
    case = start(intake_client)
    pending = case["view"]["pending_question"]
    send(intake_client, case, "x", answer_to={"message_id": pending["message_id"], "key": "amount", "choice": "attach"}, status=422)
