"""Look up provider adapters by name; the single place that lists every provider."""
from __future__ import annotations

from collections.abc import Mapping

from app.config import Settings
from app.models_config.providers.base import Provider
from app.models_config.providers.openrouter import OpenRouterProvider
from app.models_config.providers.typesafe import TypeSafeProvider
from app.models_config.types import ProviderStatus


class UnknownProvider(ValueError):
    pass


class ProviderRegistry:
    def __init__(self, settings: Settings, *, providers: Mapping[str, Provider] | None = None) -> None:
        if providers is None:
            providers = {
                "openrouter": OpenRouterProvider(settings),
                "typesafe": TypeSafeProvider(settings),
            }
        self._providers = dict(providers)

    def get(self, name: str) -> Provider:
        try:
            return self._providers[name]
        except KeyError:
            raise UnknownProvider(f"Unknown model provider {name!r}.") from None

    def names(self) -> tuple[str, ...]:
        return tuple(self._providers)

    def status(self, name: str) -> ProviderStatus:
        return self.get(name).status()


def provider_errors() -> tuple[type[BaseException], ...]:
    """Errors any chat provider may raise for an unusable model request."""
    import httpx
    from openrouter.errors import OpenRouterError

    from app.llm import LLMUnavailable

    return (httpx.HTTPError, OpenRouterError, LLMUnavailable)
