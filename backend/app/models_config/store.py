"""Admin model settings: Postgres is durable, an in-process cache serves reads.

This API runs one worker process, so the cache is authoritative after load()
and is updated on every save.
"""
from __future__ import annotations

import logging
import threading
from datetime import UTC, datetime
from typing import Any
from uuid import UUID

from sqlalchemy import select, update
from sqlalchemy.orm import Session, sessionmaker

from app.config import Settings
from app.intake.db_models import IntakeSessionRow
from app.models_config.db_models import ModelSettingAuditRow, ModelSettingRow
from app.models_config.providers.registry import ProviderRegistry, UnknownProvider
from app.models_config.resolver import ActiveModels
from app.models_config.steps import PROVIDERS_FOR_STEP, REQUIREMENTS, intake_timeout_s
from app.models_config.types import ModelChoice, Step

logger = logging.getLogger(__name__)


def _iso(value: datetime | None) -> str | None:
    return value.isoformat() if value else None


class ModelSettingsStore:
    def __init__(self, session_factory: sessionmaker, settings: Settings,
                 registry: ProviderRegistry | None = None) -> None:
        self._sf = session_factory
        self.settings = settings
        self.registry = registry or ProviderRegistry(settings)
        self._lock = threading.Lock()
        self._rows: dict[Step, dict[str, Any]] = {}

    def load(self) -> None:
        with self._sf() as session:
            rows = list(session.scalars(select(ModelSettingRow)))
        loaded: dict[Step, dict[str, Any]] = {}
        for row in rows:
            try:
                step = Step(row.step)
                self.registry.get(row.provider)
                if row.provider not in PROVIDERS_FOR_STEP[step]:
                    raise ValueError(f"{row.provider} is not allowed for {step.value}")
            except (ValueError, UnknownProvider):
                logger.warning("Ignoring stored model setting %s=%s:%s", row.step, row.provider, row.model)
                continue
            loaded[step] = {"choice": ModelChoice(row.provider, row.model, dict(row.options or {})),
                            "updated_at": row.updated_at, "updated_by": row.updated_by}
        with self._lock:
            self._rows = loaded

    def active(self) -> ActiveModels:
        with self._lock:
            choices = {step: entry["choice"] for step, entry in self._rows.items()}
        return ActiveModels(self.settings, choices, self.registry)

    def choice(self, step: Step) -> ModelChoice:
        return self.active().choice(step)

    def describe(self) -> list[dict[str, Any]]:
        active = self.active()
        with self._lock:
            rows = dict(self._rows)
        described = []
        for step in Step:
            choice, entry = active.choice(step), rows.get(step)
            status = self.registry.status(choice.provider)
            described.append({
                "step": step.value, "provider": choice.provider, "model": choice.model,
                "options": dict(choice.options), "source": "admin" if entry else "env",
                "updated_at": _iso(entry["updated_at"]) if entry else None,
                "updated_by": entry["updated_by"] if entry else None,
                "locality": status.locality, "status": status.state, "status_detail": status.detail,
                "requirements": sorted(c.value for c in REQUIREMENTS[step]),
                "providers": list(PROVIDERS_FOR_STEP[step]),
            })
        return described

    def save(self, step: Step, choice: ModelChoice, *, changed_by: str, latency_ms: int,
             session: Session | None = None) -> datetime:
        """Persist and audit. With an external session the caller commits, then calls remember()."""
        own = session is None
        session = session or self._sf()
        try:
            previous = self.choice(step)
            now = datetime.now(UTC)
            row = session.get(ModelSettingRow, step.value, with_for_update=True)
            if row is None:
                row = ModelSettingRow(step=step.value)
                session.add(row)
            row.provider, row.model, row.options = choice.provider, choice.model, dict(choice.options)
            row.updated_at, row.updated_by = now, changed_by
            session.add(ModelSettingAuditRow(step=step.value, previous=previous.to_json(),
                                             current=choice.to_json(), changed_by=changed_by,
                                             changed_at=now, test_latency_ms=latency_ms))
            if own:
                session.commit()
        finally:
            if own:
                session.close()
        if own:
            self.remember(step, choice, changed_by=changed_by, updated_at=now)
        return now

    def remember(self, step: Step, choice: ModelChoice, *, changed_by: str, updated_at: datetime) -> None:
        """Update the in-memory cache for a setting that is already committed; never touches the database."""
        with self._lock:
            self._rows[step] = {"choice": choice, "updated_at": updated_at, "updated_by": changed_by}

    def audit(self, limit: int = 50) -> list[dict[str, Any]]:
        with self._sf() as session:
            rows = session.scalars(select(ModelSettingAuditRow)
                                   .order_by(ModelSettingAuditRow.id.desc()).limit(limit))
            return [{"id": row.id, "step": row.step, "previous": row.previous, "current": row.current,
                     "changed_by": row.changed_by, "changed_at": _iso(row.changed_at),
                     "test_latency_ms": row.test_latency_ms} for row in rows]

    def intake_pin(self, session_id: UUID) -> tuple[ModelChoice, float]:
        """The intake model for one customer conversation: pinned on its first model call."""
        current = self.choice(Step.INTAKE)
        with self._sf.begin() as session:
            session.execute(update(IntakeSessionRow)
                            .where(IntakeSessionRow.id == session_id, IntakeSessionRow.model_choice.is_(None))
                            .values(model_choice=current.to_json()))
            stored = session.scalar(select(IntakeSessionRow.model_choice)
                                    .where(IntakeSessionRow.id == session_id))
            choice = current
            if stored is not None:
                try:
                    candidate = ModelChoice.from_json(stored)
                    self.registry.get(candidate.provider)
                    choice = candidate
                except (ValueError, UnknownProvider):
                    logger.warning("Intake session %s has an unusable pinned model; re-pinning", session_id)
                    session.execute(update(IntakeSessionRow).where(IntakeSessionRow.id == session_id)
                                    .values(model_choice=current.to_json()))
        return choice, intake_timeout_s(self.settings, self.registry.get(choice.provider).locality)
