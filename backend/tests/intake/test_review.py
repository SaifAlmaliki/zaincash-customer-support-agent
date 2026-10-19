from datetime import datetime
from uuid import uuid4
from zoneinfo import ZoneInfo

import pytest

from app.intake.contracts import ReviewText
from app.intake.errors import InvalidEvidence
from app.intake.review import build_review, validate_review_numbers
from tests.intake.helpers import context, fact, message


def test_grouped_amount_matches_canonical_digits():
    source = message("The amount is 50000", language="en")
    state = context([source], [fact("amount", "50,000", source, normalized="50000")]).state
    validate_review_numbers(state, ReviewText(
        customer_text="Amount 50,000", employee_text_ar="المبلغ 50000", fact_keys=["amount"],
    ))


def test_persian_digits_and_unsupported_number(taxonomy=None):
    source = message("المبلغ ٥٠٠٠٠", language="ar")
    state = context([source], [fact("amount", "٥٠٠٠٠", source, normalized="50000")], category="other").state
    validate_review_numbers(state, ReviewText(
        customer_text="المبلغ ۵۰۰۰۰", employee_text_ar="المبلغ 50000", fact_keys=["amount"],
    ))
    with pytest.raises(InvalidEvidence):
        validate_review_numbers(state, ReviewText(
            customer_text="المبلغ 500000", employee_text_ar="المبلغ 50000", fact_keys=["amount"],
        ))


def test_midnight_date_survives_the_arabic_summary():
    sent = datetime(2026, 10, 18, 0, 5, tzinfo=ZoneInfo("Asia/Baghdad"))
    source = message("حصل أمس", language="ar", at=sent)
    dated = fact("date", "أمس", source, normalized="2026-10-17")
    issue = fact("issue", source.text, source)
    state = context([source], [issue, dated], category="general_inquiry").state
    snapshot = build_review(context([source], [issue, dated], category="general_inquiry"), state, ReviewText(
        customer_text="حصل بتاريخ 2026-10-17", employee_text_ar="حصل بتاريخ 2026-10-17", fact_keys=["issue"],
    ), publication=2, language="ar")
    assert "2026-10-17" in snapshot.ticket_text_ar
    assert snapshot.revision == 2
    assert uuid4()


def test_review_keeps_optional_facts_and_displays_missing_material_fields():
    source = message("Reference DEMO-2410000123 failed with E-12")
    ctx = context([source], [fact("issue", "transfer failed", source), fact("txn_ref", "DEMO-2410000123", source),
                             fact("exact_error", "E-12", source)], category="failed_transfer")
    text = ReviewText(customer_text="Transfer failed", employee_text_ar="فشل التحويل",
                      fact_keys=["issue", "actual", "expected", "date", "amount", "debited", "recipient_outcome"])
    review = build_review(ctx, ctx.state, text, publication=1, language="en")
    assert "DEMO-2410000123" in review.ticket_text_ar
    assert "E-12" in review.ticket_text_ar
    assert "amount" in review.unknown_keys
    assert review.facts["amount"].status == "missing"


def test_arabic_customer_and_employee_share_one_narrative():
    source = message("لم يصل التحويل")
    ctx = context([source], [fact("issue", source.text, source)], category="general_inquiry")
    text = ReviewText(customer_text="لم يصل التحويل", employee_text_ar="وصل التحويل وتم حل المشكلة", fact_keys=["issue"])
    review = build_review(ctx, ctx.state, text, publication=1, language="ar")
    assert review.customer_text == review.employee_text_ar


def test_number_punctuation_is_not_part_of_the_value_but_reference_prefix_is():
    source = message("Amount 50000, reference DEMO-2410000123")
    state = context([source], [fact("amount", "50000", source), fact("txn_ref", "DEMO-2410000123", source)]).state
    validate_review_numbers(state, ReviewText(customer_text="Amount 50,000.", employee_text_ar="المبلغ 50000.", fact_keys=[]))
    with pytest.raises(InvalidEvidence):
        validate_review_numbers(state, ReviewText(customer_text="Reference OTHER-2410000123", employee_text_ar="المبلغ 50000", fact_keys=[]))
