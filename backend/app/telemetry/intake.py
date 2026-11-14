"""Intake model calls arrive as JSON trace entries; store them as ledger rows too."""
from __future__ import annotations

import uuid
from typing import Any

from sqlalchemy import update
from sqlalchemy.orm import Session

from app.datetime import parse_dt
from app.telemetry.calls import AiCall, count, money
from app.telemetry.db_models import AiCallRow
from app.telemetry.store import add_calls


def intake_calls(trace: list[dict[str, Any]]) -> list[AiCall]:
    calls = []
    for item in trace:
        if "provider" not in item or "started_at" not in item:
            continue  # recorded before the ledger existed
        usage = item.get("usage") or {}
        source = item.get("cost_source") or "unknown"
        if source == "provider":
            cost = money(item.get("cost_usd")) or 0.0
        elif source == "estimate":
            cost = money(item.get("cost_estimate_usd")) or 0.0
        else:
            cost = 0.0
        detail = {"kind": item.get("kind")}
        if item.get("rejected"):
            detail["rejected"] = True
        calls.append(AiCall(
            "intake", item["provider"], item["model"], item.get("locality") or "cloud",
            parse_dt(item["started_at"]), int(item.get("latency_ms") or 0),
            input_tokens=count(usage.get("input_tokens")), output_tokens=count(usage.get("output_tokens")),
            cost_usd=cost, cost_source=source, status="error" if item.get("error") else "ok",
            error=item.get("error"), detail=detail,
        ))
    return calls


def add_intake_calls(session: Session, session_id: uuid.UUID, trace: list[dict[str, Any]]) -> None:
    add_calls(session, intake_calls(trace), intake_session_id=session_id)


def link_intake_calls(session: Session, session_id: uuid.UUID, *, run_id: int, ticket_id: int) -> None:
    session.execute(update(AiCallRow).where(AiCallRow.intake_session_id == session_id)
                    .values(run_id=run_id, ticket_id=ticket_id))
