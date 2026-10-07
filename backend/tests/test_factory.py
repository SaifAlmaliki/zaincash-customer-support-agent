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
    assert model_ids(s, "jev") == {"jev": "jev-1.13.0", "gemini": "google/gemini-3.8-flash"}
    assert model_ids(s, "gemini") == {"gemini": "google/gemini-3.8-flash"}


def test_openrouter_key_enables_gemini_pipeline():
    graph = build_pipeline(_settings(openrouter_api_key="test-openrouter-key"), "gemini", REPO)
    assert "gemini_classify" in graph.get_graph().nodes
