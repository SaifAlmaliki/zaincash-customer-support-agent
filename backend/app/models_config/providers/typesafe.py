"""TypeSafe: the Jev classifier. It has no model catalog."""
from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from app.config import Settings
from app.models_config.providers.base import UnsupportedOperation
from app.models_config.types import CatalogEntry, CatalogKind, ProviderStatus


class TypeSafeProvider:
    name = "typesafe"
    locality = "cloud"

    def __init__(self, settings: Settings) -> None:
        self._settings = settings

    def status(self) -> ProviderStatus:
        if not self._settings.typesafe_api_key:
            return ProviderStatus(self.name, self.locality, "missing_key", "Set TYPESAFE_API_KEY in .env.")
        return ProviderStatus(self.name, self.locality, "ready")

    async def catalog(self, kind: CatalogKind) -> list[CatalogEntry]:
        return []

    def chat_model(self, model: str, *, temperature: float | None, timeout_s: float,
                   options: Mapping[str, Any]):
        raise UnsupportedOperation("TypeSafe only provides the Jev classifier.")

    def embedder(self, model: str, *, dimensions: int, price_per_m: float | None = None):
        raise UnsupportedOperation("TypeSafe only provides the Jev classifier.")

    def classifier(self, model: str):
        from langchain_typesafe import TypeSafeClassifier

        return TypeSafeClassifier(model=model, api_key=self._settings.typesafe_api_key)
