"""Freeze a customer-approved summary without adding unsupported numbers."""
from __future__ import annotations

import re
from uuid import uuid4

from app.intake.contracts import IntakeState, ReviewSnapshot, ReviewText, TurnContext
from app.intake.dates import canonical_digits
from app.intake.errors import InvalidEvidence
from app.intake.policy import material_keys

_GROUPING = re.compile(r"(?<=\d)[,.\s\u066c\u060c](?=\d{3}(?!\d))")
_TOKEN = re.compile(r"[\w]*\d[\w:/.,+\-]*")
_LABELS = {
    "issue": "المشكلة", "actual": "ما حدث", "expected": "المتوقع", "date": "التاريخ",
    "amount": "المبلغ", "currency": "العملة", "debited": "خصم من المحفظة",
    "recipient_outcome": "وصول المبلغ", "recipient_phone": "رقم المستلم",
    "customer_phone": "رقم الزبون", "txn_ref": "رقم العملية", "exact_error": "نص الخطأ",
    "failed_step": "خطوة الفشل", "device": "الجهاز", "app_version": "إصدار التطبيق",
    "agent_location": "موقع الوكيل", "merchant": "المتجر", "biller": "الجهة",
    "card_symptom": "مشكلة البطاقة", "kyc_step": "خطوة التوثيق", "desired_outcome": "المطلوب",
    "attempted_steps": "ما تم تجريبه", "repeats": "التكرار",
}


def _compact(token: str) -> str:
    return _GROUPING.sub("", canonical_digits(token))


def _tokens(text: str) -> set[str]:
    return {_compact(token) for token in _TOKEN.findall(canonical_digits(text or ""))}


def validate_review_numbers(state: IntakeState, text: ReviewText) -> None:
    allowed: set[str] = set()
    for fact in [*state.facts.values(), *state.additional_issues]:
        for value in (fact.value, fact.normalized):
            if value:
                allowed |= _tokens(value)
    for rendered in (text.customer_text, text.employee_text_ar):
        if not _tokens(rendered).issubset(allowed):
            raise InvalidEvidence("Summary contains an unsupported identifier or number.")


def _render_value(fact) -> str:
    if fact is None or fact.status == "missing":
        return "غير متوفر"
    if fact.status == "unknown":
        return "غير معروف"
    if fact.status == "not_applicable":
        return "لا ينطبق"
    if fact.status == "conflicting":
        return f"متعارض: {fact.normalized or fact.value or 'غير معروف'}"
    if fact.key == "date" and fact.normalized:
        return fact.normalized
    return fact.normalized or fact.value or "غير معروف"


def _ticket_text(state: IntakeState, narrative: str, keys: list[str]) -> str:
    lines = [narrative.strip(), "", "التفاصيل:"]
    for key in keys:
        lines.append(f"- {_LABELS.get(key, key)}: {_render_value(state.facts.get(key))}")
    unknowns = [key for key in keys if (item := state.facts.get(key)) is None or item.status == "unknown"]
    if unknowns:
        lines.append("غير معروف:")
        lines.extend(f"- {_LABELS.get(key, key)}" for key in unknowns)
    if state.additional_issues:
        lines.append("مشاكل إضافية:")
        for issue in state.additional_issues:
            lines.append(f"- {_LABELS.get(issue.key, issue.key)}: {_render_value(issue)}")
    rendered = "\n".join(lines).strip()
    if len(rendered) > 6000:
        raise InvalidEvidence("The Arabic ticket summary is too long.")
    return rendered


def build_review(context: TurnContext, state: IntakeState, text: ReviewText, *, publication: int,
                 language: str | None = None, taxonomy=None) -> ReviewSnapshot:
    requested = language or state.language
    employee = text.employee_text_ar.strip()
    customer = text.customer_text.strip()
    if requested == "ar" and not employee:
        employee = customer
    if not customer or not employee:
        raise InvalidEvidence("The summary needs both customer and employee text.")
    checked = text.model_copy(update={"customer_text": customer, "employee_text_ar": employee})
    validate_review_numbers(state, checked)
    required = material_keys(state.category, taxonomy)
    if not set(required).issubset(set(text.fact_keys)):
        raise InvalidEvidence("The summary is missing a material detail.")
    ordered = list(dict.fromkeys([*text.fact_keys, *required]))
    quality = "sufficient_context" if state.readiness.quality == "sufficient_context" else "partial_context"
    unknowns = [key for key, fact in state.facts.items() if fact.status == "unknown"]
    attachments = [item.id for item in context.attachments if not item.removed]
    return ReviewSnapshot(
        id=uuid4(), revision=publication, language=requested, quality=quality,
        facts=dict(state.facts), additional_issues=list(state.additional_issues), unknown_keys=unknowns,
        customer_text=customer, employee_text_ar=employee,
        ticket_text_ar=_ticket_text(state, employee, ordered), attachment_ids=attachments,
    )
