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
