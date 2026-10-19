from datetime import UTC, datetime, timedelta
from uuid import uuid4

import pytest

from app.intake.contracts import Analysis, Attachment, EvidenceRef, Fact, Question
from app.intake.dates import normalize_reported_date
from app.intake.errors import InvalidEvidence
from app.intake.evidence import merge_analysis, remove_attachment_evidence
from app.intake.policy import choose_question
from tests.intake.helpers import context, fact, message


def proposal(*updates, issues=()):
    return Analysis(language="en", category="failed_transfer", updates=list(updates), additional_issues=list(issues))


def test_date_is_normalized_from_its_message_and_rejects_fabrication():
    source = message("It failed yesterday", at=datetime(2026, 10, 17, 21, 5, tzinfo=UTC))
    ctx = context([source])
    result = merge_analysis(ctx, proposal(fact("date", "yesterday", source)))
    assert result.facts["date"].normalized == "2026-10-17"
    with pytest.raises(InvalidEvidence):
        merge_analysis(ctx, proposal(fact("date", "yesterday", source, normalized="2026-10-18")))
    with pytest.raises(InvalidEvidence):
        merge_analysis(ctx, proposal(fact("date", "2026-09-01", source)))


@pytest.mark.parametrize("text", ["today or yesterday", "day before yesterday", "قبل أمس", "اليوم أو أمس"])
def test_ambiguous_or_modified_relative_date_is_not_guessed(text):
    assert normalize_reported_date(text, datetime(2026, 10, 18, tzinfo=UTC)) is None


def test_amount_uses_supported_value_not_first_number_in_quote():
    source = message("Reference 2410000123, amount ۵۰٬۰۰۰ IQD")
    result = merge_analysis(context([source]), proposal(fact("amount", "۵۰٬۰۰۰", source)))
    assert result.facts["amount"].normalized == "50000"


@pytest.mark.parametrize("key,value,normalized,text", [
    ("amount", "500000", "50000", "amount 50000"),
    ("txn_ref", "123", None, "reference 123456"),
    ("currency", "USD", None, "amount 50000 IQD"),
    ("customer_phone", "07701234567", None, "I sent to recipient 07701234567"),
])
def test_unrelated_or_role_swapped_precise_value_is_rejected(key, value, normalized, text):
    source = message(text)
    with pytest.raises(InvalidEvidence):
        merge_analysis(context([source]), proposal(fact(key, value, source, normalized=normalized)))


def test_later_disagreement_without_correction_remains_a_conflict():
    first = message("Amount 5000", at=datetime(2026, 10, 18, tzinfo=UTC))
    later = message("Amount 50000", at=first.created_at + timedelta(minutes=1))
    ctx = context([first, later], [fact("amount", "5000", first, normalized="5000")])
    result = merge_analysis(ctx, proposal(fact("amount", "50000", later)))
    assert result.facts["amount"].status == "conflicting"


def test_additional_issue_is_resolved_in_place_instead_of_appended():
    first = message("I do not know the second issue", at=datetime(2026, 10, 18, tzinfo=UTC))
    later = message("The second issue is a locked card", at=first.created_at + timedelta(minutes=1))
    ctx = context([first, later])
    ctx.state.additional_issues = [fact("second_issue", None, first, status="unknown")]
    result = merge_analysis(ctx, proposal(issues=[fact("second_issue", "locked card", later)]))
    assert len(result.additional_issues) == 1
    assert result.additional_issues[0].status == "known"


@pytest.mark.parametrize("status", ["unknown", "not_applicable", "conflicting"])
def test_removal_invalidates_every_image_only_fact_status(status):
    image_id = uuid4()
    item = Fact(key="amount", status=status, evidence=[EvidenceRef(kind="image", source_id=image_id, quote="unreadable")])
    state = remove_attachment_evidence(context(facts=[item]).state, image_id)
    assert state.facts["amount"].status == "missing"


def test_unseen_uploaded_image_cannot_ground_a_new_fact():
    image_id = uuid4()
    ctx = context(attachments=[Attachment(id=image_id, filename="r.png", mime_type="image/png", size=10, width=1, height=1)])
    item = Fact(key="amount", status="known", value="50000", evidence=[EvidenceRef(kind="image", source_id=image_id, quote="50000")])
    with pytest.raises(InvalidEvidence):
        merge_analysis(ctx, proposal(item))


def test_full_payment_card_question_uses_safe_fallback():
    ctx = context(category="failed_transfer")
    question = Question(key="amount", text="What is your full payment-card number?", reason="identify payment", basis_revision=0)
    result = choose_question(ctx.state, question, 1)
    assert "card" not in result.text


def test_two_phone_numbers_do_not_lose_their_roles():
    source = message("My number is 07701234567; recipient number is 07801234567")
    with pytest.raises(InvalidEvidence):
        merge_analysis(context([source]), proposal(fact("customer_phone", "07801234567", source)))
    result = merge_analysis(context([source]), proposal(fact("customer_phone", "07701234567", source)))
    assert result.facts["customer_phone"].normalized == "07701234567"
