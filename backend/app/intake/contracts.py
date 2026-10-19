"""Public and internal intake contracts. JSON state is always dumped with mode='json'."""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Literal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, field_validator

Language = Literal["ar", "en"]
FactStatus = Literal["known", "missing", "unknown", "conflicting", "not_applicable"]
Phase = Literal["collecting", "review_ready", "submitted"]
TurnStatus = Literal["idle", "processing", "retryable_failure"]
Quality = Literal["collecting", "sufficient_context", "partial_context"]
ReviewQuality = Literal["sufficient_context", "partial_context"]
ProcessingStatus = Literal["processing", "ready_for_employee", "needs_attention"]


def _aware(value: datetime) -> datetime:
    if value.tzinfo is None or value.tzinfo.utcoffset(value) is None:
        raise ValueError("datetime must be timezone-aware")
    return value


class IntakeModel(BaseModel):
    model_config = ConfigDict(extra="forbid")


class EvidenceRef(IntakeModel):
    kind: Literal["message", "image"]
    source_id: UUID
    quote: str


class Fact(IntakeModel):
    key: str
    status: FactStatus
    value: str | None = None
    normalized: str | None = None
    evidence: list[EvidenceRef] = Field(default_factory=list)
    supersedes: list[EvidenceRef] = Field(default_factory=list)


class Question(IntakeModel):
    key: str
    text: str
    reason: str
    basis_revision: int


class QuestionRecord(IntakeModel):
    key: str
    basis_revision: int
    message_id: UUID
    outcome: Literal["asked", "answered", "unknown"]


class Message(IntakeModel):
    id: UUID
    role: Literal["user", "assistant"]
    text: str
    language: Language
    created_at: datetime
    attachment_ids: list[UUID] = Field(default_factory=list)

    @field_validator("created_at")
    @classmethod
    def timezone_aware(cls, value: datetime) -> datetime:
        return _aware(value)


class Attachment(IntakeModel):
    id: UUID
    filename: str
    mime_type: str
    size: int
    width: int
    height: int
    message_id: UUID | None = None
    removed: bool = False


class Readiness(IntakeModel):
    quality: Quality
    missing: list[str] = Field(default_factory=list)
    conflicts: list[str] = Field(default_factory=list)
    reason: str
    next_key: str | None = None


class IntakeState(IntakeModel):
    language: Language = "ar"
    category: str = "other"
    facts: dict[str, Fact] = Field(default_factory=dict)
    additional_issues: list[Fact] = Field(default_factory=list)
    additional_needed: list[str] = Field(default_factory=list)
    questions: list[QuestionRecord] = Field(default_factory=list)
    readiness: Readiness = Field(
        default_factory=lambda: Readiness(
            quality="collecting", missing=["issue"], conflicts=[], reason="Waiting for the customer's report.", next_key="issue"
        )
    )


class Analysis(IntakeModel):
    language: Language
    category: str
    updates: list[Fact] = Field(default_factory=list)
    additional_issues: list[Fact] = Field(default_factory=list)
    suggested_question: Question | None = None
    additional_needed: list[str] = Field(default_factory=list)
    reinspect_images: list[UUID] = Field(default_factory=list)


class ReviewText(IntakeModel):
    customer_text: str
    employee_text_ar: str
    fact_keys: list[str] = Field(default_factory=list)


class ReviewSnapshot(IntakeModel):
    id: UUID
    revision: int
    language: Language
    quality: ReviewQuality
    facts: dict[str, Fact] = Field(default_factory=dict)
    additional_issues: list[Fact] = Field(default_factory=list)
    unknown_keys: list[str] = Field(default_factory=list)
    customer_text: str
    employee_text_ar: str
    ticket_text_ar: str
    attachment_ids: list[UUID] = Field(default_factory=list)


class Receipt(IntakeModel):
    ticket_reference: str
    submitted_at: datetime
    processing_status: ProcessingStatus

    @field_validator("submitted_at")
    @classmethod
    def timezone_aware(cls, value: datetime) -> datetime:
        return _aware(value)


class CustomerReview(IntakeModel):
    id: UUID
    revision: int
    language: Language
    quality: ReviewQuality
    text: str
    facts: dict[str, Fact] = Field(default_factory=dict)
    additional_issues: list[Fact] = Field(default_factory=list)
    unknown_keys: list[str] = Field(default_factory=list)
    attachment_ids: list[UUID] = Field(default_factory=list)


class SessionView(IntakeModel):
    id: UUID
    revision: int
    phase: Phase
    language: Language
    turn_status: TurnStatus
    active_request_id: UUID | None = None
    messages: list[Message] = Field(default_factory=list)
    attachments: list[Attachment] = Field(default_factory=list)
    readiness: Readiness
    review: CustomerReview | None = None
    receipt: Receipt | None = None
    error_code: str | None = None


class Credentials(IntakeModel):
    session_id: UUID
    token: str


@dataclass
class ImageInput:
    id: UUID
    mime_type: str
    data: bytes


@dataclass
class TurnContext:
    session_id: UUID
    revision: int
    state: IntakeState
    messages: list[Message]
    attachments: list[Attachment]
    current_message_id: UUID | None
    needs_analysis: bool = False


@dataclass
class TurnResult:
    state: IntakeState
    assistant_text: str | None
    review: ReviewSnapshot | None
    trace: list[dict] = field(default_factory=list)


@dataclass
class ModelCall:
    value: Analysis | ReviewText
    trace: list[dict] = field(default_factory=list)


@dataclass
class OperationClaim:
    session_id: UUID
    request_id: UUID
    attempt_id: UUID
    revision: int
    context: TurnContext
    kind: str = "message"
    payload: dict = field(default_factory=dict)
