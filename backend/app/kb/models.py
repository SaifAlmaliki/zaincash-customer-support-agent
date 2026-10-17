"""Derived knowledge data; deleting the source cascades through both tables."""
from datetime import datetime

from pgvector.sqlalchemy import Vector
from sqlalchemy import DateTime, Float, ForeignKey, Index, String, Text, UniqueConstraint, func
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import Mapped, mapped_column

from app.db.models import Base


class KnowledgeDocumentIndex(Base):
    __tablename__ = "kb_document_indexes"

    document_id: Mapped[int] = mapped_column(
        ForeignKey("uploaded_documents.id", ondelete="CASCADE"), primary_key=True,
    )
    status: Mapped[str] = mapped_column(String(32), default="awaiting_indexing")
    attempt_id: Mapped[str | None] = mapped_column(String(36))
    embedding_model: Mapped[str] = mapped_column(String(255))
    embedding_dimensions: Mapped[int]
    chunking_version: Mapped[str] = mapped_column(String(64))
    category_tags: Mapped[list[str]] = mapped_column(ARRAY(String(64)), default=list)
    chunk_count: Mapped[int] = mapped_column(default=0)
    cost_usd: Mapped[float] = mapped_column(Float, default=0.0)
    error: Mapped[str | None] = mapped_column(String(512))
    indexed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now(),
    )


class KnowledgeChunk(Base):
    __tablename__ = "kb_chunks"
    __table_args__ = (
        UniqueConstraint("document_id", "chunk_index", name="uq_kb_document_chunk"),
        Index("ix_kb_chunks_embedding", "embedding", postgresql_using="hnsw",
              postgresql_ops={"embedding": "vector_cosine_ops"}),
    )

    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    document_id: Mapped[int] = mapped_column(
        ForeignKey("kb_document_indexes.document_id", ondelete="CASCADE"), index=True,
    )
    attempt_id: Mapped[str] = mapped_column(String(36))
    chunk_index: Mapped[int]
    text: Mapped[str] = mapped_column(Text)
    filename: Mapped[str] = mapped_column(String(255))
    page_start: Mapped[int | None]
    page_end: Mapped[int | None]
    category_tags: Mapped[list[str]] = mapped_column(ARRAY(String(64)), default=list)
    embedding_model: Mapped[str] = mapped_column(String(255))
    embedding: Mapped[list[float]] = mapped_column(Vector(768))
