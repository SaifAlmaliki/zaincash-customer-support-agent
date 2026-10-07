"""Resolve date phrases against the ticket's received_at. Arithmetic stays in code (Jev docs)."""
from __future__ import annotations

import re
from datetime import date, datetime, timedelta

from app.pipeline.normalize import to_ascii_digits

_TODAY = {"اليوم", "today", "lyom"}
_YESTERDAY = {"امس", "أمس", "البارحة", "البارحه", "امبارح", "yesterday", "ams", "embareh"}
_WEEKDAYS = {
    "الاثنين": 0, "الإثنين": 0, "الثلاثاء": 1, "الاربعاء": 2, "الأربعاء": 2, "الخميس": 3,
    "الجمعة": 4, "الجمعه": 4, "السبت": 5, "الاحد": 6, "الأحد": 6,
}


def _safe_date(y: int, m: int, d: int) -> date | None:
    try:
        return date(y, m, d)
    except ValueError:
        return None


def resolve_date(span: str, received_at: datetime) -> date | None:
    s = to_ascii_digits(span or "").strip().lower()
    if not s:
        return None
    base = received_at.date()
    if s in _TODAY:
        return base
    if s in _YESTERDAY:
        return base - timedelta(days=1)
    if "يومين" in s:
        return base - timedelta(days=2)
    if m := re.fullmatch(r"قبل\s?(\d+)\s?(?:يوم|ايام|أيام)", s):
        return base - timedelta(days=int(m.group(1)))
    if "سبوع" in s:
        return base - timedelta(days=7)
    day_name = s.removeprefix("يوم").strip()
    if day_name in _WEEKDAYS:
        return base - timedelta(days=(base.weekday() - _WEEKDAYS[day_name]) % 7)
    if m := re.fullmatch(r"(\d{4})-(\d{1,2})-(\d{1,2})", s):
        return _safe_date(int(m.group(1)), int(m.group(2)), int(m.group(3)))
    if m := re.fullmatch(r"(\d{1,2})[/-](\d{1,2})(?:[/-](\d{2}|\d{4}))?", s):
        day, month = int(m.group(1)), int(m.group(2))  # Iraq writes day first
        if m.group(3):
            year = int(m.group(3))
            return _safe_date(year + 2000 if year < 100 else year, month, day)
        d = _safe_date(base.year, month, day)
        if d and d > base:
            d = _safe_date(base.year - 1, month, day)
        return d
    return None
