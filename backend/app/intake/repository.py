"""Session ownership and the customer projection. Tokens are stored only as hashes."""
from __future__ import annotations

import hashlib
import json
import secrets
import uuid
from datetime import UTC, datetime

from sqlalchemy import select
from sqlalchemy.orm import Session, sessionmaker

from app.db.models import TicketResultRow, TicketRow
from app.intake.contracts import (
    Attachment,
    Credentials,
    CustomerReview,
    IntakeState,
    Message,
    Readiness,
    Receipt,
    ReviewSnapshot,
    SessionView,
    TurnContext,
)
from app.intake.db_models import (
    IntakeAttachmentRow,
    IntakeMessageRow,
    IntakeSessionRow,
    IntakeSubmissionRow,
)
from app.intake.errors import NotOwned, OperationConflict


def operation_fingerprint(kind: str, payload: dict) -> str:
    stable = {key: value for key, value in payload.items() if key != "expected_revision"}
    raw = json.dumps([kind, stable], sort_keys=True, separators=(",", ":"), ensure_ascii=False, default=str)
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()


def assert_same_operation(stored: str, incoming: str) -> None:
    if not secrets.compare_digest(stored, incoming):
        raise OperationConflict("This request was already used with different content.")


def new_access_token() -> tuple[str, str]:
    token = secrets.token_urlsafe(32)
    return token, hashlib.sha256(token.encode("utf-8")).hexdigest()


def processing_status(result_status: str) -> str:
    if result_status == "processing":
        return "processing"
    if result_status == "failed":
        return "needs_attention"
    return "ready_for_employee"


def initial_state(language: str) -> IntakeState:
    return IntakeState(
        language=language,
        category="other",
        facts={},
        additional_issues=[],
        additional_needed=[],
        questions=[],
        readiness=Readiness(
            quality="collecting",
            missing=["issue"],
            conflicts=[],
            reason="Waiting for the customer's report.",
            next_key="issue",
        ),
    )


def _message(row: IntakeMessageRow, attachment_ids: list) -> Message:
    return Message(
        id=row.id,
        role=row.role,
        text=row.text,
        language=row.language,
        created_at=row.created_at,
        attachment_ids=attachment_ids,
    )


def _attachment(row: IntakeAttachmentRow) -> Attachment:
    return Attachment(
        id=row.id,
        filename=row.filename,
        mime_type=row.mime_type,
        size=row.size,
        width=row.width,
        height=row.height,
        message_id=row.message_id,
        removed=row.removed,
    )


def load_messages(session: Session, session_id: uuid.UUID) -> list[Message]:
    rows = list(session.scalars(
        select(IntakeMessageRow).where(IntakeMessageRow.session_id == session_id).order_by(IntakeMessageRow.sequence)
    ))
    attachments = list(session.scalars(select(IntakeAttachmentRow).where(IntakeAttachmentRow.session_id == session_id)))
    by_message: dict = {}
    for item in attachments:
        if item.message_id is not None:
            by_message.setdefault(item.message_id, []).append(item.id)
    return [_message(row, by_message.get(row.id, [])) for row in rows]


def load_attachments(session: Session, session_id: uuid.UUID) -> list[Attachment]:
    rows = session.scalars(
        select(IntakeAttachmentRow)
        .where(IntakeAttachmentRow.session_id == session_id)
        .order_by(IntakeAttachmentRow.created_at, IntakeAttachmentRow.id)
    )
    return [_attachment(row) for row in rows]


def customer_review(data: dict | None) -> CustomerReview | None:
    if not data:
        return None
    snap = ReviewSnapshot.model_validate(data)
    return CustomerReview(
        id=snap.id,
        revision=snap.revision,
        language=snap.language,
        quality=snap.quality,
        text=snap.customer_text,
        facts=snap.facts,
        additional_issues=snap.additional_issues,
        unknown_keys=snap.unknown_keys,
        attachment_ids=snap.attachment_ids,
    )


def receipt_for(session: Session, row: IntakeSessionRow) -> Receipt | None:
    if row.phase != "submitted":
        return None
    submission = session.scalar(select(IntakeSubmissionRow).where(IntakeSubmissionRow.session_id == row.id))
    if submission is None:
        return None
    ticket = session.get(TicketRow, submission.ticket_id)
    result = session.scalar(
        select(TicketResultRow)
        .where(TicketResultRow.ticket_id == submission.ticket_id)
        .order_by(TicketResultRow.id.desc())
    )
    status = processing_status(result.status) if result is not None else "processing"
    return Receipt(ticket_reference=ticket.external_id, submitted_at=submission.submitted_at, processing_status=status)


def session_view(session: Session, row: IntakeSessionRow) -> SessionView:
    state = IntakeState.model_validate(row.state)
    return SessionView(
        id=row.id,
        revision=row.revision,
        phase=row.phase,
        language=row.language,
        turn_status=row.turn_status,
        active_request_id=row.active_request_id,
        messages=load_messages(session, row.id),
        attachments=load_attachments(session, row.id),
        readiness=state.readiness,
        review=customer_review(row.review),
        receipt=receipt_for(session, row),
        error_code=row.error_code,
    )


def turn_context(session: Session, row: IntakeSessionRow) -> TurnContext:
    messages = load_messages(session, row.id)
    current = next((item.id for item in reversed(messages) if item.role == "user"), None)
    return TurnContext(
        session_id=row.id,
        revision=row.revision,
        state=IntakeState.model_validate(row.state),
        messages=messages,
        attachments=load_attachments(session, row.id),
        current_message_id=current,
    )


class IntakeRepository:
    def __init__(self, session_factory: sessionmaker) -> None:
        self._sf = session_factory

    def create(self, language: str) -> tuple[Credentials, SessionView]:
        if language not in {"ar", "en"}:
            raise ValueError("language must be ar or en")
        token, token_hash = new_access_token()
        session_id = uuid.uuid4()
        now = datetime.now(UTC)
        with self._sf() as session:
            session.add(IntakeSessionRow(
                id=session_id,
                token_hash=token_hash,
                revision=0,
                phase="collecting",
                turn_status="idle",
                language=language,
                state=initial_state(language).model_dump(mode="json"),
                review=None,
                active_request_id=None,
                error_code=None,
                created_at=now,
                updated_at=now,
            ))
            session.commit()
        credentials = Credentials(session_id=session_id, token=token)
        return credentials, self.get(credentials)

    def get(self, credentials: Credentials) -> SessionView:
        with self._sf() as session:
            row = self.authenticate(session, credentials)
            return session_view(session, row)

    def authenticate(self, session: Session, credentials: Credentials, *, lock: bool = False) -> IntakeSessionRow:
        query = select(IntakeSessionRow).where(IntakeSessionRow.id == credentials.session_id)
        if lock:
            query = query.with_for_update()
        row = session.scalar(query)
        digest = hashlib.sha256(credentials.token.encode("utf-8")).hexdigest()
        if row is None or not secrets.compare_digest(row.token_hash, digest):
            raise NotOwned("Conversation not found.")
        return row
