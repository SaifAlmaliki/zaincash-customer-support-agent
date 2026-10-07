import json

from app.pipeline.contracts import Decision, ExtractedField, TicketOutcome
from app.pipeline.serialize import outcome_to_dict, outcome_to_row
from tests.fakes import make_output
from tests.helpers import make_ticket


def test_full_outcome_is_json_safe():
    o = TicketOutcome(
        ticket=make_ticket("x", id=7), status="escalated", classifier=make_output(),
        extracted={"amount": ExtractedField(50000, "50 الف", 0, 6, "jev_pick", 0.9, "IQD")},
        decision=Decision("Payments Ops", "P2", True, ("txn_not_found",), "Escalated: ..."),
    )
    row = outcome_to_row(o)
    assert row["ticket_id"] == 7 and row["escalation_reasons"] == ["txn_not_found"]
    assert row["extracted"]["amount"]["value"] == 50000
    json.dumps(row, ensure_ascii=False)


def test_failed_outcome_and_dict_form():
    o = TicketOutcome(ticket=make_ticket("x", external_id="E-1"), status="failed", error="boom")
    d = outcome_to_dict(o)
    assert d["external_id"] == "E-1" and d["status"] == "failed" and d["category"] is None
    assert "ticket_id" not in d
    json.dumps(d)
