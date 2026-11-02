import pytest
from fastapi.testclient import TestClient
from sqlalchemy import text
from sqlalchemy.engine import make_url
from typer.testing import CliRunner

from app import cli
from app.config import Settings
from app.db.session import make_engine, reset_db
from app.main import create_app


@pytest.mark.integration
@pytest.mark.parametrize("entrypoint", ["api", "cli"])
def test_entry_points_upgrade_legacy_run_status(entrypoint, monkeypatch, tmp_path):
    settings = Settings(
        _env_file=None,
        database_url=Settings(_env_file=None).test_database_url,
        openrouter_api_key="",
        typesafe_api_key="",
        intake_upload_dir=str(tmp_path),
    )
    assert make_url(settings.database_url).database == "support_test"
    engine = make_engine(settings.database_url)
    reset_db(engine)
    try:
        with engine.begin() as connection:
            run_id = connection.execute(text(
                "INSERT INTO runs (mode, prompt_version, model_ids, degraded, counts, "
                "total_cost_usd, status) VALUES ('jev', 'v1', CAST('{}' AS jsonb), false, "
                "CAST('{}' AS jsonb), 0, 'completed') RETURNING id"
            )).scalar_one()
            connection.execute(text("ALTER TABLE runs ALTER COLUMN status TYPE VARCHAR(16)"))

        if entrypoint == "cli":
            monkeypatch.setattr(cli, "get_settings", lambda: settings)
            result = CliRunner().invoke(cli.app, ["init-db"])
            assert result.exit_code == 0, result.output
        else:
            with TestClient(create_app(settings)) as client:
                assert client.get("/api/health").status_code == 200

        with engine.begin() as connection:
            length = connection.scalar(text(
                "SELECT character_maximum_length FROM information_schema.columns "
                "WHERE table_schema = current_schema() AND table_name = 'runs' "
                "AND column_name = 'status'"
            ))
            connection.execute(
                text("UPDATE runs SET status = 'completed_with_errors' WHERE id = :run_id"),
                {"run_id": run_id},
            )
            preserved = connection.execute(
                text("SELECT mode, status FROM runs WHERE id = :run_id"), {"run_id": run_id},
            ).one()
        assert length == 32
        assert preserved == ("jev", "completed_with_errors")
    finally:
        engine.dispose()
