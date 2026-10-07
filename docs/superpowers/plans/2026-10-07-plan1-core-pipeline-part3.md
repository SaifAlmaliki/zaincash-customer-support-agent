# Plan 1, Part 3: The LangGraph pipeline, persistence and the CLI (Tasks 12–15)

> This continues `2026-10-07-plan1-core-pipeline.md` and `-part2.md`. Global Constraints and Review Focus apply. Commands run from `~/dev/zaincash-support/backend` unless a step says otherwise.

---

### Task 12: The pipeline graph and batch runner

**Files:**
- Create: `app/pipeline/state.py`, `app/pipeline/drafting.py`, `app/pipeline/graph.py`
- Test: `tests/test_graph.py`

**Interfaces:**
- Consumes:
  - from Task 3: `normalize`
  - from Task 4: `find_candidates`
  - from Task 6: `Classifier`, `FieldExtractor`, `LLMUnavailable`
  - from Task 8: `combine`
  - from Task 9: `finalize`, `fill_gaps`
  - from Task 10: `match_transaction`, `TransactionRepo`
  - from Task 11: `decide`, `merge_reasons`, `empty_ticket_decision`
- Produces:
  - `state.PipelineState`, a TypedDict. `cost_usd` is summed across nodes with `operator.add`.
  - `drafting.Drafter`, a protocol with `async draft(state) -> DraftResult`
  - `drafting.NullDrafter`
  - in `graph`:
    - `MODES = ("jev", "gemini", "cascade")`
    - `PipelineDeps`, a dataclass with fields `mode`, `taxonomy`, `txn_repo`, `jev`, `gemini`, `gap_filler`, `drafter`, `t_gem` and `retry`
    - `build_graph(deps) -> CompiledStateGraph`
    - `outcome_from_state(state) -> TicketOutcome`
    - `RunSummary`, with `.to_dict()`
    - `summarize(outcomes) -> RunSummary`
    - `async run_batch(graph, tickets, *, concurrency) -> tuple[list[TicketOutcome], RunSummary]`

The graph's nodes and edges:

| From | To |
|---|---|
| START | `prepare` |
| `prepare` | `escalate_empty`, `jev_classify` or `gemini_classify` (chosen by `route_after_prepare`) |
| `jev_classify` | `extract` or `gemini_classify` (chosen by `route_after_jev`) |
| `gemini_classify` | `extract` |
| `extract` | `lookup` |
| `lookup` | `decide` |
| `decide` | `draft` |
| `draft` | END |
| `escalate_empty` | END |

- [ ] **Step 1: Write `app/pipeline/state.py`**

Do not add `from __future__ import annotations` to this file. LangGraph reads these annotations at runtime to find the `cost_usd` reducer.

```python
import operator
from typing import Annotated, TypedDict

from app.pipeline.contracts import (
    Candidates, ClassifierOutput, Decision, DraftResult, ExtractedField, LookupResult,
    NormalizedTicket, Ticket,
)


class PipelineState(TypedDict, total=False):
    ticket: Ticket
    nt: NormalizedTicket
    cands: Candidates
    jev: ClassifierOutput | None
    classifier: ClassifierOutput
    extracted: dict[str, ExtractedField]
    lookup: LookupResult
    decision: Decision
    draft: DraftResult
    degraded: bool
    cost_usd: Annotated[float, operator.add]
    started_at: float
    finished_at: float
```

- [ ] **Step 2: Write `app/pipeline/drafting.py`**

```python
from __future__ import annotations

from typing import Protocol

from app.pipeline.contracts import DraftResult
from app.pipeline.state import PipelineState


class Drafter(Protocol):
    async def draft(self, state: PipelineState) -> DraftResult: ...


class NullDrafter:
    """Plan 1 drafter. It produces no draft and adds no escalation reasons. Plan 3 replaces it with the RAG agent."""

    async def draft(self, state: PipelineState) -> DraftResult:
        return DraftResult()
```

- [ ] **Step 3: Write the failing tests**

`tests/test_graph.py`:
```python
import pytest
from langgraph.types import RetryPolicy

from app.pipeline.classify.jev import JevClassifier
from app.pipeline.contracts import DraftResult
from app.pipeline.drafting import NullDrafter
from app.pipeline.graph import PipelineDeps, build_graph, run_batch
from app.pipeline.lookup import InMemoryTransactionRepo, txn_from_dict
from tests.fakes import FakeClassifier, FakeJevRunnable, make_output
from tests.helpers import make_ticket

REPO = InMemoryTransactionRepo([txn_from_dict({
    "txn_ref": "ZC2410000123", "sender_phone": "07809876543", "receiver_phone": "07701234567",
    "receiver_name": "علي", "amount_iqd": 50000, "type": "p2p", "status": "pending",
    "created_at": "2026-10-06T18:10:00+03:00",
})])
FAST_RETRY = RetryPolicy(max_attempts=2, initial_interval=0.01, jitter=False)


def _deps(tax, mode="jev", jev=None, gemini=None, drafter=None):
    return PipelineDeps(mode=mode, taxonomy=tax, txn_repo=REPO, jev=jev, gemini=gemini,
                        drafter=drafter or NullDrafter(), retry=FAST_RETRY)


async def _run(deps, tickets, concurrency=4):
    return await run_batch(build_graph(deps), tickets, concurrency=concurrency)


async def test_jev_mode_happy_path(tax):
    runnable = FakeJevRunnable(picks={"amount": ("50 الف", 0.9), "date": ("امس", 0.9),
                                      "txn_ref": ("ZC2410000123", 0.95)})
    jev = JevClassifier(runnable, tax, model_id="jev-1.13.0", t_jev=0.6, min_top_prob=0.6,
                        price_in_per_m=0.042, max_state_chars=6000)
    t = make_ticket("حولت ٥٠ الف امس رقم العملية ZC2410000123 وما وصلت",
                    customer_phone="07809876543")
    [o], summary = await _run(_deps(tax, jev=jev), [t])
    assert o.status == "pending_review", o.decision
    assert o.decision.team == "Payments Ops" and o.decision.priority == "P2"
    assert o.lookup.status == "matched" and o.extracted["amount"].value == 50000
    assert o.cost_usd > 0 and o.latency_ms >= 0
    assert summary.total == 1 and summary.by_status == {"pending_review": 1}


async def test_empty_ticket_escalates_without_model_calls(tax):
    jev = FakeClassifier(make_output())
    [o], _ = await _run(_deps(tax, jev=jev), [make_ticket("   ")])
    assert o.status == "escalated" and o.decision.reasons == ("empty_ticket",)
    assert jev.calls == 0


async def test_cascade_uncertain_jev_goes_to_gemini(tax):
    jev = FakeClassifier(make_output(confidence=0.3, uncertain=True, reasons=("low_confidence",)))
    gem = FakeClassifier(make_output("wrong_recipient", confidence=1.0, source="gemini", path="gemini"))
    [o], summary = await _run(_deps(tax, "cascade", jev, gem), [make_ticket("غلطت بالرقم")])
    assert gem.calls == 1
    assert o.classifier.path == "gemini_fallback"
    assert o.classifier.classification.category == "wrong_recipient"
    assert summary.fallback_rate == 1.0


async def test_cascade_confident_jev_skips_gemini(tax):
    jev, gem = FakeClassifier(make_output()), FakeClassifier(make_output(source="gemini"))
    await _run(_deps(tax, "cascade", jev, gem), [make_ticket("حولت وما وصلت")])
    assert gem.calls == 0


async def test_cascade_degrades_when_jev_fails(tax):
    jev = FakeClassifier(raises=RuntimeError("jev down"))
    gem = FakeClassifier(make_output(source="gemini", path="gemini"))
    [o], summary = await _run(_deps(tax, "cascade", jev, gem), [make_ticket("حولت وما وصلت")])
    assert o.classifier.degraded and summary.degraded


async def test_failed_ticket_does_not_stop_batch(tax):
    jev = FakeClassifier(make_output(), fail_for={"T-2"})
    tickets = [make_ticket("a", external_id=f"T-{i}") for i in range(1, 4)]
    outcomes, summary = await _run(_deps(tax, jev=jev), tickets)
    assert [o.status for o in outcomes][1] == "failed"
    assert "boom" in outcomes[1].error
    assert summary.failed_ids == ["T-2"] and summary.total == 3


async def test_concurrency_is_limited(tax):
    jev = FakeClassifier(make_output(), delay=0.02)
    tickets = [make_ticket("a", external_id=f"T-{i}") for i in range(6)]
    await _run(_deps(tax, jev=jev), tickets, concurrency=2)
    assert jev.max_inflight <= 2


async def test_drafter_reasons_escalate(tax):
    class Guarded:
        async def draft(self, state):
            return DraftResult(text="مرحبا", reasons=("draft_failed_guardrail",))

    jev = FakeClassifier(make_output("general_inquiry", priority="P4"))
    [o], summary = await _run(_deps(tax, jev=jev, drafter=Guarded()), [make_ticket("شكد العمولة")])
    assert o.status == "escalated" and o.draft.text == "مرحبا"
    assert summary.escalation_reasons == {"draft_failed_guardrail": 1}


def test_deps_validate_mode(tax):
    with pytest.raises(ValueError):
        PipelineDeps(mode="cascade", taxonomy=tax, txn_repo=REPO, jev=FakeClassifier(make_output()))
    with pytest.raises(ValueError):
        PipelineDeps(mode="fast", taxonomy=tax, txn_repo=REPO)


async def test_empty_batch(tax):
    outcomes, summary = await _run(_deps(tax, jev=FakeClassifier(make_output())), [])
    assert outcomes == [] and summary.total == 0
```

- [ ] **Step 4: Run the tests and confirm they fail**

Run: `uv run pytest tests/test_graph.py -v`

Expected: FAIL with `ModuleNotFoundError: app.pipeline.graph`.

- [ ] **Step 5: Implement `app/pipeline/graph.py`**

```python
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
from app.pipeline.candidates import find_candidates
from app.pipeline.classify.base import Classifier, FieldExtractor
from app.pipeline.classify.cascade import combine
from app.pipeline.contracts import Ticket, TicketOutcome
from app.pipeline.drafting import Drafter, NullDrafter
from app.pipeline.extract import fill_gaps, finalize
from app.pipeline.lookup import TransactionRepo, match_transaction
from app.pipeline.normalize import normalize
from app.pipeline.rules import decide, empty_ticket_decision, merge_reasons
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
```

- [ ] **Step 6: Run the tests and confirm they pass**

Run: `uv run pytest tests/test_graph.py -v`

Expected: 10 passed.

If `add_node` rejects `retry_policy=None`, add the `jev_classify` node with no keyword when the mode is not `jev`. If your installed langgraph uses the older keyword `retry=` instead of `retry_policy=`, check with `uv run python -c "import inspect, langgraph.graph as g; print(inspect.signature(g.StateGraph.add_node))"` and use whichever keyword it shows.

- [ ] **Step 7: Run the whole suite**

Run: `uv run pytest -q && uv run ruff check app tests`

Expected: everything passes.

- [ ] **Step 8: Commit**

```bash
cd .. && git add backend && git commit -m "feat(pipeline): LangGraph pipeline graph with cascade routing and batch runner"
```

---

### Task 13: Postgres, the ORM models, serialization and the repository

**Files:**
- Create: `docker-compose.yml`, `docker/db/init.sql`
- Create: `app/db/__init__.py` (empty), `app/db/models.py`, `app/db/session.py`, `app/db/repository.py`, `app/pipeline/serialize.py`
- Test: `tests/test_serialize.py` (unit), `tests/test_repository.py` (integration)

**Interfaces:**
- Consumes: `TicketOutcome`, `Ticket` and `TxnRecord` (Task 3), `RunSummary` (Task 12), `parse_dt` (Task 10)
- Produces:
  - in `serialize`:
    - `outcome_to_row(o) -> dict`, whose keys are the columns of `ticket_results` except `run_id`
    - `outcome_to_dict(o) -> dict`, which adds `external_id` and `text`
  - in `db.session`:
    - `make_engine(url)`
    - `make_sessionmaker(engine)`
    - `init_db(engine)`
    - `reset_db(engine)`
  - in `db.repository`:
    - `upsert_tickets(session, tickets, *, source, batch_id=None) -> list[Ticket]`, which returns the tickets with `id` set
    - `create_run(session, *, mode, prompt_version, model_ids) -> int`
    - `save_outcomes(session, run_id, outcomes) -> None`
    - `finish_run(session, run_id, summary, *, status="completed") -> None`
    - `load_transactions(session, records) -> int`
    - `load_incidents(session, rows) -> int`
    - `SqlTransactionRepo(session_factory)`, which implements `TransactionRepo`
- **Spec deviation:** the knowledge-base tables are left out here. Plan 3 uses `langchain-postgres` PGVector, which manages its own tables (spec §14). `init_db` still creates the `vector` extension.

- [ ] **Step 1: Write the Docker files (in the repo root)**

`docker-compose.yml`:
```yaml
services:
  db:
    image: pgvector/pgvector:pg16
    environment:
      POSTGRES_USER: support
      POSTGRES_PASSWORD: support
      POSTGRES_DB: support
    ports: ["5432:5432"]
    volumes:
      - pgdata:/var/lib/postgresql/data
      - ./docker/db/init.sql:/docker-entrypoint-initdb.d/init.sql:ro
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U support -d support"]
      interval: 5s
      timeout: 3s
      retries: 10
volumes:
  pgdata:
```

`docker/db/init.sql`:
```sql
CREATE DATABASE support_test;
```

Run: `cd .. && docker compose up -d db && docker compose ps`

Expected: `db` is listed as `healthy` after a few seconds.

- [ ] **Step 2: Write `app/pipeline/serialize.py` and its test**

`app/pipeline/serialize.py`:
```python
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
```

`tests/test_serialize.py`:
```python
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
```

Run: `cd backend && uv run pytest tests/test_serialize.py -v`

Expected: 2 passed.

- [ ] **Step 3: Write `app/db/models.py` and `app/db/session.py`**

`app/db/models.py`:
```python
from __future__ import annotations

from datetime import datetime

from sqlalchemy import (
    BigInteger, Boolean, DateTime, Float, ForeignKey, Integer, String, Text, UniqueConstraint, func,
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class TicketRow(Base):
    __tablename__ = "tickets"
    id: Mapped[int] = mapped_column(primary_key=True)
    external_id: Mapped[str] = mapped_column(String(128), unique=True)
    channel: Mapped[str] = mapped_column(String(32), default="app")
    customer_phone: Mapped[str | None] = mapped_column(String(32))
    text: Mapped[str] = mapped_column(Text)
    received_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    source: Mapped[str] = mapped_column(String(16))
    batch_id: Mapped[str | None] = mapped_column(String(64))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


class RunRow(Base):
    __tablename__ = "runs"
    id: Mapped[int] = mapped_column(primary_key=True)
    started_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    finished_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    mode: Mapped[str] = mapped_column(String(16))
    prompt_version: Mapped[str] = mapped_column(String(16))
    model_ids: Mapped[dict] = mapped_column(JSONB, default=dict)
    degraded: Mapped[bool] = mapped_column(Boolean, default=False)
    counts: Mapped[dict] = mapped_column(JSONB, default=dict)
    total_cost_usd: Mapped[float] = mapped_column(Float, default=0.0)
    status: Mapped[str] = mapped_column(String(16), default="running")


class TicketResultRow(Base):
    __tablename__ = "ticket_results"
    __table_args__ = (UniqueConstraint("run_id", "ticket_id", name="uq_result_run_ticket"),)
    id: Mapped[int] = mapped_column(primary_key=True)
    run_id: Mapped[int] = mapped_column(ForeignKey("runs.id", ondelete="CASCADE"))
    ticket_id: Mapped[int] = mapped_column(ForeignKey("tickets.id", ondelete="CASCADE"))
    category: Mapped[str | None] = mapped_column(String(64))
    category_confidence: Mapped[float | None] = mapped_column(Float)
    category_probs: Mapped[dict] = mapped_column(JSONB, default=dict)
    priority: Mapped[str | None] = mapped_column(String(4))
    priority_confidence: Mapped[float | None] = mapped_column(Float)
    flags: Mapped[dict] = mapped_column(JSONB, default=dict)
    classifier_path: Mapped[str | None] = mapped_column(String(32))
    extracted: Mapped[dict] = mapped_column(JSONB, default=dict)
    lookup_status: Mapped[str | None] = mapped_column(String(32))
    matched_txn_ref: Mapped[str | None] = mapped_column(String(32))
    team: Mapped[str | None] = mapped_column(String(64))
    escalated: Mapped[bool] = mapped_column(Boolean, default=False)
    escalation_reasons: Mapped[list] = mapped_column(JSONB, default=list)
    escalation_note: Mapped[str | None] = mapped_column(Text)
    draft_text: Mapped[str | None] = mapped_column(Text)
    citations: Mapped[list] = mapped_column(JSONB, default=list)
    agent_trace: Mapped[list] = mapped_column(JSONB, default=list)
    status: Mapped[str] = mapped_column(String(32))
    error: Mapped[str | None] = mapped_column(Text)
    latency_ms: Mapped[int] = mapped_column(Integer, default=0)
    cost_usd: Mapped[float] = mapped_column(Float, default=0.0)
    jev_model_version: Mapped[str | None] = mapped_column(String(32))
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )


class ReviewRow(Base):
    __tablename__ = "reviews"
    id: Mapped[int] = mapped_column(primary_key=True)
    result_id: Mapped[int] = mapped_column(ForeignKey("ticket_results.id", ondelete="CASCADE"))
    reviewer: Mapped[str] = mapped_column(String(64))
    action: Mapped[str] = mapped_column(String(16))
    final_text: Mapped[str | None] = mapped_column(Text)
    edit_distance: Mapped[int | None] = mapped_column(Integer)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


class TransactionRow(Base):
    __tablename__ = "transactions"
    txn_ref: Mapped[str] = mapped_column(String(32), primary_key=True)
    sender_phone: Mapped[str] = mapped_column(String(32), index=True)
    receiver_phone: Mapped[str | None] = mapped_column(String(32), index=True)
    receiver_name: Mapped[str | None] = mapped_column(String(128))
    amount_iqd: Mapped[int] = mapped_column(BigInteger)
    type: Mapped[str] = mapped_column(String(16))
    status: Mapped[str] = mapped_column(String(16))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), index=True)
    biller: Mapped[str | None] = mapped_column(String(64))
    agent_id: Mapped[str | None] = mapped_column(String(32))
    failure_reason: Mapped[str | None] = mapped_column(String(128))


class IncidentRow(Base):
    __tablename__ = "service_incidents"
    id: Mapped[str] = mapped_column(String(32), primary_key=True)
    service: Mapped[str] = mapped_column(String(64))
    started_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    ended_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    description: Mapped[str] = mapped_column(Text)
```

`app/db/session.py`:
```python
from __future__ import annotations

from sqlalchemy import Engine, create_engine, text
from sqlalchemy.orm import sessionmaker

from app.db.models import Base


def make_engine(url: str) -> Engine:
    return create_engine(url, pool_pre_ping=True)


def make_sessionmaker(engine: Engine) -> sessionmaker:
    return sessionmaker(engine, expire_on_commit=False)


def init_db(engine: Engine) -> None:
    with engine.begin() as conn:
        conn.execute(text("CREATE EXTENSION IF NOT EXISTS vector"))
    Base.metadata.create_all(engine)


def reset_db(engine: Engine) -> None:
    Base.metadata.drop_all(engine)
    init_db(engine)
```

- [ ] **Step 4: Write the failing integration tests**

`tests/test_repository.py`:
```python
from datetime import datetime, timedelta

import pytest
from sqlalchemy import func, select
from sqlalchemy.exc import OperationalError

from app.config import Settings
from app.db.models import RunRow, TicketResultRow, TicketRow
from app.db.repository import (
    SqlTransactionRepo, create_run, finish_run, load_incidents, load_transactions, save_outcomes,
    upsert_tickets,
)
from app.db.session import make_engine, make_sessionmaker, reset_db
from app.pipeline.contracts import Decision, TicketOutcome
from app.pipeline.graph import summarize
from app.pipeline.lookup import txn_from_dict
from tests.helpers import BAGHDAD, make_ticket

pytestmark = pytest.mark.integration


@pytest.fixture
def sf():
    engine = make_engine(Settings().test_database_url)
    try:
        reset_db(engine)
    except OperationalError:
        pytest.skip("Postgres is not running: docker compose up -d db")
    yield make_sessionmaker(engine)
    engine.dispose()


def _count(s, model):
    return s.scalar(select(func.count()).select_from(model))


def test_upsert_tickets_is_idempotent(sf):
    with sf() as s:
        a = upsert_tickets(s, [make_ticket("x", external_id="A"), make_ticket("y", external_id="B")],
                           source="dataset")
        b = upsert_tickets(s, [make_ticket("changed", external_id="A")], source="dataset")
        s.commit()
        assert a[0].id == b[0].id and a[0].id is not None
        assert _count(s, TicketRow) == 2


def test_rerun_is_idempotent(sf):
    with sf() as s:
        [t] = upsert_tickets(s, [make_ticket("x", external_id="A")], source="dataset")
        run_id = create_run(s, mode="jev", prompt_version="v1", model_ids={"jev": "jev-1.13.0"})
        first = TicketOutcome(ticket=t, status="pending_review",
                              decision=Decision("General Care", "P4", False, (), ""))
        second = TicketOutcome(ticket=t, status="escalated",
                               decision=Decision("General Care", "P4", True, ("low_confidence",), "n"))
        save_outcomes(s, run_id, [first])
        save_outcomes(s, run_id, [second])
        finish_run(s, run_id, summarize([second]))
        s.commit()
        assert _count(s, TicketResultRow) == 1
        assert s.scalar(select(TicketResultRow.status)) == "escalated"
        run = s.get(RunRow, run_id)
        assert run.status == "completed" and run.counts["total"] == 1


def test_sql_transaction_repo(sf):
    rec = txn_from_dict({"txn_ref": "ZC2410000123", "sender_phone": "07809876543",
                         "receiver_phone": "07701234567", "amount_iqd": 50000, "type": "p2p",
                         "status": "pending", "created_at": "2026-10-06T18:10:00+03:00"})
    with sf() as s:
        assert load_transactions(s, [rec, rec]) == 2  # second copy is an update, not a duplicate
        assert load_incidents(s, [{"id": "INC-01", "service": "bill_pay",
                                   "started_at": "2026-10-01T08:00:00+03:00",
                                   "description": "Electricity biller timeout"}]) == 1
        s.commit()
    repo = SqlTransactionRepo(sf)
    assert repo.get_by_ref("ZC2410000123").amount_iqd == 50000
    when = datetime(2026, 10, 6, 12, tzinfo=BAGHDAD)
    hits = repo.search(phone="07701234567", amount_min=49500, amount_max=50500,
                       start=when - timedelta(days=3), end=when + timedelta(days=3))
    assert [h.txn_ref for h in hits] == ["ZC2410000123"]
    assert repo.search(phone="07000000000", amount_min=None, amount_max=None,
                       start=when - timedelta(days=3), end=when + timedelta(days=3)) == []
```

Run: `uv run pytest tests/test_repository.py -v`

Expected: FAIL with `ModuleNotFoundError: app.db.repository`.

- [ ] **Step 5: Implement `app/db/repository.py`**

```python
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
from app.pipeline.lookup import parse_dt
from app.pipeline.serialize import outcome_to_row


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
```

- [ ] **Step 6: Run all the tests**

Run: `uv run pytest tests/test_repository.py tests/test_serialize.py -v`

Expected: 5 passed. If Docker isn't running, the repository tests are SKIPPED. In that case, start it with `docker compose up -d db` and run again; they must pass, not skip, before you commit.

- [ ] **Step 7: Commit**

```bash
cd .. && git add docker-compose.yml docker backend && git commit -m "feat(db): postgres schema, idempotent repository and outcome serialization"
```

---

### Task 14: Loading tickets, building the pipeline and the CLI

**Files:**
- Create: `app/ingest.py`, `app/pipeline/factory.py`, `app/cli.py`
- Create: `tests/fixtures/sample_tickets.jsonl`, `tests/fixtures/sample_transactions.jsonl`, `tests/fixtures/sample_incidents.jsonl`
- Test: `tests/test_ingest.py`, `tests/test_factory.py`, `tests/test_cli.py`

**Interfaces:**
- Consumes: everything from Tasks 1–13
- Produces:
  - in `ingest`:
    - `load_jsonl(path) -> list[dict]`
    - `load_tickets(path, *, now=None) -> list[Ticket]`
  - in `factory`:
    - `ConfigError`
    - `make_jev_client(settings)`
    - `make_gemini_llm(settings)`
    - `model_ids(settings, mode) -> dict`
    - `build_pipeline(settings, mode, txn_repo, *, jev_client=None, llm=None, drafter=None)`, which returns the compiled graph
  - in `cli`, the typer `app` with the commands `init-db`, `seed-db` and `run-batch`

- [ ] **Step 1: Write the fixtures**

`tests/fixtures/sample_tickets.jsonl` (one JSON object per line):
```json
{"external_id": "S-001", "text": "حولت ٥٠ الف لاخوي على رقم 07701234567 امس وانقطعت من رصيدي بس ما وصلتله. رقم العملية ZC2410000123", "channel": "app", "customer_phone": "07809876543", "received_at": "2026-10-07T09:30:00+03:00"}
{"external_id": "S-002", "text": "واحد اتصل بيه يكول انه موظف زين كاش وطلب الرمز اللي وصلني، انطيته وبعدها انسحب من حسابي 200 الف!! الحكوني", "channel": "whatsapp", "customer_phone": "07501112233", "received_at": "2026-10-07T10:05:00+03:00"}
{"external_id": "S-003", "text": "ma da ywselni el code mal ta2keed, ma agdar afta7 el 7isab", "channel": "app", "customer_phone": "07712223344", "received_at": "2026-10-07T11:00:00+03:00"}
{"external_id": "S-004", "text": "دفعت فاتورة الكهرباء 35,000 دينار يوم الخميس وطلعت ناجحة بس بعدها جاني اشعار انها ما مدفوعة", "channel": "app", "customer_phone": "07723334455", "received_at": "2026-10-07T12:15:00+03:00"}
{"external_id": "S-005", "text": "شكد عمولة التحويل لحساب بنكي؟", "channel": "whatsapp", "received_at": "2026-10-07T13:00:00+03:00"}
```

`tests/fixtures/sample_transactions.jsonl`:
```json
{"txn_ref": "ZC2410000123", "sender_phone": "07809876543", "receiver_phone": "07701234567", "receiver_name": "علي حسين", "amount_iqd": 50000, "type": "p2p", "status": "pending", "created_at": "2026-10-06T18:10:00+03:00"}
{"txn_ref": "ZC2410000456", "sender_phone": "07723334455", "receiver_phone": null, "receiver_name": null, "amount_iqd": 35000, "type": "bill", "biller": "electricity", "status": "completed", "created_at": "2026-10-01T12:00:00+03:00"}
{"txn_ref": "ZC2410000789", "sender_phone": "07501112233", "receiver_phone": "07901234567", "receiver_name": "مجهول", "amount_iqd": 200000, "type": "p2p", "status": "completed", "created_at": "2026-10-07T08:00:00+03:00"}
```

`tests/fixtures/sample_incidents.jsonl`:
```json
{"id": "INC-01", "service": "bill_pay", "started_at": "2026-10-01T08:00:00+03:00", "ended_at": "2026-10-01T16:00:00+03:00", "description": "Electricity biller confirmation timeout: payments marked successful in the app but not posted to the biller"}
```

- [ ] **Step 2: Write the failing tests**

`tests/test_ingest.py`:
```python
from datetime import datetime
from pathlib import Path

import pytest

from app.ingest import load_tickets
from tests.helpers import BAGHDAD

FIXTURES = Path(__file__).parent / "fixtures"
NOW = datetime(2026, 10, 7, 15, 0, tzinfo=BAGHDAD)


def test_jsonl_fixture_loads():
    tickets = load_tickets(FIXTURES / "sample_tickets.jsonl", now=NOW)
    assert [t.external_id for t in tickets] == ["S-001", "S-002", "S-003", "S-004", "S-005"]
    assert tickets[0].customer_phone == "07809876543"
    assert tickets[4].customer_phone is None and tickets[4].channel == "whatsapp"


def test_csv_with_bom_and_missing_columns(tmp_path):
    p = tmp_path / "batch.csv"
    p.write_bytes("\ufeffexternal_id,text\nC-1,حولت 50 الف وبطاقتي 5123456789012346\n".encode())
    [t] = load_tickets(p, now=NOW)
    assert t.external_id == "C-1" and t.channel == "app" and t.received_at == NOW
    assert "************2346" in t.text  # card masked before storage


def test_duplicate_external_ids_keep_first(tmp_path):
    p = tmp_path / "dup.jsonl"
    p.write_text('{"external_id": "X", "text": "first"}\n{"external_id": "X", "text": "second"}\n',
                 encoding="utf-8")
    [t] = load_tickets(p, now=NOW)
    assert t.text == "first"


def test_json_object_without_ids(tmp_path):
    p = tmp_path / "judges.json"
    p.write_text('{"tickets": [{"message": "مرحبا", "received_at": "2026-10-07T08:00:00"}]}',
                 encoding="utf-8")
    [t] = load_tickets(p, now=NOW)
    assert t.external_id == "judges-1" and t.text == "مرحبا"
    assert t.received_at == datetime(2026, 10, 7, 8, 0, tzinfo=BAGHDAD)


def test_unsupported_format(tmp_path):
    p = tmp_path / "x.txt"
    p.write_text("hi", encoding="utf-8")
    with pytest.raises(ValueError):
        load_tickets(p)
```

`tests/test_factory.py`:
```python
import pytest

from app.config import Settings
from app.pipeline.factory import ConfigError, build_pipeline, model_ids
from app.pipeline.lookup import InMemoryTransactionRepo
from tests.fakes import FakeJevRunnable, FakeStructuredLLM

REPO = InMemoryTransactionRepo([])


def _settings(**kw):
    return Settings(_env_file=None, google_api_key="", typesafe_api_key="", **kw)


def test_missing_keys_raise_config_error():
    with pytest.raises(ConfigError):
        build_pipeline(_settings(), "gemini", REPO)
    with pytest.raises(ConfigError):
        build_pipeline(_settings(), "jev", REPO)


def test_builds_with_injected_clients():
    for mode in ("jev", "gemini", "cascade"):
        graph = build_pipeline(_settings(), mode, REPO, jev_client=FakeJevRunnable(),
                               llm=FakeStructuredLLM([None]))
        assert "prepare" in graph.get_graph().nodes


def test_model_ids():
    s = _settings()
    assert model_ids(s, "jev") == {"jev": "jev-1.13.0", "gemini": "gemini-2.5-flash"}
    assert model_ids(s, "gemini") == {"gemini": "gemini-2.5-flash"}
```

`tests/test_cli.py`:
```python
import json
from pathlib import Path

from typer.testing import CliRunner

from app import cli
from app.pipeline import factory
from app.pipeline.graph import PipelineDeps, build_graph
from app.pipeline.lookup import InMemoryTransactionRepo
from app.taxonomy import load_taxonomy
from tests.fakes import FakeClassifier, make_output

FIXTURES = Path(__file__).parent / "fixtures"
runner = CliRunner()


def test_run_batch_no_db_writes_summary_and_out(monkeypatch, tmp_path):
    def fake_build(settings, mode, repo, **kw):
        assert isinstance(repo, InMemoryTransactionRepo)
        tax = load_taxonomy(settings.taxonomy_path)
        return build_graph(PipelineDeps(mode="jev", taxonomy=tax, txn_repo=repo,
                                        jev=FakeClassifier(make_output("general_inquiry", priority="P4"))))

    monkeypatch.setattr(factory, "build_pipeline", fake_build)
    out = tmp_path / "out.json"
    result = runner.invoke(cli.app, [
        "run-batch", str(FIXTURES / "sample_tickets.jsonl"), "--mode", "jev", "--no-db",
        "--transactions", str(FIXTURES / "sample_transactions.jsonl"), "--out", str(out), "--limit", "3",
    ])
    assert result.exit_code == 0, result.output
    assert json.loads(result.output)["total"] == 3
    rows = json.loads(out.read_text(encoding="utf-8"))
    assert [r["external_id"] for r in rows] == ["S-001", "S-002", "S-003"]


def test_config_error_exits_2(monkeypatch):
    def boom(*a, **kw):
        raise factory.ConfigError("TYPESAFE_API_KEY is required")

    monkeypatch.setattr(factory, "build_pipeline", boom)
    result = runner.invoke(cli.app, ["run-batch", str(FIXTURES / "sample_tickets.jsonl"),
                                     "--mode", "jev", "--no-db"])
    assert result.exit_code == 2 and "TYPESAFE_API_KEY" in result.output
```

- [ ] **Step 3: Run the tests and confirm they fail**

Run: `uv run pytest tests/test_ingest.py tests/test_factory.py tests/test_cli.py -v`

Expected: FAIL with `ModuleNotFoundError`.

- [ ] **Step 4: Implement `app/ingest.py`**

```python
"""Load judge/user ticket files: .jsonl, .json (a list or {"tickets": [...]}), and .csv (UTF-8 with or without a BOM)."""
from __future__ import annotations

import csv
import json
from datetime import datetime
from pathlib import Path
from typing import Any

from app.pipeline.contracts import Ticket
from app.pipeline.lookup import BAGHDAD, parse_dt
from app.pipeline.normalize import sanitize_for_storage


def load_jsonl(path: str | Path) -> list[dict[str, Any]]:
    lines = Path(path).read_text(encoding="utf-8-sig").splitlines()
    return [json.loads(line) for line in lines if line.strip()]


def _rows(path: Path) -> list[dict[str, Any]]:
    suffix = path.suffix.lower()
    if suffix == ".jsonl":
        return load_jsonl(path)
    if suffix == ".json":
        data = json.loads(path.read_text(encoding="utf-8-sig"))
        return data.get("tickets", []) if isinstance(data, dict) else list(data)
    if suffix == ".csv":
        with path.open(encoding="utf-8-sig", newline="") as f:
            return list(csv.DictReader(f))
    raise ValueError(f"unsupported ticket file type {suffix!r}; use .jsonl, .json or .csv")


def load_tickets(path: str | Path, *, now: datetime | None = None) -> list[Ticket]:
    path = Path(path)
    now = now or datetime.now(BAGHDAD)
    seen: set[str] = set()
    tickets: list[Ticket] = []
    for i, row in enumerate(_rows(path), start=1):
        external_id = str(row.get("external_id") or row.get("id") or f"{path.stem}-{i}").strip()
        if external_id in seen:
            continue
        seen.add(external_id)
        phone = str(row.get("customer_phone") or "").strip() or None
        tickets.append(Ticket(
            external_id=external_id,
            text=sanitize_for_storage(str(row.get("text") or row.get("message") or "")),
            received_at=parse_dt(row["received_at"]) if row.get("received_at") else now,
            channel=str(row.get("channel") or "app"),
            customer_phone=phone,
        ))
    return tickets
```

- [ ] **Step 5: Implement `app/pipeline/factory.py`**

```python
"""Wire settings into a compiled pipeline graph. This is the only place that builds real model clients."""
from __future__ import annotations

from typing import Any

from app.config import Settings
from app.llm import GeminiStructuredLLM, StructuredLLM
from app.pipeline.classify.gemini import GeminiClassifier, GeminiExtractor
from app.pipeline.classify.jev import JevClassifier
from app.pipeline.drafting import Drafter, NullDrafter
from app.pipeline.graph import MODES, PipelineDeps, build_graph
from app.pipeline.lookup import TransactionRepo
from app.taxonomy import load_taxonomy


class ConfigError(RuntimeError):
    """Missing or invalid configuration (for example, an API key)."""


def make_jev_client(settings: Settings) -> Any:
    from langchain_typesafe import TypeSafeClassifier

    return TypeSafeClassifier(model=settings.jev_model, api_key=settings.typesafe_api_key)


def make_gemini_llm(settings: Settings) -> GeminiStructuredLLM:
    return GeminiStructuredLLM(
        api_key=settings.google_api_key, model=settings.gemini_model,
        price_in_per_m=settings.price_gemini_flash_in, price_out_per_m=settings.price_gemini_flash_out,
    )


def model_ids(settings: Settings, mode: str) -> dict[str, str]:
    ids = {"jev": settings.jev_model} if mode != "gemini" else {}
    return ids | {"gemini": settings.gemini_model}


def build_pipeline(settings: Settings, mode: str, txn_repo: TransactionRepo, *,
                   jev_client: Any = None, llm: StructuredLLM | None = None,
                   drafter: Drafter | None = None):
    if mode not in MODES:
        raise ConfigError(f"unknown mode {mode!r}; choose one of {MODES}")
    taxonomy = load_taxonomy(settings.taxonomy_path)
    if llm is None and settings.google_api_key:
        llm = make_gemini_llm(settings)
    if mode in ("gemini", "cascade") and llm is None:
        raise ConfigError(f"GOOGLE_API_KEY is required for mode={mode}")
    if mode in ("jev", "cascade") and jev_client is None:
        if not settings.typesafe_api_key:
            raise ConfigError(f"TYPESAFE_API_KEY is required for mode={mode}")
        jev_client = make_jev_client(settings)
    jev = None
    if mode != "gemini":
        jev = JevClassifier(
            jev_client, taxonomy, model_id=settings.jev_model, t_jev=settings.t_jev,
            min_top_prob=settings.jev_min_top_prob, price_in_per_m=settings.price_jev_in,
            max_state_chars=settings.max_state_chars,
        )
    gemini = None
    if mode != "jev" and llm is not None:
        gemini = GeminiClassifier(llm, taxonomy, t_gem=settings.t_gem,
                                  max_state_chars=settings.max_state_chars)
    deps = PipelineDeps(
        mode=mode, taxonomy=taxonomy, txn_repo=txn_repo, jev=jev, gemini=gemini,
        gap_filler=GeminiExtractor(llm, max_state_chars=settings.max_state_chars) if llm else None,
        drafter=drafter or NullDrafter(), t_gem=settings.t_gem,
    )
    return build_graph(deps)
```

- [ ] **Step 6: Implement `app/cli.py`**

```python
"""`support` CLI: init-db, seed-db, run-batch. The same pipeline code is used by the API (Plan 4) and eval (Plan 2)."""
from __future__ import annotations

import asyncio
import json
from enum import Enum
from pathlib import Path

import typer

from app.config import Settings, get_settings
from app.db.repository import (
    SqlTransactionRepo, create_run, finish_run, load_incidents, load_transactions, save_outcomes,
    upsert_tickets,
)
from app.db.session import init_db, make_engine, make_sessionmaker
from app.ingest import load_jsonl, load_tickets
from app.pipeline import factory
from app.pipeline.contracts import Ticket
from app.pipeline.graph import run_batch
from app.pipeline.lookup import InMemoryTransactionRepo, txn_from_dict
from app.pipeline.prompts import PROMPT_VERSION
from app.pipeline.serialize import outcome_to_dict

app = typer.Typer(no_args_is_help=True, add_completion=False, help="ZainCash support pipeline")


class Mode(str, Enum):
    jev = "jev"
    gemini = "gemini"
    cascade = "cascade"


def _sessionmaker(settings: Settings):
    engine = make_engine(settings.database_url)
    init_db(engine)
    return make_sessionmaker(engine)


@app.command("init-db")
def init_db_cmd() -> None:
    """Create the database schema (idempotent)."""
    _sessionmaker(get_settings())
    typer.echo("database ready")


@app.command("seed-db")
def seed_db_cmd(
    transactions: Path = typer.Option(..., exists=True, dir_okay=False, help="transactions JSONL"),
    incidents: Path | None = typer.Option(None, exists=True, dir_okay=False, help="incidents JSONL"),
) -> None:
    """Load mock transactions (and optional service incidents) into Postgres."""
    sf = _sessionmaker(get_settings())
    with sf() as s:
        n = load_transactions(s, [txn_from_dict(r) for r in load_jsonl(transactions)])
        m = load_incidents(s, load_jsonl(incidents)) if incidents else 0
        s.commit()
    typer.echo(f"loaded {n} transactions and {m} incidents")


def _run_in_memory(settings: Settings, mode: str, tickets: list[Ticket],
                   transactions: Path | None):
    records = [txn_from_dict(r) for r in load_jsonl(transactions)] if transactions else []
    graph = factory.build_pipeline(settings, mode, InMemoryTransactionRepo(records))
    return asyncio.run(run_batch(graph, tickets, concurrency=settings.pipeline_concurrency))


def _run_with_db(settings: Settings, mode: str, tickets: list[Ticket]):
    sf = _sessionmaker(settings)
    graph = factory.build_pipeline(settings, mode, SqlTransactionRepo(sf))  # fail fast before writing
    with sf() as s:
        tickets = upsert_tickets(s, tickets, source="dataset")
        run_id = create_run(s, mode=mode, prompt_version=PROMPT_VERSION,
                            model_ids=factory.model_ids(settings, mode))
        s.commit()
    outcomes, summary = asyncio.run(
        run_batch(graph, tickets, concurrency=settings.pipeline_concurrency)
    )
    with sf() as s:
        save_outcomes(s, run_id, outcomes)
        finish_run(s, run_id, summary)
        s.commit()
    return outcomes, summary


@app.command("run-batch")
def run_batch_cmd(
    path: Path = typer.Argument(..., exists=True, dir_okay=False, help=".jsonl, .json or .csv"),
    mode: Mode = typer.Option(Mode.cascade, "--mode"),
    limit: int | None = typer.Option(None, "--limit", min=1),
    out: Path | None = typer.Option(None, "--out", help="write per-ticket results as JSON"),
    no_db: bool = typer.Option(False, "--no-db", help="run without Postgres"),
    transactions: Path | None = typer.Option(None, "--transactions", exists=True, dir_okay=False,
                                             help="transactions JSONL for --no-db runs"),
) -> None:
    """Run the pipeline over a batch of tickets and print the run summary."""
    settings = get_settings()
    tickets = load_tickets(path)[: limit or None]
    try:
        if no_db:
            outcomes, summary = _run_in_memory(settings, mode.value, tickets, transactions)
        else:
            outcomes, summary = _run_with_db(settings, mode.value, tickets)
    except factory.ConfigError as exc:
        typer.echo(f"Config error: {exc}", err=True)
        raise typer.Exit(code=2) from exc
    typer.echo(json.dumps(summary.to_dict(), ensure_ascii=False, indent=2))
    if out:
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps([outcome_to_dict(o) for o in outcomes], ensure_ascii=False,
                                  indent=2, default=str), encoding="utf-8")
```

- [ ] **Step 7: Run the tests and confirm they pass**

Run: `uv run pytest tests/test_ingest.py tests/test_factory.py tests/test_cli.py -v`

Expected: 10 passed. Typer's `CliRunner` mixes stderr into `result.output` by default, which `test_config_error_exits_2` relies on. If your typer version separates the streams, assert on `result.stderr` instead.

- [ ] **Step 8: Run the whole suite and lint, then commit**

Run: `uv run pytest -q && uv run ruff check app tests`

Expected: everything passes, with the integration tests running because Docker is up.

```bash
cd .. && git add backend && git commit -m "feat(cli): ticket ingestion, pipeline factory and support CLI"
```

---

### Task 15: Live end-to-end smoke run and quickstart

This task proves the pipeline works against the real Jev and Gemini APIs before Plan 2 builds the evaluation on top of it.

**Files:**
- Modify: `README.md` (add a Quickstart section under "Status")
- Modify: `.env` (local only, never committed). Copy it from `.env.example` and fill in `GOOGLE_API_KEY` and `TYPESAFE_API_KEY`.

- [ ] **Step 1: Run the Jev shape probe** (Task 6, Step 8) if you haven't yet. Fix any mismatches in both `jev.py` and `tests/fakes.py`, then re-run `uv run pytest -q`.

- [ ] **Step 2: Do an in-memory smoke run in each mode**

```bash
cd backend
for m in jev gemini cascade; do
  uv run support run-batch tests/fixtures/sample_tickets.jsonl --mode $m --no-db \
    --transactions tests/fixtures/sample_transactions.jsonl --out ../out/smoke-$m.json || exit 1
done
```

Expected for each mode:
- `total` is 5 and `failed_ids` is `[]`.
- In `out/smoke-cascade.json`:
  - S-001: `category` is `failed_transfer`, `lookup_status` is `matched`, and `extracted.amount.value` is `50000`.
  - S-002: escalated with `fraud_suspected`, priority `P1`.
  - S-005: `general_inquiry`, P4.

Record the actual results in your notes. If a fixture ticket is misclassified, that isn't a bug in this plan; prompt and threshold tuning happen in Plan 2, on the dev set only.

- [ ] **Step 3: Do a database-backed run**

```bash
uv run support seed-db --transactions tests/fixtures/sample_transactions.jsonl \
  --incidents tests/fixtures/sample_incidents.jsonl
uv run support run-batch tests/fixtures/sample_tickets.jsonl --mode cascade
uv run support run-batch tests/fixtures/sample_tickets.jsonl --mode cascade
docker compose exec db psql -U support -d support -c \
  "select r.id, r.status, count(t.id) from runs r join ticket_results t on t.run_id=r.id group by r.id;"
```

Expected: two runs, each `completed` with 5 results. The `tickets` table still has 5 rows (`select count(*) from tickets;` returns 5).

- [ ] **Step 4: Add the Quickstart to `README.md`**

Replace the "Status" section with:

````markdown
## Quickstart (WSL Ubuntu, Docker Engine, uv)

```bash
cp .env.example .env            # add GOOGLE_API_KEY and TYPESAFE_API_KEY
docker compose up -d db
cd backend && uv sync
uv run support seed-db --transactions tests/fixtures/sample_transactions.jsonl
uv run support run-batch tests/fixtures/sample_tickets.jsonl --mode cascade --out ../out/run.json
```

`--mode` is one of `jev`, `gemini` or `cascade` (the default). Add `--no-db --transactions <file>` to run without Postgres. Ticket files can be `.jsonl`, `.json` or `.csv`. Each row needs `text`; `external_id`, `channel`, `customer_phone` and `received_at` are optional.

Run the tests with `uv run pytest`. The integration tests need `docker compose up -d db`.

## Status

Plan 1 of 5 is done: the core pipeline and CLI. Still to come: synthetic data and evaluation, RAG drafting, the review UI, and the weekly report. The disclosure and failure-mode docs land with Plan 5.
````

- [ ] **Step 5: Final verification**

Run: `uv run pytest -q && uv run ruff check app tests && git status --short`

Expected: all tests pass, there are no lint findings, and the only uncommitted changes are `README.md` plus the ignored `out/` and `.env`.

- [ ] **Step 6: Commit**

```bash
cd .. && git add README.md && git commit -m "docs: quickstart for the core pipeline CLI"
```

---

## Self-review notes (for the plan author)

**Spec coverage:**

| Spec section | Where it is implemented |
|---|---|
| §6.1 normalize | Task 3 |
| §6.2 classify (cascade, order check, thresholds) | Tasks 6, 7, 8 and 12 |
| §6.3 extract (Jev picks, Gemini fallback, null rule, dates) | Tasks 4, 5, 7 and 9 |
| §6.4 rules and lookup | Tasks 10 and 11 |
| §6.7 persist, no send path | Tasks 13 and 14 |
| §6.8 batch summary and concurrency | Task 12 |
| §6.9 failures: Jev down → degraded; per-ticket isolation; Gemini down → keep Jev or fail ticket | Task 12 tests |

**Not in this plan, by design:**

| Item | Plan |
|---|---|
| §6.5 drafting agent and §6.6 guardrails | Plan 3 (`NullDrafter` here) |
| §7 data and eval | Plan 2 |
| §8 UI | Plan 4 |
| §9 weekly report, §11 docs, CI | Plan 5 |

**Spec deviations** are recorded in spec §14: LangGraph runner, `langchain-typesafe`, `T_GEM=0.66`, the `ambiguous` lookup status, `create_all` instead of Alembic, and KB tables deferred to PGVector.
