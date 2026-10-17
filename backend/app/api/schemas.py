from datetime import UTC, datetime
from typing import Literal
from uuid import uuid4

from pydantic import BaseModel, Field, field_validator, model_validator

from app.pipeline.stage1_normalize.normalize import sanitize_for_storage

Mode = Literal["jev", "gemini", "cascade"]


class TicketInput(BaseModel):
    external_id: str = Field(default_factory=lambda: f"UI-{uuid4().hex[:12]}", max_length=128)
    text: str = Field(min_length=1, max_length=6000)
    received_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    channel: Literal["app", "whatsapp", "call_note"] = "app"
    customer_phone: str | None = Field(default=None, max_length=32)

    @field_validator("text")
    @classmethod
    def clean_text(cls, value):
        value = sanitize_for_storage(value)
        if not value:
            raise ValueError("Enter a ticket message.")
        return value

    @field_validator("external_id")
    @classmethod
    def nonempty_id(cls, value):
        if not value.strip():
            raise ValueError("Ticket ID cannot be blank.")
        return value.strip()

    @field_validator("received_at")
    @classmethod
    def ensure_timezone(cls, value):
        if value.tzinfo is None:
            from app.pipeline.stage4_lookup.lookup import BAGHDAD
            value = value.replace(tzinfo=BAGHDAD)
        return value


class BatchInput(BaseModel):
    mode: Mode = "cascade"
    tickets: list[TicketInput] = Field(min_length=1, max_length=500)

    @model_validator(mode="after")
    def unique_ids(self):
        ids = [ticket.external_id for ticket in self.tickets]
        if len(set(ids)) != len(ids):
            raise ValueError("Each ticket in a batch must have a unique ID.")
        return self


class ReviewInput(BaseModel):
    action: Literal["approve", "edit_approve", "reject", "reassign"]
    reviewer: str = Field(min_length=1, max_length=64)
    final_text: str | None = Field(default=None, max_length=8000)
    team: str | None = None
    expected_updated_at: datetime

    @model_validator(mode="after")
    def validate_review(self):
        self.reviewer = self.reviewer.strip()
        if not self.reviewer:
            raise ValueError("A reviewer name is required.")
        if self.action in ("approve", "edit_approve") and not (self.final_text or "").strip():
            raise ValueError("Write a reply before approving it.")
        if self.action == "reassign" and not self.team:
            raise ValueError("Select a team.")
        return self


class KnowledgeIndexInput(BaseModel):
    category_tags: list[str] | None = Field(default=None, max_length=100)


class KnowledgeSearchInput(BaseModel):
    query: str = Field(min_length=1, max_length=2000)
    category: str | None = Field(default=None, max_length=64)
    k: int = Field(default=5, ge=1, le=10, strict=True)

    @field_validator("query")
    @classmethod
    def nonblank_query(cls, value):
        if not value.strip():
            raise ValueError("Enter a knowledge query.")
        return value.strip()
