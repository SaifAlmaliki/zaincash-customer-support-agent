"""Wire intake services and hand a committed submission to the existing batch runner."""
from __future__ import annotations

import logging

from app.intake.attachments import AttachmentStore
from app.intake.graph import IntakeGraph
from app.intake.model import OpenRouterIntakeModel
from app.intake.repository import IntakeRepository
from app.intake.service import IntakeService
from app.intake.submission import SubmissionService
from app.intake.turns import TurnStore
from app.services.batch_jobs import run_job

logger = logging.getLogger(__name__)


def make_intake_service(session_factory, settings, taxonomy) -> IntakeService:
    store = AttachmentStore(settings, session_factory)
    model = OpenRouterIntakeModel(settings)
    graph = IntakeGraph(model, taxonomy, store, settings)
    repo = IntakeRepository(session_factory)
    turns = TurnStore(session_factory, max_images_per_message=settings.intake_max_images_per_message)
    service = IntakeService(repo, turns, graph, store)
    service.submission = SubmissionService(session_factory, settings)
    return service


def dispatch_intake(app, submission) -> None:
    if not submission.dispatch:
        return
    try:
        run_job(app, submission.run_id, [submission.ticket], submission.mode)
    except Exception:
        logger.warning("Intake dispatch failed for run %s", submission.run_id)
        raise
