"""Durable intake tables. Registered on the shared metadata before create_all."""
from __future__ import annotations

import uuid
from datetime import datetime

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String, Text, UniqueConstraint, func
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.db.models import Base


class IntakeSessionRow(Base):
    __tablename__ = "intake_sessions"
    id: Mapped[uuid.UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    token_hash: Mapped[str] = mapped_column(String(64))
    revision: Mapped[int] = mapped_column(Integer, default=0)
    phase: Mapped[str] = mapped_column(String(32), default="collecting")
    turn_status: Mapped[str] = mapped_column(String(32), default="idle")
    language: Mapped[str] = mapped_column(String(8), default="ar")
    state: Mapped[dict] = mapped_column(JSONB)
    review: Mapped[dict | None] = mapped_column(JSONB)
    active_request_id: Mapped[uuid.UUID | None] = mapped_column(PG_UUID(as_uuid=True))
    error_code: Mapped[str | None] = mapped_column(String(64))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


class IntakeOperationRow(Base):
    __tablename__ = "intake_operations"
    __table_args__ = (UniqueConstraint("session_id", "request_id", name="uq_intake_operation_request"),)
    id: Mapped[uuid.UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    session_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("intake_sessions.id", ondelete="CASCADE"))
    request_id: Mapped[uuid.UUID] = mapped_column(PG_UUID(as_uuid=True))
    kind: Mapped[str] = mapped_column(String(32))
    fingerprint: Mapped[str] = mapped_column(String(64))
    status: Mapped[str] = mapped_column(String(32))
    attempt_id: Mapped[uuid.UUID] = mapped_column(PG_UUID(as_uuid=True))
    claimed_revision: Mapped[int] = mapped_column(Integer)
    request_json: Mapped[dict] = mapped_column(JSONB)
    result_json: Mapped[dict | None] = mapped_column(JSONB)
    error_code: Mapped[str | None] = mapped_column(String(64))
    usage: Mapped[list | None] = mapped_column(JSONB)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


class IntakeMessageRow(Base):
    __tablename__ = "intake_messages"
    __table_args__ = (UniqueConstraint("session_id", "sequence", name="uq_intake_message_sequence"),)
    id: Mapped[uuid.UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    session_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("intake_sessions.id", ondelete="CASCADE"))
    sequence: Mapped[int] = mapped_column(Integer)
    role: Mapped[str] = mapped_column(String(16))
    text: Mapped[str] = mapped_column(Text)
    language: Mapped[str] = mapped_column(String(8))
    operation_id: Mapped[uuid.UUID | None] = mapped_column(ForeignKey("intake_operations.id"))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))


class IntakeAttachmentRow(Base):
    __tablename__ = "intake_attachments"
    id: Mapped[uuid.UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    session_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("intake_sessions.id", ondelete="CASCADE"))
    message_id: Mapped[uuid.UUID | None] = mapped_column(ForeignKey("intake_messages.id"))
    operation_id: Mapped[uuid.UUID | None] = mapped_column(ForeignKey("intake_operations.id"))
    request_id: Mapped[uuid.UUID | None] = mapped_column(PG_UUID(as_uuid=True))
    storage_key: Mapped[str] = mapped_column(String(256))
    content_hash: Mapped[str] = mapped_column(String(64))
    filename: Mapped[str] = mapped_column(String(256))
    mime_type: Mapped[str] = mapped_column(String(64))
    size: Mapped[int] = mapped_column(Integer)
    width: Mapped[int] = mapped_column(Integer)
    height: Mapped[int] = mapped_column(Integer)
    removed: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


class IntakeSubmissionRow(Base):
    __tablename__ = "intake_submissions"
    id: Mapped[uuid.UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    session_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("intake_sessions.id", ondelete="CASCADE"), unique=True)
    ticket_id: Mapped[int] = mapped_column(ForeignKey("tickets.id"), unique=True)
    run_id: Mapped[int] = mapped_column(ForeignKey("runs.id"))
    result_id: Mapped[int] = mapped_column(ForeignKey("ticket_results.id"))
    review_id: Mapped[uuid.UUID] = mapped_column(PG_UUID(as_uuid=True))
    request_id: Mapped[uuid.UUID] = mapped_column(PG_UUID(as_uuid=True))
    snapshot: Mapped[dict] = mapped_column(JSONB)
    submitted_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
