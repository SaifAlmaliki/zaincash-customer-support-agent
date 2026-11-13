import pytest
from sqlalchemy import text
from sqlalchemy.engine import make_url

from app.config import Settings
from app.db.session import make_engine, reset_db
from app.db.workspace_schema import LegacySchemaError, upgrade_workspace_schema

pytestmark = pytest.mark.integration


@pytest.fixture
def engine():
    settings = Settings(_env_file=None, openrouter_api_key="", typesafe_api_key="")
    assert make_url(settings.test_database_url).database == "support_test"
    engine = make_engine(settings.test_database_url)
    reset_db(engine)
    yield engine
    reset_db(engine)
    engine.dispose()


def test_fresh_schema_passes_the_customer_check(engine):
    upgrade_workspace_schema(engine)


def test_nullable_ticket_phone_stops_startup_with_a_reset_instruction(engine):
    with engine.begin() as connection:
        connection.execute(text("ALTER TABLE tickets ALTER COLUMN customer_phone DROP NOT NULL"))
    with pytest.raises(LegacySchemaError, match="docker compose down -v"):
        upgrade_workspace_schema(engine)


def test_intake_sessions_without_a_customer_phone_stop_startup(engine):
    with engine.begin() as connection:
        connection.execute(text("ALTER TABLE intake_sessions DROP COLUMN customer_phone"))
    with pytest.raises(LegacySchemaError):
        upgrade_workspace_schema(engine)