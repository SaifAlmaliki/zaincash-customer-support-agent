"""TicketOutcome to JSON-safe dicts. Used by the DB repository and the CLI --out file."""
from __future__ import annotations

from dataclasses import asdict
from typing import Any

from app.pipeline.contracts import TicketOutcome


def outcome_to_row(o: TicketOutcome) -> dict[str, Any]:
    c = o.classifier.classification if o.classifier else None
    d, dr, lk = o.decision, o.draft, o.lookup
    return {
        "ticket_id": o.ticket.id,
        "category": c.category if c else None,
        "category_confidence": c.category_confidence if c else None,
        "category_probs": dict(c.category_probs) if c else {},
        "priority": d.priority if d else (c.priority if c else None),
        "priority_confidence": c.priority_confidence if c else None,
        "flags": dict(c.flags) if c else {},
        "classifier_path": o.classifier.path if o.classifier else None,
        "extracted": {k: asdict(v) for k, v in o.extracted.items()},
        "lookup_status": lk.status if lk else None,
        "matched_txn_ref": lk.txn.txn_ref if lk and lk.txn else None,
        "team": d.team if d else None,
        "escalated": d.escalated if d else False,
        "escalation_reasons": list(d.reasons) if d else [],
        "escalation_note": d.note if d else None,
        "draft_text": dr.text if dr else None,
        "citations": list(dr.citations) if dr else [],
        "agent_trace": list(dr.trace) if dr else [],
        "status": o.status,
        "error": o.error,
        "latency_ms": o.latency_ms,
        "cost_usd": o.cost_usd,
        "jev_model_version": c.model if c and c.source == "jev" else None,
    }


def outcome_to_dict(o: TicketOutcome) -> dict[str, Any]:
    row = outcome_to_row(o)
    row.pop("ticket_id")
    return {"external_id": o.ticket.external_id, "text": o.ticket.text, **row}
