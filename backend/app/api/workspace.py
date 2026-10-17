from collections import Counter
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

from fastapi import APIRouter, Request
from sqlalchemy import func, select, text

from app.api.dependencies import SessionDep
from app.db.models import TicketRow
from app.kb.models import KnowledgeChunk, KnowledgeDocumentIndex
from app.kb.service import CHUNKING_VERSION
from app.services.knowledge_runtime import knowledge_configured
from app.services.workspace_queries import STAGES, latest_results_query

router = APIRouter(prefix="/api", tags=["Workspace"])


@router.get("/health")
def health(request: Request, session: SessionDep):
    session.execute(text("SELECT 1"))
    settings = request.app.state.settings
    modes = []
    if settings.typesafe_api_key:
        modes.append("jev")
    if settings.openrouter_api_key:
        modes.append("gemini")
    if len(modes) == 2:
        modes.append("cascade")
    configured = knowledge_configured(settings)
    compatible_chunks = select(KnowledgeChunk.id).where(
        KnowledgeChunk.document_id == KnowledgeDocumentIndex.document_id,
        KnowledgeChunk.attempt_id == KnowledgeDocumentIndex.attempt_id,
        KnowledgeChunk.embedding_model == settings.embedding_model,
    ).exists()
    indexed_count = session.scalar(select(func.count()).select_from(KnowledgeDocumentIndex).where(
        KnowledgeDocumentIndex.status == "indexed",
        KnowledgeDocumentIndex.embedding_model == settings.embedding_model,
        KnowledgeDocumentIndex.embedding_dimensions == settings.embed_dim,
        KnowledgeDocumentIndex.chunking_version == CHUNKING_VERSION,
        KnowledgeDocumentIndex.chunk_count > 0, compatible_chunks,
    ))
    ready = configured and indexed_count > 0
    states = set(session.scalars(select(KnowledgeDocumentIndex.status).distinct()))
    status = ("disabled" if not settings.rag_enabled else "unconfigured" if not configured
              else "ready" if ready else "indexing" if "indexing" in states
              else "failed" if "failed" in states else "empty")
    return {"database": "connected", "configured_modes": modes,
            "capabilities": {"drafting": ready, "rag_indexing": configured, "evaluation": False},
            "knowledge": {"enabled": settings.rag_enabled, "configured": configured, "ready": ready,
                          "status": status, "indexed_document_count": indexed_count,
                          "embedding_model": settings.embedding_model, "embedding_dimensions": settings.embed_dim},
            "drafting": {"enabled": settings.rag_enabled, "configured": configured, "ready": ready,
                         "credential_check_configured": bool(settings.typesafe_api_key)}}


@router.get("/workspace")
def workspace(request: Request, session: SessionDep):
    rows = list(session.scalars(latest_results_query()))
    tax = request.app.state.taxonomy
    return {"taxonomy": [{"id": cat.id, "team": cat.team, "description": cat.what_en}
                          for cat in tax.categories.values()],
            "teams": list(tax.teams), "stages": STAGES,
            "counts": {"total": len(rows), "by_status": dict(Counter(row.status for row in rows)),
                       "by_category": dict(Counter(row.category or "unclassified" for row in rows))}}


@router.get("/insights")
def insights(session: SessionDep):
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
