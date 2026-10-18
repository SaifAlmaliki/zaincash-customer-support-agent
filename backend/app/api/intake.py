"""Customer intake routes. Ownership failures do not reveal whether a session exists."""
from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, BackgroundTasks, File, Form, HTTPException, Request, UploadFile
from fastapi.responses import JSONResponse, Response
from starlette.concurrency import run_in_threadpool

from app.api.intake_schemas import (
    CreateSessionInput,
    MessageInput,
    RemoveInput,
    RetryInput,
    ReviewInput,
    SubmitInput,
)
from app.intake.contracts import Credentials
from app.services.intake_recovery import fail_intake_placeholders, reconcile_intake_run

router = APIRouter(prefix="/api/intake", tags=["Customer intake"])


def _credentials(request: Request, session_id: UUID) -> Credentials:
    header = request.headers.get("authorization") or ""
    scheme, _, token = header.partition(" ")
    if scheme.lower() != "bearer" or not token.strip():
        raise HTTPException(status_code=401, detail={"code": "not_owned", "message": "Missing access token."})
    return Credentials(session_id=session_id, token=token.strip())


def _dump(model) -> dict:
    return model.model_dump(mode="json")


def _status(view, request_id: UUID) -> int:
    return 202 if view.turn_status == "processing" and view.active_request_id == request_id else 200


async def _safe_dispatch(app, submission) -> None:
    if not submission.dispatch:
        return
    try:
        app.state.intake_dispatcher(app, submission)
    except Exception:
        with app.state.session_factory() as session:
            fail_intake_placeholders(session, submission.run_id, "Dispatch failed. The submitted report was kept.")
            from datetime import UTC, datetime

            from app.db.models import RunRow
            run = session.get(RunRow, submission.run_id)
            if run is not None and run.status == "running":
                run.status = "failed"
                run.finished_at = datetime.now(UTC)
                reconcile_intake_run(session, run)
            session.commit()


@router.post("/sessions", status_code=201)
def create_session(body: CreateSessionInput, request: Request):
    credentials, view = request.app.state.intake.create(body.language)
    return {"credentials": _dump(credentials), "session": _dump(view)}


@router.get("/sessions/{session_id}")
def get_session(session_id: UUID, request: Request):
    return request.app.state.intake.get(_credentials(request, session_id))


@router.post("/sessions/{session_id}/messages")
async def post_message(session_id: UUID, body: MessageInput, request: Request):
    if not body.text and not body.attachment_ids:
        raise HTTPException(status_code=422, detail={"code": "invalid_evidence", "message": "Enter a message or attach a screenshot."})
    view = await request.app.state.intake.message(_credentials(request, session_id), body.model_dump())
    return JSONResponse(_dump(view), status_code=_status(view, body.request_id))


@router.post("/sessions/{session_id}/operations/{request_id}/retry")
async def retry_operation(session_id: UUID, request_id: UUID, body: RetryInput, request: Request):
    view = await request.app.state.intake.retry(_credentials(request, session_id), request_id, body.expected_revision)
    return JSONResponse(_dump(view), status_code=_status(view, request_id))


@router.post("/sessions/{session_id}/attachments", status_code=201)
async def upload_attachment(
    session_id: UUID, request: Request, file: Annotated[UploadFile, File()],
    request_id: Annotated[UUID, Form()], expected_revision: Annotated[int, Form()],
):
    content = await file.read()
    attachment, view = await run_in_threadpool(
        request.app.state.intake_store.upload, _credentials(request, session_id),
        request_id, expected_revision, file.filename or "screenshot", content,
    )
    return {"attachment": _dump(attachment), "session": _dump(view)}


@router.get("/sessions/{session_id}/attachments/{attachment_id}")
def read_attachment(session_id: UUID, attachment_id: UUID, request: Request):
    image = request.app.state.intake_store.read(_credentials(request, session_id), attachment_id)
    return Response(content=image.data, media_type=image.mime_type, headers={"Cache-Control": "no-store"})


@router.delete("/sessions/{session_id}/attachments/{attachment_id}")
def remove_attachment(session_id: UUID, attachment_id: UUID, body: RemoveInput, request: Request):
    view = request.app.state.intake_store.remove(
        _credentials(request, session_id), attachment_id, body.request_id, body.expected_revision
    )
    return view


@router.post("/sessions/{session_id}/review")
async def request_review(session_id: UUID, body: ReviewInput, request: Request):
    view = await request.app.state.intake.review(_credentials(request, session_id), body.model_dump())
    return JSONResponse(_dump(view), status_code=_status(view, body.request_id))


@router.post("/sessions/{session_id}/submit")
async def submit_session(session_id: UUID, body: SubmitInput, request: Request, background: BackgroundTasks):
    result = await run_in_threadpool(
        request.app.state.submission.submit, _credentials(request, session_id),
        body.request_id, body.expected_revision, body.review_id, body.confirmed,
    )
    if result.dispatch:
        background.add_task(_safe_dispatch, request.app, result)
    return result.receipt
