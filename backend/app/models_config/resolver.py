"""One immutable snapshot of the configured models; consumers build clients only through it."""
from __future__ import annotations

from collections.abc import Mapping
from typing import Any, Literal

from app.config import Settings
from app.models_config.pricing import prices_for
from app.models_config.providers.registry import ProviderRegistry
from app.models_config.steps import (
    DEFAULT_TEMPERATURE,
    EMBED_DIMENSIONS,
    draft_timeout_s,
    env_defaults,
)
from app.models_config.types import Locality, ModelChoice, ProviderStatus, Step
from app.pipeline.stage6_draft.model_info import DraftModelInfo

EXTRACT_TIMEOUT_S = 60.0


class ActiveModels:
    def __init__(self, settings: Settings, choices: Mapping[Step, ModelChoice],
                 registry: ProviderRegistry) -> None:
        self.settings = settings
        self.registry = registry
        self._choices: dict[Step, ModelChoice] = {**env_defaults(settings), **dict(choices)}

    @classmethod
    def from_env(cls, settings: Settings, registry: ProviderRegistry | None = None) -> ActiveModels:
        return cls(settings, {}, registry or ProviderRegistry(settings))

    def choice(self, step: Step) -> ModelChoice:
        return self._choices[step]

    def locality(self, step: Step) -> Locality:
        return self.registry.get(self.choice(step).provider).locality

    def is_local(self, step: Step) -> bool:
        return self.locality(step) == "local"

    def step_status(self, step: Step) -> ProviderStatus:
        """Provider status, downgraded when the chosen model has been removed from a ready provider."""
        choice = self.choice(step)
        status = self.registry.status(choice.provider)
        if status.state == "ready":
            has_model = getattr(self.registry.get(choice.provider), "has_model", None)
            if has_model is not None and has_model(choice.model) is False:
                return ProviderStatus(status.name, status.locality, "model_missing",
                                      "The model is not installed in Ollama.")
        return status

    def ready(self, step: Step) -> bool:
        return self.step_status(step).state == "ready"

    def overall_locality(self) -> Literal["local", "cloud", "mixed"]:
        values = {self.locality(step) for step in Step}
        return values.pop() if len(values) == 1 else "mixed"

    def temperature(self, step: Step) -> float | None:
        value = self.choice(step).options.get("temperature")
        return value if value is not None else DEFAULT_TEMPERATURE.get(step)

    def chat(self, step: Step, *, timeout_s: float):
        choice = self.choice(step)
        return self.registry.get(choice.provider).chat_model(
            choice.model, temperature=self.temperature(step), timeout_s=timeout_s, options=choice.options)

    def structured_llm(self, *, max_retries: int = 2):
        from app.llm import StructuredChatLLM

        choice = self.choice(Step.EXTRACT)
        provider = self.registry.get(choice.provider)
        timeout = self.settings.local_agent_timeout_s if provider.locality == "local" else EXTRACT_TIMEOUT_S
        override = choice.options.get("temperature")
        price_in, price_out = self.token_prices(Step.EXTRACT)

        def chat_factory(temperature: float):
            return provider.chat_model(choice.model, temperature=temperature if override is None else override,
                                       timeout_s=timeout, options=choice.options)

        return StructuredChatLLM(chat_factory=chat_factory, price_in_per_m=price_in,
                                 price_out_per_m=price_out, max_retries=max_retries)

    def embedder(self):
        choice = self.choice(Step.EMBED)
        return self.registry.get(choice.provider).embedder(choice.model, dimensions=EMBED_DIMENSIONS)

    def jev_client(self) -> Any:
        choice = self.choice(Step.CLASSIFY)
        return self.registry.get(choice.provider).classifier(choice.model)

    def prices(self, step: Step) -> tuple[float, float] | None:
        return prices_for(self.settings, step, self.choice(step), self.locality(step))

    def token_prices(self, step: Step) -> tuple[float, float]:
        return self.prices(step) or (0.0, 0.0)

    def draft_info(self) -> DraftModelInfo:
        return DraftModelInfo(model=self.choice(Step.DRAFT).model, token_prices=self.token_prices(Step.DRAFT),
                              timeout_s=draft_timeout_s(self.settings, self.locality(Step.DRAFT)),
                              embedding_model=self.choice(Step.EMBED).model,
                              provider=self.choice(Step.DRAFT).provider,
                              locality=self.locality(Step.DRAFT),
                              prices_known=self.prices(Step.DRAFT) is not None)

    def model_ids(self) -> dict[str, str]:
        return {step.value: self.choice(step).ref for step in Step}

    def summary(self) -> dict[str, Any]:
        steps = {}
        for step in Step:
            choice = self.choice(step)
            status = self.step_status(step)
            steps[step.value] = {"provider": choice.provider, "model": choice.model,
                                 "locality": status.locality, "status": status.state}
        return {"locality": self.overall_locality(), "steps": steps}
