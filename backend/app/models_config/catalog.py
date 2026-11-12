"""Per-provider model listings, cached briefly and filtered by what a step needs."""
from __future__ import annotations

import asyncio
import time
from collections.abc import Callable
from typing import Any

from app.models_config.providers.registry import ProviderRegistry
from app.models_config.steps import CATALOG_KIND, PROVIDERS_FOR_STEP, eligibility
from app.models_config.types import CatalogEntry, CatalogKind, Step


class CatalogCache:
    def __init__(self, registry: ProviderRegistry, *, ttl_s: float = 300.0,
                 clock: Callable[[], float] = time.monotonic) -> None:
        self._registry, self._ttl, self._clock = registry, ttl_s, clock
        self._entries: dict[tuple[str, CatalogKind], tuple[float, list[CatalogEntry]]] = {}

    async def entries(self, provider_name: str, kind: CatalogKind, *, refresh: bool = False) -> list[CatalogEntry]:
        key = (provider_name, kind)
        cached = self._entries.get(key)
        if not refresh and cached is not None and self._clock() - cached[0] < self._ttl:
            return cached[1]
        entries = await self._registry.get(provider_name).catalog(kind)
        self._entries[key] = (self._clock(), entries)
        return entries


async def step_catalog(step: Step, registry: ProviderRegistry, cache: CatalogCache, *,
                       refresh: bool = False) -> list[dict[str, Any]]:
    providers = []
    for name in PROVIDERS_FOR_STEP[step]:
        status = await asyncio.to_thread(registry.status, name)
        item: dict[str, Any] = {"provider": name, "locality": status.locality, "status": status.state,
                                "status_detail": status.detail, "entries": [], "error": None}
        if status.state == "ready":
            try:
                entries = await cache.entries(name, CATALOG_KIND[step], refresh=refresh)
            except Exception as exc:
                item["error"] = f"Could not list models: {type(exc).__name__}"
            else:
                listed = []
                for entry in sorted(entries, key=lambda value: value.name.lower()):
                    verdict = eligibility(step, entry.capabilities)
                    if verdict != "ineligible":
                        listed.append(entry.to_json() | {"eligibility": verdict})
                item["entries"] = listed
        providers.append(item)
    return providers
