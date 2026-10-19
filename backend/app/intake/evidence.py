"""Ground model proposals in the customer's own messages and screenshots."""
from __future__ import annotations

import re

from app.intake.contracts import EvidenceRef, Fact, IntakeState, TurnContext
from app.intake.dates import canonical_digits, normalize_reported_date
from app.intake.errors import InvalidEvidence
from app.intake.policy import HIGH_VALUE, field_is_resolved
from app.pipeline.stage1_normalize.candidates import normalize_phone, parse_amount

_PRECISE = {"txn_ref", "amount", "customer_phone", "recipient_phone", "exact_error", "date"}
_GROUPING = re.compile(r"(?<=\d)[,.\s\u066c\u060c](?=\d{3}(?!\d))")
_CURRENCIES = {"IQD": ("iqd", "دينار", "د.ع"), "USD": ("usd", "دولار", "$")}
_CORRECTION = re.compile(r"\b(i meant|correction|correct(?:ed|ion)?|actually|instead|not .+ but)\b|أقصد|اقصد|تصحيح|الصحيح|قصدي|مو .+ وإنما", re.I)
_OWN_PHONE = re.compile(r"\b(my|mine|own|customer)\b|رقمي|هاتفي|حسابي|رقم الزبون|رقم العميل", re.I)
_OTHER_PHONE = re.compile(r"\b(recipient|receiver|sent to|his|her|their)\b|المستلم|المستفيد|حولت للرقم|رقمه|رقمها", re.I)


def _own_phone_quote(value: str, quote: str) -> bool:
    text = _compact(quote)
    match = re.search(re.escape(value), text)
    if match is None:
        return False
    prefix = text[:match.start()]
    own = list(_OWN_PHONE.finditer(prefix))
    other = list(_OTHER_PHONE.finditer(prefix))
    return bool(own) and (not other or own[-1].start() > other[-1].start())


def _compact(value: str) -> str:
    return _GROUPING.sub("", canonical_digits(value or ""))


def _value_supported(fact: Fact, quotes: list[str]) -> bool:
    value = _compact(fact.value or "")
    # The reported value itself must be supported, never just a provider's
    # normalization. Token boundaries prevent 123 from matching 123456.
    return bool(value) and any(
        re.search(rf"(?<!\w){re.escape(value)}(?!\w)", _compact(quote), re.I)
        for quote in quotes
    )


def _check_reference(ref: EvidenceRef, messages: dict, images: dict) -> None:
    if not ref.quote.strip():
        raise InvalidEvidence("Evidence needs a quote from the customer.")
    if ref.kind == "message":
        message = messages.get(ref.source_id)
        if message is None or message.role != "user" or ref.quote not in message.text:
            raise InvalidEvidence("Evidence must quote this customer's message.")
        return
    image = images.get(ref.source_id)
    if image is None or image.removed:
        raise InvalidEvidence("Evidence must use an attached screenshot.")


def _normalize_precise(fact: Fact, messages: dict) -> Fact:
    message_refs = [ref for ref in fact.evidence if ref.kind == "message"]
    if fact.key not in _PRECISE or fact.status != "known":
        return fact
    quotes = [ref.quote for ref in fact.evidence]
    if not _value_supported(fact, quotes):
        raise InvalidEvidence("Reported value is not in the supporting text.")
    sources = [messages[ref.source_id] for ref in message_refs if ref.source_id in messages]
    source_time = max((item.created_at for item in sources), default=None)
    value = _compact(fact.value or "")
    if fact.key == "amount":
        parsed = parse_amount(value)
        if parsed is None:
            return fact.model_copy(update={"normalized": None})
        if fact.normalized and _compact(fact.normalized) != str(parsed[0]):
            raise InvalidEvidence("Normalized amount does not match the reported text.")
        return fact.model_copy(update={"normalized": str(parsed[0])})
    if fact.key in {"customer_phone", "recipient_phone"}:
        if fact.key == "customer_phone" and not any(_own_phone_quote(value, quote) for quote in quotes):
            # A bare answer to our own account-phone question is also grounded
            # in customer evidence; a recipient report alone is not.
            ordered = sorted(messages.values(), key=lambda item: item.created_at)
            own_answer = any(
                index > 0 and item in sources and not _OTHER_PHONE.search(item.text) and ordered[index - 1].role == "assistant"
                and re.search(r"your.*(?:phone|number|account)|هاتف حسابك|رقمك", ordered[index - 1].text, re.I)
                for index, item in enumerate(ordered)
            )
            if not own_answer:
                raise InvalidEvidence("Confirm which number belongs to the customer.")
        parsed = normalize_phone(value)
        if parsed is None:
            return fact.model_copy(update={"normalized": None})
        if fact.normalized and _compact(fact.normalized) != parsed:
            raise InvalidEvidence("Normalized phone does not match the reported text.")
        return fact.model_copy(update={"normalized": parsed})
    if fact.key == "date":
        parsed = normalize_reported_date(fact.value or "", source_time) if source_time else None
        if parsed is None:
            return fact.model_copy(update={"normalized": None})
        if fact.normalized and fact.normalized != parsed:
            raise InvalidEvidence("Normalized date does not match the reported text.")
        return fact.model_copy(update={"normalized": parsed})
    if fact.normalized and _compact(fact.normalized) not in _compact(" ".join(quotes)):
        raise InvalidEvidence("Normalized value is not in the supporting text.")
    return fact.model_copy(update={"normalized": canonical_digits(fact.value or "")}) if fact.key == "txn_ref" else fact


def _validate_fact(fact: Fact, messages: dict, images: dict) -> Fact:
    for ref in [*fact.evidence, *fact.supersedes]:
        _check_reference(ref, messages, images)
    if fact.status == "known":
        if not (fact.value or "").strip() or not fact.evidence:
            raise InvalidEvidence("A known fact needs a value and evidence.")
        if fact.key == "currency":
            quotes = " ".join(ref.quote for ref in fact.evidence).lower()
            value = (fact.value or "").lower()
            currencies = [key for key, tokens in _CURRENCIES.items() if any(token in value for token in tokens)]
            if len(currencies) != 1 or not any(token in quotes for token in _CURRENCIES[currencies[0]]):
                raise InvalidEvidence("Currency was not stated by the customer.")
            if fact.normalized and fact.normalized.upper() != currencies[0]:
                raise InvalidEvidence("Currency does not match the reported text.")
            return fact.model_copy(update={"normalized": currencies[0]})
        return _normalize_precise(fact, messages)
    if fact.value not in (None, "") or fact.normalized not in (None, ""):
        raise InvalidEvidence("Only known facts may carry a value.")
    if fact.status in {"unknown", "not_applicable"} and not fact.evidence:
        raise InvalidEvidence("Explain why this detail is unknown or not applicable.")
    return fact.model_copy(update={"value": None, "normalized": None})


def _newer_correction(previous: Fact, update: Fact, messages: dict) -> bool:
    if previous.value == update.value and previous.normalized == update.normalized:
        return False
    previous_ids = {ref.source_id for ref in previous.evidence if ref.kind == "message"}
    new_ids = {ref.source_id for ref in update.evidence if ref.kind == "message"}
    if not new_ids:
        return False
    previous_times = [messages[item].created_at for item in previous_ids if item in messages]
    new_times = [messages[item].created_at for item in new_ids if item in messages]
    if not new_times:
        return False
    if previous_times and max(new_times) <= max(previous_times):
        return False
    return any(_CORRECTION.search(messages[item].text) for item in new_ids - previous_ids if item in messages)


def _apply(previous: Fact | None, update: Fact, messages: dict) -> Fact:
    if previous is None or previous.status in {"missing", "unknown"}:
        return update
    if previous.status == "not_applicable" and update.status == "not_applicable":
        return previous
    if previous.value == update.value and previous.status == update.status and previous.normalized == update.normalized:
        return previous
    if update.status == "known" and _newer_correction(previous, update, messages):
        return update.model_copy(update={"supersedes": [*previous.evidence, *previous.supersedes]})
    return previous.model_copy(update={
        "status": "conflicting",
        "value": update.value or previous.value,
        "normalized": None,
        "evidence": [*previous.evidence, *update.evidence],
        "supersedes": list(previous.supersedes),
    })


def merge_analysis(context: TurnContext, analysis, *, visible_image_ids=None) -> IntakeState:
    messages = {item.id: item for item in context.messages}
    images = {item.id: item for item in context.attachments}
    visible = set(visible_image_ids) if visible_image_ids is not None else {
        aid for message in context.messages if message.id == context.current_message_id for aid in message.attachment_ids
    }
    def checked_update(update, previous):
        retained = [] if previous is None else [*previous.evidence, *previous.supersedes]
        for ref in [*update.evidence, *update.supersedes]:
            if ref.kind == "image" and ref.source_id not in visible and ref not in retained:
                raise InvalidEvidence("Read the screenshot before using new observations.")
        return _validate_fact(update, messages, images)

    facts = dict(context.state.facts)
    for update in analysis.updates:
        checked = checked_update(update, facts.get(update.key))
        facts[checked.key] = _apply(facts.get(checked.key), checked, messages)
    issues = {item.key: item for item in context.state.additional_issues}
    for issue in analysis.additional_issues:
        checked = checked_update(issue, issues.get(issue.key))
        issues[issue.key] = _apply(issues.get(issue.key), checked, messages)
    needed = [
        key for key in analysis.additional_needed
        if key in HIGH_VALUE and not field_is_resolved(facts.get(key))
    ]
    return context.state.model_copy(update={
        "language": analysis.language,
        "category": analysis.category or context.state.category,
        "facts": facts,
        "additional_issues": list(issues.values()),
        "additional_needed": needed,
    })


def remove_attachment_evidence(state: IntakeState, attachment_id) -> IntakeState:
    def strip(item: Fact) -> Fact:
        evidence = [ref for ref in item.evidence if not (ref.kind == "image" and ref.source_id == attachment_id)]
        supersedes = [ref for ref in item.supersedes if not (ref.kind == "image" and ref.source_id == attachment_id)]
        if item.evidence and not evidence:
            return item.model_copy(update={
                "status": "missing", "value": None, "normalized": None, "evidence": [], "supersedes": supersedes
            })
        return item.model_copy(update={"evidence": evidence, "supersedes": supersedes})

    facts = {key: strip(item) for key, item in state.facts.items()}
    return state.model_copy(update={
        "facts": facts,
        "additional_issues": [strip(item) for item in state.additional_issues],
        "readiness": state.readiness.model_copy(update={
            "quality": "collecting",
            "missing": [key for key, item in facts.items() if item.status in {"missing", "conflicting"}],
            "reason": "A screenshot was removed, so related details need confirmation.",
            "next_key": None,
        }),
    })
