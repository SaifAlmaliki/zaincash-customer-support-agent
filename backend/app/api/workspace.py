from collections import Counter
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

from fastapi import APIRouter, Depends, Request
from sqlalchemy import text

from app.api.dependencies import get_session
from app.db.models import TicketRow
from app.services.workspace_queries import STAGES, latest_results_query

router = APIRouter(prefix="/api", tags=["Workspace"])


@router.get("/health")
def health(request: Request, session=Depends(get_session)):
    session.execute(text("SELECT 1"))
    settings = request.app.state.settings
    modes = []
    if settings.typesafe_api_key:
        modes.append("jev")
    if settings.google_api_key:
        modes.append("gemini")
    if len(modes) == 2:
        modes.append("cascade")
    return {"database": "connected", "configured_modes": modes,
            "capabilities": {"drafting": False, "rag_indexing": False, "evaluation": False}}


@router.get("/workspace")
def workspace(request: Request, session=Depends(get_session)):
    rows = list(session.scalars(latest_results_query()))
    tax = request.app.state.taxonomy
    return {"taxonomy": [{"id": cat.id, "team": cat.team, "description": cat.what_en}
                          for cat in tax.categories.values()],
            "teams": list(tax.teams), "stages": STAGES,
            "counts": {"total": len(rows), "by_status": dict(Counter(row.status for row in rows)),
                       "by_category": dict(Counter(row.category or "unclassified" for row in rows))}}


@router.get("/insights")
def insights(session=Depends(get_session)):
    rows = list(session.scalars(latest_results_query()))
    now = datetime.now(ZoneInfo("Asia/Baghdad"))
    current_start = (now - timedelta(days=now.weekday())).replace(hour=0, minute=0, second=0, microsecond=0)
    weeks = []
    for index in range(4, 0, -1):
        start = current_start - timedelta(weeks=index)
        end = start + timedelta(weeks=1)
        selected = [row for row in rows if start <= session.get(TicketRow, row.ticket_id).received_at < end]
        weeks.append({"start": start.isoformat(), "end": end.isoformat(), "total": len(selected),
                      "categories": dict(Counter(row.category or "unclassified" for row in selected))})
    return {"categories": dict(Counter(row.category or "unclassified" for row in rows)),
            "reasons": dict(Counter(reason for row in rows for reason in row.escalation_reasons)),
            "weeks": weeks, "total": len(rows), "evaluation": None}
