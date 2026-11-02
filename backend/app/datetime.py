"""Shared datetime parsing and the pipeline's Baghdad timezone convention."""
from __future__ import annotations

from datetime import datetime, timedelta, timezone
from typing import Any

BAGHDAD = timezone(timedelta(hours=3))


def parse_dt(value: Any) -> datetime:
    parsed = value if isinstance(value, datetime) else datetime.fromisoformat(
        str(value).replace("Z", "+00:00")
    )
    return parsed if parsed.tzinfo else parsed.replace(tzinfo=BAGHDAD)
