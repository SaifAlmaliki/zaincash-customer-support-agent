"""Claim a customer turn, publish one result, and fence abandoned attempts."""
from __future__ import annotations

import uuid
from datetime import UTC, datetime

from sqlalchemy import func, select
from sqlalchemy.orm import sessionmaker

from app.intake.contracts import OperationClaim, SessionView, TurnResult
from app.intake.db_models import (
    IntakeAttachmentRow,
    IntakeMessageRow,
    IntakeOperationRow,
    IntakeSessionRow,
)
from app.intake.errors import ImageRejected, InvalidEvidence, RevisionConflict, TurnBusy
from app.intake.repository import (
    IntakeRepository,
    assert_same_operation,
    operation_fingerprint,
    session_view,
    turn_context,
)
from app.pipeline.stage1_normalize.normalize import sanitize_for_storage


def _jsonable(value):
    if isinstance(value, uuid.UUID):
        return str(value)
    if isinstance(value, list):
        return [_jsonable(item) for item in value]
    if isinstance(value, dict):
        return {key: _jsonable(item) for key, item in value.items() if key != "expected_revision"}
    return value


class TurnStore:
    def __init__(self, session_factory: sessionmaker, *, max_images_per_message: int = 3) -> None:
        self._sf = session_factory
        self.repo = IntakeRepository(session_factory)
        self.max_images_per_message = max_images_per_message

    def claim(self, credentials, kind: str, request_id: uuid.UUID, expected_revision: int, payload: dict):
        incoming = operation_fingerprint(kind, _jsonable(payload))
        with self._sf() as session:
            row = self.repo.authenticate(session, credentials, lock=True)
            operation = self._operation(session, row.id, request_id)
            if operation is not None:
                assert_same_operation(operation.fingerprint, incoming)
                if operation.status in {"completed", "processing", "failed", "interrupted"}:
                    return session_view(session, row)
            if row.turn_status == "processing":
                raise TurnBusy("This conversation is still being updated.")
            if row.phase == "submitted":
                raise RevisionConflict("This report was already submitted.")
            if row.revision != expected_revision:
                raise RevisionConflict("Reload the current conversation.")
            now = datetime.now(UTC)
            if kind == "message":
                self._append_customer_message(session, row, payload, now)
                row.revision += 1
                row.review = None
                if row.phase == "review_ready":
                    row.phase = "collecting"
            elif kind != "review":
                raise InvalidEvidence("Unsupported conversation operation.")
            row.turn_status = "processing"
            row.active_request_id = request_id
            row.error_code = None
            row.updated_at = now
            attempt_id = uuid.uuid4()
            stored_payload = _jsonable(payload)
            session.add(IntakeOperationRow(
                id=uuid.uuid4(), session_id=row.id, request_id=request_id, kind=kind,
                fingerprint=incoming, status="processing", attempt_id=attempt_id,
                claimed_revision=row.revision, request_json=stored_payload, result_json=None,
                error_code=None, usage=[], created_at=now, updated_at=now,
            ))
            session.commit()
            return OperationClaim(
                row.id, request_id, attempt_id, row.revision, turn_context(session, row), kind, stored_payload
            )

    def finish(self, claim: OperationClaim, result: TurnResult) -> SessionView:
        with self._sf() as session:
            row, operation = self._locked_attempt(session, claim)
            if row is None or operation is None:
                self._audit(claim, result.trace)
                raise RevisionConflict("Reload the current conversation.")
            publication = claim.revision + 1
            state = result.state
            assistant_id = None
            if result.assistant_text:
                assistant_id = uuid.uuid4()
                known = {item.id for item in turn_context(session, row).messages}
                rewritten = []
                for question in state.questions:
                    if question.message_id not in known:
                        question = question.model_copy(update={"message_id": assistant_id})
                    rewritten.append(question)
                state = state.model_copy(update={"questions": rewritten})
                session.add(self._message(
                    row.id, assistant_id, "assistant", result.assistant_text, state.language,
                    self._next_sequence(session, row.id), operation.id, datetime.now(UTC),
                ))
            review = None
            if result.review is not None:
                review = result.review.model_copy(update={"revision": publication})
                row.review = review.model_dump(mode="json")
                row.phase = "review_ready"
            row.state = state.model_dump(mode="json")
            row.language = state.language
            row.revision = publication
            row.turn_status = "idle"
            row.active_request_id = None
            row.error_code = None
            row.updated_at = datetime.now(UTC)
            operation.status = "completed"
            operation.error_code = None
            operation.usage = [*(operation.usage or []), *result.trace]
            operation.result_json = {"revision": publication, "review_id": None if review is None else str(review.id)}
            operation.updated_at = row.updated_at
            session.commit()
            return session_view(session, row)

    def fail(self, claim: OperationClaim, error_code: str, trace: list[dict]) -> SessionView:
        with self._sf() as session:
            row, operation = self._locked_attempt(session, claim)
            if row is None or operation is None:
                self._audit(claim, trace)
                raise RevisionConflict("Reload the current conversation.")
            now = datetime.now(UTC)
            operation.status = "failed"
            operation.error_code = error_code
            operation.usage = [*(operation.usage or []), *trace]
            operation.updated_at = now
            row.turn_status = "retryable_failure"
            row.error_code = error_code
            row.active_request_id = claim.request_id
            row.updated_at = now
            session.commit()
            return session_view(session, row)

    def retry(self, credentials, request_id: uuid.UUID, expected_revision: int):
        with self._sf() as session:
            row = self.repo.authenticate(session, credentials, lock=True)
            operation = self._operation(session, row.id, request_id)
            if operation is None:
                raise RevisionConflict("Reload the current conversation.")
            if operation.status == "completed":
                return session_view(session, row)
            if row.turn_status == "processing" and row.active_request_id == request_id:
                return session_view(session, row)
            if row.turn_status == "processing":
                raise TurnBusy("This conversation is still being updated.")
            if row.revision != expected_revision:
                raise RevisionConflict("Reload the current conversation.")
            if operation.status not in {"failed", "interrupted"}:
                raise RevisionConflict("Reload the current conversation.")
            now = datetime.now(UTC)
            attempt_id = uuid.uuid4()
            operation.attempt_id = attempt_id
            operation.status = "processing"
            operation.error_code = None
            operation.claimed_revision = row.revision
            operation.updated_at = now
            row.turn_status = "processing"
            row.error_code = None
            row.active_request_id = request_id
            row.updated_at = now
            session.commit()
            return OperationClaim(
                row.id, request_id, attempt_id, row.revision, turn_context(session, row),
                operation.kind, dict(operation.request_json or {}),
            )

    def recover_interrupted(self) -> int:
        with self._sf() as session:
            rows = list(session.scalars(select(IntakeOperationRow).where(IntakeOperationRow.status == "processing")))
            for operation in rows:
                operation.status = "interrupted"
                operation.updated_at = datetime.now(UTC)
                holder = session.get(IntakeSessionRow, operation.session_id)
                if holder and holder.active_request_id == operation.request_id and holder.turn_status == "processing":
                    holder.turn_status = "retryable_failure"
                    holder.error_code = "interrupted"
                    holder.updated_at = operation.updated_at
            session.commit()
            return len(rows)

    def _append_customer_message(self, session, row: IntakeSessionRow, payload: dict, now: datetime) -> None:
        text = sanitize_for_storage(str(payload.get("text") or ""))
        language = payload.get("language")
        if language not in {"ar", "en"}:
            raise InvalidEvidence("Choose Arabic or English.")
        attachment_ids = list(payload.get("attachment_ids") or [])
        if len(text) > 6000:
            raise InvalidEvidence("Message is too long.")
        if not text and not attachment_ids:
            raise InvalidEvidence("Enter a message or attach a screenshot.")
        if len(attachment_ids) != len(set(attachment_ids)):
            raise ImageRejected("Attach each screenshot once.")
        if len(attachment_ids) > self.max_images_per_message:
            raise ImageRejected("Attach at most three screenshots to one message.")
        message_id = uuid.uuid4()
        for attachment_id in attachment_ids:
            attachment = session.get(IntakeAttachmentRow, attachment_id)
            if attachment is None or attachment.session_id != row.id:
                raise ImageRejected("Attach a screenshot from this conversation.")
            if attachment.removed or attachment.message_id is not None:
                raise ImageRejected("That screenshot is no longer available.")
            attachment.message_id = message_id
        operation_id = None
        session.add(self._message(row.id, message_id, "user", text, language, self._next_sequence(session, row.id), operation_id, now))

    def _locked_attempt(self, session, claim: OperationClaim):
        row = session.scalar(select(IntakeSessionRow).where(IntakeSessionRow.id == claim.session_id).with_for_update())
        operation = None if row is None else self._operation(session, row.id, claim.request_id)
        current = (
            row is not None and operation is not None and operation.attempt_id == claim.attempt_id
            and operation.status == "processing" and row.active_request_id == claim.request_id
            and row.revision == claim.revision
        )
        return (row, operation) if current else (None, None)

    def _audit(self, claim: OperationClaim, trace: list[dict]) -> None:
        if not trace:
            return
        with self._sf() as session:
            operation = self._operation(session, claim.session_id, claim.request_id)
            if operation is None:
                return
            operation.usage = [*(operation.usage or []), *[{"rejected": True, **item} for item in trace]]
            operation.updated_at = datetime.now(UTC)
            session.commit()

    @staticmethod
    def _operation(session, session_id, request_id):
        return session.scalar(select(IntakeOperationRow).where(
            IntakeOperationRow.session_id == session_id, IntakeOperationRow.request_id == request_id
        ))

    @staticmethod
    def _next_sequence(session, session_id) -> int:
        current = session.scalar(select(func.max(IntakeMessageRow.sequence)).where(IntakeMessageRow.session_id == session_id))
        return int(current or 0) + 1

    @staticmethod
    def _message(session_id, message_id, role, text, language, sequence, operation_id, created_at) -> IntakeMessageRow:
        return IntakeMessageRow(
            id=message_id, session_id=session_id, sequence=sequence, role=role, text=text,
            language=language, operation_id=operation_id, created_at=created_at,
        )
