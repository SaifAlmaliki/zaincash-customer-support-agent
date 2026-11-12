from app.config import Settings
from app.models_config.embedder import ConfiguredEmbedder
from app.models_config.resolver import ActiveModels
from app.models_config.types import ModelChoice, Step
from tests.models_config_fakes import fake_registry


class _Store:
    def __init__(self, models):
        self.models = models

    def choice(self, step):
        return self.models.choice(step)

    def active(self):
        return self.models


async def test_configured_embedder_follows_the_current_setting():
    settings = Settings(_env_file=None, openrouter_api_key="k")
    registry = fake_registry(settings)
    store = _Store(ActiveModels(settings, {}, registry))
    embedder = ConfiguredEmbedder(store)
    assert embedder.model == "openai/text-embedding-3-small" and embedder.dimensions == 768
    store.models = ActiveModels(settings, {Step.EMBED: ModelChoice("ollama", "nomic-embed-text")}, registry)
    assert embedder.model == "nomic-embed-text"
    batch = await embedder.embed(["سؤال"])
    assert len(batch.vectors[0]) == 768
    assert registry.get("ollama").embedders[0].model == "nomic-embed-text"
