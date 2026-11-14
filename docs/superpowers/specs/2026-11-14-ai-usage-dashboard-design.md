# AI usage and performance dashboard (`/evaluation`) — design specification

- **Date:** 2026-11-14
- **Status:** Design approved in conversation on 2026-11-14; written specification awaiting user review
- **Repository state at design:** `9bae0d5` on `main` (admin model configuration is implemented)
- **Supersedes:** `2026-11-12-model-evaluation-design.md` and its three plan files. Jev remains the only classifier; no language model is evaluated as a classifier.
- **Scope:** A persistent ledger of every AI call, cost and timing fixes at each call site, a reporting API, and a rebuilt, fully translated `/evaluation` page. Also translates the remaining English on the Runs and Run detail pages.

## 1. Outcome and success criteria

`/evaluation` becomes the single place to track AI in the workspace: every AI process and every ticket, measured by **cost** and **time to respond**, broken down by model.

Success means:

1. Every AI call made by the system is stored as one row with process, `provider:model`, start time, latency, tokens in/out, cost, cost source and status, linked to its ticket, run, intake session or knowledge document where one exists.
2. The page answers, for a chosen period (and optionally process, model, run):
   - total AI cost, cost per ticket (average and p95), AI time per ticket (p50 and p95), AI error rate, number of calls;
   - the same figures per AI process and per model;
   - a daily trend of cost and p95 latency;
   - every ticket with its AI cost split by process and its AI time, sortable by cost or time, with a timeline of its AI calls.
3. Cost is never silently invented: each call states whether its cost was reported by the provider, estimated from tokens and a known price, local ($0), or unknown.
4. With the Arabic profile, no English UI text remains on the Evaluation, Runs and Run detail pages (model IDs, ticket IDs and numbers excepted). `en.json` and `ar.json` keep identical keys, enforced by a test.
5. Batch, intake, drafting and knowledge behaviour is otherwise unchanged; recording never makes a ticket fail.
6. Backend tests and lint, and employee-frontend tests, lint, typecheck and build pass.

Not in this phase: measuring accuracy, precision and recall on a labelled held-out set. That is phase 2 and will appear as a "Quality" tab on the same page (section 10).

## 2. Current state

Findings at `9bae0d5`:

| AI process | Call site | Stored today | Missing |
| --- | --- | --- | --- |
| Intake chat (analyze, summarize) | `intake/model.py` L90-151 | `intake_operations.usage[]`: model, latency_ms, usage, provider cost or `null`, error | provider, per-call time, call kind; no estimate when the provider reports no cost |
| Jev classify + order check | `stage2_classify/jev.py` L162-195 | cost folded into `ticket_results.cost_usd` | tokens, latency, errors, per-call rows |
| Extraction gap-fill | `stage3_extract/gemini.py` L54 via `llm.py` | cost folded into `ticket_results.cost_usd` | tokens, latency, whether it ran; cost lost on parse failure and on LangGraph retries |
| Drafting model calls | `stage6_draft/agent.py` `_ModelUsage` L62-117 | `agent_trace` `kind=model`: usage, cost, cost source | latency and time per call |
| Knowledge search during drafting | `stage6_draft/tools.py` L211-221 | `agent_trace` `kind=tool`: duration_ms, cost_usd | tokens, cost source, model |
| Jev credential check | `stage6_draft/credentials.py` L77 | `agent_trace` `kind=guardrail`: cost_usd | tokens, latency |
| Knowledge indexing embeddings | `kb/service.py` L285 | `kb_document_indexes.cost_usd` (cumulative) | duration, tokens, per-attempt rows |
| Manual knowledge search | `api/knowledge.py` L71 | returned, not stored | everything |
| Admin live tests | `models_config/probe.py` | `model_settings_audit.test_latency_ms` on save only | cost, failed tests |

Other findings:

- `ticket_results` has no creation or processing timestamp; `updated_at` changes on review.
- `ticket_results.latency_ms` is the pipeline time from `prepare` to the end of `draft`; the draft summary entry in `agent_trace` has `duration_ms`.
- Intake tickets link to their session through `intake_submissions.ticket_id → session_id`.
- `ActiveModels.token_prices` (`models_config/resolver.py` L92-105) falls back to Gemini Flash prices for any model it does not recognise. The admin catalog knows real OpenRouter prices, but they are display-only.
- `/evaluation` (`features/insights/EvaluationPage.tsx`) is still the import-only placeholder with hardcoded English. `RunDetailPage.tsx` is still mostly hardcoded English.

## 3. Decisions

| Topic | Decision |
| --- | --- |
| Classifier | Jev only; no model comparison for classification |
| Storage | One new table, `ai_calls`, one row per AI call |
| Recording path | One recorder module; call sites record into a per-context buffer that is written with the data it belongs to |
| Historic data | Not backfilled. Older results keep their ticket totals and are marked "detail not recorded" |
| Cost precedence | provider-reported → token estimate with a known price → local $0 → unknown |
| Prices for estimates | Saved with the admin's model choice from the catalog; otherwise `.env` prices; otherwise unknown. No Gemini fallback |
| "AI time" per ticket | Pipeline time (`ticket_results.latency_ms`); drafting time shown separately; intake time = sum of its calls' latency |
| Quality metrics | Phase 2 |
| Translation scope | Evaluation, Runs and Run detail pages |

## 4. Backend design

### 4.1 `ai_calls` table

New SQLAlchemy model in `backend/app/telemetry/db_models.py`, registered before `create_all`:

| Column | Type | Notes |
| --- | --- | --- |
| `id` | bigint primary key | |
| `started_at` | timestamptz, indexed | When the call started |
| `process` | string(32), indexed | See 4.2 |
| `provider` | string(32) | `typesafe`, `openrouter`, `ollama` |
| `model` | string(200), indexed | Provider model ID; the UI shows `provider:model` |
| `locality` | string(8) | `local` or `cloud` |
| `latency_ms` | integer | Wall time of the call |
| `input_tokens`, `output_tokens` | integer, nullable | `null` when the provider gives none |
| `cost_usd` | float | `0.0` when unknown |
| `cost_source` | string(12) | `provider`, `estimate`, `local`, `unknown` |
| `status` | string(8) | `ok` or `error` |
| `error` | string(300), nullable | Exception type and a short message; never prompt or ticket text |
| `attempt` | smallint | 1 for the first try, 2+ for retries |
| `run_id` | FK `runs.id`, nullable, indexed, `ON DELETE SET NULL` | |
| `ticket_id` | FK `tickets.id`, nullable, indexed, `ON DELETE SET NULL` | |
| `intake_session_id` | UUID FK `intake_sessions.id`, nullable, indexed, `ON DELETE SET NULL` | |
| `document_id` | FK `uploaded_documents.id`, nullable, indexed, `ON DELETE SET NULL` | |
| `detail` | JSONB | Small, non-sensitive facts: intake call kind, Jev check (`main`/`order`), tool name, probe step |

`ticket_results` gains a nullable `processed_at` timestamptz (added in `db/workspace_schema.py` with `ALTER TABLE … ADD COLUMN IF NOT EXISTS`), set when the outcome is saved. For older rows the reporting queries use the run's `started_at`.

### 4.2 Processes

| `process` | What it is | Links |
| --- | --- | --- |
| `intake` | Customer intake chat model call (analyze or summarize) | intake session; ticket and run after submission (via `intake_submissions`) |
| `classify` | Jev classification (main call and order check, one row each) | run, ticket |
| `extract` | Gap-fill field extraction, every attempt | run, ticket |
| `draft` | Each drafting-agent model response | run, ticket |
| `draft_search` | Knowledge search embedding inside drafting | run, ticket |
| `credential_check` | Jev credential check on the draft | run, ticket |
| `kb_index` | Embedding request while indexing a document | document |
| `kb_search` | Manual knowledge search from the Knowledge page | none |
| `probe` | Admin live model test | none (`detail.step`) |

### 4.3 Recorder

New package `backend/app/telemetry/` with `recorder.py`:

```python
@dataclass(frozen=True)
class AiCall:
    process: str
    provider: str
    model: str
    locality: str
    started_at: datetime
    latency_ms: int
    input_tokens: int | None
    output_tokens: int | None
    cost_usd: float
    cost_source: str
    status: str = "ok"
    error: str | None = None
    attempt: int = 1
    detail: Mapping[str, object] = field(default_factory=dict)


@dataclass
class CallContext:
    run_id: int | None = None
    ticket_id: int | None = None
    intake_session_id: uuid.UUID | None = None
    document_id: int | None = None
    calls: list[AiCall] = field(default_factory=list)
```

- `current_calls: ContextVar[CallContext | None]`. LangGraph child tasks inherit it, as with the existing `ticket_execution`.
- `record(call)` appends to the current context. Without a context it logs at debug level and drops the call; recording never raises into the caller.
- `call_context(**links)` is a context manager that sets and resets the context.
- `flush(session, context)` inserts the buffered rows in the caller's session, so they are committed with the data they belong to.
- `cost_for(usage, *, provider_cost, prices, local) -> (cost_usd, cost_source)` implements the precedence rule.
- `timed()` returns the start time and a function that returns elapsed milliseconds.

Where contexts are opened and flushed:

| Path | Context | Flushed with |
| --- | --- | --- |
| `services/batch_jobs.py` `process()` per ticket | `run_id`, `ticket_id` | `save_outcomes` in the same transaction, for successful and failed tickets |
| CLI `run-batch` with the database | same | `save_outcomes` |
| CLI `run-batch --no-db` | none | not recorded (no database) |
| `intake/turns.py` per turn | `intake_session_id` | the turn's `intake_operations` write |
| `intake/submission.py` | adds `run_id`, `ticket_id` to that session's existing rows | the submission transaction |
| `kb/service.py` per indexing attempt | `document_id` | the index-state update |
| `api/knowledge.py` search | none set → opened per request | end of the request |
| `models_config/probe.py` (admin test) | per request | end of the request, including failed tests |

### 4.4 Call-site changes

- **Jev** (`jev.py`): time each of the two `ainvoke` calls; record two `classify` rows with input tokens and the estimate from `price_jev_in`. On exception, record an `error` row and re-raise.
- **Extraction** (`llm.py` `StructuredChatLLM`): record every attempt, including parse failures and retries. The cost of a failed attempt is no longer dropped from the ticket's `cost_usd`; `GeminiExtractor` raises with the cost attached and `fill_gaps` adds it.
- **Drafting** (`agent.py` `_ModelUsage`): record start times in `on_chat_model_start` keyed by LangChain run ID, compute latency at the end or error, and record one `draft` row per response. Existing `agent_trace` entries stay unchanged.
- **Draft search** (`tools.py`): record a `draft_search` row from the existing tool result (duration, cost), plus model and cost source from the embedder.
- **Credential check** (`credentials.py`): time the call; record `credential_check` with input tokens and the Jev estimate.
- **Intake** (`intake/model.py` `_record`): also record an `intake` row with provider and model from the pinned choice, `detail.kind` (`analyze`/`summarize`), and an estimate when the provider reports no cost. The existing `usage` JSON is unchanged.
- **Embeddings** (`kb/embeddings.py`, Ollama embedder): return the cost source with the cost; `kb_index` and `kb_search` rows use it.
- **Probe** (`probe.py`): record a `probe` row for every test.

### 4.5 Prices for estimates

- When the admin saves a model (`PUT /api/admin/models/{step}`, and the embedding switch), the catalog entry's `price_in_per_m` and `price_out_per_m` are saved in the choice's `options` as `price_in_per_m` / `price_out_per_m`. These are visible in the change dialog, as today.
- `ActiveModels.token_prices(step)` returns `tuple[float, float] | None`:
  1. local provider → `(0.0, 0.0)`;
  2. prices saved with the choice → those;
  3. the `.env` default choice for that step → the matching `.env` prices (existing rules for Jev, embeddings, draft, extract and intake);
  4. otherwise → `None` (cost source `unknown`).
- Existing callers that expect a tuple treat `None` as `(0.0, 0.0)` for their running totals and mark the cost unknown in the trace.

### 4.6 Reporting API

New router `backend/app/api/ai_usage.py`. Every endpoint accepts `from`, `to` (ISO timestamps; default the last 7 days), and optional `process`, `model` (`provider:model`) and `run_id`.

| Method and path | Returns |
| --- | --- |
| `GET /api/ai-usage/summary` | `totals`, `by_process[]`, `by_model[]`, `daily[]`, `unattributed` |
| `GET /api/ai-usage/tickets` | `{items, total}` of ticket results; `sort` = `cost` \| `time` \| `recent` (default `recent`); `limit` ≤ 200, `offset` |
| `GET /api/ai-usage/tickets/{result_id}/calls` | `{result, calls[]}`, ordered by `started_at`, including the intake session's calls |

`totals`:

- `cost_usd`, `calls`, `errors`, `error_rate`, `unknown_cost_calls`
- `tickets`, `cost_per_ticket_avg`, `cost_per_ticket_p95`
- `ai_time_p50_ms`, `ai_time_p95_ms` (over `ticket_results.latency_ms`), `draft_time_p50_ms`, `draft_time_p95_ms`

`by_process[]` and `by_model[]` rows:

- `process` or `{provider, model, locality}`
- `calls`, `cost_usd`, `cost_share`, `cost_per_call`
- `latency_p50_ms`, `latency_p95_ms`, `error_rate`
- `input_tokens`, `output_tokens`, `cost_sources{}`
- `by_model` rows also carry the processes the model served

`daily[]`: `{date, cost_usd, calls, latency_p95_ms, errors}`, with dates in Baghdad time.

`unattributed`: cost and calls for `kb_index`, `kb_search` and `probe`, which belong to no ticket. These are included in `totals.cost_usd` but not in cost per ticket.

Ticket rows:

- `result_id`, `ticket_id`, `external_id`, `run_id`, `received_at`, `processed_at`, `status`, `category`
- `cost_usd` (pipeline, from `ticket_results`), `intake_cost_usd`, `total_cost_usd`
- `cost_by_process{}`
- `ai_time_ms`, `draft_time_ms`, `intake_time_ms`
- `calls`, `errors`
- `detail_recorded` (false when the result has no `ai_calls` rows)

Percentiles use Postgres `percentile_cont`. The period filter uses `ai_calls.started_at` for call figures and `processed_at` (falling back to the run's `started_at`) for ticket figures.

`/api/health` reports `capabilities.evaluation: true`. `/api/insights` drops its unused `evaluation` field.

## 5. Frontend design

### 5.1 Page

`src/features/evaluation/` replaces `features/insights/EvaluationPage.tsx`; the route stays `/evaluation` and the nav label stays "Evaluation / التقييم". The page description changes to "Cost and response time of every AI process" / "تكلفة وزمن استجابة كل عملية ذكاء اصطناعي".

Layout, top to bottom:

1. **Filters bar:** period (24 hours / 7 days / 30 days), AI process, model, batch run, and a refresh button. Data refreshes automatically every 30 seconds.
2. **Headline cards:** total AI cost, cost per ticket (average, with p95 as detail), AI time per ticket (p50, with p95 as detail), AI error rate, AI calls.
3. **By AI process:** a table with calls, cost, share bar, cost per call, p50/p95 latency, error rate and tokens in/out.
4. **By model:** the same columns per `provider:model`, with badges **Local · $0** (Ollama) and **Production** (the currently active model for a step, from `health.ai`), plus the processes each model served.
5. **Daily trend:** small SVG bar chart of cost per day, with p95 latency as a line. No new chart dependency.
6. **Tickets:** a paginated table with ticket ID, received time, status, category, total AI cost, a stacked cost bar by process, AI time, drafting time and errors. It sorts by cost, time or recency. Rows with `detail_recorded = false` show totals with the note "Detail not recorded (processed before tracking)".
7. **Ticket timeline drawer** (opened from a row): a waterfall of the ticket's AI calls in order (intake turns, then classify, extract, draft, draft search, credential check). Each bar is positioned by start time and sized by latency, and shows model, tokens, cost and cost source, with errors highlighted.
8. **Not tied to a ticket:** cost and calls for knowledge indexing, manual knowledge search and model tests.

Cost source is shown wherever cost appears: an "estimated" marker, **Local · $0**, or "—" with a tooltip for unknown.

### 5.2 Components and data

| File | Responsibility |
| --- | --- |
| `EvaluationPage.tsx` | Filters state, data loading through `useResource`, layout |
| `usage-view.ts` | Pure helpers: query strings, period ranges, share bars, cost-source labels, waterfall geometry |
| `UsageFilters.tsx` | Period, process, model, run selectors |
| `UsageHeadline.tsx` | Headline cards |
| `ProcessTable.tsx`, `ModelTable.tsx` | Breakdown tables |
| `DailyTrend.tsx` | SVG chart with an accessible table fallback |
| `TicketCostTable.tsx` | Ticket list with sorting and pagination |
| `TicketTimeline.tsx` | Drawer with the call waterfall |
| `UnattributedCard.tsx` | Knowledge and test costs |

`src/lib/api.ts` gains `aiUsageApi` (`summary`, `tickets`, `ticketCalls`); `src/lib/types.ts` gains the matching types. Formatters `usd`, `msLabel`, `percent1` and `countLabel` go in `src/lib/format.ts`.

### 5.3 Text and direction

- Every string goes under `evaluation.*` in `en.json` and `ar.json`. Process names go under `evaluation.processes.*`.
- Model IDs and ticket IDs render inside `<bdi dir="ltr">`; numbers use Latin digits, as elsewhere in the workspace.
- New test `src/locales/locales.test.ts` checks identical keys and no empty values.
- `RunsPage.tsx` and `RunDetailPage.tsx`: the remaining hardcoded strings move to `runs.*` and `runDetail.*`.

## 6. Error handling

| Situation | Behaviour |
| --- | --- |
| Recording or flushing fails | Logged as a warning; the ticket, turn, index or test continues and is saved as today |
| Provider gives no usage and no cost | Row stored with `null` tokens and `cost_source = unknown`; the UI shows "—" |
| A call raises | `error` row with type and a short message, then the original exception continues as today |
| Ticket fails mid-pipeline | Calls made so far are flushed with the failed outcome |
| Batch interrupted by an API restart | Calls of tickets not yet saved are lost, as their outcomes are; nothing partial is written |
| Old results without rows | Shown with ticket totals and "detail not recorded" |
| Period with no data | Empty states per section; no zeros presented as measurements |
| API offline | The existing error state with retry |

## 7. Privacy

`ai_calls` never stores prompts, ticket text, customer messages or model output. `error` holds only the exception type and a message truncated to 300 characters; provider messages that may echo input are reduced to their type.

## 8. Testing

**Backend (pytest; no real model calls)**

- `tests/telemetry/test_recorder.py`: cost precedence; context buffering and reset; no-context drop; flush inserts rows; failures in flush are swallowed and logged.
- Call-site tests with fakes:
  - Jev records two rows and an error row on failure.
  - Extraction records each attempt, and the cost of a failed parse now reaches `cost_usd`.
  - Drafting `_ModelUsage` records latency per response (scripted chat from `tests/rag_fakes.py`).
  - Draft search and credential check record rows.
  - Intake records rows with provider and estimate.
  - Knowledge indexing records `kb_index` rows; a probe records a row for a failed test.
- `tests/test_resolver.py`: saved catalog prices win; unknown models return `None`; no Gemini fallback.
- `tests/api/test_ai_usage.py` (`integration`, Postgres):
  - summary totals, per-process and per-model figures and percentiles on a seeded ledger;
  - period, process, model and run filters;
  - ticket list sorting, pagination and intake attribution;
  - timeline order;
  - unattributed totals;
  - `detail_recorded = false` for old results.
- Batch integration: a run through the fake pipeline writes `ai_calls` with the right `run_id`/`ticket_id` and sets `processed_at`.

**Employee frontend (Vitest, static rendering)**

- Locale key parity.
- `usage-view.ts` helpers: period ranges, share bars, waterfall geometry, cost-source labels.
- The page renders headline cards, both tables, the trend, the ticket table and the unattributed card from fixtures, in Arabic and English, with no English UI text in Arabic.
- Ticket timeline renders bars in order with error styling.
- Runs and Run detail render in Arabic without the previously hardcoded English.

**Manual check**

1. Run a small batch and one customer intake through to a ticket.
2. Open `/evaluation` in Arabic:
   - the ticket shows intake plus pipeline cost by process and its AI time;
   - its timeline lists every call;
   - totals match the run's cost.
3. Switch extract or draft to `ollama:qwen3:4b` in the admin page, run a batch, and confirm the model appears with **Local · $0** and its latency.

## 9. Out of scope

- Accuracy, precision and recall on a labelled dataset (phase 2).
- Backfilling `ai_calls` from historic traces.
- Budgets, alerts and cost limits.
- GPU-time or power cost for local models.
- Exporting the ledger (CSV/JSON) — can be added later.

## 10. Phase 2 (for reference, not designed here)

A "Quality" tab on the same page. It would generate a labelled synthetic Iraqi-dialect dataset (200 dev / 100 locked test) and measure Jev classification, flags, escalation and field extraction with accuracy, precision, recall and F1, reusing the ledger for cost and time. Section 4.5 of the superseded spec describes the dataset approach.
