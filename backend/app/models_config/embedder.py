"""An Embedder for the long-lived KnowledgeService that follows the current embed setting."""
from __future__ import annotations

from typing import Protocol

from app.kb.contracts import EmbeddingBatch
from app.models_config.resolver import ActiveModels
from app.models_config.steps import EMBED_DIMENSIONS
from app.models_config.types import ModelChoice, Step


class _Store(Protocol):
    def choice(self, step: Step) -> ModelChoice: ...

    def active(self) -> ActiveModels: ...


class ConfiguredEmbedder:
    dimensions = EMBED_DIMENSIONS

    def __init__(self, store: _Store) -> None:
        self._store = store

    @property
    def model(self) -> str:
        return self._store.choice(Step.EMBED).model

    async def embed(self, texts: list[str]) -> EmbeddingBatch:
        # KnowledgeService re-reads `model` after embedding and rejects a switch mid-call.
        return await self._store.active().embedder().embed(texts)
