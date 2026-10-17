from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol


@dataclass(frozen=True)
class TextChunk:
    index: int
    text: str
    page_start: int | None = None
    page_end: int | None = None


@dataclass(frozen=True)
class EmbeddingBatch:
    vectors: tuple[tuple[float, ...], ...]
    cost_usd: float = 0.0


@dataclass(frozen=True)
class Passage:
    id: str
    document_id: int
    chunk_index: int
    text: str
    filename: str
    score: float
    page_start: int | None = None
    page_end: int | None = None


@dataclass(frozen=True)
class SearchResult:
    passages: tuple[Passage, ...]
    cost_usd: float = 0.0


class Embedder(Protocol):
    model: str
    dimensions: int

    async def embed(self, texts: list[str]) -> EmbeddingBatch: ...
