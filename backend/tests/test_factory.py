import pytest

from app.config import Settings
from app.pipeline.factory import ConfigError, build_pipeline, model_ids
from app.pipeline.stage4_lookup.lookup import InMemoryTransactionRepo
from tests.fakes import FakeJevRunnable, FakeStructuredLLM

REPO = InMemoryTransactionRepo([])


def _settings(**kw):
    return Settings(_env_file=None, **({"openrouter_api_key": "", "typesafe_api_key": ""} | kw))


def test_missing_keys_raise_config_error():
    with pytest.raises(ConfigError, match="OPENROUTER_API_KEY"):
        build_pipeline(_settings(), "gemini", REPO)
    with pytest.raises(ConfigError):
        build_pipeline(_settings(), "jev", REPO)


def test_builds_with_injected_clients():
    for mode in ("jev", "gemini", "cascade"):
        graph = build_pipeline(_settings(), mode, REPO, jev_client=FakeJevRunnable(),
                               llm=FakeStructuredLLM([None]))
        assert "prepare" in graph.get_graph().nodes


def test_model_ids():
    s = _settings()
    rag = {"drafting": "google/gemini-3.8-flash", "embedding": "openai/text-embedding-3-small"}
    assert model_ids(s, "jev") == {"jev": "jev-1.13.0", "gemini": "google/gemini-3.8-flash", **rag}
    assert model_ids(s, "gemini") == {"gemini": "google/gemini-3.8-flash", **rag}
    claude = _settings(anthropic_model="anthropic/claude-sonnet-5.5")
    assert model_ids(claude, "cascade")["drafting"] == "anthropic/claude-sonnet-5.5"
    assert model_ids(claude, "cascade")["gemini"] == "google/gemini-3.8-flash"


def test_openrouter_key_enables_gemini_pipeline():
    graph = build_pipeline(_settings(openrouter_api_key="test-openrouter-key"), "gemini", REPO)
    assert "gemini_classify" in graph.get_graph().nodes


@pytest.mark.parametrize("mode", ["jev", "gemini", "cascade"])
@pytest.mark.parametrize("key", ["typesafe-test-key", ""])
async def test_all_modes_use_credential_checker_independently_of_classifier(mode, key):
    from sqlalchemy.orm import sessionmaker

    from app.db.repository import SqlTransactionRepo
    from app.pipeline.graph import run_batch
    from app.pipeline.stage2_classify.gemini import GeminiAnalysis
    from tests.rag_fakes import REPLY, Knowledge, ScriptedChat, draft_state, script

    model = ScriptedChat(steps=script())
    graph = build_pipeline(_settings(openrouter_api_key="test-key", typesafe_api_key=key), mode,
                           SqlTransactionRepo(sessionmaker()),
                           jev_client=FakeJevRunnable(category="general_inquiry", flags={"requests_credentials": 0.2}),
                           llm=FakeStructuredLLM([GeminiAnalysis(category="general_inquiry", priority="P4")]),
                           model_factory=lambda: model, knowledge=Knowledge(), investigation=object())
    [outcome], summary = await run_batch(graph, [draft_state()["ticket"]], concurrency=1)
    assert outcome.draft.text == REPLY
    assert ("draft_failed_guardrail" in outcome.decision.reasons) is bool(key)
    assert summary.degraded is (not bool(key))
    assert ("requests_credentials" in outcome.decision.note) is bool(key)
    assert ("Credential check degraded" in outcome.decision.note) is (not bool(key))


@pytest.mark.parametrize("mode", ["jev", "gemini", "cascade"])
@pytest.mark.parametrize("inject_model", [False, True])
async def test_missing_rag_key_escalates_but_retains_classification(mode, inject_model):
    from sqlalchemy.orm import sessionmaker

    from app.db.repository import SqlTransactionRepo
    from app.pipeline.graph import run_batch
    from app.pipeline.stage2_classify.gemini import GeminiAnalysis
    from tests.rag_fakes import ScriptedChat, draft_state, script

    graph = build_pipeline(_settings(), mode, SqlTransactionRepo(sessionmaker()),
                           jev_client=FakeJevRunnable(category="general_inquiry"),
                           llm=FakeStructuredLLM([GeminiAnalysis(category="general_inquiry", priority="P4")]),
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


async def test_gemini_mode_builds_real_jev_checker_when_only_key_is_supplied(monkeypatch):
    from app.pipeline import factory
    from app.pipeline.graph import run_batch
    from app.pipeline.stage2_classify.gemini import GeminiAnalysis
    from tests.rag_fakes import Knowledge, ScriptedChat, draft_state, script

    monkeypatch.setattr(factory, "make_jev_client", lambda settings: FakeJevRunnable(flags={"requests_credentials": 0.9}))
    graph = build_pipeline(_settings(openrouter_api_key="test", typesafe_api_key="test"), "gemini", REPO,
                           llm=FakeStructuredLLM([GeminiAnalysis(category="general_inquiry", priority="P4")]),
                           knowledge=Knowledge(), investigation=object(), model_factory=lambda: ScriptedChat(steps=script()))
    [outcome], summary = await run_batch(graph, [draft_state()["ticket"]], concurrency=1)
    assert outcome.decision.reasons == ("draft_failed_guardrail",)
    assert "requests_credentials" in outcome.decision.note and not summary.degraded


async def test_sql_defaults_retrieve_real_indexed_evidence(monkeypatch):
    import json

    from sqlalchemy import text
    from sqlalchemy.engine import make_url

    from app.db.repository import SqlTransactionRepo
    from app.db.session import make_engine, make_sessionmaker, reset_db
    from app.kb.documents import store_document
    from app.kb.service import KnowledgeService
    from app.pipeline import factory
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
        monkeypatch.setattr(factory, "OpenRouterEmbedder", lambda settings: PaidEmbedder())

        async def submit(messages):
            [source] = json.loads(messages[-1].content)
            return answer(call("submit_draft", reply_ar=REPLY, citations=[source["id"]]), id="submit")

        model = ScriptedChat(steps=[answer(call("search_knowledge_base", query="سياسة الدعم"), id="search"), submit])
        graph = build_pipeline(settings, "jev", SqlTransactionRepo(sf),
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
