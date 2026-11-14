"""Per-1M token prices used for cost estimates. Unknown models have no price (spec §4.5)."""
from __future__ import annotations

from collections.abc import Iterable
from dataclasses import replace

from app.config import Settings
from app.models_config.types import CatalogEntry, ModelChoice, Step
from app.telemetry.calls import money

PRICE_KEYS = ("price_in_per_m", "price_out_per_m")


def prices_for(settings: Settings, step: Step, choice: ModelChoice,
               locality: str) -> tuple[float, float] | None:
    if locality == "local":
        return 0.0, 0.0
    saved_in = money(choice.options.get("price_in_per_m"))
    if saved_in is not None:
        return saved_in, money(choice.options.get("price_out_per_m")) or 0.0
    model = choice.model
    if step is Step.CLASSIFY:
        return settings.price_jev_in, 0.0
    if step is Step.EMBED:
        return (settings.price_embedding_in, 0.0) if model == settings.embedding_model else None
    if step is Step.DRAFT and model == settings.draft_model:
        return settings.draft_token_prices
    if model.startswith("anthropic/"):
        return settings.price_anthropic_in, settings.price_anthropic_out
    if model == settings.gemini_model:
        return settings.price_gemini_flash_in, settings.price_gemini_flash_out
    return None


def with_catalog_prices(choice: ModelChoice, entries: Iterable[CatalogEntry]) -> ModelChoice:
    entry = next((e for e in entries if e.id == choice.model), None)
    if entry is None or entry.price_in_per_m is None:
        return choice
    options = {**choice.options, "price_in_per_m": entry.price_in_per_m,
               "price_out_per_m": entry.price_out_per_m or 0.0}
    return replace(choice, options=options)
