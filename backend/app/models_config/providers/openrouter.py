"""OpenRouter: cloud chat models, embeddings and the public model catalog."""
from __future__ import annotations

from collections.abc import Mapping
from typing import Any

import httpx

from app.config import Settings
from app.kb.embeddings import OpenAICompatibleEmbedder
from app.models_config.providers.base import UnsupportedOperation
from app.models_config.types import Capability, CatalogEntry, CatalogKind, ProviderStatus

OPENROUTER_API = "https://openrouter.ai/api/v1"
CATALOG_TIMEOUT_S = 10.0


def _per_million(value: Any) -> float | None:
    try:
        price = float(value)
    except (TypeError, ValueError):
        return None
    return price * 1_000_000 if price >= 0 else None


def _capabilities(item: dict, kind: CatalogKind) -> frozenset[Capability]:
    if kind == "embedding":
        return frozenset({Capability.EMBEDDING})
    params = set(item.get("supported_parameters") or [])
    modalities = set((item.get("architecture") or {}).get("input_modalities") or [])
    found = set()
    if "tools" in params:
        found.add(Capability.TOOLS)
    if "structured_outputs" in params:
        found.add(Capability.STRUCTURED)
    if "reasoning" in params:
        found.add(Capability.THINKING)
    if "image" in modalities:
        found.add(Capability.VISION)
    return frozenset(found)


class OpenRouterProvider:
    name = "openrouter"
    locality = "cloud"

    def __init__(self, settings: Settings, *, transport: httpx.AsyncBaseTransport | None = None) -> None:
        self._settings = settings
        self._transport = transport

    def status(self) -> ProviderStatus:
        if not self._settings.openrouter_api_key:
            return ProviderStatus(self.name, self.locality, "missing_key", "Set OPENROUTER_API_KEY in .env.")
        return ProviderStatus(self.name, self.locality, "ready")

    async def catalog(self, kind: CatalogKind) -> list[CatalogEntry]:
        path = "/embeddings/models" if kind == "embedding" else "/models"
        async with httpx.AsyncClient(
            transport=self._transport, timeout=CATALOG_TIMEOUT_S,
            headers={"Authorization": f"Bearer {self._settings.openrouter_api_key}"},
        ) as client:
            response = await client.get(OPENROUTER_API + path)
            response.raise_for_status()
        entries = []
        for item in response.json().get("data") or []:
            if not isinstance(item, dict) or not isinstance(item.get("id"), str):
                continue
            pricing = item.get("pricing") or {}
            context = item.get("context_length")
            entries.append(CatalogEntry(
                id=item["id"], name=str(item.get("name") or item["id"]),
                capabilities=_capabilities(item, kind),
                price_in_per_m=_per_million(pricing.get("prompt")),
                price_out_per_m=_per_million(pricing.get("completion")),
                context_length=context if isinstance(context, int) else None,
            ))
        return entries

    def chat_model(self, model: str, *, temperature: float | None, timeout_s: float,
                   options: Mapping[str, Any]):
        from app.models_config.providers.openrouter_chat import OpenRouterChat

        extra: dict[str, Any] = {}
        if options.get("think") is not None:
            extra["reasoning"] = {"enabled": bool(options["think"])}
        # The caller owns bounded retries; the SDK must never retry on its own.
        return OpenRouterChat(model=model, temperature=temperature,
                              api_key=self._settings.openrouter_api_key,
                              timeout=int(timeout_s * 1000), max_retries=0,
                              model_kwargs={"retries": None}, **extra)

    def embedder(self, model: str, *, dimensions: int) -> OpenAICompatibleEmbedder:
        return OpenAICompatibleEmbedder(
            model=model, dimensions=dimensions, url=f"{OPENROUTER_API}/embeddings",
            api_key=self._settings.openrouter_api_key, price_per_m=self._settings.price_embedding_in,
            transport=self._transport, provider="openrouter",
        )

    def classifier(self, model: str):
        raise UnsupportedOperation("OpenRouter does not provide the Jev classifier.")
