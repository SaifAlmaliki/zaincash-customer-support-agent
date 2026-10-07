from datetime import datetime, timedelta

import pytest
from sqlalchemy import func, select
from sqlalchemy.exc import OperationalError

from app.config import Settings
from app.db.models import RunRow, TicketResultRow, TicketRow
from app.db.repository import (
    SqlTransactionRepo,
    create_run,
    finish_run,
    load_incidents,
    load_transactions,
    save_outcomes,
    upsert_tickets,
)
from app.db.session import make_engine, make_sessionmaker, reset_db
from app.pipeline.contracts import Decision, TicketOutcome
from app.pipeline.graph import summarize
from app.pipeline.lookup import txn_from_dict
from tests.helpers import BAGHDAD, make_ticket

pytestmark = pytest.mark.integration


@pytest.fixture
def sf():
    engine = make_engine(Settings().test_database_url)
    try:
        reset_db(engine)
    except OperationalError:
        pytest.skip("Postgres is not running: docker compose up -d db")
    yield make_sessionmaker(engine)
    engine.dispose()


def _count(s, model):
    return s.scalar(select(func.count()).select_from(model))


def test_upsert_tickets_is_idempotent(sf):
    with sf() as s:
        a = upsert_tickets(s, [make_ticket("x", external_id="A"), make_ticket("y", external_id="B")],
                           source="dataset")
        b = upsert_tickets(s, [make_ticket("changed", external_id="A")], source="dataset")
        s.commit()
        assert a[0].id == b[0].id and a[0].id is not None
        assert _count(s, TicketRow) == 2


def test_rerun_is_idempotent(sf):
    with sf() as s:
        [t] = upsert_tickets(s, [make_ticket("x", external_id="A")], source="dataset")
        run_id = create_run(s, mode="jev", prompt_version="v1", model_ids={"jev": "jev-1.13.0"})
        first = TicketOutcome(ticket=t, status="pending_review",
                              decision=Decision("General Care", "P4", False, (), ""))
        second = TicketOutcome(ticket=t, status="escalated",
                               decision=Decision("General Care", "P4", True, ("low_confidence",), "n"))
        save_outcomes(s, run_id, [first])
        save_outcomes(s, run_id, [second])
        finish_run(s, run_id, summarize([second]))
        s.commit()
        assert _count(s, TicketResultRow) == 1
        assert s.scalar(select(TicketResultRow.status)) == "escalated"
        run = s.get(RunRow, run_id)
        assert run.status == "completed" and run.counts["total"] == 1


def test_sql_transaction_repo(sf):
    rec = txn_from_dict({"txn_ref": "ZC2410000123", "sender_phone": "07809876543",
                         "receiver_phone": "07701234567", "amount_iqd": 50000, "type": "p2p",
                         "status": "pending", "created_at": "2026-10-06T18:10:00+03:00"})
    with sf() as s:
        assert load_transactions(s, [rec, rec]) == 2  # second copy is an update, not a duplicate
        assert load_incidents(s, [{"id": "INC-01", "service": "bill_pay",
                                   "started_at": "2026-10-01T08:00:00+03:00",
                                   "description": "Electricity biller timeout"}]) == 1
        s.commit()
    repo = SqlTransactionRepo(sf)
    assert repo.get_by_ref("ZC2410000123").amount_iqd == 50000
    when = datetime(2026, 10, 6, 12, tzinfo=BAGHDAD)
    hits = repo.search(phone="07701234567", amount_min=49500, amount_max=50500,
                       start=when - timedelta(days=3), end=when + timedelta(days=3))
    assert [h.txn_ref for h in hits] == ["ZC2410000123"]
    assert repo.search(phone="07000000000", amount_min=None, amount_max=None,
                       start=when - timedelta(days=3), end=when + timedelta(days=3)) == []
