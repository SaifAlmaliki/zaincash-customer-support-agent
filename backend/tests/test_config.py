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
