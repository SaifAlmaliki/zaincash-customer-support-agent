import json
from pathlib import Path

import pytest
from typer.testing import CliRunner

from app import cli
from app.pipeline import factory
from app.pipeline.graph import PipelineDeps, build_graph
from app.pipeline.stage4_lookup.lookup import InMemoryTransactionRepo
from app.taxonomy import load_taxonomy
from tests.fakes import FakeClassifier, make_output

FIXTURES = Path(__file__).parent / "fixtures"
runner = CliRunner()


def test_run_batch_no_db_writes_summary_and_out(monkeypatch, tmp_path):
    def fake_build(settings, mode, repo, **kw):
        assert isinstance(repo, InMemoryTransactionRepo)
        tax = load_taxonomy(settings.taxonomy_path)
        return build_graph(PipelineDeps(mode="jev", taxonomy=tax, txn_repo=repo,
                                        jev=FakeClassifier(make_output("general_inquiry", priority="P4"))))

    monkeypatch.setattr(factory, "build_pipeline", fake_build)
    out = tmp_path / "out.json"
    result = runner.invoke(cli.app, [
        "run-batch", str(FIXTURES / "sample_tickets.jsonl"), "--mode", "jev", "--no-db",
        "--transactions", str(FIXTURES / "sample_transactions.jsonl"), "--out", str(out), "--limit", "3",
    ])
    assert result.exit_code == 0, result.output
    assert json.loads(result.output)["total"] == 3
    rows = json.loads(out.read_text(encoding="utf-8"))
    assert [r["external_id"] for r in rows] == ["S-001", "S-002", "S-003"]


def test_config_error_exits_2(monkeypatch):
    def boom(*a, **kw):
        raise factory.ConfigError("TYPESAFE_API_KEY is required")

    monkeypatch.setattr(factory, "build_pipeline", boom)
    result = runner.invoke(cli.app, ["run-batch", str(FIXTURES / "sample_tickets.jsonl"),
                                     "--mode", "jev", "--no-db"])
    assert result.exit_code == 2 and "TYPESAFE_API_KEY" in result.output


@pytest.fixture
def ingest_env(monkeypatch):
    from sqlalchemy.engine import make_url

    from app.config import Settings
    from app.db.session import make_engine, make_sessionmaker, reset_db
    from app.kb.service import KnowledgeService
    from tests.kb_api_fakes import Embeddings

    settings = Settings(_env_file=None, openrouter_api_key="test-router-secret", typesafe_api_key="")
    assert make_url(settings.test_database_url).database == "support_test"
    engine = make_engine(settings.test_database_url)
    reset_db(engine)
    sf = make_sessionmaker(engine)
    embeddings = Embeddings()
    monkeypatch.setattr(cli, "get_settings", lambda: settings)
    monkeypatch.setattr(cli, "_sessionmaker", lambda settings: sf)
    monkeypatch.setattr(cli, "make_knowledge_service", lambda sf, settings: KnowledgeService(sf, settings, embeddings), raising=False)
    yield sf, embeddings
    engine.dispose()


@pytest.mark.integration
def test_ingest_directory_is_deterministic_and_duplicate_is_free(ingest_env, tmp_path):
    (tmp_path / "b.MD").write_text("Second policy", encoding="utf-8")
    (tmp_path / "a.md").write_text("First policy", encoding="utf-8")
    (tmp_path / "ignore.json").write_text("{}", encoding="utf-8")
    first = runner.invoke(cli.app, ["ingest-kb", str(tmp_path)])
    assert first.exit_code == 0, first.output
    rows = [json.loads(line) for line in first.output.splitlines()]
    assert [r["filename"] for r in rows] == ["a.md", "b.MD"]
    assert all(r["status"] == "indexed" for r in rows)
    second = runner.invoke(cli.app, ["ingest-kb", str(tmp_path)])
    assert second.exit_code == 0, second.output
    assert ingest_env[1].calls == 2


@pytest.mark.integration
def test_ingest_failure_exit_and_retry_stored(ingest_env, tmp_path):
    path = tmp_path / "policy.md"
    path.write_text("policy", encoding="utf-8")
    ingest_env[1].error = True
    failure = runner.invoke(cli.app, ["ingest-kb", str(path)])
    assert failure.exit_code == 1, failure.output
    assert json.loads(failure.output)["status"] == "failed"
    assert "test-router-secret" not in failure.output
    ingest_env[1].error = False
    retried = runner.invoke(cli.app, ["ingest-kb", "--retry-stored"])
    assert retried.exit_code == 0, retried.output
    assert json.loads(retried.output)["status"] == "indexed"
    assert json.loads(retried.output)["cost_usd"] == pytest.approx(0.04)
    assert runner.invoke(cli.app, ["ingest-kb", "--retry-stored"]).exit_code == 0
    assert ingest_env[1].calls == 2


@pytest.mark.integration
def test_ingest_invalid_source_does_not_stop_other_files(ingest_env, tmp_path):
    (tmp_path / "a.md").write_bytes(b"\xff")
    (tmp_path / "b.md").write_text("Valid policy", encoding="utf-8")
    result = runner.invoke(cli.app, ["ingest-kb", str(tmp_path)])
    assert result.exit_code == 1, result.output
    rows = [json.loads(line) for line in result.output.splitlines()]
    assert [r["status"] for r in rows] == ["failed", "indexed"]
    assert ingest_env[1].calls == 1


@pytest.mark.integration
def test_ingest_limits_batch_without_partial_side_effects(ingest_env, tmp_path):
    for i in range(101):
        (tmp_path / f"{i}.md").write_text(f"policy {i}", encoding="utf-8")
    result = runner.invoke(cli.app, ["ingest-kb", str(tmp_path)])
    assert result.exit_code == 2 and "100" in result.output
    assert ingest_env[1].calls == 0


@pytest.mark.integration
def test_retry_stored_indexes_old_uploads_without_recovering_other_process_jobs(ingest_env):
    from app.kb.documents import store_document

    with ingest_env[0].begin() as session:
        store_document(session, "old.md", b"old upload awaiting indexing")
    result = runner.invoke(cli.app, ["ingest-kb", "--retry-stored"])
    assert result.exit_code == 0, result.output
    assert json.loads(result.output)["status"] == "indexed"


@pytest.mark.integration
def test_ingest_disabled_configuration_never_calls_provider(ingest_env, tmp_path, monkeypatch):
    settings = cli.get_settings().model_copy(update={"rag_enabled": False})
    monkeypatch.setattr(cli, "get_settings", lambda: settings)
    path = tmp_path / "policy.md"
    path.write_text("policy", encoding="utf-8")
    result = runner.invoke(cli.app, ["ingest-kb", str(path)])
    assert result.exit_code == 2 and "disabled" in result.output
    assert ingest_env[1].calls == 0
