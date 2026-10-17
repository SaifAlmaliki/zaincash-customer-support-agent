"""Deterministic embedding doubles; database behavior stays real in KB tests."""
import asyncio

from app.kb.contracts import EmbeddingBatch


class FakeEmbedder:
    model = "test/embedding"
    dimensions = 768

    async def embed(self, texts):
        vectors = tuple(
            tuple([1.0, 0.0] + [0.0] * 766)
            if "تحويل" in text else tuple([0.0, 1.0] + [0.0] * 766)
            for text in texts
        )
        return EmbeddingBatch(vectors)


class PaidEmbedder(FakeEmbedder):
    async def embed(self, texts):
        return EmbeddingBatch((await super().embed(texts)).vectors, 0.125)


class GatedEmbedder(PaidEmbedder):
    """Pause at the external provider boundary, optionally fail after release."""

    def __init__(self, *, error=None):
        self.entered = asyncio.Event()
        self.release = asyncio.Event()
        self.error = error

    async def embed(self, texts):
        self.entered.set()
        try:
            await self.release.wait()
        except asyncio.CancelledError as exc:
            exc.cost_usd = 0.125
            raise
        if self.error:
            raise self.error
        return await super().embed(texts)


class LateEmbedder(GatedEmbedder):
    """Simulate a provider that swallows cancellation and supplies a late success."""

    async def embed(self, texts):
        self.entered.set()
        try:
            await self.release.wait()
        except asyncio.CancelledError:
            pass
        return await PaidEmbedder.embed(self, texts)
