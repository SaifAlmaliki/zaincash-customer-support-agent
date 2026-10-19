"""Bounded multimodal intake adapter. It does not bind transaction or knowledge tools."""
from __future__ import annotations

import asyncio
import base64
import time
from pathlib import Path

import httpx
from langchain_core.messages import HumanMessage, SystemMessage

from app.config import Settings
from app.intake.contracts import (
    Analysis,
    ImageInput,
    IntakeState,
    ModelCall,
    ReviewText,
    TurnContext,
)
from app.intake.errors import InvalidEvidence, ModelUnavailable
from app.intake.evidence import merge_analysis
from app.intake.policy import material_keys
from app.intake.review import validate_review_numbers

_PROMPTS = Path(__file__).with_name("prompts")
_INTAKE_PROMPT = (_PROMPTS / "intake_v1.md").read_text(encoding="utf-8")
_REVIEW_PROMPT = (_PROMPTS / "review_v1.md").read_text(encoding="utf-8")
_PROMPT_LIMIT = 24_000


class ModelBudget:
    def __init__(self, timeout_s: float, max_requests: int) -> None:
        self.timeout_s = timeout_s
        self.max_requests = max_requests
        self.deadline = time.monotonic() + timeout_s
        self.used = 0
        self.trace: list[dict] = []

    def remaining_s(self) -> float:
        return self.deadline - time.monotonic()

    def consume(self) -> None:
        if self.remaining_s() <= 0 or self.used >= self.max_requests:
            raise ModelUnavailable("Intake model budget is exhausted.", trace=self.trace)
        self.used += 1


class OpenRouterIntakeModel:
    def __init__(self, settings: Settings, *, runnable_factory=None) -> None:
        self.settings = settings
        self._runnable_factory = runnable_factory
        self._cache: dict[type, object] = {}

    async def analyze(self, context: TurnContext, images: list[ImageInput], budget: ModelBudget) -> ModelCall:
        system, blocks = _analysis_prompt(context, images)
        return await self._invoke(Analysis, system, blocks, budget,
            validate=lambda value: merge_analysis(context, value, visible_image_ids={item.id for item in images}))

    async def summarize(self, state: IntakeState, language: str, budget: ModelBudget) -> ModelCall:
        system, blocks = _review_prompt(state, language)
        def validate(value):
            validate_review_numbers(state, value)
            if not set(material_keys(state.category)).issubset(value.fact_keys):
                raise InvalidEvidence("Include all required_fact_keys, even when their values are unknown.")
        return await self._invoke(ReviewText, system, blocks, budget, validate=validate)

    def _runnable(self, schema: type):
        if self._runnable_factory is not None:
            return self._runnable_factory(schema)
        if schema not in self._cache:
            from langchain_openrouter import ChatOpenRouter

            chat = ChatOpenRouter(
                model=self.settings.intake_model or self.settings.gemini_model,
                api_key=self.settings.openrouter_api_key,
                timeout=int(self.settings.intake_timeout_s * 1000),
                max_retries=0,
                model_kwargs={"retries": None},
            )
            self._cache[schema] = chat.with_structured_output(schema, method="json_schema", include_raw=True)
        return self._cache[schema]

    async def _invoke(self, schema: type, system: str, blocks: list[dict], budget: ModelBudget, *, validate=None) -> ModelCall:
        repaired = False
        trace_start = len(budget.trace)
        while True:
            budget.consume()
            started = time.monotonic()
            try:
                async with asyncio.timeout(budget.remaining_s()):
                    result = await self._runnable(schema).ainvoke([
                        SystemMessage(content=system), HumanMessage(content=blocks),
                    ])
            except ModelUnavailable:
                raise
            except Exception as exc:
                _record(budget, self._model_name(), exc, None, started)
                if _transient(exc) and budget.used < budget.max_requests and budget.remaining_s() > 0:
                    continue
                raise ModelUnavailable("The assistant is temporarily unavailable.", trace=budget.trace) from exc
            _record(budget, self._model_name(), None, result, started)
            parsed = result.get("parsed") if isinstance(result, dict) else None
            try:
                if not isinstance(parsed, schema):
                    parsed = schema.model_validate(parsed)
                if validate is not None:
                    validate(parsed)
            except Exception as exc:
                budget.trace[-1]["error"] = type(exc).__name__
                if isinstance(exc, InvalidEvidence):
                    budget.trace[-1]["validation_error"] = exc.message
                if not repaired and budget.used < budget.max_requests and budget.remaining_s() > 0:
                    repaired = True
                    detail = exc.message if isinstance(exc, InvalidEvidence) else "Return one object matching the schema."
                    blocks = [*blocks, {"type": "text", "text": f"The previous output was rejected: {detail} Use the exact source UUIDs and grounded values from the supplied input; include evidence on every known fact."}]
                    continue
                raise ModelUnavailable("The assistant returned an unusable response.", trace=budget.trace) from exc
            return ModelCall(parsed, list(budget.trace[trace_start:]))

    def _model_name(self) -> str:
        return self.settings.intake_model or self.settings.gemini_model


def _transient(exc: Exception) -> bool:
    status = getattr(exc, "status_code", None)
    return isinstance(exc, httpx.TransportError) or (isinstance(status, int) and (status in {408, 429} or status >= 500))


def _record(budget: ModelBudget, model: str, error: Exception | None, result, started: float) -> None:
    usage = {}
    cost = None
    if isinstance(result, dict):
        raw = result.get("raw")
        usage = dict(getattr(raw, "usage_metadata", None) or {})
        metadata = getattr(raw, "response_metadata", None) or {}
        if metadata.get("cost") is not None:
            cost = float(metadata["cost"])
    budget.trace.append({
        "model": model,
        "latency_ms": round((time.monotonic() - started) * 1000),
        "usage": usage or None,
        "cost_usd": cost,
        "error": None if error is None else type(error).__name__,
    })


def _analysis_prompt(context: TurnContext, images: list[ImageInput]) -> tuple[str, list[dict]]:
    payload = _bounded_context(context)
    blocks: list[dict] = [{"type": "text", "text": payload}]
    for image in images:
        encoded = base64.b64encode(image.data).decode("ascii")
        blocks.append({"type": "text", "text": f"Attachment ID: {image.id}"})
        blocks.append({"type": "image_url", "image_url": {"url": f"data:{image.mime_type};base64,{encoded}"}})
    _guard_size(blocks)
    return _INTAKE_PROMPT, blocks


def _review_prompt(state: IntakeState, language: str) -> tuple[str, list[dict]]:
    payload = state.model_dump_json()
    keys = list(dict.fromkeys([*material_keys(state.category), *state.facts]))
    blocks = [{"type": "text", "text": f"Requested language: {language}\nrequired_fact_keys: {keys}\n{payload}"}]
    _guard_size(blocks)
    return _REVIEW_PROMPT, blocks


def _bounded_context(context: TurnContext) -> str:
    recent = context.messages[-6:]
    current = next((item for item in context.messages if item.id == context.current_message_id), None)
    body = {
        "language": context.state.language,
        "category": context.state.category,
        "facts": context.state.model_dump(mode="json")["facts"],
        "additional_needed": context.state.additional_needed,
        "additional_issues": [item.model_dump(mode="json") for item in context.state.additional_issues],
        "questions": [item.model_dump(mode="json") for item in context.state.questions],
        "attachments": [item.model_dump(mode="json") for item in context.attachments if not item.removed],
        "readiness": context.state.readiness.model_dump(mode="json"),
        "current_message": None if current is None else current.model_dump(mode="json"),
        "recent_messages": [item.model_dump(mode="json") for item in recent],
    }
    import json
    return json.dumps(body, ensure_ascii=False, default=str)


def _guard_size(blocks: list[dict]) -> None:
    size = sum(len(block.get("text", "")) for block in blocks if block.get("type") == "text")
    if size > _PROMPT_LIMIT:
        raise ModelUnavailable("The conversation is too large to review safely.", trace=[])
