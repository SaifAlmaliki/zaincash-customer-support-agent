"""Admin-only model configuration. Every route requires X-Admin-Token == ADMIN_TOKEN."""
from __future__ import annotations

import hmac
from typing import Annotated

from fastapi import (
    APIRouter,
    BackgroundTasks,
    Depends,
    Header,
    HTTPException,
    Query,
    Request,
    Response,
)
from pydantic import BaseModel, ConfigDict, Field
from starlette.concurrency import run_in_threadpool

from app.models_config.catalog import step_catalog
from app.models_config.embedding_switch import SwitchConflict
from app.models_config.pricing import with_catalog_prices
from app.models_config.probe import probe
from app.models_config.steps import CATALOG_KIND, PROVIDERS_FOR_STEP
from app.models_config.types import ModelChoice, Step
from app.telemetry.probe import probe_call
from app.telemetry.store import persist_calls


def require_admin(request: Request, x_admin_token: Annotated[str | None, Header()] = None) -> None:
    expected = request.app.state.settings.admin_token
    if not expected:
        raise HTTPException(403, "admin_disabled")
    supplied = (x_admin_token or "").encode("utf-8", "surrogateescape")
    if not supplied or not hmac.compare_digest(supplied, expected.encode("utf-8")):
        raise HTTPException(401, "invalid_admin_token")


router = APIRouter(prefix="/api/admin", tags=["Admin"], dependencies=[Depends(require_admin)])


class ModelOptions(BaseModel):
    model_config = ConfigDict(extra="forbid")
    temperature: float | None = Field(default=None, ge=0, le=2)
    think: bool | None = None


class ChoiceInput(BaseModel):
    model_config = ConfigDict(extra="forbid")
    provider: str = Field(min_length=1, max_length=32)
    model: str = Field(min_length=1, max_length=255)
    options: ModelOptions = Field(default_factory=ModelOptions)

    def choice(self) -> ModelChoice:
        return ModelChoice(self.provider.strip(), self.model.strip(), self.options.model_dump(exclude_none=True))


class ProbeInput(ChoiceInput):
    step: Step


class SaveInput(ChoiceInput):
    changed_by: str = Field(min_length=1, max_length=64)


def _store(request: Request):
    return request.app.state.model_store


def _check_provider(step: Step, choice: ModelChoice) -> None:
    if choice.provider not in PROVIDERS_FOR_STEP[step]:
        raise HTTPException(422, f"{choice.provider} cannot run the {step.value} step.")


async def _priced(request: Request, step: Step, choice: ModelChoice) -> ModelChoice:
    try:
        entries = await request.app.state.catalog.entries(choice.provider, CATALOG_KIND[step])
    except Exception:
        return choice  # an unreachable catalog only means no saved price
    return with_catalog_prices(choice, entries)


async def _record_probe(request: Request, step: Step, choice: ModelChoice, result) -> None:
    try:
        locality = _store(request).registry.get(choice.provider).locality
    except Exception:
        locality = "cloud"
    await run_in_threadpool(persist_calls, request.app.state.session_factory,
                            [probe_call(step, choice, result, locality)])


async def _tested(request: Request, step: Step, body: ChoiceInput):
    choice = body.choice()
    _check_provider(step, choice)
    result = await probe(step, choice, _store(request).registry)
    await _record_probe(request, step, choice, result)
    if not result.ok:
        raise HTTPException(422, f"Model test failed: {result.error}")
    choice = await _priced(request, step, choice)
    return choice, result


@router.post("/session", status_code=204)
def session() -> Response:
    return Response(status_code=204)


@router.get("/models")
async def models(request: Request):
    return {"steps": await run_in_threadpool(_store(request).describe)}


@router.get("/models/catalog")
async def catalog(request: Request, step: Step, refresh: bool = False):
    store = _store(request)
    return {"step": step.value,
            "providers": await step_catalog(step, store.registry, request.app.state.catalog, refresh=refresh)}


@router.post("/models/test")
async def test_model(request: Request, body: ProbeInput):
    choice = body.choice()
    _check_provider(body.step, choice)
    result = await probe(body.step, choice, _store(request).registry)
    await _record_probe(request, body.step, choice, result)
    return result.to_json()


@router.put("/models/{step}")
async def save_model(request: Request, step: Step, body: SaveInput):
    if step is Step.EMBED:
        raise HTTPException(400, "use_embedding_switch")
    choice, result = await _tested(request, step, body)
    store = _store(request)
    await run_in_threadpool(lambda: store.save(step, choice, changed_by=body.changed_by.strip(),
                                               latency_ms=result.latency_ms))
    described = await run_in_threadpool(store.describe)
    return next(item for item in described if item["step"] == step.value)


@router.post("/models/embed/switch", status_code=202)
async def start_embedding_switch(request: Request, body: SaveInput, background: BackgroundTasks):
    switches = request.app.state.embedding_switches
    if await run_in_threadpool(switches.running):
        raise HTTPException(409, "switch_in_progress")
    choice, result = await _tested(request, Step.EMBED, body)
    try:
        view = await run_in_threadpool(lambda: switches.start(
            choice, changed_by=body.changed_by.strip(), latency_ms=result.latency_ms))
    except SwitchConflict as exc:
        raise HTTPException(409, exc.code) from None
    background.add_task(switches.run, view["id"])
    return view


@router.get("/models/embed/switch")
async def embedding_switch(request: Request):
    return await run_in_threadpool(request.app.state.embedding_switches.current)


@router.get("/models/audit")
async def audit(request: Request, limit: Annotated[int, Query(ge=1, le=200)] = 50):
    return {"items": await run_in_threadpool(_store(request).audit, limit)}
