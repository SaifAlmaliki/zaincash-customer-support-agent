"""Stable intake errors. Public messages never include provider or storage details."""
from __future__ import annotations


class IntakeError(Exception):
    code = "intake_error"
    public_message = "The conversation could not be updated."

    def __init__(self, message: str | None = None, *, trace: list | None = None) -> None:
        self.message = message or self.public_message
        self.trace = list(trace or [])
        super().__init__(self.message)


class NotOwned(IntakeError):
    code = "not_owned"
    public_message = "Conversation not found."


class RevisionConflict(IntakeError):
    code = "revision_conflict"
    public_message = "Reload the current conversation."


class OperationConflict(IntakeError):
    code = "operation_conflict"
    public_message = "This request was already used with different content."


class TurnBusy(IntakeError):
    code = "turn_busy"
    public_message = "This conversation is still being updated."


class InvalidEvidence(IntakeError):
    code = "invalid_evidence"
    public_message = "The assistant proposal was not supported by the conversation."


class ImageRejected(IntakeError):
    code = "image_rejected"
    public_message = "This image cannot be accepted."


class ModelUnavailable(IntakeError):
    code = "model_unavailable"
    public_message = "The assistant is temporarily unavailable. Your message was kept."


class StaleReview(IntakeError):
    code = "stale_review"
    public_message = "Review the latest summary before submitting."
