"""Create one normal pipeline ticket for an approved intake review."""
from __future__ import annotations

import uuid
from dataclasses import dataclass
from datetime import UTC, datetime

from sqlalchemy import select
from sqlalchemy.orm import sessionmaker

from app.config import Settings
from app.db.models import RunRow, TicketResultRow, TicketRow
from app.db.repository import create_run, upsert_tickets
from app.intake.contracts import Credentials, Receipt, ReviewSnapshot
from app.intake.db_models import IntakeOperationRow, IntakeSubmissionRow
from app.intake.errors import InvalidEvidence, RevisionConflict, StaleReview, TurnBusy
from app.intake.repository import (
    IntakeRepository,
    assert_same_operation,
    load_attachments,
    load_messages,
    operation_fingerprint,
    processing_status,
    session_view,
)
from app.pipeline.contracts import Ticket
from app.pipeline.factory import model_ids
from app.pipeline.stage2_classify.prompts import PROMPT_VERSION


@dataclass
class SubmissionResult:
    receipt: Receipt
    run_id: int
    ticket: Ticket
    mode: str
    dispatch: bool


class SubmissionService:
    def __init__(self, session_factory: sessionmaker, settings: Settings, *, mode: str = "cascade") -> None:
        self._sf = session_factory
        self.settings = settings
        self.mode = mode
        self.repo = IntakeRepository(session_factory)

    def submit(self, credentials: Credentials, request_id: uuid.UUID, expected_revision: int,
               review_id: uuid.UUID, confirmed: bool) -> SubmissionResult:
        payload = {"review_id": str(review_id), "confirmed": confirmed}
        fingerprint = operation_fingerprint("submit", payload)
        with self._sf() as session:
            row = self.repo.authenticate(session, credentials, lock=True)
            operation = session.scalar(select(IntakeOperationRow).where(
                IntakeOperationRow.session_id == row.id, IntakeOperationRow.request_id == request_id
            ))
            submission = session.scalar(select(IntakeSubmissionRow).where(IntakeSubmissionRow.session_id == row.id))
            if operation is not None:
                assert_same_operation(operation.fingerprint, fingerprint)
                if operation.status == "completed" and submission is not None:
                    return self._result(session, submission, dispatch=False)
                if operation.status == "processing":
                    raise TurnBusy("This conversation is still being updated.")
            if submission is not None:
                if submission.review_id != review_id or confirmed is not True:
                    raise StaleReview("Review the latest summary before submitting.")
                self._record_alias(session, row, request_id, fingerprint, payload, submission)
                session.commit()
                return self._result(session, submission, dispatch=False)
            if confirmed is not True:
                raise InvalidEvidence("Confirm the review before submitting.")
            if row.turn_status == "processing":
                raise TurnBusy("This conversation is still being updated.")
            if row.revision != expected_revision:
                raise RevisionConflict("Reload the current conversation.")
            if row.phase != "review_ready" or not row.review:
                raise StaleReview("Review the latest summary before submitting.")
            snapshot = ReviewSnapshot.model_validate(row.review)
            if snapshot.id != review_id or snapshot.revision != row.revision:
                raise StaleReview("Review the latest summary before submitting.")
            owned = {item.id for item in load_attachments(session, row.id) if not item.removed}
            if any(item not in owned for item in snapshot.attachment_ids):
                raise InvalidEvidence("The review includes a screenshot that is no longer available.")
            result = self._create(session, row, request_id, fingerprint, payload, snapshot)
            session.commit()
            return result

    def _create(self, session, row, request_id, fingerprint, payload, snapshot: ReviewSnapshot) -> SubmissionResult:
        now = datetime.now(UTC)
        phone_fact = snapshot.facts.get("customer_phone")
        phone = None
        if phone_fact is not None and phone_fact.status == "known":
            phone = (phone_fact.normalized or phone_fact.value or "").strip()[:32] or None
        ticket = Ticket(
            external_id=f"INTAKE-{row.id.hex}", text=snapshot.ticket_text_ar, received_at=now,
            channel="app", customer_phone=phone,
        )
        stored = upsert_tickets(session, [ticket], source="intake")[0]
        run_id = create_run(
            session, mode=self.mode, prompt_version=PROMPT_VERSION, model_ids=model_ids(self.settings, self.mode)
        )
        placeholder = TicketResultRow(
            run_id=run_id, ticket_id=stored.id, status="processing", category_probs={}, flags={}, extracted={},
            escalation_reasons=[], citations=[], agent_trace=[], escalated=False, latency_ms=0, cost_usd=0.0,
        )
        session.add(placeholder)
        session.flush()
        run = session.get(RunRow, run_id)
        run.counts = {"expected_total": 1, "total": 0, "by_status": {}}
        messages = [item.model_dump(mode="json") for item in load_messages(session, row.id)]
        attachments = [item.model_dump(mode="json") for item in load_attachments(session, row.id) if not item.removed]
        frozen = snapshot.model_dump(mode="json")
        frozen.update({
            "messages": messages,
            "attachments": attachments,
            "employee_text_ar": snapshot.employee_text_ar,
            "submitted_at": now.isoformat(),
            "started_at": row.created_at.isoformat(),
            "readiness": row.state["readiness"],
        })
        session.add(IntakeSubmissionRow(
            id=uuid.uuid4(), session_id=row.id, ticket_id=stored.id, run_id=run_id, result_id=placeholder.id,
            review_id=snapshot.id, request_id=request_id, snapshot=frozen, submitted_at=now,
        ))
        session.add(IntakeOperationRow(
            id=uuid.uuid4(), session_id=row.id, request_id=request_id, kind="submit", fingerprint=fingerprint,
            status="completed", attempt_id=uuid.uuid4(), claimed_revision=row.revision, request_json=payload,
            result_json={"ticket_id": stored.id, "run_id": run_id}, error_code=None, usage=[],
            created_at=now, updated_at=now,
        ))
        row.phase = "submitted"
        row.turn_status = "idle"
        row.active_request_id = None
        row.error_code = None
        row.updated_at = now
        session.flush()
        receipt = Receipt(ticket_reference=stored.external_id, submitted_at=now, processing_status="processing")
        return SubmissionResult(receipt, run_id, stored, self.mode, True)

    def _record_alias(self, session, row, request_id, fingerprint, payload, submission) -> None:
        if session.scalar(select(IntakeOperationRow).where(
            IntakeOperationRow.session_id == row.id, IntakeOperationRow.request_id == request_id
        )):
            return
        now = datetime.now(UTC)
        session.add(IntakeOperationRow(
            id=uuid.uuid4(), session_id=row.id, request_id=request_id, kind="submit", fingerprint=fingerprint,
            status="completed", attempt_id=uuid.uuid4(), claimed_revision=row.revision, request_json=payload,
            result_json={"ticket_id": submission.ticket_id, "run_id": submission.run_id}, error_code=None,
            usage=[], created_at=now, updated_at=now,
        ))

    def _result(self, session, submission: IntakeSubmissionRow, *, dispatch: bool) -> SubmissionResult:
        ticket_row = session.get(TicketRow, submission.ticket_id)
        result = session.scalar(select(TicketResultRow).where(
            TicketResultRow.ticket_id == submission.ticket_id
        ).order_by(TicketResultRow.id.desc()))
        status = processing_status(result.status) if result is not None else "processing"
        ticket = Ticket(
            id=ticket_row.id, external_id=ticket_row.external_id, text=ticket_row.text,
            received_at=ticket_row.received_at, channel=ticket_row.channel, customer_phone=ticket_row.customer_phone,
        )
        receipt = Receipt(ticket_reference=ticket.external_id, submitted_at=submission.submitted_at, processing_status=status)
        return SubmissionResult(receipt, submission.run_id, ticket, self.mode, dispatch)


def current_session_view(service: SubmissionService, credentials: Credentials):
    with service._sf() as session:
        row = service.repo.authenticate(session, credentials)
        return session_view(session, row)
