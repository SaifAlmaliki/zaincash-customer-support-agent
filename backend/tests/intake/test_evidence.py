from datetime import UTC, datetime, timedelta
from uuid import uuid4

import pytest

from app.intake.contracts import Analysis, Attachment, EvidenceRef, Fact
from tests.intake.helpers import context, fact, message


def test_foreign_message_cannot_ground_fact():
    from app.intake.errors import InvalidEvidence
    from app.intake.evidence import merge_analysis
    local, foreign = message("فشل التحويل"), message("المبلغ 50000")
    proposal = Analysis(
        language="ar", category="failed_transfer", updates=[fact("amount", "50000", foreign)],
        additional_issues=[], suggested_question=None, additional_needed=[], reinspect_images=[],
    )
    with pytest.raises(InvalidEvidence):
        merge_analysis(context([local]), proposal)


def test_hallucinated_amount_normalization_is_rejected():
    from app.intake.errors import InvalidEvidence
    from app.intake.evidence import merge_analysis
    source = message("المبلغ 50000")
    bad = fact("amount", "50000", source, normalized="500000")
    proposal = Analysis(
        language="ar", category="failed_transfer", updates=[bad], additional_issues=[],
        suggested_question=None, additional_needed=[], reinspect_images=[],
    )
    with pytest.raises(InvalidEvidence):
        merge_analysis(context([source]), proposal)


def test_assistant_text_cannot_ground_a_customer_fact():
    from app.intake.errors import InvalidEvidence
    from app.intake.evidence import merge_analysis
    spoken = message("المبلغ 50000", role="assistant")
    proposal = Analysis(
        language="ar", category="other", updates=[fact("amount", "50000", spoken)],
        additional_issues=[], suggested_question=None, additional_needed=[], reinspect_images=[],
    )
    with pytest.raises(InvalidEvidence):
        merge_analysis(context([spoken]), proposal)


def test_newer_correction_replaces_and_keeps_old_evidence():
    from app.intake.evidence import merge_analysis
    first = message("المبلغ 5000", at=datetime(2026, 10, 18, 8, tzinfo=UTC))
    second = message("أقصد 50000", at=datetime(2026, 10, 18, 9, tzinfo=UTC))
    original = fact("amount", "5000", first, normalized="5000")
    corrected = fact("amount", "50000", second, normalized="50000")
    proposal = Analysis(
        language="ar", category="failed_transfer", updates=[corrected], additional_issues=[],
        suggested_question=None, additional_needed=[], reinspect_images=[],
    )
    state = merge_analysis(context([first, second], [original]), proposal)
    assert state.facts["amount"].normalized == "50000"
    assert state.facts["amount"].supersedes


def test_same_moment_disagreement_is_a_conflict():
    from app.intake.evidence import merge_analysis
    source = message("المبلغ 5000 أو 50000")
    original = fact("amount", "5000", source, normalized="5000")
    other = Fact(
        key="amount", status="known", value="50000", normalized="50000",
        evidence=[EvidenceRef(kind="message", source_id=source.id, quote="50000")],
    )
    proposal = Analysis(
        language="ar", category="failed_transfer", updates=[other], additional_issues=[],
        suggested_question=None, additional_needed=[], reinspect_images=[],
    )
    state = merge_analysis(context([source], [original]), proposal)
    assert state.facts["amount"].status == "conflicting"


def test_recipient_phone_does_not_fill_customer_phone():
    from app.intake.evidence import merge_analysis
    source = message("حولت للرقم 07701234567")
    proposal = Analysis(
        language="ar", category="wrong_recipient",
        updates=[fact("recipient_phone", "07701234567", source)],
        additional_issues=[], suggested_question=None, additional_needed=[], reinspect_images=[],
    )
    state = merge_analysis(context([source]), proposal)
    assert state.facts["recipient_phone"].normalized == "07701234567"
    assert "customer_phone" not in state.facts


def test_screenshot_removal_clears_image_only_facts():
    from app.intake.contracts import Readiness
    from app.intake.evidence import remove_attachment_evidence
    image_id = uuid4()
    source = message("خطأ بالتطبيق")
    image_fact = Fact(
        key="exact_error", status="known", value="E-12",
        evidence=[EvidenceRef(kind="image", source_id=image_id, quote="E-12")],
    )
    kept = fact("issue", source.text, source)
    state = context(
        [source], [kept, image_fact],
        attachments=[Attachment(id=image_id, filename="e.png", mime_type="image/png", size=10, width=8, height=8)],
    ).state.model_copy(update={"readiness": Readiness(quality="collecting", missing=[], conflicts=[], reason="x", next_key=None)})
    cleared = remove_attachment_evidence(state, image_id)
    assert cleared.facts["exact_error"].status == "missing"
    assert cleared.facts["exact_error"].value is None
    assert cleared.facts["issue"].status == "known"


def test_omitted_facts_are_retained():
    from app.intake.evidence import merge_analysis
    source = message("فشل التحويل")
    proposal = Analysis(
        language="en", category="general_inquiry", updates=[], additional_issues=[],
        suggested_question=None, additional_needed=["txn_ref"], reinspect_images=[],
    )
    state = merge_analysis(context([source], [fact("issue", source.text, source)], category="other"), proposal)
    assert state.facts["issue"].value == source.text
    assert state.category == "general_inquiry"
    assert state.additional_needed == ["txn_ref"]
