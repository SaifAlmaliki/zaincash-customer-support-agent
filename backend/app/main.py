"""Local support workspace API. Start with uvicorn app.main:app --port 8000."""
from contextlib import asynccontextmanager
from datetime import UTC, datetime
from functools import partial
from inspect import Parameter, signature

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy import select
from sqlalchemy.exc import OperationalError
from starlette.concurrency import run_in_threadpool

from app.api import intake, knowledge, results, runs, workspace
from app.config import Settings
from app.db.models import RunRow
from app.db.session import init_db, make_engine, make_sessionmaker
from app.db.workspace_schema import upgrade_workspace_schema
from app.intake.errors import IntakeError
from app.intake.submission import SubmissionService
from app.pipeline.factory import build_pipeline
from app.services.intake_recovery import (
    fail_intake_placeholders,
    reconcile_intake_run,
    recover_intake_processing,
)
from app.services.intake_runtime import dispatch_intake, make_intake_service
from app.services.knowledge_runtime import IndexJobs, make_knowledge_service
from app.taxonomy import load_taxonomy


def create_app(settings=None, *, session_factory=None, pipeline_builder=None, knowledge_builder=None,
               intake_builder=None, intake_dispatcher=None):
    settings = settings or Settings()

    @asynccontextmanager
    async def lifespan(app):
        engine = None
        if session_factory is None:
            engine = make_engine(settings.database_url)
            init_db(engine)
            upgrade_workspace_schema(engine)
            app.state.session_factory = make_sessionmaker(engine)
        intake_service = (intake_builder or make_intake_service)(app.state.session_factory, settings, app.state.taxonomy)
        app.state.intake = intake_service
        app.state.intake_store = intake_service.store
        app.state.submission = SubmissionService(app.state.session_factory, settings)
        app.state.intake_dispatcher = intake_dispatcher or dispatch_intake
        try:
            service = (knowledge_builder or make_knowledge_service)(app.state.session_factory, settings)
            app.state.knowledge = service
            app.state.index_jobs = IndexJobs(service)
            builder = pipeline_builder or build_pipeline
            parameters = signature(builder).parameters
            accepts_knowledge = "knowledge" in parameters or any(
                p.kind == Parameter.VAR_KEYWORD for p in parameters.values())
            app.state.pipeline_builder = partial(builder, knowledge=service) if accepts_knowledge else builder

            def recover():
                # Startup-only recovery: this local application runs one worker.
                service.recover_interrupted()
                with app.state.session_factory() as session:
                    for run in session.scalars(select(RunRow).where(RunRow.status == "running")):
                        run.status = "failed"
                        run.finished_at = datetime.now(UTC)
                        run.counts = run.counts | {"error": "API restarted during processing. Start a new run."}
                        if fail_intake_placeholders(session, run.id, "API restarted during processing. Start a new run."):
                            reconcile_intake_run(session, run)
                    session.commit()
                recover_intake_processing(app.state.session_factory)
                app.state.intake.turns.recover_interrupted()
                if session_factory is None:
                    app.state.intake_store.cleanup_orphans()

            await run_in_threadpool(recover)
            yield
        finally:
            if engine:
                engine.dispose()

    app = FastAPI(title="ZainCash Support Workspace", version="0.1.0", lifespan=lifespan,
                  docs_url="/api/docs", openapi_url="/api/openapi.json")
    app.state.settings = settings
    app.state.session_factory = session_factory
    app.state.pipeline_builder = pipeline_builder or build_pipeline
    app.state.testing_pipeline = pipeline_builder is not None
    app.state.taxonomy = load_taxonomy(settings.taxonomy_path)
    app.add_middleware(CORSMiddleware, allow_origins=[
        "http://localhost:5173", "http://127.0.0.1:5173", "http://localhost:5174", "http://127.0.0.1:5174",
        "http://localhost:4173",
    ], allow_methods=["GET", "POST", "DELETE"], allow_headers=["Authorization", "Content-Type"])

    @app.exception_handler(OperationalError)
    async def database_unavailable(_request: Request, _error: OperationalError):
        return JSONResponse(status_code=503, content={"detail": "Database unavailable. Start the db service and retry."})

    @app.exception_handler(IntakeError)
    async def intake_failed(_request: Request, error: IntakeError):
        status = {
            "not_owned": 404, "revision_conflict": 409, "operation_conflict": 409, "turn_busy": 409,
            "stale_review": 409, "image_rejected": 422, "invalid_evidence": 422, "model_unavailable": 503,
        }.get(error.code, 400)
        return JSONResponse(status_code=status, content={"detail": {"code": error.code, "message": error.message}})

    for router in (workspace.router, results.router, runs.router, knowledge.router, intake.router):
        app.include_router(router)
    return app


app = create_app()
