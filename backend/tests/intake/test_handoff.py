"""Whole intake conversations handed to the employee pipeline."""
from __future__ import annotations

from io import BytesIO
from uuid import uuid4

import pytest
from PIL import Image

from app.intake.contracts import Analysis, Question, ReviewText
from app.intake.errors import ModelUnavailable
from app.services.intake_runtime import dispatch_intake
from tests.intake.helpers import fact

pytestmark = pytest.mark.integration

_MATERIAL = ["issue", "actual", "expected", "date", "amount", "debited", "recipient_outcome"]


def _user(turn):
    return next(item for item in reversed(turn.messages) if item.role == "user")


def _opening(turn):
    source = _user(turn)
    return Analysis(
        language="en",
        category="failed_transfer",
        updates=[
            fact("issue", source.text, source),
            fact("actual", "The transfer failed", source),
            fact("expected", "I expected the money to arrive", source),
            fact("date", "", source, status="unknown"),
            fact("debited", "", source, status="unknown"),
            fact("recipient_outcome", "", source, status="unknown"),
        ],
        additional_issues=[],
        suggested_question=Question(
            key="amount",
            text="What amount was involved?",
            reason="The amount is part of this transfer report.",
            basis_revision=turn.revision,
        ),
        additional_needed=[],
        reinspect_images=[],
    )


def _amount(value):
    def analyze(turn):
        source = _user(turn)
        return Analysis(
            language="en",
            category="failed_transfer",
            updates=[fact("amount", value, source, normalized=value)],
            additional_issues=[],
            suggested_question=None,
            additional_needed=[],
            reinspect_images=[],
        )

    return analyze


def _dated(turn):
    source = _user(turn)
    return Analysis(
        language="en",
        category="failed_transfer",
        updates=[fact("date", "2026-10-17", source, normalized="2026-10-17")],
        additional_issues=[],
        suggested_question=None,
        additional_needed=[],
        reinspect_images=[],
    )


def _review(state, language):
    amount = state.facts.get("amount")
    shown = ""
    if amount is not None and amount.status == "known":
        shown = amount.normalized or amount.value or ""
    customer = f"The transfer failed. Amount {shown}." if shown else "The transfer failed."
    employee = f"فشل التحويل. المبلغ {shown}." if shown else "فشل التحويل."
    return ReviewText(customer_text=customer, employee_text_ar=employee, fact_keys=list(_MATERIAL))


def _png() -> bytes:
    buffer = BytesIO()
    Image.new("RGB", (16, 16), (220, 40, 50)).save(buffer, format="PNG")
    return buffer.getvalue()


def _message(client, case, text, attachments=()):
    response = client.post(
        f"/api/intake/sessions/{case['sid']}/messages",
        headers=case["headers"],
        json={
            "request_id": str(uuid4()),
            "expected_revision": case["view"]["revision"],
            "text": text,
            "language": "en",
            "attachment_ids": list(attachments),
        },
    )
    assert response.status_code == 200, response.text
    case["view"] = response.json()
    return case["view"]


@pytest.fixture
def complete_conversation(intake_client):
    intake_client.model.analyses = [_opening, _amount("5000"), _amount("50000"), _dated]
    intake_client.model.reviews = [_review, _review, _review, _review]
    created = intake_client.post("/api/intake/sessions", json={"language": "en"}).json()
    case = {
        "sid": created["credentials"]["session_id"],
        "headers": {"Authorization": f"Bearer {created['credentials']['token']}"},
        "view": created["session"],
    }
    uploaded = intake_client.post(
        f"/api/intake/sessions/{case['sid']}/attachments",
        headers=case["headers"],
        data={"request_id": str(uuid4()), "expected_revision": str(case["view"]["revision"])},
        files={"file": ("receipt.png", _png(), "image/png")},
    )
    assert uploaded.status_code == 201, uploaded.text
    body = uploaded.json()
    case["view"] = body["session"]
    _message(
        intake_client,
        case,
        "The transfer failed. I expected the money to arrive but it did not.",
        [body["attachment"]["id"]],
    )
    assert any(item["text"] == "What amount was involved?" for item in case["view"]["messages"])
    _message(intake_client, case, "5000")
    _message(intake_client, case, "I meant 50000 IQD")
    _message(intake_client, case, "It happened on 2026-10-17")
    assert case["view"]["review"]["facts"]["amount"]["normalized"] == "50000"
    return case


def test_review_to_employee_handoff(intake_client, complete_conversation):
    intake_client.app.state.intake_dispatcher = dispatch_intake
    assert intake_client.get("/api/results").json()["items"] == []
    view = complete_conversation["view"]
    response = intake_client.post(
        f"/api/intake/sessions/{complete_conversation['sid']}/submit",
        headers=complete_conversation["headers"],
        json={
            "request_id": str(uuid4()),
            "expected_revision": view["revision"],
            "review_id": view["review"]["id"],
            "confirmed": True,
        },
    )
    assert response.status_code == 200
    items = intake_client.get("/api/results").json()["items"]
    assert len(items) == 1
    detail = intake_client.get(f"/api/results/{items[0]['id']}").json()
    assert detail["intake"]["facts"]["amount"]["normalized"] == "50000"
    assert detail["intake"]["messages"]
    assert detail["intake"]["attachments"]
    assert detail["ticket"]["external_id"] == response.json()["ticket_reference"]
    assert detail["status"] != "processing"


def test_english_general_inquiry_asks_no_transaction_questions(intake_client):
    def analyze(turn):
        source = _user(turn)
        return Analysis(
            language="en",
            category="general_inquiry",
            updates=[fact("issue", source.text, source)],
            additional_issues=[],
            suggested_question=None,
            additional_needed=[],
            reinspect_images=[],
        )

    def review(state, language):
        issue = state.facts["issue"].value or ""
        return ReviewText(customer_text=issue, employee_text_ar=f"استفسار: {issue}", fact_keys=["issue"])

    intake_client.model.analyses = [analyze]
    intake_client.model.reviews = [review]
    created = intake_client.post("/api/intake/sessions", json={"language": "en"}).json()
    headers = {"Authorization": f"Bearer {created['credentials']['token']}"}
    response = intake_client.post(
        f"/api/intake/sessions/{created['credentials']['session_id']}/messages",
        headers=headers,
        json={
            "request_id": str(uuid4()),
            "expected_revision": created["session"]["revision"],
            "text": "What are your working hours?",
            "language": "en",
            "attachment_ids": [],
        },
    )
    assert response.status_code == 200, response.text
    view = response.json()
    asked = " ".join(item["text"] for item in view["messages"] if item["role"] == "assistant").lower()
    assert "amount" not in asked and "transaction" not in asked
    assert "amount" not in view["review"]["facts"]


def test_model_failure_retries_into_one_submission(intake_client):
    intake_client.app.state.intake_dispatcher = dispatch_intake

    def analyze(turn):
        return Analysis(
            language="en",
            category="general_inquiry",
            updates=[fact("issue", _user(turn).text, _user(turn))],
            additional_issues=[],
            suggested_question=None,
            additional_needed=[],
            reinspect_images=[],
        )

    def review(state, language):
        issue = state.facts["issue"].value or ""
        return ReviewText(customer_text=issue, employee_text_ar=issue, fact_keys=["issue"])

    intake_client.model.analyses = [ModelUnavailable("down"), analyze]
    intake_client.model.reviews = [review]
    created = intake_client.post("/api/intake/sessions", json={"language": "en"}).json()
    sid = created["credentials"]["session_id"]
    headers = {"Authorization": f"Bearer {created['credentials']['token']}"}
    request_id = str(uuid4())
    failed = intake_client.post(
        f"/api/intake/sessions/{sid}/messages",
        headers=headers,
        json={
            "request_id": request_id,
            "expected_revision": created["session"]["revision"],
            "text": "The app will not open.",
            "language": "en",
            "attachment_ids": [],
        },
    )
    assert failed.status_code == 200, failed.text
    assert failed.json()["turn_status"] == "retryable_failure"
    retried = intake_client.post(
        f"/api/intake/sessions/{sid}/operations/{request_id}/retry",
        headers=headers,
        json={"expected_revision": failed.json()["revision"]},
    )
    assert retried.status_code == 200, retried.text
    view = retried.json()
    assert view["review"]
    assert sum(item["role"] == "user" for item in view["messages"]) == 1
    submitted = intake_client.post(
        f"/api/intake/sessions/{sid}/submit",
        headers=headers,
        json={
            "request_id": str(uuid4()),
            "expected_revision": view["revision"],
            "review_id": view["review"]["id"],
            "confirmed": True,
        },
    )
    assert submitted.status_code == 200, submitted.text
    assert len(intake_client.get("/api/results").json()["items"]) == 1
