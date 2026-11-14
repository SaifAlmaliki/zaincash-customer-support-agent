"""Aggregations of the AI call ledger for the dashboard (spec §4.6)."""
from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime, timedelta
from typing import Any

from sqlalchemy import Float, Text, and_, case, cast, exists, func, literal_column, select, tuple_
from sqlalchemy.orm import Session

from app.db.models import RunRow, TicketResultRow, TicketRow
from app.telemetry.calls import PROCESSES, UNATTRIBUTED_PROCESSES
from app.telemetry.db_models import AiCallRow

DEFAULT_DAYS = 7
DRAFT_MS = cast(cast(literal_column(
    "jsonb_path_query_first(ticket_results.agent_trace, '$[*] ? (@.kind == \"draft\").duration_ms')"
), Text), Float)


@dataclass(frozen=True)
class UsageFilter:
    start: datetime
    end: datetime
    process: str | None = None
    provider: str | None = None
    model: str | None = None
    run_id: int | None = None


def usage_filter(from_: datetime | None, to: datetime | None, process: str | None, model: str | None,
                 run_id: int | None, *, now: datetime | None = None) -> UsageFilter:
    end = to or now or datetime.now(UTC)
    start = from_ or end - timedelta(days=DEFAULT_DAYS)
    if process is not None and process not in PROCESSES:
        raise ValueError("unknown process")
    provider = name = None
    if model:
        provider, _, name = model.partition(":")
        if not provider or not name:
            raise ValueError("model must be provider:model")
    return UsageFilter(start, end, process, provider, name, run_id)


def _call_conditions(f: UsageFilter) -> list:
    conditions = [AiCallRow.started_at >= f.start, AiCallRow.started_at < f.end]
    if f.process:
        conditions.append(AiCallRow.process == f.process)
    if f.provider:
        conditions += [AiCallRow.provider == f.provider, AiCallRow.model == f.model]
    if f.run_id is not None:
        conditions.append(AiCallRow.run_id == f.run_id)
    return conditions


def _p(fraction: float, column):
    return func.percentile_cont(fraction).within_group(column)


def _ratio(a: float, b: float) -> float | None:
    return a / b if b else None


def _groups(session: Session, conditions: list, keys: list, total_cost: float) -> list[dict[str, Any]]:
    errors = func.sum(case((AiCallRow.status == "error", 1), else_=0))
    rows = session.execute(select(
        *keys, func.count(), func.coalesce(func.sum(AiCallRow.cost_usd), 0.0), errors,
        _p(0.5, AiCallRow.latency_ms), _p(0.95, AiCallRow.latency_ms),
        func.coalesce(func.sum(AiCallRow.input_tokens), 0), func.coalesce(func.sum(AiCallRow.output_tokens), 0),
    ).where(*conditions).group_by(*keys).order_by(func.sum(AiCallRow.cost_usd).desc())).all()
    sources: dict[tuple, dict[str, int]] = {}
    for row in session.execute(select(*keys, AiCallRow.cost_source, func.count())
                               .where(*conditions).group_by(*keys, AiCallRow.cost_source)).all():
        sources.setdefault(tuple(row[:len(keys)]), {})[row[-2]] = row[-1]
    out = []
    for row in rows:
        key = tuple(row[:len(keys)])
        calls, cost, errs, p50, p95, tokens_in, tokens_out = row[len(keys):]
        out.append({"key": key, "calls": calls, "cost_usd": float(cost),
                    "cost_share": _ratio(float(cost), total_cost), "cost_per_call": _ratio(float(cost), calls),
                    "latency_p50_ms": p50, "latency_p95_ms": p95, "error_rate": _ratio(errs, calls),
                    "input_tokens": int(tokens_in), "output_tokens": int(tokens_out),
                    "cost_sources": sources.get(key, {})})
    return out


def _by_process(session, conditions, total):
    return [g | {"key": g["key"][0], "process": g["key"][0]}
            for g in _groups(session, conditions, [AiCallRow.process], total)]


def _by_model(session, conditions, total):
    groups = _groups(session, conditions, [AiCallRow.provider, AiCallRow.model, AiCallRow.locality], total)
    served: dict[tuple, list[str]] = {}
    for provider, model, process in session.execute(
            select(AiCallRow.provider, AiCallRow.model, AiCallRow.process).where(*conditions).distinct()):
        served.setdefault((provider, model), []).append(process)
    return [g | {"key": f"{g['key'][0]}:{g['key'][1]}", "provider": g["key"][0], "model": g["key"][1],
                 "locality": g["key"][2], "processes": sorted(served.get(g["key"][:2], []))} for g in groups]


def _time_ref():
    return func.coalesce(TicketResultRow.processed_at, RunRow.started_at)


def _ticket_query(f: UsageFilter):
    query = (select(TicketResultRow, TicketRow, RunRow.started_at)
             .join(TicketRow, TicketRow.id == TicketResultRow.ticket_id)
             .join(RunRow, RunRow.id == TicketResultRow.run_id)
             .where(_time_ref() >= f.start, _time_ref() < f.end, TicketResultRow.status != "processing"))
    if f.run_id is not None:
        query = query.where(TicketResultRow.run_id == f.run_id)
    if f.process or f.provider:
        match = [AiCallRow.run_id == TicketResultRow.run_id, AiCallRow.ticket_id == TicketResultRow.ticket_id]
        if f.process:
            match.append(AiCallRow.process == f.process)
        if f.provider:
            match += [AiCallRow.provider == f.provider, AiCallRow.model == f.model]
        query = query.where(exists(select(AiCallRow.id).where(*match)))
    return query


def _intake_totals():
    return (select(AiCallRow.run_id, AiCallRow.ticket_id,
                   func.sum(case((AiCallRow.process == "intake", AiCallRow.cost_usd), else_=0.0)).label("intake_cost"),
                   func.sum(case((AiCallRow.process == "intake", AiCallRow.latency_ms), else_=0)).label("intake_ms"),
                   func.count().label("calls"),
                   func.sum(case((AiCallRow.status == "error", 1), else_=0)).label("errors"))
            .group_by(AiCallRow.run_id, AiCallRow.ticket_id).subquery())


def _ticket_stats(session: Session, f: UsageFilter) -> dict[str, Any]:
    totals = _intake_totals()
    base = _ticket_query(f).with_only_columns(
        TicketResultRow.latency_ms.label("ai_ms"), DRAFT_MS.label("draft_ms"),
        (TicketResultRow.cost_usd + func.coalesce(totals.c.intake_cost, 0.0)).label("total_cost"),
    ).outerjoin(totals, and_(totals.c.run_id == TicketResultRow.run_id,
                             totals.c.ticket_id == TicketResultRow.ticket_id)).subquery()
    row = session.execute(select(
        func.count(), func.avg(base.c.total_cost), _p(0.95, base.c.total_cost),
        _p(0.5, base.c.ai_ms), _p(0.95, base.c.ai_ms), _p(0.5, base.c.draft_ms), _p(0.95, base.c.draft_ms),
    )).one()
    keys = ("tickets", "cost_per_ticket_avg", "cost_per_ticket_p95", "ai_time_p50_ms", "ai_time_p95_ms",
            "draft_time_p50_ms", "draft_time_p95_ms")
    return {k: (float(v) if v is not None and k != "tickets" else v) for k, v in zip(keys, row, strict=True)}


def summary(session: Session, f: UsageFilter) -> dict[str, Any]:
    conditions = _call_conditions(f)
    calls, cost, errors, unknown = session.execute(select(
        func.count(), func.coalesce(func.sum(AiCallRow.cost_usd), 0.0),
        func.coalesce(func.sum(case((AiCallRow.status == "error", 1), else_=0)), 0),
        func.coalesce(func.sum(case((AiCallRow.cost_source == "unknown", 1), else_=0)), 0),
    ).where(*conditions)).one()
    cost = float(cost)
    day = func.date_trunc("day", func.timezone("Asia/Baghdad", AiCallRow.started_at))
    daily = [{"date": d.date().isoformat(), "calls": n, "cost_usd": float(c), "errors": e, "latency_p95_ms": p95}
             for d, n, c, e, p95 in session.execute(select(
                 day, func.count(), func.sum(AiCallRow.cost_usd),
                 func.sum(case((AiCallRow.status == "error", 1), else_=0)), _p(0.95, AiCallRow.latency_ms),
             ).where(*conditions).group_by(day).order_by(day)).all()]
    unattributed_conditions = [*conditions, AiCallRow.process.in_(UNATTRIBUTED_PROCESSES)]
    unattributed = _by_process(session, unattributed_conditions, cost)
    return {
        "period": {"from": f.start.isoformat(), "to": f.end.isoformat()},
        "totals": {"cost_usd": cost, "calls": calls, "errors": errors, "error_rate": _ratio(errors, calls),
                   "unknown_cost_calls": unknown, **_ticket_stats(session, f)},
        "by_process": _by_process(session, conditions, cost),
        "by_model": _by_model(session, conditions, cost),
        "daily": daily,
        "unattributed": {"cost_usd": sum(g["cost_usd"] for g in unattributed),
                         "calls": sum(g["calls"] for g in unattributed), "by_process": unattributed},
    }


def _ticket_rows(session: Session, rows: list) -> list[dict[str, Any]]:
    if not rows:
        return []
    pairs = [(result.run_id, result.ticket_id) for result, _ticket, _started in rows]
    per_process: dict[tuple, dict[str, float]] = {}
    stats: dict[tuple, dict[str, float]] = {}
    for run_id, ticket_id, process, cost, latency, n, errors in session.execute(select(
            AiCallRow.run_id, AiCallRow.ticket_id, AiCallRow.process, func.sum(AiCallRow.cost_usd),
            func.sum(AiCallRow.latency_ms), func.count(), func.sum(case((AiCallRow.status == "error", 1), else_=0)),
    ).where(tuple_(AiCallRow.run_id, AiCallRow.ticket_id).in_(pairs))
            .group_by(AiCallRow.run_id, AiCallRow.ticket_id, AiCallRow.process)).all():
        per_process.setdefault((run_id, ticket_id), {})[process] = float(cost)
        s = stats.setdefault((run_id, ticket_id), {"calls": 0, "errors": 0, "intake_ms": 0})
        s["calls"] += n
        s["errors"] += errors
        if process == "intake":
            s["intake_ms"] = int(latency)
    draft = dict(session.execute(select(TicketResultRow.id, DRAFT_MS)
                                 .where(TicketResultRow.id.in_([r.id for r, _, _ in rows]))).all())
    items = []
    for result, ticket, _started in rows:
        key = (result.run_id, result.ticket_id)
        costs = per_process.get(key, {})
        s = stats.get(key, {"calls": 0, "errors": 0, "intake_ms": 0})
        intake_cost = costs.get("intake", 0.0)
        items.append({
            "result_id": result.id, "ticket_id": ticket.id, "external_id": ticket.external_id,
            "run_id": result.run_id, "received_at": ticket.received_at.isoformat(),
            "processed_at": result.processed_at.isoformat() if result.processed_at else None,
            "status": result.status, "category": result.category, "cost_usd": result.cost_usd,
            "intake_cost_usd": intake_cost, "total_cost_usd": result.cost_usd + intake_cost,
            "cost_by_process": costs, "ai_time_ms": result.latency_ms,
            "draft_time_ms": draft.get(result.id), "intake_time_ms": s["intake_ms"],
            "calls": s["calls"], "errors": s["errors"], "detail_recorded": bool(costs),
        })
    return items


def ticket_page(session: Session, f: UsageFilter, *, sort: str, limit: int, offset: int) -> dict[str, Any]:
    query = _ticket_query(f)
    total = session.scalar(select(func.count()).select_from(query.subquery()))
    if sort == "cost":
        totals = _intake_totals()
        query = query.outerjoin(totals, and_(totals.c.run_id == TicketResultRow.run_id,
                                             totals.c.ticket_id == TicketResultRow.ticket_id)).order_by(
            (TicketResultRow.cost_usd + func.coalesce(totals.c.intake_cost, 0.0)).desc(), TicketResultRow.id)
    elif sort == "time":
        query = query.order_by(TicketResultRow.latency_ms.desc(), TicketResultRow.id)
    else:
        query = query.order_by(_time_ref().desc(), TicketResultRow.id.desc())
    rows = session.execute(query.limit(limit).offset(offset)).all()
    return {"items": _ticket_rows(session, rows), "total": total}


def _call_view(row: AiCallRow) -> dict[str, Any]:
    return {"id": row.id, "process": row.process, "provider": row.provider, "model": row.model,
            "locality": row.locality, "started_at": row.started_at.isoformat(), "latency_ms": row.latency_ms,
            "input_tokens": row.input_tokens, "output_tokens": row.output_tokens, "cost_usd": row.cost_usd,
            "cost_source": row.cost_source, "status": row.status, "error": row.error,
            "attempt": row.attempt, "detail": row.detail}


def ticket_calls(session: Session, result_id: int) -> dict[str, Any] | None:
    row = session.execute(select(TicketResultRow, TicketRow, RunRow.started_at)
                          .join(TicketRow, TicketRow.id == TicketResultRow.ticket_id)
                          .join(RunRow, RunRow.id == TicketResultRow.run_id)
                          .where(TicketResultRow.id == result_id)).first()
    if row is None:
        return None
    result = row[0]
    calls = session.scalars(select(AiCallRow).where(AiCallRow.run_id == result.run_id,
                                                    AiCallRow.ticket_id == result.ticket_id)
                            .order_by(AiCallRow.started_at, AiCallRow.id)).all()
    return {"result": _ticket_rows(session, [row])[0], "calls": [_call_view(c) for c in calls]}
