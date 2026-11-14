# AI Usage and Performance Dashboard Implementation Plan — Part 1 of 2 (backend)

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Record every AI call (process, model, time, tokens, cost, cost source, status) in an `ai_calls` ledger linked to its ticket, run, intake session or document, and serve per-process, per-model, per-ticket and daily cost/time reports for the `/evaluation` page.

**Architecture:** A small `app/telemetry` package defines `AiCall` and a context-local buffer. Each call site appends an `AiCall`; the owner of the work (batch ticket, intake turn, indexing attempt, request) writes the buffered calls in its own transaction, inside a savepoint so recording can never fail the work. A reporting module aggregates the ledger with Postgres (`percentile_cont`), exposed by `/api/ai-usage/*`.

**Tech Stack:** Python 3.11, FastAPI, SQLAlchemy 2 (Postgres, JSONB), LangGraph/LangChain, httpx, pytest.

**Spec:** `docs/superpowers/specs/2026-11-14-ai-usage-dashboard-design.md`

**Plan parts:** Part 1 (this file) Tasks 1–10 backend. Part 2 `2026-11-14-ai-usage-dashboard-part2.md` Tasks 11–17 frontend, docs and verification.

## Global Constraints

- Backend commands run from `backend/`: `uv run pytest -q`, `uv run ruff check app tests`. Tests marked `integration` need `docker compose up -d db` (database `support_test`).
- No test calls a real model, OpenRouter, TypeSafe or Ollama.
- Jev is the only classifier. No behaviour of batch, intake, drafting or knowledge changes except the extra recording and the extraction cost fix (Task 5).
- Processes are exactly: `intake`, `classify`, `extract`, `draft`, `draft_search`, `credential_check`, `kb_index`, `kb_search`, `probe`.
- Cost precedence: local → `(0.0, "local")`; provider-reported → `"provider"`; tokens × known price → `"estimate"`; otherwise `(0.0, "unknown")`.
- Prices for estimates: prices saved with the admin's choice (`options.price_in_per_m` / `price_out_per_m`) → `.env` prices for the `.env` default models → unknown. No Gemini fallback.
- `ai_calls` never stores prompts, ticket text, messages or model output. `error` is the exception type, plus `HTTP <status>` when present; at most 300 characters.
- Recording never raises into the caller; writing calls happens in a savepoint (`session.begin_nested()`) or its own short transaction, and failures are logged as warnings.
- Not backfilled: results without ledger rows report `detail_recorded = false`.
- Reporting periods default to the last 7 days; daily buckets use Asia/Baghdad.
- Ruff line length 100; follow the surrounding style; add comments only for non-obvious behaviour.

## Review Focus

1. A ticket whose pipeline fails (exception or timeout) must still have the calls it made recorded with its run and ticket — pinned by `test_failed_ticket_keeps_its_calls` (Task 3).
2. A database error while inserting ledger rows must not lose or fail the ticket result — pinned by `test_ledger_failure_does_not_fail_the_result` (Task 3).
3. A provider that returns no usage and no cost (Ollama intake, odd OpenRouter models) must be stored as `unknown`/`local`, never as an invented estimate — pinned by `test_unknown_price_is_never_estimated` (Task 2) and `test_intake_call_without_cost_uses_estimate_or_unknown` (Task 8).
4. A period with no calls, or filters that match nothing, must return zeros/`null` percentiles and empty lists, not 500 — pinned by `test_empty_period_returns_empty_report` (Task 10).
5. Intake calls made before submission must show on the submitted ticket's timeline and cost — pinned by `test_submission_links_intake_calls` (Task 8) and `test_ticket_rows_include_intake_cost` (Task 10).

---

### Task 1: Telemetry core — `AiCall`, recording context, ledger table, `processed_at`

**Files:**
- Create: `backend/app/telemetry/__init__.py`, `backend/app/telemetry/calls.py`, `backend/app/telemetry/db_models.py`, `backend/app/telemetry/store.py`
- Modify: `backend/app/db/session.py` (register models), `backend/app/db/models.py` (`TicketResultRow.processed_at`), `backend/app/db/workspace_schema.py` (add column on existing DBs)
- Test: `backend/tests/telemetry/__init__.py`, `backend/tests/telemetry/test_calls.py`, `backend/tests/telemetry/test_store.py`

**Interfaces:**
- Produces (in `app.telemetry.calls`):
  - `PROCESSES`, `TICKET_PROCESSES = ("intake","classify","extract","draft","draft_search","credential_check")`, `UNATTRIBUTED_PROCESSES = ("kb_index","kb_search","probe")`
  - `@dataclass(frozen=True) AiCall(process, provider, model, locality, started_at: datetime, latency_ms: int, input_tokens: int|None=None, output_tokens: int|None=None, cost_usd: float=0.0, cost_source: str="unknown", status: str="ok", error: str|None=None, attempt: int=1, detail: Mapping[str, Any]=...)`
  - `@dataclass CallContext(run_id=None, ticket_id=None, intake_session_id=None, document_id=None, calls=[])`
  - `current_calls: ContextVar[CallContext | None]`; `record(call) -> None`; `call_context(**links) -> ContextManager[CallContext]`
  - `class Timer` with `.started_at: datetime` and `.ms() -> int`
  - `count(value) -> int | None`; `money(value) -> float | None`
  - `usage_of(message) -> tuple[int|None, int|None, float|None]` (input tokens, output tokens, provider cost)
  - `cost_for(*, input_tokens, output_tokens, provider_cost, prices: tuple[float,float]|None, local: bool) -> tuple[float, str]`
  - `short_error(exc: BaseException) -> str`
  - `embed_process() -> str`
- Produces (in `app.telemetry.db_models`): `AiCallRow` (`ai_calls`).
- Produces (in `app.telemetry.store`): `call_rows(calls, *, run_id=None, ticket_id=None, intake_session_id=None, document_id=None) -> list[AiCallRow]`; `add_calls(session, calls, **links) -> None` (savepoint, never raises); `persist_calls(session_factory, calls, **links) -> None` (own transaction, never raises).
- `TicketResultRow.processed_at: datetime | None`.

- [ ] **Step 1: Write the failing unit tests**

Create `backend/tests/telemetry/__init__.py` (empty) and `backend/tests/telemetry/test_calls.py`:

```python
import uuid
from datetime import UTC, datetime
from types import SimpleNamespace

import httpx
import pytest
from langchain_core.messages import AIMessage

from app.telemetry.calls import (
    AiCall,
    Timer,
    call_context,
    cost_for,
    current_calls,
    embed_process,
    record,
    short_error,
    usage_of,
)

NOW = datetime(2026, 11, 14, 9, tzinfo=UTC)


def call(**kw):
    return AiCall(**({"process": "classify", "provider": "typesafe", "model": "jev-1.13.0",
                      "locality": "cloud", "started_at": NOW, "latency_ms": 5} | kw))


def test_record_without_context_is_dropped():
    record(call())
    assert current_calls.get() is None


def test_contexts_buffer_and_nest():
    with call_context(run_id=1, ticket_id=2) as outer:
        record(call())
        with call_context(document_id=9) as inner:
            record(call(process="kb_index"))
        record(call(process="extract"))
    assert [c.process for c in outer.calls] == ["classify", "extract"]
    assert [c.process for c in inner.calls] == ["kb_index"]
    assert current_calls.get() is None


@pytest.mark.parametrize("kwargs, expected", [
    ({"local": True, "provider_cost": 0.5, "prices": (1.0, 1.0)}, (0.0, "local")),
    ({"local": False, "provider_cost": 0.5, "prices": (1.0, 1.0)}, (0.5, "provider")),
    ({"local": False, "provider_cost": None, "prices": (3.0, 15.0)}, ((1000 * 3 + 200 * 15) / 1e6, "estimate")),
    ({"local": False, "provider_cost": None, "prices": None}, (0.0, "unknown")),
])
def test_cost_precedence(kwargs, expected):
    cost, source = cost_for(input_tokens=1000, output_tokens=200, **kwargs)
    assert source == expected[1] and cost == pytest.approx(expected[0])


def test_estimate_needs_input_tokens():
    assert cost_for(input_tokens=None, output_tokens=None, provider_cost=None,
                    prices=(1.0, 1.0), local=False) == (0.0, "unknown")


def test_usage_of_reads_langchain_and_ollama_metadata():
    message = AIMessage("", usage_metadata={"input_tokens": 10, "output_tokens": 3, "total_tokens": 13},
                        response_metadata={"cost": 0.002})
    assert usage_of(message) == (10, 3, 0.002)
    ollama = AIMessage("", response_metadata={"prompt_eval_count": 900, "eval_count": 100})
    assert usage_of(ollama) == (900, 100, None)
    assert usage_of(SimpleNamespace()) == (None, None, None)
    assert usage_of(AIMessage("", response_metadata={"cost": -1})) == (None, None, None)


def test_short_error_never_includes_the_message():
    assert short_error(ValueError("ticket text: حولت 50 الف")) == "ValueError"
    error = httpx.HTTPStatusError("x", request=httpx.Request("GET", "http://x"),
                                  response=httpx.Response(429))
    error.status_code = 429
    assert short_error(error) == "HTTPStatusError: HTTP 429"


def test_embed_process_follows_the_context():
    assert embed_process() == "kb_search"
    with call_context(document_id=3):
        assert embed_process() == "kb_index"
    with call_context(run_id=1, ticket_id=2):
        assert embed_process() == "draft_search"
    with call_context(intake_session_id=uuid.uuid4()):
        assert embed_process() == "kb_search"


def test_timer_measures_elapsed_ms():
    timer = Timer()
    assert timer.started_at.tzinfo is not None and timer.ms() >= 0
```

Create `backend/tests/telemetry/test_store.py`:

```python
import logging
from datetime import UTC, datetime

import pytest
from sqlalchemy import select

from app.config import Settings
from app.db.models import RunRow
from app.db.session import make_engine, make_sessionmaker, reset_db
from app.telemetry.calls import AiCall
from app.telemetry.db_models import AiCallRow
from app.telemetry.store import add_calls, call_rows, persist_calls

NOW = datetime(2026, 11, 14, 9, tzinfo=UTC)
CALL = AiCall("kb_index", "openrouter", "openai/text-embedding-3-small", "cloud", NOW, 40,
              input_tokens=120, cost_usd=0.0000024, cost_source="provider", detail={"batch": 1})


def test_call_rows_copy_links_and_fields():
    [row] = call_rows([CALL], document_id=5)
    assert (row.process, row.document_id, row.input_tokens, row.cost_source) == ("kb_index", 5, 120, "provider")
    assert row.detail == {"batch": 1} and row.run_id is None


@pytest.fixture
def sf():
    engine = make_engine(Settings(_env_file=None).test_database_url)
    reset_db(engine)
    yield make_sessionmaker(engine)
    engine.dispose()


@pytest.mark.integration
def test_add_calls_inside_owner_transaction(sf):
    with sf() as session:
        run = RunRow(mode="jev", prompt_version="v1", model_ids={}, status="running")
        session.add(run)
        session.flush()
        add_calls(session, [CALL], run_id=run.id)
        session.commit()
        [row] = session.scalars(select(AiCallRow)).all()
        assert row.run_id == run.id and row.started_at == NOW


@pytest.mark.integration
def test_add_calls_failure_keeps_the_owner_transaction(sf, caplog):
    with sf() as session:
        run = RunRow(mode="jev", prompt_version="v1", model_ids={}, status="running")
        session.add(run)
        session.flush()
        with caplog.at_level(logging.WARNING):
            add_calls(session, [CALL], run_id=run.id, ticket_id=999_999)  # FK violation
        session.commit()
        assert session.get(RunRow, run.id) is not None
        assert session.scalars(select(AiCallRow)).all() == []
    assert "AI call recording failed" in caplog.text


@pytest.mark.integration
def test_persist_calls_own_transaction_and_swallow_errors(sf, caplog):
    persist_calls(sf, [CALL])
    with sf() as session:
        assert len(session.scalars(select(AiCallRow)).all()) == 1

    def broken():
        raise RuntimeError("db down")

    with caplog.at_level(logging.WARNING):
        persist_calls(broken, [CALL])
    assert "AI call recording failed" in caplog.text
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `uv run pytest tests/telemetry -q`
Expected: FAIL with `ModuleNotFoundError: No module named 'app.telemetry'`.

- [ ] **Step 3: Implement `app/telemetry/calls.py`**

Create `backend/app/telemetry/__init__.py`:

```python
"""AI call ledger: recording and reporting of every model and embedding request."""
```

Create `backend/app/telemetry/calls.py`:

```python
"""One record per AI request (spec §4.3).

Call sites call `record()`. The owner of the work (batch ticket, intake turn, indexing
attempt, API request) opens a `call_context()` and writes the buffered calls itself.
"""
from __future__ import annotations

import logging
import math
import uuid
from collections.abc import Iterator, Mapping
from contextlib import contextmanager
from contextvars import ContextVar
from dataclasses import dataclass, field
from datetime import UTC, datetime
from time import perf_counter
from typing import Any

logger = logging.getLogger(__name__)

TICKET_PROCESSES = ("intake", "classify", "extract", "draft", "draft_search", "credential_check")
UNATTRIBUTED_PROCESSES = ("kb_index", "kb_search", "probe")
PROCESSES = TICKET_PROCESSES + UNATTRIBUTED_PROCESSES


@dataclass(frozen=True)
class AiCall:
    process: str
    provider: str
    model: str
    locality: str
    started_at: datetime
    latency_ms: int
    input_tokens: int | None = None
    output_tokens: int | None = None
    cost_usd: float = 0.0
    cost_source: str = "unknown"
    status: str = "ok"
    error: str | None = None
    attempt: int = 1
    detail: Mapping[str, Any] = field(default_factory=dict)


@dataclass
class CallContext:
    run_id: int | None = None
    ticket_id: int | None = None
    intake_session_id: uuid.UUID | None = None
    document_id: int | None = None
    calls: list[AiCall] = field(default_factory=list)


# Child tasks (LangGraph nodes, gathered calls) inherit the owner's buffer.
current_calls: ContextVar[CallContext | None] = ContextVar("ai_calls", default=None)


def record(call: AiCall) -> None:
    context = current_calls.get()
    if context is None:
        logger.debug("AI call outside a recording context: %s %s", call.process, call.model)
        return
    context.calls.append(call)


@contextmanager
def call_context(**links: Any) -> Iterator[CallContext]:
    context = CallContext(**links)
    token = current_calls.set(context)
    try:
        yield context
    finally:
        current_calls.reset(token)


class Timer:
    def __init__(self) -> None:
        self.started_at = datetime.now(UTC)
        self._start = perf_counter()

    def ms(self) -> int:
        return max(0, round((perf_counter() - self._start) * 1000))


def count(value: Any) -> int | None:
    if isinstance(value, bool) or not isinstance(value, int | float):
        return None
    if not math.isfinite(value) or value < 0:
        return None
    return int(value)


def money(value: Any) -> float | None:
    if isinstance(value, bool) or not isinstance(value, int | float):
        return None
    if not math.isfinite(value) or value < 0:
        return None
    return float(value)


def usage_of(message: Any) -> tuple[int | None, int | None, float | None]:
    usage = dict(getattr(message, "usage_metadata", None) or {})
    meta = dict(getattr(message, "response_metadata", None) or {})
    tokens_in = count(usage.get("input_tokens", meta.get("prompt_eval_count")))
    tokens_out = count(usage.get("output_tokens", meta.get("eval_count")))
    return tokens_in, tokens_out, money(meta.get("cost"))


def cost_for(*, input_tokens: int | None, output_tokens: int | None, provider_cost: float | None,
             prices: tuple[float, float] | None, local: bool) -> tuple[float, str]:
    if local:
        return 0.0, "local"
    if provider_cost is not None:
        return provider_cost, "provider"
    if prices is not None and input_tokens is not None:
        return (input_tokens * prices[0] + (output_tokens or 0) * prices[1]) / 1e6, "estimate"
    return 0.0, "unknown"


def short_error(exc: BaseException) -> str:
    # Provider messages can echo the prompt; keep only the type and an HTTP status.
    status = getattr(exc, "status_code", None)
    if isinstance(status, int):
        return f"{type(exc).__name__}: HTTP {status}"[:300]
    return type(exc).__name__[:300]


def embed_process() -> str:
    context = current_calls.get()
    if context is not None and context.document_id is not None:
        return "kb_index"
    if context is not None and (context.ticket_id is not None or context.run_id is not None):
        return "draft_search"
    return "kb_search"
```

- [ ] **Step 4: Implement the table, `processed_at` and the store**

Create `backend/app/telemetry/db_models.py`:

```python
from __future__ import annotations

import uuid
from datetime import datetime

from sqlalchemy import DateTime, Float, ForeignKey, Integer, SmallInteger, String
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.db.models import Base


class AiCallRow(Base):
    __tablename__ = "ai_calls"
    id: Mapped[int] = mapped_column(primary_key=True)
    started_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), index=True)
    process: Mapped[str] = mapped_column(String(32), index=True)
    provider: Mapped[str] = mapped_column(String(32))
    model: Mapped[str] = mapped_column(String(200), index=True)
    locality: Mapped[str] = mapped_column(String(8))
    latency_ms: Mapped[int] = mapped_column(Integer)
    input_tokens: Mapped[int | None] = mapped_column(Integer)
    output_tokens: Mapped[int | None] = mapped_column(Integer)
    cost_usd: Mapped[float] = mapped_column(Float, default=0.0)
    cost_source: Mapped[str] = mapped_column(String(12))
    status: Mapped[str] = mapped_column(String(8))
    error: Mapped[str | None] = mapped_column(String(300))
    attempt: Mapped[int] = mapped_column(SmallInteger, default=1)
    run_id: Mapped[int | None] = mapped_column(ForeignKey("runs.id", ondelete="SET NULL"), index=True)
    ticket_id: Mapped[int | None] = mapped_column(ForeignKey("tickets.id", ondelete="SET NULL"), index=True)
    intake_session_id: Mapped[uuid.UUID | None] = mapped_column(
        PG_UUID(as_uuid=True), ForeignKey("intake_sessions.id", ondelete="SET NULL"), index=True)
    document_id: Mapped[int | None] = mapped_column(
        ForeignKey("uploaded_documents.id", ondelete="SET NULL"), index=True)
    detail: Mapped[dict] = mapped_column(JSONB, default=dict)
```

In `backend/app/db/models.py`, add to `TicketResultRow` (next to `latency_ms`):

```python
    processed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
```

In `backend/app/db/session.py`, add after the existing model imports:

```python
from app.telemetry import db_models as telemetry_db_models  # noqa: F401 -- register before create_all/drop_all
```

`ai_calls` references `intake_sessions` and `uploaded_documents`; those modules are already imported above it, so `create_all` orders the tables correctly.

In `backend/app/db/workspace_schema.py`, inside `upgrade_workspace_schema` after the `intake_sessions` statement:

```python
        connection.execute(text(
            "ALTER TABLE IF EXISTS ticket_results ADD COLUMN IF NOT EXISTS processed_at TIMESTAMPTZ"
        ))
```

Create `backend/app/telemetry/store.py`:

```python
from __future__ import annotations

import logging
from collections.abc import Callable, Iterable
from typing import Any

from sqlalchemy.orm import Session

from app.telemetry.calls import AiCall
from app.telemetry.db_models import AiCallRow

logger = logging.getLogger(__name__)


def call_rows(calls: Iterable[AiCall], *, run_id: int | None = None, ticket_id: int | None = None,
              intake_session_id: Any = None, document_id: int | None = None) -> list[AiCallRow]:
    return [AiCallRow(
        started_at=c.started_at, process=c.process, provider=c.provider, model=c.model,
        locality=c.locality, latency_ms=c.latency_ms, input_tokens=c.input_tokens,
        output_tokens=c.output_tokens, cost_usd=c.cost_usd, cost_source=c.cost_source,
        status=c.status, error=c.error, attempt=c.attempt, run_id=run_id, ticket_id=ticket_id,
        intake_session_id=intake_session_id, document_id=document_id, detail=dict(c.detail),
    ) for c in calls]


def add_calls(session: Session, calls: Iterable[AiCall], **links: Any) -> None:
    """Insert inside the owner's transaction; a failure rolls back only the savepoint."""
    rows = call_rows(calls, **links)
    if not rows:
        return
    try:
        with session.begin_nested():
            session.add_all(rows)
            session.flush()
    except Exception as exc:
        logger.warning("AI call recording failed: %s", type(exc).__name__)


def persist_calls(session_factory: Callable[[], Session], calls: Iterable[AiCall], **links: Any) -> None:
    rows = call_rows(calls, **links)
    if not rows:
        return
    try:
        with session_factory() as session:
            session.add_all(rows)
            session.commit()
    except Exception as exc:
        logger.warning("AI call recording failed: %s", type(exc).__name__)
```

- [ ] **Step 5: Run tests to verify they pass**

Run: `uv run pytest tests/telemetry tests/test_db_initialization.py tests/test_workspace_schema.py -q && uv run ruff check app tests`
Expected: all PASS, ruff clean.

- [ ] **Step 6: Commit**

```bash
git add backend/app/telemetry backend/app/db backend/tests/telemetry
git commit -m "feat: add AI call ledger table and recording context"
```

---

### Task 2: Known prices only — saved catalog prices, no Gemini fallback

**Files:**
- Create: `backend/app/models_config/pricing.py`
- Modify: `backend/app/models_config/resolver.py` (`prices`, `token_prices`, `draft_info`, `structured_llm` later uses `prices`)
- Modify: `backend/app/pipeline/stage6_draft/model_info.py` (provider, locality, prices_known)
- Modify: `backend/app/api/admin.py` (save catalog prices with the choice)
- Modify: `backend/app/models_config/store.py` (hide price keys from `describe`)
- Test: `backend/tests/models_config/test_pricing.py`, `backend/tests/models_config/test_admin_api.py`, `backend/tests/models_config/test_resolver.py`

**Interfaces:**
- Consumes: `ModelChoice`, `Step`, `CatalogEntry`, `CATALOG_KIND`.
- Produces:
  - `PRICE_KEYS = ("price_in_per_m", "price_out_per_m")`
  - `prices_for(settings: Settings, step: Step, choice: ModelChoice, locality: str) -> tuple[float, float] | None`
  - `with_catalog_prices(choice: ModelChoice, entries: Iterable[CatalogEntry]) -> ModelChoice`
  - `ActiveModels.prices(step) -> tuple[float, float] | None`; `ActiveModels.token_prices(step) -> tuple[float, float]` (= `prices(step) or (0.0, 0.0)`)
  - `DraftModelInfo(model, token_prices, timeout_s, embedding_model, provider="openrouter", locality="cloud", prices_known=True)`

- [ ] **Step 1: Write the failing tests**

Create `backend/tests/models_config/test_pricing.py`:

```python
from app.config import Settings
from app.models_config.pricing import prices_for, with_catalog_prices
from app.models_config.types import CatalogEntry, ModelChoice, Step

S = Settings(_env_file=None, anthropic_model="anthropic/claude-sonnet-5.5")


def test_local_is_free():
    assert prices_for(S, Step.DRAFT, ModelChoice("ollama", "qwen3:4b"), "local") == (0.0, 0.0)


def test_saved_prices_win():
    choice = ModelChoice("openrouter", "openai/gpt-5.5", {"price_in_per_m": 1.25, "price_out_per_m": 10.0})
    assert prices_for(S, Step.EXTRACT, choice, "cloud") == (1.25, 10.0)


def test_env_defaults_keep_their_prices():
    assert prices_for(S, Step.CLASSIFY, ModelChoice("typesafe", S.jev_model), "cloud") == (S.price_jev_in, 0.0)
    assert prices_for(S, Step.EMBED, ModelChoice("openrouter", S.embedding_model), "cloud") == (S.price_embedding_in, 0.0)
    assert prices_for(S, Step.EXTRACT, ModelChoice("openrouter", S.gemini_model), "cloud") == (
        S.price_gemini_flash_in, S.price_gemini_flash_out)
    assert prices_for(S, Step.DRAFT, ModelChoice("openrouter", S.draft_model), "cloud") == S.draft_token_prices
    assert prices_for(S, Step.INTAKE, ModelChoice("openrouter", "anthropic/claude-sonnet-5.5"), "cloud") == (
        S.price_anthropic_in, S.price_anthropic_out)


def test_unknown_price_is_never_estimated():
    assert prices_for(S, Step.EXTRACT, ModelChoice("openrouter", "mistralai/unknown-model"), "cloud") is None
    assert prices_for(S, Step.EMBED, ModelChoice("openrouter", "other/embedder"), "cloud") is None


def test_with_catalog_prices():
    entries = [CatalogEntry("x/y", "x/y", None, 1.5, 6.0), CatalogEntry("a/b", "a/b", None)]
    priced = with_catalog_prices(ModelChoice("openrouter", "x/y", {"think": False}), entries)
    assert priced.options == {"think": False, "price_in_per_m": 1.5, "price_out_per_m": 6.0}
    unchanged = ModelChoice("openrouter", "a/b")
    assert with_catalog_prices(unchanged, entries) == unchanged
```

In `backend/tests/models_config/test_resolver.py`, replace the line

```python
    assert models.token_prices(Step.EXTRACT) == (settings.price_gemini_flash_in, settings.price_gemini_flash_out)
```

keep it (the `.env` Gemini model still has Gemini prices) and append a new test:

```python
def test_unknown_admin_model_has_no_price():
    from app.models_config.resolver import ActiveModels
    from app.models_config.types import ModelChoice

    settings = Settings(_env_file=None)
    models = ActiveModels(settings, {Step.EXTRACT: ModelChoice("openrouter", "mistralai/unknown")},
                          fake_registry(settings))
    assert models.prices(Step.EXTRACT) is None
    assert models.token_prices(Step.EXTRACT) == (0.0, 0.0)
    assert models.draft_info().provider == "openrouter" and models.draft_info().prices_known is True
```

(`fake_registry` and `Settings` are already imported in that file; if not, import them from `tests.models_config_fakes` and `app.config`.)

In `backend/tests/models_config/test_admin_api.py`, append:

```python
def test_saved_choice_keeps_catalog_prices_but_hides_them(make_client):
    with make_client() as client:
        app = client.app
        app.state.model_store.registry.get("openrouter").chat = _tool_chat
        app.state.model_store.registry.get("openrouter").entries = [
            CatalogEntry("x/y", "x/y", frozenset({Capability.TOOLS}), 1.5, 6.0)]
        saved = client.put("/api/admin/models/draft", headers=HEADERS,
                           json={"provider": "openrouter", "model": "x/y", "changed_by": "Sara"})
        assert saved.status_code == 200, saved.text
        assert "price_in_per_m" not in saved.json()["options"]
        assert app.state.model_store.choice(Step.DRAFT).options["price_in_per_m"] == 1.5
        assert app.state.model_store.active().prices(Step.DRAFT) == (1.5, 6.0)
```

and add `from app.models_config.types import Step` to that file's imports. If `registry.get("openrouter")` is not the `FakeProvider` instance in this fixture (check `ProviderRegistry.get`), pass a configured `openrouter=FakeProvider("openrouter", chat=_tool_chat, entries=[...])` into `fake_registry` instead by adding an `openrouter` parameter to the `make_client` builder.

- [ ] **Step 2: Run tests to verify they fail**

Run: `uv run pytest tests/models_config/test_pricing.py tests/models_config/test_resolver.py tests/models_config/test_admin_api.py -q`
Expected: FAIL (`No module named 'app.models_config.pricing'`).

- [ ] **Step 3: Implement pricing**

Create `backend/app/models_config/pricing.py`:

```python
"""Per-1M token prices used for cost estimates. Unknown models have no price (spec §4.5)."""
from __future__ import annotations

from collections.abc import Iterable
from dataclasses import replace

from app.config import Settings
from app.models_config.types import CatalogEntry, ModelChoice, Step
from app.telemetry.calls import money

PRICE_KEYS = ("price_in_per_m", "price_out_per_m")


def prices_for(settings: Settings, step: Step, choice: ModelChoice,
               locality: str) -> tuple[float, float] | None:
    if locality == "local":
        return 0.0, 0.0
    saved_in = money(choice.options.get("price_in_per_m"))
    if saved_in is not None:
        return saved_in, money(choice.options.get("price_out_per_m")) or 0.0
    model = choice.model
    if step is Step.CLASSIFY:
        return settings.price_jev_in, 0.0
    if step is Step.EMBED:
        return (settings.price_embedding_in, 0.0) if model == settings.embedding_model else None
    if step is Step.DRAFT and model == settings.draft_model:
        return settings.draft_token_prices
    if model.startswith("anthropic/"):
        return settings.price_anthropic_in, settings.price_anthropic_out
    if model == settings.gemini_model:
        return settings.price_gemini_flash_in, settings.price_gemini_flash_out
    return None


def with_catalog_prices(choice: ModelChoice, entries: Iterable[CatalogEntry]) -> ModelChoice:
    entry = next((e for e in entries if e.id == choice.model), None)
    if entry is None or entry.price_in_per_m is None:
        return choice
    options = {**choice.options, "price_in_per_m": entry.price_in_per_m,
               "price_out_per_m": entry.price_out_per_m or 0.0}
    return replace(choice, options=options)
```

In `backend/app/models_config/resolver.py`:

```python
from app.models_config.pricing import prices_for
```

Replace `token_prices` and `draft_info` with:

```python
    def prices(self, step: Step) -> tuple[float, float] | None:
        return prices_for(self.settings, step, self.choice(step), self.locality(step))

    def token_prices(self, step: Step) -> tuple[float, float]:
        return self.prices(step) or (0.0, 0.0)

    def draft_info(self) -> DraftModelInfo:
        return DraftModelInfo(model=self.choice(Step.DRAFT).model, token_prices=self.token_prices(Step.DRAFT),
                              timeout_s=draft_timeout_s(self.settings, self.locality(Step.DRAFT)),
                              embedding_model=self.choice(Step.EMBED).model,
                              provider=self.choice(Step.DRAFT).provider,
                              locality=self.locality(Step.DRAFT),
                              prices_known=self.prices(Step.DRAFT) is not None)
```

In `backend/app/pipeline/stage6_draft/model_info.py`, extend the dataclass:

```python
@dataclass(frozen=True)
class DraftModelInfo:
    model: str
    token_prices: tuple[float, float]
    timeout_s: float
    embedding_model: str
    provider: str = "openrouter"
    locality: str = "cloud"
    prices_known: bool = True
```

(`from_settings` stays as is; defaults cover it.)

- [ ] **Step 4: Save catalog prices and hide them from the admin view**

In `backend/app/api/admin.py`, add imports:

```python
from app.models_config.pricing import with_catalog_prices
from app.models_config.steps import CATALOG_KIND
```

Add a helper below `_check_provider`:

```python
async def _priced(request: Request, step: Step, choice: ModelChoice) -> ModelChoice:
    try:
        entries = await request.app.state.catalog.entries(choice.provider, CATALOG_KIND[step])
    except Exception:
        return choice  # an unreachable catalog only means no saved price
    return with_catalog_prices(choice, entries)
```

In `_tested`, after the probe succeeds and before `return choice, result`:

```python
    choice = await _priced(request, step, choice)
```

(`save_model` and `start_embedding_switch` both use `_tested`, so both save the prices.)

In `backend/app/models_config/store.py`, in `describe` (L77) change `"options": dict(choice.options)` to:

```python
                "options": {k: v for k, v in choice.options.items() if k not in PRICE_KEYS},
```

with `from app.models_config.pricing import PRICE_KEYS` at the top. Providers only read `think` and `temperature` from options, so the extra keys do not reach provider requests; confirm with `grep -n "options" app/models_config/providers/*.py`.

Check the admin dialog: `grep -n "options" ../employee-frontend/src/features/admin/ChangeModelDialog.tsx`. It must build options only from its temperature/thinking fields (it does today); price keys never round-trip through the browser, so `ModelOptions(extra="forbid")` keeps working.

- [ ] **Step 5: Run tests to verify they pass**

Run: `uv run pytest tests/models_config tests/test_rag_drafter.py tests/test_draft_model.py -q && uv run ruff check app tests`
Expected: all PASS, ruff clean.

- [ ] **Step 6: Commit**

```bash
git add backend/app/models_config backend/app/pipeline/stage6_draft/model_info.py backend/app/api/admin.py backend/tests/models_config
git commit -m "feat: estimate costs only from known prices and keep catalog prices with admin choices"
```

---

### Task 3: Ticket outcomes carry their calls; batch and CLI write them with the result

**Files:**
- Modify: `backend/app/pipeline/contracts.py` (`TicketOutcome.ai_calls`)
- Modify: `backend/app/pipeline/graph.py` (`run_batch` per-ticket contexts)
- Modify: `backend/app/services/batch_jobs.py` (context per ticket)
- Modify: `backend/app/db/repository.py` (`save_outcomes` writes calls and `processed_at`)
- Test: `backend/tests/telemetry/fakes.py`, `backend/tests/telemetry/test_batch_recording.py`

**Interfaces:**
- Consumes: Task 1 (`call_context`, `record`, `AiCall`, `add_calls`).
- Produces: `TicketOutcome.ai_calls: tuple = ()`; `run_batch(graph, tickets, *, concurrency)` (same signature, outcomes now carry calls); `save_outcomes(session, run_id, outcomes)` also inserts each outcome's calls (`run_id`, `ticket_id`) and sets `processed_at`.
- Test helper `tests/telemetry/fakes.py`: `RecordingClassifier(output, *, fail_for=())` records one `classify` call per ticket then returns/raises like `FakeClassifier`; `fake_call(process="classify", **kw) -> AiCall`.

- [ ] **Step 1: Write the test helpers**

Create `backend/tests/telemetry/fakes.py`:

```python
from datetime import UTC, datetime

from app.telemetry.calls import AiCall, record
from tests.fakes import FakeClassifier


def fake_call(process="classify", **kw):
    return AiCall(**({"process": process, "provider": "typesafe", "model": "jev-1.13.0",
                      "locality": "cloud", "started_at": datetime.now(UTC), "latency_ms": 12,
                      "input_tokens": 100, "cost_usd": 0.0000042, "cost_source": "estimate"} | kw))


class RecordingClassifier(FakeClassifier):
    async def classify(self, nt, cands):
        record(fake_call())
        return await super().classify(nt, cands)
```

- [ ] **Step 2: Write the failing tests**

Create `backend/tests/telemetry/test_batch_recording.py`:

```python
from datetime import UTC, datetime

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import select

from app.config import Settings
from app.db.models import TicketResultRow
from app.db.session import make_engine, make_sessionmaker, reset_db
from app.main import create_app
from app.pipeline.graph import PipelineDeps, build_graph, run_batch
from app.pipeline.stage4_lookup.lookup import InMemoryTransactionRepo
from app.taxonomy import load_taxonomy
from app.telemetry.db_models import AiCallRow
from tests.fakes import make_output
from tests.helpers import make_ticket
from tests.telemetry.fakes import RecordingClassifier

PHONE = "07701234567"
SETTINGS = Settings(_env_file=None, openrouter_api_key="", typesafe_api_key="")


def graph(fail_for=()):
    return build_graph(PipelineDeps(
        taxonomy=load_taxonomy(SETTINGS.taxonomy_path), txn_repo=InMemoryTransactionRepo([]),
        jev=RecordingClassifier(make_output("general_inquiry", priority="P4"), fail_for=fail_for)))


async def test_run_batch_attaches_each_tickets_calls():
    tickets = [make_ticket("سؤال", external_id="a", id=1), make_ticket("سؤال", external_id="fail", id=2)]
    outcomes, _ = await run_batch(graph(fail_for={"fail"}), tickets, concurrency=2)
    assert [len(o.ai_calls) for o in outcomes] == [1, 1]
    assert outcomes[1].status == "failed"


@pytest.fixture
def client():
    engine = make_engine(SETTINGS.test_database_url)
    reset_db(engine)
    sf = make_sessionmaker(engine)
    with TestClient(create_app(SETTINGS, session_factory=sf,
                               pipeline_builder=lambda *_: graph(fail_for={"fail"}))) as test_client:
        yield test_client, sf
    engine.dispose()


def start(client, ids):
    response = client.post("/api/runs", json={"tickets": [
        {"external_id": i, "text": "شكد عمولة التحويل؟", "customer_phone": PHONE,
         "received_at": datetime.now(UTC).isoformat()} for i in ids]})
    assert response.status_code == 202, response.text
    return response.json()["id"]


@pytest.mark.integration
def test_batch_writes_calls_with_run_and_ticket(client):
    test_client, sf = client
    run_id = start(test_client, ["ok-1"])
    with sf() as session:
        [row] = session.scalars(select(AiCallRow)).all()
        result = session.scalars(select(TicketResultRow)).one()
        assert (row.run_id, row.ticket_id, row.process) == (run_id, result.ticket_id, "classify")
        assert result.processed_at is not None


@pytest.mark.integration
def test_failed_ticket_keeps_its_calls(client):
    test_client, sf = client
    run_id = start(test_client, ["fail"])
    with sf() as session:
        result = session.scalars(select(TicketResultRow)).one()
        assert result.status == "failed"
        [row] = session.scalars(select(AiCallRow).where(AiCallRow.run_id == run_id)).all()
        assert row.ticket_id == result.ticket_id


@pytest.mark.integration
def test_ledger_failure_does_not_fail_the_result(client, monkeypatch):
    test_client, sf = client
    import app.telemetry.store as store

    def broken_rows(*args, **kwargs):
        return [AiCallRow(started_at=datetime.now(UTC), process="classify", provider="typesafe",
                          model="m", locality="cloud", latency_ms=1, cost_usd=0.0,
                          cost_source="estimate", status="ok", attempt=1, ticket_id=999_999, detail={})]

    monkeypatch.setattr(store, "call_rows", broken_rows)
    start(test_client, ["ok-2"])
    with sf() as session:
        assert session.scalars(select(TicketResultRow)).one().status != "failed"
        assert session.scalars(select(AiCallRow)).all() == []
```

(`make_ticket` accepts `id=` because `Ticket` has an `id` field and `make_ticket` forwards `**kw`.)

- [ ] **Step 3: Run tests to verify they fail**

Run: `uv run pytest tests/telemetry/test_batch_recording.py -q`
Expected: FAIL (`TicketOutcome` has no attribute `ai_calls`).

- [ ] **Step 4: Implement**

In `backend/app/pipeline/contracts.py`, add to `TicketOutcome` (last field):

```python
    ai_calls: tuple = ()  # telemetry AiCall records, written with the result
```

In `backend/app/pipeline/graph.py`, add `from app.telemetry.calls import call_context` and replace `run_batch` with:

```python
async def run_batch(graph: Any, tickets: Sequence[Ticket], *,
                    concurrency: int) -> tuple[list[TicketOutcome], RunSummary]:
    if not tickets:
        return [], summarize([])
    limiter = asyncio.Semaphore(max(1, concurrency))

    async def one(ticket: Ticket) -> TicketOutcome:
        async with limiter:
            with call_context(ticket_id=ticket.id) as calls:
                try:
                    outcome = outcome_from_state(await graph.ainvoke({"ticket": ticket}))
                except Exception as exc:
                    outcome = TicketOutcome(ticket=ticket, status="failed", error=f"{type(exc).__name__}: {exc}")
            return replace(outcome, ai_calls=tuple(calls.calls))

    outcomes = list(await asyncio.gather(*(one(t) for t in tickets)))
    return outcomes, summarize(outcomes)
```

In `backend/app/services/batch_jobs.py`, add `from app.telemetry.calls import call_context`. In `process(ticket)`, wrap the execution so the context covers the graph and the failure path:

```python
    async def process(ticket):
        async with limiter:
            trace, state = [], None
            start = perf_counter()
            execution = TicketExecution(asyncio.timeout(timeout_s))
            token = ticket_execution.set(execution)
            with call_context(run_id=run_id, ticket_id=ticket.id) as calls:
                try:
                    ...  # existing try/except/finally body, unchanged
                finally:
                    ticket_execution.reset(token)
            draft = outcome.draft or DraftResult()
            outcome = replace(outcome, draft=replace(draft, trace=tuple(trace) + draft.trace),
                              ai_calls=tuple(calls.calls))
```

Keep the existing `try:`/`except Exception as exc:`/`finally: ticket_execution.reset(token)` exactly as they are, only indented inside the `with` block.

In `backend/app/db/repository.py`, add imports `from app.telemetry.store import add_calls` and (if missing) `from datetime import UTC, datetime`, then replace `save_outcomes`:

```python
def save_outcomes(session: Session, run_id: int, outcomes: Sequence[TicketOutcome]) -> None:
    now = datetime.now(UTC)
    rows = [{"run_id": run_id, **outcome_to_row(o), "processed_at": now}
            for o in outcomes if o.ticket.id is not None]
    if not rows:
        return
    stmt = insert(TicketResultRow).values(rows)
    updatable = [k for k in rows[0] if k not in ("run_id", "ticket_id")]
    session.execute(stmt.on_conflict_do_update(
        constraint="uq_result_run_ticket", set_={k: stmt.excluded[k] for k in updatable}
    ))
    for outcome in outcomes:
        if outcome.ticket.id is not None and outcome.ai_calls:
            add_calls(session, outcome.ai_calls, run_id=run_id, ticket_id=outcome.ticket.id)
```

The CLI `run-batch` database path already calls `run_batch` and then `save_outcomes`, so it records calls with no further change.

- [ ] **Step 5: Run tests to verify they pass, including existing batch tests**

Run: `uv run pytest tests/telemetry tests/test_graph.py tests/test_workspace_api.py tests/test_cli_run_batch.py tests/test_repository.py tests/models_config/test_batch_timeout.py -q && uv run ruff check app tests`
Expected: all PASS.

- [ ] **Step 6: Commit**

```bash
git add backend/app/pipeline/contracts.py backend/app/pipeline/graph.py backend/app/services/batch_jobs.py backend/app/db/repository.py backend/tests/telemetry
git commit -m "feat: write each ticket's AI calls with its result"
```

---

### Task 4: Record Jev classification and the credential check

**Files:**
- Modify: `backend/app/pipeline/stage2_classify/jev.py`
- Modify: `backend/app/pipeline/stage6_draft/credentials.py`
- Modify: `backend/app/pipeline/factory.py` (pass the Jev model to the checker)
- Test: `backend/tests/telemetry/test_jev_calls.py`

**Interfaces:**
- Consumes: `AiCall`, `Timer`, `record`, `short_error`, `call_context` (Task 1).
- Produces: `JevClassifier.classify` records two `classify` rows (`detail.check` = `main` / `order`); `JevCredentialChecker(runnable, *, price_in_per_m, model="jev")` records one `credential_check` row per check.

- [ ] **Step 1: Write the failing tests**

Create `backend/tests/telemetry/test_jev_calls.py`:

```python
import pytest
from langchain_typesafe.client import TypeSafeError

from app.pipeline.stage1_normalize.candidates import find_candidates
from app.pipeline.stage1_normalize.normalize import normalize
from app.pipeline.stage2_classify.jev import JevClassifier
from app.pipeline.stage6_draft.credentials import JevCredentialChecker
from app.telemetry.calls import call_context
from tests.fakes import FakeJevRunnable
from tests.helpers import make_ticket


async def test_classify_records_main_and_order_calls(tax):
    nt = normalize(make_ticket("حولت 50 الف وما وصلت"))
    classifier = JevClassifier(FakeJevRunnable(), tax, model_id="jev-1.13.0", t_jev=0.6,
                               min_top_prob=0.6, price_in_per_m=0.042, max_state_chars=6000)
    with call_context(run_id=1, ticket_id=1) as calls:
        out = await classifier.classify(nt, find_candidates(nt.match_text))
    assert sorted(c.detail["check"] for c in calls.calls) == ["main", "order"]
    assert all(c.process == "classify" and c.provider == "typesafe" for c in calls.calls)
    assert all(c.input_tokens == 1000 and c.cost_source == "estimate" for c in calls.calls)
    assert sum(c.cost_usd for c in calls.calls) == pytest.approx(out.cost_usd)


async def test_classify_failure_records_an_error_row(tax):
    nt = normalize(make_ticket("سؤال"))
    classifier = JevClassifier(FakeJevRunnable(raises=RuntimeError("down")), tax, model_id="jev-1.13.0",
                               t_jev=0.6, min_top_prob=0.6, price_in_per_m=0.042, max_state_chars=6000)
    with call_context(ticket_id=1) as calls, pytest.raises(RuntimeError):
        await classifier.classify(nt, find_candidates(nt.match_text))
    assert {c.status for c in calls.calls} == {"error"}
    assert calls.calls[0].error == "RuntimeError"


class _Runnable:
    def __init__(self, result):
        self.result = result

    async def ainvoke(self, request):
        if isinstance(self.result, BaseException):
            raise self.result
        return self.result


async def test_credential_check_records_tokens_and_errors():
    ok = {"usage": {"input_tokens": 500}, "nouls": {"requests_credentials": {"noul": 0.05}}}
    checker = JevCredentialChecker(_Runnable(ok), price_in_per_m=0.042, model="jev-1.13.0")
    with call_context(ticket_id=1) as calls:
        check = await checker.check("رد")
    [row] = calls.calls
    assert (row.process, row.input_tokens, row.status) == ("credential_check", 500, "ok")
    assert row.cost_usd == pytest.approx(check.cost_usd)
    failing = JevCredentialChecker(_Runnable(TypeSafeError("bad")), price_in_per_m=0.042)
    with call_context(ticket_id=1) as calls:
        await failing.check("رد")
    assert calls.calls[0].status == "error" and calls.calls[0].model == "jev"
```

If `TypeSafeError("bad")` needs more constructor arguments in the installed version, build it with `TypeSafeError.__new__(TypeSafeError)` and assert the same.

- [ ] **Step 2: Run tests to verify they fail**

Run: `uv run pytest tests/telemetry/test_jev_calls.py -q`
Expected: FAIL (no rows recorded / unexpected `model` keyword).

- [ ] **Step 3: Implement Jev recording**

In `backend/app/pipeline/stage2_classify/jev.py`, import:

```python
from app.telemetry.calls import AiCall, Timer, record, short_error
```

Add a method to `JevClassifier` and use it in `classify`:

```python
    async def _invoke(self, request: dict, check: str) -> Any:
        timer = Timer()
        try:
            response = await self._runnable.ainvoke(request)
        except Exception as exc:
            record(AiCall("classify", "typesafe", self._model_id, "cloud", timer.started_at, timer.ms(),
                          status="error", error=short_error(exc), detail={"check": check}))
            raise
        tokens = _input_tokens(response)
        record(AiCall("classify", "typesafe", self._model_id, "cloud", timer.started_at, timer.ms(),
                      input_tokens=tokens, cost_usd=tokens * self._price / 1e6,
                      cost_source="estimate", detail={"check": check}))
        return response
```

and in `classify` replace the `asyncio.gather(...)` with:

```python
        main, order = await asyncio.gather(
            self._invoke({"state": state, "questions": build_questions(self._tax, cands)}, "main"),
            self._invoke({"state": state, "questions": build_order_check(self._tax)}, "order"),
        )
```

- [ ] **Step 4: Implement credential-check recording**

In `backend/app/pipeline/stage6_draft/credentials.py`, import `from app.telemetry.calls import AiCall, Timer, record, short_error`, add `model: str = "jev"` to `JevCredentialChecker.__init__` (store as `self._model`), and wrap `check`'s runnable call:

```python
        timer = Timer()
        try:
            response = await self._runnable.ainvoke({"state": {"reply_ar": reply}, "questions": questions})
        except TypeSafeError as error:
            explicit = getattr(error, "cost_usd", None)
            cost = explicit if _finite_nonnegative(explicit) else self._cost(getattr(error, "body", None))
            self._record(timer, cost, None, short_error(error))
            return CredentialCheck(None, True, cost)
        except Exception as error:
            self._record(timer, 0.0, None, short_error(error))
            raise
        cost = self._cost(response)
        tokens = _get(_get(response, "usage"), "input_tokens", None)
        self._record(timer, cost, tokens if _finite_nonnegative(tokens) else None, None)
```

with the helper:

```python
    def _record(self, timer: Timer, cost: float, tokens: Any, error: str | None) -> None:
        record(AiCall("credential_check", "typesafe", self._model, "cloud", timer.started_at, timer.ms(),
                      input_tokens=int(tokens) if tokens is not None else None, cost_usd=cost,
                      cost_source="estimate", status="error" if error else "ok", error=error))
```

Keep the rest of `check` (score validation) unchanged.

In `backend/app/pipeline/factory.py` L97 pass the model:

```python
                    credential_checker = JevCredentialChecker(
                        jev_client, price_in_per_m=jev_price, model=models.choice(Step.CLASSIFY).model)
```

- [ ] **Step 5: Run tests**

Run: `uv run pytest tests/telemetry tests/test_jev.py tests/test_credential_check.py tests/test_factory.py -q && uv run ruff check app tests`
Expected: all PASS.

- [ ] **Step 6: Commit**

```bash
git add backend/app/pipeline backend/tests/telemetry/test_jev_calls.py
git commit -m "feat: record Jev classification and credential-check calls"
```

---

### Task 5: Record extraction attempts and keep the cost of failed parses

**Files:**
- Modify: `backend/app/llm.py` (`StructuredChatLLM` records each attempt)
- Modify: `backend/app/models_config/resolver.py` (`structured_llm` passes identity and price knowledge)
- Modify: `backend/app/pipeline/stage3_extract/gemini.py`, `backend/app/pipeline/stage3_extract/extract.py`
- Test: `backend/tests/telemetry/test_extract_calls.py`

**Interfaces:**
- Consumes: Task 1, Task 2 (`ActiveModels.prices`).
- Produces: `StructuredChatLLM(..., process="extract", provider="", model="", local=False, price_known=True)`; each attempt (retries included) records an `extract` row with `attempt`; `GeminiExtractor.extract` raises `LLMUnavailable` with `.cost_usd`; `fill_gaps` returns that cost.

- [ ] **Step 1: Write the failing tests**

Create `backend/tests/telemetry/test_extract_calls.py`:

```python
import httpx
import pytest
from pydantic import BaseModel

from app.llm import LLMUnavailable, StructuredChatLLM
from app.pipeline.contracts import ExtractedField
from app.pipeline.stage1_normalize.normalize import normalize
from app.pipeline.stage3_extract.extract import fill_gaps
from app.telemetry.calls import call_context
from tests.helpers import make_ticket
from tests.telemetry.messages import raw


class _S(BaseModel):
    x: int


class _Chat:
    def __init__(self, results):
        self.results = list(results)

    def with_structured_output(self, schema, **kw):
        return self

    async def ainvoke(self, prompt):
        item = self.results.pop(0)
        if isinstance(item, BaseException):
            raise item
        return item


def llm(results, **kw):
    options = dict(chat_factory=lambda t: _Chat(results), price_in_per_m=1.0, price_out_per_m=2.0,
                   provider="openrouter", model="google/gemini-3.8-flash")
    return StructuredChatLLM(**(options | kw))


async def test_each_attempt_is_recorded():
    results = [httpx.ConnectError("x"), {"raw": raw(1000, 100), "parsed": _S(x=1), "parsing_error": None}]
    with call_context(ticket_id=1) as calls:
        [sample] = await llm(results).sample("p", _S, temperature=0.0)
    assert sample.parsed == _S(x=1)
    assert [(c.attempt, c.status) for c in calls.calls] == [(1, "error"), (2, "ok")]
    assert calls.calls[1].cost_usd == pytest.approx((1000 + 200) / 1e6)
    assert calls.calls[1].cost_source == "estimate" and calls.calls[0].error == "ConnectError"


async def test_unknown_price_and_local_sources():
    ok = {"raw": raw(10, 1), "parsed": _S(x=1), "parsing_error": None}
    with call_context() as calls:
        await llm([ok], price_known=False).sample("p", _S, temperature=0.0)
        await llm([dict(ok)], local=True, provider="ollama", model="qwen3:4b").sample("p", _S, temperature=0.0)
    assert [c.cost_source for c in calls.calls] == ["unknown", "local"]
    assert calls.calls[1].locality == "local"


class _FailingExtractor:
    async def extract(self, nt, fields):
        error = LLMUnavailable("bad json")
        error.cost_usd = 0.003
        raise error


async def test_failed_parse_cost_reaches_the_ticket():
    nt = normalize(make_ticket("حولت فلوس"))
    extracted = {f: ExtractedField(None, None, None, None, "none", 0.0) for f in ("txn_ref", "amount", "phone", "date")}
    _, cost = await fill_gaps(extracted, nt, ["amount"], _FailingExtractor())
    assert cost == pytest.approx(0.003)
```

Create `backend/tests/telemetry/messages.py`:

```python
from langchain_core.messages import AIMessage


def raw(input_tokens=100, output_tokens=20, **metadata):
    return AIMessage("", usage_metadata={"input_tokens": input_tokens, "output_tokens": output_tokens,
                                         "total_tokens": input_tokens + output_tokens},
                     response_metadata=metadata)
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `uv run pytest tests/telemetry/test_extract_calls.py -q`
Expected: FAIL (unexpected keyword `provider`).

- [ ] **Step 3: Implement**

In `backend/app/llm.py`, import `from app.telemetry.calls import AiCall, Timer, cost_for, record, short_error, usage_of`. Extend `__init__` with keyword arguments and store them:

```python
        process: str = "extract",
        provider: str = "",
        model: str = "",
        local: bool = False,
        price_known: bool = True,
```

```python
        self._process, self._provider, self._model = process, provider, model
        self._local, self._price_known = local, price_known
```

Replace `_invoke` with:

```python
    async def _invoke(self, runnable, prompt):
        """Retry transient failures at most max_retries times per sample; record every attempt."""
        for attempt in range(max(0, self._max_retries) + 1):
            timer = Timer()
            try:
                result = await runnable.ainvoke(prompt)
            except Exception as exc:
                self._record(timer, attempt + 1, None, short_error(exc))
                status = getattr(exc, "status_code", None)
                transient = isinstance(exc, httpx.TransportError) or (
                    isinstance(status, int) and (status in (408, 429) or status >= 500)
                )
                if not transient or attempt >= self._max_retries:
                    return exc
                await asyncio.sleep(min(0.5 * 2**attempt, 8.0))
                continue
            parsed_error = None if result.get("parsed") is not None else "ParsingError"
            self._record(timer, attempt + 1, result.get("raw"), parsed_error)
            return result

    def _record(self, timer: Timer, attempt: int, raw: Any, error: str | None) -> None:
        tokens_in, tokens_out, provider_cost = usage_of(raw)
        prices = (self._price_in, self._price_out) if self._price_known else None
        cost, source = cost_for(input_tokens=tokens_in, output_tokens=tokens_out,
                                provider_cost=provider_cost, prices=prices, local=self._local)
        record(AiCall(self._process, self._provider, self._model,
                      "local" if self._local else "cloud", timer.started_at, timer.ms(),
                      input_tokens=tokens_in, output_tokens=tokens_out, cost_usd=cost,
                      cost_source=source, status="error" if error else "ok", error=error,
                      attempt=attempt))
```

In `backend/app/models_config/resolver.py` `structured_llm`, replace the price line and the return:

```python
        prices = self.prices(Step.EXTRACT)
        price_in, price_out = prices or (0.0, 0.0)
        ...
        return StructuredChatLLM(chat_factory=chat_factory, price_in_per_m=price_in,
                                 price_out_per_m=price_out, max_retries=max_retries,
                                 provider=choice.provider, model=choice.model,
                                 local=provider.locality == "local", price_known=prices is not None)
```

In `backend/app/pipeline/stage3_extract/gemini.py`, replace the raise:

```python
        if sample.parsed is None:
            error = LLMUnavailable(sample.error or "extraction failed")
            error.cost_usd = sample.cost_usd
            raise error
```

In `backend/app/pipeline/stage3_extract/extract.py` `fill_gaps`, replace the except branch:

```python
    except LLMUnavailable as exc:
        return extracted, float(getattr(exc, "cost_usd", 0.0) or 0.0)
```

- [ ] **Step 4: Run tests**

Run: `uv run pytest tests/telemetry tests/test_llm.py tests/test_gemini.py tests/test_extract.py tests/models_config/test_resolver.py -q && uv run ruff check app tests`
Expected: all PASS. If an existing test asserted that a failed parse contributes `0.0`, update it to the attempted cost — that is the intended fix (spec §4.4).

- [ ] **Step 5: Commit**

```bash
git add backend/app/llm.py backend/app/models_config/resolver.py backend/app/pipeline/stage3_extract backend/tests/telemetry/test_extract_calls.py backend/tests/telemetry/messages.py
git commit -m "feat: record every extraction attempt and keep failed-parse cost"
```

---

### Task 6: Record drafting model calls with latency

**Files:**
- Modify: `backend/app/pipeline/stage6_draft/agent.py` (`_ModelUsage`)
- Test: `backend/tests/telemetry/test_draft_calls.py`

**Interfaces:**
- Consumes: Task 1; Task 2 (`DraftModelInfo.provider/locality/prices_known`).
- Produces: one `draft` row per recorded model response (same de-duplication as the trace), with latency from `on_chat_model_start`, and one `error` row per failed request without response.

- [ ] **Step 1: Write the failing tests**

Create `backend/tests/telemetry/test_draft_calls.py`:

```python
import pytest

from app.config import Settings
from app.pipeline.stage6_draft.agent import RagDrafter
from app.pipeline.stage6_draft.model_info import DraftModelInfo
from app.telemetry.calls import call_context
from tests.rag_fakes import Checker, Knowledge, ScriptedChat, draft_state, script


def drafter(info=None):
    settings = Settings(_env_file=None, openrouter_api_key="", typesafe_api_key="")
    model = ScriptedChat(steps=script())
    return RagDrafter(settings, model_factory=lambda: model, knowledge=Knowledge(), investigation=object(),
                      credential_checker=Checker(), info=info)


async def test_each_model_response_is_a_draft_row():
    with call_context(run_id=1, ticket_id=1) as calls:
        result = await drafter().draft(draft_state())
    rows = [c for c in calls.calls if c.process == "draft"]
    assert len(rows) == len([e for e in result.trace if e["kind"] == "model"]) == 2
    assert all(r.cost_source == "provider" and r.cost_usd == pytest.approx(0.01) for r in rows)
    assert all(r.input_tokens == 100 and r.output_tokens == 20 and r.latency_ms >= 0 for r in rows)


async def test_local_draft_model_is_free():
    info = DraftModelInfo("qwen3:4b", (0.0, 0.0), 30, "nomic-embed-text", provider="ollama", locality="local")
    with call_context(ticket_id=1) as calls:
        await drafter(info).draft(draft_state())
    rows = [c for c in calls.calls if c.process == "draft"]
    assert {(r.provider, r.locality, r.cost_source, r.cost_usd) for r in rows} == {("ollama", "local", "local", 0.0)}
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `uv run pytest tests/telemetry/test_draft_calls.py -q`
Expected: FAIL (no `draft` rows).

- [ ] **Step 3: Implement**

In `backend/app/pipeline/stage6_draft/agent.py`, import `from app.telemetry.calls import AiCall, Timer, cost_for, count, record`. In `_ModelUsage.__init__` add `self.timers: dict[str, Timer] = {}`. Add:

```python
    async def on_chat_model_start(self, serialized, messages, *, run_id, **kwargs):
        self.timers[str(run_id)] = Timer()

    def _ledger(self, run_id, *, model, usage, reported, error_type=None, cost=None):
        timer = self.timers.pop(str(run_id), None) or Timer()
        tokens_in, tokens_out = count(usage.get("input_tokens")), count(usage.get("output_tokens"))
        local = self.info.locality == "local"
        if cost is None:
            prices = self.info.token_prices if self.info.prices_known else None
            cost, source = cost_for(input_tokens=tokens_in, output_tokens=tokens_out,
                                    provider_cost=reported, prices=prices, local=local)
        else:
            source = "local" if local else "provider" if reported is not None else "unknown"
        record(AiCall("draft", self.info.provider, model, self.info.locality, timer.started_at, timer.ms(),
                      input_tokens=tokens_in, output_tokens=tokens_out, cost_usd=cost, cost_source=source,
                      status="error" if error_type else "ok", error=error_type))
```

Change `on_llm_end` to pass `run_id` into `_record_response(..., run_id=run_id)`, and at the end of `_record_response` (after `self.context.trace.append(entry)`) add:

```python
        reported_cost = float(reported) if source == "provider" else None
        self._ledger(run_id, model=entry["model"], usage=usage, reported=reported_cost,
                     error_type=error_type)
```

Give `_record_response` a `run_id=None` keyword parameter (it already receives `fallback_id`); in `on_llm_error`'s `_has_response_usage` branch pass `run_id=run_id`. In the final branch of `on_llm_error`, after appending the trace entry, add:

```python
        self._ledger(run_id, model=self.info.model, usage={}, reported=None,
                     error_type=type(error).__name__, cost=cost)
```

Existing trace entries and `self.cost_usd` stay exactly as they are.

- [ ] **Step 4: Run tests**

Run: `uv run pytest tests/telemetry tests/test_rag_drafter.py tests/test_draft_model.py tests/test_final_fix_handoff.py -q && uv run ruff check app tests`
Expected: all PASS.

- [ ] **Step 5: Commit**

```bash
git add backend/app/pipeline/stage6_draft/agent.py backend/tests/telemetry/test_draft_calls.py
git commit -m "feat: record each drafting model call with latency"
```

---

### Task 7: Record embeddings — draft search, knowledge indexing and manual search

**Files:**
- Modify: `backend/app/kb/embeddings.py` (`OpenAICompatibleEmbedder` records each request)
- Modify: `backend/app/models_config/providers/openrouter.py`, `backend/app/models_config/providers/ollama.py` (pass provider identity)
- Modify: `backend/app/kb/service.py` (`index_document` context + persist)
- Modify: `backend/app/api/knowledge.py` (search context + persist)
- Test: `backend/tests/telemetry/test_embedding_calls.py`

**Interfaces:**
- Consumes: Task 1 (`embed_process`, `call_context`, `persist_calls`).
- Produces: `OpenAICompatibleEmbedder(..., provider="openrouter", local=False)`; each HTTP request records one row with process from `embed_process()`; `_response_cost(payload, price) -> tuple[float, str, int | None]` (cost, source, tokens).

- [ ] **Step 1: Write the failing tests**

Create `backend/tests/telemetry/test_embedding_calls.py`:

```python
import httpx
import pytest

from app.kb.embeddings import EmbeddingError, OpenAICompatibleEmbedder
from app.telemetry.calls import call_context


def transport(payload, status=200):
    def handler(request):
        return httpx.Response(status, json=payload)
    return httpx.MockTransport(handler)


def vector():
    return [1.0] + [0.0] * 767


def embedder(payload, **kw):
    return OpenAICompatibleEmbedder(model="openai/text-embedding-3-small", dimensions=768,
                                    url="https://x/embeddings", price_per_m=0.02,
                                    transport=transport(payload), **kw)


async def test_draft_search_embedding_is_recorded_with_tokens_and_estimate():
    payload = {"data": [{"index": 0, "embedding": vector()}], "usage": {"prompt_tokens": 50}}
    with call_context(run_id=1, ticket_id=1) as calls:
        batch = await embedder(payload).embed(["سياسة"])
    [row] = calls.calls
    assert (row.process, row.input_tokens, row.cost_source) == ("draft_search", 50, "estimate")
    assert row.cost_usd == pytest.approx(batch.cost_usd)


async def test_indexing_and_provider_cost():
    payload = {"data": [{"index": 0, "embedding": vector()}], "usage": {"prompt_tokens": 50, "cost": 0.001}}
    with call_context(document_id=4) as calls:
        await embedder(payload).embed(["نص"])
    assert (calls.calls[0].process, calls.calls[0].cost_source) == ("kb_index", "provider")


async def test_local_embedder_and_failures():
    payload = {"data": [{"index": 0, "embedding": vector()}]}
    with call_context() as calls:
        await embedder(payload, provider="ollama", local=True).embed(["نص"])
        with pytest.raises(EmbeddingError):
            await OpenAICompatibleEmbedder(model="m", dimensions=768, url="https://x/e",
                                           transport=transport({}, status=500)).embed(["نص"])
    assert (calls.calls[0].process, calls.calls[0].cost_source, calls.calls[0].locality) == (
        "kb_search", "local", "local")
    assert calls.calls[1].status == "error"
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `uv run pytest tests/telemetry/test_embedding_calls.py -q`
Expected: FAIL (unexpected keyword `provider` / no rows).

- [ ] **Step 3: Implement embedder recording**

In `backend/app/kb/embeddings.py`, import `from app.telemetry.calls import AiCall, Timer, embed_process, record`. Change `_response_cost` to also return the source and tokens:

```python
def _response_cost(payload: dict, price_per_m: float) -> tuple[float, str, int | None]:
    usage = payload.get("usage")
    if usage is None:
        usage = {}
    if not isinstance(usage, dict):
        raise EmbeddingError("Embedding provider returned invalid usage or cost.")
    tokens = usage.get("prompt_tokens", usage.get("total_tokens"))
    if tokens is not None and (isinstance(tokens, bool) or not isinstance(tokens, int)):
        raise EmbeddingError("Embedding provider returned invalid token usage.")
    cost = usage.get("cost")
    if cost is None:
        cost = payload.get("cost")
    # A reported zero is real, not a signal to use the fallback estimate.
    if cost is not None:
        return _nonnegative_number(cost), "provider", tokens
    if tokens is None:
        # No token usage means no estimate; do not invent a tokenizer/character estimate.
        return 0.0, "unknown", None
    return _nonnegative_number(_nonnegative_number(tokens) / 1_000_000 * price_per_m), "estimate", tokens
```

Add `provider: str = "openrouter"` and `local: bool = False` to `OpenAICompatibleEmbedder.__init__` (store `self._provider`, `self._local`). In `embed`, replace the loop body:

```python
                for start in range(0, len(texts), EMBEDDING_BATCH_SIZE):
                    batch = texts[start:start + EMBEDDING_BATCH_SIZE]
                    timer = Timer()
                    try:
                        payload = await self._request(client, batch)
                        cost, source, tokens = _response_cost(payload, self._price_per_m)
                    except EmbeddingError:
                        self._record(timer, None, 0.0, "unknown", "EmbeddingError")
                        raise
                    if self._local:
                        cost, source = 0.0, "local"
                    self._record(timer, tokens, cost, source, None)
                    cost_usd = _nonnegative_number(cost_usd + cost)
                    batch_vectors = _ordered_vectors(payload, len(batch), self.dimensions)
                    vectors.extend(batch_vectors)
```

and add:

```python
    def _record(self, timer: Timer, tokens: int | None, cost: float, source: str, error: str | None) -> None:
        record(AiCall(embed_process(), self._provider, self.model, "local" if self._local else "cloud",
                      timer.started_at, timer.ms(), input_tokens=tokens, cost_usd=cost,
                      cost_source=source, status="error" if error else "ok", error=error))
```

In `backend/app/models_config/providers/ollama.py` `embedder(...)`, pass `provider="ollama", local=True` to `OpenAICompatibleEmbedder`. In `providers/openrouter.py` `embedder(...)`, pass `provider="openrouter"`.

Run `uv run pytest tests/test_embeddings.py -q`. If a test unpacked `_response_cost` as a float, update it to `cost, _, _ = _response_cost(...)`.

- [ ] **Step 4: Persist indexing and manual-search calls**

In `backend/app/kb/service.py`, import `from app.telemetry.calls import call_context` and `from app.telemetry.store import persist_calls`. Rename the existing `index_document` to `_index_document` and add:

```python
    async def index_document(self, document_id: int, *, category_tags: list[str] | None = None) -> dict:
        with call_context(document_id=document_id) as calls:
            try:
                return await self._index_document(document_id, category_tags=category_tags)
            finally:
                await asyncio.to_thread(persist_calls, self._sessions, calls.calls,
                                        document_id=document_id)
```

(`KnowledgeService` keeps its session factory in `self._sessions`.) If the document was deleted while indexing, the `document_id` FK insert fails inside `persist_calls`, which logs a warning and drops those rows; that is acceptable.

In `backend/app/api/knowledge.py` `search_knowledge`, wrap the search:

```python
    with call_context() as calls:
        try:
            ...  # existing body unchanged
        finally:
            await run_in_threadpool(persist_calls, request.app.state.session_factory, calls.calls)
```

with imports `from starlette.concurrency import run_in_threadpool`, `from app.telemetry.calls import call_context`, `from app.telemetry.store import persist_calls`.

- [ ] **Step 5: Add an integration check for indexing**

Append to `backend/tests/telemetry/test_embedding_calls.py`:

```python
@pytest.mark.integration
def test_knowledge_search_api_persists_kb_search(monkeypatch):
    from fastapi.testclient import TestClient
    from sqlalchemy import select

    from app.config import Settings
    from app.db.session import make_engine, make_sessionmaker, reset_db
    from app.main import create_app
    from app.telemetry.calls import AiCall, Timer, record
    from app.telemetry.db_models import AiCallRow

    settings = Settings(_env_file=None, openrouter_api_key="k", typesafe_api_key="")
    engine = make_engine(settings.test_database_url)
    reset_db(engine)
    sf = make_sessionmaker(engine)
    with TestClient(create_app(settings, session_factory=sf)) as client:
        async def fake_search(query, *, category=None, k=5):
            timer = Timer()
            record(AiCall("kb_search", "openrouter", "m", "cloud", timer.started_at, 1, cost_usd=0.001,
                          cost_source="provider"))
            from app.kb.contracts import SearchResult
            return SearchResult(passages=(), cost_usd=0.001)

        monkeypatch.setattr(client.app.state.knowledge, "search", fake_search)
        monkeypatch.setattr("app.api.knowledge._require_provider", lambda request: None)
        assert client.post("/api/knowledge/search", json={"query": "سياسة"}).status_code == 200
    with sf() as session:
        assert [r.process for r in session.scalars(select(AiCallRow))] == ["kb_search"]
    engine.dispose()
```

- [ ] **Step 6: Run tests**

Run: `uv run pytest tests/telemetry tests/test_embeddings.py tests/test_kb_service.py tests/test_rag_api.py tests/models_config/test_embedder.py tests/models_config/test_ollama_provider.py -q && uv run ruff check app tests`
Expected: all PASS.

- [ ] **Step 7: Commit**

```bash
git add backend/app/kb backend/app/models_config/providers backend/app/api/knowledge.py backend/tests/telemetry/test_embedding_calls.py
git commit -m "feat: record embedding calls for drafting search, indexing and manual search"
```

---

### Task 8: Record intake calls and link them to the submitted ticket

**Files:**
- Modify: `backend/app/intake/model.py` (`_record` adds provider, locality, kind, start time, cost source, estimate)
- Create: `backend/app/telemetry/intake.py`
- Modify: `backend/app/intake/turns.py` (`finish`, `fail`, `_audit` insert rows)
- Modify: `backend/app/intake/submission.py` (`_create` links rows to run and ticket)
- Test: `backend/tests/telemetry/test_intake_calls.py`

**Interfaces:**
- Consumes: Task 1, Task 2 (`prices_for`).
- Produces:
  - Intake trace entries gain keys `provider`, `locality`, `kind` (`analyze`/`summarize`), `started_at` (ISO), `cost_source`, `cost_estimate_usd`.
  - `app.telemetry.intake.intake_calls(trace: list[dict]) -> list[AiCall]`; `add_intake_calls(session, session_id, trace) -> None`; `link_intake_calls(session, session_id, *, run_id, ticket_id) -> None`.

- [ ] **Step 1: Write the failing tests**

Create `backend/tests/telemetry/test_intake_calls.py`:

```python
import uuid
from datetime import UTC, datetime

import pytest

from app.telemetry.intake import intake_calls

START = datetime(2026, 11, 14, 9, tzinfo=UTC).isoformat()


def entry(**kw):
    return {"model": "google/gemini-3.8-flash", "provider": "openrouter", "locality": "cloud",
            "kind": "analyze", "started_at": START, "latency_ms": 900,
            "usage": {"input_tokens": 1200, "output_tokens": 300}, "cost_usd": 0.002,
            "cost_source": "provider", "cost_estimate_usd": None, "error": None,
            "attempt_id": str(uuid.uuid4())} | kw


def test_provider_cost_entry():
    [call] = intake_calls([entry()])
    assert (call.process, call.provider, call.cost_usd, call.cost_source) == ("intake", "openrouter", 0.002, "provider")
    assert (call.input_tokens, call.output_tokens, call.detail["kind"]) == (1200, 300, "analyze")


def test_intake_call_without_cost_uses_estimate_or_unknown():
    estimated, unknown, local = intake_calls([
        entry(cost_usd=None, cost_source="estimate", cost_estimate_usd=0.0015),
        entry(cost_usd=None, cost_source="unknown"),
        entry(cost_usd=None, cost_source="local", locality="local", provider="ollama"),
    ])
    assert (estimated.cost_usd, estimated.cost_source) == (0.0015, "estimate")
    assert (unknown.cost_usd, unknown.cost_source) == (0.0, "unknown")
    assert (local.cost_usd, local.cost_source) == (0.0, "local")


def test_errors_rejections_and_legacy_entries():
    failed, rejected = intake_calls([entry(error="TimeoutError", usage=None, cost_usd=None,
                                           cost_source="unknown"),
                                     entry(rejected=True, error="InvalidEvidence")])
    assert failed.status == "error" and failed.error == "TimeoutError"
    assert rejected.detail["rejected"] is True
    assert intake_calls([{"model": "m", "latency_ms": 1}]) == []  # entries from before this change


@pytest.mark.integration
def test_submission_links_intake_calls():
    from sqlalchemy import select

    from app.config import Settings
    from app.customers.repository import ensure_customers
    from app.db.models import RunRow, TicketRow
    from app.db.session import make_engine, make_sessionmaker, reset_db
    from app.intake.db_models import IntakeSessionRow
    from app.telemetry.db_models import AiCallRow
    from app.telemetry.intake import add_intake_calls, link_intake_calls

    engine = make_engine(Settings(_env_file=None).test_database_url)
    reset_db(engine)
    sf = make_sessionmaker(engine)
    phone = "07701234567"
    with sf() as session:
        ensure_customers(session, [phone])
        intake = IntakeSessionRow(token_hash="0" * 64, customer_phone=phone, state={})
        session.add(intake)
        session.flush()
        add_intake_calls(session, intake.id, [entry()])
        ticket = TicketRow(external_id=f"INTAKE-{intake.id.hex}", channel="app", customer_phone=phone,
                           text="x", received_at=datetime.now(UTC), source="intake")
        run = RunRow(mode="jev", prompt_version="v1", model_ids={}, status="running")
        session.add_all([ticket, run])
        session.flush()
        link_intake_calls(session, intake.id, run_id=run.id, ticket_id=ticket.id)
        session.commit()
        [row] = session.scalars(select(AiCallRow)).all()
        assert (row.run_id, row.ticket_id, row.intake_session_id) == (run.id, ticket.id, intake.id)
    engine.dispose()
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `uv run pytest tests/telemetry/test_intake_calls.py -q`
Expected: FAIL (`No module named 'app.telemetry.intake'`).

- [ ] **Step 3: Enrich the intake trace**

In `backend/app/intake/model.py`, import `from datetime import UTC, datetime`, `from app.models_config.pricing import prices_for` and `from app.telemetry.calls import cost_for, count`. In `_invoke`, capture the wall-clock start next to `started = time.monotonic()`:

```python
            started_at = datetime.now(UTC)
```

and pass identity into both `_record` calls:

```python
                _record(budget, self._identity(budget, schema), exc, None, started, started_at)
            ...
            _record(budget, self._identity(budget, schema), None, result, started, started_at)
```

Add to `IntakeModel`:

```python
    def _identity(self, budget: ModelBudget, schema: type) -> dict:
        choice = self._choice(budget)
        try:
            locality = self._registry.get(choice.provider).locality
        except Exception:
            locality = "cloud"
        return {"model": choice.model, "provider": choice.provider, "locality": locality,
                "kind": "summarize" if schema is ReviewText else "analyze",
                "prices": prices_for(self.settings, Step.INTAKE, choice, locality)}
```

Replace `_record`:

```python
def _record(budget: ModelBudget, identity: dict, error: Exception | None, result, started: float,
            started_at: datetime) -> None:
    usage = {}
    cost = None
    if isinstance(result, dict):
        raw = result.get("raw")
        usage = dict(getattr(raw, "usage_metadata", None) or {})
        metadata = getattr(raw, "response_metadata", None) or {}
        if metadata.get("cost") is not None:
            cost = float(metadata["cost"])
    estimate, source = cost_for(input_tokens=count(usage.get("input_tokens")),
                                output_tokens=count(usage.get("output_tokens")), provider_cost=cost,
                                prices=identity["prices"], local=identity["locality"] == "local")
    budget.trace.append({
        "model": identity["model"],
        "provider": identity["provider"],
        "locality": identity["locality"],
        "kind": identity["kind"],
        "started_at": started_at.isoformat(),
        "latency_ms": round((time.monotonic() - started) * 1000),
        "usage": usage or None,
        "cost_usd": cost,
        "cost_source": source,
        "cost_estimate_usd": estimate if source == "estimate" else None,
        "error": None if error is None else type(error).__name__,
    })
```

`_model_name` is no longer used by `_invoke`; delete it if nothing else references it (`grep -n _model_name app`).

- [ ] **Step 4: Convert and store**

Create `backend/app/telemetry/intake.py`:

```python
"""Intake model calls arrive as JSON trace entries; store them as ledger rows too."""
from __future__ import annotations

import uuid
from typing import Any

from sqlalchemy import update
from sqlalchemy.orm import Session

from app.datetime import parse_dt
from app.telemetry.calls import AiCall, count, money
from app.telemetry.db_models import AiCallRow
from app.telemetry.store import add_calls


def intake_calls(trace: list[dict[str, Any]]) -> list[AiCall]:
    calls = []
    for item in trace:
        if "provider" not in item or "started_at" not in item:
            continue  # recorded before the ledger existed
        usage = item.get("usage") or {}
        source = item.get("cost_source") or "unknown"
        if source == "provider":
            cost = money(item.get("cost_usd")) or 0.0
        elif source == "estimate":
            cost = money(item.get("cost_estimate_usd")) or 0.0
        else:
            cost = 0.0
        detail = {"kind": item.get("kind")}
        if item.get("rejected"):
            detail["rejected"] = True
        calls.append(AiCall(
            "intake", item["provider"], item["model"], item.get("locality") or "cloud",
            parse_dt(item["started_at"]), int(item.get("latency_ms") or 0),
            input_tokens=count(usage.get("input_tokens")), output_tokens=count(usage.get("output_tokens")),
            cost_usd=cost, cost_source=source, status="error" if item.get("error") else "ok",
            error=item.get("error"), detail=detail,
        ))
    return calls


def add_intake_calls(session: Session, session_id: uuid.UUID, trace: list[dict[str, Any]]) -> None:
    add_calls(session, intake_calls(trace), intake_session_id=session_id)


def link_intake_calls(session: Session, session_id: uuid.UUID, *, run_id: int, ticket_id: int) -> None:
    session.execute(update(AiCallRow).where(AiCallRow.intake_session_id == session_id)
                    .values(run_id=run_id, ticket_id=ticket_id))
```

In `backend/app/intake/turns.py`, import `from app.telemetry.intake import add_intake_calls` and, in each of `finish`, `fail` and `_audit`, immediately after the line that extends `operation.usage`, add (for `_audit`, pass the rejected entries):

```python
            add_intake_calls(session, claim.session_id, self._trace(claim, result.trace))   # finish
            add_intake_calls(session, claim.session_id, self._trace(claim, trace))          # fail
            add_intake_calls(session, claim.session_id,
                             [{**item, "rejected": True} for item in self._trace(claim, trace)])  # _audit
```

In `backend/app/intake/submission.py` `_create`, after `session.flush()` following the placeholder:

```python
        link_intake_calls(session, row.id, run_id=run_id, ticket_id=stored.id)
```

with `from app.telemetry.intake import link_intake_calls`.

- [ ] **Step 5: Run tests**

Run: `uv run pytest tests/telemetry tests/intake -q && uv run ruff check app tests`
Expected: all PASS. If an intake test compares a trace entry dict exactly, update it to include the new keys (they are additive).

- [ ] **Step 6: Commit**

```bash
git add backend/app/intake backend/app/telemetry/intake.py backend/tests/telemetry/test_intake_calls.py
git commit -m "feat: record intake model calls and link them to the submitted ticket"
```

---

### Task 9: Record admin model tests

**Files:**
- Modify: `backend/app/api/admin.py`
- Create: `backend/app/telemetry/probe.py`
- Test: `backend/tests/models_config/test_admin_api.py`

**Interfaces:**
- Consumes: `ProbeResult`, `persist_calls`, `Timer`-free (uses the probe's own latency).
- Produces: `probe_call(step: Step, choice: ModelChoice, result: ProbeResult, locality: str) -> AiCall`; every `POST /models/test` and every test inside `PUT /models/{step}` / embedding switch writes one `probe` row (successful or failed).

- [ ] **Step 1: Write the failing test**

Append to `backend/tests/models_config/test_admin_api.py`:

```python
def test_model_tests_are_recorded(make_client):
    from sqlalchemy import select

    from app.telemetry.db_models import AiCallRow

    with make_client() as client:
        body = {"provider": "ollama", "model": "qwen3:4b", "options": {"think": False}}
        client.post("/api/admin/models/test", headers=HEADERS, json={"step": "draft", **body})
        client.post("/api/admin/models/test", headers=HEADERS,
                    json={"step": "draft", "provider": "ollama", "model": "missing"})
        with client.app.state.session_factory() as session:
            rows = session.scalars(select(AiCallRow).order_by(AiCallRow.id)).all()
        assert [(r.process, r.locality, r.cost_source) for r in rows] == [("probe", "local", "local")] * 2
        assert rows[0].status == "ok" and rows[0].detail == {"step": "draft"}
        assert rows[1].status == "error"
```

(If the fake Ollama provider answers any model, make the second request fail by using `step: "embed"` with `model: "qwen3:4b"` instead; the assertion only needs one failed test.)

- [ ] **Step 2: Run to verify it fails**

Run: `uv run pytest tests/models_config/test_admin_api.py::test_model_tests_are_recorded -q`
Expected: FAIL (no rows).

- [ ] **Step 3: Implement**

Create `backend/app/telemetry/probe.py`:

```python
from __future__ import annotations

from datetime import UTC, datetime, timedelta

from app.models_config.types import ModelChoice, ProbeResult, Step
from app.telemetry.calls import AiCall


def probe_call(step: Step, choice: ModelChoice, result: ProbeResult, locality: str) -> AiCall:
    local = locality == "local"
    return AiCall("probe", choice.provider, choice.model, locality,
                  datetime.now(UTC) - timedelta(milliseconds=result.latency_ms), result.latency_ms,
                  cost_source="local" if local else "unknown", status="ok" if result.ok else "error",
                  error=None if result.ok else (result.error or "failed")[:300],
                  detail={"step": step.value})
```

In `backend/app/api/admin.py`, import `from app.telemetry.probe import probe_call` and `from app.telemetry.store import persist_calls`, and add:

```python
async def _record_probe(request: Request, step: Step, choice: ModelChoice, result) -> None:
    try:
        locality = _store(request).registry.get(choice.provider).locality
    except Exception:
        locality = "cloud"
    await run_in_threadpool(persist_calls, request.app.state.session_factory,
                            [probe_call(step, choice, result, locality)])
```

Call `await _record_probe(request, step, choice, result)` in `_tested` right after `result = await probe(...)` (before the `if not result.ok` check), and in `test_model` right after its probe:

```python
    result = await probe(body.step, choice, _store(request).registry)
    await _record_probe(request, body.step, choice, result)
    return result.to_json()
```

- [ ] **Step 4: Run tests**

Run: `uv run pytest tests/models_config -q && uv run ruff check app tests`
Expected: all PASS.

- [ ] **Step 5: Commit**

```bash
git add backend/app/api/admin.py backend/app/telemetry/probe.py backend/tests/models_config/test_admin_api.py
git commit -m "feat: record admin model tests in the AI call ledger"
```

---

### Task 10: Reports and `/api/ai-usage` endpoints

**Files:**
- Create: `backend/app/telemetry/reports.py`
- Create: `backend/app/api/ai_usage.py`
- Modify: `backend/app/main.py` (register router)
- Modify: `backend/app/api/workspace.py` (`capabilities.evaluation: True`; drop `evaluation` from insights)
- Test: `backend/tests/telemetry/test_reports_api.py`

**Interfaces:**
- Consumes: `AiCallRow`, `TicketResultRow`, `TicketRow`, `RunRow`.
- Produces:
  - `@dataclass(frozen=True) UsageFilter(start: datetime, end: datetime, process: str|None, provider: str|None, model: str|None, run_id: int|None)`; `usage_filter(from_: datetime|None, to: datetime|None, process, model, run_id, *, now=None) -> UsageFilter` (raises `ValueError` for a bad model ref or process)
  - `summary(session, f) -> dict`, `ticket_page(session, f, *, sort: str, limit: int, offset: int) -> dict`, `ticket_calls(session, result_id: int) -> dict | None`
  - Routes: `GET /api/ai-usage/summary`, `GET /api/ai-usage/tickets`, `GET /api/ai-usage/tickets/{result_id}/calls` (query `from`, `to`, `process`, `model`, `run_id`; tickets also `sort`, `limit` ≤ 200, `offset`). Bad filters → 422.
- Response shapes (frontend relies on these exact keys):
  - `summary`: `{"period": {"from", "to"}, "totals": {cost_usd, calls, errors, error_rate, unknown_cost_calls, tickets, cost_per_ticket_avg, cost_per_ticket_p95, ai_time_p50_ms, ai_time_p95_ms, draft_time_p50_ms, draft_time_p95_ms}, "by_process": [Group], "by_model": [Group], "daily": [{date, cost_usd, calls, errors, latency_p95_ms}], "unattributed": {cost_usd, calls, by_process: [Group]}}`
  - `Group`: `{key, process?, provider?, model?, locality?, processes?, calls, cost_usd, cost_share, cost_per_call, latency_p50_ms, latency_p95_ms, error_rate, input_tokens, output_tokens, cost_sources: {source: calls}}`
  - `tickets`: `{"items": [{result_id, ticket_id, external_id, run_id, received_at, processed_at, status, category, cost_usd, intake_cost_usd, total_cost_usd, cost_by_process: {process: usd}, ai_time_ms, draft_time_ms, intake_time_ms, calls, errors, detail_recorded}], "total"}`
  - `ticket calls`: `{"result": <ticket row as above>, "calls": [{id, process, provider, model, locality, started_at, latency_ms, input_tokens, output_tokens, cost_usd, cost_source, status, error, attempt, detail}]}`

- [ ] **Step 1: Write the failing tests**

Create `backend/tests/telemetry/test_reports_api.py`:

```python
from datetime import UTC, datetime, timedelta

import pytest
from fastapi.testclient import TestClient

from app.config import Settings
from app.customers.repository import ensure_customers
from app.db.models import RunRow, TicketResultRow, TicketRow
from app.db.session import make_engine, make_sessionmaker, reset_db
from app.main import create_app
from app.telemetry.db_models import AiCallRow

pytestmark = pytest.mark.integration
NOW = datetime.now(UTC).replace(microsecond=0)
PHONE = "07701234567"


def call(process, model, cost, latency, *, run=None, ticket=None, status="ok", source="provider",
         provider="openrouter", locality="cloud", when=NOW - timedelta(hours=1)):
    return AiCallRow(started_at=when, process=process, provider=provider, model=model, locality=locality,
                     latency_ms=latency, input_tokens=100, output_tokens=10, cost_usd=cost,
                     cost_source=source, status=status, error=None if status == "ok" else "TimeoutError",
                     attempt=1, run_id=run, ticket_id=ticket, detail={})


@pytest.fixture
def seeded():
    settings = Settings(_env_file=None, openrouter_api_key="", typesafe_api_key="")
    engine = make_engine(settings.test_database_url)
    reset_db(engine)
    sf = make_sessionmaker(engine)
    with sf() as s:
        ensure_customers(s, [PHONE])
        run = RunRow(mode="jev", prompt_version="v1", model_ids={}, status="completed", started_at=NOW - timedelta(hours=2))
        s.add(run)
        s.flush()
        tickets = [TicketRow(external_id=f"T-{i}", channel="app", customer_phone=PHONE, text="x",
                             received_at=NOW - timedelta(hours=2), source="upload") for i in range(3)]
        s.add_all(tickets)
        s.flush()
        draft = [{"kind": "draft", "duration_ms": 1500.0}]
        results = [
            TicketResultRow(run_id=run.id, ticket_id=tickets[0].id, status="pending_review", category="failed_transfer",
                            category_probs={}, flags={}, extracted={}, escalation_reasons=[], citations=[],
                            agent_trace=draft, escalated=False, latency_ms=2000, cost_usd=0.012,
                            processed_at=NOW - timedelta(hours=1)),
            TicketResultRow(run_id=run.id, ticket_id=tickets[1].id, status="escalated", category="fraud_report",
                            category_probs={}, flags={}, extracted={}, escalation_reasons=[], citations=[],
                            agent_trace=[], escalated=True, latency_ms=6000, cost_usd=0.002,
                            processed_at=NOW - timedelta(hours=1)),
            TicketResultRow(run_id=run.id, ticket_id=tickets[2].id, status="pending_review", category="other",
                            category_probs={}, flags={}, extracted={}, escalation_reasons=[], citations=[],
                            agent_trace=[], escalated=False, latency_ms=1000, cost_usd=0.5,
                            processed_at=None),  # old result: no ledger rows, falls back to run start
        ]
        s.add_all(results)
        s.flush()
        t0, t1 = tickets[0].id, tickets[1].id
        s.add_all([
            call("intake", "google/gemini-3.8-flash", 0.004, 800, run=run.id, ticket=t0),
            call("classify", "jev-1.13.0", 0.0001, 900, run=run.id, ticket=t0, provider="typesafe", source="estimate"),
            call("draft", "anthropic/claude-sonnet-5.5", 0.010, 1200, run=run.id, ticket=t0),
            call("classify", "jev-1.13.0", 0.0001, 950, run=run.id, ticket=t1, provider="typesafe", source="estimate"),
            call("extract", "qwen3:4b", 0.0, 4000, run=run.id, ticket=t1, provider="ollama", locality="local",
                 source="local", status="error"),
            call("kb_index", "openai/text-embedding-3-small", 0.0002, 300),
            call("probe", "x/y", 0.0, 100, source="unknown"),
            call("classify", "jev-1.13.0", 9.0, 1, when=NOW - timedelta(days=30)),  # outside 7 days
        ])
        s.commit()
        ids = {"run": run.id, "results": [r.id for r in results]}
    client = TestClient(create_app(settings, session_factory=sf, pipeline_builder=lambda *a, **k: None))
    with client:
        yield client, ids
    engine.dispose()


def test_summary_totals_and_groups(seeded):
    client, _ = seeded
    data = client.get("/api/ai-usage/summary").json()
    t = data["totals"]
    assert t["calls"] == 7 and t["errors"] == 1
    assert t["cost_usd"] == pytest.approx(0.004 + 0.0001 + 0.010 + 0.0001 + 0.0002)
    assert t["unknown_cost_calls"] == 1
    assert t["tickets"] == 3
    assert t["ai_time_p50_ms"] == pytest.approx(2000)
    assert t["draft_time_p50_ms"] == pytest.approx(1500)
    processes = {g["process"]: g for g in data["by_process"]}
    assert processes["classify"]["calls"] == 2 and processes["extract"]["error_rate"] == 1.0
    assert processes["classify"]["cost_sources"] == {"estimate": 2}
    models = {g["key"]: g for g in data["by_model"]}
    assert models["ollama:qwen3:4b"]["locality"] == "local"
    assert models["typesafe:jev-1.13.0"]["processes"] == ["classify"]
    assert data["unattributed"]["calls"] == 2
    assert {g["process"] for g in data["unattributed"]["by_process"]} == {"kb_index", "probe"}
    assert sum(d["calls"] for d in data["daily"]) == 7


def test_filters(seeded):
    client, ids = seeded
    only = client.get("/api/ai-usage/summary", params={"process": "classify"}).json()
    assert only["totals"]["calls"] == 2
    local = client.get("/api/ai-usage/summary", params={"model": "ollama:qwen3:4b"}).json()
    assert local["totals"]["calls"] == 1
    run = client.get("/api/ai-usage/summary", params={"run_id": ids["run"]}).json()
    assert run["totals"]["calls"] == 5
    assert client.get("/api/ai-usage/summary", params={"process": "bogus"}).status_code == 422
    assert client.get("/api/ai-usage/summary", params={"model": "no-provider"}).status_code == 422


def test_ticket_rows_include_intake_cost(seeded):
    client, ids = seeded
    page = client.get("/api/ai-usage/tickets", params={"sort": "cost"}).json()
    assert page["total"] == 3
    first = page["items"][0]
    assert first["result_id"] == ids["results"][2] and first["detail_recorded"] is False
    t0 = next(i for i in page["items"] if i["result_id"] == ids["results"][0])
    assert t0["intake_cost_usd"] == pytest.approx(0.004)
    assert t0["total_cost_usd"] == pytest.approx(0.016)
    assert t0["cost_by_process"] == pytest.approx({"intake": 0.004, "classify": 0.0001, "draft": 0.010})
    assert (t0["ai_time_ms"], t0["draft_time_ms"], t0["intake_time_ms"]) == (2000, 1500, 800)
    by_time = client.get("/api/ai-usage/tickets", params={"sort": "time", "limit": 1}).json()
    assert by_time["items"][0]["ai_time_ms"] == 6000 and by_time["total"] == 3
    filtered = client.get("/api/ai-usage/tickets", params={"model": "ollama:qwen3:4b"}).json()
    assert [i["result_id"] for i in filtered["items"]] == [ids["results"][1]]


def test_ticket_timeline(seeded):
    client, ids = seeded
    data = client.get(f"/api/ai-usage/tickets/{ids['results'][0]}/calls").json()
    assert [c["process"] for c in data["calls"]] == ["intake", "classify", "draft"]
    assert data["result"]["external_id"] == "T-0"
    assert client.get("/api/ai-usage/tickets/999999/calls").status_code == 404


def test_empty_period_returns_empty_report(seeded):
    client, _ = seeded
    params = {"from": (NOW + timedelta(days=1)).isoformat(), "to": (NOW + timedelta(days=2)).isoformat()}
    data = client.get("/api/ai-usage/summary", params=params).json()
    assert data["totals"]["calls"] == 0 and data["totals"]["ai_time_p50_ms"] is None
    assert data["by_process"] == [] and data["daily"] == []
    assert client.get("/api/ai-usage/tickets", params=params).json() == {"items": [], "total": 0}


def test_health_reports_the_capability(seeded):
    client, _ = seeded
    assert client.get("/api/health").json()["capabilities"]["evaluation"] is True
```

All three seeded tickets fall in the default 7-day window: two by `processed_at`, the third by its run's `started_at`. Because all three calls of `T-0` happen at the same timestamp, `ticket_calls` must order by `started_at, id` so the insertion order (intake, classify, draft) is kept.

- [ ] **Step 2: Run tests to verify they fail**

Run: `uv run pytest tests/telemetry/test_reports_api.py -q`
Expected: FAIL (404 for `/api/ai-usage/summary`).

- [ ] **Step 3: Implement `app/telemetry/reports.py`**

```python
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
```

Notes for the implementer:
- `percentile_cont` returns `None` over no rows, which is what the empty-period test expects.
- `_ticket_stats` relies on `Select.with_only_columns` keeping the joins added by `_ticket_query`. If SQLAlchemy drops them, build the select explicitly with `select(...).select_from(TicketResultRow).join(TicketRow, ...).join(RunRow, ...)` and the same `where` clauses.

- [ ] **Step 4: Implement the router and wire it**

Create `backend/app/api/ai_usage.py`:

```python
from datetime import datetime
from typing import Annotated, Literal

from fastapi import APIRouter, HTTPException, Query

from app.api.dependencies import SessionDep
from app.telemetry.reports import summary, ticket_calls, ticket_page, usage_filter

router = APIRouter(prefix="/api/ai-usage", tags=["AI usage"])


def _filter(from_: datetime | None, to: datetime | None, process: str | None, model: str | None,
            run_id: int | None):
    try:
        return usage_filter(from_, to, process, model, run_id)
    except ValueError as exc:
        raise HTTPException(422, str(exc)) from None


@router.get("/summary")
def usage_summary(session: SessionDep, from_: Annotated[datetime | None, Query(alias="from")] = None,
                  to: datetime | None = None, process: str | None = None, model: str | None = None,
                  run_id: int | None = None):
    return summary(session, _filter(from_, to, process, model, run_id))


@router.get("/tickets")
def usage_tickets(session: SessionDep, from_: Annotated[datetime | None, Query(alias="from")] = None,
                  to: datetime | None = None, process: str | None = None, model: str | None = None,
                  run_id: int | None = None, sort: Literal["cost", "time", "recent"] = "recent",
                  limit: Annotated[int, Query(ge=1, le=200)] = 50,
                  offset: Annotated[int, Query(ge=0)] = 0):
    return ticket_page(session, _filter(from_, to, process, model, run_id), sort=sort, limit=limit, offset=offset)


@router.get("/tickets/{result_id}/calls")
def usage_ticket_calls(result_id: int, session: SessionDep):
    data = ticket_calls(session, result_id)
    if data is None:
        raise HTTPException(404, "Ticket result not found.")
    return data
```

In `backend/app/main.py`, import `ai_usage` alongside the other routers and add `ai_usage.router` to the `for router in (...)` tuple.

In `backend/app/api/workspace.py`: change `"evaluation": False` to `"evaluation": True` in `health`, and remove `"evaluation": None` from the `insights` response. Then `grep -rn '"evaluation"' backend/tests` and update any assertion of the old values.

- [ ] **Step 5: Run tests and the full backend suite**

Run: `uv run pytest tests/telemetry/test_reports_api.py -q && uv run pytest -q && uv run ruff check app tests`
Expected: all PASS, ruff clean.

- [ ] **Step 6: Commit**

```bash
git add backend/app/telemetry/reports.py backend/app/api/ai_usage.py backend/app/main.py backend/app/api/workspace.py backend/tests
git commit -m "feat: serve AI usage summary, ticket costs and call timelines"
```

Continue with **Part 2**: `docs/superpowers/plans/2026-11-14-ai-usage-dashboard-part2.md`.
