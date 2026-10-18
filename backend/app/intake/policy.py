"""Material-field readiness. Unknown answers never count as a complete report."""
from __future__ import annotations

import re

from app.intake.contracts import Fact, IntakeState, Question, Readiness
from app.taxonomy import Taxonomy

HIGH_VALUE = ("txn_ref", "exact_error", "repeats", "attempted_steps", "app_version")
PRECISE = {"amount", "customer_phone", "recipient_phone", "date", "txn_ref"}
_ALIASES = {
    "login": "login_access",
    "card": "card_issue",
    "kyc": "account_kyc",
    "fraud": "fraud_report",
    "refund": "refund_request",
}
_PROBLEMS = {
    "failed_transfer", "wrong_recipient", "agent_dispute", "bill_payment", "refund_request",
    "app_bug", "login_access", "card_issue", "account_kyc", "fraud_report",
}
_SPECIFIC = {
    "failed_transfer": ["amount", "debited", "recipient_outcome"],
    "wrong_recipient": ["amount", "recipient_phone"],
    "agent_dispute": ["amount", "agent_location"],
    "bill_payment": ["amount", "biller"],
    "refund_request": ["amount", "merchant"],
    "app_bug": ["failed_step", "device"],
    "login_access": ["failed_step"],
    "card_issue": ["card_symptom"],
    "account_kyc": ["kyc_step"],
    "fraud_report": [],
}
_SECRET = re.compile(
    r"\b(pin|otp|password|passcode|cvv|cvc)\b|رمز\s*(السر|التحقق|التأكيد)|كلمة\s*(السر|المرور)|رقم\s*البطاقة",
    re.IGNORECASE,
)
_ASK = {
    "en": {
        "issue": "What happened?",
        "actual": "What actually happened?",
        "expected": "What did you expect to happen?",
        "date": "When did this happen?",
        "amount": "What amount was involved?",
        "debited": "Was the amount taken from your wallet?",
        "recipient_outcome": "Did the other person receive the money?",
        "recipient_phone": "What number did you send the money to?",
        "customer_phone": "Which phone number is on your ZainCash account?",
        "txn_ref": "Do you have a transaction or reference number?",
        "exact_error": "What exact error appeared?",
        "failed_step": "Which step failed?",
        "device": "Which phone were you using?",
        "agent_location": "Where was the agent or shop?",
        "biller": "Which bill or company was this for?",
        "merchant": "Which shop was this?",
        "card_symptom": "What happened with the card?",
        "kyc_step": "Which verification step is stuck?",
        "desired_outcome": "What would you like us to do?",
        "attempted_steps": "What have you already tried?",
        "repeats": "Has this happened more than once?",
        "app_version": "Which app version is installed?",
        "currency": "Which currency was the amount in?",
    },
    "ar": {
        "issue": "شنو صار بالضبط؟",
        "actual": "شنو اللي صار فعلياً؟",
        "expected": "شنو كنت تتوقع يصير؟",
        "date": "متى صارت هالمشكلة؟",
        "amount": "شكد المبلغ؟",
        "debited": "انخصم المبلغ من محفظتك؟",
        "recipient_outcome": "وصلت الفلوس للشخص الثاني؟",
        "recipient_phone": "على أي رقم حولت الفلوس؟",
        "customer_phone": "شنو رقم هاتف حسابك بزين كاش؟",
        "txn_ref": "عدك رقم عملية أو مرجع؟",
        "exact_error": "شنو نص الخطأ اللي طلع؟",
        "failed_step": "بأي خطوة صار الفشل؟",
        "device": "شنو نوع الهاتف اللي تستخدمه؟",
        "agent_location": "وين موقع الوكيل أو المحل؟",
        "biller": "لفائدة أي جهة أو فاتورة؟",
        "merchant": "شنو اسم المتجر؟",
        "card_symptom": "شنو اللي صار ويا البطاقة؟",
        "kyc_step": "بأي خطوة توقف التوثيق؟",
        "desired_outcome": "شنو تحب نسوي؟",
        "attempted_steps": "شنو جربت لحد هسة؟",
        "repeats": "تكررت المشكلة أكثر من مرة؟",
        "app_version": "شنو إصدار التطبيق؟",
        "currency": "المبلغ بالدينار لو بعملة ثانية؟",
    },
}


def field_needs_question(item: Fact | None) -> bool:
    return item is None or item.status in {"missing", "conflicting"}


def field_is_resolved(item: Fact | None) -> bool:
    return item is not None and item.status in {"known", "not_applicable"}


def canonical_category(category: str) -> str:
    return _ALIASES.get(category, category)


def material_keys(category: str, taxonomy: Taxonomy | None = None) -> list[str]:
    cid = canonical_category(category)
    if cid == "general_inquiry":
        keys = ["issue"]
    elif cid == "other" or cid not in _PROBLEMS:
        keys = ["issue", "desired_outcome"]
    else:
        keys = ["issue", "actual", "expected", "date", *_SPECIFIC.get(cid, [])]
    if taxonomy is not None and cid in getattr(taxonomy, "categories", {}):
        for name in taxonomy.get(cid).required_fields:
            if name == "phone":
                if cid == "wrong_recipient":
                    keys.append("recipient_phone")
            elif name in {"date", "amount"}:
                keys.append(name)
    return list(dict.fromkeys(keys))


def asks_for_secret(text: str) -> bool:
    return _SECRET.search(text or "") is not None


def _needs_precision(item: Fact | None) -> bool:
    return item is not None and item.status == "known" and item.key in PRECISE and not item.normalized


def _asked_already(state: IntakeState, key: str) -> bool:
    asked = [item for item in state.questions if item.key == key and item.outcome == "asked"]
    if not asked:
        return False
    current = state.facts.get(key)
    # A new contradiction may be asked once more. Unchanged missing evidence is not.
    if current is not None and current.status == "conflicting":
        return len(asked) >= 2
    return True


def _question_keys(state: IntakeState, taxonomy: Taxonomy | None) -> list[str]:
    ordered = material_keys(state.category, taxonomy) + list(state.additional_needed) + list(HIGH_VALUE)
    return list(dict.fromkeys(ordered))


def _can_ask(state: IntakeState, key: str) -> bool:
    item = state.facts.get(key)
    if item is not None and item.status in {"unknown", "not_applicable"}:
        return False
    if not field_needs_question(item) and not _needs_precision(item):
        return False
    return not _asked_already(state, key)


def _fallback(state: IntakeState, key: str, revision: int) -> Question:
    language = state.language if state.language in _ASK else "ar"
    text = _ASK[language].get(key, "ممكن توضح هالنقطة أكثر؟" if language == "ar" else "Could you tell us more about this?")
    reason = "This detail is needed to understand the report." if language == "en" else "هالتفصيلة ضرورية حتى نفهم المشكلة."
    return Question(key=key, text=text, reason=reason, basis_revision=revision)


def choose_question(state: IntakeState, suggested: Question | None, revision: int, taxonomy: Taxonomy | None = None) -> Question | None:
    candidates = [key for key in _question_keys(state, taxonomy) if _can_ask(state, key)]
    if suggested is not None and suggested.key in candidates and not asks_for_secret(suggested.text):
        reason = suggested.reason.strip() or _fallback(state, suggested.key, revision).reason
        return suggested.model_copy(update={"basis_revision": revision, "reason": reason, "text": suggested.text})
    if suggested is not None and asks_for_secret(suggested.text) and suggested.key in candidates:
        return _fallback(state, suggested.key, revision)
    if not candidates:
        return None
    return _fallback(state, candidates[0], revision)


def assess_readiness(state: IntakeState, taxonomy: Taxonomy, *, allow_partial: bool = False) -> Readiness:
    keys = material_keys(state.category, taxonomy)
    missing = [key for key in keys if field_needs_question(state.facts.get(key)) or _needs_precision(state.facts.get(key))]
    conflicts = [key for key in keys if (item := state.facts.get(key)) is not None and item.status == "conflicting"]
    unknowns = [key for key in keys if (item := state.facts.get(key)) is not None and item.status == "unknown"]
    gaps = [key for key in state.additional_needed if key in HIGH_VALUE and not field_is_resolved(state.facts.get(key))]
    issues_unclear = any(item.status not in {"known", "not_applicable"} for item in state.additional_issues)
    resolved = all(
        field_is_resolved(state.facts.get(key)) and not _needs_precision(state.facts.get(key)) for key in keys
    )
    if resolved and not conflicts and not unknowns and not gaps and not issues_unclear:
        return Readiness(
            quality="sufficient_context", missing=[], conflicts=[], reason="The report has the material context.", next_key=None
        )
    askable = [key for key in list(dict.fromkeys(missing + gaps)) if _can_ask(state, key)]
    next_key = askable[0] if askable else None
    issue = state.facts.get("issue")
    exhausted = not askable
    if (exhausted or allow_partial) and field_is_resolved(issue):
        return Readiness(
            quality="partial_context",
            missing=missing,
            conflicts=conflicts,
            reason="Some details are still unknown. The customer can review what we have.",
            next_key=next_key,
        )
    return Readiness(
        quality="collecting", missing=missing, conflicts=conflicts, reason="More context is needed.", next_key=next_key
    )
