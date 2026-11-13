from sqlalchemy import text

LEGACY_SCHEMA_MESSAGE = (
    "This database was created before customers were identified by phone number. "
    "Reset the demo database: run `docker compose down -v`, then `docker compose up --build -d`, "
    "then load docker/db/seed_demo.sql."
)


class LegacySchemaError(RuntimeError):
    """The database predates the customer phone identity and must be recreated."""


def _nullable(connection, table: str, column: str) -> str | None:
    return connection.scalar(text(
        "SELECT is_nullable FROM information_schema.columns "
        "WHERE table_schema = current_schema() AND table_name = :table AND column_name = :column"
    ), {"table": table, "column": column})


def assert_customer_schema(connection) -> None:
    if _nullable(connection, "tickets", "customer_phone") == "YES":
        raise LegacySchemaError(LEGACY_SCHEMA_MESSAGE)


def upgrade_workspace_schema(engine):
    """Apply additive schema upgrades that create_all cannot perform on existing tables."""
    with engine.begin() as connection:
        assert_customer_schema(connection)
        length = connection.scalar(text(
            "SELECT character_maximum_length FROM information_schema.columns "
            "WHERE table_schema = current_schema() AND table_name = 'runs' AND column_name = 'status'"
        ))
        if length is not None and length < 32:
            connection.execute(text("ALTER TABLE runs ALTER COLUMN status TYPE VARCHAR(32)"))
        # Intake sessions created before admin model settings have no pinned model.
        connection.execute(text(
            "ALTER TABLE IF EXISTS intake_sessions ADD COLUMN IF NOT EXISTS model_choice JSONB"
        ))