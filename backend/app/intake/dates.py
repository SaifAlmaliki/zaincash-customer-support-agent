"""Conservative date and digit normalization for customer reports."""
from __future__ import annotations

import re
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

from app.pipeline.stage1_normalize.normalize import to_ascii_digits

BAGHDAD = ZoneInfo("Asia/Baghdad")
_RELATIVE = {
    "today": 0,
    "yesterday": -1,
    "اليوم": 0,
    "أمس": -1,
    "امس": -1,
    "البارحة": -1,
    "البارحه": -1,
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
    for word, delta in _RELATIVE.items():
        matched = (
            re.search(rf"(?<!\w){re.escape(word)}(?!\w)", folded) is not None
            if word.isascii() else word in text
        )
        if matched:
            anchor = source_time.astimezone(BAGHDAD).date() + timedelta(days=delta)
            return anchor.isoformat()
    return None
