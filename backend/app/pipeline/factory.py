"""Wire settings into a compiled pipeline graph. This is the only place that builds real model clients."""
from __future__ import annotations

from typing import Any

from app.config import Settings
from app.llm import GeminiStructuredLLM, StructuredLLM
from app.pipeline.graph import MODES, PipelineDeps, build_graph
from app.pipeline.stage2_classify.gemini import GeminiClassifier, GeminiExtractor
from app.pipeline.stage2_classify.jev import JevClassifier
from app.pipeline.stage4_lookup.lookup import TransactionRepo
from app.pipeline.stage6_draft.drafting import Drafter, NullDrafter
from app.taxonomy import load_taxonomy


class ConfigError(RuntimeError):
    """Missing or invalid configuration (for example, an API key)."""


def make_jev_client(settings: Settings) -> Any:
    from langchain_typesafe import TypeSafeClassifier

    return TypeSafeClassifier(model=settings.jev_model, api_key=settings.typesafe_api_key)


def make_gemini_llm(settings: Settings) -> GeminiStructuredLLM:
    return GeminiStructuredLLM(
        api_key=settings.google_api_key, model=settings.gemini_model,
        price_in_per_m=settings.price_gemini_flash_in, price_out_per_m=settings.price_gemini_flash_out,
    )


def model_ids(settings: Settings, mode: str) -> dict[str, str]:
    ids = {"jev": settings.jev_model} if mode != "gemini" else {}
    return ids | {"gemini": settings.gemini_model}


def build_pipeline(settings: Settings, mode: str, txn_repo: TransactionRepo, *,
                   jev_client: Any = None, llm: StructuredLLM | None = None,
                   drafter: Drafter | None = None):
    if mode not in MODES:
        raise ConfigError(f"unknown mode {mode!r}; choose one of {MODES}")
    taxonomy = load_taxonomy(settings.taxonomy_path)
    if llm is None and settings.google_api_key:
        llm = make_gemini_llm(settings)
    if mode in ("gemini", "cascade") and llm is None:
        raise ConfigError(f"GOOGLE_API_KEY is required for mode={mode}")
    if mode in ("jev", "cascade") and jev_client is None:
        if not settings.typesafe_api_key:
            raise ConfigError(f"TYPESAFE_API_KEY is required for mode={mode}")
        jev_client = make_jev_client(settings)
    jev = None
    if mode != "gemini":
        jev = JevClassifier(
            jev_client, taxonomy, model_id=settings.jev_model, t_jev=settings.t_jev,
            min_top_prob=settings.jev_min_top_prob, price_in_per_m=settings.price_jev_in,
            max_state_chars=settings.max_state_chars,
        )
    gemini = None
    if mode != "jev" and llm is not None:
        gemini = GeminiClassifier(llm, taxonomy, t_gem=settings.t_gem,
                                  max_state_chars=settings.max_state_chars)
    deps = PipelineDeps(
        mode=mode, taxonomy=taxonomy, txn_repo=txn_repo, jev=jev, gemini=gemini,
        gap_filler=GeminiExtractor(llm, max_state_chars=settings.max_state_chars) if llm else None,
        drafter=drafter or NullDrafter(), t_gem=settings.t_gem,
    )
    return build_graph(deps)
