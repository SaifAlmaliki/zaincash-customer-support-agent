from datetime import datetime
from typing import Annotated, Literal

from fastapi import APIRouter, HTTPException, Query

from app.api.dependencies import SessionDep
from app.telemetry.reports import summary, ticket_calls, ticket_page, usage_filter

router = APIRouter(prefix="/api/ai-usage", tags=["AI usage"])


def _filter(from_: datetime | None, to: datetime | None, process: str | None, model: str | None,
            run_id: int | None):
    try:
        return usage_filter(from_, to, process, model, run_id)
    except ValueError as exc:
        raise HTTPException(422, str(exc)) from None


@router.get("/summary")
def usage_summary(session: SessionDep, from_: Annotated[datetime | None, Query(alias="from")] = None,
                  to: datetime | None = None, process: str | None = None, model: str | None = None,
                  run_id: int | None = None):
    return summary(session, _filter(from_, to, process, model, run_id))


@router.get("/tickets")
def usage_tickets(session: SessionDep, from_: Annotated[datetime | None, Query(alias="from")] = None,
                  to: datetime | None = None, process: str | None = None, model: str | None = None,
                  run_id: int | None = None, sort: Literal["cost", "time", "recent"] = "recent",
                  limit: Annotated[int, Query(ge=1, le=200)] = 50,
                  offset: Annotated[int, Query(ge=0)] = 0):
    return ticket_page(session, _filter(from_, to, process, model, run_id), sort=sort, limit=limit, offset=offset)


@router.get("/tickets/{result_id}/calls")
def usage_ticket_calls(result_id: int, session: SessionDep):
    data = ticket_calls(session, result_id)
    if data is None:
        raise HTTPException(404, "Ticket result not found.")
    return data
