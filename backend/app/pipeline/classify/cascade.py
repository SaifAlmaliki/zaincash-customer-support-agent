"""Pure cascade decision logic: Jev first, then Gemini when Jev is unsure, then a human (spec §6.2)."""
from __future__ import annotations

from dataclasses import replace

from app.llm import LLMUnavailable
from app.pipeline.contracts import FIELD_NAMES, ClassifierOutput, FieldPick

_EMPTY = FieldPick(None, 0.0, "none")


def merge_picks(jev: dict[str, FieldPick], gem: dict[str, FieldPick]) -> dict[str, FieldPick]:
    merged: dict[str, FieldPick] = {}
    for f in FIELD_NAMES:
        j, g = jev.get(f, _EMPTY), gem.get(f, _EMPTY)
        jev_trusted = j.method == "jev_pick" and j.confidence >= 0.5
        merged[f] = j if jev_trusted or g.value is None else g
    return merged


def combine(jev: ClassifierOutput | None, gem: ClassifierOutput | None, *, t_gem: float,
            min_jev_conf: float = 0.4) -> ClassifierOutput:
    if jev is None and gem is None:
        raise LLMUnavailable("neither Jev nor Gemini produced a classification")
    if jev is None:
        return replace(gem, path="gemini", degraded=True)
    if gem is None:
        return jev
    picks = merge_picks(jev.picks, gem.picks)
    cost = jev.cost_usd + gem.cost_usd
    g, j = gem.classification, jev.classification
    if g.category_confidence < t_gem:
        path, reasons = "gemini_fallback", ("low_confidence",)
    elif g.category != j.category and j.category_confidence >= min_jev_conf:
        path, reasons = "disagreement", ("classifier_disagreement",)
    else:
        path, reasons = "gemini_fallback", ()
    return ClassifierOutput(g, picks, path=path, reasons=reasons, cost_usd=cost)
