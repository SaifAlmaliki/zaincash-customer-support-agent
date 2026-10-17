import pytest

from app.config import REPO_ROOT, Settings


def test_repo_root_is_project_root():
    assert (REPO_ROOT / "backend" / "app").is_dir()


def test_defaults():
    s = Settings(_env_file=None)
    assert s.taxonomy_path == str(REPO_ROOT / "data" / "taxonomy.yaml")
    assert s.jev_model == "jev-1.13.0"
    assert s.t_gem == 0.66
    assert s.pipeline_concurrency == 20


def test_env_overrides(monkeypatch):
    monkeypatch.setenv("T_JEV", "0.75")
    monkeypatch.setenv("PIPELINE_CONCURRENCY", "5")
    s = Settings(_env_file=None)
    assert s.t_jev == 0.75
    assert s.pipeline_concurrency == 5


def test_openrouter_key_is_loaded_from_environment(monkeypatch):
    monkeypatch.setenv("OPENROUTER_API_KEY", "test-openrouter-key")
    assert Settings(_env_file=None).openrouter_api_key == "test-openrouter-key"


@pytest.mark.parametrize("model, expected", [
    ("gemini-2.5-flash", "google/gemini-2.5-flash"),
    ("google/gemini-3.8-flash", "google/gemini-3.8-flash"),
])
def test_legacy_gemini_model_names_are_qualified_for_openrouter(model, expected):
    assert Settings(_env_file=None, gemini_model=model).gemini_model == expected


def test_drafting_limits_load_from_environment(monkeypatch):
    monkeypatch.setenv("AGENT_MAX_TOOL_CALLS", "6")
    monkeypatch.setenv("AGENT_TIMEOUT_S", "30")
    settings = Settings(_env_file=None)
    assert settings.agent_max_tool_calls == 6 and settings.agent_timeout_s == 30


@pytest.mark.parametrize("values", [{"agent_max_tool_calls": 7}, {"agent_max_tool_calls": 0},
                                    {"agent_max_tool_calls": True}, {"agent_timeout_s": 31},
                                    {"agent_timeout_s": 0}, {"agent_timeout_s": float("nan")}])
def test_drafting_configuration_cannot_bypass_hard_limits(values):
    from pydantic import ValidationError

    with pytest.raises(ValidationError):
        Settings(_env_file=None, **values)
