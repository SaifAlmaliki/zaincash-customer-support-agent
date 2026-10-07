from datetime import datetime

from app.pipeline.contracts import FIELD_NAMES, ExtractedField
from app.pipeline.stage4_lookup.lookup import (
    InMemoryTransactionRepo,
    match_transaction,
    txn_from_dict,
)
from tests.helpers import BAGHDAD, RECEIVED

CUSTOMER = "07809876543"
REPO = InMemoryTransactionRepo([
    txn_from_dict({"txn_ref": "ZC2410000123", "sender_phone": CUSTOMER, "receiver_phone": "07701234567",
                   "receiver_name": "علي", "amount_iqd": 50000, "type": "p2p", "status": "pending",
                   "created_at": "2026-10-06T18:10:00+03:00"}),
    txn_from_dict({"txn_ref": "ZC2410000124", "sender_phone": CUSTOMER, "receiver_phone": "07711111111",
                   "receiver_name": "حسن", "amount_iqd": 25000, "type": "p2p", "status": "completed",
                   "created_at": "2026-10-05T10:00:00+03:00"}),
    txn_from_dict({"txn_ref": "ZC2410000125", "sender_phone": CUSTOMER, "receiver_phone": "07722222222",
                   "receiver_name": "زينب", "amount_iqd": 25000, "type": "p2p", "status": "completed",
                   "created_at": "2026-10-04T10:00:00+03:00"}),
])


def _ex(**values):
    out = {f: ExtractedField(None, None, None, None, "none", 0.0) for f in FIELD_NAMES}
    for k, v in values.items():
        out[k] = ExtractedField(v, str(v), 0, 1, "jev_pick", 0.9)
    return out


def _match(tax, category="failed_transfer", phone=CUSTOMER, **values):
    return match_transaction(tax.get(category), _ex(**values), customer_phone=phone,
                             received_at=RECEIVED, repo=REPO)


def test_not_applicable_category(tax):
    assert _match(tax, "login_access").status == "not_applicable"


def test_ref_matched(tax):
    r = _match(tax, txn_ref="ZC2410000123", amount=50000, date="2026-10-06")
    assert r.status == "matched" and r.txn.txn_ref == "ZC2410000123"


def test_ref_not_found(tax):
    assert _match(tax, txn_ref="ZC0000000000").status == "not_found"


def test_amount_and_date_mismatch(tax):
    assert _match(tax, txn_ref="ZC2410000123", amount=60000).status == "amount_mismatch"
    assert _match(tax, txn_ref="ZC2410000123", date="2026-09-20").status == "date_mismatch"


def test_search_by_phone_amount_date(tax):
    r = _match(tax, amount=50000, date="2026-10-06")
    assert r.status == "matched" and r.txn.txn_ref == "ZC2410000123"


def test_ambiguous_then_disambiguated_by_counterpart(tax):
    r = _match(tax, amount=25000)
    assert r.status == "ambiguous" and r.candidates_found == 2
    ex = _ex(amount=25000, phone="07722222222")
    r = match_transaction(tax.get("failed_transfer"), ex, customer_phone=CUSTOMER,
                          received_at=RECEIVED, repo=REPO)
    assert r.status == "matched" and r.txn.txn_ref == "ZC2410000125"


def test_no_phone_is_not_found(tax):
    assert _match(tax, phone=None, amount=50000).status == "not_found"


def test_txn_from_dict_parses_datetime():
    t = txn_from_dict({"txn_ref": "ZC1", "sender_phone": "07", "amount_iqd": "5", "type": "p2p",
                       "status": "completed", "created_at": "2026-10-06T18:10:00"})
    assert t.created_at == datetime(2026, 10, 6, 18, 10, tzinfo=BAGHDAD) and t.amount_iqd == 5
