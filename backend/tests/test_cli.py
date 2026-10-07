import json
from pathlib import Path

from typer.testing import CliRunner

from app import cli
from app.pipeline import factory
from app.pipeline.graph import PipelineDeps, build_graph
from app.pipeline.lookup import InMemoryTransactionRepo
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
