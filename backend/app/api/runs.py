from fastapi import APIRouter, BackgroundTasks, HTTPException, Request
from sqlalchemy import select

from app.api.dependencies import SessionDep
from app.api.schemas import BatchInput
from app.db.models import RunRow, TicketRow
from app.db.repository import create_run, upsert_tickets
from app.pipeline.contracts import Ticket
from app.pipeline.factory import model_ids
from app.pipeline.stage2_classify.prompts import PROMPT_VERSION
from app.services.batch_jobs import run_job
from app.services.workspace_queries import run_view

router = APIRouter(prefix="/api/runs", tags=["Batch runs"])


@router.get("")
def list_runs(session: SessionDep):
    return [run_view(session, run) for run in session.scalars(select(RunRow).order_by(RunRow.id.desc()).limit(100))]


@router.get("/{run_id}")
def get_run(run_id: int, session: SessionDep):
    run = session.get(RunRow, run_id)
    if not run:
        raise HTTPException(404, "Batch run not found.")
    return run_view(session, run)


@router.post("", status_code=202)
def start_run(batch: BatchInput, background: BackgroundTasks, request: Request, session: SessionDep):
    settings = request.app.state.settings
    if not request.app.state.testing_pipeline:
        missing = []
        if batch.mode in ("gemini", "cascade") and not settings.openrouter_api_key:
            missing.append("OPENROUTER_API_KEY")
        if batch.mode in ("jev", "cascade") and not settings.typesafe_api_key:
            missing.append("TYPESAFE_API_KEY")
        if missing:
            raise HTTPException(503, f"Configure {' and '.join(missing)} in the backend .env, then restart the API.")
    tickets = [Ticket(**ticket.model_dump()) for ticket in batch.tickets]
    existing = {row.external_id: row for row in session.scalars(select(TicketRow).where(
        TicketRow.external_id.in_([ticket.external_id for ticket in tickets])
    ))}
    for ticket in tickets:
        previous = existing.get(ticket.external_id)
        if previous and (previous.text != ticket.text or previous.customer_phone != ticket.customer_phone):
            raise HTTPException(409, f"Ticket {ticket.external_id} already exists with different content. Use a new ID.")
    stored = upsert_tickets(session, tickets, source="upload")
    # Repeated IDs must use their stored timestamp too: relative dates cannot silently change on reruns.
    stored = [Ticket(id=t.id, external_id=t.external_id, text=t.text, channel=t.channel,
                     customer_phone=t.customer_phone,
                     received_at=existing[t.external_id].received_at if t.external_id in existing else t.received_at)
              for t in stored]
    run_id = create_run(session, mode=batch.mode, prompt_version=PROMPT_VERSION,
                        model_ids=model_ids(settings, batch.mode))
    run = session.get(RunRow, run_id)
    run.counts = {"expected_total": len(stored)}
    session.commit()
    background.add_task(run_job, request.app, run_id, stored, batch.mode)
    return run_view(session, run)
