"""The Topic 06 pipeline as a LangGraph StateGraph (spec §6, §14). One node per stage."""
from __future__ import annotations

import asyncio
import logging
import math
from collections import Counter
from collections.abc import Sequence
from dataclasses import asdict, dataclass, field
from time import perf_counter
from typing import Any

from langgraph.graph import END, START, StateGraph
from langgraph.types import RetryPolicy

from app.llm import LLMUnavailable
from app.pipeline.contracts import Ticket, TicketOutcome
from app.pipeline.stage1_normalize.candidates import find_candidates
from app.pipeline.stage1_normalize.normalize import normalize
from app.pipeline.stage2_classify.base import Classifier, FieldExtractor
from app.pipeline.stage2_classify.cascade import combine
from app.pipeline.stage3_extract.extract import fill_gaps, finalize
from app.pipeline.stage4_lookup.lookup import TransactionRepo, match_transaction
from app.pipeline.stage5_decide.rules import decide, empty_ticket_decision, merge_reasons
from app.pipeline.stage6_draft.drafting import Drafter, NullDrafter
from app.pipeline.state import PipelineState
from app.taxonomy import Taxonomy

logger = logging.getLogger(__name__)
MODES = ("jev", "gemini", "cascade")
_NOT_RETRYABLE = (ValueError, TypeError, KeyError, AttributeError, AssertionError)


def _retryable(exc: BaseException) -> bool:
    return not isinstance(exc, _NOT_RETRYABLE)


def _default_retry() -> RetryPolicy:
    return RetryPolicy(max_attempts=3, initial_interval=0.5, retry_on=_retryable)


@dataclass
class PipelineDeps:
    mode: str
    taxonomy: Taxonomy
    txn_repo: TransactionRepo
    jev: Classifier | None = None
    gemini: Classifier | None = None
    gap_filler: FieldExtractor | None = None
    drafter: Drafter = field(default_factory=NullDrafter)
    t_gem: float = 0.66
    retry: RetryPolicy = field(default_factory=_default_retry)

    def __post_init__(self) -> None:
        if self.mode not in MODES:
            raise ValueError(f"mode must be one of {MODES}, got {self.mode!r}")
        if self.mode in ("jev", "cascade") and self.jev is None:
            raise ValueError(f"mode={self.mode} needs a Jev classifier")
        if self.mode in ("gemini", "cascade") and self.gemini is None:
            raise ValueError(f"mode={self.mode} needs a Gemini classifier")


class _Nodes:
    def __init__(self, deps: PipelineDeps) -> None:
        self.d = deps

    def _category(self, state: PipelineState):
        return self.d.taxonomy.get(state["classifier"].classification.category)

    async def prepare(self, state: PipelineState) -> dict[str, Any]:
        nt = normalize(state["ticket"])
        return {"nt": nt, "cands": find_candidates(nt.match_text), "started_at": perf_counter(),
                "degraded": False}

    def route_after_prepare(self, state: PipelineState) -> str:
        if not state["ticket"].text.strip():
            return "escalate_empty"
        return "gemini_classify" if self.d.mode == "gemini" else "jev_classify"

    async def escalate_empty(self, state: PipelineState) -> dict[str, Any]:
        return {"decision": empty_ticket_decision(self.d.taxonomy.get("other")),
                "finished_at": perf_counter()}

    async def jev_classify(self, state: PipelineState) -> dict[str, Any]:
        try:
            out = await self.d.jev.classify(state["nt"], state["cands"])
        except Exception:
            if self.d.mode != "cascade":
                raise
            logger.warning("Jev failed for %s; using Gemini", state["ticket"].external_id,
                           exc_info=True)
            return {"jev": None, "degraded": True}
        update: dict[str, Any] = {"jev": out, "cost_usd": out.cost_usd}
        if self.d.mode == "jev" or not out.classification.uncertain:
            update["classifier"] = out
        return update

    def route_after_jev(self, state: PipelineState) -> str:
        return "extract" if state.get("classifier") is not None else "gemini_classify"

    async def gemini_classify(self, state: PipelineState) -> dict[str, Any]:
        jev_out = state.get("jev")
        try:
            gem = await self.d.gemini.classify(state["nt"], state["cands"])
        except LLMUnavailable:
            if jev_out is None:
                raise
            gem = None
        final = gem if self.d.mode == "gemini" else combine(jev_out, gem, t_gem=self.d.t_gem)
        return {"classifier": final, "cost_usd": gem.cost_usd if gem else 0.0}

    async def extract(self, state: PipelineState) -> dict[str, Any]:
        nt = state["nt"]
        extracted = finalize(state["classifier"].picks, state["cands"], nt)
        extracted, cost = await fill_gaps(
            extracted, nt, self._category(state).required_fields, self.d.gap_filler
        )
        return {"extracted": extracted, "cost_usd": cost}

    async def lookup(self, state: PipelineState) -> dict[str, Any]:
        t = state["ticket"]
        result = await asyncio.to_thread(
            match_transaction, self._category(state), state["extracted"],
            customer_phone=t.customer_phone, received_at=t.received_at, repo=self.d.txn_repo,
        )
        return {"lookup": result}

    async def decide(self, state: PipelineState) -> dict[str, Any]:
        return {"decision": decide(category=self._category(state), classifier=state["classifier"],
                                   extracted=state["extracted"], lookup=state["lookup"])}

    async def draft(self, state: PipelineState) -> dict[str, Any]:
        result = await self.d.drafter.draft(state)
        return {"draft": result, "decision": merge_reasons(state["decision"], result.reasons),
                "cost_usd": result.cost_usd, "finished_at": perf_counter()}


def build_graph(deps: PipelineDeps):
    n = _Nodes(deps)
    b = StateGraph(PipelineState)
    b.add_node("prepare", n.prepare)
    b.add_node("escalate_empty", n.escalate_empty)
    b.add_node("jev_classify", n.jev_classify,
               retry_policy=deps.retry if deps.mode == "jev" else None)
    b.add_node("gemini_classify", n.gemini_classify, retry_policy=deps.retry)
    b.add_node("extract", n.extract, retry_policy=deps.retry)
    b.add_node("lookup", n.lookup)
    b.add_node("decide", n.decide)
    b.add_node("draft", n.draft, retry_policy=deps.retry)
    b.add_edge(START, "prepare")
    b.add_conditional_edges("prepare", n.route_after_prepare,
                            ["escalate_empty", "jev_classify", "gemini_classify"])
    b.add_conditional_edges("jev_classify", n.route_after_jev, ["extract", "gemini_classify"])
    b.add_edge("gemini_classify", "extract")
    b.add_edge("extract", "lookup")
    b.add_edge("lookup", "decide")
    b.add_edge("decide", "draft")
    b.add_edge("draft", END)
    b.add_edge("escalate_empty", END)
    return b.compile()


def outcome_from_state(state: PipelineState) -> TicketOutcome:
    decision = state["decision"]
    started, finished = state.get("started_at"), state.get("finished_at")
    latency = int((finished - started) * 1000) if started is not None and finished is not None else 0
    return TicketOutcome(
        ticket=state["ticket"],
        status="escalated" if decision.escalated else "pending_review",
        classifier=state.get("classifier"),
        extracted=state.get("extracted", {}),
        lookup=state.get("lookup"),
        decision=decision,
        draft=state.get("draft"),
        latency_ms=latency,
        cost_usd=round(state.get("cost_usd", 0.0), 6),
    )


@dataclass(frozen=True)
class RunSummary:
    total: int
    by_status: dict[str, int]
    by_category: dict[str, int]
    by_team: dict[str, int]
    by_priority: dict[str, int]
    escalation_reasons: dict[str, int]
    classifier_paths: dict[str, int]
    fallback_rate: float
    degraded: bool
    failed_ids: list[str]
    latency_p50_ms: int
    latency_p95_ms: int
    total_cost_usd: float
    cost_per_ticket_usd: float

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def _percentile(values: Sequence[int], pct: float) -> int:
    if not values:
        return 0
    ordered = sorted(values)
    return int(ordered[max(0, math.ceil(pct / 100 * len(ordered)) - 1)])


def summarize(outcomes: Sequence[TicketOutcome]) -> RunSummary:
    ok = [o for o in outcomes if o.status != "failed"]
    classified = [o for o in ok if o.classifier is not None]
    decided = [o for o in ok if o.decision is not None]
    paths = Counter(o.classifier.path for o in classified)
    fallback = paths["gemini_fallback"] + paths["disagreement"]
    total_cost = round(sum(o.cost_usd for o in outcomes), 6)
    latencies = [o.latency_ms for o in ok]
    return RunSummary(
        total=len(outcomes),
        by_status=dict(Counter(o.status for o in outcomes)),
        by_category=dict(Counter(o.classifier.classification.category for o in classified)),
        by_team=dict(Counter(o.decision.team for o in decided)),
        by_priority=dict(Counter(o.decision.priority for o in decided)),
        escalation_reasons=dict(Counter(r for o in decided for r in o.decision.reasons)),
        classifier_paths=dict(paths),
        fallback_rate=round(fallback / len(classified), 4) if classified else 0.0,
        degraded=any(o.classifier.degraded for o in classified),
        failed_ids=[o.ticket.external_id for o in outcomes if o.status == "failed"],
        latency_p50_ms=_percentile(latencies, 50),
        latency_p95_ms=_percentile(latencies, 95),
        total_cost_usd=total_cost,
        cost_per_ticket_usd=round(total_cost / len(outcomes), 6) if outcomes else 0.0,
    )


async def run_batch(graph: Any, tickets: Sequence[Ticket], *,
                    concurrency: int) -> tuple[list[TicketOutcome], RunSummary]:
    if not tickets:
        return [], summarize([])
    results = await graph.abatch(
        [{"ticket": t} for t in tickets],
        config={"max_concurrency": concurrency},
        return_exceptions=True,
    )
    outcomes = [
        TicketOutcome(ticket=t, status="failed", error=f"{type(r).__name__}: {r}")
        if isinstance(r, BaseException) else outcome_from_state(r)
        for t, r in zip(tickets, results, strict=True)
    ]
    return outcomes, summarize(outcomes)
