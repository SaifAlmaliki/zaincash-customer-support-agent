"""Start one new pipeline run for a ticket that was already processed."""
from sqlalchemy import select

from app.db.models import RunRow, TicketResultRow, TicketRow
from app.db.repository import create_run
from app.pipeline.contracts import Ticket


class ReprocessNotFound(LookupError):
    pass


class ReprocessBusy(RuntimeError):
    pass


def start_reprocess(session, result_id: int, *, mode: str, prompt_version: str, model_ids: dict):
    result = session.get(TicketResultRow, result_id)
    if result is None:
        raise ReprocessNotFound("Ticket result not found.")
    ticket_row = session.get(TicketRow, result.ticket_id)
    if ticket_row is None:
        raise ReprocessNotFound("Ticket result not found.")
    session.execute(select(TicketRow).where(TicketRow.id == ticket_row.id).with_for_update())
    running = session.scalar(
        select(TicketResultRow.id)
        .join(RunRow, TicketResultRow.run_id == RunRow.id)
        .where(
            TicketResultRow.ticket_id == ticket_row.id,
            TicketResultRow.status == "processing",
            RunRow.status == "running",
        )
        .limit(1)
    )
    if running is not None:
        raise ReprocessBusy("This ticket is already being reprocessed.")
    for stale in session.scalars(select(TicketResultRow).where(
        TicketResultRow.ticket_id == ticket_row.id, TicketResultRow.status == "processing",
    )):
        stale.status = "failed"
        stale.error = "Reprocessing did not finish. Start it again."
    run_id = create_run(session, mode=mode, prompt_version=prompt_version, model_ids=model_ids)
    placeholder = TicketResultRow(
        run_id=run_id, ticket_id=ticket_row.id, status="processing", category_probs={}, flags={}, extracted={},
        escalation_reasons=[], citations=[], agent_trace=[], escalated=False, latency_ms=0, cost_usd=0.0,
    )
    session.add(placeholder)
    session.flush()
    run = session.get(RunRow, run_id)
    run.counts = {"expected_total": 1}
    ticket = Ticket(
        id=ticket_row.id, external_id=ticket_row.external_id, text=ticket_row.text, channel=ticket_row.channel,
        customer_phone=ticket_row.customer_phone, received_at=ticket_row.received_at,
    )
    return placeholder, ticket
