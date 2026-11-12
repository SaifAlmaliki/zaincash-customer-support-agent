import httpx

from app.config import Settings
from app.models_config.catalog import CatalogCache, step_catalog
from app.models_config.types import Capability, CatalogEntry, Step
from tests.models_config_fakes import FakeProvider, fake_registry

TOOLS = CatalogEntry("qwen3:4b", "qwen3:4b", frozenset({Capability.TOOLS, Capability.STRUCTURED}))
PLAIN = CatalogEntry("plain", "plain", frozenset({Capability.STRUCTURED}))
UNKNOWN = CatalogEntry("mystery", "mystery", None)


async def test_step_catalog_filters_and_marks_unknown():
    registry = fake_registry(Settings(_env_file=None),
                             ollama=FakeProvider("ollama", locality="local", entries=[TOOLS, PLAIN, UNKNOWN]),
                             openrouter=FakeProvider("openrouter", state="missing_key"))
    openrouter, ollama = await step_catalog(Step.DRAFT, registry, CatalogCache(registry))
    assert openrouter["status"] == "missing_key" and openrouter["entries"] == []
    assert [(e["id"], e["eligibility"]) for e in ollama["entries"]] == [("mystery", "unknown"), ("qwen3:4b", "eligible")]


async def test_catalog_errors_stay_per_provider_and_cache_respects_ttl():
    now = [0.0]
    ollama = FakeProvider("ollama", locality="local", entries=[TOOLS])
    registry = fake_registry(Settings(_env_file=None), ollama=ollama,
                             openrouter=FakeProvider("openrouter", catalog_error=httpx.ConnectError("down")))
    cache = CatalogCache(registry, ttl_s=300, clock=lambda: now[0])
    openrouter, local = await step_catalog(Step.DRAFT, registry, cache)
    assert openrouter["error"] == "Could not list models: ConnectError" and local["entries"]
    await step_catalog(Step.DRAFT, registry, cache)
    assert ollama.catalog_calls == 1
    await step_catalog(Step.DRAFT, registry, cache, refresh=True)
    now[0] = 301
    await step_catalog(Step.DRAFT, registry, cache)
    assert ollama.catalog_calls == 3


async def test_classify_catalog_only_offers_typesafe():
    registry = fake_registry(Settings(_env_file=None))
    [only] = await step_catalog(Step.CLASSIFY, registry, CatalogCache(registry))
    assert only["provider"] == "typesafe"
