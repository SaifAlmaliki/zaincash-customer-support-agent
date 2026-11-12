import json

import httpx
import pytest

from app.config import Settings
from app.models_config.providers.openrouter import OpenRouterProvider
from app.models_config.providers.registry import ProviderRegistry, UnknownProvider, provider_errors
from app.models_config.providers.typesafe import TypeSafeProvider
from app.models_config.types import Capability


def _provider(handler=None, **kw):
    settings = Settings(_env_file=None, **({"openrouter_api_key": "test-key"} | kw))
    return OpenRouterProvider(settings, transport=httpx.MockTransport(handler) if handler else None)


def test_status_reports_missing_key():
    assert _provider(openrouter_api_key="").status().state == "missing_key"
    ready = _provider().status()
    assert ready.state == "ready" and ready.locality == "cloud"


async def test_chat_catalog_maps_capabilities_and_prices():
    def handler(request):
        assert str(request.url) == "https://openrouter.ai/api/v1/models"
        assert request.headers["authorization"] == "Bearer test-key"
        return httpx.Response(200, json={"data": [
            {"id": "anthropic/claude-sonnet-5.5", "name": "Claude Sonnet 5.5", "context_length": 200000,
             "pricing": {"prompt": "0.000003", "completion": "0.000015"},
             "architecture": {"input_modalities": ["text", "image"]},
             "supported_parameters": ["tools", "structured_outputs", "reasoning"]},
            {"id": "x/plain", "name": "Plain", "pricing": {"prompt": "-1"}, "supported_parameters": []},
            {"name": "missing id"},
        ]})

    first, plain = await _provider(handler).catalog("chat")
    assert first.capabilities == {Capability.TOOLS, Capability.STRUCTURED, Capability.THINKING, Capability.VISION}
    assert first.price_in_per_m == pytest.approx(3.0) and first.price_out_per_m == pytest.approx(15.0)
    assert first.context_length == 200000
    assert plain.capabilities == frozenset() and plain.price_in_per_m is None


async def test_embedding_catalog_uses_the_embedding_listing():
    def handler(request):
        assert str(request.url) == "https://openrouter.ai/api/v1/embeddings/models"
        return httpx.Response(200, json={"data": [{"id": "openai/text-embedding-3-small", "name": "Small"}]})

    [entry] = await _provider(handler).catalog("embedding")
    assert entry.capabilities == {Capability.EMBEDDING}


def test_chat_model_disables_sdk_retries_and_maps_thinking():
    chat = _provider().chat_model("google/gemini-3.8-flash", temperature=0.1, timeout_s=30,
                                  options={"think": False})
    assert chat.model_name == "google/gemini-3.8-flash"
    assert chat.temperature == 0.1
    assert chat.request_timeout == 30000 and chat.max_retries == 0
    assert chat.model_kwargs == {"retries": None}
    assert chat.reasoning == {"enabled": False}
    assert _provider().chat_model("m", temperature=None, timeout_s=60, options={}).reasoning is None


async def test_embedder_posts_to_openrouter_with_dimensions():
    seen = []

    def handler(request):
        seen.append(request)
        return httpx.Response(200, json={"data": [{"index": 0, "embedding": [1.0] + [0.0] * 767}]})

    batch = await _provider(handler).embedder("openai/text-embedding-3-small", dimensions=768).embed(["x"])
    assert len(batch.vectors[0]) == 768
    assert str(seen[0].url) == "https://openrouter.ai/api/v1/embeddings"
    assert json.loads(seen[0].content)["dimensions"] == 768


def test_typesafe_status_and_unsupported_chat():
    provider = TypeSafeProvider(Settings(_env_file=None, typesafe_api_key=""))
    assert provider.status().state == "missing_key"
    with pytest.raises(ValueError):
        provider.chat_model("jev-1.13.0", temperature=None, timeout_s=1, options={})


def test_registry_rejects_unknown_providers_and_exposes_errors():
    registry = ProviderRegistry(Settings(_env_file=None))
    assert {"openrouter", "typesafe"} <= set(registry.names())
    with pytest.raises(UnknownProvider):
        registry.get("nope")
    from openrouter.errors import OpenRouterError

    assert OpenRouterError in provider_errors() and httpx.HTTPError in provider_errors()
