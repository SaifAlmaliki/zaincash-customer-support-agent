import httpx
import pytest

from app.kb.embeddings import EmbeddingError, OpenAICompatibleEmbedder
from app.telemetry.calls import call_context


def transport(payload, status=200):
    def handler(request):
        return httpx.Response(status, json=payload)
    return httpx.MockTransport(handler)


def vector():
    return [1.0] + [0.0] * 767


def embedder(payload, **kw):
    return OpenAICompatibleEmbedder(model="openai/text-embedding-3-small", dimensions=768,
                                    url="https://x/embeddings", price_per_m=0.02,
                                    transport=transport(payload), **kw)


async def test_draft_search_embedding_is_recorded_with_tokens_and_estimate():
    payload = {"data": [{"index": 0, "embedding": vector()}], "usage": {"prompt_tokens": 50}}
    with call_context(run_id=1, ticket_id=1) as calls:
        batch = await embedder(payload).embed(["سياسة"])
    [row] = calls.calls
    assert (row.process, row.input_tokens, row.cost_source) == ("draft_search", 50, "estimate")
    assert row.cost_usd == pytest.approx(batch.cost_usd)


async def test_indexing_and_provider_cost():
    payload = {"data": [{"index": 0, "embedding": vector()}], "usage": {"prompt_tokens": 50, "cost": 0.001}}
    with call_context(document_id=4) as calls:
        await embedder(payload).embed(["نص"])
    assert (calls.calls[0].process, calls.calls[0].cost_source) == ("kb_index", "provider")


async def test_local_embedder_and_failures():
    payload = {"data": [{"index": 0, "embedding": vector()}]}
    with call_context() as calls:
        await embedder(payload, provider="ollama", local=True).embed(["نص"])
        with pytest.raises(EmbeddingError):
            await OpenAICompatibleEmbedder(model="m", dimensions=768, url="https://x/e",
                                           transport=transport({}, status=500)).embed(["نص"])
    assert (calls.calls[0].process, calls.calls[0].cost_source, calls.calls[0].locality) == (
        "kb_search", "local", "local")
    assert calls.calls[1].status == "error"


@pytest.mark.integration
def test_knowledge_search_api_persists_kb_search(monkeypatch):
    from fastapi.testclient import TestClient
    from sqlalchemy import select

    from app.config import Settings
    from app.db.session import make_engine, make_sessionmaker, reset_db
    from app.main import create_app
    from app.telemetry.calls import AiCall, Timer, record
    from app.telemetry.db_models import AiCallRow

    settings = Settings(_env_file=None, openrouter_api_key="k", typesafe_api_key="")
    engine = make_engine(settings.test_database_url)
    reset_db(engine)
    sf = make_sessionmaker(engine)
    with TestClient(create_app(settings, session_factory=sf)) as client:
        async def fake_search(query, *, category=None, k=5):
            timer = Timer()
            record(AiCall("kb_search", "openrouter", "m", "cloud", timer.started_at, 1, cost_usd=0.001,
                          cost_source="provider"))
            from app.kb.contracts import SearchResult
            return SearchResult(passages=(), cost_usd=0.001)

        monkeypatch.setattr(client.app.state.knowledge, "search", fake_search)
        monkeypatch.setattr("app.api.knowledge._require_provider", lambda request: None)
        assert client.post("/api/knowledge/search", json={"query": "سياسة"}).status_code == 200
    with sf() as session:
        assert [r.process for r in session.scalars(select(AiCallRow))] == ["kb_search"]
    engine.dispose()
