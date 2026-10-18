import pytest

from app.config import Settings
from app.taxonomy import load_taxonomy


@pytest.fixture
def taxonomy():
    return load_taxonomy(Settings(_env_file=None).taxonomy_path)


def test_known_answer_is_not_asked_again(taxonomy):
    from app.intake.policy import assess_readiness
    from tests.intake.helpers import context, fact, message
    source = message("حولت ٥٠ ألف أمس وما وصلت")
    turn = context(
        [source],
        [fact("issue", source.text, source), fact("amount", "٥٠ ألف", source, normalized="50000")],
        category="failed_transfer",
    )
    readiness = assess_readiness(turn.state, taxonomy)
    assert "amount" not in readiness.missing
    assert readiness.quality == "collecting"


def test_unknown_material_fact_is_not_sufficient(taxonomy):
    from app.intake.contracts import EvidenceRef, Fact
    from app.intake.policy import assess_readiness
    from tests.intake.helpers import context, fact, message
    source = message("ما أعرف المبلغ")
    unknown = Fact(
        key="amount", status="unknown", value=None,
        evidence=[EvidenceRef(kind="message", source_id=source.id, quote=source.text)],
    )
    turn = context(
        [source],
        [fact("issue", source.text, source), fact("actual", source.text, source), fact("expected", source.text, source),
         fact("date", "أمس", source, normalized="2026-10-17"), fact("debited", "yes", source),
         fact("recipient_outcome", "no", source), unknown],
        category="failed_transfer",
    )
    readiness = assess_readiness(turn.state, taxonomy)
    assert readiness.quality != "sufficient_context"
    assert readiness.quality == "partial_context"


def test_conflicting_fact_stays_unresolved(taxonomy):
    from app.intake.contracts import Fact
    from app.intake.policy import assess_readiness, choose_question
    from tests.intake.helpers import context, fact, message
    source = message("المبلغ مو واضح")
    conflict = Fact(key="amount", status="conflicting", value="50000", evidence=[])
    known = [
        fact("issue", source.text, source), fact("actual", source.text, source), fact("expected", source.text, source),
        fact("date", "أمس", source, normalized="2026-10-17"), conflict,
    ]
    turn = context([source], known, category="failed_transfer")
    readiness = assess_readiness(turn.state, taxonomy)
    assert "amount" in readiness.conflicts
    assert readiness.quality != "sufficient_context"
    question = choose_question(turn.state, None, 1, taxonomy)
    assert question is not None and question.key == "amount"


def test_complete_transfer_is_sufficient(taxonomy):
    from app.intake.policy import assess_readiness
    from tests.intake.helpers import context, fact, message
    source = message("حولت 50000 أمس وانخصم وما وصل")
    keys = {
        "issue": source.text, "actual": "ما وصل", "expected": "يوصل", "date": "أمس",
        "amount": "50000", "debited": "yes", "recipient_outcome": "not received",
    }
    facts = [
        fact(key, value, source, normalized="2026-10-17" if key == "date" else "50000" if key == "amount" else None)
        for key, value in keys.items()
    ]
    readiness = assess_readiness(context([source], facts, category="failed_transfer").state, taxonomy)
    assert readiness.quality == "sufficient_context"
    assert readiness.missing == []


def test_general_inquiry_skips_incident_questions(taxonomy):
    from app.intake.policy import assess_readiness
    from tests.intake.helpers import context, fact, message
    source = message("شكد عمولة التحويل؟")
    readiness = assess_readiness(context([source], [fact("issue", source.text, source)], category="general_inquiry").state, taxonomy)
    assert readiness.quality == "sufficient_context"
    assert "amount" not in readiness.missing
    assert "date" not in readiness.missing


def test_secret_question_uses_a_safe_fallback():
    from app.intake.contracts import Question
    from app.intake.policy import choose_question
    from tests.intake.helpers import context, message
    state = context([message("The transfer failed", language="en")], category="failed_transfer").state
    suggested = Question(key="amount", text="What is your PIN?", reason="need it", basis_revision=0)
    question = choose_question(state, suggested, 2)
    assert question is not None
    assert question.key == "amount"
    assert "PIN" not in question.text
    assert "pin" not in question.text.lower()
