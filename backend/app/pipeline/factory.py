"""Wire settings and the active model snapshot into a compiled pipeline graph."""
from __future__ import annotations

from collections.abc import Callable
from functools import partial
from typing import Any

from langchain_core.language_models.chat_models import BaseChatModel

from app.config import Settings
from app.db.repository import SqlTransactionRepo
from app.kb.service import KnowledgeService
from app.llm import StructuredChatLLM, StructuredLLM
from app.models_config.resolver import ActiveModels
from app.models_config.types import Step
from app.pipeline.graph import MODES, PipelineDeps, build_graph
from app.pipeline.stage2_classify.jev import JevClassifier
from app.pipeline.stage3_extract.gemini import GeminiExtractor
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


def make_gemini_llm(settings: Settings) -> StructuredChatLLM:
    """The .env-configured extraction model (CLI and tests)."""
    return ActiveModels.from_env(settings).structured_llm()


def model_ids(settings: Settings) -> dict[str, str]:
    return ActiveModels.from_env(settings).model_ids()


def make_draft_model(settings: Settings) -> BaseChatModel:
    # The agent retries individual transient requests, inside its overall
    # deadline; providers must never retry on their own.
    models = ActiveModels.from_env(settings)
    return models.chat(Step.DRAFT, timeout_s=models.draft_info().timeout_s)


def build_pipeline(settings: Settings, mode: str, txn_repo: TransactionRepo, *,
                   models: ActiveModels | None = None,
                   jev_client: Any = None, llm: StructuredLLM | None = None,
                   drafter: Drafter | None = None,
                   model_factory: Callable[[], BaseChatModel] | None = None,
                   knowledge: KnowledgeService | None = None,
                   investigation: SqlInvestigationRepo | None = None,
                   credential_checker: CredentialChecker | None = None):
    """Build the Jev classifier and, for SQL repositories, an isolated bounded drafter.

    `models` is the snapshot for this run; omitted, the .env defaults apply.
    A supplied drafter wins. SQL defaults use the repository's public session
    factory; alternative repositories may opt into RAG by supplying BOTH adapters.
    A no-DB repository without both adapters stays classification-only.
    """
    if mode not in MODES:
        raise ConfigError(f"unknown mode {mode!r}; choose one of {MODES}")
    models = models or ActiveModels.from_env(settings)
    taxonomy = load_taxonomy(settings.taxonomy_path)
    if llm is None and models.ready(Step.EXTRACT):
        llm = models.structured_llm()
    if jev_client is None:
        if not models.ready(Step.CLASSIFY):
            raise ConfigError("TYPESAFE_API_KEY is required for Jev classification")
        jev_client = models.jev_client()
    jev_price = models.token_prices(Step.CLASSIFY)[0]
    jev = JevClassifier(
        jev_client, taxonomy, model_id=models.choice(Step.CLASSIFY).model, t_jev=settings.t_jev,
        min_top_prob=settings.jev_min_top_prob, price_in_per_m=jev_price,
        max_state_chars=settings.max_state_chars,
    )
    if drafter is None:
        database_backed = isinstance(txn_repo, SqlTransactionRepo)
        if not settings.rag_enabled:
            drafter = NullDrafter("rag_disabled")
        elif not database_backed and (knowledge is None or investigation is None):
            drafter = NullDrafter("no_database")
        elif not models.ready(Step.DRAFT):
            drafter = UnavailableDrafter()
        else:
            if knowledge is None:
                knowledge = KnowledgeService(txn_repo.session_factory, settings, models.embedder())
            if investigation is None:
                investigation = SqlInvestigationRepo(txn_repo.session_factory)
            if credential_checker is None:
                if models.ready(Step.CLASSIFY):
                    credential_checker = JevCredentialChecker(
                        jev_client, price_in_per_m=jev_price, model=models.choice(Step.CLASSIFY).model)
                else:
                    credential_checker = DegradedCredentialChecker()
            info = models.draft_info()
            drafter = RagDrafter(settings,
                                 model_factory=model_factory or partial(models.chat, Step.DRAFT,
                                                                        timeout_s=info.timeout_s),
                                 knowledge=knowledge, investigation=investigation,
                                 credential_checker=credential_checker, info=info)
    deps = PipelineDeps(
        taxonomy=taxonomy, txn_repo=txn_repo, jev=jev,
        gap_filler=GeminiExtractor(llm, max_state_chars=settings.max_state_chars) if llm else None,
        drafter=drafter,
    )
    return build_graph(deps)
