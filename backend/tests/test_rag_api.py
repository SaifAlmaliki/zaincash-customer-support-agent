"""Real HTTP/pgvector lifecycle with fake external providers only."""
import asyncio
import json
from concurrent.futures import ThreadPoolExecutor
from threading import Event

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import select
from sqlalchemy.engine import make_url

from app.config import Settings
from app.db.document_models import UploadedDocument
from app.db.session import make_engine, make_sessionmaker, reset_db
from app.kb.documents import store_document
from app.kb.models import KnowledgeDocumentIndex
from app.kb.service import KnowledgeService
from app.main import create_app
from tests.kb_api_fakes import Embeddings

pytestmark = pytest.mark.integration


@pytest.fixture
def kb_env():
    settings = Settings(_env_file=None, openrouter_api_key="test-router-secret",
                        typesafe_api_key="test-jev-secret")
    assert make_url(settings.test_database_url).database == "support_test"
    engine = make_engine(settings.test_database_url)
    reset_db(engine)
    sf = make_sessionmaker(engine)
    embedder = Embeddings()
    service = KnowledgeService(sf, settings, embedder)
    yield settings, sf, embedder, service
    engine.dispose()


@pytest.fixture
def client(kb_env):
    settings, sf, _, service = kb_env
    with TestClient(create_app(settings, session_factory=sf,
                               knowledge_builder=lambda sf, settings: service)) as client:
        yield client


def upload(client, text=b"# Policy\nContact support.", name="policy.md"):
    response = client.post("/api/knowledge", files={"file": (name, text)})
    assert response.status_code == 200, response.text
    return response.json()


def test_upload_commits_then_indexes_duplicate_does_not_reembed(client, kb_env):
    first = upload(client)
    indexed = client.get("/api/knowledge").json()[0]
    assert indexed["status"] == "indexed"
    assert indexed["chunk_count"] == 1 and indexed["cost_usd"] == pytest.approx(0.02)
    assert indexed["embedding_dimensions"] == 768
    duplicate = upload(client, name="duplicate.md")
    assert duplicate["id"] == first["id"] and duplicate["filename"] == "policy.md"
    assert kb_env[2].calls == 1
    assert client.get(f"/api/knowledge/{first['id']}/download").content == b"# Policy\nContact support."


def test_explicit_retry_tags_search_and_chunk_pagination(client, kb_env):
    doc = upload(client, b"policy " * 500)
    url = f"/api/knowledge/{doc['id']}"
    response = client.post(url + "/index", json={"category_tags": ["general_inquiry"]})
    assert response.status_code == 202, response.text
    page = client.get(url + "/chunks?offset=1&limit=1").json()
    assert page["total"] > 1 and len(page["items"]) == 1
    assert page["items"][0]["chunk_index"] == 1
    assert page["items"][0]["category_tags"] == ["general_inquiry"]
    assert "embedding" not in page["items"][0]
    result = client.post("/api/knowledge/search", json={"query": "policy", "category": "general_inquiry", "k": 1})
    assert result.status_code == 200, result.text
    assert len(result.json()["passages"]) == 1
    assert result.json()["passages"][0]["document_id"] == doc["id"]
    assert result.json()["cost_usd"] == pytest.approx(0.02)
    excluded = client.post("/api/knowledge/search", json={"query": "policy", "category": "failed_transfer"})
    assert excluded.status_code == 200, excluded.text
    assert excluded.json()["passages"] == []
    assert client.get(url + "/chunks?limit=101").status_code == 422
    assert client.get(url + "/chunks?offset=-1").status_code == 422
    assert client.get(url + "/chunks?offset=999").json()["items"] == []


@pytest.mark.parametrize("payload", [
    {"query": " "}, {"query": "x" * 2001}, {"query": "x", "category": "unknown"},
    {"query": "x", "k": 0}, {"query": "x", "k": 11}, {"query": "x", "k": True},
    {"query": "x", "k": "5"}, {"query": "x", "k": 1.5},
])
def test_search_rejects_invalid_input_before_provider(client, kb_env, payload):
    assert client.post("/api/knowledge/search", json=payload).status_code == 422
    assert kb_env[2].calls == 0


def test_safe_failure_retry_and_missing_documents(client, kb_env):
    kb_env[2].error = True
    doc = upload(client)
    failed = client.get("/api/knowledge").json()[0]
    assert failed["status"] == "failed" and failed["error"]
    assert failed["cost_usd"] == pytest.approx(0.02)
    search = client.post("/api/knowledge/search", json={"query": "policy"})
    assert search.status_code == 503
    assert "test-router-secret" not in search.text + str(failed)
    assert "test-jev-secret" not in search.text + str(failed)
    kb_env[2].error = False
    url = f"/api/knowledge/{doc['id']}/index"
    assert client.post(url, json={"category_tags": ["invalid"]}).status_code == 422
    assert client.post(url).status_code == 202
    indexed = client.get("/api/knowledge").json()[0]
    assert indexed["status"] == "indexed" and indexed["error"] is None
    assert indexed["cost_usd"] == pytest.approx(0.04)
    assert client.post("/api/knowledge/99999/index").status_code == 404
    assert client.get("/api/knowledge/99999/chunks").status_code == 404


@pytest.mark.parametrize("enabled,key,state", [(False, "test-router-secret", "disabled"), (True, "", "unconfigured")])
def test_disabled_or_missing_provider_stores_without_indexing(kb_env, enabled, key, state):
    settings, sf, embeddings, service = kb_env
    settings = settings.model_copy(update={"rag_enabled": enabled, "openrouter_api_key": key})
    with TestClient(create_app(settings, session_factory=sf, knowledge_builder=lambda sf, settings: service)) as client:
        doc = upload(client)
        assert client.get("/api/knowledge").json()[0]["status"] == "awaiting_indexing"
        assert client.post(f"/api/knowledge/{doc['id']}/index").status_code == 503
        assert client.post("/api/knowledge/search", json={"query": "policy"}).status_code == 503
        health = client.get("/api/health").json()
        assert health["knowledge"]["status"] == state
        assert health["knowledge"]["ready"] is False
        assert embeddings.calls == 0


def test_health_requires_compatible_nonempty_index(client, kb_env):
    health = client.get("/api/health")
    assert "test-router-secret" not in health.text and "test-jev-secret" not in health.text
    assert health.json()["knowledge"]["configured"] is True
    assert health.json()["knowledge"]["ready"] is False
    assert health.json()["knowledge"]["indexed_document_count"] == 0
    doc = upload(client)
    health = client.get("/api/health").json()
    assert health["knowledge"]["ready"] is True and health["capabilities"]["drafting"] is True
    assert health["knowledge"]["indexed_document_count"] == 1
    with kb_env[1].begin() as session:
        session.get(KnowledgeDocumentIndex, doc["id"]).embedding_model = "incompatible"
    assert client.get("/api/health").json()["knowledge"]["ready"] is False


def test_concurrent_index_requests_share_active_work(client, kb_env):
    doc = upload(client)
    embedder = kb_env[2]
    embedder.started.clear()
    embedder.release = Event()
    url = f"/api/knowledge/{doc['id']}/index"
    with ThreadPoolExecutor() as pool:
        first = pool.submit(client.post, url)
        try:
            assert embedder.started.wait(5)
            duplicate = client.post(url)
            assert duplicate.status_code == 202
            assert duplicate.json()["status"] == "indexing"
            assert client.get("/api/knowledge").json()[0]["status"] == "indexing"
        finally:
            embedder.release.set()
        assert first.result().status_code == 202
    assert embedder.calls == 2
    assert client.get("/api/knowledge").json()[0]["cost_usd"] == pytest.approx(0.04)


def test_startup_recovers_even_with_injected_sessions(kb_env):
    settings, sf, embeddings, service = kb_env
    with sf.begin() as session:
        document = store_document(session, "old.md", b"old policy")
        document_id = document.id
    asyncio.run(service.index_document(document_id))
    with sf.begin() as session:
        session.get(KnowledgeDocumentIndex, document_id).status = "indexing"
    with TestClient(create_app(settings, session_factory=sf, knowledge_builder=lambda sf, settings: service)) as client:
        recovered = client.get("/api/knowledge").json()[0]
        assert recovered["status"] == "failed" and "restart" in recovered["error"]
        assert recovered["cost_usd"] == pytest.approx(0.02)
    assert embeddings.calls == 1
    with sf() as session:
        assert session.scalar(select(UploadedDocument.id)) == document_id


@pytest.fixture
def evidence_client(kb_env, request):
    from langchain_core.messages import ToolMessage

    from app.pipeline.factory import build_pipeline
    from tests.fakes import FakeJevRunnable, FakeStructuredLLM
    from tests.rag_fakes import REPLY, Checker, ScriptedChat, answer, call

    async def submit(messages):
        passages = json.loads(next(m.content for m in reversed(messages) if isinstance(m, ToolMessage)))
        return answer(call("submit_draft", reply_ar=REPLY, citations=[passages[0]["id"]],
                           internal_note="Review the cited policy only."), id="submit")

    def pipeline(settings, mode, repo, *, knowledge):
        return build_pipeline(
            settings, mode, repo, knowledge=knowledge,
            jev_client=FakeJevRunnable(category="general_inquiry"), llm=FakeStructuredLLM([{}]),
            model_factory=lambda: ScriptedChat(steps=[
                answer(call("search_knowledge_base", query="policy"), id="search"), submit,
            ]), credential_checker=Checker(getattr(request, "param", None),
                                           degraded=not hasattr(request, "param")),
        )

    settings, sf, _, service = kb_env
    with TestClient(create_app(settings, session_factory=sf, pipeline_builder=pipeline,
                               knowledge_builder=lambda sf, settings: service)) as client:
        upload(client, "سياسة الدعم: راجع طلب العميل ولا تطلب أسراره.".encode(), "one.md")
        upload(client, "سياسة ثانية: انتظر مراجعة فريق الدعم.".encode(), "two.md")
        response = client.post("/api/runs", json={"mode": "jev", "tickets": [
            {"external_id": "evidence", "text": "شلون أطلب مساعدة؟"},
        ]})
        assert response.status_code == 202, response.text
        result_id = client.get("/api/results").json()["items"][0]["id"]
        yield client, result_id


def test_persisted_actual_trace_projects_only_citations_after_reindex_and_delete(evidence_client, kb_env):
    client, result_id = evidence_client
    url = f"/api/results/{result_id}"
    detail = client.get(url).json()
    assert detail["draft_text"] and len(detail["citations"]) == 1
    retrieved = next(e["retrieved_passages"] for e in detail["agent_trace"] if e.get("retrieved_passages"))
    assert len(retrieved) == 2
    assert detail["citation_sources"] == [p for p in retrieved if p["id"] in detail["citations"]]
    assert detail["guardrail_findings"] == []
    assert detail["credential_check_degraded"] is True
    assert detail["requests_credentials"] is None
    assert detail["internal_note"] == "Review the cited policy only."
    before = detail["citation_sources"]
    # Reindex and delete the live documents, then read evidence from a new request/session.
    for document in client.get("/api/knowledge").json():
        assert client.post(f"/api/knowledge/{document['id']}/index").status_code == 202
        assert client.delete(f"/api/knowledge/{document['id']}").status_code == 204
    assert client.get(url).json()["citation_sources"] == before
    assert client.get("/api/knowledge").json() == []
    assert client.get("/api/health").json()["knowledge"]["ready"] is False


def test_malformed_entries_do_not_destroy_valid_persisted_evidence(evidence_client, kb_env):
    from app.db.models import TicketResultRow

    client, result_id = evidence_client
    original = client.get(f"/api/results/{result_id}").json()
    with kb_env[1].begin() as session:
        result = session.get(TicketResultRow, result_id)
        result.agent_trace = [None, "old", 4, {"retrieved_passages": "broken"}] + result.agent_trace + [
            {"kind": "tool", "retrieved_passages": [None, {"id": result.citations[0], "text": "broken"}]},
            {"kind": "guardrail", "findings": "wrong", "credential_check_degraded": "false"},
            {"kind": "draft", "internal_note": 99, "citation_sources": [{"id": []}]},
        ]
    detail = client.get(f"/api/results/{result_id}").json()
    assert detail["citation_sources"] == original["citation_sources"]
    assert detail["credential_check_degraded"] is True
    assert detail["internal_note"] == "Review the cited policy only."


@pytest.mark.parametrize("trace", [None, {}, "legacy", [None, {"kind": "stage", "node": "draft"}],
                                       [{"kind": "guardrail", "findings": [3], "requests_credentials": "bad"}]])
def test_old_or_invalid_traces_have_safe_unknown_defaults(evidence_client, kb_env, trace):
    from app.db.models import TicketResultRow

    client, result_id = evidence_client
    with kb_env[1].begin() as session:
        session.get(TicketResultRow, result_id).agent_trace = trace
    detail = client.get(f"/api/results/{result_id}").json()
    assert detail["citation_sources"] == []
    assert detail["guardrail_findings"] == []
    assert detail["credential_check_degraded"] is None
    assert detail["requests_credentials"] is None and detail["internal_note"] is None


@pytest.mark.parametrize("evidence_client", [0.8], indirect=True)
def test_actual_guardrail_failure_is_separate_from_reply(evidence_client):
    client, result_id = evidence_client
    detail = client.get(f"/api/results/{result_id}").json()
    assert detail["guardrail_findings"] == ["requests_credentials"]
    assert detail["credential_check_degraded"] is False
    assert detail["requests_credentials"] == 0.8
    assert "draft_failed_guardrail" in detail["escalation_reasons"]
    assert detail["draft_text"] and detail["citation_sources"]


def test_health_distinguishes_failed_from_empty(client, kb_env):
    kb_env[2].error = True
    upload(client)
    state = client.get("/api/health").json()["knowledge"]
    assert state["configured"] is True and state["ready"] is False
    assert state["status"] == "failed"


def test_index_background_admission_is_bounded_and_releases_capacity(client, kb_env):
    docs = [upload(client, f"policy {i}".encode()) for i in range(4)]
    embedder = kb_env[2]
    embedder.release = Event()
    with ThreadPoolExecutor(max_workers=4) as pool:
        pending = []
        try:
            for doc in docs:
                embedder.started.clear()
                pending.append(pool.submit(client.post, f"/api/knowledge/{doc['id']}/index"))
                assert embedder.started.wait(5)
            extra = upload(client, b"extra policy")
            assert extra["index_requested"] is False
            url = f"/api/knowledge/{extra['id']}/index"
            assert client.post(url).status_code == 503
            assert client.get("/api/health").json()["knowledge"]["status"] == "indexing"
        finally:
            embedder.release.set()
        assert all(task.result().status_code == 202 for task in pending)
    assert client.post(url).status_code == 202
    assert embedder.calls == 9


def test_index_deadline_persists_failure_and_retry_releases_slot(client, kb_env, monkeypatch):
    from app.kb import service as service_module

    monkeypatch.setattr(service_module, "INDEXING_TIMEOUT_S", 0.1)
    embedder = kb_env[2]
    embedder.release = Event()
    try:
        document = upload(client)
        row = client.get("/api/knowledge").json()[0]
        assert row["status"] == "failed" and "timed out" in row["error"]
        assert row["cost_usd"] == pytest.approx(0.02)
    finally:
        embedder.release.set()
    monkeypatch.setattr(service_module, "INDEXING_TIMEOUT_S", 120)
    assert client.post(f"/api/knowledge/{document['id']}/index").status_code == 202
    assert client.get("/api/knowledge").json()[0]["cost_usd"] == pytest.approx(0.04)


@pytest.mark.parametrize("name,content", [("bad.pdf", b"not pdf"), ("bad.txt", b"\xff"),
                                           ("bad.md", b""), ("bad.exe", b"x")])
def test_upload_validation_uses_shared_rules(client, kb_env, name, content):
    assert client.post("/api/knowledge", files={"file": (name, content)}).status_code == 422
    assert client.get("/api/knowledge").json() == []
    assert kb_env[2].calls == 0
