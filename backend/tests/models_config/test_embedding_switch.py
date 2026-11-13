from datetime import UTC, datetime

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import select
from sqlalchemy.engine import make_url

from app.config import Settings
from app.db.models import RunRow
from app.db.session import make_engine, make_sessionmaker, reset_db
from app.kb.documents import store_document
from app.kb.models import KnowledgeChunk
from app.main import create_app
from app.models_config.db_models import EmbeddingSwitchRow
from app.models_config.types import ModelChoice, Step
from tests.models_config_fakes import FakeProvider, fake_registry

pytestmark = pytest.mark.integration
HEADERS = {"X-Admin-Token": "secret"}
SWITCH = {"provider": "ollama", "model": "nomic-embed-text", "changed_by": "Sara"}


@pytest.fixture
def env():
    settings = Settings(_env_file=None, openrouter_api_key="k", typesafe_api_key="t", admin_token="secret")
    assert make_url(settings.test_database_url).database == "support_test"
    engine = make_engine(settings.test_database_url)
    reset_db(engine)
    sf = make_sessionmaker(engine)
    yield settings, sf
    engine.dispose()


def _client(settings, sf, **providers):
    return TestClient(create_app(settings, session_factory=sf, model_registry=fake_registry(settings, **providers)))


def _documents(sf, *texts):
    with sf.begin() as session:
        return [store_document(session, f"doc-{i}.md", text.encode()).id for i, text in enumerate(texts)]


def test_switch_reindexes_every_document_with_the_new_model(env):
    settings, sf = env
    ids = _documents(sf, "# Policy A\nسياسة أولى", "# Policy B\nسياسة ثانية")
    with _client(settings, sf) as client:
        response = client.post("/api/admin/models/embed/switch", headers=HEADERS, json=SWITCH)
        assert response.status_code == 202, response.text
        view = client.get("/api/admin/models/embed/switch", headers=HEADERS).json()
        assert view["status"] == "completed" and view["total"] == 2 and view["done"] == 2
        assert view["previous"]["model"] == "openai/text-embedding-3-small"
        assert client.get("/api/health").json()["knowledge"]["embedding_model"] == "nomic-embed-text"
    with sf() as session:
        models = set(session.scalars(select(KnowledgeChunk.embedding_model).where(KnowledgeChunk.document_id.in_(ids))))
    assert models == {"nomic-embed-text"}


def test_failed_documents_are_listed(env):
    settings, sf = env
    good, bad = _documents(sf, "# Good\nسياسة", "# Bad\nFAILME")
    ollama = FakeProvider("ollama", locality="local", embed_fail_for=("FAILME",))
    with _client(settings, sf, ollama=ollama) as client:
        client.post("/api/admin/models/embed/switch", headers=HEADERS, json=SWITCH)
        view = client.get("/api/admin/models/embed/switch", headers=HEADERS).json()
    assert view["status"] == "completed_with_errors" and view["failed_document_ids"] == [bad]


def test_switch_with_no_documents_completes_immediately(env):
    with _client(*env) as client:
        client.post("/api/admin/models/embed/switch", headers=HEADERS, json=SWITCH)
        view = client.get("/api/admin/models/embed/switch", headers=HEADERS).json()
    assert view["status"] == "completed" and view["total"] == 0


def test_start_updates_the_cache_without_reloading_from_the_database(env, monkeypatch):
    settings, sf = env
    with _client(settings, sf) as client:
        store = client.app.state.model_store

        def broken_load():
            raise RuntimeError("database went away after the commit")

        monkeypatch.setattr(store, "load", broken_load)
        target = ModelChoice("ollama", "nomic-embed-text")
        view = client.app.state.embedding_switches.start(target, changed_by="Sara", latency_ms=5)
        assert view["status"] == "running"
        assert store.choice(Step.EMBED) == target
        entry = next(item for item in store.describe() if item["step"] == "embed")
        assert entry["source"] == "admin" and entry["updated_by"] == "Sara"


def test_run_start_locks_the_switch_table_before_its_first_write(env):
    from sqlalchemy import event

    settings, sf = env
    statements = []
    engine = sf.kw["bind"]

    @event.listens_for(engine, "before_cursor_execute")
    def record(conn, cursor, statement, parameters, context, executemany):
        statements.append(statement.strip().split("\n")[0])

    with _client(settings, sf) as client:
        statements.clear()
        response = client.post("/api/runs", json={"tickets": [
            {"external_id": "x", "text": "شكد العمولة", "customer_phone": "07701234567"}]})
        assert response.status_code == 202, response.text
    lock = next(i for i, sql in enumerate(statements) if sql.startswith("LOCK TABLE embedding_switch IN SHARE MODE"))
    first_write = next(i for i, sql in enumerate(statements) if sql.startswith(("INSERT", "UPDATE")))
    assert lock < first_write


def test_switch_is_refused_while_a_run_is_running(env):
    settings, sf = env
    with _client(settings, sf) as client:
        with sf.begin() as session:
            session.add(RunRow(mode="jev", prompt_version="v", model_ids={}, status="running", counts={}))
        response = client.post("/api/admin/models/embed/switch", headers=HEADERS, json=SWITCH)
        assert response.status_code == 409 and response.json()["detail"] == "run_in_progress"
        assert client.get("/api/admin/models/embed/switch", headers=HEADERS).json() is None


def test_runs_are_blocked_while_a_switch_runs_and_restart_recovers(env):
    settings, sf = env
    with sf.begin() as session:
        session.add(EmbeddingSwitchRow(target={"provider": "ollama", "model": "n", "options": {}},
                                       previous={"provider": "openrouter", "model": "o", "options": {}},
                                       status="running", total=1, done=0, failed_document_ids=[],
                                       started_by="Sara", started_at=datetime.now(UTC)))
    app = create_app(settings, session_factory=sf, model_registry=fake_registry(settings))
    app.state.recover_embedding_switches = False  # keep the row running for the first assertion
    with TestClient(app) as client:
        blocked = client.post("/api/runs", json={"tickets": [
            {"external_id": "x", "text": "شكد العمولة", "customer_phone": "07701234567"}]})
        assert blocked.status_code == 409 and blocked.json()["detail"] == "knowledge_switch_in_progress"
    with TestClient(create_app(settings, session_factory=sf, model_registry=fake_registry(settings))) as client:
        view = client.get("/api/admin/models/embed/switch", headers=HEADERS).json()
        assert view["status"] == "failed" and "restarted" in view["error"]
