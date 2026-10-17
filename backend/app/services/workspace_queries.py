"""Response projections shared by list/detail endpoints and review mutations."""
from sqlalchemy import func, select

from app.db.models import ReviewRow, RunRow, TicketResultRow, TicketRow, TransactionRow
from app.services.draft_evidence import draft_evidence

STAGES = [
    {"id": "prepare", "number": 1, "label": "Prepare", "description": "Normalize text and find candidate details", "file": "stage1_normalize/normalize.py"},
    {"id": "classify", "number": 2, "label": "Classify", "description": "Jev triage with Gemini fallback", "file": "stage2_classify/jev.py"},
    {"id": "extract", "number": 3, "label": "Extract", "description": "Anchor reference, amount and date to the source", "file": "stage3_extract/extract.py"},
    {"id": "lookup", "number": 4, "label": "Investigate", "description": "Find the matching mock transaction", "file": "stage4_lookup/lookup.py"},
    {"id": "decide", "number": 5, "label": "Route", "description": "Apply team, priority and escalation rules", "file": "stage5_decide/rules.py"},
    {"id": "draft", "number": 6, "label": "Draft & review", "description": "Retrieve policy evidence, draft an Arabic reply and check guardrails for human review", "file": "stage6_draft/agent.py"},
]


def columns(row):
    return {column.name: getattr(row, column.name) for column in row.__table__.columns}


def latest_results_query():
    latest = select(func.max(TicketResultRow.id)).group_by(TicketResultRow.ticket_id)
    return select(TicketResultRow).where(TicketResultRow.id.in_(latest))


def result_view(session, result, *, detail=False):
    value = columns(result)
    value["ticket"] = columns(session.get(TicketRow, result.ticket_id))
    approvals = session.scalars(select(ReviewRow).where(
        ReviewRow.result_id == result.id, ReviewRow.action.in_(["approve", "edit_approve"])
    ).order_by(ReviewRow.id.desc())).first()
    value["final_text"] = approvals.final_text if approvals else None
    if detail:
        value.update(draft_evidence(result.agent_trace, result.citations))
        value["reviews"] = [columns(review) for review in session.scalars(
            select(ReviewRow).where(ReviewRow.result_id == result.id).order_by(ReviewRow.id.desc())
        )]
        txn = session.get(TransactionRow, result.matched_txn_ref) if result.matched_txn_ref else None
        value["transaction"] = columns(txn) if txn else None
    return value


def run_view(session, run: RunRow):
    value = columns(run)
    value["processed"] = session.scalar(select(func.count()).select_from(TicketResultRow).where(
        TicketResultRow.run_id == run.id
    ))
    value["total"] = run.counts.get("expected_total", run.counts.get("total", 0))
    return value
