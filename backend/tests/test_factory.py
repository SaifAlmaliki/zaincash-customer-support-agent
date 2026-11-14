import pytest

from app.config import Settings
from app.pipeline.factory import ConfigError, build_pipeline, model_ids
from app.pipeline.stage4_lookup.lookup import InMemoryTransactionRepo
from tests.fakes import FakeJevRunnable, FakeStructuredLLM

REPO = InMemoryTransactionRepo([])


def _settings(**kw):
    return Settings(_env_file=None, **({"openrouter_api_key": "", "typesafe_api_key": ""} | kw))


def test_missing_jev_key_raises_config_error():
    with pytest.raises(ConfigError, match="TYPESAFE_API_KEY"):
        build_pipeline(_settings(), "jev", REPO)


def test_builds_jev_pipeline_with_injected_clients():
    graph = build_pipeline(_settings(), "jev", REPO, jev_client=FakeJevRunnable(),
                           llm=FakeStructuredLLM([None]))
    assert "prepare" in graph.get_graph().nodes
    assert "gemini_classify" not in graph.get_graph().nodes


def test_model_ids():
    assert model_ids(_settings()) == {
        "intake": "openrouter:google/gemini-3.8-flash", "classify": "typesafe:jev-1.13.0",
        "extract": "openrouter:google/gemini-3.8-flash", "draft": "openrouter:google/gemini-3.8-flash",
        "embed": "openrouter:openai/text-embedding-3-small",
    }
    claude = model_ids(_settings(anthropic_model="anthropic/claude-sonnet-5.5"))
    assert claude["draft"] == "openrouter:anthropic/claude-sonnet-5.5"
    assert claude["extract"] == "openrouter:google/gemini-3.8-flash"


@pytest.mark.parametrize("mode", ["gemini", "cascade"])
def test_retired_classification_modes_are_rejected(mode):
    with pytest.raises(ConfigError, match="unknown mode"):
        build_pipeline(_settings(openrouter_api_key="test-openrouter-key"), mode, REPO,
                       jev_client=FakeJevRunnable(), llm=FakeStructuredLLM([None]))


@pytest.mark.parametrize("key", ["typesafe-test-key", ""])
async def test_credential_checker_is_independent_of_jev_classification(key):
    from sqlalchemy.orm import sessionmaker

    from app.db.repository import SqlTransactionRepo
    from app.pipeline.graph import run_batch
    from tests.rag_fakes import REPLY, Knowledge, ScriptedChat, draft_state, script

    model = ScriptedChat(steps=script())
    graph = build_pipeline(_settings(openrouter_api_key="test-key", typesafe_api_key=key), "jev",
                           SqlTransactionRepo(sessionmaker()),
                           jev_client=FakeJevRunnable(category="general_inquiry", flags={"requests_credentials": 0.2}),
                           llm=FakeStructuredLLM([None]),
                           model_factory=lambda: model, knowledge=Knowledge(), investigation=object())
    [outcome], summary = await run_batch(graph, [draft_state()["ticket"]], concurrency=1)
    assert outcome.draft.text == REPLY
    assert ("draft_failed_guardrail" in outcome.decision.reasons) is bool(key)
    assert summary.degraded is (not bool(key))
    assert ("requests_credentials" in outcome.decision.note) is bool(key)
    assert ("Credential check degraded" in outcome.decision.note) is (not bool(key))


@pytest.mark.parametrize("inject_model", [False, True])
async def test_missing_rag_key_escalates_but_retains_classification(inject_model):
    from sqlalchemy.orm import sessionmaker

    from app.db.repository import SqlTransactionRepo
    from app.pipeline.graph import run_batch
    from tests.rag_fakes import ScriptedChat, draft_state, script

    graph = build_pipeline(_settings(), "jev", SqlTransactionRepo(sessionmaker()),
                           jev_client=FakeJevRunnable(category="general_inquiry"),
                           llm=FakeStructuredLLM([None]),
                           model_factory=(lambda: ScriptedChat(steps=script())) if inject_model else None)
    [outcome], _ = await run_batch(graph, [draft_state()["ticket"]], concurrency=1)
    assert outcome.status == "escalated" and outcome.classifier.classification.category == "general_inquiry"
    assert outcome.decision.reasons == ("llm_unavailable",)
    assert outcome.draft.trace[-1]["status"] == "unavailable"


@pytest.mark.parametrize("disabled, database, expected", [(True, True, "rag_disabled"),
                                                         (False, False, "no_database")])
async def test_opt_out_and_no_database_record_skipped_trace(disabled, database, expected):
    from sqlalchemy.orm import sessionmaker

    from app.db.repository import SqlTransactionRepo
    from app.pipeline.graph import run_batch
    from tests.rag_fakes import draft_state

    repo = SqlTransactionRepo(sessionmaker()) if database else REPO
    graph = build_pipeline(_settings(rag_enabled=not disabled), "jev", repo,
                           jev_client=FakeJevRunnable(category="general_inquiry"))
    [outcome], _ = await run_batch(graph, [draft_state()["ticket"]], concurrency=1)
    assert outcome.draft.trace == ({"kind": "skipped", "stage": "draft", "reason": expected},)
    assert outcome.status == "pending_review"


async def test_explicit_even_falsy_drafter_wins_over_default_wiring():
    from app.pipeline.contracts import DraftResult
    from app.pipeline.graph import run_batch
    from tests.rag_fakes import draft_state

    class Injected:
        def __bool__(self):
            return False

        async def draft(self, state):
            return DraftResult(text="رد مخصص")

    graph = build_pipeline(_settings(), "jev", REPO,
                           jev_client=FakeJevRunnable(category="general_inquiry"), drafter=Injected())
    [outcome], _ = await run_batch(graph, [draft_state()["ticket"]], concurrency=1)
    assert outcome.draft.text == "رد مخصص"


async def test_jev_mode_builds_real_jev_checker_from_the_classify_provider():
    from app.models_config.resolver import ActiveModels
    from app.pipeline.graph import run_batch
    from tests.models_config_fakes import FakeProvider, fake_registry
    from tests.rag_fakes import Knowledge, ScriptedChat, draft_state, script

    settings = _settings(openrouter_api_key="test", typesafe_api_key="test")
    typesafe = FakeProvider("typesafe", classifier=FakeJevRunnable(
        category="general_inquiry", flags={"requests_credentials": 0.9}))
    models = ActiveModels(settings, {}, fake_registry(settings, typesafe=typesafe))
    graph = build_pipeline(settings, "jev", REPO, models=models, llm=FakeStructuredLLM([None]),
                           knowledge=Knowledge(), investigation=object(),
                           model_factory=lambda: ScriptedChat(steps=script()))
    [outcome], summary = await run_batch(graph, [draft_state()["ticket"]], concurrency=1)
    assert outcome.decision.reasons == ("draft_failed_guardrail",)
    assert "requests_credentials" in outcome.decision.note and not summary.degraded


async def test_sql_defaults_retrieve_real_indexed_evidence():
    import json

    from sqlalchemy import text
    from sqlalchemy.engine import make_url

    from app.db.repository import SqlTransactionRepo
    from app.db.session import make_engine, make_sessionmaker, reset_db
    from app.kb.documents import store_document
    from app.kb.service import KnowledgeService
    from app.pipeline.graph import run_batch
    from tests.kb_fakes import PaidEmbedder
    from tests.rag_fakes import REPLY, ScriptedChat, answer, call, draft_state

    settings = _settings(openrouter_api_key="test", embedding_model=PaidEmbedder.model)
    assert make_url(settings.test_database_url).database == "support_test"
    engine = make_engine(settings.test_database_url)
    try:
        with engine.connect() as connection:
            assert connection.scalar(text("SELECT current_database()")) == "support_test"
        reset_db(engine)
        sf = make_sessionmaker(engine)
        with sf.begin() as session:
            document = store_document(session, "policy.md", "نراجع طلب العميل ولا نطلب أسراره.".encode())
            document_id = document.id
        await KnowledgeService(sf, settings, PaidEmbedder()).index_document(document_id)

        async def submit(messages):
            [source] = json.loads(messages[-1].content)
            return answer(call("submit_draft", reply_ar=REPLY, citations=[source["id"]]), id="submit")

        model = ScriptedChat(steps=[answer(call("search_knowledge_base", query="سياسة الدعم"), id="search"), submit])
        from app.models_config.resolver import ActiveModels
        from tests.models_config_fakes import FakeProvider, fake_registry

        class PaidProvider(FakeProvider):
            def embedder(self, model, *, dimensions, price_per_m=None):
                return PaidEmbedder()

        models = ActiveModels(settings, {}, fake_registry(settings, openrouter=PaidProvider("openrouter")))
        graph = build_pipeline(settings, "jev", SqlTransactionRepo(sf), models=models,
                               jev_client=FakeJevRunnable(category="general_inquiry"),
                               model_factory=lambda: model)
        [outcome], _ = await run_batch(graph, [draft_state()["ticket"]], concurrency=1)
        assert outcome.status == "pending_review", outcome.error
        assert outcome.draft.text == REPLY
        source = outcome.draft.trace[-1]["citation_sources"][0]
        assert source["document_id"] == document_id and source["filename"] == "policy.md"
        assert outcome.draft.citations == (source["id"],)
    finally:
        engine.dispose()


async def test_local_draft_model_is_built_by_its_provider_with_local_timeout():
    from app.models_config.resolver import ActiveModels
    from app.models_config.types import ModelChoice, Step
    from app.pipeline.graph import run_batch
    from tests.models_config_fakes import FakeProvider, fake_registry
    from tests.rag_fakes import REPLY, Knowledge, ScriptedChat, draft_state, script

    settings = _settings(typesafe_api_key="t", local_agent_timeout_s=200)
    ollama = FakeProvider("ollama", locality="local", chat=ScriptedChat(steps=script()))
    models = ActiveModels(settings, {Step.DRAFT: ModelChoice("ollama", "qwen3:4b")},
                          fake_registry(settings, ollama=ollama))
    graph = build_pipeline(settings, "jev", REPO, models=models,
                           jev_client=FakeJevRunnable(category="general_inquiry"),
                           llm=FakeStructuredLLM([None]), knowledge=Knowledge(), investigation=object())
    [outcome], _ = await run_batch(graph, [draft_state()["ticket"]], concurrency=1)
    assert outcome.draft.text == REPLY
    assert ollama.chat_calls[0]["model"] == "qwen3:4b" and ollama.chat_calls[0]["timeout_s"] == 200
    assert outcome.draft.trace[-1]["model"] == "qwen3:4b"


async def test_unreachable_local_draft_provider_never_falls_back_to_cloud():
    from app.models_config.resolver import ActiveModels
    from app.models_config.types import ModelChoice, Step
    from app.pipeline.graph import run_batch
    from tests.models_config_fakes import FakeProvider, fake_registry
    from tests.rag_fakes import Knowledge, draft_state

    settings = _settings(openrouter_api_key="k", typesafe_api_key="t")
    openrouter = FakeProvider("openrouter")  # chat=None: any chat call fails the test
    registry = fake_registry(settings, openrouter=openrouter,
                             ollama=FakeProvider("ollama", locality="local", state="unreachable"))
    models = ActiveModels(settings, {Step.DRAFT: ModelChoice("ollama", "qwen3:4b")}, registry)
    graph = build_pipeline(settings, "jev", REPO, models=models,
                           jev_client=FakeJevRunnable(category="general_inquiry"),
                           llm=FakeStructuredLLM([None]), knowledge=Knowledge(), investigation=object())
    [outcome], _ = await run_batch(graph, [draft_state()["ticket"]], concurrency=1)
    assert outcome.decision.reasons == ("llm_unavailable",)
    assert openrouter.chat_calls == []
