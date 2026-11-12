"""Ollama: local chat models, OpenAI-compatible embeddings and the installed-model list."""
from __future__ import annotations

import asyncio
import threading
import time
from collections.abc import Callable, Mapping
from typing import Any

import httpx

from app.config import Settings
from app.kb.embeddings import OpenAICompatibleEmbedder
from app.models_config.providers.base import UnsupportedOperation
from app.models_config.types import Capability, CatalogEntry, CatalogKind, ProviderStatus

CATALOG_TIMEOUT_S = 10.0
STATUS_TIMEOUT_S = 2.0
STATUS_TTL_S = 15.0
_CAPABILITIES = {
    "completion": Capability.STRUCTURED,  # Ollama applies JSON-schema output to any completion model.
    "tools": Capability.TOOLS,
    "vision": Capability.VISION,
    "thinking": Capability.THINKING,
    "embedding": Capability.EMBEDDING,
}


class OllamaProvider:
    name = "ollama"
    locality = "local"

    def __init__(self, settings: Settings, *, transport: httpx.BaseTransport | None = None,
                 clock: Callable[[], float] = time.monotonic) -> None:
        self._base = settings.ollama_base_url
        self._transport = transport
        self._clock = clock
        self._lock = threading.Lock()
        self._cached: tuple[float, ProviderStatus] | None = None

    def status(self) -> ProviderStatus:
        with self._lock:
            if self._cached is not None and self._clock() - self._cached[0] < STATUS_TTL_S:
                return self._cached[1]
        try:
            with httpx.Client(transport=self._transport, timeout=STATUS_TIMEOUT_S) as client:
                client.get(f"{self._base}/api/version").raise_for_status()
            status = ProviderStatus(self.name, self.locality, "ready")
        except httpx.HTTPError:
            status = ProviderStatus(self.name, self.locality, "unreachable",
                                    f"Ollama is not reachable at {self._base}.")
        with self._lock:
            self._cached = (self._clock(), status)
        return status

    async def catalog(self, kind: CatalogKind) -> list[CatalogEntry]:
        async with httpx.AsyncClient(transport=self._transport, timeout=CATALOG_TIMEOUT_S) as client:
            response = await client.get(f"{self._base}/api/tags")
            response.raise_for_status()
            names = []
            for item in response.json().get("models") or []:
                name = (item.get("model") or item.get("name")) if isinstance(item, dict) else None
                if isinstance(name, str) and name:
                    names.append(name)
            details = await asyncio.gather(*(self._show(client, name) for name in names))
        return [CatalogEntry(id=name, name=name, capabilities=capabilities, price_in_per_m=0.0,
                             price_out_per_m=0.0, context_length=context)
                for name, (capabilities, context) in zip(names, details, strict=True)]

    async def _show(self, client: httpx.AsyncClient, name: str):
        try:
            response = await client.post(f"{self._base}/api/show", json={"model": name})
            response.raise_for_status()
            body = response.json()
        except (httpx.HTTPError, ValueError):
            return None, None
        raw = body.get("capabilities") if isinstance(body, dict) else None
        capabilities = (frozenset(_CAPABILITIES[item] for item in raw if item in _CAPABILITIES)
                        if isinstance(raw, list) else None)
        info = body.get("model_info") if isinstance(body, dict) else None
        context = next((value for key, value in (info or {}).items()
                        if key.endswith(".context_length") and isinstance(value, int)), None)
        return capabilities, context

    def chat_model(self, model: str, *, temperature: float | None, timeout_s: float,
                   options: Mapping[str, Any]):
        from langchain_ollama import ChatOllama

        return ChatOllama(model=model, base_url=self._base, temperature=temperature,
                          reasoning=options.get("think"), client_kwargs={"timeout": timeout_s},
                          validate_model_on_init=False)

    def embedder(self, model: str, *, dimensions: int) -> OpenAICompatibleEmbedder:
        return OpenAICompatibleEmbedder(model=model, dimensions=dimensions,
                                        url=f"{self._base}/v1/embeddings", send_dimensions=False,
                                        transport=self._transport)

    def classifier(self, model: str):
        raise UnsupportedOperation("Ollama does not provide the Jev classifier.")
