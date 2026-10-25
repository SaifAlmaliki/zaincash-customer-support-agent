"""Wire settings into a compiled pipeline graph. This is the only place that builds real model clients."""
from __future__ import annotations

from collections.abc import Callable
from functools import partial
from typing import Any

from langchain_core.language_models.chat_models import BaseChatModel

from app.config import Settings
from app.db.repository import SqlTransactionRepo
from app.kb.embeddings import OpenRouterEmbedder
from app.kb.service import KnowledgeService
from app.llm import GeminiStructuredLLM, StructuredLLM
from app.pipeline.graph import MODES, PipelineDeps, build_graph
from app.pipeline.stage2_classify.gemini import GeminiClassifier, GeminiExtractor
from app.pipeline.stage2_classify.jev import JevClassifier
from app.pipeline.stage4_lookup.lookup import TransactionRepo
from app.pipeline.stage6_draft.agent import RagDrafter
from app.pipeline.stage6_draft.credentials import (
    CredentialChecker,
    DegradedCredentialChecker,
    JevCredentialChecker,
)
from app.pipeline.stage6_draft.drafting import Drafter, NullDrafter, UnavailableDrafter
from app.pipeline.stage6_draft.investigation import SqlInvestigationRepo
from app.taxonomy import load_taxonomy


class ConfigError(RuntimeError):
    """Missing or invalid configuration (for example, an API key)."""


def make_jev_client(settings: Settings) -> Any:
    from langchain_typesafe import TypeSafeClassifier

    return TypeSafeClassifier(model=settings.jev_model, api_key=settings.typesafe_api_key)


def make_gemini_llm(settings: Settings) -> GeminiStructuredLLM:
    return GeminiStructuredLLM(
        api_key=settings.openrouter_api_key, model=settings.gemini_model,
        price_in_per_m=settings.price_gemini_flash_in, price_out_per_m=settings.price_gemini_flash_out,
    )


def model_ids(settings: Settings, mode: str) -> dict[str, str]:
    ids = {"jev": settings.jev_model} if mode != "gemini" else {}
    return ids | {"gemini": settings.gemini_model, "drafting": settings.draft_model,
                  "embedding": settings.embedding_model}


def make_draft_model(settings: Settings) -> BaseChatModel:
    from app.pipeline.stage6_draft.model import DraftChatOpenRouter

    # Same provider conventions as llm.py. The agent retries individual transient
    # requests, inside its overall deadline; the SDK must never retry on its own.
    return DraftChatOpenRouter(model=settings.draft_model, temperature=0.1,
                               api_key=settings.openrouter_api_key,
                               timeout=int(settings.agent_timeout_s * 1000), max_retries=0,
                               model_kwargs={"retries": None})


def build_pipeline(settings: Settings, mode: str, txn_repo: TransactionRepo, *,
                   jev_client: Any = None, llm: StructuredLLM | None = None,
                   drafter: Drafter | None = None,
                   model_factory: Callable[[], BaseChatModel] | None = None,
                   knowledge: KnowledgeService | None = None,
                   investigation: SqlInvestigationRepo | None = None,
                   credential_checker: CredentialChecker | None = None):
    """Build classifiers and, for SQL repositories, an isolated bounded drafter.

    A supplied drafter wins. SQL defaults use the repository's public session
    factory; alternative repositories may opt into RAG by supplying BOTH adapters.
    A no-DB repository without both adapters stays classification-only.
    """
    if mode not in MODES:
        raise ConfigError(f"unknown mode {mode!r}; choose one of {MODES}")
    taxonomy = load_taxonomy(settings.taxonomy_path)
    if llm is None and settings.openrouter_api_key:
        llm = make_gemini_llm(settings)
    if mode in ("gemini", "cascade") and llm is None:
        raise ConfigError(f"OPENROUTER_API_KEY is required for mode={mode}")
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
    if drafter is None:
        database_backed = isinstance(txn_repo, SqlTransactionRepo)
        if not settings.rag_enabled:
            drafter = NullDrafter("rag_disabled")
        elif not database_backed and (knowledge is None or investigation is None):
            drafter = NullDrafter("no_database")
        elif not settings.openrouter_api_key:
            drafter = UnavailableDrafter()
        else:
            if knowledge is None:
                knowledge = KnowledgeService(txn_repo.session_factory, settings, OpenRouterEmbedder(settings))
            if investigation is None:
                investigation = SqlInvestigationRepo(txn_repo.session_factory)
            if credential_checker is None:
                if settings.typesafe_api_key:
                    credential_checker = JevCredentialChecker(
                        jev_client if jev_client is not None else make_jev_client(settings),
                        price_in_per_m=settings.price_jev_in)
                else:
                    credential_checker = DegradedCredentialChecker()
            drafter = RagDrafter(settings, model_factory=model_factory or partial(make_draft_model, settings),
                                 knowledge=knowledge, investigation=investigation,
                                 credential_checker=credential_checker)
    deps = PipelineDeps(
        mode=mode, taxonomy=taxonomy, txn_repo=txn_repo, jev=jev, gemini=gemini,
        gap_filler=GeminiExtractor(llm, max_state_chars=settings.max_state_chars) if llm else None,
        drafter=drafter, t_gem=settings.t_gem,
    )
    return build_graph(deps)
