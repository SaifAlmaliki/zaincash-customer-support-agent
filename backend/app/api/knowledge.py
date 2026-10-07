from hashlib import sha256
from pathlib import PurePath
from urllib.parse import quote

from fastapi import APIRouter, Depends, HTTPException, Response, UploadFile
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from app.api.dependencies import get_session
from app.db.document_models import UploadedDocument

router = APIRouter(prefix="/api/knowledge", tags=["Knowledge documents"])
MAX_UPLOAD_BYTES = 10 * 1024 * 1024
TYPES = {".pdf": "application/pdf", ".md": "text/markdown", ".txt": "text/plain"}


def document_view(doc):
    return {"id": doc.id, "filename": doc.filename, "sha256": doc.sha256,
            "size": len(doc.content), "created_at": doc.created_at,
            "status": "awaiting_indexing", "content_type": doc.content_type}


@router.get("")
def list_documents(session=Depends(get_session)):
    return [document_view(doc) for doc in session.scalars(select(UploadedDocument).order_by(UploadedDocument.id.desc()))]


@router.post("")
async def upload_document(file: UploadFile, session=Depends(get_session)):
    filename = PurePath((file.filename or "document").replace("\\", "/")).name[:255]
    suffix = PurePath(filename).suffix.lower()
    if suffix not in TYPES:
        raise HTTPException(422, "Upload a PDF, Markdown or UTF-8 text document.")
    content = await file.read(MAX_UPLOAD_BYTES + 1)
    await file.close()
    if not content or len(content) > MAX_UPLOAD_BYTES:
        raise HTTPException(413, "Upload a nonempty document smaller than 10 MB.")
    if suffix == ".pdf" and not content.startswith(b"%PDF-"):
        raise HTTPException(422, "This file is not a valid PDF.")
    if suffix != ".pdf":
        try:
            content.decode("utf-8-sig")
        except UnicodeDecodeError as exc:
            raise HTTPException(422, "Text documents must use UTF-8 encoding.") from exc
    digest = sha256(content).hexdigest()
    existing = session.scalar(select(UploadedDocument).where(UploadedDocument.sha256 == digest))
    if existing:
        return document_view(existing)
    doc = UploadedDocument(filename=filename, sha256=digest, content=content, content_type=TYPES[suffix])
    session.add(doc)
    try:
        session.commit()
    except IntegrityError:
        session.rollback()
        doc = session.scalar(select(UploadedDocument).where(UploadedDocument.sha256 == digest))
    session.refresh(doc)
    return document_view(doc)


@router.get("/{document_id}/download")
def download_document(document_id: int, session=Depends(get_session)):
    doc = session.get(UploadedDocument, document_id)
    if not doc:
        raise HTTPException(404, "Document not found.")
    return Response(doc.content, media_type=doc.content_type,
                    headers={"Content-Disposition": f"attachment; filename*=UTF-8''{quote(doc.filename)}"})


@router.delete("/{document_id}", status_code=204)
def delete_document(document_id: int, session=Depends(get_session)):
    doc = session.get(UploadedDocument, document_id)
    if not doc:
        raise HTTPException(404, "Document not found.")
    session.delete(doc)
    session.commit()
