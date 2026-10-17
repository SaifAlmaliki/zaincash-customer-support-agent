"""Source upload validation shared by HTTP, indexing and future CLI consumers."""
from hashlib import sha256
from pathlib import PurePath

from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import Session

from app.db.document_models import UploadedDocument
from app.kb.models import KnowledgeDocumentIndex
from app.kb.parse import MAX_UPLOAD_BYTES

TYPES = {".pdf": "application/pdf", ".md": "text/markdown", ".txt": "text/plain"}


class DocumentValidationError(ValueError):
    def __init__(self, message: str, *, status_code: int = 422) -> None:
        super().__init__(message)
        self.status_code = status_code


def document_filename(filename: str) -> str:
    """Normalize a browser-supplied name and reject unsupported source types."""
    filename = PurePath((filename or "document").replace("\\", "/")).name[:255]
    if PurePath(filename).suffix.lower() not in TYPES:
        raise DocumentValidationError("Upload a PDF, Markdown or UTF-8 text document.")
    return filename


def store_document(session: Session, filename: str, content: bytes) -> UploadedDocument:
    """Validate/upsert source bytes. The caller owns commit/rollback of this session."""
    filename = document_filename(filename)
    suffix = PurePath(filename).suffix.lower()
    if not content or len(content) > MAX_UPLOAD_BYTES:
        raise DocumentValidationError(
            "Upload a nonempty document smaller than 10 MB.", status_code=413,
        )
    if suffix == ".pdf" and not content.startswith(b"%PDF-"):
        raise DocumentValidationError("This file is not a valid PDF.")
    if suffix != ".pdf":
        try:
            content.decode("utf-8-sig")
        except UnicodeDecodeError:
            raise DocumentValidationError("Text documents must use UTF-8 encoding.") from None
    digest = sha256(content).hexdigest()
    document = session.scalar(insert(UploadedDocument).values(
        filename=filename, sha256=digest, content=content, content_type=TYPES[suffix],
    ).on_conflict_do_nothing(index_elements=[UploadedDocument.sha256]).returning(UploadedDocument))
    if document is None:
        document = session.scalar(select(UploadedDocument).where(UploadedDocument.sha256 == digest))
    return document


def document_view(session: Session, document: UploadedDocument) -> dict:
    """Project old sources and real lifecycle metadata without source bytes/vectors."""
    index = session.get(KnowledgeDocumentIndex, document.id)
    return {
        "id": document.id, "filename": document.filename, "sha256": document.sha256,
        "size": len(document.content), "created_at": document.created_at,
        "content_type": document.content_type,
        "status": index.status if index else "awaiting_indexing",
        "category_tags": list(index.category_tags) if index else [],
        "chunk_count": index.chunk_count if index else 0,
        "embedding_model": index.embedding_model if index else None,
        "embedding_dimensions": index.embedding_dimensions if index else None,
        "chunking_version": index.chunking_version if index else None,
        "indexed_at": index.indexed_at if index else None,
        "updated_at": index.updated_at if index else document.created_at,
        "error": index.error if index else None,
        "cost_usd": index.cost_usd if index else 0.0,
    }
