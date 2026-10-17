"""Injectable OpenRouter embeddings with validated, input-ordered immutable results."""
from __future__ import annotations

import asyncio
import math
from typing import Any

import httpx

from app.config import Settings
from app.kb.contracts import EmbeddingBatch

EMBEDDING_BATCH_SIZE = 32
EMBEDDING_TIMEOUT_S = 20.0
EMBEDDING_URL = "https://openrouter.ai/api/v1/embeddings"


class EmbeddingError(RuntimeError):
    """Safe public failure; cost_usd retains completed requests in this embed call."""

    def __init__(self, message: str, *, cost_usd: float = 0.0) -> None:
        super().__init__(message)
        self.cost_usd = cost_usd


def _nonnegative_number(value: Any) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise EmbeddingError("Embedding provider returned invalid usage or cost.")
    try:
        number = float(value)
    except OverflowError:
        raise EmbeddingError("Embedding provider returned invalid usage or cost.") from None
    if not math.isfinite(number) or number < 0:
        raise EmbeddingError("Embedding provider returned invalid usage or cost.")
    return number


def _response_cost(payload: dict, price_per_m: float) -> float:
    usage = payload.get("usage")
    if usage is None:
        usage = {}
    if not isinstance(usage, dict):
        raise EmbeddingError("Embedding provider returned invalid usage or cost.")
    # A reported zero is real, not a signal to use the fallback estimate.
    cost = usage.get("cost")
    if cost is None:
        cost = payload.get("cost")
    if cost is not None:
        return _nonnegative_number(cost)
    tokens = usage.get("prompt_tokens", usage.get("total_tokens", 0))
    if isinstance(tokens, bool) or not isinstance(tokens, int):
        raise EmbeddingError("Embedding provider returned invalid token usage.")
    # No token usage means no estimate; do not invent a tokenizer/character estimate.
    return _nonnegative_number(_nonnegative_number(tokens) / 1_000_000 * price_per_m)


def _ordered_vectors(payload: dict, count: int, dimensions: int) -> list[tuple[float, ...]]:
    data = payload.get("data")
    if not isinstance(data, list) or len(data) != count:
        raise EmbeddingError("Embedding provider returned a missing or unexpected vector count.")
    indexed: dict[int, tuple[float, ...]] = {}
    for item in data:
        if not isinstance(item, dict):
            raise EmbeddingError("Embedding provider returned an invalid embedding item.")
        index = item.get("index")
        if type(index) is not int or not 0 <= index < count or index in indexed:
            raise EmbeddingError("Embedding provider returned invalid or duplicate response indexes.")
        raw = item.get("embedding")
        if not isinstance(raw, list) or len(raw) != dimensions:
            raise EmbeddingError("Embedding provider returned a vector with invalid dimensions.")
        if any(isinstance(value, bool) or not isinstance(value, (int, float)) for value in raw):
            raise EmbeddingError("Embedding provider returned a nonnumeric vector.")
        try:
            vector = tuple(float(value) for value in raw)
        except OverflowError:
            raise EmbeddingError("Embedding provider returned a nonfinite vector.") from None
        if not all(math.isfinite(value) for value in vector):
            raise EmbeddingError("Embedding provider returned a nonfinite vector.")
        if not any(value != 0.0 for value in vector):
            raise EmbeddingError("Embedding provider returned a zero vector.")
        indexed[index] = vector
    return [indexed[index] for index in range(count)]


class OpenRouterEmbedder:
    """Implements Embedder; owns one context-managed HTTP client per embed call.

    A transport may be injected for offline tests. Requests are sequential, batched
    at 32 texts, have a 20s elapsed request deadline plus HTTP timeouts, and are
    never automatically retried. The request deadline includes the full body read.
    Caller cancellation propagates with this call's measured cost_usd attached to
    the original CancelledError. An outer asyncio.timeout retains it as the raised
    TimeoutError's __cause__. Consumers record that cost once on failure, instead
    of the EmbeddingBatch cost they would record on success.
    """

    def __init__(
        self, settings: Settings, *, transport: httpx.AsyncBaseTransport | None = None,
    ) -> None:
        self.model = settings.embedding_model
        self.dimensions = settings.embed_dim
        self._api_key = settings.openrouter_api_key
        self._price_per_m = settings.price_embedding_in
        self._transport = transport

    async def embed(self, texts: list[str]) -> EmbeddingBatch:
        if not texts:
            return EmbeddingBatch(())
        if any(not isinstance(text, str) or not text.strip() for text in texts):
            raise EmbeddingError("Embedding input must contain non-empty text strings.")
        vectors: list[tuple[float, ...]] = []
        cost_usd = 0.0
        try:
            async with httpx.AsyncClient(
                transport=self._transport, timeout=EMBEDDING_TIMEOUT_S,
                headers={"Authorization": f"Bearer {self._api_key}"},
            ) as client:
                for start in range(0, len(texts), EMBEDDING_BATCH_SIZE):
                    batch = texts[start:start + EMBEDDING_BATCH_SIZE]
                    payload = await self._request(client, batch)
                    cost_usd = _nonnegative_number(cost_usd + _response_cost(payload, self._price_per_m))
                    batch_vectors = _ordered_vectors(payload, len(batch), self.dimensions)
                    vectors.extend(batch_vectors)
        except (EmbeddingError, asyncio.CancelledError) as exc:
            # Include cancellation during client cleanup. Re-raise the same exception
            # so asyncio.timeout can still translate its own cancellation normally.
            exc.cost_usd = cost_usd
            raise
        return EmbeddingBatch(tuple(vectors), cost_usd)

    async def _request(self, client: httpx.AsyncClient, texts: list[str]) -> dict:
        try:
            async with asyncio.timeout(EMBEDDING_TIMEOUT_S):
                response = await client.post(EMBEDDING_URL, json={
                    "input": texts, "model": self.model,
                    "dimensions": self.dimensions, "encoding_format": "float",
                })
                response.raise_for_status()
        except (TimeoutError, httpx.TimeoutException):
            raise EmbeddingError("Embedding request timed out; please retry.") from None
        except httpx.HTTPStatusError as exc:
            raise EmbeddingError(
                f"Embedding provider request failed (HTTP {exc.response.status_code}); check provider availability and configuration."
            ) from None
        except httpx.RequestError:
            raise EmbeddingError("Embedding provider is unavailable; please retry.") from None
        try:
            payload = response.json()
        except ValueError:
            raise EmbeddingError("Embedding provider returned invalid JSON.") from None
        if not isinstance(payload, dict) or "error" in payload:
            raise EmbeddingError("Embedding provider returned an invalid response.")
        return payload
