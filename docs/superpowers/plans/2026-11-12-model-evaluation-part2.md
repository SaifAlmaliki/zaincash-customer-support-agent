# Per-model Evaluation Implementation Plan — Part 2 of 3 (evaluation engine)

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Score each model's predictions (quality, system, cost), store runs and predictions, run evaluations in the background with progress/cancel, and expose them through an API and a CLI.

**Architecture:** Pure metric functions in `app/eval/metrics.py` turn `Prediction` records into a per-model summary. `app/eval/runner.py` builds the real pipeline per model (Part 1's `build_pipeline(classifier=...)`), evaluates each ticket under a `UsageMeter`, writes `eval_predictions` rows and summaries into `eval_runs`. `app/api/evaluations.py` validates requests (`prepare_evaluation`) and starts the runner as a background job; `support eval` reuses the same functions.

**Tech Stack:** Python 3.11, FastAPI, SQLAlchemy 2 (Postgres JSONB), LangGraph, pytest.

**Spec:** `docs/superpowers/specs/2026-11-12-model-evaluation-design.md`. Part 1 (`2026-11-12-model-evaluation.md`) must be complete; its **Global Constraints** and **Review Focus** apply here unchanged.

## Global Constraints

Same as Part 1. Repeated for the items this part touches:

- Precision/recall/F1 with a zero denominator is `None`; an errored ticket counts as wrong for every quality metric and toward the error rate.
- Cost per request is `None` when any call's cost source is `"unknown"`.
- Concurrency per provider: Ollama 1, OpenRouter 4, TypeSafe 4. Per-ticket timeout `EVAL_TIMEOUT_S`.
- Early stop: more than 5 errors among a model's first 10 completed tickets → that model `failed`, others continue.
- One active (`queued`/`running`) evaluation at a time → 409. 422 detail is `{"code", "message", "model", "reason"}` with codes `no_models`, `unknown_model`, `model_unavailable`, `dataset_missing`, `test_split_modified`.
- On API startup, `queued`/`running` evaluations become `failed` with error `interrupted`.
- Integration tests are marked `pytest.mark.integration` and use `Settings().test_database_url` (database `support_test`).

## Deviations from the spec (intentional, small)

- `eval_runs.models` stores model descriptors (`EvalModel.to_dict()`: id, provider, model, locality, prices, concurrency) instead of bare IDs, so the page can show Local/Production badges without another request.
- `eval_predictions` also stores `text` and `tags` so drill-down and slices never depend on the dataset files still matching.
- Money columns use `Float`, matching existing tables (`runs.total_cost_usd`).

---

### Task 7: Metrics

**Files:**
- Create: `backend/app/eval/metrics.py`
- Test: `backend/tests/eval/test_metrics.py`

**Interfaces:**
- Consumes: `FIELD_NAMES`, `FLAG_NAMES` from `app.pipeline.contracts`.
- Produces (in `app.eval.metrics`):
  - `@dataclass(frozen=True) class Prediction`: `ticket_id: str`, `tags: tuple[str, ...]`, `gold: dict`, `predicted: dict | None`, `latency_ms: int`, `usage: tuple[dict, ...]`, `cost_usd: float`, `error: str | None = None`. `predicted` keys: `category, priority, flags (bool per flag), fields, lookup, escalated, reasons, confidence`.
  - `ERROR_LABEL = "error"`
  - `prf(tp: int, fp: int, fn: int) -> dict` (`precision`, `recall`, `f1`, each `float | None`)
  - `wilson(k: int, n: int, z: float = 1.96) -> list[float] | None`
  - `percentile(values: Sequence[float], pct: float) -> int | None`
  - `classification_metrics(preds, labels) -> dict`, `flag_metrics(preds) -> dict`, `extraction_metrics(preds) -> dict`, `escalation_metrics(preds) -> dict`, `system_metrics(preds) -> dict`, `cost_metrics(preds) -> dict`, `slice_metrics(preds) -> dict`
  - `summarize_model(preds: Sequence[Prediction], labels: Sequence[str]) -> dict` with keys `n, classification, flags, extraction, escalation, system, cost, slices`

- [ ] **Step 1: Write the failing tests**

Create `backend/tests/eval/test_metrics.py`:

```python
import pytest

from app.eval.metrics import (
    ERROR_LABEL,
    Prediction,
    classification_metrics,
    cost_metrics,
    escalation_metrics,
    extraction_metrics,
    flag_metrics,
    percentile,
    prf,
    slice_metrics,
    summarize_model,
    system_metrics,
    wilson,
)
from app.pipeline.contracts import FLAG_NAMES

NO_FLAGS = dict.fromkeys(FLAG_NAMES, False)
NO_FIELDS = {"txn_ref": None, "amount": None, "phone": None, "date": None}


def gold(category="A", priority="P3", escalated=False, flags=None, fields=None):
    return {"category": category, "priority": priority, "escalated": escalated,
            "flags": NO_FLAGS | (flags or {}), "fields": NO_FIELDS | (fields or {}),
            "lookup": "not_applicable", "reasons": []}


def pred(gold_category="A", predicted_category="A", *, error=None, priority="P3",
         escalated=False, gold_escalated=False, flags=None, gold_flags=None, fields=None,
         gold_fields=None, tags=(), usage=(), cost=0.0, latency=100):
    predicted = None if error else {
        "category": predicted_category, "priority": priority, "escalated": escalated,
        "flags": NO_FLAGS | (flags or {}), "fields": NO_FIELDS | (fields or {}),
        "lookup": "not_applicable", "reasons": [], "confidence": 0.9}
    return Prediction("T", tuple(tags), gold(gold_category, escalated=gold_escalated,
                                             flags=gold_flags, fields=gold_fields),
                      predicted, latency, tuple(usage), cost, error)


def call(role="classify", latency=50, tokens_in=100, tokens_out=20, cost=0.001,
         source="estimate", tps=None, error=None):
    return {"role": role, "model": "m", "input_tokens": tokens_in, "output_tokens": tokens_out,
            "latency_ms": latency, "cost_usd": cost, "cost_source": source,
            "tokens_per_s": tps, "error": error}


def test_prf_handles_zero_denominators():
    assert prf(0, 0, 0) == {"precision": None, "recall": None, "f1": None}
    assert prf(0, 2, 0) == {"precision": 0.0, "recall": None, "f1": None}
    assert prf(0, 1, 1) == {"precision": 0.0, "recall": 0.0, "f1": 0.0}
    assert prf(1, 1, 0)["f1"] == pytest.approx(2 / 3)


def test_wilson_and_percentile():
    low, high = wilson(50, 100)
    assert low == pytest.approx(0.4038, abs=1e-3) and high == pytest.approx(0.5962, abs=1e-3)
    assert wilson(0, 0) is None
    assert percentile([], 50) is None
    assert percentile([10, 20, 30, 40], 50) == 20
    assert percentile([10, 20, 30, 40], 95) == 40


def test_classification_counts_errors_as_wrong():
    preds = [pred("A", "A"), pred("A", "B"), pred("B", "B"), pred("B", error="boom")]
    m = classification_metrics(preds, ["A", "B", "C"])
    assert m["accuracy"] == 0.5 and m["correct"] == 2
    assert m["per_category"]["A"] == {"precision": 1.0, "recall": 0.5, "f1": pytest.approx(2 / 3),
                                      "support": 2}
    assert m["per_category"]["B"]["precision"] == 0.5 and m["per_category"]["B"]["recall"] == 0.5
    assert m["per_category"]["C"] == {"precision": None, "recall": None, "f1": None, "support": 0}
    assert m["macro_precision"] == pytest.approx(0.75)
    assert m["confusion"] == {"A": {"A": 1, "B": 1}, "B": {"B": 1, ERROR_LABEL: 1}}
    assert m["accuracy_ci"][0] < 0.5 < m["accuracy_ci"][1]


def test_priority_exact_and_within_one():
    preds = [pred(priority="P3"), pred(priority="P2"), pred(priority="P1"), pred(error="x")]
    m = classification_metrics(preds, ["A"])
    assert m["priority_exact"] == 0.25 and m["priority_within_one"] == 0.5


def test_flags():
    preds = [pred(flags={"fraud_suspected": True}, gold_flags={"fraud_suspected": True}),
             pred(flags={"fraud_suspected": True}),
             pred(gold_flags={"fraud_suspected": True}, error="x")]
    fraud = flag_metrics(preds)["fraud_suspected"]
    assert (fraud["precision"], fraud["recall"], fraud["support"]) == (0.5, 0.5, 2)
    # The errored ticket counts as the opposite of gold (a false positive here); no gold positives.
    human = flag_metrics(preds)["asks_for_human"]
    assert (human["precision"], human["recall"], human["support"]) == (0.0, None, 0)


def test_extraction_hallucination_and_missed():
    preds = [pred(fields={"amount": 50000}, gold_fields={"amount": 50000}),
             pred(fields={"amount": 1000}, gold_fields={"amount": 50000}),
             pred(fields={"txn_ref": "ZC1"}),
             pred(gold_fields={"phone": "0770"})]
    m = extraction_metrics(preds)
    assert m["per_field"]["amount"] == {"precision": 0.5, "recall": 0.5, "f1": 0.5, "support": 2}
    assert m["per_field"]["txn_ref"]["precision"] == 0.0
    assert m["hallucination_rate"] == pytest.approx(1 / 13)
    assert m["missed_rate"] == pytest.approx(1 / 3)
    assert m["micro_precision"] == pytest.approx(1 / 3)


def test_escalation():
    preds = [pred(escalated=True, gold_escalated=True), pred(escalated=True),
             pred(gold_escalated=True), pred(), pred("A", "B"), pred(error="x")]
    m = escalation_metrics(preds)
    # tp: first; fp: second and the errored ticket (counted as escalated, gold not); fn: third.
    assert m["precision"] == pytest.approx(1 / 3) and m["recall"] == 0.5
    assert m["rate"] == pytest.approx(3 / 6) and m["gold_rate"] == pytest.approx(2 / 6)
    assert m["coverage"] == pytest.approx(3 / 6)
    assert m["accuracy_not_escalated"] == pytest.approx(2 / 3)


def test_system_metrics():
    preds = [pred(latency=100, usage=[call(latency=40, tps=50.0)]),
             pred(latency=300, usage=[call(latency=60, error="bad json"), call(latency=70)]),
             pred(latency=200, error="timeout", usage=[call(latency=500, tokens_in=None,
                                                             tokens_out=None, error="timeout")])]
    m = system_metrics(preds)
    assert (m["latency_p50_ms"], m["latency_p95_ms"]) == (200, 300)
    assert m["classifier_p50_ms"] == 130
    assert m["error_rate"] == pytest.approx(1 / 3)
    assert m["invalid_output_rate"] == pytest.approx(2 / 3)
    assert m["mean_input_tokens"] == 150 and m["mean_output_tokens"] == 30
    assert m["tokens_per_s"] == 50.0


def test_cost_metrics_and_unknown_prices():
    preds = [pred(cost=0.003, usage=[call(cost=0.002), call(role="extract", cost=0.001)]),
             pred(cost=0.001, usage=[call(cost=0.001)])]
    m = cost_metrics(preds)
    assert m["classifier_cost_per_request"] == pytest.approx(0.0015)
    assert m["total_cost_per_request"] == pytest.approx(0.002)
    assert m["cost_per_1k_tickets"] == pytest.approx(2.0)
    assert m["cost_sources"] == {"estimate": 3}
    unknown = cost_metrics([pred(usage=[call(source="unknown", cost=0.0)])])
    assert unknown["classifier_cost_per_request"] is None and unknown["cost_per_1k_tickets"] is None
    local = cost_metrics([pred(usage=[call(source="local", cost=0.0)])])
    assert local["classifier_cost_per_request"] == 0.0 and local["local"] is True


def test_slices_and_summary():
    preds = [pred(tags=("arabizi",)), pred("A", "B", tags=("arabizi", "angry")),
             pred(error="x", tags=("angry",))]
    assert slice_metrics(preds)["arabizi"] == {"n": 2, "accuracy": 0.5, "error_rate": 0.0}
    assert slice_metrics(preds)["angry"]["error_rate"] == 0.5
    summary = summarize_model(preds, ["A", "B"])
    assert summary["n"] == 3
    assert set(summary) == {"n", "classification", "flags", "extraction", "escalation", "system",
                            "cost", "slices"}
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `uv run pytest tests/eval/test_metrics.py -q`
Expected: FAIL with `ModuleNotFoundError: No module named 'app.eval.metrics'`.

- [ ] **Step 3: Implement `app/eval/metrics.py`**

```python
"""Pure evaluation metrics (spec §4.7). Errored tickets count as wrong everywhere."""
from __future__ import annotations

import math
from collections import Counter
from collections.abc import Iterable, Sequence
from dataclasses import dataclass
from typing import Any

from app.pipeline.contracts import FIELD_NAMES, FLAG_NAMES

ERROR_LABEL = "error"
PRIORITIES = ("P1", "P2", "P3", "P4")


@dataclass(frozen=True)
class Prediction:
    ticket_id: str
    tags: tuple[str, ...]
    gold: dict[str, Any]
    predicted: dict[str, Any] | None
    latency_ms: int
    usage: tuple[dict[str, Any], ...]
    cost_usd: float
    error: str | None = None


def _ratio(numerator: float, denominator: float) -> float | None:
    return numerator / denominator if denominator else None


def _mean(values: Iterable[float | None]) -> float | None:
    present = [v for v in values if v is not None]
    return sum(present) / len(present) if present else None


def prf(tp: int, fp: int, fn: int) -> dict[str, float | None]:
    precision, recall = _ratio(tp, tp + fp), _ratio(tp, tp + fn)
    if precision is None or recall is None:
        f1 = None
    else:
        f1 = 2 * precision * recall / (precision + recall) if precision + recall else 0.0
    return {"precision": precision, "recall": recall, "f1": f1}


def wilson(k: int, n: int, z: float = 1.96) -> list[float] | None:
    if n == 0:
        return None
    p = k / n
    denominator = 1 + z * z / n
    centre = (p + z * z / (2 * n)) / denominator
    half = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / denominator
    return [max(0.0, centre - half), min(1.0, centre + half)]


def percentile(values: Sequence[float], pct: float) -> int | None:
    if not values:
        return None
    ordered = sorted(values)
    return int(ordered[max(0, math.ceil(pct / 100 * len(ordered)) - 1)])


def _category(p: Prediction) -> str:
    return p.predicted["category"] if p.predicted else ERROR_LABEL


def _calls(p: Prediction, role: str) -> list[dict[str, Any]]:
    return [u for u in p.usage if u.get("role") == role]


def classification_metrics(preds: Sequence[Prediction], labels: Sequence[str]) -> dict[str, Any]:
    n = len(preds)
    correct = sum(_category(p) == p.gold["category"] for p in preds)
    confusion: dict[str, dict[str, int]] = {}
    for p in preds:
        row = confusion.setdefault(p.gold["category"], {})
        row[_category(p)] = row.get(_category(p), 0) + 1
    per_category = {}
    for label in labels:
        tp = sum(p.gold["category"] == label and _category(p) == label for p in preds)
        fp = sum(p.gold["category"] != label and _category(p) == label for p in preds)
        fn = sum(p.gold["category"] == label and _category(p) != label for p in preds)
        per_category[label] = prf(tp, fp, fn) | {"support": tp + fn}

    def within_one(p: Prediction) -> bool:
        if not p.predicted:
            return False
        return abs(PRIORITIES.index(p.predicted["priority"]) - PRIORITIES.index(p.gold["priority"])) <= 1

    return {
        "accuracy": _ratio(correct, n), "accuracy_ci": wilson(correct, n), "correct": correct,
        "macro_precision": _mean(v["precision"] for v in per_category.values()),
        "macro_recall": _mean(v["recall"] for v in per_category.values()),
        "macro_f1": _mean(v["f1"] for v in per_category.values()),
        "per_category": per_category, "confusion": confusion,
        "priority_exact": _ratio(sum(bool(p.predicted) and p.predicted["priority"] == p.gold["priority"]
                                     for p in preds), n),
        "priority_within_one": _ratio(sum(within_one(p) for p in preds), n),
    }


def flag_metrics(preds: Sequence[Prediction]) -> dict[str, dict[str, Any]]:
    out = {}
    for flag in FLAG_NAMES:
        tp = fp = fn = 0
        for p in preds:
            gold = bool(p.gold["flags"].get(flag))
            predicted = bool(p.predicted["flags"].get(flag)) if p.predicted else not gold
            tp += gold and predicted
            fp += predicted and not gold
            fn += gold and not predicted
        out[flag] = prf(tp, fp, fn) | {"support": tp + fn}
    return out


def extraction_metrics(preds: Sequence[Prediction]) -> dict[str, Any]:
    per_field, totals = {}, Counter()
    for field in FIELD_NAMES:
        tp = fp = fn = 0
        for p in preds:
            gold = p.gold["fields"].get(field)
            predicted = p.predicted["fields"].get(field) if p.predicted else None
            if predicted is not None and gold is not None and str(predicted) == str(gold):
                tp += 1
            else:
                fp += predicted is not None
                fn += gold is not None
            if gold is None:
                totals["gold_null"] += 1
                totals["hallucinated"] += predicted is not None
            else:
                totals["gold_set"] += 1
                totals["missed"] += predicted is None
        per_field[field] = prf(tp, fp, fn) | {"support": tp + fn}
        totals.update(tp=tp, fp=fp, fn=fn)
    micro = prf(totals["tp"], totals["fp"], totals["fn"])
    return {"per_field": per_field, "micro_precision": micro["precision"],
            "micro_recall": micro["recall"], "micro_f1": micro["f1"],
            "hallucination_rate": _ratio(totals["hallucinated"], totals["gold_null"]),
            "missed_rate": _ratio(totals["missed"], totals["gold_set"])}


def escalation_metrics(preds: Sequence[Prediction]) -> dict[str, Any]:
    n = len(preds)
    tp = fp = fn = escalated = gold_escalated = automated = automated_correct = 0
    for p in preds:
        gold = bool(p.gold["escalated"])
        predicted = bool(p.predicted["escalated"]) if p.predicted else not gold
        tp += gold and predicted
        fp += predicted and not gold
        fn += gold and not predicted
        escalated += predicted
        gold_escalated += gold
        if p.predicted and not predicted:
            automated += 1
            automated_correct += _category(p) == p.gold["category"]
    return prf(tp, fp, fn) | {
        "rate": _ratio(escalated, n), "gold_rate": _ratio(gold_escalated, n),
        "coverage": _ratio(automated, n),
        "accuracy_not_escalated": _ratio(automated_correct, automated),
    }


def system_metrics(preds: Sequence[Prediction]) -> dict[str, Any]:
    n = len(preds)
    latencies = [p.latency_ms for p in preds]
    classify = [_calls(p, "classify") for p in preds]
    classifier_ms = [sum(c["latency_ms"] for c in calls) for calls in classify if calls]
    tokens_in = [sum(c["input_tokens"] or 0 for c in calls) for calls in classify
                 if any(c["input_tokens"] is not None for c in calls)]
    tokens_out = [sum(c["output_tokens"] or 0 for c in calls) for calls in classify
                  if any(c["output_tokens"] is not None for c in calls)]
    return {
        "latency_p50_ms": percentile(latencies, 50), "latency_p95_ms": percentile(latencies, 95),
        "latency_mean_ms": _mean(latencies),
        "classifier_p50_ms": percentile(classifier_ms, 50),
        "classifier_p95_ms": percentile(classifier_ms, 95),
        "error_rate": _ratio(sum(p.error is not None for p in preds), n),
        "invalid_output_rate": _ratio(sum(any(c.get("error") for c in calls) for calls in classify), n),
        "mean_input_tokens": _mean(tokens_in), "mean_output_tokens": _mean(tokens_out),
        "tokens_per_s": _mean(c.get("tokens_per_s") for calls in classify for c in calls),
    }


def cost_metrics(preds: Sequence[Prediction]) -> dict[str, Any]:
    n = len(preds)
    usage = [u for p in preds for u in p.usage]
    sources = Counter(u["cost_source"] for u in usage)
    known = "unknown" not in sources
    total = sum(p.cost_usd for p in preds)
    classifier = sum(u["cost_usd"] for p in preds for u in _calls(p, "classify"))
    return {
        "classifier_cost_per_request": _ratio(classifier, n) if known and n else None,
        "total_cost_per_request": _ratio(total, n) if known and n else None,
        "total_cost_usd": round(total, 6),
        "cost_per_1k_tickets": total / n * 1000 if known and n else None,
        "cost_sources": dict(sources),
        "local": bool(usage) and all(u["cost_source"] == "local" for u in _all_classify(preds)),
    }


def _all_classify(preds: Sequence[Prediction]) -> list[dict[str, Any]]:
    return [u for p in preds for u in _calls(p, "classify")]


def slice_metrics(preds: Sequence[Prediction]) -> dict[str, dict[str, Any]]:
    out = {}
    for tag in sorted({t for p in preds for t in p.tags}):
        selected = [p for p in preds if tag in p.tags]
        out[tag] = {"n": len(selected),
                    "accuracy": _ratio(sum(_category(p) == p.gold["category"] for p in selected),
                                       len(selected)),
                    "error_rate": _ratio(sum(p.error is not None for p in selected), len(selected))}
    return out


def summarize_model(preds: Sequence[Prediction], labels: Sequence[str]) -> dict[str, Any]:
    return {"n": len(preds), "classification": classification_metrics(preds, labels),
            "flags": flag_metrics(preds), "extraction": extraction_metrics(preds),
            "escalation": escalation_metrics(preds), "system": system_metrics(preds),
            "cost": cost_metrics(preds), "slices": slice_metrics(preds)}
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `uv run pytest tests/eval/test_metrics.py -q && uv run ruff check app tests`
Expected: all PASS, ruff clean. If a hand-computed expectation fails, recompute it by hand from the fixture before touching the implementation; the fixture values in Step 1 are the contract.

- [ ] **Step 5: Commit**

```bash
git add backend/app/eval/metrics.py backend/tests/eval/test_metrics.py
git commit -m "feat: compute per-model quality, system and cost metrics"
```

---

### Task 8: Evaluation storage and views

**Files:**
- Create: `backend/app/eval/db_models.py`
- Create: `backend/app/eval/service.py`
- Modify: `backend/app/db/session.py` (register models before `create_all`)
- Test: `backend/tests/eval/conftest.py`, `backend/tests/eval/dataset_fixture.py`, `backend/tests/eval/test_service.py`

**Interfaces:**
- Consumes: `Prediction` (Task 7); `EvalModel` (Part 1 Task 4); `EvalTicket` (Part 1 Task 5).
- Produces:
  - `EvalRunRow` (`eval_runs`) and `EvalPredictionRow` (`eval_predictions`) — columns below.
  - `app.eval.service`:
    - `ACTIVE_STATUSES = ("queued", "running")`
    - `create_eval_run(session, *, split: str, dataset_sha256: str, models: list[EvalModel], tickets: int, prompt_version: str, estimated_cost_usd: float | None, triggered_by: str) -> EvalRunRow` (flushes; caller commits)
    - `active_run(session) -> EvalRunRow | None`
    - `save_prediction(session, run_id: int, model_id: str, ticket: EvalTicket, prediction: Prediction) -> None`
    - `prediction_from_row(row) -> Prediction`
    - `run_view(run: EvalRunRow, *, include_summary: bool = True) -> dict`
    - `prediction_view(row: EvalPredictionRow) -> dict`
    - `fail_interrupted(session) -> int`
    - `export_run(run: EvalRunRow) -> dict` (format `zaincash-eval/v2`)
    - `comparison_table(run: EvalRunRow) -> str`
  - Test helpers: `tests/eval/dataset_fixture.py` → `make_tickets(n: int = 6) -> list[EvalTicket]`, `write_dataset(directory: Path, tickets: list[EvalTicket]) -> None`; `tests/eval/conftest.py` → fixture `session_factory` (test DB, reset per test)

- [ ] **Step 1: Write the test helpers**

Create `backend/tests/eval/dataset_fixture.py`:

```python
"""A tiny, hand-labelled evaluation dataset for runner and API tests."""
from __future__ import annotations

from datetime import datetime
from pathlib import Path

from app.datetime import BAGHDAD
from app.eval.dataset.store import EvalTicket, dataset_paths, sha256_file, write_jsonl
from app.pipeline.contracts import FLAG_NAMES

NO_FIELDS = {"txn_ref": None, "amount": None, "phone": None, "date": None}


def make_tickets(n: int = 6) -> list[EvalTicket]:
    tickets = []
    for i in range(n):
        category = "general_inquiry" if i % 2 == 0 else "app_bug"
        tickets.append(EvalTicket(
            id=f"E-{i + 1:04d}", text=f"سؤال رقم {i + 1}" if category == "general_inquiry"
            else f"التطبيق يطلع خطأ {i + 1}",
            received_at=datetime(2026, 10, 7, 9, i, tzinfo=BAGHDAD), channel="app",
            customer_phone="07701234567", tags=("arabizi",) if i == 0 else (),
            gold={"category": category, "priority": "P4" if category == "general_inquiry" else "P3",
                  "flags": dict.fromkeys(FLAG_NAMES, False), "fields": dict(NO_FIELDS),
                  "lookup": "not_applicable", "escalated": False, "reasons": []},
        ))
    return tickets


def write_dataset(directory: Path, tickets: list[EvalTicket]) -> None:
    paths = dataset_paths(directory)
    write_jsonl(paths.dev, [t.to_dict() for t in tickets])
    write_jsonl(paths.test, [t.to_dict() for t in tickets])
    write_jsonl(paths.transactions, [])
    paths.test_hash.write_text(sha256_file(paths.test) + "\n", encoding="utf-8")
```

Create `backend/tests/eval/conftest.py`:

```python
import pytest
from sqlalchemy.engine import make_url

from app.config import Settings
from app.db.session import make_engine, make_sessionmaker, reset_db


@pytest.fixture
def session_factory():
    settings = Settings(_env_file=None)
    assert make_url(settings.test_database_url).database == "support_test"
    engine = make_engine(settings.test_database_url)
    reset_db(engine)
    yield make_sessionmaker(engine)
    engine.dispose()
```

- [ ] **Step 2: Write the failing tests**

Create `backend/tests/eval/test_service.py`:

```python
import pytest

from app.config import Settings
from app.eval.db_models import EvalPredictionRow, EvalRunRow
from app.eval.metrics import Prediction
from app.eval.models import resolve_model
from app.eval.service import (
    active_run,
    comparison_table,
    create_eval_run,
    export_run,
    fail_interrupted,
    prediction_from_row,
    prediction_view,
    run_view,
    save_prediction,
)
from tests.eval.dataset_fixture import make_tickets

pytestmark = pytest.mark.integration
SETTINGS = Settings(_env_file=None)


def new_run(session, **kw):
    models = [resolve_model("jev", SETTINGS), resolve_model("ollama:qwen3:4b", SETTINGS)]
    options = dict(split="dev", dataset_sha256="abc", models=models, tickets=6,
                   prompt_version="llm_classify_v1+jev-1.13.0", estimated_cost_usd=0.01,
                   triggered_by="ui")
    return create_eval_run(session, **(options | kw))


def test_create_run_and_active_run(session_factory):
    with session_factory() as session:
        run = new_run(session)
        session.commit()
        assert run.status == "queued"
        assert run.progress == {"jev": {"done": 0, "total": 6}, "ollama:qwen3:4b": {"done": 0, "total": 6}}
        assert run.model_status["jev"] == {"status": "pending", "error": None}
        assert [m["id"] for m in run.models] == ["jev", "ollama:qwen3:4b"]
        assert active_run(session).id == run.id
        run.status = "completed"
        session.commit()
        assert active_run(session) is None


def test_prediction_round_trip_and_views(session_factory):
    ticket = make_tickets(1)[0]
    prediction = Prediction(ticket.id, ticket.tags, ticket.gold, None, 120,
                            ({"role": "classify", "cost_usd": 0.0, "cost_source": "local"},), 0.0,
                            "timeout after 120s")
    with session_factory() as session:
        run = new_run(session)
        save_prediction(session, run.id, "ollama:qwen3:4b", ticket, prediction)
        session.commit()
        row = session.query(EvalPredictionRow).one()
        assert row.predicted is None and row.correct_category is False
        assert prediction_from_row(row) == prediction
        view = prediction_view(row)
        assert view["text"] == ticket.text and view["error"] == "timeout after 120s"
        full = run_view(run)
        assert full["sample_size"] == 6 and "summary" in full
        assert "summary" not in run_view(run, include_summary=False)


def test_fail_interrupted(session_factory):
    with session_factory() as session:
        queued, running, done = new_run(session), new_run(session), new_run(session)
        running.status, done.status = "running", "completed"
        session.commit()
        assert fail_interrupted(session) == 2
        session.commit()
        assert session.get(EvalRunRow, queued.id).status == "failed"
        assert session.get(EvalRunRow, running.id).error == "interrupted"
        assert session.get(EvalRunRow, done.id).status == "completed"


def test_export_and_comparison_table(session_factory):
    with session_factory() as session:
        run = new_run(session)
        run.status = "completed"
        run.summary = {"jev": {"n": 6, "classification": {"accuracy": 0.5, "macro_f1": 0.4},
                               "escalation": {"recall": 1.0},
                               "system": {"latency_p50_ms": 900, "error_rate": 0.0},
                               "cost": {"total_cost_per_request": 0.0001}}}
        run.model_status = {"jev": {"status": "completed", "error": None},
                            "ollama:qwen3:4b": {"status": "failed", "error": "unreachable"}}
        session.commit()
        exported = export_run(run)
        assert exported["format"] == "zaincash-eval/v2" and exported["split"] == "dev"
        assert exported["models"]["jev"]["n"] == 6 and exported["sample_size"] == 6
        table = comparison_table(run)
        assert "jev" in table and "50.0%" in table and "failed: unreachable" in table
```

- [ ] **Step 3: Run tests to verify they fail**

Run: `docker compose up -d db` (from the repo root), then `uv run pytest tests/eval/test_service.py -q`
Expected: FAIL with `ModuleNotFoundError: No module named 'app.eval.db_models'`.

- [ ] **Step 4: Implement the models**

Create `backend/app/eval/db_models.py`:

```python
from __future__ import annotations

from datetime import datetime

from sqlalchemy import Boolean, DateTime, Float, ForeignKey, Index, Integer, String, Text, func
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from app.db.models import Base


class EvalRunRow(Base):
    __tablename__ = "eval_runs"
    id: Mapped[int] = mapped_column(primary_key=True)
    status: Mapped[str] = mapped_column(String(16), default="queued")
    split: Mapped[str] = mapped_column(String(8))
    dataset_sha256: Mapped[str] = mapped_column(String(64))
    prompt_version: Mapped[str] = mapped_column(String(128))
    models: Mapped[list] = mapped_column(JSONB, default=list)
    model_status: Mapped[dict] = mapped_column(JSONB, default=dict)
    progress: Mapped[dict] = mapped_column(JSONB, default=dict)
    estimated_cost_usd: Mapped[float | None] = mapped_column(Float)
    actual_cost_usd: Mapped[float] = mapped_column(Float, default=0.0)
    summary: Mapped[dict] = mapped_column(JSONB, default=dict)
    triggered_by: Mapped[str] = mapped_column(String(8))
    cancel_requested: Mapped[bool] = mapped_column(Boolean, default=False)
    error: Mapped[str | None] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    started_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    finished_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))


class EvalPredictionRow(Base):
    __tablename__ = "eval_predictions"
    __table_args__ = (Index("ix_eval_predictions_run_model", "eval_run_id", "model"),)
    id: Mapped[int] = mapped_column(primary_key=True)
    eval_run_id: Mapped[int] = mapped_column(ForeignKey("eval_runs.id", ondelete="CASCADE"))
    model: Mapped[str] = mapped_column(String(160))
    ticket_id: Mapped[str] = mapped_column(String(64))
    text: Mapped[str] = mapped_column(Text)
    tags: Mapped[list] = mapped_column(JSONB, default=list)
    gold: Mapped[dict] = mapped_column(JSONB)
    # SQL NULL (not JSON null) when the ticket errored, so filters can use IS NULL.
    predicted: Mapped[dict | None] = mapped_column(JSONB(none_as_null=True))
    correct_category: Mapped[bool] = mapped_column(Boolean)
    latency_ms: Mapped[int] = mapped_column(Integer)
    usage: Mapped[list] = mapped_column(JSONB, default=list)
    cost_usd: Mapped[float] = mapped_column(Float, default=0.0)
    error: Mapped[str | None] = mapped_column(Text)
```

In `backend/app/db/session.py`, add after the `document_models` import:

```python
from app.eval import db_models as eval_db_models  # noqa: F401 -- register before create_all/drop_all
```

- [ ] **Step 5: Implement the service**

Create `backend/app/eval/service.py`:

```python
"""Evaluation persistence and JSON views."""
from __future__ import annotations

from datetime import UTC, datetime
from typing import Any

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.eval.dataset.store import EvalTicket
from app.eval.db_models import EvalPredictionRow, EvalRunRow
from app.eval.metrics import Prediction
from app.eval.models import EvalModel

ACTIVE_STATUSES = ("queued", "running")


def create_eval_run(session: Session, *, split: str, dataset_sha256: str, models: list[EvalModel],
                    tickets: int, prompt_version: str, estimated_cost_usd: float | None,
                    triggered_by: str) -> EvalRunRow:
    run = EvalRunRow(
        status="queued", split=split, dataset_sha256=dataset_sha256, prompt_version=prompt_version,
        models=[m.to_dict() for m in models],
        model_status={m.id: {"status": "pending", "error": None} for m in models},
        progress={m.id: {"done": 0, "total": tickets} for m in models},
        estimated_cost_usd=estimated_cost_usd, actual_cost_usd=0.0, summary={},
        triggered_by=triggered_by, cancel_requested=False,
    )
    session.add(run)
    session.flush()
    return run


def active_run(session: Session) -> EvalRunRow | None:
    return session.scalars(select(EvalRunRow).where(EvalRunRow.status.in_(ACTIVE_STATUSES))
                           .order_by(EvalRunRow.id.desc()).limit(1)).first()


def save_prediction(session: Session, run_id: int, model_id: str, ticket: EvalTicket,
                    prediction: Prediction) -> None:
    predicted = prediction.predicted
    session.add(EvalPredictionRow(
        eval_run_id=run_id, model=model_id, ticket_id=ticket.id, text=ticket.text,
        tags=list(ticket.tags), gold=ticket.gold, predicted=predicted,
        correct_category=bool(predicted) and predicted["category"] == ticket.gold["category"],
        latency_ms=prediction.latency_ms, usage=list(prediction.usage),
        cost_usd=prediction.cost_usd, error=prediction.error,
    ))


def prediction_from_row(row: EvalPredictionRow) -> Prediction:
    return Prediction(row.ticket_id, tuple(row.tags), row.gold, row.predicted, row.latency_ms,
                      tuple(row.usage), row.cost_usd, row.error)


def _iso(value: datetime | None) -> str | None:
    return value.isoformat() if value else None


def _sample_size(run: EvalRunRow) -> int:
    return max((p.get("total", 0) for p in run.progress.values()), default=0)


def run_view(run: EvalRunRow, *, include_summary: bool = True) -> dict[str, Any]:
    view = {
        "id": run.id, "status": run.status, "split": run.split,
        "dataset_sha256": run.dataset_sha256, "prompt_version": run.prompt_version,
        "models": run.models, "model_status": run.model_status, "progress": run.progress,
        "estimated_cost_usd": run.estimated_cost_usd, "actual_cost_usd": run.actual_cost_usd,
        "triggered_by": run.triggered_by, "cancel_requested": run.cancel_requested,
        "error": run.error, "sample_size": _sample_size(run), "created_at": _iso(run.created_at),
        "started_at": _iso(run.started_at), "finished_at": _iso(run.finished_at),
    }
    if include_summary:
        view["summary"] = run.summary
    return view


def prediction_view(row: EvalPredictionRow) -> dict[str, Any]:
    return {"id": row.id, "ticket_id": row.ticket_id, "text": row.text, "tags": row.tags,
            "gold": row.gold, "predicted": row.predicted, "correct_category": row.correct_category,
            "latency_ms": row.latency_ms, "cost_usd": row.cost_usd, "error": row.error,
            "usage": row.usage}


def fail_interrupted(session: Session) -> int:
    runs = list(session.scalars(select(EvalRunRow).where(EvalRunRow.status.in_(ACTIVE_STATUSES))))
    for run in runs:
        run.status, run.error, run.finished_at = "failed", "interrupted", datetime.now(UTC)
    return len(runs)


def export_run(run: EvalRunRow) -> dict[str, Any]:
    return {"format": "zaincash-eval/v2", "run_id": run.id, "split": run.split,
            "sample_size": _sample_size(run),
            "generated_at": _iso(run.finished_at or run.created_at),
            "dataset_sha256": run.dataset_sha256, "prompt_version": run.prompt_version,
            "models": run.summary, "model_info": run.models, "model_status": run.model_status}


def _pct(value: float | None) -> str:
    return "—" if value is None else f"{value * 100:.1f}%"


def comparison_table(run: EvalRunRow) -> str:
    header = f"{'model':45} {'accuracy':>9} {'macro F1':>9} {'esc. rec.':>9} {'p50 ms':>8} {'errors':>8} {'$/req':>10}"
    lines = [header, "-" * len(header)]
    for model in run.models:
        model_id = model["id"]
        status = run.model_status.get(model_id, {})
        summary = run.summary.get(model_id)
        if not summary:
            lines.append(f"{model_id:45} {status.get('status')}: {status.get('error') or ''}")
            continue
        c, e, s, k = (summary["classification"], summary["escalation"], summary["system"],
                      summary["cost"])
        cost = k.get("total_cost_per_request")
        lines.append(
            f"{model_id:45} {_pct(c.get('accuracy')):>9} {_pct(c.get('macro_f1')):>9} "
            f"{_pct(e.get('recall')):>9} {s.get('latency_p50_ms') or '—':>8} "
            f"{_pct(s.get('error_rate')):>8} {'—' if cost is None else f'${cost:.5f}':>10}")
    return "\n".join(lines)
```

Note the failed-model line format: `f"{model_id:45} {status}: {error}"` produces `"... failed: unreachable"`, which the test asserts.

- [ ] **Step 6: Run tests to verify they pass**

Run: `uv run pytest tests/eval/test_service.py tests/test_db_initialization.py -q && uv run ruff check app tests`
Expected: all PASS, ruff clean.

- [ ] **Step 7: Commit**

```bash
git add backend/app/eval/db_models.py backend/app/eval/service.py backend/app/db/session.py backend/tests/eval/conftest.py backend/tests/eval/dataset_fixture.py backend/tests/eval/test_service.py
git commit -m "feat: store evaluation runs and predictions"
```

---

### Task 9: Runner, request validation and cost estimate

**Files:**
- Create: `backend/app/eval/runner.py`
- Create: `backend/app/eval/estimate.py`
- Test: `backend/tests/eval/test_runner.py`, `backend/tests/eval/test_estimate.py`

**Interfaces:**
- Consumes: Part 1 (`build_pipeline(classifier=...)`, `UsageMeter`, `current_meter`, `configured_models`, `availability`, `build_classifier`, `load_split`, `load_eval_transactions`, `DatasetError`, `render_classify_prompt`, `LLM_CLASSIFY_PROMPT_VERSION`); Task 7 (`Prediction`, `summarize_model`); Task 8 (service functions, `EvalRunRow`).
- Produces:
  - `app.eval.runner`:
    - `@dataclass class EvalContext`: `settings: Settings`, `session_factory: Any`, `taxonomy: Taxonomy`, `classifier_factory: Callable[[EvalModel], Classifier]`, `availability: Callable[[EvalModel], str]`, `llm: StructuredLLM | None = None`; property `prompt_version -> str`
    - `make_eval_context(settings, session_factory, taxonomy) -> EvalContext`
    - `class EvalRequestError(Exception)`: `code`, `model`, `reason`; `detail() -> dict`
    - `@dataclass(frozen=True) class PreparedEvaluation`: `models: list[EvalModel]`, `split: str`, `tickets: list[EvalTicket]`, `transactions: list[TxnRecord]`, `sha256: str`
    - `prepare_evaluation(ctx, model_ids: list[str], split: str) -> PreparedEvaluation`
    - `predicted_from_state(state) -> dict`
    - `async evaluate_ticket(graph, ticket: EvalTicket, timeout_s: float) -> Prediction`
    - `async run_evaluation(ctx, run_id: int, prepared: PreparedEvaluation) -> None`
    - `run_eval_job(ctx, run_id: int, prepared: PreparedEvaluation) -> None` (thread entry)
    - constants `EARLY_WINDOW = 10`, `EARLY_MAX_ERRORS = 5`
  - `app.eval.estimate`:
    - `prompt_token_estimate(taxonomy, ticket: EvalTicket, max_chars: int) -> int`
    - `last_token_means(session) -> dict[str, tuple[float, float]]`
    - `estimate_cost(models: list[EvalModel], tickets: int, prompt_tokens: int, last_tokens: dict[str, tuple[float, float]]) -> dict` with `models: {id: {cost_usd, basis}}`, `total_usd`, `unknown: bool`, `approximate: True`, `includes_gap_fill: False`

- [ ] **Step 1: Write the failing estimate tests**

Create `backend/tests/eval/test_estimate.py`:

```python
import pytest

from app.config import Settings
from app.eval.estimate import estimate_cost, prompt_token_estimate
from app.eval.models import resolve_model
from tests.eval.dataset_fixture import make_tickets

S = Settings(_env_file=None)


def test_prompt_token_estimate_is_positive(tax):
    assert prompt_token_estimate(tax, make_tickets(1)[0], 6000) > 500


def test_estimate_uses_prices_previous_runs_and_marks_unknown():
    models = [resolve_model("jev", S), resolve_model("openrouter:anthropic/claude-sonnet-5.5", S),
              resolve_model("ollama:qwen3:4b", S), resolve_model("openrouter:openai/gpt-5.5", S)]
    est = estimate_cost(models, 100, 1000,
                        {"openrouter:anthropic/claude-sonnet-5.5": (2000.0, 100.0)})
    m = est["models"]
    assert m["jev"]["cost_usd"] == pytest.approx(100 * 2000 * 0.042 / 1e6)
    assert m["jev"]["basis"] == "prompt_length"
    assert m["openrouter:anthropic/claude-sonnet-5.5"]["cost_usd"] == pytest.approx(
        100 * (2000 * 3.0 + 100 * 15.0) / 1e6)
    assert m["openrouter:anthropic/claude-sonnet-5.5"]["basis"] == "previous_run"
    assert m["ollama:qwen3:4b"] == {"cost_usd": 0.0, "basis": "local"}
    assert m["openrouter:openai/gpt-5.5"]["cost_usd"] is None
    assert est["unknown"] is True and est["approximate"] is True
    assert est["total_usd"] == pytest.approx(m["jev"]["cost_usd"]
                                             + m["openrouter:anthropic/claude-sonnet-5.5"]["cost_usd"])
```

- [ ] **Step 2: Write the failing runner tests**

Create `backend/tests/eval/test_runner.py`:

```python
import asyncio
from dataclasses import replace

import pytest

from app.config import Settings
from app.eval.db_models import EvalPredictionRow, EvalRunRow
from app.eval.runner import (
    EvalContext,
    EvalRequestError,
    evaluate_ticket,
    prepare_evaluation,
    run_evaluation,
)
from app.eval.service import create_eval_run
from app.pipeline.factory import build_pipeline
from app.pipeline.stage4_lookup.lookup import InMemoryTransactionRepo
from app.pipeline.stage6_draft.drafting import NullDrafter
from app.taxonomy import load_taxonomy
from tests.eval.dataset_fixture import make_tickets, write_dataset
from tests.fakes import FakeClassifier, make_output


def settings(tmp_path, **kw):
    return Settings(_env_file=None, openrouter_api_key="", typesafe_api_key="",
                    eval_models="jev,ollama:qwen3:4b", eval_data_dir=str(tmp_path), **kw)


def context(tmp_path, classifiers, *, session_factory=None, availability=None, **kw):
    s = settings(tmp_path, **kw)
    return EvalContext(settings=s, session_factory=session_factory,
                       taxonomy=load_taxonomy(s.taxonomy_path),
                       classifier_factory=lambda m: classifiers[m.id],
                       availability=availability or (lambda m: "ready"))


def graph_for(classifier, tmp_path):
    return build_pipeline(settings(tmp_path), "jev", InMemoryTransactionRepo([]),
                          classifier=classifier, drafter=NullDrafter("evaluation"))


async def test_evaluate_ticket_success(tmp_path):
    ticket = make_tickets(1)[0]
    graph = graph_for(FakeClassifier(make_output("general_inquiry", priority="P4")), tmp_path)
    p = await evaluate_ticket(graph, ticket, 5)
    assert p.error is None and p.predicted["category"] == "general_inquiry"
    assert p.predicted["escalated"] is False and p.predicted["priority"] == "P4"
    assert set(p.predicted["flags"]) >= {"fraud_suspected"} and p.predicted["fields"]["amount"] is None


async def test_runner_times_out_slow_ticket(tmp_path):
    graph = graph_for(FakeClassifier(make_output(), delay=1.0), tmp_path)
    p = await evaluate_ticket(graph, make_tickets(1)[0], 0.05)
    assert p.predicted is None and p.error == "timeout after 0.05s"


async def test_evaluate_ticket_degraded_classifier_is_an_error(tmp_path):
    degraded = replace(make_output("other", reasons=("llm_unavailable",)), degraded=True)
    p = await evaluate_ticket(graph_for(FakeClassifier(degraded), tmp_path), make_tickets(1)[0], 5)
    assert p.predicted is None and p.error == "classifier unavailable"


async def test_evaluate_ticket_exception_is_an_error(tmp_path):
    graph = graph_for(FakeClassifier(raises=RuntimeError("down")), tmp_path)
    p = await evaluate_ticket(graph, make_tickets(1)[0], 5)
    assert p.error == "RuntimeError: down"


def test_prepare_validates_models_and_dataset(tmp_path):
    write_dataset(tmp_path, make_tickets())
    ctx = context(tmp_path, {})
    prepared = prepare_evaluation(ctx, ["jev", " jev ", "ollama:qwen3:4b"], "dev")
    assert [m.id for m in prepared.models] == ["jev", "ollama:qwen3:4b"]
    assert len(prepared.tickets) == 6 and prepared.transactions == []
    for ids, code in ((["", " "], "no_models"), (["openrouter:x/y"], "unknown_model")):
        with pytest.raises(EvalRequestError) as err:
            prepare_evaluation(ctx, ids, "dev")
        assert err.value.code == code
    down = context(tmp_path, {}, availability=lambda m: "unreachable" if m.provider == "ollama" else "ready")
    with pytest.raises(EvalRequestError) as err:
        prepare_evaluation(down, ["ollama:qwen3:4b"], "dev")
    assert err.value.detail() == {"code": "model_unavailable", "model": "ollama:qwen3:4b",
                                  "reason": "unreachable", "message": err.value.detail()["message"]}
    with pytest.raises(EvalRequestError) as err:
        prepare_evaluation(context(tmp_path / "missing", {}), ["jev"], "dev")
    assert err.value.code == "dataset_missing"


@pytest.mark.integration
async def test_run_evaluation_scores_each_model(tmp_path, session_factory):
    write_dataset(tmp_path, make_tickets())
    classifiers = {"jev": FakeClassifier(make_output("general_inquiry", priority="P4")),
                   "ollama:qwen3:4b": FakeClassifier(make_output("app_bug", priority="P3"))}
    ctx = context(tmp_path, classifiers, session_factory=session_factory)
    prepared = prepare_evaluation(ctx, ["jev", "ollama:qwen3:4b"], "dev")
    with session_factory() as session:
        run = create_eval_run(session, split="dev", dataset_sha256=prepared.sha256,
                              models=prepared.models, tickets=6, prompt_version=ctx.prompt_version,
                              estimated_cost_usd=0.0, triggered_by="ui")
        session.commit()
        run_id = run.id
    await run_evaluation(ctx, run_id, prepared)
    with session_factory() as session:
        run = session.get(EvalRunRow, run_id)
        assert run.status == "completed" and run.started_at and run.finished_at
        assert run.model_status == {"jev": {"status": "completed", "error": None},
                                    "ollama:qwen3:4b": {"status": "completed", "error": None}}
        assert run.progress["jev"] == {"done": 6, "total": 6}
        assert run.summary["jev"]["classification"]["accuracy"] == 0.5
        assert run.summary["ollama:qwen3:4b"]["classification"]["accuracy"] == 0.5
        assert session.query(EvalPredictionRow).count() == 12


@pytest.mark.integration
async def test_early_stop_marks_model_failed_and_continues(tmp_path, session_factory):
    write_dataset(tmp_path, make_tickets(12))
    classifiers = {"jev": FakeClassifier(raises=RuntimeError("TypeSafe down")),
                   "ollama:qwen3:4b": FakeClassifier(make_output("general_inquiry", priority="P4"))}
    ctx = context(tmp_path, classifiers, session_factory=session_factory)
    prepared = prepare_evaluation(ctx, ["jev", "ollama:qwen3:4b"], "dev")
    with session_factory() as session:
        run_id = create_eval_run(session, split="dev", dataset_sha256=prepared.sha256,
                                 models=prepared.models, tickets=12, prompt_version="v",
                                 estimated_cost_usd=None, triggered_by="cli").id
        session.commit()
    await run_evaluation(ctx, run_id, prepared)
    with session_factory() as session:
        run = session.get(EvalRunRow, run_id)
        assert run.model_status["jev"] == {"status": "failed", "error": "RuntimeError: TypeSafe down"}
        assert run.progress["jev"]["done"] <= 12
        assert run.model_status["ollama:qwen3:4b"]["status"] == "completed"
        assert run.status == "completed"


@pytest.mark.integration
async def test_cancel_stops_remaining_models(tmp_path, session_factory):
    write_dataset(tmp_path, make_tickets())
    ctx = context(tmp_path, {"jev": FakeClassifier(make_output(), delay=0.01),
                             "ollama:qwen3:4b": FakeClassifier(make_output())},
                  session_factory=session_factory)
    prepared = prepare_evaluation(ctx, ["jev", "ollama:qwen3:4b"], "dev")
    with session_factory() as session:
        run = create_eval_run(session, split="dev", dataset_sha256=prepared.sha256,
                              models=prepared.models, tickets=6, prompt_version="v",
                              estimated_cost_usd=None, triggered_by="ui")
        run.cancel_requested = True
        session.commit()
        run_id = run.id
    await asyncio.wait_for(run_evaluation(ctx, run_id, prepared), 5)
    with session_factory() as session:
        run = session.get(EvalRunRow, run_id)
        assert run.status == "cancelled"
        assert run.model_status["ollama:qwen3:4b"]["status"] == "cancelled"
```

- [ ] **Step 3: Run tests to verify they fail**

Run: `uv run pytest tests/eval/test_estimate.py tests/eval/test_runner.py -q`
Expected: FAIL with `ModuleNotFoundError: No module named 'app.eval.estimate'` / `'app.eval.runner'`.

- [ ] **Step 4: Implement the estimate**

Create `backend/app/eval/estimate.py`:

```python
"""Approximate classifier cost before a run starts (spec §4.8)."""
from __future__ import annotations

from typing import Any

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.eval.dataset.store import EvalTicket
from app.eval.db_models import EvalRunRow
from app.eval.models import EvalModel
from app.pipeline.stage1_normalize.candidates import find_candidates
from app.pipeline.stage1_normalize.normalize import normalize
from app.pipeline.stage2_classify.llm import render_classify_prompt
from app.taxonomy import Taxonomy

CHARS_PER_TOKEN = 3.5
DEFAULT_OUTPUT_TOKENS = 120


def prompt_token_estimate(taxonomy: Taxonomy, ticket: EvalTicket, max_chars: int) -> int:
    nt = normalize(ticket.to_ticket())
    prompt = render_classify_prompt(taxonomy, nt, find_candidates(nt.match_text), max_chars)
    return int(len(prompt) / CHARS_PER_TOKEN)


def last_token_means(session: Session) -> dict[str, tuple[float, float]]:
    out: dict[str, tuple[float, float]] = {}
    runs = session.scalars(select(EvalRunRow).where(EvalRunRow.status == "completed")
                           .order_by(EvalRunRow.id.desc()).limit(20))
    for run in runs:
        for model_id, summary in (run.summary or {}).items():
            system = (summary or {}).get("system") or {}
            if model_id not in out and system.get("mean_input_tokens") is not None:
                out[model_id] = (float(system["mean_input_tokens"]),
                                 float(system.get("mean_output_tokens") or 0.0))
    return out


def estimate_cost(models: list[EvalModel], tickets: int, prompt_tokens: int,
                  last_tokens: dict[str, tuple[float, float]]) -> dict[str, Any]:
    per_model: dict[str, dict[str, Any]] = {}
    for m in models:
        if m.locality == "local":
            per_model[m.id] = {"cost_usd": 0.0, "basis": "local"}
            continue
        if m.price_in is None:
            per_model[m.id] = {"cost_usd": None, "basis": "unknown_price"}
            continue
        if m.id in last_tokens:
            tokens_in, tokens_out = last_tokens[m.id]
            basis = "previous_run"
        elif m.provider == "typesafe":  # main call plus order check, input tokens only
            tokens_in, tokens_out, basis = 2 * prompt_tokens, 0.0, "prompt_length"
        else:
            tokens_in, tokens_out, basis = prompt_tokens, DEFAULT_OUTPUT_TOKENS, "prompt_length"
        cost = tickets * (tokens_in * m.price_in + tokens_out * (m.price_out or 0.0)) / 1e6
        per_model[m.id] = {"cost_usd": cost, "basis": basis}
    known = [v["cost_usd"] for v in per_model.values() if v["cost_usd"] is not None]
    return {"models": per_model, "total_usd": sum(known),
            "unknown": len(known) < len(per_model), "approximate": True,
            "includes_gap_fill": False}
```

- [ ] **Step 5: Implement the runner**

Create `backend/app/eval/runner.py`:

```python
"""Run the real pipeline per model on a dataset split and store scored predictions (spec §4.6)."""
from __future__ import annotations

import asyncio
import logging
from collections import Counter
from collections.abc import Callable
from dataclasses import dataclass
from datetime import UTC, datetime
from time import perf_counter
from typing import Any

from app.config import Settings
from app.eval.dataset.store import DatasetError, EvalTicket, load_eval_transactions, load_split
from app.eval.db_models import EvalRunRow
from app.eval.metrics import Prediction, summarize_model
from app.eval.models import EvalModel, availability, build_classifier, configured_models
from app.eval.service import save_prediction
from app.eval.usage import UsageMeter, current_meter, elapsed_ms
from app.llm import StructuredLLM
from app.pipeline.contracts import FIELD_NAMES, FLAG_NAMES, TxnRecord
from app.pipeline.factory import build_pipeline
from app.pipeline.stage2_classify.base import Classifier
from app.pipeline.stage2_classify.prompts import LLM_CLASSIFY_PROMPT_VERSION
from app.pipeline.stage4_lookup.lookup import InMemoryTransactionRepo
from app.pipeline.stage6_draft.drafting import NullDrafter
from app.taxonomy import Taxonomy

logger = logging.getLogger(__name__)
EARLY_WINDOW = 10
EARLY_MAX_ERRORS = 5


@dataclass
class EvalContext:
    settings: Settings
    session_factory: Any
    taxonomy: Taxonomy
    classifier_factory: Callable[[EvalModel], Classifier]
    availability: Callable[[EvalModel], str]
    llm: StructuredLLM | None = None

    @property
    def prompt_version(self) -> str:
        return f"{LLM_CLASSIFY_PROMPT_VERSION}+{self.settings.jev_model}"


def make_eval_context(settings: Settings, session_factory: Any, taxonomy: Taxonomy) -> EvalContext:
    return EvalContext(settings, session_factory, taxonomy,
                       classifier_factory=lambda m: build_classifier(m, settings, taxonomy),
                       availability=lambda m: availability(m, settings))


class EvalRequestError(Exception):
    def __init__(self, code: str, message: str, *, model: str | None = None,
                 reason: str | None = None) -> None:
        super().__init__(message)
        self.code, self.model, self.reason = code, model, reason

    def detail(self) -> dict[str, Any]:
        return {"code": self.code, "message": str(self), "model": self.model, "reason": self.reason}


@dataclass(frozen=True)
class PreparedEvaluation:
    models: list[EvalModel]
    split: str
    tickets: list[EvalTicket]
    transactions: list[TxnRecord]
    sha256: str


def prepare_evaluation(ctx: EvalContext, model_ids: list[str], split: str) -> PreparedEvaluation:
    ids = list(dict.fromkeys(i.strip() for i in model_ids if i.strip()))
    if not ids:
        raise EvalRequestError("no_models", "Choose at least one model.")
    configured = {m.id: m for m in configured_models(ctx.settings)}
    models = []
    for model_id in ids:
        if model_id not in configured:
            raise EvalRequestError("unknown_model", f"{model_id} is not listed in EVAL_MODELS.",
                                   model=model_id)
        status = ctx.availability(configured[model_id])
        if status != "ready":
            raise EvalRequestError("model_unavailable", f"{model_id} is not available: {status}.",
                                   model=model_id, reason=status)
        models.append(configured[model_id])
    try:
        tickets, digest = load_split(ctx.settings.eval_data_dir, split)
        transactions = load_eval_transactions(ctx.settings.eval_data_dir)
    except DatasetError as exc:
        raise EvalRequestError(exc.code, str(exc)) from exc
    return PreparedEvaluation(models, split, tickets, transactions, digest)


def predicted_from_state(state: dict[str, Any]) -> dict[str, Any]:
    classifier, decision = state["classifier"], state["decision"]
    extracted, lookup = state.get("extracted", {}), state.get("lookup")
    return {
        "category": classifier.classification.category,
        "confidence": classifier.classification.category_confidence,
        "priority": decision.priority,
        "flags": {f: classifier.classification.flags.get(f, 0.0) > 0.5 for f in FLAG_NAMES},
        "fields": {f: extracted[f].value if f in extracted else None for f in FIELD_NAMES},
        "lookup": lookup.status if lookup else None,
        "escalated": decision.escalated, "reasons": list(decision.reasons),
    }


async def evaluate_ticket(graph: Any, ticket: EvalTicket, timeout_s: float) -> Prediction:
    meter = UsageMeter()
    token = current_meter.set(meter)
    start = perf_counter()
    predicted, error = None, None
    try:
        async with asyncio.timeout(timeout_s):
            state = await graph.ainvoke({"ticket": ticket.to_ticket()})
        if state.get("classifier") is not None and state["classifier"].degraded:
            error = (meter.errors("classify") or ["classifier unavailable"])[-1]
        else:
            predicted = predicted_from_state(state)
    except TimeoutError:
        error = f"timeout after {timeout_s:g}s"
    except Exception as exc:
        error = f"{type(exc).__name__}: {exc}"[:500]
    finally:
        current_meter.reset(token)
    return Prediction(ticket.id, ticket.tags, ticket.gold, predicted, elapsed_ms(start),
                      tuple(c.to_dict() for c in meter.calls), round(meter.cost(), 8), error)


def _update_run(ctx: EvalContext, run_id: int, **changes: Any) -> EvalRunRow:
    with ctx.session_factory() as session:
        run = session.get(EvalRunRow, run_id)
        for key, value in changes.items():
            setattr(run, key, value(run) if callable(value) else value)
        session.commit()
        return run


def _model_status(model_id: str, status: str, error: str | None = None):
    return lambda run: {**run.model_status, model_id: {"status": status, "error": error}}


async def _run_model(ctx: EvalContext, run_id: int, prepared: PreparedEvaluation,
                     model: EvalModel, cancel: asyncio.Event) -> tuple[str, str | None, list[Prediction]]:
    try:
        classifier = ctx.classifier_factory(model)
    except Exception as exc:
        return "failed", f"{type(exc).__name__}: {exc}"[:500], []
    graph = build_pipeline(ctx.settings, "jev", InMemoryTransactionRepo(prepared.transactions),
                           classifier=classifier, llm=ctx.llm, drafter=NullDrafter("evaluation"))
    limiter = asyncio.Semaphore(model.concurrency)
    stop = asyncio.Event()
    preds: list[Prediction] = []
    failure: list[str] = []
    total = len(prepared.tickets)

    async def one(ticket: EvalTicket) -> None:
        async with limiter:
            if stop.is_set():
                return
            prediction = await evaluate_ticket(graph, ticket, ctx.settings.eval_timeout_s)
            preds.append(prediction)
            with ctx.session_factory() as session:
                save_prediction(session, run_id, model.id, ticket, prediction)
                run = session.get(EvalRunRow, run_id)
                run.progress = {**run.progress, model.id: {"done": len(preds), "total": total}}
                run.actual_cost_usd = round((run.actual_cost_usd or 0.0) + prediction.cost_usd, 8)
                cancelled = run.cancel_requested
                session.commit()
            if cancelled:
                cancel.set()
                stop.set()
            first = preds[:EARLY_WINDOW]
            errors = [p.error for p in first if p.error]
            if not failure and len(first) == EARLY_WINDOW and len(errors) > EARLY_MAX_ERRORS:
                failure.append(Counter(errors).most_common(1)[0][0])
                stop.set()

    await asyncio.gather(*(one(t) for t in prepared.tickets))
    if failure:
        return "failed", failure[0], preds
    if cancel.is_set():
        return "cancelled", None, preds
    return "completed", None, preds


async def run_evaluation(ctx: EvalContext, run_id: int, prepared: PreparedEvaluation) -> None:
    run = _update_run(ctx, run_id, status="running", started_at=datetime.now(UTC))
    cancel = asyncio.Event()
    if run.cancel_requested:
        cancel.set()
    statuses: list[str] = []
    for model in prepared.models:
        if cancel.is_set() or _update_run(ctx, run_id).cancel_requested:
            cancel.set()
            _update_run(ctx, run_id, model_status=_model_status(model.id, "cancelled"))
            statuses.append("cancelled")
            continue
        _update_run(ctx, run_id, model_status=_model_status(model.id, "running"))
        status, error, preds = await _run_model(ctx, run_id, prepared, model, cancel)
        statuses.append(status)
        changes: dict[str, Any] = {"model_status": _model_status(model.id, status, error)}
        if preds:
            summary = summarize_model(preds, ctx.taxonomy.ids)
            changes["summary"] = lambda run, s=summary, m=model.id: {**run.summary, m: s}
        _update_run(ctx, run_id, **changes)
    all_failed = bool(statuses) and all(s == "failed" for s in statuses)
    _update_run(ctx, run_id, finished_at=datetime.now(UTC),
                status="cancelled" if cancel.is_set() else "failed" if all_failed else "completed",
                error="All models failed." if all_failed and not cancel.is_set() else None)


def run_eval_job(ctx: EvalContext, run_id: int, prepared: PreparedEvaluation) -> None:
    try:
        asyncio.run(run_evaluation(ctx, run_id, prepared))
    except Exception as exc:
        logger.warning("Evaluation %s failed: %s", run_id, type(exc).__name__)
        _update_run(ctx, run_id, status="failed", finished_at=datetime.now(UTC),
                    error="Evaluation interrupted. Completed predictions were retained.")
```

Note on `_update_run(ctx, run_id)` with no changes: it reloads the row and returns it, which is how the loop sees a cancel requested through the API between models.

- [ ] **Step 6: Run tests to verify they pass**

Run: `uv run pytest tests/eval/test_estimate.py tests/eval/test_runner.py -q && uv run ruff check app tests`
Expected: all PASS (integration tests need the db container), ruff clean.

- [ ] **Step 7: Commit**

```bash
git add backend/app/eval/runner.py backend/app/eval/estimate.py backend/tests/eval/test_runner.py backend/tests/eval/test_estimate.py
git commit -m "feat: run evaluations per model with progress, early stop and cancel"
```

---

### Task 10: Evaluation API, health capability and startup recovery

**Files:**
- Create: `backend/app/api/evaluations.py`
- Modify: `backend/app/main.py` (context, router, recovery, `evaluation_builder` parameter)
- Modify: `backend/app/api/workspace.py` (`capabilities.evaluation: True`; drop `evaluation` from `/api/insights`)
- Test: `backend/tests/eval/test_api.py`

**Interfaces:**
- Consumes: Task 8 service, Task 9 runner/estimate.
- Produces HTTP routes (all JSON):
  - `GET /api/evaluations/models` → `[EvalModel.to_dict() | {"availability": str}]`
  - `POST /api/evaluations/estimate` body `{"models": [str], "split": "dev"|"test"}` → estimate dict + `"tickets": int`
  - `POST /api/evaluations` (202) same body → `run_view(run)`; 409 `{"detail": "An evaluation is already running."}`; 422 `{"detail": {code, message, model, reason}}`
  - `POST /api/evaluations/{id}/cancel` → `run_view(run)`; 404 if missing
  - `GET /api/evaluations?limit=20` → `[run_view(run, include_summary=False)]`
  - `GET /api/evaluations/{id}` → `run_view(run)`; 404 if missing
  - `GET /api/evaluations/{id}/predictions?model=&gold=&predicted=&correct=&limit=50&offset=0` → `{"items": [prediction_view], "total": int}`; `predicted=error` selects errored rows
- `create_app(..., evaluation_builder=None)` where `evaluation_builder(settings, session_factory, taxonomy) -> EvalContext`; `app.state.evaluation` holds the context.

- [ ] **Step 1: Write the failing tests**

Create `backend/tests/eval/test_api.py`:

```python
import pytest
from fastapi.testclient import TestClient

from app.config import Settings
from app.eval.db_models import EvalRunRow
from app.eval.runner import EvalContext
from app.eval.service import create_eval_run
from app.main import create_app
from app.taxonomy import load_taxonomy
from tests.eval.dataset_fixture import make_tickets, write_dataset
from tests.fakes import FakeClassifier, make_output

pytestmark = pytest.mark.integration


@pytest.fixture
def make_client(tmp_path, session_factory):
    clients = []

    def build(*, availability=None, data_dir=None):
        write_dataset(tmp_path, make_tickets())
        settings = Settings(_env_file=None, openrouter_api_key="", typesafe_api_key="",
                            eval_models="jev,ollama:qwen3:4b",
                            eval_data_dir=str(data_dir or tmp_path))
        classifiers = {"jev": FakeClassifier(make_output("general_inquiry", priority="P4")),
                       "ollama:qwen3:4b": FakeClassifier(raises=RuntimeError("down"))}

        def builder(s, sf, taxonomy):
            return EvalContext(s, sf, taxonomy, classifier_factory=lambda m: classifiers[m.id],
                               availability=availability or (lambda m: "ready"))

        client = TestClient(create_app(settings, session_factory=session_factory,
                                       pipeline_builder=lambda *a, **k: None,
                                       evaluation_builder=builder))
        client.__enter__()
        clients.append(client)
        return client

    yield build
    for client in clients:
        client.__exit__(None, None, None)


def test_models_and_estimate(make_client):
    client = make_client()
    models = client.get("/api/evaluations/models").json()
    assert [(m["id"], m["availability"], m["locality"]) for m in models] == [
        ("jev", "ready", "cloud"), ("ollama:qwen3:4b", "ready", "local")]
    estimate = client.post("/api/evaluations/estimate",
                           json={"models": ["jev", "ollama:qwen3:4b"], "split": "dev"}).json()
    assert estimate["tickets"] == 6
    assert estimate["models"]["ollama:qwen3:4b"]["cost_usd"] == 0.0
    assert estimate["models"]["jev"]["cost_usd"] > 0


def test_start_runs_and_exposes_results(make_client):
    client = make_client()
    response = client.post("/api/evaluations", json={"models": ["jev", "ollama:qwen3:4b"],
                                                     "split": "test"})
    assert response.status_code == 202, response.text
    run_id = response.json()["id"]
    run = client.get(f"/api/evaluations/{run_id}").json()
    assert run["status"] == "completed" and run["triggered_by"] == "ui"
    assert run["summary"]["jev"]["classification"]["accuracy"] == 0.5
    assert run["model_status"]["ollama:qwen3:4b"]["status"] == "completed"
    assert run["summary"]["ollama:qwen3:4b"]["system"]["error_rate"] == 1.0
    listed = client.get("/api/evaluations").json()
    assert listed[0]["id"] == run_id and "summary" not in listed[0]
    page = client.get(f"/api/evaluations/{run_id}/predictions",
                      params={"model": "jev", "gold": "app_bug"}).json()
    assert page["total"] == 3 and all(i["gold"]["category"] == "app_bug" for i in page["items"])
    wrong = client.get(f"/api/evaluations/{run_id}/predictions",
                       params={"model": "jev", "correct": "false", "predicted": "general_inquiry"}).json()
    assert wrong["total"] == 3
    errors = client.get(f"/api/evaluations/{run_id}/predictions",
                        params={"model": "ollama:qwen3:4b", "predicted": "error", "limit": 2}).json()
    assert errors["total"] == 6 and len(errors["items"]) == 2
    assert errors["items"][0]["error"] == "RuntimeError: down"


def test_conflict_when_a_run_is_active(make_client, session_factory):
    client = make_client()
    with session_factory() as session:
        create_eval_run(session, split="dev", dataset_sha256="x", models=[], tickets=0,
                        prompt_version="v", estimated_cost_usd=None, triggered_by="cli")
        session.commit()
    response = client.post("/api/evaluations", json={"models": ["jev"], "split": "dev"})
    assert response.status_code == 409


def test_prepare_rejects_empty_and_dedupes(make_client):
    client = make_client()
    empty = client.post("/api/evaluations", json={"models": [" "], "split": "dev"})
    assert empty.status_code == 422 and empty.json()["detail"]["code"] == "no_models"
    response = client.post("/api/evaluations", json={"models": ["jev", "jev"], "split": "dev"})
    assert response.status_code == 202
    assert [m["id"] for m in response.json()["models"]] == ["jev"]


@pytest.mark.parametrize("body, code", [
    ({"models": ["openrouter:x/y"], "split": "dev"}, "unknown_model"),
    ({"models": ["ollama:qwen3:4b"], "split": "dev"}, "model_unavailable"),
])
def test_validation_errors(make_client, body, code):
    client = make_client(availability=lambda m: "unreachable" if m.provider == "ollama" else "ready")
    response = client.post("/api/evaluations", json=body)
    assert response.status_code == 422 and response.json()["detail"]["code"] == code


def test_dataset_errors(make_client, tmp_path):
    client = make_client(data_dir=tmp_path / "empty")
    response = client.post("/api/evaluations", json={"models": ["jev"], "split": "dev"})
    assert response.json()["detail"]["code"] == "dataset_missing"


def test_modified_test_split_is_refused(make_client, tmp_path):
    client = make_client()
    (tmp_path / "test.jsonl").write_text((tmp_path / "test.jsonl").read_text() + "\n", encoding="utf-8")
    response = client.post("/api/evaluations", json={"models": ["jev"], "split": "test"})
    assert response.status_code == 422 and response.json()["detail"]["code"] == "test_split_modified"


def test_cancel_and_not_found(make_client, session_factory):
    client = make_client()
    with session_factory() as session:
        run = create_eval_run(session, split="dev", dataset_sha256="x", models=[], tickets=0,
                              prompt_version="v", estimated_cost_usd=None, triggered_by="ui")
        session.commit()
    assert client.post(f"/api/evaluations/{run.id}/cancel").json()["cancel_requested"] is True
    assert client.get("/api/evaluations/99999").status_code == 404
    assert client.post("/api/evaluations/99999/cancel").status_code == 404


def test_startup_marks_interrupted_runs(tmp_path, session_factory):
    with session_factory() as session:
        run = create_eval_run(session, split="dev", dataset_sha256="x", models=[], tickets=0,
                              prompt_version="v", estimated_cost_usd=None, triggered_by="ui")
        run.status = "running"
        session.commit()
        run_id = run.id
    settings = Settings(_env_file=None, eval_data_dir=str(tmp_path))
    with TestClient(create_app(settings, session_factory=session_factory,
                               pipeline_builder=lambda *a, **k: None)):
        pass
    with session_factory() as session:
        assert session.get(EvalRunRow, run_id).status == "failed"
        assert session.get(EvalRunRow, run_id).error == "interrupted"


def test_health_reports_evaluation_capability(make_client):
    assert make_client().get("/api/health").json()["capabilities"]["evaluation"] is True
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `uv run pytest tests/eval/test_api.py -q`
Expected: FAIL with `TypeError: create_app() got an unexpected keyword argument 'evaluation_builder'`.

- [ ] **Step 3: Implement the router**

Create `backend/app/api/evaluations.py`:

```python
from typing import Literal

from fastapi import APIRouter, BackgroundTasks, HTTPException, Query, Request
from pydantic import BaseModel, Field
from sqlalchemy import func, select

from app.api.dependencies import SessionDep
from app.eval.db_models import EvalPredictionRow, EvalRunRow
from app.eval.estimate import estimate_cost, last_token_means, prompt_token_estimate
from app.eval.models import configured_models
from app.eval.runner import EvalContext, EvalRequestError, prepare_evaluation, run_eval_job
from app.eval.service import active_run, create_eval_run, prediction_view, run_view

router = APIRouter(prefix="/api/evaluations", tags=["Evaluation"])


class EvaluationInput(BaseModel):
    models: list[str] = Field(max_length=20)
    split: Literal["dev", "test"] = "dev"


def _context(request: Request) -> EvalContext:
    return request.app.state.evaluation


def _prepare(request: Request, body: EvaluationInput):
    try:
        return prepare_evaluation(_context(request), body.models, body.split)
    except EvalRequestError as exc:
        raise HTTPException(422, exc.detail()) from exc


def _estimate(request: Request, session, prepared) -> dict:
    ctx = _context(request)
    prompt_tokens = prompt_token_estimate(ctx.taxonomy, prepared.tickets[0], ctx.settings.max_state_chars) \
        if prepared.tickets else 0
    return estimate_cost(prepared.models, len(prepared.tickets), prompt_tokens,
                         last_token_means(session)) | {"tickets": len(prepared.tickets)}


def _run_or_404(session, run_id: int) -> EvalRunRow:
    run = session.get(EvalRunRow, run_id)
    if not run:
        raise HTTPException(404, "Evaluation not found.")
    return run


@router.get("/models")
def list_models(request: Request):
    ctx = _context(request)
    return [m.to_dict() | {"availability": ctx.availability(m)} for m in configured_models(ctx.settings)]


@router.post("/estimate")
def estimate(body: EvaluationInput, request: Request, session: SessionDep):
    return _estimate(request, session, _prepare(request, body))


@router.post("", status_code=202)
def start(body: EvaluationInput, background: BackgroundTasks, request: Request, session: SessionDep):
    if active_run(session):
        raise HTTPException(409, "An evaluation is already running.")
    prepared = _prepare(request, body)
    ctx = _context(request)
    run = create_eval_run(session, split=prepared.split, dataset_sha256=prepared.sha256,
                          models=prepared.models, tickets=len(prepared.tickets),
                          prompt_version=ctx.prompt_version,
                          estimated_cost_usd=_estimate(request, session, prepared)["total_usd"],
                          triggered_by="ui")
    session.commit()
    background.add_task(run_eval_job, ctx, run.id, prepared)
    return run_view(run)


@router.post("/{run_id}/cancel")
def cancel(run_id: int, session: SessionDep):
    run = _run_or_404(session, run_id)
    if run.status in ("queued", "running"):
        run.cancel_requested = True
        session.commit()
    return run_view(run)


@router.get("")
def list_runs(session: SessionDep, limit: int = Query(20, ge=1, le=100)):
    runs = session.scalars(select(EvalRunRow).order_by(EvalRunRow.id.desc()).limit(limit))
    return [run_view(run, include_summary=False) for run in runs]


@router.get("/{run_id}")
def get_run(run_id: int, session: SessionDep):
    return run_view(_run_or_404(session, run_id))


@router.get("/{run_id}/predictions")
def predictions(run_id: int, session: SessionDep, model: str, gold: str | None = None,
                predicted: str | None = None, correct: bool | None = None,
                limit: int = Query(50, ge=1, le=500), offset: int = Query(0, ge=0)):
    _run_or_404(session, run_id)
    query = select(EvalPredictionRow).where(EvalPredictionRow.eval_run_id == run_id,
                                            EvalPredictionRow.model == model)
    if gold:
        query = query.where(EvalPredictionRow.gold["category"].astext == gold)
    if predicted == "error":
        query = query.where(EvalPredictionRow.predicted.is_(None))
    elif predicted:
        query = query.where(EvalPredictionRow.predicted["category"].astext == predicted)
    if correct is not None:
        query = query.where(EvalPredictionRow.correct_category.is_(correct))
    total = session.scalar(select(func.count()).select_from(query.subquery()))
    rows = session.scalars(query.order_by(EvalPredictionRow.ticket_id).limit(limit).offset(offset))
    return {"items": [prediction_view(row) for row in rows], "total": total}
```

- [ ] **Step 4: Wire it into the app**

In `backend/app/main.py`:

Imports:

```python
from app.api import evaluations, intake, knowledge, results, runs, workspace
from app.eval.runner import make_eval_context
from app.eval.service import fail_interrupted
```

Signature:

```python
def create_app(settings=None, *, session_factory=None, pipeline_builder=None, knowledge_builder=None,
               intake_builder=None, intake_dispatcher=None, evaluation_builder=None):
```

In `lifespan`, right after the `if session_factory is None:` block (before `intake_service = ...`):

```python
        app.state.evaluation = (evaluation_builder or make_eval_context)(
            settings, app.state.session_factory, app.state.taxonomy)
```

In `recover()`, inside the `with app.state.session_factory() as session:` block, before `session.commit()`:

```python
                    fail_interrupted(session)
```

Router registration:

```python
    for router in (workspace.router, results.router, runs.router, knowledge.router, intake.router,
                   evaluations.router):
```

In `backend/app/api/workspace.py`:
- in `health`, change `"evaluation": False` to `"evaluation": True`;
- in `insights`, remove `, "evaluation": None` from the returned dict.

Check for existing tests that assert the old values: `grep -rn '"evaluation"' backend/tests` and update any assertion of `evaluation: False` / `"evaluation": None` to the new values.

- [ ] **Step 5: Run tests to verify they pass**

Run: `uv run pytest tests/eval/test_api.py tests/test_workspace_api.py -q && uv run ruff check app tests`
Expected: all PASS, ruff clean.

- [ ] **Step 6: Commit**

```bash
git add backend/app/api/evaluations.py backend/app/main.py backend/app/api/workspace.py backend/tests
git commit -m "feat: add evaluation API with background runs, cancel and drill-down"
```

---

### Task 11: `support eval` CLI and v2 export

**Files:**
- Modify: `backend/app/cli.py`
- Test: `backend/tests/eval/test_cli_eval.py`

**Interfaces:**
- Consumes: `make_eval_context`, `prepare_evaluation`, `EvalRequestError`, `run_evaluation` (Task 9); `create_eval_run`, `active_run`, `comparison_table`, `export_run` (Task 8); `configured_models` (Part 1).
- Produces: `support eval [--models a,b] [--split dev|test] [--out FILE]` — exit 2 on validation errors (prints `Evaluation error (<code>): <message>`), prints the comparison table, writes `export_run(run)` JSON to `--out`.

- [ ] **Step 1: Write the failing tests**

Create `backend/tests/eval/test_cli_eval.py`:

```python
import json

import pytest
from typer.testing import CliRunner

from app import cli
from app.config import Settings, get_settings
from app.db.session import make_engine, reset_db
from tests.eval.dataset_fixture import make_tickets, write_dataset
from tests.fakes import FakeClassifier, make_output

runner = CliRunner()


@pytest.fixture
def env(tmp_path, monkeypatch):
    write_dataset(tmp_path, make_tickets())
    monkeypatch.setenv("EVAL_DATA_DIR", str(tmp_path))
    monkeypatch.setenv("EVAL_MODELS", "jev,ollama:qwen3:4b")
    get_settings.cache_clear()
    yield tmp_path
    get_settings.cache_clear()


def test_unknown_model_exits_before_touching_the_database(env, monkeypatch):
    monkeypatch.setattr(cli, "_sessionmaker", lambda settings: pytest.fail("database used"))
    result = runner.invoke(cli.app, ["eval", "--models", "bedrock:x"])
    assert result.exit_code == 2
    assert "Evaluation error (unknown_model)" in result.output


@pytest.mark.integration
def test_eval_runs_prints_table_and_exports(env, monkeypatch):
    settings = Settings(_env_file=None)
    monkeypatch.setenv("DATABASE_URL", settings.test_database_url)
    get_settings.cache_clear()
    reset_db(make_engine(settings.test_database_url))
    real = cli.make_eval_context

    def fake_context(s, sf, taxonomy):
        ctx = real(s, sf, taxonomy)
        ctx.classifier_factory = lambda m: FakeClassifier(make_output("general_inquiry", priority="P4"))
        ctx.availability = lambda m: "ready"
        return ctx

    monkeypatch.setattr(cli, "make_eval_context", fake_context)
    out = env / "result.json"
    result = runner.invoke(cli.app, ["eval", "--models", "jev,ollama:qwen3:4b", "--out", str(out)])
    assert result.exit_code == 0, result.output
    assert "jev" in result.output and "50.0%" in result.output
    exported = json.loads(out.read_text())
    assert exported["format"] == "zaincash-eval/v2" and set(exported["models"]) == {
        "jev", "ollama:qwen3:4b"}
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `uv run pytest tests/eval/test_cli_eval.py -q`
Expected: FAIL (`No such command 'eval'`, exit code 2 without the expected message, or `AttributeError: module 'app.cli' has no attribute 'make_eval_context'`).

- [ ] **Step 3: Implement the command**

In `backend/app/cli.py`, add imports:

```python
from app.eval.db_models import EvalRunRow
from app.eval.models import configured_models
from app.eval.runner import EvalRequestError, make_eval_context, prepare_evaluation, run_evaluation
from app.eval.service import active_run, comparison_table, create_eval_run, export_run
```

Add an enum next to `Mode`:

```python
class Split(StrEnum):
    dev = "dev"
    test = "test"
```

Add the command after `eval-generate`:

```python
@app.command("eval")
def eval_cmd(
    models: str | None = typer.Option(None, "--models", help="comma-separated; default EVAL_MODELS"),
    split: Split = typer.Option(Split.dev, "--split"),
    out: Path | None = typer.Option(None, "--out", help="write the run as zaincash-eval/v2 JSON"),
) -> None:
    """Evaluate models on a dataset split and print a comparison table."""
    settings = _command_settings()
    taxonomy = load_taxonomy(settings.taxonomy_path)
    ctx = make_eval_context(settings, None, taxonomy)
    ids = models.split(",") if models else [m.id for m in configured_models(settings)]
    try:
        prepared = prepare_evaluation(ctx, ids, split.value)
    except EvalRequestError as exc:
        typer.echo(f"Evaluation error ({exc.code}): {exc}", err=True)
        raise typer.Exit(2) from None
    sf = _sessionmaker(settings)
    ctx.session_factory = sf
    with sf() as session:
        if active_run(session):
            typer.echo("An evaluation is already running.", err=True)
            raise typer.Exit(2)
        run_id = create_eval_run(session, split=prepared.split, dataset_sha256=prepared.sha256,
                                 models=prepared.models, tickets=len(prepared.tickets),
                                 prompt_version=ctx.prompt_version, estimated_cost_usd=None,
                                 triggered_by="cli").id
        session.commit()
    asyncio.run(run_evaluation(ctx, run_id, prepared))
    with sf() as session:
        run = session.get(EvalRunRow, run_id)
        typer.echo(comparison_table(run))
        if out:
            out.parent.mkdir(parents=True, exist_ok=True)
            out.write_text(json.dumps(export_run(run), ensure_ascii=False, indent=2), encoding="utf-8")
```

- [ ] **Step 4: Run tests to verify they pass, then the whole backend suite**

Run: `uv run pytest tests/eval/test_cli_eval.py -q && uv run pytest -q && uv run ruff check app tests`
Expected: all PASS, ruff clean.

- [ ] **Step 5: Commit**

```bash
git add backend/app/cli.py backend/tests/eval/test_cli_eval.py
git commit -m "feat: add support eval CLI with comparison table and v2 export"
```

Continue with **Part 3**: `docs/superpowers/plans/2026-11-12-model-evaluation-part3.md`.
