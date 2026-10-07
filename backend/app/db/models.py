from __future__ import annotations

from datetime import datetime

from sqlalchemy import (
    BigInteger, Boolean, DateTime, Float, ForeignKey, Integer, String, Text, UniqueConstraint, func,
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class TicketRow(Base):
    __tablename__ = "tickets"
    id: Mapped[int] = mapped_column(primary_key=True)
    external_id: Mapped[str] = mapped_column(String(128), unique=True)
    channel: Mapped[str] = mapped_column(String(32), default="app")
    customer_phone: Mapped[str | None] = mapped_column(String(32))
    text: Mapped[str] = mapped_column(Text)
    received_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    source: Mapped[str] = mapped_column(String(16))
    batch_id: Mapped[str | None] = mapped_column(String(64))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


class RunRow(Base):
    __tablename__ = "runs"
    id: Mapped[int] = mapped_column(primary_key=True)
    started_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    finished_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    mode: Mapped[str] = mapped_column(String(16))
    prompt_version: Mapped[str] = mapped_column(String(16))
    model_ids: Mapped[dict] = mapped_column(JSONB, default=dict)
    degraded: Mapped[bool] = mapped_column(Boolean, default=False)
    counts: Mapped[dict] = mapped_column(JSONB, default=dict)
    total_cost_usd: Mapped[float] = mapped_column(Float, default=0.0)
    status: Mapped[str] = mapped_column(String(16), default="running")


class TicketResultRow(Base):
    __tablename__ = "ticket_results"
    __table_args__ = (UniqueConstraint("run_id", "ticket_id", name="uq_result_run_ticket"),)
    id: Mapped[int] = mapped_column(primary_key=True)
    run_id: Mapped[int] = mapped_column(ForeignKey("runs.id", ondelete="CASCADE"))
    ticket_id: Mapped[int] = mapped_column(ForeignKey("tickets.id", ondelete="CASCADE"))
    category: Mapped[str | None] = mapped_column(String(64))
    category_confidence: Mapped[float | None] = mapped_column(Float)
    category_probs: Mapped[dict] = mapped_column(JSONB, default=dict)
    priority: Mapped[str | None] = mapped_column(String(4))
    priority_confidence: Mapped[float | None] = mapped_column(Float)
    flags: Mapped[dict] = mapped_column(JSONB, default=dict)
    classifier_path: Mapped[str | None] = mapped_column(String(32))
    extracted: Mapped[dict] = mapped_column(JSONB, default=dict)
    lookup_status: Mapped[str | None] = mapped_column(String(32))
    matched_txn_ref: Mapped[str | None] = mapped_column(String(32))
    team: Mapped[str | None] = mapped_column(String(64))
    escalated: Mapped[bool] = mapped_column(Boolean, default=False)
    escalation_reasons: Mapped[list] = mapped_column(JSONB, default=list)
    escalation_note: Mapped[str | None] = mapped_column(Text)
    draft_text: Mapped[str | None] = mapped_column(Text)
    citations: Mapped[list] = mapped_column(JSONB, default=list)
    agent_trace: Mapped[list] = mapped_column(JSONB, default=list)
    status: Mapped[str] = mapped_column(String(32))
    error: Mapped[str | None] = mapped_column(Text)
    latency_ms: Mapped[int] = mapped_column(Integer, default=0)
    cost_usd: Mapped[float] = mapped_column(Float, default=0.0)
    jev_model_version: Mapped[str | None] = mapped_column(String(32))
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )


class ReviewRow(Base):
    __tablename__ = "reviews"
    id: Mapped[int] = mapped_column(primary_key=True)
    result_id: Mapped[int] = mapped_column(ForeignKey("ticket_results.id", ondelete="CASCADE"))
    reviewer: Mapped[str] = mapped_column(String(64))
    action: Mapped[str] = mapped_column(String(16))
    final_text: Mapped[str | None] = mapped_column(Text)
    edit_distance: Mapped[int | None] = mapped_column(Integer)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


class TransactionRow(Base):
    __tablename__ = "transactions"
    txn_ref: Mapped[str] = mapped_column(String(32), primary_key=True)
    sender_phone: Mapped[str] = mapped_column(String(32), index=True)
    receiver_phone: Mapped[str | None] = mapped_column(String(32), index=True)
    receiver_name: Mapped[str | None] = mapped_column(String(128))
    amount_iqd: Mapped[int] = mapped_column(BigInteger)
    type: Mapped[str] = mapped_column(String(16))
    status: Mapped[str] = mapped_column(String(16))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), index=True)
    biller: Mapped[str | None] = mapped_column(String(64))
    agent_id: Mapped[str | None] = mapped_column(String(32))
    failure_reason: Mapped[str | None] = mapped_column(String(128))


class IncidentRow(Base):
    __tablename__ = "service_incidents"
    id: Mapped[str] = mapped_column(String(32), primary_key=True)
    service: Mapped[str] = mapped_column(String(64))
    started_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    ended_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    description: Mapped[str] = mapped_column(Text)
