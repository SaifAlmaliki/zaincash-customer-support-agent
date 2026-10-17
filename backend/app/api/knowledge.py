from urllib.parse import quote

from fastapi import APIRouter, HTTPException, Response, UploadFile
from sqlalchemy import select

from app.api.dependencies import SessionDep
from app.db.document_models import UploadedDocument
from app.kb.documents import (
    MAX_UPLOAD_BYTES,
    DocumentValidationError,
    document_filename,
    document_view,
    store_document,
)

router = APIRouter(prefix="/api/knowledge", tags=["Knowledge documents"])


@router.get("")
def list_documents(session: SessionDep):
    return [document_view(session, doc) for doc in session.scalars(select(UploadedDocument).order_by(UploadedDocument.id.desc()))]


@router.post("")
async def upload_document(file: UploadFile, session: SessionDep):
    try:
        filename = document_filename(file.filename or "document")
        content = await file.read(MAX_UPLOAD_BYTES + 1)
    except DocumentValidationError as exc:
        raise HTTPException(exc.status_code, str(exc)) from None
    finally:
        await file.close()
    try:
        doc = store_document(session, filename, content)
        session.commit()
    except DocumentValidationError as exc:
        raise HTTPException(exc.status_code, str(exc)) from None
    return document_view(session, doc)


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
