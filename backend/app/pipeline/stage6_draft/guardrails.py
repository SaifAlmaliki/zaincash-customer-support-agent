"""Deterministic draft findings; these heuristics do not prove natural-language safety.

Only ticket evidence and a confirmed match ground financial facts. Retrieved
policy text grounds citations, never a customer's transaction details.
"""
from __future__ import annotations

import re
import unicodedata
from datetime import datetime
from decimal import Decimal

from app.kb.contracts import Passage
from app.pipeline.contracts import FIELD_NAMES
from app.pipeline.stage1_normalize.candidates import (
    MAX_CANDIDATES_PER_FIELD,
    find_candidates,
    normalize_phone,
    parse_amount,
)
from app.pipeline.stage1_normalize.normalize import fold_arabic, to_ascii_digits
from app.pipeline.stage3_extract.extract import normalize_value
from app.pipeline.state import PipelineState

_SECRET = re.compile(
    r"(?<!\w)(?:otp|pin|passwords?|passcodes?|one[ -]time[ -](?:password|code)"
    r"|(?:[وبفل])?(?:(?:ال)?(?:رقم|رمز)\s+(?:ال)?(?:سري|تحقق|تاكيد|دخول)"
    r"|كلم[ةه]\s+(?:ال)?(?:سر|مرور)(?:ك)?|الباسورد|باسورد|الرمز))(?!\w)",
    re.IGNORECASE,
)
_REQUEST = re.compile(
    r"(?<!\w)(?:send|share|provide|disclose|reveal|forward|give|tell|email|text|need|require"
    r"|reply\s+with|(?:[وف])?(?:[ت]?دز(?:لي|لنا|لنه)?|ارسل(?:ه|ي|وا)?"
    r"|ارسال|مشارك[ةه]|تزويد(?:نا|ني)?|تقديم"
    r"|ترسل|تشارك|شارك(?:نا)?|[نت]حتاج|زودنا|زودني|اعطنا|اعطيني|انطيني|انطينا|اكتب(?:لنا|لي)?))(?!\w)",
    re.IGNORECASE,
)
_CLAUSE = re.compile(r"[.!?؟;؛،,\n]|\b(?:but|however|بس|لكن)\b", re.IGNORECASE)
_NEGATION = re.compile(
    r"(?:\b(?:never|not|don't|dont|avoid)\s+(?:ever\s+)?(?:ask\s+you\s+to\s+)?"
    r"|(?<!\w)(?:[وف])?(?:لا|ما|مو|ممنوع|اياك|عدم|لا\s+نطلب\s+منك|نحذرك\s+من)\s+)$",
    re.IGNORECASE,
)
_COORDINATION = re.compile(r"\s*(?:or|nor|and|او|ولا|و)\s*", re.IGNORECASE)
_NEED_ACTION = re.compile(r"(?:need|require|[وف]?[نت]حتاج)", re.IGNORECASE)
_NEED_COMPLEMENT = re.compile(r"\s*(?:to|ان|الي)?\s*", re.IGNORECASE)
_NOMINAL_ACTION = re.compile(r"[وف]?(?:ارسال|مشارك[ةه]|تزويد(?:نا|ني)?|تقديم)")
_POST_PROHIBITION = re.compile(r"\s+ممنوع[ةه]?(?!\w)")
_NUMBER = r"(?:\d{1,3}(?:,\d{3})+(?:\.\d+)?|\d{1,3}(?:\.\d{3})+|\d+(?:\.\d+)?)"
_GROUPED_COMMA = re.compile(r"(?<![\w.,])\d{1,3}(?:,\d{3})+(?:\.\d+)?(?!\d)")
_PREFIX_CURRENCY = re.compile(r"\b(IQD|USD)\s+(" + _NUMBER + r")(?!\w)", re.IGNORECASE)
_SMALL_AMOUNT = re.compile(
    r"(?<!\w)(?:(?:[وب])?(?:ال)?مبلغ|(?:ال)?رسوم|(?:ال)?قيم[ةه]|amount|fee)"
    r"\s*(?:الحوال[ةه]\s*)?[:=]?\s*(" + _NUMBER + r")(?!\w|[.,]\d)", re.IGNORECASE,
)
_CURRENCY_SUFFIX = re.compile(r"\s+(?:دولار|USD|دينار|IQD|د\.ع)(?!\w)", re.IGNORECASE)
_UNIT_SUFFIX = re.compile(
    r"\s*(?:الف|الاف|مليون|دينار|دنانير|دولار|IQD|USD|million|alf|dinar|k|د\.ع)(?!\w)",
    re.IGNORECASE,
)
_REFERENCE_SHAPE = re.compile(r"(?<![a-z0-9])zc[\s-]?\d+[a-z0-9]*", re.IGNORECASE)
_DOTTED_DATE = re.compile(r"(?<![\d.])(\d{1,2})\.(\d{1,2})\.(\d{4})(?!\d)")
_YEAR_FIRST_DATE = re.compile(r"(?<![\d/])(\d{4})/(\d{1,2})/(\d{1,2})(?!\d)")


def _normalized(text: str) -> str:
    return fold_arabic(to_ascii_digits(unicodedata.normalize("NFKC", text))).translate(
        str.maketrans({"٬": ",", "٫": ".", "’": "'"})
    )


def requests_credentials(reply: str) -> bool:
    """Recognize common Arabic/Iraqi/English disclosure requests, with local negation.

    Each action gets its own negation scope: a warning cannot excuse the next
    request, even if punctuation is absent. Jev supplies complementary review.
    """
    for clause in _CLAUSE.split(_normalized(reply)):
        actions = list(_REQUEST.finditer(clause))
        previous_negated = False
        for index, action in enumerate(actions):
            previous_end = actions[index - 1].end() if index else 0
            next_start = actions[index + 1].start() if index + 1 < len(actions) else len(clause)
            before = clause[previous_end:action.start()]
            after = clause[action.end():next_start]
            secret = _SECRET.search(after)
            # A nominal action can be prohibited after its object. Bind the
            # prohibition to that secret, never to another action later on.
            prohibited = (
                _NOMINAL_ACTION.fullmatch(action[0]) and secret
                and _POST_PROHIBITION.match(after, secret.end())
            )
            negated = bool(_NEGATION.search(before) or prohibited)
            if index and previous_negated:
                # Share negation only across a bare coordinating link or a
                # negated need's complement. An intervening object/new clause
                # ends that scope: "Never share PIN and send OTP" is unsafe.
                coordinated = _COORDINATION.fullmatch(before) or (
                    not before.strip() and action[0].startswith("و")
                )
                indirect = _NEED_ACTION.fullmatch(actions[index - 1][0]) and (
                    _NEED_COMPLEMENT.fullmatch(before)
                )
                negated = negated or bool(coordinated or indirect)
            previous_negated = negated
            if negated:
                continue
            # A preposed secret belongs only to the first action, not to a later
            # unrelated request ("Never share PIN and send the transaction ref").
            if secret or (index == 0 and _SECRET.search(before)):
                return True
    return False


def _reply_findings(reply: str) -> list[str]:
    if not reply.strip():
        return ["empty_reply"]
    findings = []
    letters = [c for c in reply if c.isalpha()]
    arabic = sum(unicodedata.name(c, "").startswith("ARABIC") for c in letters)
    if not letters or arabic / len(letters) < 0.5:
        findings.append("non_arabic_reply")
    if len(reply.split()) > 120:
        findings.append("reply_too_long")
    return findings


def _citation_findings(citations: list[str], retrieved: dict[str, Passage]) -> list[str]:
    if not citations:
        return ["missing_citations"]
    return ["invalid_citations"] if any(c not in retrieved for c in citations) else []


def _exact_amount(span: str) -> tuple[Decimal, str]:
    """Reuse the unit/currency parser without rounding away fractional claims."""
    number = re.search(_NUMBER, span)
    raw = number[0].replace(",", "")
    if re.fullmatch(r"\d{1,3}(?:\.\d{3})+", raw):
        raw = raw.replace(".", "")
    multiplier, currency = parse_amount(span[:number.start()] + "1" + span[number.end():])
    value = Decimal(raw) * multiplier
    if span.lstrip().startswith("-"):
        value = -value
    return value, currency


def _values(text: str, received_at: datetime) -> dict[str, set[tuple]]:
    text = _normalized(text)
    text = _DOTTED_DATE.sub(r"\1/\2/\3", text)
    text = _YEAR_FIRST_DATE.sub(r"\1-\2-\3", text)
    text = _GROUPED_COMMA.sub(lambda m: m[0].replace(",", ""), text)
    # Extend the existing suffix parser to common currency-prefix and small
    # explicitly labelled amounts. Neither transform treats numbered steps as money.
    text = _PREFIX_CURRENCY.sub(lambda m: f"{m[2]} {m[1]}", text)
    text = _SMALL_AMOUNT.sub(
        lambda m: m[0] + " دينار"
        if parse_amount(m[1])[0] < 250 and not _UNIT_SUFFIX.match(text, m.end()) else m[0],
        text,
    )
    values: dict[str, set[tuple]] = {name: set() for name in FIELD_NAMES}
    for reference in _REFERENCE_SHAPE.finditer(text):
        values["txn_ref"].add(normalize_value("txn_ref", reference[0], None, received_at))
    for name in FIELD_NAMES:
        remaining = text
        while remaining:
            candidates = find_candidates(remaining).for_field(name)
            if not candidates:
                break
            if name == "amount":
                # Classification deduplicates raw spans (e.g. "50 الف") before
                # currency suffix/sign enrichment. Consume only its first hit,
                # then rescan after that occurrence so later variants survive.
                candidates = candidates[:1]
            for candidate in candidates:
                span = candidate.span
                if name == "amount":
                    if suffix := _CURRENCY_SUFFIX.match(remaining, candidate.end):
                        span += suffix[0]
                    if candidate.start and remaining[candidate.start - 1] == "-":
                        span = "-" + span
                    values[name].add(_exact_amount(span))
                else:
                    values[name].add(normalize_value(name, span, None, received_at))
            if name != "amount" and len(candidates) < MAX_CANDIDATES_PER_FIELD:
                break
            # Candidate limits protect classifier prompts, not this validation.
            remaining = remaining[candidates[-1].end:]
    return values


def _grounding_findings(reply: str, used_txn_ref: str | None, state: PipelineState) -> list[str]:
    ticket = state["ticket"]
    received_at = ticket.received_at
    evidence = _values(ticket.text, received_at)
    if phone := normalize_phone(ticket.customer_phone or ""):
        evidence["phone"].add((phone, None))
    # Extraction can resolve word amounts/dates the numeric candidate finder cannot.
    # Require its original span anchor before trusting that normalized hint.
    for name, field in state.get("extracted", {}).items():
        if (name not in evidence or field.value is None or not field.span
                or field.start is None or field.end is None or field.start < 0):
            continue
        if to_ascii_digits(ticket.text[field.start:field.end]) != to_ascii_digits(field.span):
            continue
        if name == "amount" and re.search(_NUMBER, _normalized(field.span)):
            value, currency = _exact_amount(_normalized(field.span))
        else:
            value, currency = normalize_value(name, _normalized(field.span), str(field.value), received_at)
            if name == "amount":
                currency = field.currency or currency
        if value is not None:
            evidence[name].add((value, currency))
    lookup = state.get("lookup")
    matched = lookup.txn if lookup and lookup.status == "matched" else None
    match_ref = None
    if matched:
        match_ref, _ = normalize_value("txn_ref", _normalized(matched.txn_ref), None, received_at)
        evidence["txn_ref"].add((match_ref, None))
        evidence["amount"].add((matched.amount_iqd, "IQD"))
        evidence["date"].add((matched.created_at.date().isoformat(), None))
        for phone in (matched.sender_phone, matched.receiver_phone):
            if canonical := normalize_phone(phone or ""):
                evidence["phone"].add((canonical, None))
    findings = []
    if used_txn_ref is not None:
        reference, _ = normalize_value("txn_ref", _normalized(used_txn_ref), None, received_at)
        if reference is None or match_ref is None or reference != match_ref:
            findings.append("invalid_used_txn_ref")
    stated = _values(reply, received_at)
    for name in ("amount", "date", "phone", "txn_ref"):
        if any(value[0] is None or value not in evidence[name] for value in stated[name]):
            findings.append(f"ungrounded_{name}")
    return findings


def check_draft(reply: str, citations: list[str], used_txn_ref: str | None,
                state: PipelineState, retrieved: dict[str, Passage]) -> list[str]:
    """Return ordered, deduplicated finding IDs without changing pipeline state.

    The caller owns the current ticket's retrieved map. Jev evaluation, escalation,
    retention of failed drafts and trace persistence belong to the outer drafter.
    """
    findings = _reply_findings(reply) + _citation_findings(citations, retrieved)
    findings.extend(_grounding_findings(reply, used_txn_ref, state))
    if requests_credentials(reply):
        findings.append("requests_credentials")
    return findings
