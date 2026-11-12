"""What the drafting agent needs to know about its model, independent of the provider."""
from __future__ import annotations

from dataclasses import dataclass

from app.config import Settings


@dataclass(frozen=True)
class DraftModelInfo:
    model: str
    token_prices: tuple[float, float]
    timeout_s: float
    embedding_model: str

    @classmethod
    def from_settings(cls, settings: Settings) -> DraftModelInfo:
        return cls(settings.draft_model, settings.draft_token_prices, settings.agent_timeout_s,
                   settings.embedding_model)
