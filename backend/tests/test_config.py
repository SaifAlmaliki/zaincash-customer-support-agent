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
