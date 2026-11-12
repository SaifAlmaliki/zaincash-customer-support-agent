from sqlalchemy import text


def upgrade_workspace_schema(engine):
    """Apply additive schema upgrades that create_all cannot perform on existing tables."""
    with engine.begin() as connection:
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
