"""Employee-facing intake evidence. Draft attachments are never served from a result."""
from __future__ import annotations

from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.models import TicketResultRow
from app.intake.contracts import ImageInput
from app.intake.db_models import IntakeSubmissionRow
from app.intake.errors import NotOwned


def intake_result_view(session: Session, ticket_id: int) -> dict | None:
    submission = session.scalar(select(IntakeSubmissionRow).where(IntakeSubmissionRow.ticket_id == ticket_id))
    if submission is None:
        return None
    snap = dict(submission.snapshot or {})
    attachments = []
    for item in snap.get("attachments") or []:
        attachments.append({key: value for key, value in item.items() if key not in {"storage_key", "content_hash"}})
    submitted = submission.submitted_at.isoformat() if hasattr(submission.submitted_at, "isoformat") else snap.get("submitted_at")
    return {
        "summary_ar": snap.get("employee_text_ar") or snap.get("summary_ar") or "",
        "quality": snap.get("quality"),
        "facts": snap.get("facts") or {},
        "additional_issues": snap.get("additional_issues") or [],
        "unknown_keys": snap.get("unknown_keys") or [],
        "messages": snap.get("messages") or [],
        "attachments": attachments,
        "submitted_at": submitted,
    }


def employee_attachment(session: Session, result_id: int, attachment_id: UUID, store) -> ImageInput:
    result = session.get(TicketResultRow, result_id)
    submission = None if result is None else session.scalar(
        select(IntakeSubmissionRow).where(IntakeSubmissionRow.ticket_id == result.ticket_id)
    )
    allowed = set()
    if submission is not None:
        allowed.update(str(item) for item in (submission.snapshot.get("attachment_ids") or []))
        allowed.update(str(item.get("id")) for item in (submission.snapshot.get("attachments") or []) if item.get("id"))
    if submission is None or str(attachment_id) not in allowed:
        raise NotOwned("Conversation not found.")
    return store.load_for_session(submission.session_id, attachment_id)
