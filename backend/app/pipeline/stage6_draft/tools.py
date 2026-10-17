"""Eight async tools sharing a per-ticket execution guard; no outer agent here."""
from __future__ import annotations

import asyncio
from copy import deepcopy
from dataclasses import asdict, is_dataclass
from datetime import datetime
from itertools import islice
from math import isfinite
from time import perf_counter
from typing import Annotated

from langchain_core.tools import BaseTool, tool
from pydantic import BaseModel, ConfigDict, Field, StringConstraints, ValidationError

from app.kb.service import KnowledgeExecutionError, KnowledgeService
from app.pipeline.stage5_decide.rules import REASON_TEXT
from app.pipeline.stage6_draft.context import (
    DraftAlreadySubmitted,
    DraftContext,
    DraftSubmission,
    DraftToolInputError,
    DraftToolLimit,
    Note,
    Reference,
)
from app.pipeline.stage6_draft.investigation import SqlInvestigationRepo

Phone = Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=32)]
DateText = Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=40)]


class _Input(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True)


class _Lookup(_Input):
    txn_ref: Reference = Field(description="Reference from this ticket, confirmed match, or its investigation results")


class _Search(_Input):
    phone: Phone = Field(description="Ticket customer's or verified counterpart's phone")
    date_from: DateText = Field(description="ISO date/datetime within 90 days before receipt")
    date_to: DateText = Field(description="ISO date/datetime; upper bound capped at ticket receipt")
    amount_iqd: int | None = Field(default=None, ge=0, le=2**63 - 1, description="IQD amount; +/-1% tolerance")


class _Recent(_Input):
    phone: Phone
    days: int = Field(default=14, ge=1, le=90, description="Lookback from ticket receipt, not the current clock")


class _History(_Recent):
    days: int = Field(default=30, ge=1, le=90, description="Prior contacts only, excluding the current ticket")


class _Service(_Input):
    service: Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=64)]
    at_time: DateText = Field(description="ISO date/datetime within 90 days before receipt")


class _Knowledge(_Input):
    query: Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=2000)]
    category: Annotated[str, StringConstraints(min_length=1, max_length=64)] | None = Field(
        default=None, description="Configured taxonomy category ID; includes untagged general policies")
    k: int = Field(default=5, ge=1, le=10)


_REASONS = frozenset(REASON_TEXT) | {"kb_unavailable", "draft_timeout", "draft_tool_limit", "draft_not_submitted"}


class _Flag(_Input):
    reason: Annotated[str, StringConstraints(min_length=1, max_length=64)] = Field(
        json_schema_extra={"enum": sorted(_REASONS)}, description="Existing escalation reason ID")
    note: Note


def _json(value):
    if is_dataclass(value) and not isinstance(value, type):
        return _json(asdict(value))
    if isinstance(value, datetime):
        return value.isoformat()
    if isinstance(value, dict):
        return {key: _json(item) for key, item in value.items()}
    if isinstance(value, (tuple, list)):
        return [_json(item) for item in value]
    return value


def _bounded(value, budget=6000):
    """Keep JSON-shaped evidence while bounding arbitrary rejected arguments/results."""
    remaining = budget

    def visit(item, depth=0):
        nonlocal remaining
        if remaining <= 0 or depth > 5:
            return "…"
        if isinstance(item, dict):
            result = {}
            for key, child in islice(item.items(), 16):
                if remaining <= 0:
                    break
                key = str(key)[:64]
                remaining -= len(key) + 8
                result[key] = visit(child, depth + 1)
            return result
        if isinstance(item, (tuple, list)):
            result = []
            for child in item[:10]:
                if remaining <= 0:
                    break
                remaining -= 4
                result.append(visit(child, depth + 1))
            return result
        if isinstance(item, int) and item.bit_length() > 64:
            item = "[oversized integer]"
        if isinstance(item, float) and not isfinite(item):
            item = "[nonfinite number]"
        if item is None or isinstance(item, (bool, int, float)):
            remaining -= 32
            return item
        output = str(item)[:max(0, min(2000, remaining))]
        remaining -= len(output) + 4
        return output

    return visit(value)


def _error_cost(error):
    if hasattr(error, "cost_usd"):
        return error.cost_usd
    if isinstance(error, TimeoutError) and error.__cause__ is not None:
        return getattr(error.__cause__, "cost_usd", 0.0)
    return 0.0


def build_tools(context: DraftContext, knowledge: KnowledgeService,
                investigation: SqlInvestigationRepo) -> list[BaseTool]:
    """Bind eight tools to one context. Call tools asynchronously using ainvoke.

    JSON schemas advertise full validation, but actual Pydantic validation runs
    INSIDE the guard. This also traces invalid calls and gives terminal rejection
    precedence over input validation. Executed failures consume budget; guard
    rejections do not execute or mutate state. Exceptions propagate to Task 5.
    """

    def guarded(name, schema, description, operation, *, terminal=False):
        @tool(name, args_schema=schema.model_json_schema(), return_direct=terminal,
              description=description)
        async def invoke(**kwargs):
            async with context.lock:
                if context.submission is not None:
                    raise DraftAlreadySubmitted("A draft has already been submitted")
                if context.tool_count >= min(context.max_tool_calls, 6):
                    raise DraftToolLimit("Six-call drafting budget exhausted")
                context.tool_count += 1
                started, cost_before = perf_counter(), context.cost_usd
                entry = {"kind": "tool", "tool": name, "arguments": _bounded(kwargs)}
                try:
                    try:
                        args = schema.model_validate(kwargs)
                    except ValidationError as exc:
                        error = exc.errors(include_input=False, include_url=False)[0]
                        raise DraftToolInputError(f"{error['loc']}: {error['msg']}") from None
                    result = _json(await operation(args))
                    entry.update(status="ok", result=_bounded(result))
                    if name == "search_knowledge_base":
                        # Independent of returned mutable data, exact Passage snapshots.
                        entry["retrieved_passages"] = deepcopy(result)
                    if terminal:
                        entry["internal_note"] = context.submission.internal_note
                    return result
                except (Exception, asyncio.CancelledError) as exc:
                    entry.update(status="cancelled" if isinstance(exc, asyncio.CancelledError) else "error",
                                 error_type=exc.diagnostic_type if isinstance(exc, KnowledgeExecutionError) else type(exc).__name__,
                                 error=str(exc)[:500] or type(exc).__name__)
                    raise
                finally:
                    entry["duration_ms"] = round((perf_counter() - started) * 1000, 3)
                    entry["cost_usd"] = context.cost_usd - cost_before
                    context.trace.append(entry)

        return invoke

    async def lookup(args):
        return await asyncio.to_thread(investigation.lookup_transaction, context.state, args.txn_ref,
                                       known_refs=tuple(context.investigated_refs))

    async def search(args):
        records = await asyncio.to_thread(investigation.search_transactions, context.state,
                                          args.phone, args.amount_iqd, args.date_from, args.date_to)
        context.investigated_refs.update(r.txn_ref for r in records)
        return records

    async def recent(args):
        records = await asyncio.to_thread(investigation.get_customer_recent_transactions,
                                          context.state, args.phone, args.days)
        context.investigated_refs.update(r.txn_ref for r in records)
        return records

    async def history(args):
        return await asyncio.to_thread(investigation.get_customer_ticket_history,
                                       context.state, args.phone, args.days)

    async def status(args):
        return await asyncio.to_thread(investigation.check_service_status,
                                       context.state, args.service, args.at_time)

    async def retrieve(args):
        try:
            result = await knowledge.search(args.query, category=args.category, k=args.k)
        except (Exception, asyncio.CancelledError) as exc:
            context.cost_usd += _error_cost(exc)
            if isinstance(exc, ValueError):
                raise DraftToolInputError(str(exc)[:500]) from exc
            raise
        context.cost_usd += result.cost_usd
        context.retrieved.update((p.id, p) for p in result.passages)
        return result.passages

    async def flag(args):
        if args.reason not in _REASONS:
            raise DraftToolInputError("Unknown escalation reason")
        if args.reason not in context.reasons:
            context.reasons.append(args.reason)
        context.notes.append(args.note)
        return {"reason": args.reason, "note": args.note}

    async def submit(args):
        context.submission = args
        return args.model_dump(mode="json")

    return [
        guarded("lookup_transaction", _Lookup, "Exact ticket-scoped transaction lookup; does not confirm a match.", lookup),
        guarded("search_transactions", _Search, "Search at most 10 ticket-scoped transactions, with 1% amount tolerance.", search),
        guarded("get_customer_recent_transactions", _Recent, "Up to 10 transactions before ticket receipt; candidates only.", recent),
        guarded("get_customer_ticket_history", _History, "Up to 10 prior customer contacts; exclude current and future tickets.", history),
        guarded("check_service_status", _Service, "Up to 10 incidents overlapping the requested time, inclusive of boundaries.", status),
        guarded("search_knowledge_base", _Knowledge, "Find policy passages with stable citation IDs and record evidence snapshots.", retrieve),
        guarded("flag_for_human", _Flag, "Add an escalation reason and reviewer note; does not submit or terminate.", flag),
        guarded("submit_draft", DraftSubmission, "Submit one final Arabic reply; terminal. Grounding and language checks follow.", submit, terminal=True),
    ]
