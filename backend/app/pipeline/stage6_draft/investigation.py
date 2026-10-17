"""Bounded, ticket-scoped, read-only SQL investigation. Call from a worker thread."""
from __future__ import annotations

from collections.abc import Collection
from contextlib import contextmanager
from dataclasses import fields
from datetime import datetime, time, timedelta

from sqlalchemy import case, func, or_, select, text
from sqlalchemy.orm import sessionmaker

from app.db.models import IncidentRow, TicketRow, TransactionRow
from app.pipeline.contracts import TxnRecord
from app.pipeline.stage1_normalize.candidates import normalize_phone
from app.pipeline.stage4_lookup.lookup import parse_dt
from app.pipeline.stage6_draft.context import DraftToolInputError
from app.pipeline.state import PipelineState


def _string(value, name, maximum=32):
    if not isinstance(value, str) or not value.strip() or len(value) > maximum:
        raise DraftToolInputError(f"{name} must be nonempty text of at most {maximum} characters")
    return value.strip()


def _field(state, name):
    item = state.get("extracted", {}).get(name)
    return item.value if item else None


def _phones(state):
    """Never widen customer access using phone numbers returned by a search."""
    principal = normalize_phone(state["ticket"].customer_phone or "")
    phones = {p for value in (principal, _field(state, "phone"))
              if (p := normalize_phone(str(value or "")))}
    lookup = state.get("lookup")
    if lookup and lookup.status == "matched" and lookup.txn:
        phones.update(p for value in (lookup.txn.sender_phone, lookup.txn.receiver_phone)
                      if (p := normalize_phone(value or "")))
    return principal, phones


def _phone(state, phone):
    value = normalize_phone(_string(phone, "phone"))
    if value is None or value not in _phones(state)[1]:
        raise DraftToolInputError("phone is outside this ticket's verified context")
    return value


def _stored_phone(column):
    """Canonicalize approved digit/prefix spellings and phone formatting only.

    After Arabic/Persian digit translation, accept ASCII digits, whitespace/NBSP,
    plus, parentheses and hyphens. Reject other characters before stripping: an
    unsupported decimal digit must never disappear and alias another customer.
    SQLAlchemy binds the translation/regex literals and comparison values. Keep
    this in the predicates so filtering precedes LIMIT without rewriting rows.
    """
    ascii_digits = func.translate(column, "٠١٢٣٤٥٦٧٨٩۰۱۲۳۴۵۶۷۸۹", "0123456789" * 2)
    approved = ascii_digits.op("~")("^[0123456789+()[:space:]\u00a0-]+$")
    digits = func.regexp_replace(ascii_digits, "[^0-9]", "", "g")
    return case((approved, func.regexp_replace(digits, "^964", "0")), else_=None)


def _involves(phone):
    return or_(_stored_phone(TransactionRow.sender_phone) == phone,
               _stored_phone(TransactionRow.receiver_phone) == phone)


def _scope(state):
    principal, phones = _phones(state)
    if principal:
        return _involves(principal)
    if phones:
        return or_(_stored_phone(TransactionRow.sender_phone).in_(phones),
                   _stored_phone(TransactionRow.receiver_phone).in_(phones))
    return None


def _datetime(value, name, *, end_of_day=False):
    if not isinstance(value, datetime):
        value = _string(value, name, 40)
    try:
        result = parse_dt(value)
    except (ValueError, OverflowError) as exc:
        raise DraftToolInputError(f"{name} must be an ISO date or datetime") from exc
    if end_of_day and isinstance(value, str) and len(value) == 10:
        result = datetime.combine(result.date(), time.max, result.tzinfo)
    return result


def _days(days):
    if type(days) is not int or not 1 <= days <= 90:
        raise DraftToolInputError("days must be an integer in 1–90")
    return days


def _record(row):
    # Match the existing repository's dataclass projection, without importing its graph dependency.
    return TxnRecord(**{f.name: getattr(row, f.name) for f in fields(TxnRecord)})


class SqlInvestigationRepo:
    """Shared repository; every call supplies its ticket snapshot and gets a fresh session.

    All methods are synchronous. Date strings without a zone use the pipeline's
    Baghdad convention. Date-only date_to includes that day, capped at receipt.
    SQL transactions are read-only, with 5s statement and 1s lock timeouts.
    """

    def __init__(self, session_factory: sessionmaker) -> None:
        self._sf = session_factory

    @contextmanager
    def _session(self):
        with self._sf() as session:
            session.execute(text("SET TRANSACTION READ ONLY"))
            session.execute(text("SET LOCAL statement_timeout = '5000ms'"))
            session.execute(text("SET LOCAL lock_timeout = '1000ms'"))
            yield session

    def lookup_transaction(self, state: PipelineState, txn_ref: str, *,
                           known_refs: Collection[str] = ()) -> TxnRecord | None:
        ref = _string(txn_ref, "txn_ref").upper()
        allowed = {str(_field(state, "txn_ref") or "").upper(), *known_refs}
        lookup = state.get("lookup")
        if lookup and lookup.status == "matched" and lookup.txn:
            allowed.add(lookup.txn.txn_ref)
        if ref not in allowed:
            raise DraftToolInputError("txn_ref is outside this ticket's verified context")
        q = select(TransactionRow).where(TransactionRow.txn_ref == ref,
                                        TransactionRow.created_at <= parse_dt(state["ticket"].received_at))
        scope = _scope(state)
        if scope is not None:
            q = q.where(scope)
        with self._session() as session:
            row = session.scalar(q)
            return _record(row) if row else None

    def search_transactions(self, state: PipelineState, phone: str, amount_iqd: int | None,
                            date_from: str, date_to: str) -> list[TxnRecord]:
        phone = _phone(state, phone)
        start = _datetime(date_from, "date_from")
        end = _datetime(date_to, "date_to", end_of_day=True)
        receipt = parse_dt(state["ticket"].received_at)
        if start > end or start < receipt - timedelta(days=90) or start > receipt:
            raise DraftToolInputError("search must start within 90 days before receipt and precede date_to")
        end = min(end, receipt)
        if amount_iqd is not None and (type(amount_iqd) is not int or not 0 <= amount_iqd <= 2**63 - 1):
            raise DraftToolInputError("amount_iqd must be a nonnegative signed 64-bit integer")
        q = select(TransactionRow).where(_involves(phone), _scope(state),
                                        TransactionRow.created_at.between(start, end))
        if amount_iqd is not None:
            tolerance = amount_iqd // 100
            q = q.where(TransactionRow.amount_iqd.between(
                max(0, amount_iqd - tolerance), min(2**63 - 1, amount_iqd + tolerance)))
        return self._transactions(q)

    def _transactions(self, statement):
        statement = statement.order_by(TransactionRow.created_at.desc(), TransactionRow.txn_ref).limit(10)
        with self._session() as session:
            return [_record(row) for row in session.scalars(statement)]

    def get_customer_recent_transactions(self, state: PipelineState, phone: str,
                                         days: int = 14) -> list[TxnRecord]:
        phone = _phone(state, phone)
        receipt = parse_dt(state["ticket"].received_at)
        start = receipt - timedelta(days=_days(days))
        return self._transactions(select(TransactionRow).where(
            _involves(phone), _scope(state), TransactionRow.created_at.between(start, receipt)))

    def get_customer_ticket_history(self, state: PipelineState, phone: str,
                                    days: int = 30) -> list[dict]:
        phone = _phone(state, phone)
        principal, _ = _phones(state)
        if principal and phone != principal:
            raise DraftToolInputError("ticket history is restricted to the current customer")
        ticket = state["ticket"]
        receipt = parse_dt(ticket.received_at)
        q = select(TicketRow.id, TicketRow.external_id, TicketRow.channel, TicketRow.customer_phone,
                   TicketRow.received_at, func.left(TicketRow.text, 2000).label("text")).where(
            _stored_phone(TicketRow.customer_phone) == phone,
            TicketRow.received_at >= receipt - timedelta(days=_days(days)),
            TicketRow.received_at < receipt, TicketRow.external_id != ticket.external_id)
        if ticket.id is not None:
            q = q.where(TicketRow.id != ticket.id)
        q = q.order_by(TicketRow.received_at.desc(), TicketRow.id.desc()).limit(10)
        with self._session() as session:
            return [dict(row) for row in session.execute(q).mappings()]

    def check_service_status(self, state: PipelineState, service: str, at_time: str) -> list[dict]:
        service = _string(service, "service", 64)
        when = _datetime(at_time, "at_time")
        receipt = parse_dt(state["ticket"].received_at)
        if not receipt - timedelta(days=90) <= when <= receipt:
            raise DraftToolInputError("at_time must be within 90 days before ticket receipt")
        q = select(IncidentRow.id, IncidentRow.service, IncidentRow.started_at, IncidentRow.ended_at,
                   func.left(IncidentRow.description, 2000).label("description")).where(
            IncidentRow.service == service, IncidentRow.started_at <= when,
            or_(IncidentRow.ended_at.is_(None), IncidentRow.ended_at >= when),
        ).order_by(IncidentRow.started_at.desc(), IncidentRow.id).limit(10)
        with self._session() as session:
            return [dict(row) for row in session.execute(q).mappings()]
