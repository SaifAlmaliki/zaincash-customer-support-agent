"""One record per AI request (spec §4.3).

Call sites call `record()`. The owner of the work (batch ticket, intake turn, indexing
attempt, API request) opens a `call_context()` and writes the buffered calls itself.
"""
from __future__ import annotations

import logging
import math
import uuid
from collections.abc import Iterator, Mapping
from contextlib import contextmanager
from contextvars import ContextVar
from dataclasses import dataclass, field
from datetime import UTC, datetime
from time import perf_counter
from typing import Any

logger = logging.getLogger(__name__)

TICKET_PROCESSES = ("intake", "classify", "extract", "draft", "draft_search", "credential_check")
UNATTRIBUTED_PROCESSES = ("kb_index", "kb_search", "probe")
PROCESSES = TICKET_PROCESSES + UNATTRIBUTED_PROCESSES


@dataclass(frozen=True)
class AiCall:
    process: str
    provider: str
    model: str
    locality: str
    started_at: datetime
    latency_ms: int
    input_tokens: int | None = None
    output_tokens: int | None = None
    cost_usd: float = 0.0
    cost_source: str = "unknown"
    status: str = "ok"
    error: str | None = None
    attempt: int = 1
    detail: Mapping[str, Any] = field(default_factory=dict)


@dataclass
class CallContext:
    run_id: int | None = None
    ticket_id: int | None = None
    intake_session_id: uuid.UUID | None = None
    document_id: int | None = None
    calls: list[AiCall] = field(default_factory=list)


# Child tasks (LangGraph nodes, gathered calls) inherit the owner's buffer.
current_calls: ContextVar[CallContext | None] = ContextVar("ai_calls", default=None)


def record(call: AiCall) -> None:
    context = current_calls.get()
    if context is None:
        logger.debug("AI call outside a recording context: %s %s", call.process, call.model)
        return
    context.calls.append(call)


@contextmanager
def call_context(**links: Any) -> Iterator[CallContext]:
    context = CallContext(**links)
    token = current_calls.set(context)
    try:
        yield context
    finally:
        current_calls.reset(token)


class Timer:
    def __init__(self) -> None:
        self.started_at = datetime.now(UTC)
        self._start = perf_counter()

    def ms(self) -> int:
        return max(0, round((perf_counter() - self._start) * 1000))


def count(value: Any) -> int | None:
    if isinstance(value, bool) or not isinstance(value, int | float):
        return None
    if not math.isfinite(value) or value < 0:
        return None
    return int(value)


def money(value: Any) -> float | None:
    if isinstance(value, bool) or not isinstance(value, int | float):
        return None
    if not math.isfinite(value) or value < 0:
        return None
    return float(value)


def usage_of(message: Any) -> tuple[int | None, int | None, float | None]:
    usage = dict(getattr(message, "usage_metadata", None) or {})
    meta = dict(getattr(message, "response_metadata", None) or {})
    tokens_in = count(usage.get("input_tokens", meta.get("prompt_eval_count")))
    tokens_out = count(usage.get("output_tokens", meta.get("eval_count")))
    return tokens_in, tokens_out, money(meta.get("cost"))


def cost_for(*, input_tokens: int | None, output_tokens: int | None, provider_cost: float | None,
             prices: tuple[float, float] | None, local: bool) -> tuple[float, str]:
    if local:
        return 0.0, "local"
    if provider_cost is not None:
        return provider_cost, "provider"
    if prices is not None and input_tokens is not None:
        return (input_tokens * prices[0] + (output_tokens or 0) * prices[1]) / 1e6, "estimate"
    return 0.0, "unknown"


def short_error(exc: BaseException) -> str:
    # Provider messages can echo the prompt; keep only the type and an HTTP status.
    status = getattr(exc, "status_code", None)
    if isinstance(status, int):
        return f"{type(exc).__name__}: HTTP {status}"[:300]
    return type(exc).__name__[:300]


def embed_process() -> str:
    context = current_calls.get()
    if context is not None and context.document_id is not None:
        return "kb_index"
    if context is not None and (context.ticket_id is not None or context.run_id is not None):
        return "draft_search"
    return "kb_search"
