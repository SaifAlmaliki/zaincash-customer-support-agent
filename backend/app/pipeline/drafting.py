from __future__ import annotations

from typing import Protocol

from app.pipeline.contracts import DraftResult
from app.pipeline.state import PipelineState


class Drafter(Protocol):
    async def draft(self, state: PipelineState) -> DraftResult: ...


class NullDrafter:
    """Plan 1 drafter. It produces no draft and adds no escalation reasons. Plan 3 replaces it with the RAG agent."""

    async def draft(self, state: PipelineState) -> DraftResult:
        return DraftResult()
