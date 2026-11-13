"""Field plan, question choice and readiness. Unknown answers never count as a complete report."""
from __future__ import annotations

import re

from app.intake.contracts import (
    AnswerKind,
    AskedQuestion,
    Choice,
    Fact,
    IntakeState,
    Question,
    Readiness,
)
from app.taxonomy import Taxonomy

HIGH_VALUE = ("txn_ref", "exact_error", "repeats", "attempted_steps", "app_version")
PRECISE = {"amount", "recipient_phone", "date", "txn_ref"}
REQUIRED_ASKS = 2
OPTIONAL_ASKS = 1
_ALIASES = {
    "login": "login_access",
    "card": "card_issue",
    "kyc": "account_kyc",
    "fraud": "fraud_report",
    "refund": "refund_request",
}
# category -> (required keys, ask-once keys)
_PLAN: dict[str, tuple[tuple[str, ...], tuple[str, ...]]] = {
    "failed_transfer": (
        ("issue", "amount", "date", "debited", "recipient_outcome", "recipient_phone"), ("recipient_name", "txn_ref"),
    ),
    "wrong_recipient": (("issue", "amount", "date", "recipient_phone"), ("recipient_name", "txn_ref")),
    "bill_payment": (("issue", "biller", "amount", "date"), ("txn_ref", "debited")),
    "agent_dispute": (("issue", "amount", "agent_location", "date"), ("txn_ref",)),
    "refund_request": (("issue", "merchant", "amount", "date"), ("txn_ref",)),
    "app_bug": (("issue", "failed_step", "expected"), ("exact_error", "device", "app_version")),
    "login_access": (("issue", "failed_step", "expected"), ("exact_error", "device", "app_version")),
    "card_issue": (("issue", "card_symptom", "expected"), ("exact_error",)),
    "account_kyc": (("issue", "kyc_step", "expected"), ("exact_error",)),
    "fraud_report": (("issue", "date"), ("amount", "recipient_phone", "txn_ref")),
    "general_inquiry": (("issue",), ()),
    "other": (("issue", "desired_outcome"), ()),
}
_KINDS: dict[str, AnswerKind] = {
    "debited": "yes_no", "recipient_outcome": "yes_no", "repeats": "yes_no",
    "amount": "amount", "recipient_phone": "phone", "txn_ref": "reference", "date": "date",
}
_CHOICES: dict[str, list[Choice]] = {"yes_no": ["yes", "no", "unknown"], "reference": ["unknown", "attach"]}
_SECRET = re.compile(
    r"\b(pin|otp|password|passcode|cvv|cvc)\b|card[\s-]*(number|details)|رمز\s*(السر|التحقق|التأكيد)|كلمة\s*(السر|المرور)|رقم\s*البطاقة",
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
        "recipient_name": "What is the recipient's name?",
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
        "recipient_name": "شنو اسم الشخص اللي حولتله؟",
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
_WHY = {
    "en": {
        "issue": "It helps us understand the problem.",
        "actual": "It tells us what went wrong.",
        "expected": "It tells us what should have happened.",
        "date": "It helps us find the transaction.",
        "amount": "It helps us find the transaction.",
        "debited": "It tells us whether the money left your wallet.",
        "recipient_outcome": "It tells us whether the money arrived.",
        "recipient_phone": "It helps us find the transfer.",
        "recipient_name": "It helps us confirm the right transfer.",
        "txn_ref": "It lets us find the transaction directly.",
        "exact_error": "The exact message points to the cause.",
        "failed_step": "It shows where the problem happens.",
        "device": "Some problems only happen on certain phones.",
        "agent_location": "It helps us identify the agent.",
        "biller": "It helps us find the payment.",
        "merchant": "It helps us find the payment.",
        "card_symptom": "It tells us what is wrong with the card.",
        "kyc_step": "It shows where verification stopped.",
        "desired_outcome": "It tells us how to help.",
        "attempted_steps": "It saves you repeating steps.",
        "repeats": "It shows whether the problem is ongoing.",
        "app_version": "Some problems only affect certain versions.",
        "currency": "It helps us read the amount correctly.",
    },
    "ar": {
        "issue": "حتى نفهم المشكلة.",
        "actual": "حتى نعرف شنو اللي صار غلط.",
        "expected": "حتى نعرف شنو المفروض يصير.",
        "date": "يساعدنا نلگه العملية.",
        "amount": "يساعدنا نلگه العملية.",
        "debited": "حتى نعرف إذا الفلوس طلعت من محفظتك.",
        "recipient_outcome": "حتى نعرف إذا الفلوس وصلت.",
        "recipient_phone": "يساعدنا نلگه التحويل.",
        "recipient_name": "يساعدنا نتأكد من التحويل الصحيح.",
        "txn_ref": "بيه نلگه العملية مباشرة.",
        "exact_error": "نص الخطأ يدلنا على السبب.",
        "failed_step": "حتى نعرف وين تصير المشكلة.",
        "device": "بعض المشاكل تصير بس على أجهزة معينة.",
        "agent_location": "حتى نعرف الوكيل.",
        "biller": "يساعدنا نلگه الدفعة.",
        "merchant": "يساعدنا نلگه الدفعة.",
        "card_symptom": "حتى نعرف شنو مشكلة البطاقة.",
        "kyc_step": "حتى نعرف وين وگف التوثيق.",
        "desired_outcome": "حتى نعرف شلون نساعدك.",
        "attempted_steps": "حتى ما تعيد نفس الخطوات.",
        "repeats": "حتى نعرف إذا المشكلة مستمرة.",
        "app_version": "بعض المشاكل تخص إصدارات معينة.",
        "currency": "حتى نقرأ المبلغ صح.",
    },
}
_REASK = {"en": "Just so we can complete the report: ", "ar": "بس حتى نكمل التقرير: "}
_GENERIC = {
    "en": ("Could you tell us more about this?", "This detail is needed to understand the report."),
    "ar": ("ممكن توضح هالنقطة أكثر؟", "هالتفصيلة ضرورية حتى نفهم المشكلة."),
}


def field_needs_question(item: Fact | None) -> bool:
    return item is None or item.status in {"missing", "conflicting"}


def field_is_resolved(item: Fact | None) -> bool:
    return item is not None and item.status in {"known", "not_applicable"}


def canonical_category(category: str) -> str:
    return _ALIASES.get(category, category)


def _plan(category: str) -> tuple[tuple[str, ...], tuple[str, ...]]:
    return _PLAN.get(canonical_category(category), _PLAN["other"])


def material_keys(category: str, taxonomy: Taxonomy | None = None) -> list[str]:
    cid = canonical_category(category)
    keys = list(_plan(cid)[0])
    if taxonomy is not None and cid in getattr(taxonomy, "categories", {}):
        for name in taxonomy.get(cid).required_fields:
            if name == "phone":
                if cid == "wrong_recipient":
                    keys.append("recipient_phone")
            elif name in {"date", "amount"}:
                keys.append(name)
    return list(dict.fromkeys(keys))


def ask_once_keys(category: str) -> list[str]:
    required = set(material_keys(category))
    return [key for key in _plan(category)[1] if key not in required]


def optional_keys(state: IntakeState, taxonomy: Taxonomy | None = None) -> list[str]:
    required = set(material_keys(state.category, taxonomy))
    extra = [key for key in state.additional_needed if key in HIGH_VALUE]
    return [key for key in dict.fromkeys([*ask_once_keys(state.category), *extra]) if key not in required]


def answer_kind(key: str) -> AnswerKind:
    return _KINDS.get(key, "text")


def answer_choices(key: str) -> list[Choice]:
    return list(_CHOICES.get(answer_kind(key), ["unknown"]))


def asks_for_secret(text: str) -> bool:
    return _SECRET.search(text or "") is not None


def _needs_precision(item: Fact | None) -> bool:
    return item is not None and item.status == "known" and item.key in PRECISE and not item.normalized


def asked_count(state: IntakeState, key: str) -> int:
    return sum(1 for item in state.questions if item.key == key and item.outcome == "asked")


def _limit(state: IntakeState, key: str, taxonomy: Taxonomy | None) -> int:
    item = state.facts.get(key)
    if item is not None and item.status == "conflicting":
        return REQUIRED_ASKS
    return REQUIRED_ASKS if key in material_keys(state.category, taxonomy) else OPTIONAL_ASKS


def _can_ask(state: IntakeState, key: str, taxonomy: Taxonomy | None = None) -> bool:
    item = state.facts.get(key)
    if item is not None and item.status in {"unknown", "not_applicable"}:
        return False
    if not field_needs_question(item) and not _needs_precision(item):
        return False
    return asked_count(state, key) < _limit(state, key, taxonomy)


def _candidates(state: IntakeState, taxonomy: Taxonomy | None) -> list[str]:
    keys = list(dict.fromkeys([*material_keys(state.category, taxonomy), *optional_keys(state, taxonomy)]))
    # First asks come before any re-ask; plan order is kept inside each round.
    return sorted((key for key in keys if _can_ask(state, key, taxonomy)), key=lambda key: asked_count(state, key))


def _language(state: IntakeState) -> str:
    return state.language if state.language in _ASK else "ar"


def _question(key: str, text: str, reason: str, revision: int, attempt: int) -> AskedQuestion:
    return AskedQuestion(
        key=key, text=text, reason=reason, basis_revision=revision,
        answer_kind=answer_kind(key), choices=answer_choices(key), attempt=attempt,
    )


def _template(state: IntakeState, key: str, revision: int, attempt: int, *, reword: bool) -> AskedQuestion:
    language = _language(state)
    generic_text, generic_reason = _GENERIC[language]
    text = _ASK[language].get(key, generic_text)
    if reword and attempt > 1:
        text = _REASK[language] + text
    return _question(key, text, _WHY[language].get(key, generic_reason), revision, attempt)


def choose_question(state: IntakeState, suggested: Question | None, revision: int,
                    taxonomy: Taxonomy | None = None) -> AskedQuestion | None:
    candidates = _candidates(state, taxonomy)
    if not candidates:
        return None
    current_round = asked_count(state, candidates[0])
    eligible = [key for key in candidates if asked_count(state, key) == current_round]
    if suggested is not None and suggested.key in eligible:
        if asks_for_secret(suggested.text):
            return _template(state, suggested.key, revision, current_round + 1, reword=True)
        fallback = _template(state, suggested.key, revision, current_round + 1, reword=False)
        return _question(suggested.key, suggested.text, suggested.reason.strip() or fallback.reason,
                         revision, current_round + 1)
    return _template(state, candidates[0], revision, current_round + 1, reword=True)


def ask_for(state: IntakeState, key: str, revision: int) -> AskedQuestion:
    """The customer chose this detail, so the ask limits do not apply."""
    return _template(state, key, revision, asked_count(state, key) + 1, reword=False)


def assess_readiness(state: IntakeState, taxonomy: Taxonomy, *, allow_partial: bool = False) -> Readiness:
    keys = material_keys(state.category, taxonomy)
    missing = [key for key in keys if field_needs_question(state.facts.get(key)) or _needs_precision(state.facts.get(key))]
    conflicts = [key for key in keys if (item := state.facts.get(key)) is not None and item.status == "conflicting"]
    unknowns = [key for key in keys if (item := state.facts.get(key)) is not None and item.status == "unknown"]
    optional_open = [key for key in optional_keys(state, taxonomy) if _can_ask(state, key, taxonomy)]
    issues_unclear = any(item.status not in {"known", "not_applicable"} for item in state.additional_issues)
    resolved = all(
        field_is_resolved(state.facts.get(key)) and not _needs_precision(state.facts.get(key)) for key in keys
    )
    if resolved and not conflicts and not unknowns and not optional_open and not issues_unclear:
        return Readiness(
            quality="sufficient_context", missing=[], conflicts=[], reason="The report has the material context.", next_key=None
        )
    candidates = _candidates(state, taxonomy)
    next_key = candidates[0] if candidates else None
    if (not candidates or allow_partial) and field_is_resolved(state.facts.get("issue")):
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
