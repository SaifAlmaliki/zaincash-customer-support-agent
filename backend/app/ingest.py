"""Load judge/user ticket files: .jsonl, .json (a list or {"tickets": [...]}), and .csv (UTF-8 with or without a BOM). Rows may omit customer_phone; storing such a ticket is rejected later."""
from __future__ import annotations

import csv
import json
from datetime import datetime
from pathlib import Path
from typing import Any

from app.customers.phone import InvalidPhone, normalize_customer_phone
from app.datetime import BAGHDAD, parse_dt
from app.pipeline.contracts import Ticket
from app.pipeline.stage1_normalize.normalize import sanitize_for_storage


def load_jsonl(path: str | Path) -> list[dict[str, Any]]:
    lines = Path(path).read_text(encoding="utf-8-sig").splitlines()
    return [json.loads(line) for line in lines if line.strip()]


def _rows(path: Path) -> list[dict[str, Any]]:
    suffix = path.suffix.lower()
    if suffix == ".jsonl":
        return load_jsonl(path)
    if suffix == ".json":
        data = json.loads(path.read_text(encoding="utf-8-sig"))
        return data.get("tickets", []) if isinstance(data, dict) else list(data)
    if suffix == ".csv":
        with path.open(encoding="utf-8-sig", newline="") as f:
            return list(csv.DictReader(f))
    raise ValueError(f"unsupported ticket file type {suffix!r}; use .jsonl, .json or .csv")


def load_tickets(path: str | Path, *, now: datetime | None = None) -> list[Ticket]:
    path = Path(path)
    now = now or datetime.now(BAGHDAD)
    seen: set[str] = set()
    tickets: list[Ticket] = []
    for i, row in enumerate(_rows(path), start=1):
        external_id = str(row.get("external_id") or row.get("id") or f"{path.stem}-{i}").strip()
        if external_id in seen:
            continue
        seen.add(external_id)
        raw_phone = str(row.get("customer_phone") or "").strip()
        try:
            phone = normalize_customer_phone(raw_phone) if raw_phone else None
        except InvalidPhone as exc:
            raise ValueError(f"Row {i} ({external_id}): {exc}") from None
        tickets.append(Ticket(
            external_id=external_id,
            text=sanitize_for_storage(str(row.get("text") or row.get("message") or "")),
            received_at=parse_dt(row["received_at"]) if row.get("received_at") else now,
            channel=str(row.get("channel") or "app"),
            customer_phone=phone,
        ))
    return tickets
