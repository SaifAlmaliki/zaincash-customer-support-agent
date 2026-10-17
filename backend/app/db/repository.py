from __future__ import annotations

from collections.abc import Iterable, Sequence
from dataclasses import asdict, fields, replace
from datetime import UTC, datetime
from typing import Any

from sqlalchemy import or_, select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import Session, sessionmaker

from app.db.models import IncidentRow, RunRow, TicketResultRow, TicketRow, TransactionRow
from app.pipeline.contracts import Ticket, TicketOutcome, TxnRecord
from app.pipeline.graph import RunSummary
from app.pipeline.io.serialize import outcome_to_row
from app.pipeline.stage4_lookup.lookup import parse_dt


def upsert_tickets(session: Session, tickets: Sequence[Ticket], *, source: str,
                   batch_id: str | None = None) -> list[Ticket]:
    if not tickets:
        return []
    rows = [{"external_id": t.external_id, "channel": t.channel, "customer_phone": t.customer_phone,
             "text": t.text, "received_at": t.received_at, "source": source, "batch_id": batch_id}
            for t in tickets]
    session.execute(insert(TicketRow).values(rows).on_conflict_do_nothing(index_elements=["external_id"]))
    ids = dict(session.execute(
        select(TicketRow.external_id, TicketRow.id)
        .where(TicketRow.external_id.in_([t.external_id for t in tickets]))
    ).all())
    return [replace(t, id=ids[t.external_id]) for t in tickets]


def create_run(session: Session, *, mode: str, prompt_version: str, model_ids: dict) -> int:
    run = RunRow(mode=mode, prompt_version=prompt_version, model_ids=model_ids, status="running")
    session.add(run)
    session.flush()
    return run.id


def save_outcomes(session: Session, run_id: int, outcomes: Sequence[TicketOutcome]) -> None:
    rows = [{"run_id": run_id, **outcome_to_row(o)} for o in outcomes if o.ticket.id is not None]
    if not rows:
        return
    stmt = insert(TicketResultRow).values(rows)
    updatable = [k for k in rows[0] if k not in ("run_id", "ticket_id")]
    session.execute(stmt.on_conflict_do_update(
        constraint="uq_result_run_ticket", set_={k: stmt.excluded[k] for k in updatable}
    ))


def finish_run(session: Session, run_id: int, summary: RunSummary, *,
               status: str = "completed") -> None:
    run = session.get(RunRow, run_id)
    run.finished_at = datetime.now(UTC)
    run.counts = summary.to_dict()
    run.degraded = summary.degraded
    run.total_cost_usd = summary.total_cost_usd
    run.status = status


def _upsert(session: Session, model: Any, key: str, rows: list[dict]) -> int:
    if not rows:
        return 0
    stmt = insert(model).values(rows)
    session.execute(stmt.on_conflict_do_update(
        index_elements=[key], set_={k: stmt.excluded[k] for k in rows[0] if k != key}
    ))
    return len(rows)


def load_transactions(session: Session, records: Iterable[TxnRecord]) -> int:
    """Upsert by txn_ref. Returns the number of records passed in; duplicates collapse to one row."""
    records = list(records)
    unique = {r.txn_ref: asdict(r) for r in records}  # one row per txn_ref within one statement
    _upsert(session, TransactionRow, "txn_ref", list(unique.values()))
    return len(records)


def load_incidents(session: Session, rows: Iterable[dict]) -> int:
    clean = [{"id": str(r["id"]), "service": str(r["service"]),
              "started_at": parse_dt(r["started_at"]),
              "ended_at": parse_dt(r["ended_at"]) if r.get("ended_at") else None,
              "description": str(r["description"])} for r in rows]
    return _upsert(session, IncidentRow, "id", clean)


def _to_record(row: TransactionRow) -> TxnRecord:
    return TxnRecord(**{f.name: getattr(row, f.name) for f in fields(TxnRecord)})


class SqlTransactionRepo:
    def __init__(self, session_factory: sessionmaker) -> None:
        self._sf = session_factory

    @property
    def session_factory(self) -> sessionmaker:
        """Public factory for sibling read-only KB/investigation adapters.

        Each adapter opens its own session; callers must not share live sessions.
        Exposing the factory does not open a connection or change its lifecycle.
        """
        return self._sf

    def get_by_ref(self, txn_ref: str) -> TxnRecord | None:
        with self._sf() as s:
            row = s.get(TransactionRow, txn_ref)
            return _to_record(row) if row else None

    def search(self, *, phone, amount_min, amount_max, start, end, limit=10):
        q = select(TransactionRow).where(
            or_(TransactionRow.sender_phone == phone, TransactionRow.receiver_phone == phone),
            TransactionRow.created_at.between(start, end),
        )
        if amount_min is not None:
            q = q.where(TransactionRow.amount_iqd >= amount_min)
        if amount_max is not None:
            q = q.where(TransactionRow.amount_iqd <= amount_max)
        q = q.order_by(TransactionRow.created_at.desc()).limit(limit)
        with self._sf() as s:
            return [_to_record(r) for r in s.scalars(q)]
