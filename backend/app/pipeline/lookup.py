"""Match extracted details to a mock ZainCash transaction (spec §6.4)."""
from __future__ import annotations

from collections.abc import Iterable
from datetime import date, datetime, timedelta, timezone
from typing import Any, Protocol

from app.pipeline.contracts import ExtractedField, LookupResult, TxnRecord
from app.taxonomy import Category

AMOUNT_TOLERANCE = 0.01
DATE_TOLERANCE_DAYS = 3
DEFAULT_WINDOW_DAYS = 14
BAGHDAD = timezone(timedelta(hours=3))


class TransactionRepo(Protocol):
    def get_by_ref(self, txn_ref: str) -> TxnRecord | None: ...

    def search(self, *, phone: str, amount_min: int | None, amount_max: int | None,
               start: datetime, end: datetime, limit: int = 10) -> list[TxnRecord]: ...


def parse_dt(value: Any) -> datetime:
    dt = value if isinstance(value, datetime) else datetime.fromisoformat(str(value).replace("Z", "+00:00"))
    return dt if dt.tzinfo else dt.replace(tzinfo=BAGHDAD)


def txn_from_dict(d: dict[str, Any]) -> TxnRecord:
    return TxnRecord(
        txn_ref=str(d["txn_ref"]), sender_phone=str(d["sender_phone"]),
        receiver_phone=d.get("receiver_phone"), receiver_name=d.get("receiver_name"),
        amount_iqd=int(d["amount_iqd"]), type=str(d["type"]), status=str(d["status"]),
        created_at=parse_dt(d["created_at"]), biller=d.get("biller"), agent_id=d.get("agent_id"),
        failure_reason=d.get("failure_reason"),
    )


class InMemoryTransactionRepo:
    def __init__(self, records: Iterable[TxnRecord]) -> None:
        self._records = list(records)
        self._by_ref = {r.txn_ref: r for r in self._records}

    def get_by_ref(self, txn_ref: str) -> TxnRecord | None:
        return self._by_ref.get(txn_ref)

    def search(self, *, phone, amount_min, amount_max, start, end, limit=10):
        hits = [
            r for r in self._records
            if phone in (r.sender_phone, r.receiver_phone)
            and start <= r.created_at <= end
            and (amount_min is None or r.amount_iqd >= amount_min)
            and (amount_max is None or r.amount_iqd <= amount_max)
        ]
        return sorted(hits, key=lambda r: r.created_at, reverse=True)[:limit]


def _iqd_amount(field: ExtractedField) -> int | None:
    if field.value is None or field.currency not in (None, "IQD"):
        return None
    return int(field.value)


def _as_date(field: ExtractedField) -> date | None:
    return date.fromisoformat(str(field.value)) if field.value else None


def match_transaction(category: Category, extracted: dict[str, ExtractedField], *,
                      customer_phone: str | None, received_at: datetime,
                      repo: TransactionRepo) -> LookupResult:
    if not category.needs_transaction:
        return LookupResult("not_applicable")
    amount = _iqd_amount(extracted["amount"])
    when = _as_date(extracted["date"])
    ref = extracted["txn_ref"].value
    if ref:
        txn = repo.get_by_ref(str(ref))
        if txn is None:
            return LookupResult("not_found")
        if amount is not None and abs(txn.amount_iqd - amount) > AMOUNT_TOLERANCE * txn.amount_iqd:
            return LookupResult("amount_mismatch", txn, 1)
        if when is not None and abs((txn.created_at.date() - when).days) > DATE_TOLERANCE_DAYS:
            return LookupResult("date_mismatch", txn, 1)
        return LookupResult("matched", txn, 1)
    counterpart = extracted["phone"].value
    phone = customer_phone or counterpart
    if not phone:
        return LookupResult("not_found")
    if when is not None:
        start = datetime.combine(when - timedelta(days=DATE_TOLERANCE_DAYS), datetime.min.time(), BAGHDAD)
        end = datetime.combine(when + timedelta(days=DATE_TOLERANCE_DAYS), datetime.max.time(), BAGHDAD)
    else:
        start, end = received_at - timedelta(days=DEFAULT_WINDOW_DAYS), received_at
    tol = int(amount * AMOUNT_TOLERANCE) if amount is not None else 0
    hits = repo.search(
        phone=str(phone),
        amount_min=amount - tol if amount is not None else None,
        amount_max=amount + tol if amount is not None else None,
        start=start, end=end,
    )
    if len(hits) > 1 and counterpart and customer_phone:
        narrowed = [h for h in hits if counterpart in (h.sender_phone, h.receiver_phone)]
        hits = narrowed or hits
    if not hits:
        return LookupResult("not_found")
    if len(hits) > 1:
        return LookupResult("ambiguous", None, len(hits))
    return LookupResult("matched", hits[0], 1)
