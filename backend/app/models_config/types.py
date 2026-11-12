"""Provider-neutral values shared by the store, the resolver, probes and the admin API."""
from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum
from typing import Any, Literal

Locality = Literal["local", "cloud"]
ProviderState = Literal["ready", "missing_key", "unreachable", "model_missing"]
CatalogKind = Literal["chat", "embedding"]


class Step(StrEnum):
    INTAKE = "intake"
    CLASSIFY = "classify"
    EXTRACT = "extract"
    DRAFT = "draft"
    EMBED = "embed"


class Capability(StrEnum):
    STRUCTURED = "structured_output"
    TOOLS = "tools"
    VISION = "vision"
    EMBEDDING = "embedding"
    THINKING = "thinking"
    CLASSIFIER = "classifier"


@dataclass(frozen=True)
class ModelChoice:
    provider: str
    model: str
    options: dict[str, Any] = field(default_factory=dict)

    @property
    def ref(self) -> str:
        return f"{self.provider}:{self.model}"

    def to_json(self) -> dict[str, Any]:
        return {"provider": self.provider, "model": self.model, "options": dict(self.options)}

    @classmethod
    def from_json(cls, value: Any) -> ModelChoice:
        if not isinstance(value, dict):
            raise ValueError("A model choice must be an object.")
        provider, model = value.get("provider"), value.get("model")
        options = value.get("options") if value.get("options") is not None else {}
        if not isinstance(provider, str) or not provider.strip():
            raise ValueError("A model choice needs a provider.")
        if not isinstance(model, str) or not model.strip():
            raise ValueError("A model choice needs a model ID.")
        if not isinstance(options, dict):
            raise ValueError("Model options must be an object.")
        return cls(provider.strip(), model.strip(), dict(options))


@dataclass(frozen=True)
class CatalogEntry:
    id: str
    name: str
    capabilities: frozenset[Capability] | None  # None: the provider did not report them
    price_in_per_m: float | None = None
    price_out_per_m: float | None = None
    context_length: int | None = None

    def to_json(self) -> dict[str, Any]:
        return {
            "id": self.id, "name": self.name,
            "capabilities": None if self.capabilities is None else sorted(c.value for c in self.capabilities),
            "price_in_per_m": self.price_in_per_m, "price_out_per_m": self.price_out_per_m,
            "context_length": self.context_length,
        }


@dataclass(frozen=True)
class ProviderStatus:
    name: str
    locality: Locality
    state: ProviderState
    detail: str | None = None


@dataclass(frozen=True)
class ProbeResult:
    ok: bool
    latency_ms: int
    error: str | None = None

    def to_json(self) -> dict[str, Any]:
        return {"ok": self.ok, "latency_ms": self.latency_ms, "error": self.error}
