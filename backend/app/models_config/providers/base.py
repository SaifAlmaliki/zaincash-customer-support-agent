"""The contract every model provider adapter implements."""
from __future__ import annotations

from collections.abc import Mapping
from typing import Any, Protocol

from langchain_core.language_models.chat_models import BaseChatModel

from app.kb.contracts import Embedder
from app.models_config.types import CatalogEntry, CatalogKind, Locality, ProviderStatus


class UnsupportedOperation(ValueError):
    """The provider does not offer this kind of model."""


class Provider(Protocol):
    name: str
    locality: Locality

    def status(self) -> ProviderStatus: ...

    async def catalog(self, kind: CatalogKind) -> list[CatalogEntry]: ...

    def chat_model(self, model: str, *, temperature: float | None, timeout_s: float,
                   options: Mapping[str, Any]) -> BaseChatModel: ...

    def embedder(self, model: str, *, dimensions: int) -> Embedder: ...

    def classifier(self, model: str) -> Any: ...
