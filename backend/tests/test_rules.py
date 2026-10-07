from app.pipeline.contracts import FIELD_NAMES, ExtractedField, LookupResult
from app.pipeline.rules import decide, empty_ticket_decision, merge_reasons, note_for
from tests.fakes import make_output


def _ex(**values):
    out = {f: ExtractedField(None, None, None, None, "none", 0.0) for f in FIELD_NAMES}
    for k, v in values.items():
        out[k] = ExtractedField(v, str(v), 0, 1, "jev_pick", 0.9)
    return out


def _decide(tax, category="failed_transfer", out=None, lookup="matched", **values):
    out = out or make_output(category)
    return decide(category=tax.get(category), classifier=out,
                  extracted=_ex(**values), lookup=LookupResult(lookup))


def test_clean_ticket_not_escalated(tax):
    d = _decide(tax, amount=50000, date="2026-10-06")
    assert d.team == "Payments Ops" and d.priority == "P2"
    assert not d.escalated and d.reasons == () and d.note == ""


def test_fraud_flag_forces_p1_and_escalates(tax):
    out = make_output("failed_transfer", priority="P3", flags={"fraud_suspected": 0.9})
    d = _decide(tax, out=out, amount=1, date="2026-10-06")
    assert d.priority == "P1" and "fraud_suspected" in d.reasons


def test_money_lost_raises_to_p2_and_min_priority_applies(tax):
    out = make_output("app_bug", priority="P4", flags={"money_lost": 0.8})
    d = _decide(tax, "app_bug", out=out, lookup="not_applicable")
    assert d.priority == "P2"
    assert _decide(tax, "fraud_report", out=make_output("fraud_report", priority="P4"),
                   lookup="not_applicable").priority == "P1"


def test_missing_required_fields_unless_matched(tax):
    d = _decide(tax, lookup="not_found")
    assert d.reasons == ("missing_required_fields", "txn_not_found")
    assert "missing_required_fields" not in _decide(tax, lookup="matched").reasons


def test_classifier_reasons_come_first(tax):
    out = make_output(uncertain=True, reasons=("low_confidence",), flags={"multi_issue": 0.7})
    d = _decide(tax, out=out, amount=1, date="2026-10-06")
    assert d.reasons[:2] == ("low_confidence", "multi_issue")
    assert d.note.startswith("Escalated: ")


def test_lookup_reason_mapping(tax):
    assert "txn_ambiguous" in _decide(tax, lookup="ambiguous", amount=1, date="x").reasons
    assert "amount_mismatch" in _decide(tax, lookup="amount_mismatch", amount=1, date="x").reasons


def test_merge_and_empty(tax):
    d = _decide(tax, amount=1, date="2026-10-06")
    m = merge_reasons(d, ("draft_failed_guardrail",))
    assert m.escalated and m.reasons == ("draft_failed_guardrail",)
    assert merge_reasons(d, ()) == d
    e = empty_ticket_decision(tax.get("other"))
    assert e.escalated and e.reasons == ("empty_ticket",) and e.priority == "P4"
    assert note_for(()) == ""
