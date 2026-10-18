"""Decode screenshots locally and store only server-generated paths."""
from __future__ import annotations

import hashlib
import os
import re
import uuid
from datetime import UTC, datetime
from io import BytesIO
from pathlib import Path

from PIL import Image, UnidentifiedImageError
from sqlalchemy import func, select
from sqlalchemy.orm import sessionmaker

from app.config import Settings
from app.intake.contracts import Attachment, Credentials, ImageInput, IntakeState, SessionView
from app.intake.db_models import IntakeAttachmentRow, IntakeOperationRow, IntakeSessionRow
from app.intake.errors import ImageRejected, NotOwned, RevisionConflict, TurnBusy
from app.intake.evidence import remove_attachment_evidence
from app.intake.repository import (
    IntakeRepository,
    assert_same_operation,
    operation_fingerprint,
    session_view,
)

_FORMATS = {"JPEG": ("image/jpeg", "jpg"), "PNG": ("image/png", "png"), "WEBP": ("image/webp", "webp")}
_NAME = re.compile(r"[^A-Za-z0-9._-]+")


def _display_name(filename: str, extension: str) -> str:
    base = Path(str(filename or "").replace("\\", "/")).name
    cleaned = _NAME.sub("_", base).strip("._")
    return (cleaned or f"screenshot.{extension}")[:120]


class AttachmentStore:
    def __init__(self, settings: Settings, session_factory: sessionmaker) -> None:
        self.settings = settings
        self._sf = session_factory
        self.root = Path(settings.intake_upload_dir)
        self.repo = IntakeRepository(session_factory)

    def upload(self, credentials: Credentials, request_id: uuid.UUID, expected_revision: int,
               filename: str, content: bytes) -> tuple[Attachment, SessionView]:
        decoded = self._decode(content)
        digest = hashlib.sha256(content).hexdigest()
        safe_name = _display_name(filename, decoded["extension"])
        fingerprint = operation_fingerprint("attachment", {"content_hash": digest, "filename": safe_name})
        created_path: Path | None = None
        try:
            with self._sf() as session:
                row = self.repo.authenticate(session, credentials, lock=True)
                existing = session.scalar(select(IntakeOperationRow).where(
                    IntakeOperationRow.session_id == row.id, IntakeOperationRow.request_id == request_id
                ))
                if existing is not None:
                    assert_same_operation(existing.fingerprint, fingerprint)
                    stored = session.scalar(select(IntakeAttachmentRow).where(IntakeAttachmentRow.operation_id == existing.id))
                    return self._public(stored), session_view(session, row)
                self._ensure_mutable(row, expected_revision)
                count = session.scalar(select(func.count()).select_from(IntakeAttachmentRow).where(
                    IntakeAttachmentRow.session_id == row.id, IntakeAttachmentRow.removed.is_(False)
                ))
                if count >= self.settings.intake_max_images_per_session:
                    raise ImageRejected("This conversation already has the maximum number of screenshots.")
                attachment_id = uuid.uuid4()
                created_path = self._write(row.id, attachment_id, decoded["extension"], content)
                now = datetime.now(UTC)
                operation = IntakeOperationRow(
                    id=uuid.uuid4(), session_id=row.id, request_id=request_id, kind="attachment",
                    fingerprint=fingerprint, status="completed", attempt_id=uuid.uuid4(),
                    claimed_revision=row.revision + 1, request_json={"content_hash": digest, "filename": safe_name},
                    result_json={"attachment_id": str(attachment_id)}, error_code=None, usage=[],
                    created_at=now, updated_at=now,
                )
                session.add(operation)
                session.flush()
                session.add(IntakeAttachmentRow(
                    id=attachment_id, session_id=row.id, message_id=None, operation_id=operation.id,
                    request_id=request_id, storage_key=created_path.relative_to(self.root).as_posix(),
                    content_hash=digest, filename=safe_name, mime_type=decoded["mime"], size=len(content),
                    width=decoded["width"], height=decoded["height"], removed=False, created_at=now,
                ))
                row.revision += 1
                row.review = None
                if row.phase == "review_ready":
                    row.phase = "collecting"
                row.updated_at = now
                session.commit()
                stored = session.get(IntakeAttachmentRow, attachment_id)
                return self._public(stored), session_view(session, row)
        except Exception:
            if created_path is not None and created_path.exists():
                with self._sf() as session:
                    kept = session.scalar(select(IntakeAttachmentRow).where(
                        IntakeAttachmentRow.storage_key == created_path.relative_to(self.root).as_posix()
                    ))
                if kept is None:
                    created_path.unlink(missing_ok=True)
            raise

    def read(self, credentials: Credentials, attachment_id: uuid.UUID) -> ImageInput:
        with self._sf() as session:
            self.repo.authenticate(session, credentials)
            row = session.get(IntakeAttachmentRow, attachment_id)
            if row is None or row.session_id != credentials.session_id:
                raise NotOwned("Conversation not found.")
            if row.removed:
                raise ImageRejected("This screenshot was removed.")
            return self._load_row(row)

    def load_for_session(self, session_id: uuid.UUID, attachment_id: uuid.UUID) -> ImageInput:
        with self._sf() as session:
            row = session.get(IntakeAttachmentRow, attachment_id)
            if row is None or row.session_id != session_id or row.removed:
                raise NotOwned("Conversation not found.")
            return self._load_row(row)

    def remove(self, credentials: Credentials, attachment_id: uuid.UUID, request_id: uuid.UUID,
               expected_revision: int) -> SessionView:
        fingerprint = operation_fingerprint("remove", {"attachment_id": str(attachment_id)})
        path: Path | None = None
        with self._sf() as session:
            row = self.repo.authenticate(session, credentials, lock=True)
            existing = session.scalar(select(IntakeOperationRow).where(
                IntakeOperationRow.session_id == row.id, IntakeOperationRow.request_id == request_id
            ))
            if existing is not None:
                assert_same_operation(existing.fingerprint, fingerprint)
                return session_view(session, row)
            self._ensure_mutable(row, expected_revision)
            attachment = session.get(IntakeAttachmentRow, attachment_id)
            if attachment is None or attachment.session_id != row.id:
                raise NotOwned("Conversation not found.")
            now = datetime.now(UTC)
            session.add(IntakeOperationRow(
                id=uuid.uuid4(), session_id=row.id, request_id=request_id, kind="remove",
                fingerprint=fingerprint, status="completed", attempt_id=uuid.uuid4(),
                claimed_revision=row.revision + 1, request_json={"attachment_id": str(attachment_id)},
                result_json={"removed": True}, error_code=None, usage=[], created_at=now, updated_at=now,
            ))
            attachment.removed = True
            state = remove_attachment_evidence(IntakeState.model_validate(row.state), attachment_id)
            row.state = state.model_dump(mode="json")
            row.review = None
            row.phase = "collecting" if row.phase != "submitted" else row.phase
            row.revision += 1
            row.updated_at = now
            path = self.root / attachment.storage_key
            session.commit()
            view = session_view(session, row)
        if path is not None:
            path.unlink(missing_ok=True)
        return view

    def cleanup_orphans(self, *, max_age_s: int = 3600) -> int:
        if not self.root.exists():
            return 0
        with self._sf() as session:
            referenced = set(session.scalars(select(IntakeAttachmentRow.storage_key)))
        removed = 0
        cutoff = datetime.now(UTC).timestamp() - max_age_s
        for path in self.root.rglob("*"):
            if not path.is_file():
                continue
            key = path.relative_to(self.root).as_posix()
            stale = path.stat().st_mtime <= cutoff
            staging = path.name.endswith(".staging")
            if staging and stale:
                path.unlink(missing_ok=True)
                removed += 1
            elif key not in referenced and stale:
                path.unlink(missing_ok=True)
                removed += 1
        return removed

    def _ensure_mutable(self, row: IntakeSessionRow, expected_revision: int) -> None:
        if row.phase == "submitted":
            raise RevisionConflict("This report was already submitted.")
        if row.turn_status == "processing":
            raise TurnBusy("This conversation is still being updated.")
        if row.revision != expected_revision:
            raise RevisionConflict("Reload the current conversation.")

    def _decode(self, content: bytes) -> dict:
        if not content or len(content) > self.settings.intake_max_image_bytes:
            raise ImageRejected("Image is too large.")
        try:
            with Image.open(BytesIO(content)) as image:
                if image.format not in _FORMATS:
                    raise ImageRejected("Unsupported image format.")
                if image.width * image.height > self.settings.intake_max_image_pixels:
                    raise ImageRejected("Image resolution is too large.")
                if getattr(image, "n_frames", 1) != 1:
                    raise ImageRejected("Upload a single screenshot.")
                image.verify()
            with Image.open(BytesIO(content)) as image:
                image.load()
                width, height = image.size
                fmt = image.format
        except ImageRejected:
            raise
        except (UnidentifiedImageError, OSError, ValueError) as exc:
            raise ImageRejected("Image could not be read.") from exc
        mime, extension = _FORMATS[fmt]
        return {"mime": mime, "extension": extension, "width": width, "height": height}

    def _write(self, session_id: uuid.UUID, attachment_id: uuid.UUID, extension: str, content: bytes) -> Path:
        destination = self.root / str(session_id) / f"{attachment_id}.{extension}"
        destination.parent.mkdir(parents=True, exist_ok=True)
        staging = destination.with_name(destination.name + ".staging")
        staging.write_bytes(content)
        os.replace(staging, destination)
        return destination

    def _load_row(self, row: IntakeAttachmentRow) -> ImageInput:
        path = self.root / row.storage_key
        if not path.is_file():
            raise ImageRejected("Image could not be read.")
        return ImageInput(id=row.id, mime_type=row.mime_type, data=path.read_bytes())

    @staticmethod
    def _public(row: IntakeAttachmentRow) -> Attachment:
        return Attachment(
            id=row.id, filename=row.filename, mime_type=row.mime_type, size=row.size,
            width=row.width, height=row.height, message_id=row.message_id, removed=row.removed,
        )
