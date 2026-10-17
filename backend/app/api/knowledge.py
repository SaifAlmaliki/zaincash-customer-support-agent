import asyncio
from dataclasses import asdict
from urllib.parse import quote

from fastapi import APIRouter, BackgroundTasks, HTTPException, Query, Request, Response, UploadFile
from sqlalchemy import select
from starlette.concurrency import run_in_threadpool

from app.api.dependencies import SessionDep
from app.api.schemas import KnowledgeIndexInput, KnowledgeSearchInput
from app.db.document_models import UploadedDocument
from app.kb.documents import (
    MAX_UPLOAD_BYTES,
    DocumentValidationError,
    document_filename,
    document_view,
    store_document,
)
from app.kb.service import DocumentNotFoundError
from app.services.knowledge_runtime import knowledge_configured

router = APIRouter(prefix="/api/knowledge", tags=["Knowledge documents"])


@router.get("")
def list_documents(session: SessionDep):
    return [document_view(session, doc) for doc in session.scalars(select(UploadedDocument).order_by(UploadedDocument.id.desc()))]


@router.post("")
async def upload_document(file: UploadFile, background: BackgroundTasks, request: Request, session: SessionDep):
    try:
        filename = document_filename(file.filename or "document")
        content = await file.read(MAX_UPLOAD_BYTES + 1)
        if not content:
            raise DocumentValidationError("Upload a nonempty document.")
    except DocumentValidationError as exc:
        raise HTTPException(exc.status_code, str(exc)) from None
    finally:
        await file.close()
    try:
        doc = store_document(session, filename, content)
        session.commit()
    except DocumentValidationError as exc:
        raise HTTPException(exc.status_code, str(exc)) from None
    value = document_view(session, doc)
    requested = False
    if knowledge_configured(request.app.state.settings) and value["status"] == "awaiting_indexing":
        requested = request.app.state.index_jobs.submit(background, value)
    return value | {"index_requested": requested}


def _validate_categories(request, categories):
    if any(category not in request.app.state.taxonomy.categories for category in categories):
        raise HTTPException(422, "Unknown knowledge category; use a taxonomy category ID.")


def _require_provider(request):
    if not knowledge_configured(request.app.state.settings):
        raise HTTPException(503, "Knowledge provider is disabled or unconfigured.")


@router.post("/search")
async def search_knowledge(body: KnowledgeSearchInput, request: Request):
    _validate_categories(request, [] if body.category is None else [body.category])
    _require_provider(request)
    try:
        # Search's adapter timeout is also inside the overall request budget.
        async with asyncio.timeout(request.app.state.settings.agent_timeout_s):
            result = await request.app.state.knowledge.search(body.query, category=body.category, k=body.k)
        return asdict(result)
    except Exception:
        raise HTTPException(503, "Knowledge search unavailable; check the provider and index, then retry.") from None


@router.post("/{document_id}/index", status_code=202)
def index_document(document_id: int, background: BackgroundTasks, request: Request, session: SessionDep,
                   body: KnowledgeIndexInput | None = None):
    tags = body.category_tags if body else None
    _validate_categories(request, tags or [])
    doc = session.get(UploadedDocument, document_id)
    if doc is None:
        raise HTTPException(404, "Document not found.")
    _require_provider(request)
    value = document_view(session, doc)
    if not request.app.state.index_jobs.submit(background, value, category_tags=tags):
        raise HTTPException(503, "Indexing is busy; retry shortly.")
    return value | {"index_requested": True}


@router.get("/{document_id}/chunks")
async def list_chunks(document_id: int, request: Request,
                      offset: int = Query(0, ge=0), limit: int = Query(50, ge=1, le=100)):
    try:
        # Service output is already bounded by the 1,200-chunk document limit.
        chunks = await run_in_threadpool(request.app.state.knowledge.list_chunks, document_id)
    except DocumentNotFoundError:
        raise HTTPException(404, "Document not found.") from None
    return {"items": chunks[offset:offset + limit], "total": len(chunks)}


@router.get("/{document_id}/download")
def download_document(document_id: int, session: SessionDep):
    doc = session.get(UploadedDocument, document_id)
    if not doc:
        raise HTTPException(404, "Document not found.")
    return Response(doc.content, media_type=doc.content_type,
                    headers={"Content-Disposition": f"attachment; filename*=UTF-8''{quote(doc.filename)}"})


@router.delete("/{document_id}", status_code=204)
def delete_document(document_id: int, session: SessionDep):
    doc = session.get(UploadedDocument, document_id)
    if not doc:
        raise HTTPException(404, "Document not found.")
    session.delete(doc)
    session.commit()
