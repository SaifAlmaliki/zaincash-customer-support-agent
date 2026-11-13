import re

import pytest
from sqlalchemy import select
from sqlalchemy.engine import make_url

from app.config import REPO_ROOT, Settings
from app.db.models import CustomerRow, TicketRow
from app.db.session import make_engine, make_sessionmaker, reset_db

pytestmark = pytest.mark.integration
SEED = REPO_ROOT / "docker" / "db" / "seed_demo.sql"


def test_demo_seed_gives_every_ticket_a_customer():
    settings = Settings(_env_file=None, openrouter_api_key="", typesafe_api_key="")
    assert make_url(settings.test_database_url).database == "support_test"
    engine = make_engine(settings.test_database_url)
    try:
        reset_db(engine)
        raw = engine.raw_connection()
        try:
            raw.driver_connection.autocommit = True  # the script has its own BEGIN/COMMIT
            with raw.driver_connection.cursor() as cursor:
                cursor.execute(SEED.read_text(encoding="utf-8"))
        finally:
            raw.driver_connection.rollback()
            raw.driver_connection.autocommit = False  # do not return an autocommit connection to the pool
            raw.close()
        with make_sessionmaker(engine)() as session:
            phones = list(session.scalars(select(TicketRow.customer_phone)))
            customers = set(session.scalars(select(CustomerRow.phone)))
        assert len(phones) == 7
        assert set(phones) <= customers
        assert all(re.fullmatch(r"07[3-9][0-9]{8}", phone) for phone in phones)
    finally:
        reset_db(engine)
        engine.dispose()
