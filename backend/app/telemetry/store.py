from __future__ import annotations

import logging
from collections.abc import Callable, Iterable
from typing import Any

from sqlalchemy.orm import Session

from app.telemetry.calls import AiCall
from app.telemetry.db_models import AiCallRow

logger = logging.getLogger(__name__)


def call_rows(calls: Iterable[AiCall], *, run_id: int | None = None, ticket_id: int | None = None,
              intake_session_id: Any = None, document_id: int | None = None) -> list[AiCallRow]:
    return [AiCallRow(
        started_at=c.started_at, process=c.process, provider=c.provider, model=c.model,
        locality=c.locality, latency_ms=c.latency_ms, input_tokens=c.input_tokens,
        output_tokens=c.output_tokens, cost_usd=c.cost_usd, cost_source=c.cost_source,
        status=c.status, error=c.error, attempt=c.attempt, run_id=run_id, ticket_id=ticket_id,
        intake_session_id=intake_session_id, document_id=document_id, detail=dict(c.detail),
    ) for c in calls]


def add_calls(session: Session, calls: Iterable[AiCall], **links: Any) -> None:
    """Insert inside the owner's transaction; a failure rolls back only the savepoint."""
    rows = call_rows(calls, **links)
    if not rows:
        return
    try:
        with session.begin_nested():
            session.add_all(rows)
            session.flush()
    except Exception as exc:
        logger.warning("AI call recording failed: %s", type(exc).__name__)


def persist_calls(session_factory: Callable[[], Session], calls: Iterable[AiCall], **links: Any) -> None:
    rows = call_rows(calls, **links)
    if not rows:
        return
    try:
        with session_factory() as session:
            session.add_all(rows)
            session.commit()
    except Exception as exc:
        logger.warning("AI call recording failed: %s", type(exc).__name__)
