"""Bounded multimodal intake adapter. It does not bind transaction or knowledge tools."""
from __future__ import annotations

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
from app.intake.errors import ModelUnavailable

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
        return await self._invoke(Analysis, system, blocks, budget)

    async def summarize(self, state: IntakeState, language: str, budget: ModelBudget) -> ModelCall:
        system, blocks = _review_prompt(state, language)
        return await self._invoke(ReviewText, system, blocks, budget)

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

    async def _invoke(self, schema: type, system: str, blocks: list[dict], budget: ModelBudget) -> ModelCall:
        repaired = False
        while True:
            budget.consume()
            try:
                result = await self._runnable(schema).ainvoke([
                    SystemMessage(content=system), HumanMessage(content=blocks),
                ])
            except ModelUnavailable:
                raise
            except Exception as exc:
                _record(budget, self._model_name(), exc, None)
                if _transient(exc) and budget.used < budget.max_requests and budget.remaining_s() > 0:
                    continue
                raise ModelUnavailable("The assistant is temporarily unavailable.", trace=budget.trace) from exc
            _record(budget, self._model_name(), None, result)
            parsed = result.get("parsed") if isinstance(result, dict) else None
            if parsed is None and not repaired and budget.used < budget.max_requests and budget.remaining_s() > 0:
                repaired = True
                blocks = [*blocks, {"type": "text", "text": "The previous output did not match the schema. Return one valid object."}]
                continue
            if parsed is None or not isinstance(parsed, schema):
                try:
                    parsed = schema.model_validate(parsed)
                except Exception as exc:
                    raise ModelUnavailable("The assistant returned an unusable response.", trace=budget.trace) from exc
            return ModelCall(parsed, list(budget.trace))

    def _model_name(self) -> str:
        return self.settings.intake_model or self.settings.gemini_model


def _transient(exc: Exception) -> bool:
    status = getattr(exc, "status_code", None)
    return isinstance(exc, httpx.TransportError) or (isinstance(status, int) and (status in {408, 429} or status >= 500))


def _record(budget: ModelBudget, model: str, error: Exception | None, result) -> None:
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
    blocks = [{"type": "text", "text": f"Requested language: {language}\n{payload}"}]
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
