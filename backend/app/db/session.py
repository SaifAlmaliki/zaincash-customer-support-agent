from __future__ import annotations

from sqlalchemy import Engine, create_engine, text
from sqlalchemy.orm import sessionmaker

from app.db import document_models  # noqa: F401 -- register sources for CLI initialization too
from app.db.models import Base
from app.intake import (
    db_models as intake_db_models,  # noqa: F401 -- register before create_all/drop_all
)
from app.kb import models as kb_models  # noqa: F401 -- register before create_all/drop_all


def make_engine(url: str) -> Engine:
    return create_engine(url, pool_pre_ping=True)


def make_sessionmaker(engine: Engine) -> sessionmaker:
    return sessionmaker(engine, expire_on_commit=False)


def init_db(engine: Engine) -> None:
    with engine.begin() as conn:
        conn.execute(text("CREATE EXTENSION IF NOT EXISTS vector"))
    Base.metadata.create_all(engine)


def reset_db(engine: Engine) -> None:
    Base.metadata.drop_all(engine)
    init_db(engine)
