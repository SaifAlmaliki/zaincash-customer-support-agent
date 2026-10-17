from __future__ import annotations

from typing import Protocol

from app.kb.service import KnowledgeExecutionError
from app.pipeline.contracts import DraftResult
from app.pipeline.state import PipelineState


class Drafter(Protocol):
    async def draft(self, state: PipelineState) -> DraftResult: ...


class DraftExecutionError(RuntimeError):
    """Unexpected fault, with completed drafting evidence and measured spend.

    The pipeline records a failed outcome, never a provider-unavailable escalation.
    The immediate exception remains available as __cause__; retrieval faults
    carry their original diagnostic type in a sanitized service exception.
    """

    def __init__(self, cause: Exception, result: DraftResult):
        message = str(cause) if isinstance(cause, KnowledgeExecutionError) else f"{type(cause).__name__}: {str(cause)[:500]}"
        super().__init__(message)
        self.result = result


class NullDrafter:
    """Explicit classification-only operation, with an auditable skipped stage."""

    def __init__(self, reason: str = "rag_disabled") -> None:
        self.reason = reason

    async def draft(self, state: PipelineState) -> DraftResult:
        return DraftResult(trace=({"kind": "skipped", "stage": "draft", "reason": self.reason},))


class UnavailableDrafter:
    """RAG requested but its provider is unconfigured; preserve earlier stages."""

    async def draft(self, state: PipelineState) -> DraftResult:
        return DraftResult(reasons=("llm_unavailable",), trace=({
            "kind": "draft", "status": "unavailable", "reasons": ["llm_unavailable"],
            "internal_note": "Drafting unavailable: OPENROUTER_API_KEY is missing.", "cost_usd": 0.0,
        },))
