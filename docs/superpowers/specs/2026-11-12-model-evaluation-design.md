# Per-model evaluation (quality, system, cost) — design specification

- **Date:** 2026-11-12
- **Status:** Superseded on 2026-11-14 by `2026-11-14-ai-usage-dashboard-design.md` (Jev stays the only classifier; the labelled-dataset approach in §4.5 is kept for phase 2)
- **Repository state at design:** `cbad948` on `main`
- **Depends on:** `2026-11-12-admin-model-config-design.md` (provider adapters only — see 4.1)
- **Scope:** Labelled synthetic dataset, pluggable LLM classifier, evaluation runner and metrics, evaluation API, a rebuilt `/evaluation` page, and full Arabic/English text for the Evaluation, Runs and Run detail pages

## 1. Outcome and success criteria

The `/evaluation` page today only renders a JSON file the user imports; nothing is measured by the system, it ignores the models actually in use (Jev, Gemini, Claude Sonnet) and local Ollama models, and most of its text is hardcoded English even in the Arabic profile.

After this work, the team can compare models on the same held-out tickets, through the same production pipeline, and see for each model:

- **Task quality:** accuracy, precision, recall and F1 for issue category, flags, field extraction and escalation.
- **System behaviour:** response time (p50/p95) and error rate.
- **Cost per request:** from tokens used and API prices; local Ollama models show **$0 (local)** plus latency and tokens/second.

Success means:

1. `support eval-generate` produces a committed, labelled dataset of 300 synthetic Iraqi-dialect tickets (200 dev / 100 test) with linked transactions, and a committed `test.sha256`.
2. An evaluation can be started from the page (**Run evaluation**) or the CLI (`support eval`), for any subset of the configured models and either split, after showing an estimated cost.
3. The page shows a model comparison table and per-model detail (per-category metrics, confusion matrix with drill-down, flags, extraction, slices) from stored results.
4. `jev`, `openrouter:anthropic/claude-sonnet-5.5`, `openrouter:google/gemini-3.8-flash` and `ollama:qwen3:4b` can all be evaluated.
5. With the Arabic profile, no English text remains on the Evaluation, Runs and Run detail pages (model IDs, JSON and metric abbreviations in tooltips excepted). `en.json` and `ar.json` have identical keys, enforced by a test.
6. Backend tests and lint, and employee-frontend tests, lint, typecheck and build pass. No test calls a real model.

## 2. Current state

Findings from the code at `cbad948`:

- `employee-frontend/src/features/insights/EvaluationPage.tsx` reads an imported JSON report (validated by `validateEvaluation` in `src/lib/imports.ts`) into React state. There is no API. Only the title and description are translated; about 35 strings are hardcoded English (including the static "Classification strategy: Jev" card and the "Topic 06 brief" checklist). The JSON example `<pre>` has no `dir="ltr"`.
- `/api/insights` returns `evaluation: null`; `/api/health` returns `capabilities.evaluation: false` (`backend/app/api/workspace.py`).
- `src/features/runs/RunsPage.tsx` is partly translated; `RunDetailPage.tsx` does not use `useCopy` at all.
- Translations: `src/lib/locale.tsx` with `src/locales/{en,ar}.json` (437 keys each, matching today, no parity test). Arabic is the default.
- Pipeline (`backend/app/pipeline/graph.py`): `prepare → jev_classify → extract → lookup → decide → draft`. `PipelineDeps.jev` is typed as the `Classifier` protocol (`stage2_classify/base.py`), so any classifier returning `ClassifierOutput` can be plugged in. `build_pipeline` (`factory.py`) always constructs `JevClassifier`. `InMemoryTransactionRepo` exists in `stage4_lookup/lookup.py`.
- `stage5_decide/rules.py::decide` is deterministic from category, classifier output (flags thresholded at 0.5, reasons), extracted fields and lookup result.
- Usage: per-ticket `latency_ms`, `cost_usd`, `error` and `agent_trace` are stored; Jev counts input tokens only and Gemini gap-fill does not expose token counts. Prices live in `config.py` (`price_jev_in`, `price_gemini_flash_in/out`, `price_anthropic_in/out`); OpenRouter-reported cost overrides estimates.
- No labelled dataset, split or evaluation script exists (planned in `2026-10-07-support-pipeline-design.md` §7 but never built).
- The admin model-config spec (same date, not yet implemented) defines `backend/app/models_config/providers/{openrouter,ollama,typesafe}.py`, `OLLAMA_BASE_URL`, a `think` option and `provider:model` identifiers.

## 3. Decisions

| Topic | Decision |
| --- | --- |
| Ground truth | Synthetic labelled set; labels come from code, not from a model |
| Tasks benchmarked | Category classification, field extraction, escalation and flags. Drafting is not benchmarked. |
| Comparison method | Swap only the classify stage (approach A); extraction, lookup and decide stay identical for every model |
| Ticket-text generator | An OpenAI GPT model via OpenRouter (a family not under test); bias disclosed in the data card |
| Local model cost | Shown as $0 labelled "local"; latency and tokens/second reported instead |
| Local model | `qwen3:4b` on the user's Windows Ollama, thinking off |
| How evals run | From the UI (background job with progress) and from the CLI; results stored in Postgres |
| Provider layer | Reuse the admin spec's provider adapters; build that subset first if it has not landed |
| i18n scope | Evaluation page, plus Runs and Run detail pages |

## 4. Backend design

### 4.1 Prerequisite: shared provider adapters

The evaluation uses the provider layer defined in the admin model-config spec (§4.1–4.2) and builds **only this subset** if that project has not landed yet, exactly as that spec defines it so nothing is reworked later:

- `models_config/providers/base.py` — the `Provider` protocol (`name`, `locality`, `status()`, `chat_model(...)`, `provider_errors()`, `response_cost(...)`).
- `providers/openrouter.py` — `chat_model` (taking over the OpenRouter conventions from `llm.py`), `status()` (`ready` / `missing_key`), `response_cost` from `response_metadata["cost"]`.
- `providers/ollama.py` — `ChatOllama` from `langchain-ollama` with `reasoning=False` when `think` is off; `status()` from `GET /api/tags` (`ready` / `unreachable`), plus `has_model(name)` from the same response.
- `providers/registry.py` — provider name → adapter.
- Settings: `OLLAMA_BASE_URL` (default `http://localhost:11434`), documented for WSL (mirrored networking, or `OLLAMA_HOST=0.0.0.0` with the Windows host IP) and Docker (`host.docker.internal`, `extra_hosts`).

Catalog discovery, the admin store/API/page and embeddings are **not** part of this work.

### 4.2 Usage metering

New module `backend/app/eval/usage.py`:

```python
@dataclass(frozen=True)
class CallUsage:
    role: str            # "classify" | "extract"
    model: str           # "provider:model", e.g. "ollama:qwen3:4b"
    input_tokens: int | None
    output_tokens: int | None
    latency_ms: int
    cost_usd: float
    cost_source: str     # "provider" | "estimate" | "local"
    tokens_per_s: float | None   # Ollama only: eval_count / eval_duration
    error: str | None
```

A `UsageMeter` (one per ticket per model, passed through a `contextvars.ContextVar` so stage code is not re-plumbed) collects `CallUsage` records. Changes to emit them:

- `JevClassifier`: records each TypeSafe call (input tokens as today; output tokens `None`).
- `GeminiStructuredLLM`: reads `usage_metadata` (input/output tokens) and provider cost from the response it already receives.
- `LlmClassifier` (4.3): records every attempt.
- Ollama timings come from the `ChatOllama` response metadata (`prompt_eval_count`, `eval_count`, `eval_duration`).

Cost rule: provider-reported cost wins (`cost_source="provider"`); otherwise tokens × configured price (`"estimate"`); Ollama is always `0.0` with `"local"`. Outside an evaluation the meter is absent and recording is a no-op, so batch runs are unaffected.

### 4.3 `LlmClassifier`

New `backend/app/pipeline/stage2_classify/llm.py`, implementing the `Classifier` protocol for any chat model obtained from `Provider.chat_model(model, temperature=0, ...)`.

- Prompt `stage2_classify/prompts/llm_classify_v1.md`: the 12 taxonomy categories with descriptions and examples from `data/taxonomy.yaml`, priority P1–P4 definitions, the six flags (`FLAG_NAMES`) with definitions, field-pick rules (choose one of the supplied candidates per field or none), and Iraqi Arabic / Arabizi / mixed-language guidance. Input is truncated to `max_state_chars`, like Jev.
- Structured output schema: `category` (enum of 12), `category_confidence` (0–1), `priority` (enum), `flags` (object of six booleans), `picks` (per field: candidate index or null).
- Mapping to `ClassifierOutput`: `category_probs = {category: confidence}`; flags become `1.0`/`0.0`; a chosen candidate becomes `FieldPick(value=<candidate span>, confidence=category_confidence, method="llm_pick")` (resolved by `stage3_extract/extract.py` through its verbatim-span branch, since candidate spans are substrings of `match_text`), and no choice becomes `FieldPick(None, 0.0, "none")` so the Gemini gap-fill runs under exactly the same rule as for Jev; an out-of-range index counts as invalid output; `source` and `model` are the `provider:model` ID; `path="llm"`.
- `uncertain` and reason `low_confidence` when `category_confidence < T_JEV` (same threshold as Jev, so escalation is comparable). The page notes that LLM confidence is self-reported and uncalibrated.
- Invalid or schema-violating output → one retry; if it fails again, return `uncertain=True`, reason `llm_unavailable`, `degraded=True`, category `other`, and record the error.

`build_pipeline` gains an optional `classifier: Classifier | None` argument; when supplied it is used instead of constructing `JevClassifier`.

### 4.4 Evaluation model list

New setting `EVAL_MODELS` (comma-separated `provider:model`, plus the literal `jev`), default:

```
jev,openrouter:anthropic/claude-sonnet-5.5,openrouter:google/gemini-3.8-flash,ollama:qwen3:4b
```

`app/eval/models.py` resolves each entry to a classifier factory and prices: `jev` → `JevClassifier` with `price_jev_in`; OpenRouter Anthropic models → `price_anthropic_in/out`; OpenRouter Gemini models → `price_gemini_flash_in/out`; any other OpenRouter model → provider-reported cost only (`estimate` unavailable, shown as "—" until a provider cost arrives); Ollama → 0, local. Availability per entry: `ready`, `missing_key` (TypeSafe/OpenRouter key absent), `unreachable` (Ollama down) or `model_missing` (not pulled).

### 4.5 Dataset (`data/eval/`)

Generated by `support eval-generate` (module `app/eval/generate/`), run once, outputs committed:

1. **Scenario sampler** (pure code, seed 42): 300 specs, 25 per category. Each spec: category, priority, gold flags, gold fields (`txn_ref`, `amount`, `phone`, `date`, any of which may be absent or deliberately misstated), channel, `received_at` spread over 4 weeks, and edge-case tags: Arabizi ~10%, Arabic+English ~15%, multi-issue ~8%, missing details ~15%, prompt injection ~3%; untargeted: angry, Arabic-Indic digits, amounts in words, typos.
2. **Transactions** (pure code): per spec, the linked transaction plus 0–3 distractors for the same phone, or no transaction (to produce `not_found`), or a record whose amount/date differs from the ticket (to produce mismatches). Written to `data/eval/transactions.jsonl`.
3. **Ticket text**: `EVAL_GENERATOR_MODEL` (an OpenAI GPT model on OpenRouter; the exact ID is set in `.env.example` at implementation time from OpenRouter's catalogue) writes the ticket in the requested dialect/style from the spec. Code verifies every non-null gold field value appears verbatim (after the pipeline's digit normalisation) in the text; on failure it regenerates up to 2 times, then sets that gold value to `null` and records it.
4. **Gold escalation**: computed by calling `rules.decide` with the gold category, a `ClassifierOutput` built from the gold flags (no `low_confidence`), gold extracted fields and the gold lookup result (`InMemoryTransactionRepo` lookup on gold fields). Stored as `gold.escalated` and `gold.reasons`.
5. **Split**: stratified by category, seed 42 → `dev.jsonl` (200), `test.jsonl` (100); `test.sha256` committed.
6. **Data card** `data/eval/data-card.md`: generator model and date, tag shares, regenerate/null counts, the known-bias note, and a section for the team's 50-ticket realism hand-check (1–5).

Each JSONL row: `{id, text, received_at, channel, customer_phone, tags[], gold: {category, priority, flags{}, fields{}, escalated, reasons[]}}`.

### 4.6 Runner

`backend/app/eval/runner.py`:

- Verifies the split file; for `test`, refuses to run if the SHA-256 does not match `test.sha256`.
- For each selected model: builds the pipeline via `build_pipeline(..., classifier=<model's classifier>, txn_repo=InMemoryTransactionRepo(<dataset transactions>), drafter=NullDrafter("evaluation"))`, then processes the split with an `asyncio.Semaphore` per provider (Ollama 1, OpenRouter and TypeSafe 4) and the existing per-ticket timeout.
- Per ticket: sets a fresh `UsageMeter`, runs the graph, measures end-to-end latency, and writes an `eval_predictions` row with the predicted category, priority, flags, extracted fields, escalation decision and reasons, usage records, cost and error.
- Updates `eval_runs.progress` after each ticket; checks a cancel flag between tickets.
- **Early stop per model:** if more than 5 of the first 10 tickets for a model error, that model is marked `failed` with the most common error, and the run continues with the other models.
- When a model finishes, computes its metrics (4.7) into `eval_runs.summary[model]`.
- Only one evaluation may be `queued` or `running` at a time.
- Started from the API via the same background-thread pattern as `services/batch_jobs.py::run_job`. On API startup, any run left `running` is marked `failed` with error `interrupted`.

### 4.7 Metrics

`backend/app/eval/metrics.py`, pure functions over gold/predicted pairs. An errored ticket counts as wrong for quality metrics and is also counted in the error rate.

| Group | Metrics |
| --- | --- |
| Classification | accuracy with Wilson 95% interval; macro precision, recall, F1; per-category precision, recall, F1, support; 12×12 confusion matrix; priority exact and within-one accuracy |
| Flags | per-flag precision, recall, F1, support (fraud recall is the headline) |
| Extraction | per-field precision and recall (exact match after the pipeline's normalisation), micro F1 across fields, hallucination rate (value predicted where gold is null), missed-field rate |
| Escalation | precision, recall, F1 (positive = escalated), escalation rate, accuracy on non-escalated tickets |
| System | p50, p95 and mean latency (classifier calls and end-to-end), error rate, invalid-output rate, mean input/output tokens per request, mean tokens/second (Ollama) |
| Cost | mean cost per request for the classifier and for the whole pipeline (classifier + Gemini gap-fill), total run cost, projected cost per 1,000 tickets, cost source mix |
| Slices | accuracy and error rate per edge-case tag |

Precision/recall with a zero denominator is reported as `null` (shown "—"), never 0 or 1.

### 4.8 Cost estimate

`app/eval/estimate.py`: for each model, `tickets × (mean input tokens × price_in + mean output tokens × price_out)`. Mean tokens come from that model's most recent completed evaluation; without one, input = prompt token count (characters / 3.5 for Arabic-heavy text) + mean ticket length, output = 120 tokens. Ollama is 0. Models without known prices show "unknown". The estimate is labelled approximate.

### 4.9 Storage

New SQLAlchemy models (`backend/app/eval/db_models.py`), registered before `create_all`:

`eval_runs`

| Column | Type | Notes |
| --- | --- | --- |
| `id` | bigint primary key | |
| `status` | string | `queued`, `running`, `completed`, `failed`, `cancelled` |
| `split` | string | `dev` or `test` |
| `dataset_sha256` | string | Hash of the split file used |
| `prompt_version` | string | e.g. `llm_classify_v1` plus Jev model version |
| `models` | JSONB | List of `provider:model` IDs |
| `model_status` | JSONB | Per model: `pending`, `running`, `completed`, `failed` + error |
| `progress` | JSONB | Per model `{done, total}` |
| `estimated_cost_usd`, `actual_cost_usd` | numeric | |
| `summary` | JSONB | Per model metrics (4.7) |
| `triggered_by` | string | `ui` or `cli` |
| `cancel_requested` | boolean | |
| `error` | text, nullable | |
| `created_at`, `started_at`, `finished_at` | timestamptz | |

`eval_predictions`

| Column | Type |
| --- | --- |
| `id` | bigint primary key |
| `eval_run_id` | FK → `eval_runs.id`, indexed |
| `model` | string, indexed with `eval_run_id` |
| `ticket_id` | string |
| `gold` | JSONB |
| `predicted` | JSONB |
| `correct_category` | boolean |
| `latency_ms` | integer |
| `usage` | JSONB (list of `CallUsage`) |
| `cost_usd` | numeric |
| `error` | text, nullable |

### 4.10 API

New router `backend/app/api/evaluations.py`:

| Method and path | Purpose |
| --- | --- |
| `GET /api/evaluations/models` | `EVAL_MODELS` entries with provider, locality, prices and availability |
| `POST /api/evaluations/estimate` | Body `{models, split}` → per-model and total estimate |
| `POST /api/evaluations` | Body `{models, split}` → the new run (`409` if one is active; `422` if a model is unavailable or the test hash mismatches, with a machine-readable code and the model) |
| `POST /api/evaluations/{id}/cancel` | Requests cancellation |
| `GET /api/evaluations?limit=20` | Recent runs (without `summary`) |
| `GET /api/evaluations/{id}` | Run with `summary`, `progress`, `model_status` |
| `GET /api/evaluations/{id}/predictions?model=&gold=&predicted=&correct=&limit=&offset=` | Drill-down rows, joined with the ticket text from the dataset |

`/api/health` reports `capabilities.evaluation: true`. `/api/insights` drops the unused `evaluation` field (the frontend `Insights` type is updated accordingly).

Error codes for `422`: `model_unavailable`, `unknown_model`, `test_split_modified`, `dataset_missing`. The frontend maps each to a translated message.

### 4.11 CLI

In `app/cli.py`:

- `support eval-generate [--seed 42] [--count 300]`
- `support eval --models jev,ollama:qwen3:4b --split dev [--out eval/results/<id>.json]` — same runner and tables (`triggered_by="cli"`), prints a comparison table, optionally writes the run as JSON in the import format (5.5).

## 5. Employee-frontend design

### 5.1 Data access

- `src/lib/api.ts` gains `evaluationsApi` (`models`, `estimate`, `start`, `cancel`, `list`, `get`, `predictions`).
- `src/lib/types.ts` gains `EvalModel`, `EvalRun`, `EvalModelSummary`, `EvalPrediction`.
- The page uses `useResource` and polls `GET /api/evaluations/{id}` every 3 seconds while the selected run is `queued` or `running`, as `RunsPage` does.

### 5.2 Page structure

`src/features/evaluation/` (moved out of `insights/`; the route stays `/evaluation`):

| Component | Responsibility |
| --- | --- |
| `EvaluationPage.tsx` | Header, run selector (latest by default), state switching |
| `RunEvaluationDialog.tsx` | Model checkboxes with availability badges (disabled with reason when not `ready`), split choice (test shows "held-out — do not tune prompts on these results"), per-model and total estimate, confirm |
| `EvaluationProgress.tsx` | Per-model progress bars, status, Cancel |
| `ProvenanceStrip.tsx` | Split, ticket count, dataset hash (short), prompt version, generator model, date, `triggered_by`; for imported reports, the existing "not independently verified" note |
| `HeadlineMetrics.tsx` | Four cards: best accuracy, lowest error rate, cheapest per request, fastest p50 — each naming the model |
| `ModelComparisonTable.tsx` | One row per model: accuracy ± CI, macro P/R/F1, extraction F1, escalation P/R, fraud recall, p50/p95, error rate, tokens in/out, tokens/s, $/request (classifier, total), $/1k tickets. Best value per column highlighted. Badges: **Production** (Jev), **Local · $0** (Ollama), **Failed** with reason |
| `ModelDetail.tsx` | Model picker, then tabs: Categories (per-category P/R/F1), Confusion matrix, Flags, Extraction, Slices |
| `ConfusionMatrix.tsx` | 12×12 heatmap; clicking a cell opens `PredictionsDrawer` |
| `PredictionsDrawer.tsx` | Tickets for that gold/predicted pair: text (`dir="auto"`), gold vs predicted, escalation, latency, cost, error |
| `EmptyState.tsx` | Translated intro, **Run evaluation** call to action, and the translated Topic 06 checklist |

- The static "Classification strategy: Jev" card is removed.
- **Import report** stays as a secondary action. An imported report is shown through the same `ProvenanceStrip` and `ModelComparisonTable` (5.5).
- Interval note under the table: "100 tickets: accuracy is ±~9 points at 95% confidence" (computed, translated).
- Existing components are reused: `Card`, `Badge`, `Dialog`, `Tabs`, `Button`, `Metric`, `PageHeader`, `FilterSelect`, and helpers in `src/lib/format.ts` (adding `formatUsd`, `formatMs` there if missing).

### 5.3 Text and direction

- All strings go under `evaluation.*` (and `runs.*`, `runDetail.*` for 5.4) in `src/locales/en.json` and `src/locales/ar.json`, including the validator errors in `src/lib/imports.ts` (which returns error keys instead of English text).
- Metric names are shown in Arabic with the English term as a tooltip (for example "الاستدعاء" → "Recall"). Category and flag names reuse existing taxonomy translations where present.
- Model IDs, the JSON example and the dataset hash render with `dir="ltr"`. The layout uses logical CSS properties so it works right-to-left.
- New test `src/locales/locales.test.ts`: identical key sets in `en.json` and `ar.json`, and no empty values.

### 5.4 Runs pages

`RunsPage.tsx` and `RunDetailPage.tsx`: every hardcoded string moves to `runs.*` / `runDetail.*` keys in both locales. No behaviour changes.

### 5.5 Import format

The import validator accepts the new format (what `support eval --out` writes): `{format: "zaincash-eval/v2", split, sample_size, generated_at, dataset_sha256, models: {<id>: <summary>}}`. The old v1 format (`model`, `classification_accuracy`, ...) remains accepted and is shown as a single-model row with only the fields it has.

## 6. Error handling

| Situation | Behaviour |
| --- | --- |
| One ticket fails (timeout, provider error, invalid output after retry) | Stored with its error; counts toward error rate and as wrong for quality |
| Model unavailable at start (no key, Ollama down, model not pulled) | `422 model_unavailable` naming the model and reason; nothing starts |
| Model fails repeatedly (>5 errors in first 10 tickets) | That model is `failed` with the reason; others continue |
| Test split file changed | `422 test_split_modified`; the run is refused |
| Dataset not generated | `422 dataset_missing`; the page explains how to run `support eval-generate` |
| Second evaluation while one is active | `409` |
| Cancel | Stops after the current tickets; completed models keep their summaries; status `cancelled` |
| API restarted during a run | On startup the run is marked `failed` with `interrupted` |
| Provider reports no cost | Token estimate used, labelled "estimated"; if no price is known, cost shows "—" |
| Precision/recall undefined | `null`, shown as "—" |

## 7. Testing

**Backend (pytest; no real model calls)**

- `tests/eval/test_metrics.py`: precision/recall/F1 on hand-built cases (including zero denominators), confusion matrix, Wilson interval, percentiles, cost aggregation, slices, errors counted as wrong.
- `tests/eval/test_llm_classifier.py`: valid structured output → `ClassifierOutput`; invalid then valid (one retry); invalid twice → `llm_unavailable`; low confidence → `uncertain`; picks mapping. Uses `tests/rag_fakes.py`/`tests/fakes.py` fake chat models.
- `tests/eval/test_usage.py`: meter no-op outside an eval; provider cost vs estimate vs local; Ollama timing parsing from recorded response metadata.
- `tests/models_config/test_ollama_provider.py`, `test_openrouter_provider.py` (if not already present from the admin work): `think` mapping, status from mocked `/api/tags`.
- `tests/eval/test_generate.py`: sampler determinism and category balance; verbatim-span check; gold escalation via `rules.decide`; stratified split; hash.
- `tests/eval/test_runner.py`: 6-ticket fixture with fake classifiers — predictions and summaries written, early stop, cancel, test-hash refusal.
- `tests/api/test_evaluations.py` (marked `integration`, Postgres): models, estimate, start, `409`, `422` codes, list, detail, predictions filters, cancel, startup marks interrupted runs.

**Employee frontend (Vitest)**

- `src/locales/locales.test.ts`: key parity.
- `src/features/evaluation/EvaluationPage.test.tsx`: empty state, running state with progress, completed results (comparison table, best-value highlight, Local badge, failed model) in both locales from mocked API data.
- `ConfusionMatrix.test.tsx`: cell click opens the drawer with the right filter.
- `RunEvaluationDialog.test.tsx`: unavailable models disabled with reason; test-split warning; estimate shown.
- `src/lib/imports.test.ts`: v1 and v2 accepted; translated error keys.
- `RunsPage` / `RunDetailPage` tests: render in Arabic without the previously hardcoded English strings.

**Manual check**

1. `support eval-generate`; hand-check 50 tickets and record results in the data card.
2. Start Ollama with `qwen3:4b`; set `OLLAMA_BASE_URL`.
3. From `/evaluation`, run all four models on `dev`; confirm metrics, latency, costs and the Local badge look plausible, and the confusion drill-down works in Arabic and English.
4. Run `test` once for the frozen configuration and commit the exported JSON.

## 8. Out of scope

- Drafting quality evaluation (LLM judge, human ratings).
- Calibration metrics (ECE, reliability diagrams).
- Using human reviews as live ground truth.
- GPU-time or power-based cost for local models.
- Admin model configuration (catalog, admin API/page, embeddings) beyond the provider subset in 4.1.
- Translating pages other than Evaluation, Runs and Run detail.
