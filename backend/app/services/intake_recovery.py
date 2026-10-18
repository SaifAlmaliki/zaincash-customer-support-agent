"""Keep a submitted intake ticket visible when processing never finishes."""
from __future__ import annotations

from collections import Counter
from datetime import UTC, datetime

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.models import RunRow, TicketResultRow
from app.intake.db_models import IntakeSubmissionRow


def fail_intake_placeholders(session: Session, run_id: int, reason: str) -> int:
    rows = list(session.scalars(select(TicketResultRow).where(
        TicketResultRow.run_id == run_id, TicketResultRow.status == "processing"
    )))
    count = 0
    for row in rows:
        linked = session.scalar(select(IntakeSubmissionRow.id).where(IntakeSubmissionRow.ticket_id == row.ticket_id))
        if linked is None:
            continue
        row.status = "failed"
        row.error = reason
        count += 1
    return count


def reconcile_intake_run(session: Session, run: RunRow) -> None:
    rows = list(session.scalars(select(TicketResultRow).where(TicketResultRow.run_id == run.id)))
    durable = [row for row in rows if row.status != "processing"]
    expected = run.counts.get("expected_total", len(rows) or 1)
    run.counts = {
        **run.counts,
        "expected_total": expected,
        "total": len(durable),
        "by_status": dict(Counter(row.status for row in durable)),
    }
    run.total_cost_usd = round(sum(row.cost_usd or 0 for row in durable), 6)


def recover_intake_processing(session_factory) -> int:
    with session_factory() as session:
        rows = list(session.scalars(select(TicketResultRow).where(TicketResultRow.status == "processing")))
        count = 0
        runs: set[int] = set()
        for row in rows:
            linked = session.scalar(select(IntakeSubmissionRow).where(IntakeSubmissionRow.ticket_id == row.ticket_id))
            if linked is None:
                continue
            row.status = "failed"
            row.error = "Processing did not finish. The submitted report was kept."
            runs.add(row.run_id)
            count += 1
        now = datetime.now(UTC)
        for run_id in runs:
            run = session.get(RunRow, run_id)
            if run is None:
                continue
            if run.status == "running":
                run.status = "failed"
                run.finished_at = now
            reconcile_intake_run(session, run)
            run.counts = run.counts | {"error": "Processing did not finish. The submitted report was kept."}
        session.commit()
        return count
