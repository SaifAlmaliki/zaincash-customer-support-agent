"""Field plan, question choice and readiness. Unknown answers never count as a complete report."""
from __future__ import annotations

import re

from app.intake.contracts import (
    AnswerKind,
    AskedQuestion,
    Choice,
    Fact,
    IntakeState,
    Message,
    PendingQuestion,
    ProgressItem,
    Question,
    Readiness,
)
from app.intake.dates import canonical_digits
from app.taxonomy import Taxonomy

HIGH_VALUE = ("txn_ref", "exact_error", "repeats", "attempted_steps", "app_version")
PRECISE = {"amount", "recipient_phone", "sender_phone", "date", "txn_ref"}
# These describe a transfer the customer sent. They do not apply when the customer received the money.
_OUTBOUND_ONLY = {"recipient_phone", "recipient_name", "debited", "recipient_outcome"}
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
    "amount": "amount", "recipient_phone": "phone", "sender_phone": "phone",
    "txn_ref": "reference", "date": "date",
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
# A transfer the customer received. "ما وصلني" means it did not arrive, so it is not incoming.
_MONEY = re.compile(r"تحويل|فلوس|مبلغ|دينار|دولار|حوالة|transfer|money|dinar", re.IGNORECASE)
_OUTBOUND_ACT = re.compile(r"حولت|دزيت|أرسلت|ارسلت|\bI\s+sent\b|\bI\s+transferred\b", re.IGNORECASE)
_INCOMING = re.compile(
    r"(?<!ما\s)(?<!ما)(?:وصلني|استلمت|جاني|جاءني|جايني)"
    r"|ما\s*[^\s]{0,3}عرف\s*(?:منو\s*)?المرسل"
    r"|unknown sender|don'?t know (?:the )?sender|don'?t know who sent"
    r"|received (?:a )?(?:transfer|money)|someone sent me",
    re.IGNORECASE,
)
_UNKNOWN_SENDER = re.compile(
    r"ما\s*[^\s]{0,3}عرف\s*(?:منو\s*)?المرسل|unknown sender|don'?t know (?:the )?sender|don'?t know who sent",
    re.IGNORECASE,
)
_SENDER_FRAMED = re.compile(
    r"حولت|دزيت|أرسلت|ارسلت|did you send|you send the money|number did you send",
    re.IGNORECASE,
)
_MOBILE = re.compile(r"(?<!\d)07\d{9}(?!\d)")
_INBOUND_ASK = {
    "en": {
        "sender_phone": "Which number did this money come from?",
        "unknown_sender": "You received money and don't know who sent it. What would you like us to do?",
        "desired_outcome": "What would you like us to do about the transfer you received?",
    },
    "ar": {
        "sender_phone": "من أي رقم وصلتك الفلوس؟",
        "unknown_sender": "وصلتلك فلوس وما تعرف المرسل. شنو تحب نسوي بيها؟",
        "desired_outcome": "شنو تحب نسوي بالتحويل اللي وصلك؟",
    },
}
_INBOUND_WHY = {
    "en": {
        "sender_phone": "It helps us find who sent the transfer.",
        "desired_outcome": "So we can identify the sender or report the transfer.",
    },
    "ar": {
        "sender_phone": "حتى نعرف منو اللي دز التحويل.",
        "desired_outcome": "حتى نعرف إذا تريد نحدد المرسل أو نبلغ عن التحويل.",
    },
}


def field_needs_question(item: Fact | None) -> bool:
    return item is None or item.status in {"missing", "conflicting"}


def field_is_resolved(item: Fact | None) -> bool:
    return item is not None and item.status in {"known", "not_applicable"}


def _grounded_text(state: IntakeState) -> str:
    parts: list[str] = []
    for item in [*state.facts.values(), *state.additional_issues]:
        if item.key == "customer_phone":
            continue
        if item.value:
            parts.append(item.value)
        parts.extend(ref.quote for ref in item.evidence if ref.quote)
    return "\n".join(parts)


def customer_received_money(state: IntakeState) -> bool:
    """The customer is the recipient. Outbound reports such as 'حولت وما وصلت' stay outbound."""
    text = _grounded_text(state)
    if not text or _OUTBOUND_ACT.search(text) or not _MONEY.search(text):
        return False
    return _INCOMING.search(text) is not None


def _unknown_sender(state: IntakeState) -> bool:
    return _UNKNOWN_SENDER.search(_grounded_text(state)) is not None


def _sender_number_stated(state: IntakeState) -> bool:
    item = state.facts.get("sender_phone")
    if item is not None and item.status in {"known", "unknown", "not_applicable"}:
        return True
    text = canonical_digits(_grounded_text(state))
    own = state.facts.get("customer_phone")
    own_number = canonical_digits((own.normalized or own.value or "") if own is not None else "")
    if own_number:
        text = text.replace(own_number, " ")
    return _MOBILE.search(text) is not None


def interview_plan(state: IntakeState, taxonomy: Taxonomy | None = None) -> tuple[list[str], list[str]]:
    required = list(material_keys(state.category, taxonomy))
    optional = list(ask_once_keys(state.category))
    if not customer_received_money(state):
        return required, optional
    required = [key for key in required if key not in _OUTBOUND_ONLY]
    optional = [key for key in optional if key not in _OUTBOUND_ONLY]
    if not _sender_number_stated(state) and "sender_phone" not in required:
        if "desired_outcome" in required:
            required.insert(required.index("desired_outcome"), "sender_phone")
        else:
            required.append("sender_phone")
    if "desired_outcome" not in required:
        required.append("desired_outcome")
    return list(dict.fromkeys(required)), list(dict.fromkeys(key for key in optional if key not in required))


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
    required, optional = interview_plan(state, taxonomy)
    inbound = customer_received_money(state)
    extra = [
        key for key in state.additional_needed
        if key in HIGH_VALUE and not (inbound and key in _OUTBOUND_ONLY)
    ]
    return [key for key in dict.fromkeys([*optional, *extra]) if key not in set(required)]


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
    required, _ = interview_plan(state, taxonomy)
    return REQUIRED_ASKS if key in required else OPTIONAL_ASKS


def _can_ask(state: IntakeState, key: str, taxonomy: Taxonomy | None = None) -> bool:
    item = state.facts.get(key)
    if item is not None and item.status in {"unknown", "not_applicable"}:
        return False
    if not field_needs_question(item) and not _needs_precision(item):
        return False
    return asked_count(state, key) < _limit(state, key, taxonomy)


def _candidates(state: IntakeState, taxonomy: Taxonomy | None) -> list[str]:
    required, _ = interview_plan(state, taxonomy)
    keys = list(dict.fromkeys([*required, *optional_keys(state, taxonomy)]))
    # First asks come before any re-ask; plan order is kept inside each round.
    return sorted((key for key in keys if _can_ask(state, key, taxonomy)), key=lambda key: asked_count(state, key))


def _language(state: IntakeState) -> str:
    return state.language if state.language in _ASK else "ar"


def _question(key: str, text: str, reason: str, revision: int, attempt: int) -> AskedQuestion:
    return AskedQuestion(
        key=key, text=text, reason=reason, basis_revision=revision,
        answer_kind=answer_kind(key), choices=answer_choices(key), attempt=attempt,
    )


def _inbound_wording(state: IntakeState, key: str, language: str) -> tuple[str, str] | None:
    if not customer_received_money(state):
        return None
    if key == "sender_phone":
        return _INBOUND_ASK[language]["sender_phone"], _INBOUND_WHY[language]["sender_phone"]
    if key == "desired_outcome":
        variant = "unknown_sender" if _unknown_sender(state) else "desired_outcome"
        return _INBOUND_ASK[language][variant], _INBOUND_WHY[language]["desired_outcome"]
    return None


def _template(state: IntakeState, key: str, revision: int, attempt: int, *, reword: bool) -> AskedQuestion:
    language = _language(state)
    generic_text, generic_reason = _GENERIC[language]
    inbound = _inbound_wording(state, key, language)
    if inbound is not None:
        text, reason = inbound
    else:
        text = _ASK[language].get(key, generic_text)
        reason = _WHY[language].get(key, generic_reason)
    if reword and attempt > 1:
        text = _REASK[language] + text
    return _question(key, text, reason, revision, attempt)


def choose_question(state: IntakeState, suggested: Question | None, revision: int,
                    taxonomy: Taxonomy | None = None) -> AskedQuestion | None:
    candidates = _candidates(state, taxonomy)
    if not candidates:
        return None
    current_round = asked_count(state, candidates[0])
    eligible = [key for key in candidates if asked_count(state, key) == current_round]
    suggestion_fits = (
        suggested is not None
        and suggested.key in eligible
        and not (
            customer_received_money(state)
            and (suggested.key in _OUTBOUND_ONLY or _SENDER_FRAMED.search(suggested.text or "") or _SENDER_FRAMED.search(suggested.reason or ""))
        )
    )
    if suggestion_fits and suggested is not None:
        if asks_for_secret(suggested.text):
            return _template(state, suggested.key, revision, current_round + 1, reword=True)
        fallback = _template(state, suggested.key, revision, current_round + 1, reword=False)
        reason = suggested.reason.strip()
        if asks_for_secret(reason):
            reason = fallback.reason
        return _question(suggested.key, suggested.text, reason or fallback.reason, revision, current_round + 1)
    return _template(state, candidates[0], revision, current_round + 1, reword=True)


def ask_for(state: IntakeState, key: str, revision: int) -> AskedQuestion:
    """The customer chose this detail, so the ask limits do not apply."""
    return _template(state, key, revision, asked_count(state, key) + 1, reword=False)


def assess_readiness(state: IntakeState, taxonomy: Taxonomy, *, allow_partial: bool = False) -> Readiness:
    keys, _ = interview_plan(state, taxonomy)
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


def progress(state: IntakeState, taxonomy: Taxonomy | None = None) -> list[ProgressItem]:
    if not any(key != "customer_phone" for key in state.facts):
        return []
    items: list[ProgressItem] = []
    required, _ = interview_plan(state, taxonomy)
    tiers = (("required", required), ("ask_once", optional_keys(state, taxonomy)))
    for tier, keys in tiers:
        for key in keys:
            item = state.facts.get(key)
            known = item is not None and item.status == "known"
            items.append(ProgressItem(
                key=key, tier=tier, status=item.status if item is not None else "missing",
                display=(item.normalized or item.value) if known else None,
            ))
    if customer_received_money(state):
        present = {item.key for item in items}
        remembered = []
        for key in ("amount", "date", "sender_phone", "txn_ref"):
            if key in present:
                continue
            item = state.facts.get(key)
            if item is None or item.status != "known":
                continue
            remembered.append(ProgressItem(
                key=key, tier="ask_once", status="known", display=item.normalized or item.value,
            ))
        if remembered:
            index = next((i for i, item in enumerate(items) if item.status != "known"), len(items))
            items[index:index] = remembered
    return items


def pending_question(state: IntakeState, messages: list[Message], phase: str) -> PendingQuestion | None:
    if phase != "collecting" or not state.questions or not messages:
        return None
    record = state.questions[-1]
    latest = messages[-1]
    if latest.role != "assistant" or latest.id != record.message_id:
        return None
    return PendingQuestion(
        key=record.key, message_id=record.message_id, text=latest.text, reason=record.reason,
        answer_kind=answer_kind(record.key), choices=answer_choices(record.key), attempt=record.attempt,
    )
