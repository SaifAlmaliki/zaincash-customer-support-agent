"""Turn picks into normalized, span-anchored fields. A value is never invented (spec §6.3)."""
from __future__ import annotations

import re
from collections.abc import Sequence
from datetime import date, datetime

from app.llm import LLMUnavailable
from app.pipeline.candidates import TXN_FULL, normalize_phone, parse_amount
from app.pipeline.classify.base import FieldExtractor
from app.pipeline.contracts import FIELD_NAMES, Candidates, ExtractedField, FieldPick, NormalizedTicket
from app.pipeline.dates import resolve_date

_NO_PICK = FieldPick(None, 0.0, "none")
WEAK_JEV_CONFIDENCE = 0.5


def _iso(value: str | None) -> date | None:
    try:
        return date.fromisoformat(value) if value else None
    except ValueError:
        return None


def normalize_value(field: str, span: str, hint: str | None,
                    received_at: datetime) -> tuple[str | int | None, str | None]:
    if field == "txn_ref":
        v = re.sub(r"[^A-Za-z0-9]", "", span).upper()
        return (v if TXN_FULL.fullmatch(v) else None), None
    if field == "phone":
        return normalize_phone(span) or (normalize_phone(hint) if hint else None), None
    if field == "amount":
        parsed = parse_amount(span) or (parse_amount(hint) if hint else None)
        return (parsed[0], parsed[1]) if parsed else (None, None)
    if field == "date":
        d = resolve_date(span, received_at) or _iso(hint)
        return (d.isoformat() if d else None), None
    raise ValueError(f"unknown field {field}")


def _field(name: str, pick: FieldPick, cands: Candidates, nt: NormalizedTicket) -> ExtractedField:
    empty = ExtractedField(None, None, None, None, pick.method, pick.confidence)
    if pick.value is None:
        return empty
    if pick.method == "jev_pick":
        cand = next((c for c in cands.for_field(name) if c.span == pick.value), None)
        if cand is None:
            return empty
        span, start, end = cand.span, cand.start, cand.end
    else:
        start = nt.match_text.find(pick.value)
        if start < 0:
            return empty
        span, end = pick.value, start + len(pick.value)
    value, currency = normalize_value(name, span, pick.normalized, nt.ticket.received_at)
    if value is None:
        return empty
    return ExtractedField(value, span, start, end, pick.method, pick.confidence, currency)


def finalize(picks: dict[str, FieldPick], cands: Candidates,
             nt: NormalizedTicket) -> dict[str, ExtractedField]:
    return {f: _field(f, picks.get(f, _NO_PICK), cands, nt) for f in FIELD_NAMES}


def _is_weak(x: ExtractedField) -> bool:
    if x.value is None and x.method == "none":
        return True  # no regex candidates at all; the value may be written in words
    return x.method == "jev_pick" and x.confidence < WEAK_JEV_CONFIDENCE


async def fill_gaps(extracted: dict[str, ExtractedField], nt: NormalizedTicket,
                    required: Sequence[str], extractor: FieldExtractor | None
                    ) -> tuple[dict[str, ExtractedField], float]:
    weak = [f for f in required if _is_weak(extracted[f])]
    if not weak or extractor is None:
        return extracted, 0.0
    try:
        picks, cost = await extractor.extract(nt, weak)
    except LLMUnavailable:
        return extracted, 0.0
    updated = dict(extracted)
    for f in weak:
        pick = picks.get(f)
        if pick is not None and pick.value is not None:
            candidate = _field(f, pick, Candidates(), nt)
            if candidate.value is not None:
                updated[f] = candidate
    return updated, cost
