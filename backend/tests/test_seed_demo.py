import re
from dataclasses import astuple

import pytest
from sqlalchemy import select
from sqlalchemy.engine import make_url

from app.config import REPO_ROOT, Settings
from app.db.models import CustomerRow, TicketRow, TransactionRow
from app.db.session import make_engine, make_sessionmaker, reset_db
from app.ingest import load_jsonl, load_tickets
from app.pipeline.contracts import TxnRecord
from app.pipeline.stage4_lookup.lookup import txn_from_dict

pytestmark = pytest.mark.integration
SEED = REPO_ROOT / "docker" / "db" / "seed_demo.sql"
FIXTURES = REPO_ROOT / "backend" / "tests" / "fixtures"


@pytest.fixture
def seeded():
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
            raw.driver_connection.autocommit = False
            raw.close()
        with make_sessionmaker(engine)() as session:
            yield session
    finally:
        reset_db(engine)
        engine.dispose()


def test_seed_transactions_equal_the_startup_fixture(seeded):
    """The API seeds sample_transactions.jsonl at startup; both sources must hold the same rows."""
    seeded_rows = {astuple(TxnRecord(**{f: getattr(r, f) for f in TxnRecord.__dataclass_fields__}))
                   for r in seeded.scalars(select(TransactionRow))}
    fixture = {astuple(txn_from_dict(r)) for r in load_jsonl(FIXTURES / "sample_transactions.jsonl")}
    assert seeded_rows == fixture


@pytest.mark.parametrize("path", [REPO_ROOT / "data" / "demo" / "rag_tickets.jsonl",
                                  FIXTURES / "sample_tickets.jsonl"], ids=lambda p: p.name)
def test_seeded_tickets_equal_their_upload_fixture(seeded, path):
    """A re-upload reuses the stored ticket, so shared IDs must agree on every stored field."""
    stored = {r.external_id: (r.channel, r.customer_phone, r.text, r.received_at)
              for r in seeded.scalars(select(TicketRow))}
    shared = [t for t in load_tickets(path) if t.external_id in stored]
    assert shared
    assert {t.external_id: (t.channel, t.customer_phone, t.text, t.received_at) for t in shared} == {
        t.external_id: stored[t.external_id] for t in shared}


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
            refs = set(session.scalars(select(TransactionRow.txn_ref)))
        assert len(phones) == 7
        assert set(phones) <= customers
        assert {
            "ZC2410001001", "ZC2410001002", "ZC2410001003", "ZC2410001004",
        } <= refs
        assert all(re.fullmatch(r"07[3-9][0-9]{8}", phone) for phone in phones)
    finally:
        reset_db(engine)
        engine.dispose()
