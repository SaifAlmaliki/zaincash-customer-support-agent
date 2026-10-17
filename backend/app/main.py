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

from app.api import knowledge, results, runs, workspace
from app.config import Settings
from app.db.models import RunRow
from app.db.session import init_db, make_engine, make_sessionmaker
from app.db.workspace_schema import upgrade_workspace_schema
from app.pipeline.factory import build_pipeline
from app.services.knowledge_runtime import IndexJobs, make_knowledge_service
from app.taxonomy import load_taxonomy


def create_app(settings=None, *, session_factory=None, pipeline_builder=None, knowledge_builder=None):
    settings = settings or Settings()

    @asynccontextmanager
    async def lifespan(app):
        engine = None
        if session_factory is None:
            engine = make_engine(settings.database_url)
            init_db(engine)
            upgrade_workspace_schema(engine)
            app.state.session_factory = make_sessionmaker(engine)
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
                    session.commit()

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
    app.add_middleware(CORSMiddleware, allow_origins=["http://localhost:5173", "http://localhost:5174",
                       "http://localhost:4173", "http://127.0.0.1:5173"], allow_methods=["GET", "POST", "DELETE"],
                       allow_headers=["Content-Type"])

    @app.exception_handler(OperationalError)
    async def database_unavailable(_request: Request, _error: OperationalError):
        return JSONResponse(status_code=503, content={"detail": "Database unavailable. Start the db service and retry."})

    for router in (workspace.router, results.router, runs.router, knowledge.router):
        app.include_router(router)
    return app


app = create_app()
