from dataclasses import dataclass
from datetime import UTC, datetime
from typing import Literal

from sqlalchemy import select

from app.db.models import ReviewRow, TicketResultRow


@dataclass(frozen=True)
class ReviewCommand:
    action: Literal["approve", "edit_approve", "reject", "reassign"]
    reviewer: str
    final_text: str | None
    team: str | None
    expected_updated_at: datetime


class ReviewNotFound(LookupError):
    pass


class ReviewConflict(RuntimeError):
    pass


class InvalidReviewTeam(ValueError):
    pass


def record_review(session, result_id: int, review: ReviewCommand, teams):
    result = session.scalar(select(TicketResultRow).where(TicketResultRow.id == result_id).with_for_update())
    if result is None:
        raise ReviewNotFound("Ticket result not found.")
    if result.updated_at != review.expected_updated_at:
        raise ReviewConflict("This ticket was updated by another reviewer. Refresh before saving.")
    if result.status == "processing":
        raise ReviewConflict("This ticket is still processing.")
    if result.status == "failed":
        raise ReviewConflict("Processing failed. Run the ticket again before reviewing it.")
    final_text = (review.final_text or "").strip() or None
    if review.action == "reassign":
        if review.team not in teams:
            raise InvalidReviewTeam("Select a valid support team.")
        final_text = f"Assigned from {result.team} to {review.team}"
        result.team = review.team
    else:
        result.status = {"approve": "approved", "edit_approve": "edited", "reject": "rejected"}[review.action]
    # Keep the original generated draft intact; the reviewed text belongs to the audit record.
    session.add(ReviewRow(result_id=result.id, reviewer=review.reviewer, action=review.action,
                          final_text=final_text, edit_distance=None))
    result.updated_at = datetime.now(UTC)
    session.commit()
    session.refresh(result)
    return result
