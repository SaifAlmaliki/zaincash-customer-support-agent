"""Local support workspace API. Start with uvicorn app.main:app --port 8000."""
from contextlib import asynccontextmanager
from datetime import UTC, datetime

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy import select
from sqlalchemy.exc import OperationalError

from app.api import knowledge, results, runs, workspace
from app.config import Settings
from app.db.models import RunRow
from app.db.session import init_db, make_engine, make_sessionmaker
from app.db.workspace_schema import upgrade_workspace_schema
from app.pipeline.factory import build_pipeline
from app.taxonomy import load_taxonomy


def create_app(settings=None, *, session_factory=None, pipeline_builder=None):
    settings = settings or Settings()

    @asynccontextmanager
    async def lifespan(app):
        engine = None
        if session_factory is None:
            engine = make_engine(settings.database_url)
            init_db(engine)
            upgrade_workspace_schema(engine)
            app.state.session_factory = make_sessionmaker(engine)
            with app.state.session_factory() as session:
                # This local server uses one worker; an old running row represents an interrupted process.
                for run in session.scalars(select(RunRow).where(RunRow.status == "running")):
                    run.status = "failed"
                    run.finished_at = datetime.now(UTC)
                    run.counts = run.counts | {"error": "API restarted during processing. Start a new run."}
                session.commit()
        yield
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
