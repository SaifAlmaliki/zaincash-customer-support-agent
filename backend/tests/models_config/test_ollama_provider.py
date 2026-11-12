import json

import httpx

from app.config import Settings
from app.models_config.providers.ollama import OllamaProvider
from app.models_config.providers.registry import ProviderRegistry, provider_errors
from app.models_config.types import Capability

BASE = "http://ollama.test:11434"


def _provider(handler, clock=None):
    settings = Settings(_env_file=None, ollama_base_url=BASE)
    kwargs = {"clock": clock} if clock else {}
    return OllamaProvider(settings, transport=httpx.MockTransport(handler), **kwargs)


async def test_catalog_lists_installed_models_with_reported_capabilities():
    def handler(request):
        if request.url.path == "/api/tags":
            return httpx.Response(200, json={"models": [
                {"name": "qwen3:4b", "model": "qwen3:4b"},
                {"name": "nomic-embed-text:latest", "model": "nomic-embed-text:latest"},
                {"name": "old:1b", "model": "old:1b"},
            ]})
        body = json.loads(request.content)
        if body["model"] == "qwen3:4b":
            return httpx.Response(200, json={"capabilities": ["completion", "tools", "thinking"],
                                             "model_info": {"qwen3.context_length": 40960}})
        if body["model"] == "nomic-embed-text:latest":
            return httpx.Response(200, json={"capabilities": ["embedding"]})
        return httpx.Response(200, json={})

    qwen, nomic, old = await _provider(handler).catalog("chat")
    assert qwen.id == "qwen3:4b"
    assert qwen.capabilities == {Capability.STRUCTURED, Capability.TOOLS, Capability.THINKING}
    assert qwen.context_length == 40960 and qwen.price_in_per_m == 0.0
    assert nomic.capabilities == {Capability.EMBEDDING}
    assert old.capabilities is None


def test_status_is_cached_and_reports_unreachable():
    calls = []
    now = [0.0]

    def handler(request):
        calls.append(request.url.path)
        raise httpx.ConnectError("refused", request=request)

    provider = _provider(handler, clock=lambda: now[0])
    first = provider.status()
    assert first.state == "unreachable" and first.locality == "local"
    assert first.detail == "Ollama is not reachable. Check OLLAMA_BASE_URL in the backend .env."
    assert BASE not in first.detail
    provider.status()
    assert calls == ["/api/version"]
    now[0] = 16.0
    provider.status()
    assert calls == ["/api/version", "/api/version"]


def test_status_ready_when_version_answers():
    provider = _provider(lambda request: httpx.Response(200, json={"version": "0.35.1"}))
    assert provider.status().state == "ready"


def test_chat_model_targets_the_configured_server():
    chat = _provider(lambda r: httpx.Response(200)).chat_model(
        "qwen3:4b", temperature=0.1, timeout_s=180, options={"think": False})
    assert chat.model == "qwen3:4b" and chat.base_url == BASE
    assert chat.temperature == 0.1 and chat.reasoning is False
    assert chat.client_kwargs == {"timeout": 180}
    unset = _provider(lambda r: httpx.Response(200)).chat_model(
        "qwen3:4b", temperature=None, timeout_s=10, options={})
    assert unset.reasoning is None


def test_chat_model_sets_the_configured_context_window():
    settings = Settings(_env_file=None, ollama_base_url=BASE, local_num_ctx=8192)
    chat = OllamaProvider(settings).chat_model("qwen3:4b", temperature=None, timeout_s=10, options={})
    assert chat.num_ctx == 8192
    default = _provider(lambda r: httpx.Response(200)).chat_model(
        "qwen3:4b", temperature=None, timeout_s=10, options={})
    assert default.num_ctx == 16384


async def test_embedder_uses_openai_compatible_endpoint_without_dimensions():
    seen = []

    def handler(request):
        seen.append(request)
        return httpx.Response(200, json={"data": [{"index": 0, "embedding": [0.5] + [0.0] * 767}],
                                         "usage": {"prompt_tokens": 3, "total_tokens": 3}})

    batch = await _provider(handler).embedder("nomic-embed-text", dimensions=768).embed(["سؤال"])
    assert batch.cost_usd == 0.0 and len(batch.vectors[0]) == 768
    assert str(seen[0].url) == f"{BASE}/v1/embeddings"
    assert "dimensions" not in json.loads(seen[0].content)


def test_registry_includes_ollama_and_its_errors():
    from ollama import ResponseError

    assert "ollama" in ProviderRegistry(Settings(_env_file=None)).names()
    assert ResponseError in provider_errors() and ConnectionError in provider_errors()
