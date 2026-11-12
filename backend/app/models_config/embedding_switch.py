"""Switch the embedding model: flip the setting, then re-index every document once.

The KB keeps one index per document, so search pauses while documents are
re-indexed. Workspace batch starts are blocked meanwhile; intake runs are not.
"""
from __future__ import annotations

import asyncio
import logging
from datetime import UTC, datetime
from typing import Any

from sqlalchemy import func, select, text
from sqlalchemy.orm import sessionmaker

from app.db.document_models import UploadedDocument
from app.db.models import RunRow
from app.kb.service import DocumentNotFoundError, KnowledgeService
from app.models_config.db_models import EmbeddingSwitchRow
from app.models_config.store import ModelSettingsStore
from app.models_config.types import ModelChoice, Step

logger = logging.getLogger(__name__)
RESTART_ERROR = "API restarted during switch; run the switch again."


class SwitchConflict(RuntimeError):
    def __init__(self, code: str) -> None:
        super().__init__(code)
        self.code = code


def _view(row: EmbeddingSwitchRow) -> dict[str, Any]:
    return {"id": row.id, "status": row.status, "total": row.total, "done": row.done,
            "failed_document_ids": list(row.failed_document_ids or []), "error": row.error,
            "target": row.target, "previous": row.previous, "started_by": row.started_by,
            "started_at": row.started_at.isoformat() if row.started_at else None,
            "finished_at": row.finished_at.isoformat() if row.finished_at else None}


class EmbeddingSwitches:
    def __init__(self, session_factory: sessionmaker, store: ModelSettingsStore,
                 knowledge: KnowledgeService) -> None:
        self._sf, self._store, self._knowledge = session_factory, store, knowledge

    def running(self) -> bool:
        with self._sf() as session:
            return session.scalar(select(EmbeddingSwitchRow.id)
                                  .where(EmbeddingSwitchRow.status == "running").limit(1)) is not None

    def current(self) -> dict[str, Any] | None:
        with self._sf() as session:
            row = session.scalar(select(EmbeddingSwitchRow).order_by(EmbeddingSwitchRow.id.desc()).limit(1))
            return _view(row) if row else None

    def start(self, choice: ModelChoice, *, changed_by: str, latency_ms: int) -> dict[str, Any]:
        with self._sf() as session:
            # Serialize concurrent starts; the check-then-insert below is then race-free.
            session.execute(text("LOCK TABLE embedding_switch IN EXCLUSIVE MODE"))
            if session.scalar(select(RunRow.id).where(RunRow.status == "running").limit(1)) is not None:
                raise SwitchConflict("run_in_progress")
            if session.scalar(select(EmbeddingSwitchRow.id)
                              .where(EmbeddingSwitchRow.status == "running").limit(1)) is not None:
                raise SwitchConflict("switch_in_progress")
            total = session.scalar(select(func.count()).select_from(UploadedDocument)) or 0
            row = EmbeddingSwitchRow(target=choice.to_json(), previous=self._store.choice(Step.EMBED).to_json(),
                                     status="running", total=total, done=0, failed_document_ids=[],
                                     started_by=changed_by, started_at=datetime.now(UTC))
            session.add(row)
            updated_at = self._store.save(Step.EMBED, choice, changed_by=changed_by,
                                          latency_ms=latency_ms, session=session)
            session.commit()
            view = _view(row)
        # The commit succeeded: refresh the cache without database I/O, which cannot strand the switch.
        self._store.remember(Step.EMBED, choice, changed_by=changed_by, updated_at=updated_at)
        return view

    async def run(self, switch_id: int) -> None:
        failed: list[int] = []
        try:
            ids = await asyncio.to_thread(self._document_ids)
            for document_id in ids:
                try:
                    view = await self._knowledge.index_document(document_id)
                    if view.get("status") != "indexed":
                        failed.append(document_id)
                except DocumentNotFoundError:
                    pass  # deleted during the switch: nothing left to index
                except Exception as exc:
                    logger.warning("Switch %s could not index document %s: %s",
                                   switch_id, document_id, type(exc).__name__)
                    failed.append(document_id)
                await asyncio.to_thread(self._progress, switch_id, failed)
            await asyncio.to_thread(self._finish, switch_id, failed, None)
        except Exception as exc:
            logger.warning("Switch %s failed: %s", switch_id, type(exc).__name__)
            await asyncio.to_thread(self._finish, switch_id, failed, f"{type(exc).__name__}: switch stopped.")

    def recover_interrupted(self) -> int:
        with self._sf.begin() as session:
            rows = list(session.scalars(select(EmbeddingSwitchRow).where(EmbeddingSwitchRow.status == "running")))
            for row in rows:
                row.status, row.error, row.finished_at = "failed", RESTART_ERROR, datetime.now(UTC)
            return len(rows)

    def _document_ids(self) -> list[int]:
        with self._sf() as session:
            return list(session.scalars(select(UploadedDocument.id).order_by(UploadedDocument.id)))

    def _progress(self, switch_id: int, failed: list[int]) -> None:
        with self._sf.begin() as session:
            row = session.get(EmbeddingSwitchRow, switch_id, with_for_update=True)
            row.done = min(row.total, row.done + 1)
            row.failed_document_ids = list(failed)

    def _finish(self, switch_id: int, failed: list[int], error: str | None) -> None:
        with self._sf.begin() as session:
            row = session.get(EmbeddingSwitchRow, switch_id, with_for_update=True)
            row.failed_document_ids = list(failed)
            row.error = error
            row.status = "failed" if error else "completed_with_errors" if failed else "completed"
            row.finished_at = datetime.now(UTC)
