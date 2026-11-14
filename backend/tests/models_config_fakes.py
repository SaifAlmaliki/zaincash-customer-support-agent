"""Provider doubles: real store/resolver logic, scripted provider boundaries."""
from __future__ import annotations

from app.kb.contracts import EmbeddingBatch
from app.kb.embeddings import EmbeddingError
from app.models_config.providers.registry import ProviderRegistry
from app.models_config.types import ProviderStatus
from tests.fakes import FakeJevRunnable


class NamedEmbedder:
    dimensions = 768

    def __init__(self, model, *, fail_for=()):
        self.model, self.fail_for, self.calls = model, tuple(fail_for), []

    async def embed(self, texts):
        self.calls.append(list(texts))
        if any(marker in text for text in texts for marker in self.fail_for):
            raise EmbeddingError("Fake embedding failure.")
        return EmbeddingBatch(tuple(tuple([1.0] + [0.0] * 767) for _ in texts))


class FakeProvider:
    def __init__(self, name, *, locality="cloud", state="ready", chat=None, entries=(),
                 catalog_error=None, classifier=None, embed_fail_for=(), installed=None):
        self.name, self.locality, self.state = name, locality, state
        if installed is not None:
            self.has_model = lambda model: model in installed
        self.chat, self.entries, self.catalog_error = chat, list(entries), catalog_error
        self.classifier_obj, self.embed_fail_for = classifier, embed_fail_for
        self.chat_calls, self.catalog_calls, self.embedders = [], 0, []

    def status(self):
        return ProviderStatus(self.name, self.locality, self.state)

    async def catalog(self, kind):
        self.catalog_calls += 1
        if self.catalog_error is not None:
            raise self.catalog_error
        return list(self.entries)

    def chat_model(self, model, *, temperature, timeout_s, options):
        self.chat_calls.append({"model": model, "temperature": temperature,
                                "timeout_s": timeout_s, "options": dict(options)})
        if self.chat is None:
            raise AssertionError(f"{self.name} chat was not expected")
        return self.chat(model) if callable(self.chat) else self.chat

    def embedder(self, model, *, dimensions, price_per_m=None):
        embedder = NamedEmbedder(model, fail_for=self.embed_fail_for)
        embedder.price_per_m = price_per_m
        self.embedders.append(embedder)
        return embedder

    def classifier(self, model):
        return self.classifier_obj or FakeJevRunnable(model=model)


def fake_registry(settings, **providers):
    defaults = {
        "openrouter": FakeProvider("openrouter"),
        "ollama": FakeProvider("ollama", locality="local"),
        "typesafe": FakeProvider("typesafe"),
    }
    return ProviderRegistry(settings, providers=defaults | providers)
