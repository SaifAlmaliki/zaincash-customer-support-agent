from sqlalchemy import text


def upgrade_workspace_schema(engine):
    """Expand the original 16-character run status without dropping existing data."""
    with engine.begin() as connection:
        length = connection.scalar(text(
            "SELECT character_maximum_length FROM information_schema.columns "
            "WHERE table_schema = current_schema() AND table_name = 'runs' AND column_name = 'status'"
        ))
        if length is not None and length < 32:
            connection.execute(text("ALTER TABLE runs ALTER COLUMN status TYPE VARCHAR(32)"))
