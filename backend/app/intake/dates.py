"""Conservative date and digit normalization for customer reports."""
from __future__ import annotations

import re
from datetime import datetime, timedelta

from app.datetime import BAGHDAD
from app.text import to_ascii_digits

_RELATIVE = {
    "today": 0,
    "yesterday": -1,
    "اليوم": 0,
    "أمس": -1,
    "امس": -1,
    "البارحة": -1,
    "البارحه": -1,
}
# Python weekday(): Monday is 0. A named day means the latest matching calendar day.
_WEEKDAYS = {
    "الاثنين": 0, "الإثنين": 0, "الثلاثاء": 1, "الاربعاء": 2, "الأربعاء": 2, "الخميس": 3,
    "الجمعة": 4, "الجمعه": 4, "السبت": 5, "الاحد": 6, "الأحد": 6,
    "monday": 0, "tuesday": 1, "wednesday": 2, "thursday": 3, "friday": 4, "saturday": 5, "sunday": 6,
}
_ISO = re.compile(r"^\d{4}-\d{2}-\d{2}$")
_SLASH = re.compile(r"\d{1,2}\s*/\s*\d{1,2}")


def canonical_digits(value: str) -> str:
    return to_ascii_digits(value or "")


def normalize_reported_date(value: str, source_time: datetime) -> str | None:
    """Resolve an unambiguous calendar date. Never invents an hour."""
    if value is None or source_time.tzinfo is None or source_time.tzinfo.utcoffset(source_time) is None:
        return None
    text = " ".join(canonical_digits(value).strip().split())
    if not text or _SLASH.search(text):
        return None
    if _ISO.fullmatch(text):
        try:
            datetime.strptime(text, "%Y-%m-%d")
        except ValueError:
            return None
        return text
    folded = text.lower()
    if re.search(r"\bbefore\b|قبل", folded):
        return None
    matches = []
    for word, delta in _RELATIVE.items():
        matched = (
            re.search(rf"(?<!\w){re.escape(word)}(?!\w)", folded) is not None
            if word.isascii() else word in text
        )
        if matched:
            matches.append(delta)
    if matches and len(set(matches)) == 1:
        anchor = source_time.astimezone(BAGHDAD).date() + timedelta(days=matches[0])
        return anchor.isoformat()
    day_name = folded.removeprefix("يوم").strip()
    if day_name in _WEEKDAYS:
        anchor = source_time.astimezone(BAGHDAD).date()
        resolved = anchor - timedelta(days=(anchor.weekday() - _WEEKDAYS[day_name]) % 7)
        return resolved.isoformat()
    return None
