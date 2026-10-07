"""Recall-tuned regex candidate finders. Jev later picks among these spans (spec §6.3)."""
from __future__ import annotations

import re

from app.pipeline.contracts import Candidate, Candidates
from app.pipeline.normalize import to_ascii_digits

MAX_CANDIDATES_PER_FIELD = 50  # Jev Choice allows at most 255 options
MIN_BARE_AMOUNT = 250  # a number with no unit below this is not treated as an amount

TXN_FULL = re.compile(r"ZC\d{10}")
_TXN_RE = re.compile(r"(?<![A-Za-z0-9])[Zz][Cc][\s-]?(\d{10})(?!\d)")
_PHONE_RE = re.compile(r"(?<![\d+])(?:\+?964[\s-]?|0)(7[3-9]\d)[\s-]?(\d{3})[\s-]?(\d{4})(?!\d)")
_ABS_DATE_RE = re.compile(
    r"(?<![\d/.-])(\d{4}-\d{1,2}-\d{1,2}|\d{1,2}[/-]\d{1,2}(?:[/-](?:\d{4}|\d{2}))?)(?![\d/-])"
)
_REL_DATE_RE = re.compile(
    r"(?<!\w)(?:و|ب)?("
    r"اليوم|امس|أمس|البارحة|البارحه|امبارح"
    r"|قبل\s?يومين|قبل\s?\d+\s?(?:يوم|ايام|أيام)"
    r"|(?:ال)?[اأ]سبوع\s(?:الماضي|الفات|اللي\sفات)"
    r"|(?:يوم\s)?(?:السبت|الاحد|الأحد|الاثنين|الإثنين|الثلاثاء|الاربعاء|الأربعاء|الخميس|الجمعة|الجمعه)"
    r"|yesterday|today|lyom|ams|embareh"
    r")(?!\w)",
    re.IGNORECASE,
)
_UNITS = r"الف|ألف|آلاف|الاف|الآف|مليون|دينار|دنانير|دولار|IQD|USD|million|alf|dinar|k|د\.ع"
_AMOUNT_RE = re.compile(
    r"(?<![\w.,$])(\$\s?)?(\d{1,3}(?:[,.]\d{3})+|\d+(?:\.\d+)?)(?:\s?(" + _UNITS + r"))?(?!\w)",
    re.IGNORECASE,
)
_NUM_RE = re.compile(r"\d{1,3}(?:[,.]\d{3})+|\d+(?:\.\d+)?")
_GROUPED = re.compile(r"\d{1,3}(?:[,.]\d{3})+")
_THOUSANDS_AR = ("الف", "ألف", "آلاف", "الاف", "الآف")


def normalize_phone(text: str) -> str | None:
    digits = re.sub(r"\D", "", to_ascii_digits(text or ""))
    if digits.startswith("964"):
        digits = "0" + digits[3:]
    return digits if re.fullmatch(r"07[3-9]\d{8}", digits) else None


def parse_amount(span: str) -> tuple[int, str] | None:
    s = to_ascii_digits(span or "").strip().lower()
    m = _NUM_RE.search(s)
    if not m:
        return None
    raw = m.group(0)
    number = float(re.sub(r"[,.]", "", raw)) if _GROUPED.fullmatch(raw) else float(raw)
    rest = s[: m.start()] + " " + s[m.end() :]
    if "مليون" in rest or "million" in rest:
        number *= 1_000_000
    elif any(u in rest for u in _THOUSANDS_AR) or re.search(r"(?<![a-z])(k|alf)(?![a-z])", rest):
        number *= 1000
    usd = "$" in s or "دولار" in s or re.search(r"(?<![a-z])usd(?![a-z])", s) is not None
    return int(round(number)), ("USD" if usd else "IQD")


def _overlaps(start: int, end: int, taken: list[tuple[int, int]]) -> bool:
    return any(start < e and s < end for s, e in taken)


def _add(bucket: list[Candidate], cand: Candidate, taken: list[tuple[int, int]]) -> None:
    taken.append((cand.start, cand.end))
    if len(bucket) < MAX_CANDIDATES_PER_FIELD and all(c.value != cand.value for c in bucket):
        bucket.append(cand)


def find_candidates(match_text: str) -> Candidates:
    """Over-collect candidate spans. `match_text` must already have ASCII digits."""
    out = Candidates()
    taken: list[tuple[int, int]] = []
    for m in _TXN_RE.finditer(match_text):
        _add(out.txn_ref, Candidate("txn_ref", "ZC" + m.group(1), m.group(0), m.start(), m.end()), taken)
    for m in _PHONE_RE.finditer(match_text):
        value = "0" + m.group(1) + m.group(2) + m.group(3)
        _add(out.phone, Candidate("phone", value, m.group(0), m.start(), m.end()), taken)
    for rx in (_ABS_DATE_RE, _REL_DATE_RE):
        for m in rx.finditer(match_text):
            if _overlaps(m.start(1), m.end(1), taken):
                continue
            _add(out.date, Candidate("date", m.group(1), m.group(1), m.start(1), m.end(1)), taken)
    for m in _AMOUNT_RE.finditer(match_text):
        if _overlaps(m.start(), m.end(), taken):
            continue
        span = m.group(0)
        parsed = parse_amount(span)
        has_unit = bool(m.group(1) or m.group(3))
        if parsed is None or (not has_unit and parsed[0] < MIN_BARE_AMOUNT):
            continue
        _add(out.amount, Candidate("amount", span, span, m.start(), m.end()), taken)
    return out
