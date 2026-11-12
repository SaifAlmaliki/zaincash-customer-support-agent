import uuid
from datetime import UTC, datetime

import pytest
from sqlalchemy.engine import make_url

from app.config import Settings
from app.db.session import make_engine, make_sessionmaker, reset_db
from app.intake.db_models import IntakeSessionRow
from app.models_config.db_models import ModelSettingRow
from app.models_config.store import ModelSettingsStore
from app.models_config.types import ModelChoice, Step
from tests.models_config_fakes import FakeProvider, fake_registry

pytestmark = pytest.mark.integration


@pytest.fixture
def env():
    settings = Settings(_env_file=None, openrouter_api_key="k", typesafe_api_key="t",
                        local_intake_timeout_s=150)
    assert make_url(settings.test_database_url).database == "support_test"
    engine = make_engine(settings.test_database_url)
    reset_db(engine)
    yield settings, make_sessionmaker(engine)
    engine.dispose()


def _store(settings, sf):
    store = ModelSettingsStore(sf, settings, fake_registry(settings))
    store.load()
    return store


def test_empty_store_uses_env_defaults(env):
    store = _store(*env)
    assert store.choice(Step.DRAFT) == ModelChoice("openrouter", "google/gemini-3.8-flash")
    draft = next(item for item in store.describe() if item["step"] == "draft")
    assert draft["source"] == "env" and draft["updated_by"] is None
    assert draft["requirements"] == ["tools"] and draft["providers"] == ["openrouter", "ollama"]


def test_save_updates_cache_database_and_audit(env):
    settings, sf = env
    store = _store(settings, sf)
    choice = ModelChoice("ollama", "qwen3:4b", {"think": False})
    store.save(Step.DRAFT, choice, changed_by="Sara", latency_ms=1200)
    assert store.choice(Step.DRAFT) == choice
    assert _store(settings, sf).choice(Step.DRAFT) == choice
    [entry] = store.audit()
    assert entry["step"] == "draft" and entry["changed_by"] == "Sara"
    assert entry["previous"]["model"] == "google/gemini-3.8-flash"
    assert entry["current"] == choice.to_json() and entry["test_latency_ms"] == 1200
    draft = next(item for item in store.describe() if item["step"] == "draft")
    assert draft["source"] == "admin" and draft["locality"] == "local" and draft["updated_by"] == "Sara"


def test_describe_reports_a_saved_model_that_is_no_longer_installed(env):
    settings, sf = env
    ollama = FakeProvider("ollama", locality="local", installed={"present:1b"})
    store = ModelSettingsStore(sf, settings, fake_registry(settings, ollama=ollama))
    store.load()
    store.save(Step.DRAFT, ModelChoice("ollama", "gone:1b"), changed_by="Sara", latency_ms=1)
    store.save(Step.EXTRACT, ModelChoice("ollama", "present:1b"), changed_by="Sara", latency_ms=1)
    steps = {item["step"]: item for item in store.describe()}
    assert steps["draft"]["status"] == "model_missing"
    assert steps["draft"]["status_detail"] == "The model is not installed in Ollama."
    assert steps["extract"]["status"] == "ready" and steps["extract"]["status_detail"] is None


def test_rows_for_unknown_providers_are_ignored(env):
    settings, sf = env
    with sf.begin() as session:
        session.add(ModelSettingRow(step="draft", provider="retired", model="x", options={},
                                    updated_at=datetime.now(UTC), updated_by="old"))
        session.add(ModelSettingRow(step="no-such-step", provider="ollama", model="x", options={},
                                    updated_at=datetime.now(UTC), updated_by="old"))
        session.add(ModelSettingRow(step="classify", provider="openrouter", model="x", options={},
                                    updated_at=datetime.now(UTC), updated_by="old"))
    store = _store(settings, sf)
    assert store.choice(Step.DRAFT).provider == "openrouter"
    assert store.choice(Step.CLASSIFY).provider == "typesafe"
    assert len(store.describe()) == 5


def test_intake_pin_keeps_the_first_model_for_a_session(env):
    settings, sf = env
    store = _store(settings, sf)
    session_id = uuid.uuid4()
    with sf.begin() as session:
        session.add(IntakeSessionRow(id=session_id, token_hash="h" * 64, state={}))
    store.save(Step.INTAKE, ModelChoice("ollama", "gemma3:4b"), changed_by="Sara", latency_ms=1)
    first, timeout = store.intake_pin(session_id)
    assert first == ModelChoice("ollama", "gemma3:4b") and timeout == 150
    store.save(Step.INTAKE, ModelChoice("openrouter", "google/gemini-2.5-flash"), changed_by="Sara", latency_ms=1)
    assert store.intake_pin(session_id)[0] == first
    assert store.intake_pin(uuid.uuid4())[0] == ModelChoice("openrouter", "google/gemini-2.5-flash")


def test_unusable_intake_pin_is_replaced_with_the_current_choice(env, caplog):
    settings, sf = env
    store = _store(settings, sf)
    session_id = uuid.uuid4()
    with sf.begin() as session:
        session.add(IntakeSessionRow(id=session_id, token_hash="h" * 64, state={},
                                     model_choice={"provider": "retired", "model": "x", "options": {}}))
    choice, _timeout = store.intake_pin(session_id)
    current = store.choice(Step.INTAKE)
    assert choice == current
    with sf() as session:
        assert session.get(IntakeSessionRow, session_id).model_choice == current.to_json()
    store.intake_pin(session_id)
    assert len([r for r in caplog.records if "unusable pinned model" in r.getMessage()]) == 1
