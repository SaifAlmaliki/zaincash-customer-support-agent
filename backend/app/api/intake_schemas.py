"""Customer intake HTTP models. These omit token hashes, storage keys, and model traces."""
from __future__ import annotations

from typing import Literal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class IntakeBody(BaseModel):
    model_config = ConfigDict(extra="forbid")


class CreateSessionInput(IntakeBody):
    language: Literal["ar", "en"]


class MessageInput(IntakeBody):
    request_id: UUID
    expected_revision: int = Field(ge=0)
    text: str = Field(default="", max_length=6000)
    language: Literal["ar", "en"]
    attachment_ids: list[UUID] = Field(default_factory=list)

class ReviewInput(IntakeBody):
    request_id: UUID
    expected_revision: int = Field(ge=0)
    allow_partial: bool
    language: Literal["ar", "en"]


class RetryInput(IntakeBody):
    expected_revision: int = Field(ge=0)


class RemoveInput(IntakeBody):
    request_id: UUID
    expected_revision: int = Field(ge=0)


class SubmitInput(IntakeBody):
    request_id: UUID
    expected_revision: int = Field(ge=0)
    review_id: UUID
    confirmed: bool
