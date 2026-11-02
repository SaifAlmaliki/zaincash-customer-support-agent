from uuid import UUID

from fastapi import APIRouter, HTTPException, Query, Request
from fastapi.responses import Response
from sqlalchemy import func, select

from app.api.dependencies import SessionDep
from app.api.schemas import ReviewInput
from app.db.models import TicketResultRow, TicketRow
from app.intake.projection import employee_attachment
from app.services.reviews import (
    InvalidReviewTeam,
    ReviewCommand,
    ReviewConflict,
    ReviewNotFound,
    record_review,
)
from app.services.workspace_queries import latest_results_query, result_view

router = APIRouter(prefix="/api/results", tags=["Results & review"])


@router.get("")
def list_results(session: SessionDep, status: str | None = None, team: str | None = None, category: str | None = None,
                 priority: str | None = None, q: str = "", run_id: int | None = None,
                 offset: int = Query(0, ge=0), limit: int = Query(200, ge=1, le=500)):
    query = select(TicketResultRow).where(TicketResultRow.run_id == run_id) if run_id else latest_results_query()
    for column, value in [(TicketResultRow.status, status), (TicketResultRow.team, team),
                          (TicketResultRow.category, category), (TicketResultRow.priority, priority)]:
        if value:
            query = query.where(column == value)
    if q:
        ticket_ids = select(TicketRow.id).where(TicketRow.text.contains(q, autoescape=True) |
                                               TicketRow.external_id.contains(q, autoescape=True))
        query = query.where(TicketResultRow.ticket_id.in_(ticket_ids))
    total = session.scalar(
        select(func.count()).select_from(query.order_by(None).subquery())
    ) or 0
    rows = session.scalars(
        query.order_by(TicketResultRow.priority.asc().nullslast(), TicketResultRow.id.desc())
        .offset(offset)
        .limit(limit)
    )
    return {"items": [result_view(session, row) for row in rows], "total": total}


@router.get("/{result_id}")
def get_result(result_id: int, session: SessionDep):
    result = session.get(TicketResultRow, result_id)
    if result is None:
        raise HTTPException(404, "Ticket result not found.")
    return result_view(session, result, detail=True)


@router.get("/{result_id}/intake/attachments/{attachment_id}")
def read_intake_attachment(result_id: int, attachment_id: UUID, request: Request, session: SessionDep):
    image = employee_attachment(session, result_id, attachment_id, request.app.state.intake_store)
    return Response(content=image.data, media_type=image.mime_type, headers={"Cache-Control": "no-store"})


@router.post("/{result_id}/reviews")
def review_result(result_id: int, review: ReviewInput, request: Request, session: SessionDep):
    try:
        result = record_review(
            session, result_id, ReviewCommand(**review.model_dump()), request.app.state.taxonomy.teams,
        )
    except ReviewNotFound as exc:
        raise HTTPException(404, str(exc)) from None
    except ReviewConflict as exc:
        raise HTTPException(409, str(exc)) from None
    except InvalidReviewTeam as exc:
        raise HTTPException(422, str(exc)) from None
    return result_view(session, result, detail=True)
