import pytest

from app.llm import LLMUnavailable
from app.pipeline.classify.cascade import combine, merge_picks
from app.pipeline.contracts import FieldPick
from tests.fakes import make_output


def test_gemini_low_confidence():
    jev = make_output(confidence=0.5, uncertain=True, reasons=("low_confidence",))
    gem = make_output(confidence=0.34, uncertain=True, source="gemini", path="gemini")
    out = combine(jev, gem, t_gem=0.66)
    assert out.path == "gemini_fallback" and out.reasons == ("low_confidence",)


def test_disagreement_when_jev_was_partly_confident():
    jev = make_output("failed_transfer", confidence=0.5, uncertain=True)
    gem = make_output("wrong_recipient", confidence=1.0, source="gemini", path="gemini")
    out = combine(jev, gem, t_gem=0.66)
    assert out.path == "disagreement" and out.reasons == ("classifier_disagreement",)
    assert out.classification.category == "wrong_recipient"


def test_gemini_wins_when_jev_was_weak():
    jev = make_output("failed_transfer", confidence=0.2, uncertain=True)
    gem = make_output("wrong_recipient", confidence=1.0, source="gemini", path="gemini")
    out = combine(jev, gem, t_gem=0.66)
    assert out.path == "gemini_fallback" and out.reasons == ()


def test_degraded_when_jev_missing():
    gem = make_output(source="gemini", path="gemini")
    out = combine(None, gem, t_gem=0.66)
    assert out.degraded and out.path == "gemini"


def test_jev_kept_when_gemini_missing():
    jev = make_output(confidence=0.5, uncertain=True, reasons=("low_confidence",))
    assert combine(jev, None, t_gem=0.66) == jev


def test_both_missing_raises():
    with pytest.raises(LLMUnavailable):
        combine(None, None, t_gem=0.66)


def test_cost_is_summed():
    jev = make_output(confidence=0.5, uncertain=True, cost=0.001)
    gem = make_output(confidence=1.0, source="gemini", cost=0.01)
    assert combine(jev, gem, t_gem=0.66).cost_usd == pytest.approx(0.011)


def test_merge_prefers_confident_jev_pick():
    jev = {"amount": FieldPick("50 الف", 0.9, "jev_pick"), "date": FieldPick("امس", 0.3, "jev_pick")}
    gem = {"amount": FieldPick("خمسين", 0.6, "gemini", "50000"), "date": FieldPick("البارحة", 0.6, "gemini")}
    merged = merge_picks(jev, gem)
    assert merged["amount"].value == "50 الف"
    assert merged["date"].value == "البارحة"
