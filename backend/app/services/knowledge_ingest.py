"""Bounded CLI ingestion; source storage and index/cost ownership stay in kb/."""
from itertools import islice
from pathlib import Path

from sqlalchemy import or_, select

from app.db.document_models import UploadedDocument
from app.kb.documents import (
    MAX_UPLOAD_BYTES,
    TYPES,
    DocumentValidationError,
    document_view,
    store_document,
)
from app.kb.models import KnowledgeDocumentIndex

MAX_INGEST_DOCUMENTS = 100


def ingest_paths(path: Path) -> list[Path]:
    if path.is_file():
        return [path]
    paths = list(islice((p for p in path.rglob("*") if p.is_file() and p.suffix.lower() in TYPES),
                        MAX_INGEST_DOCUMENTS + 1))
    if not paths:
        raise ValueError("No PDF, Markdown or text documents found.")
    if len(paths) > MAX_INGEST_DOCUMENTS:
        raise ValueError("Ingest at most 100 documents per invocation.")
    return sorted(paths, key=lambda p: p.relative_to(path).as_posix())


def retry_ids(session_factory):
    with session_factory() as session:
        return list(session.scalars(select(UploadedDocument.id).outerjoin(KnowledgeDocumentIndex).where(or_(
            KnowledgeDocumentIndex.document_id.is_(None),
            KnowledgeDocumentIndex.status.in_(["awaiting_indexing", "failed"]),
        )).order_by(UploadedDocument.id).limit(MAX_INGEST_DOCUMENTS + 1)))


def ingest_status(value):
    return {key: value[key] for key in ("id", "filename", "status", "chunk_count", "error", "cost_usd")}


async def ingest_one(session_factory, service, source: Path | int):
    document_id = source if isinstance(source, int) else None
    filename = source.name if isinstance(source, Path) else None
    try:
        with session_factory() as session:
            if isinstance(source, Path):
                with source.open("rb") as file:
                    content = file.read(MAX_UPLOAD_BYTES + 1)
                document = store_document(session, source.name, content)
                session.commit()  # The indexer opens its own sessions after this commit.
            else:
                document = session.get(UploadedDocument, source)
            if document is None:
                raise ValueError("Document no longer exists.")
            value = document_view(session, document)
            document_id, filename = document.id, document.filename
        if value["status"] not in ("indexed", "indexing"):
            value = await service.index_document(document_id)
        return ingest_status(value)
    except Exception as exc:
        return {"id": document_id, "filename": filename, "status": "failed", "chunk_count": 0,
                "error": str(exc) if isinstance(exc, DocumentValidationError) else "Ingestion failed; check source, database and provider, then retry.",
                "cost_usd": getattr(exc, "cost_usd", 0.0)}
