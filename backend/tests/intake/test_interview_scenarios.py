"""The vague-to-complete transfer interview from the design, end to end."""
from __future__ import annotations

from uuid import uuid4

import pytest

from app.intake.contracts import Analysis, ReviewText
from tests.intake.helpers import fact

pytestmark = pytest.mark.integration

VAGUE = "حولت فلوس وما وصلت"
COMPLETE = "حولت 50000 دينار لعلي حسين على رقم 07701234567 بتاريخ 2026-10-06 وانقطعت من رصيدي بس ما وصلتله. رقم العملية ZC2410000123"
REQUIRED = ["issue", "amount", "date", "debited", "recipient_outcome", "recipient_phone"]


def source_of(turn):
    return next(item for item in reversed(turn.messages) if item.role == "user")


def updates(*builders):
    def analyze(turn):
        source = source_of(turn)
        return Analysis(language="ar", category="failed_transfer", updates=[build(source) for build in builders])
    return analyze


def summary(state, language):
    return ReviewText(customer_text="التحويل ما وصل للمستلم.", employee_text_ar="التحويل ما وصل للمستلم.",
                      fact_keys=[*REQUIRED, *state.facts])


class Chat:
    def __init__(self, client):
        self.client = client
        created = client.post("/api/intake/sessions", json={"language": "ar", "customer_phone": "07809876543"}).json()
        self.sid = created["credentials"]["session_id"]
        self.headers = {"Authorization": f"Bearer {created['credentials']['token']}"}
        self.view = created["session"]

    def say(self, text, answer_to=None):
        body = {"request_id": str(uuid4()), "expected_revision": self.view["revision"], "text": text,
                "language": "ar", "attachment_ids": []}
        if answer_to is not None:
            body["answer_to"] = answer_to
        response = self.client.post(f"/api/intake/sessions/{self.sid}/messages", headers=self.headers, json=body)
        assert response.status_code == 200, response.text
        self.view = response.json()
        return self.view

    def tap(self, text, choice):
        pending = self.view["pending_question"]
        return self.say(text, {"message_id": pending["message_id"], "key": pending["key"], "choice": choice})

    def asked(self):
        return self.view["pending_question"]["key"] if self.view["pending_question"] else None


def analyze_calls(client):
    return sum(1 for call in client.model.calls if call[0] == "analyze")


def test_vague_report_is_interviewed_into_a_complete_ticket(intake_client):
    intake_client.model.analyses = [
        updates(lambda s: fact("issue", s.text, s), lambda s: fact("recipient_outcome", "ما وصلت", s, normalized="no")),
        updates(lambda s: fact("amount", "50000", s)),
        updates(lambda s: fact("date", "2026-10-06", s)),
        updates(lambda s: fact("recipient_phone", "07701234567", s)),
        updates(lambda s: fact("recipient_name", "علي حسين", s)),
        updates(lambda s: fact("txn_ref", "ZC2410000123", s)),
    ]
    intake_client.model.reviews = [summary]
    chat = Chat(intake_client)
    asked = []
    chat.say(VAGUE)
    asked.append(chat.asked())
    chat.say("50000 دينار")
    asked.append(chat.asked())
    chat.say("2026-10-06")
    asked.append(chat.asked())
    chat.tap("اي", "yes")
    asked.append(chat.asked())
    chat.say("07701234567")
    asked.append(chat.asked())
    chat.say("علي حسين")
    asked.append(chat.asked())
    view = chat.say("ZC2410000123")
    assert asked == ["amount", "date", "debited", "recipient_phone", "recipient_name", "txn_ref"]
    assert analyze_calls(intake_client) == 6
    review = view["review"]
    assert review["quality"] == "sufficient_context"
    facts = review["facts"]
    assert facts["amount"]["normalized"] == "50000"
    assert facts["date"]["normalized"] == "2026-10-06"
    assert facts["debited"]["normalized"] == "yes"
    assert facts["recipient_outcome"]["normalized"] == "no"
    assert facts["recipient_phone"]["normalized"] == "07701234567"
    assert facts["recipient_name"]["value"] == "علي حسين"
    assert facts["txn_ref"]["normalized"] == "ZC2410000123"
    questions = [item["text"] for item in view["messages"] if item["role"] == "assistant"][:-1]
    assert len(questions) == len(set(questions)) == 6


def test_complete_report_goes_straight_to_review(intake_client):
    intake_client.model.analyses = [updates(
        lambda s: fact("issue", s.text, s), lambda s: fact("amount", "50000", s), lambda s: fact("date", "2026-10-06", s),
        lambda s: fact("debited", "انقطعت من رصيدي", s, normalized="yes"),
        lambda s: fact("recipient_outcome", "ما وصلتله", s, normalized="no"),
        lambda s: fact("recipient_phone", "07701234567", s), lambda s: fact("recipient_name", "علي حسين", s),
        lambda s: fact("txn_ref", "ZC2410000123", s),
    )]
    intake_client.model.reviews = [summary]
    view = Chat(intake_client).say(COMPLETE)
    assert view["review"]["quality"] == "sufficient_context"
    assert view["pending_question"] is None
    assert [item["role"] for item in view["messages"]] == ["user", "assistant"]
    assert view["messages"][-1]["text"] == "راجع التفاصيل قبل الإرسال."


def test_no_reference_number_still_gives_a_complete_report(intake_client):
    intake_client.model.analyses = [updates(
        lambda s: fact("issue", s.text, s), lambda s: fact("amount", "50000", s), lambda s: fact("date", "2026-10-06", s),
        lambda s: fact("debited", "انقطعت من رصيدي", s, normalized="yes"),
        lambda s: fact("recipient_outcome", "ما وصلتله", s, normalized="no"),
        lambda s: fact("recipient_phone", "07701234567", s), lambda s: fact("recipient_name", "علي حسين", s),
    )]
    intake_client.model.reviews = [summary]
    chat = Chat(intake_client)
    chat.say(COMPLETE.replace(" رقم العملية ZC2410000123", ""))
    assert chat.asked() == "txn_ref"
    view = chat.tap("ما عندي رقم", "unknown")
    assert view["review"]["quality"] == "sufficient_context"
    assert view["review"]["facts"]["txn_ref"]["status"] == "unknown"
    assert analyze_calls(intake_client) == 1
