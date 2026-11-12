import pytest
from fastapi.testclient import TestClient
from sqlalchemy.engine import make_url

from app.config import Settings
from app.db.session import make_engine, make_sessionmaker, reset_db
from app.main import create_app
from app.models_config.types import Capability, CatalogEntry
from tests.models_config_fakes import FakeProvider, fake_registry
from tests.rag_fakes import ScriptedChat, answer, call

pytestmark = pytest.mark.integration
HEADERS = {"X-Admin-Token": "secret"}


def _tool_chat(model):
    return ScriptedChat(steps=[answer(call("record_number", number=7))])


@pytest.fixture
def make_client():
    engines = []

    def build(**settings_kw):
        settings = Settings(_env_file=None, **({"openrouter_api_key": "k", "typesafe_api_key": "t",
                                                "admin_token": "secret"} | settings_kw))
        assert make_url(settings.test_database_url).database == "support_test"
        engine = make_engine(settings.test_database_url)
        engines.append(engine)
        reset_db(engine)
        ollama = FakeProvider("ollama", locality="local", chat=_tool_chat, entries=[
            CatalogEntry("qwen3:4b", "qwen3:4b", frozenset({Capability.TOOLS, Capability.STRUCTURED})),
            CatalogEntry("nomic-embed-text", "nomic-embed-text", frozenset({Capability.EMBEDDING})),
        ])
        app = create_app(settings, session_factory=make_sessionmaker(engine),
                         model_registry=fake_registry(settings, ollama=ollama))
        return TestClient(app)

    yield build
    for engine in engines:
        engine.dispose()


def test_admin_is_disabled_without_a_token(make_client):
    with make_client(admin_token="") as client:
        response = client.get("/api/admin/models", headers=HEADERS)
        assert response.status_code == 403 and response.json()["detail"] == "admin_disabled"


def test_non_ascii_and_blank_tokens_are_rejected(make_client):
    with make_client() as client:
        assert client.post("/api/admin/session").status_code == 401
        assert client.post("/api/admin/session", headers={"X-Admin-Token": ""}).status_code == 401
        assert client.post("/api/admin/session", headers={"X-Admin-Token": "sécret".encode("latin-1")}).status_code == 401
        assert client.post("/api/admin/session", headers={"X-Admin-Token": "wrong"}).json()["detail"] == "invalid_admin_token"
        assert client.post("/api/admin/session", headers=HEADERS).status_code == 204


def test_models_and_catalog(make_client):
    with make_client() as client:
        steps = client.get("/api/admin/models", headers=HEADERS).json()["steps"]
        assert [item["step"] for item in steps] == ["intake", "classify", "extract", "draft", "embed"]
        assert all(item["source"] == "env" for item in steps)
        catalog = client.get("/api/admin/models/catalog?step=draft", headers=HEADERS).json()
        assert catalog["step"] == "draft"
        ollama = next(p for p in catalog["providers"] if p["provider"] == "ollama")
        assert [entry["id"] for entry in ollama["entries"]] == ["qwen3:4b"]
        assert client.get("/api/admin/models/catalog?step=bogus", headers=HEADERS).status_code == 422


def test_test_save_and_audit(make_client):
    with make_client() as client:
        body = {"provider": "ollama", "model": "qwen3:4b", "options": {"think": False}}
        result = client.post("/api/admin/models/test", headers=HEADERS, json={"step": "draft", **body}).json()
        assert result["ok"] is True and result["error"] is None
        saved = client.put("/api/admin/models/draft", headers=HEADERS, json={**body, "changed_by": "Sara"})
        assert saved.status_code == 200, saved.text
        assert saved.json()["source"] == "admin" and saved.json()["model"] == "qwen3:4b"
        assert client.get("/api/health").json()["ai"]["steps"]["draft"]["provider"] == "ollama"
        [entry] = client.get("/api/admin/models/audit", headers=HEADERS).json()["items"]
        assert entry["changed_by"] == "Sara" and entry["current"]["model"] == "qwen3:4b"


def test_save_rejections_change_nothing(make_client):
    with make_client() as client:
        failing = client.put("/api/admin/models/extract", headers=HEADERS,
                             json={"provider": "openrouter", "model": "m", "changed_by": "Sara"})
        assert failing.status_code == 422 and failing.json()["detail"].startswith("Model test failed:")
        wrong = client.put("/api/admin/models/classify", headers=HEADERS,
                           json={"provider": "ollama", "model": "qwen3:4b", "changed_by": "Sara"})
        assert wrong.status_code == 422
        embed = client.put("/api/admin/models/embed", headers=HEADERS,
                           json={"provider": "ollama", "model": "nomic-embed-text", "changed_by": "Sara"})
        assert embed.status_code == 400 and embed.json()["detail"] == "use_embedding_switch"
        extra = client.put("/api/admin/models/draft", headers=HEADERS,
                           json={"provider": "ollama", "model": "qwen3:4b", "changed_by": "Sara",
                                 "options": {"api_key": "x"}})
        assert extra.status_code == 422
        assert client.get("/api/admin/models/audit", headers=HEADERS).json()["items"] == []
