"""What each pipeline step needs, who may serve it, and today's .env defaults."""
from __future__ import annotations

from typing import Literal

from app.config import Settings
from app.models_config.types import Capability, CatalogKind, Locality, ModelChoice, Step

EMBED_DIMENSIONS = 768

REQUIREMENTS: dict[Step, frozenset[Capability]] = {
    Step.INTAKE: frozenset({Capability.STRUCTURED, Capability.VISION}),
    Step.CLASSIFY: frozenset({Capability.CLASSIFIER}),
    Step.EXTRACT: frozenset({Capability.STRUCTURED}),
    Step.DRAFT: frozenset({Capability.TOOLS}),
    Step.EMBED: frozenset({Capability.EMBEDDING}),
}

PROVIDERS_FOR_STEP: dict[Step, tuple[str, ...]] = {
    Step.INTAKE: ("openrouter", "ollama"),
    Step.CLASSIFY: ("typesafe",),
    Step.EXTRACT: ("openrouter", "ollama"),
    Step.DRAFT: ("openrouter", "ollama"),
    Step.EMBED: ("openrouter", "ollama"),
}

CATALOG_KIND: dict[Step, CatalogKind] = {
    Step.INTAKE: "chat", Step.CLASSIFY: "chat", Step.EXTRACT: "chat",
    Step.DRAFT: "chat", Step.EMBED: "embedding",
}

DEFAULT_TEMPERATURE: dict[Step, float] = {Step.EXTRACT: 0.0, Step.DRAFT: 0.1}


def env_defaults(settings: Settings) -> dict[Step, ModelChoice]:
    return {
        Step.INTAKE: ModelChoice("openrouter", settings.intake_model or settings.gemini_model),
        Step.CLASSIFY: ModelChoice("typesafe", settings.jev_model),
        Step.EXTRACT: ModelChoice("openrouter", settings.gemini_model),
        Step.DRAFT: ModelChoice("openrouter", settings.draft_model),
        Step.EMBED: ModelChoice("openrouter", settings.embedding_model),
    }


def eligibility(step: Step, capabilities: frozenset[Capability] | None
                ) -> Literal["eligible", "unknown", "ineligible"]:
    if capabilities is None:
        return "unknown"
    return "eligible" if REQUIREMENTS[step] <= capabilities else "ineligible"


def draft_timeout_s(settings: Settings, locality: Locality) -> float:
    return settings.local_agent_timeout_s if locality == "local" else settings.agent_timeout_s


def intake_timeout_s(settings: Settings, locality: Locality) -> float:
    return settings.local_intake_timeout_s if locality == "local" else settings.intake_timeout_s
