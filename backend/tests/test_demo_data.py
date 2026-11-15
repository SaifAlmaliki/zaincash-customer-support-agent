"""The demo tickets must match the transaction fixture the API seeds at startup."""
from datetime import timedelta

import pytest

from app.config import REPO_ROOT
from app.ingest import load_jsonl, load_tickets
from app.pipeline.contracts import ExtractedField
from app.pipeline.stage1_normalize.candidates import find_candidates, parse_amount
from app.pipeline.stage1_normalize.dates import resolve_date
from app.pipeline.stage1_normalize.normalize import normalize
from app.pipeline.stage4_lookup.lookup import InMemoryTransactionRepo, match_transaction, txn_from_dict

FIXTURES = REPO_ROOT / "backend" / "tests" / "fixtures"
RAG_TICKETS = REPO_ROOT / "data" / "demo" / "rag_tickets.jsonl"

# external_id -> (category, txn_ref the lookup must match), as listed in data/demo/README.md
PAYMENT_TICKETS = {
    "RAG-DEMO-FAILED-TRANSFER": ("failed_transfer", "ZC2410000123"),
    "RAG-DEMO-FRAUD": ("fraud_report", "ZC2410000789"),
    "RAG-DEMO-WRONG-RECIPIENT": ("wrong_recipient", "ZC2410001001"),
    "RAG-DEMO-AGENT": ("agent_dispute", "ZC2410001002"),
    "RAG-DEMO-BILL": ("bill_payment", "ZC2410001003"),
    "RAG-DEMO-REFUND": ("refund_request", "ZC2410001004"),
}

_NONE = ExtractedField(None, None, None, None, "none", 0.0)


def _first_candidates(ticket):
    """Stand in for Jev's picks: the first candidate of each field, as stage 3 would finalize it."""
    nt = normalize(ticket)
    cands = find_candidates(nt.match_text)
    extracted = {"txn_ref": _NONE, "amount": _NONE, "phone": _NONE, "date": _NONE}
    if cands.txn_ref:
        c = cands.txn_ref[0]
        extracted["txn_ref"] = ExtractedField(c.value, c.span, c.start, c.end, "jev_pick", 1.0)
    if cands.amount:
        c = cands.amount[0]
        value, currency = parse_amount(c.span)
        extracted["amount"] = ExtractedField(value, c.span, c.start, c.end, "jev_pick", 1.0, currency)
    counterparts = [c for c in cands.phone if c.value != ticket.customer_phone]
    if counterparts:
        c = counterparts[0]
        extracted["phone"] = ExtractedField(c.value, c.span, c.start, c.end, "jev_pick", 1.0)
    if cands.date and (when := resolve_date(cands.date[0].span, ticket.received_at)):
        c = cands.date[0]
        extracted["date"] = ExtractedField(when.isoformat(), c.span, c.start, c.end, "jev_pick", 1.0)
    return extracted


@pytest.mark.parametrize("external_id", sorted(PAYMENT_TICKETS))
def test_payment_demo_ticket_matches_seeded_transaction(external_id, tax):
    tickets = {t.external_id: t for t in load_tickets(RAG_TICKETS)}
    repo = InMemoryTransactionRepo(txn_from_dict(r) for r in load_jsonl(FIXTURES / "sample_transactions.jsonl"))
    category, expected = PAYMENT_TICKETS[external_id]
    ticket = tickets[external_id]

    result = match_transaction(tax.get(category), _first_candidates(ticket),
                               customer_phone=ticket.customer_phone, received_at=ticket.received_at, repo=repo)

    assert (result.status, result.txn.txn_ref if result.txn else None) == ("matched", expected)
    assert result.txn.created_at <= ticket.received_at


def test_card_ticket_customer_has_declined_card_attempts():
    ticket = {t.external_id: t for t in load_tickets(RAG_TICKETS)}["RAG-DEMO-CARD"]
    repo = InMemoryTransactionRepo(txn_from_dict(r) for r in load_jsonl(FIXTURES / "sample_transactions.jsonl"))
    rows = repo.search(phone=ticket.customer_phone, amount_min=None, amount_max=None,
                       start=ticket.received_at - timedelta(days=14), end=ticket.received_at)
    assert [r.txn_ref for r in rows] == ["ZC2410001007", "ZC2410001006", "ZC2410001005"]
    assert {(r.type, r.status, r.failure_reason) for r in rows} == {
        ("card", "declined", "الدفع الإلكتروني غير مفعّل على البطاقة")}
    assert all(r.receiver_name for r in rows)
