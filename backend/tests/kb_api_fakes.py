"""External provider doubles; storage, retrieval and indexing remain real."""
from threading import Event

from app.kb.contracts import EmbeddingBatch
from app.kb.embeddings import EmbeddingError


class Embeddings:
    model = "openai/text-embedding-3-small"
    dimensions = 768

    def __init__(self):
        self.calls = 0
        self.error = False
        self.started = Event()
        self.release = None

    async def embed(self, texts):
        import asyncio

        self.calls += 1
        self.started.set()
        if self.release is not None:
            try:
                await asyncio.to_thread(self.release.wait, 5)
            except asyncio.CancelledError as exc:
                exc.cost_usd = 0.02
                raise
        if self.error:
            raise EmbeddingError("Bearer test-router-secret test-jev-secret", cost_usd=0.02)
        return EmbeddingBatch(tuple((1.0,) + (0.0,) * 767 for _ in texts), 0.02)
