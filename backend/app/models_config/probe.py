"""Tiny live tests: a model is saved only if it can do its step's real job once."""
from __future__ import annotations

import asyncio
import re
import time
from collections.abc import Awaitable, Callable, Mapping

from langchain_core.messages import HumanMessage
from langchain_core.tools import tool
from pydantic import BaseModel

from app.models_config.providers.base import Provider
from app.models_config.providers.registry import ProviderRegistry
from app.models_config.steps import DEFAULT_TEMPERATURE, EMBED_DIMENSIONS, PROVIDERS_FOR_STEP
from app.models_config.types import ModelChoice, ProbeResult, Step

PROBE_TIMEOUT_S = 60.0
_URL = re.compile(r"https?://\S+")
_SECRET = re.compile(r"sk-[A-Za-z0-9_\-]{8,}|Bearer\s+\S+")
_PIXEL = ("data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8"
          "z8BQDwAEhQGAhKmMIQAAAABJRU5ErkJggg==")


class _ProbeAnswer(BaseModel):
    word: str


@tool
def record_number(number: int) -> str:
    """Record the number the user asks you to record."""
    return "recorded"


def _scrub(text: str) -> str:
    """Provider messages can echo URLs and keys; neither may reach the admin API."""
    return _SECRET.sub("<redacted>", _URL.sub("<url>", text))[:300]


def _chat(provider: Provider, choice: ModelChoice, step: Step):
    temperature = choice.options.get("temperature", DEFAULT_TEMPERATURE.get(step))
    return provider.chat_model(choice.model, temperature=temperature,
                               timeout_s=PROBE_TIMEOUT_S, options=choice.options)


async def _structured(provider: Provider, choice: ModelChoice, step: Step, *, image: bool) -> str | None:
    runnable = _chat(provider, choice, step).with_structured_output(_ProbeAnswer, method="json_schema", include_raw=True)
    content: list[dict] = [{"type": "text", "text": 'Return JSON with the field "word" set to "ok".'}]
    if image:
        content.append({"type": "image_url", "image_url": {"url": _PIXEL}})
    result = await runnable.ainvoke([HumanMessage(content=content)])
    if isinstance(result, dict) and result.get("parsed") is not None:
        return None
    reason = result.get("parsing_error") if isinstance(result, dict) else None
    return _scrub(f"The model did not return the required JSON ({reason or 'no output'}).")


async def _intake(provider: Provider, choice: ModelChoice) -> str | None:
    return await _structured(provider, choice, Step.INTAKE, image=True)


async def _extract(provider: Provider, choice: ModelChoice) -> str | None:
    return await _structured(provider, choice, Step.EXTRACT, image=False)


async def _draft(provider: Provider, choice: ModelChoice) -> str | None:
    chat = _chat(provider, choice, Step.DRAFT).bind_tools([record_number])
    message = await chat.ainvoke([HumanMessage(
        content="Call the record_number tool with number 7. Do not answer in text.")])
    for item in getattr(message, "tool_calls", None) or []:
        if item.get("name") == "record_number" and str((item.get("args") or {}).get("number")) == "7":
            return None
    return "The model did not call the test tool correctly."


async def _embed(provider: Provider, choice: ModelChoice) -> str | None:
    batch = await provider.embedder(choice.model, dimensions=EMBED_DIMENSIONS).embed(["probe"])
    if len(batch.vectors) == 1 and len(batch.vectors[0]) == EMBED_DIMENSIONS:
        return None
    return f"Expected one {EMBED_DIMENSIONS}-dimension vector."


async def _classify(provider: Provider, choice: ModelChoice) -> str | None:
    from langchain_typesafe import Noul, NoulCriteria

    response = await provider.classifier(choice.model).ainvoke({
        "state": {"text": "probe"},
        "questions": {"probe": Noul(instructions="Is `text` empty?",
                                    criteria=NoulCriteria(true="It is empty.", false="It has text."))},
    })
    nouls = getattr(response, "nouls", None)
    return None if isinstance(nouls, Mapping) and "probe" in nouls else "Jev did not answer the test question."


_CHECKS: dict[Step, Callable[[Provider, ModelChoice], Awaitable[str | None]]] = {
    Step.INTAKE: _intake, Step.CLASSIFY: _classify, Step.EXTRACT: _extract,
    Step.DRAFT: _draft, Step.EMBED: _embed,
}


def _describe(error: BaseException) -> str:
    if isinstance(error, TimeoutError):
        return f"The model did not answer within {PROBE_TIMEOUT_S:g} seconds."
    return _scrub(f"{type(error).__name__}: {error}")


async def probe(step: Step, choice: ModelChoice, registry: ProviderRegistry) -> ProbeResult:
    started = time.monotonic()
    try:
        if choice.provider not in PROVIDERS_FOR_STEP[step]:
            raise ValueError(f"{choice.provider} cannot run the {step.value} step.")
        provider = registry.get(choice.provider)
        async with asyncio.timeout(PROBE_TIMEOUT_S):
            error = await _CHECKS[step](provider, choice)
    except Exception as exc:  # every failure is reported to the admin, never raised
        error = _describe(exc)
    return ProbeResult(error is None, round((time.monotonic() - started) * 1000), error)
