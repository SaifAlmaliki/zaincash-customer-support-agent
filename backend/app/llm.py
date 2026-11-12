"""Structured-output sampling over any LangChain chat model, behind a small protocol."""
from __future__ import annotations

import asyncio
from collections.abc import Callable
from dataclasses import dataclass
from typing import Any, Generic, Protocol, TypeVar

import httpx
from pydantic import BaseModel

T = TypeVar("T", bound=BaseModel)


class LLMUnavailable(RuntimeError):
    """The generative model could not produce a usable answer."""


@dataclass(frozen=True)
class Sample(Generic[T]):
    parsed: T | None
    cost_usd: float
    error: str | None = None


class StructuredLLM(Protocol):
    async def sample(
        self, prompt: str, schema: type[T], *, temperature: float, n: int = 1
    ) -> list[Sample[T]]: ...


class StructuredChatLLM:
    """`chat.with_structured_output(method="json_schema", include_raw=True)` for any provider."""

    def __init__(
        self,
        *,
        chat_factory: Callable[[float], Any],
        price_in_per_m: float,
        price_out_per_m: float,
        max_retries: int = 2,
    ) -> None:
        self._chat_factory = chat_factory
        self._price_in = price_in_per_m
        self._price_out = price_out_per_m
        self._max_retries = max_retries
        self._cache: dict[tuple[type, float], Any] = {}

    def _runnable(self, schema: type[BaseModel], temperature: float) -> Any:
        key = (schema, temperature)
        if key not in self._cache:
            chat = self._chat_factory(temperature)
            self._cache[key] = chat.with_structured_output(schema, method="json_schema", include_raw=True)
        return self._cache[key]

    async def sample(self, prompt, schema, *, temperature, n=1):
        runnable = self._runnable(schema, temperature)
        results = await asyncio.gather(*(self._invoke(runnable, prompt) for _ in range(n)))
        return [self.to_sample(r) for r in results]

    async def _invoke(self, runnable, prompt):
        """Retry transient failures at most max_retries times per sample."""
        for attempt in range(max(0, self._max_retries) + 1):
            try:
                return await runnable.ainvoke(prompt)
            except Exception as exc:
                status = getattr(exc, "status_code", None)
                transient = isinstance(exc, httpx.TransportError) or (
                    isinstance(status, int) and (status in (408, 429) or status >= 500)
                )
                if not transient or attempt >= self._max_retries:
                    return exc
                await asyncio.sleep(min(0.5 * 2**attempt, 8.0))

    def to_sample(self, result: Any) -> Sample:
        if isinstance(result, BaseException):
            return Sample(None, 0.0, f"{type(result).__name__}: {result}")
        usage = getattr(result.get("raw"), "usage_metadata", None) or {}
        cost = (
            usage.get("input_tokens", 0) * self._price_in
            + usage.get("output_tokens", 0) * self._price_out
        ) / 1e6
        metadata = getattr(result.get("raw"), "response_metadata", None) or {}
        if metadata.get("cost") is not None:
            cost = float(metadata["cost"])  # Includes provider-specific pricing and cache discounts.
        parsed = result.get("parsed")
        if parsed is None:
            return Sample(None, cost, str(result.get("parsing_error") or "no parsed output"))
        return Sample(parsed, cost)
