"""Deterministic routing, priority overrides and escalation reasons (spec §6.4)."""
from __future__ import annotations

from collections.abc import Sequence
from dataclasses import replace

from app.pipeline.contracts import ClassifierOutput, Decision, ExtractedField, LookupResult
from app.taxonomy import Category, most_urgent

FLAG_THRESHOLD = 0.5
REASON_TEXT = {
    "low_confidence": "the classifier was not confident",
    "classifier_disagreement": "Jev and Gemini disagree on the category",
    "fraud_suspected": "possible fraud or scam",
    "multi_issue": "the ticket raises more than one issue",
    "asks_for_human": "the customer asked for a person",
    "missing_required_fields": "required details are missing",
    "txn_not_found": "no matching transaction was found",
    "txn_ambiguous": "several transactions match",
    "amount_mismatch": "the amount differs from the transaction record",
    "date_mismatch": "the date differs from the transaction record",
    "empty_ticket": "the ticket text is empty",
    "llm_unavailable": "the drafting model was unavailable",
    "draft_failed_guardrail": "the draft failed a safety check",
    "no_kb_support": "no policy document supports a reply",
}
_LOOKUP_REASONS = {
    "not_found": "txn_not_found",
    "ambiguous": "txn_ambiguous",
    "amount_mismatch": "amount_mismatch",
    "date_mismatch": "date_mismatch",
}


def note_for(reasons: Sequence[str]) -> str:
    if not reasons:
        return ""
    return "Escalated: " + "; ".join(REASON_TEXT.get(r, r) for r in reasons) + "."


def _unique(items: Sequence[str]) -> tuple[str, ...]:
    return tuple(dict.fromkeys(items))


def decide(*, category: Category, classifier: ClassifierOutput,
           extracted: dict[str, ExtractedField], lookup: LookupResult) -> Decision:
    c = classifier.classification
    flags = c.flags
    priority = c.priority
    if flags.get("fraud_suspected", 0.0) > FLAG_THRESHOLD:
        priority = "P1"
    if flags.get("money_lost", 0.0) > FLAG_THRESHOLD:
        priority = most_urgent(priority, "P2")
    priority = most_urgent(priority, category.min_priority)

    reasons = list(classifier.reasons)
    if flags.get("fraud_suspected", 0.0) > FLAG_THRESHOLD or category.id == "fraud_report":
        reasons.append("fraud_suspected")
    if flags.get("multi_issue", 0.0) > FLAG_THRESHOLD:
        reasons.append("multi_issue")
    if flags.get("asks_for_human", 0.0) > FLAG_THRESHOLD:
        reasons.append("asks_for_human")
    missing = [f for f in category.required_fields if extracted[f].value is None]
    if missing and lookup.status != "matched":
        reasons.append("missing_required_fields")
    if lookup.status in _LOOKUP_REASONS:
        reasons.append(_LOOKUP_REASONS[lookup.status])
    final = _unique(reasons)
    return Decision(category.team, priority, bool(final), final, note_for(final))


def merge_reasons(decision: Decision, extra: Sequence[str]) -> Decision:
    if not extra:
        return decision
    reasons = _unique([*decision.reasons, *extra])
    return replace(decision, escalated=True, reasons=reasons, note=note_for(reasons))


def empty_ticket_decision(other: Category) -> Decision:
    reasons = ("empty_ticket",)
    return Decision(other.team, "P4", True, reasons, note_for(reasons))
