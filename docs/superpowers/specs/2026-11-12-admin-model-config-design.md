# Admin-managed, model-agnostic pipeline configuration — design specification

- **Date:** 2026-11-12
- **Status:** Written specification approved by the user on 2026-11-12. Revised the same day during planning: the embedding switch became a short guarded pause (section 4.8), with user approval, because the KB schema holds one index per document.
- **Repository state at design:** `e173dfb` on `main`
- **Scope:** Backend model/provider layer, admin API, employee-frontend admin page, local model (Ollama) support, setup documentation

## 1. Outcome and success criteria

ZainCash support must be able to run its AI steps on local models (Ollama) for privacy and offline use, and switch any model in the pipeline without code changes or restarts. Model choice is a **central, admin-owned configuration**. Customers (users-frontend) and regular employees cannot change it; when the admin changes the intake model, customers notice nothing.

Success means:

1. An admin can change the provider and model of every pipeline step — intake, classify (Jev), extract, draft, embed — from the employee workspace, without restarting the API.
2. OpenRouter and Ollama are both supported for chat steps and embeddings. Adding another provider later means adding one adapter, not touching pipeline code.
3. The admin only sees models that can perform each step, and a model cannot be saved unless a live test of that step passes on the server.
4. Changing the embedding model never lets a workspace batch draft against a half-built index: the switch re-indexes every document, and workspace batch starts are blocked until it finishes.
5. A run or intake session uses one consistent set of models from start to finish, and each run records which provider and model each step used.
6. When a configured provider is unavailable, the step fails visibly. The system never silently falls back to a different (for example, cloud) provider.
7. With no admin changes saved, behavior is identical to today (all values come from `.env`).
8. Backend tests, lint, and employee-frontend tests, lint, typecheck, and build pass. A manual smoke run with `qwen3:4b` (draft) and `nomic-embed-text` (embed) completes a small batch end to end.

## 2. Current state

Findings from the code at `e173dfb`:

- All chat model calls go through OpenRouter via `langchain_openrouter.ChatOpenRouter`, constructed in three places:
  - `backend/app/llm.py` (`GeminiStructuredLLM`, extraction, structured output),
  - `backend/app/pipeline/factory.py` → `stage6_draft/model.py` (`DraftChatOpenRouter`, RAG drafting agent with eight tools),
  - `backend/app/intake/model.py` (`OpenRouterIntakeModel`, multimodal structured output).
- Embeddings are a raw `httpx` POST to a hardcoded OpenRouter URL (`backend/app/kb/embeddings.py`). The vector column is fixed at 768 dimensions (`kb/models.py`). Each chunk and document index already stores `embedding_model`, and search filters by it.
- `kb_document_indexes` holds **one row per document** (primary key `document_id`), and publishing an index deletes all of that document's chunks first (`kb/service.py` `_publish`). Chunk IDs and the `(document_id, chunk_index)` unique constraint do not include the model. Two embedding models' indexes of the same document therefore cannot coexist.
- `KnowledgeService._metadata` requires `embedder.model == settings.embedding_model`, and `api/workspace.py` health counts indexed documents by `settings.embedding_model`.
- Jev classification uses `langchain_typesafe.TypeSafeClassifier`. TypeSafe exposes no model-listing endpoint.
- Model IDs come only from `Settings` (`backend/app/config.py`) and are fixed at API start. `RunRow.model_ids` records models per run.
- OpenRouter-specific behavior is spread across the code: `model_kwargs={"retries": None}`, the private `_create_usage_metadata` import, `OpenRouterError` handling in `stage6_draft/agent.py`, cost from `response_metadata["cost"]`, prices chosen by whether `anthropic_model` is set, and feature availability derived from `bool(settings.openrouter_api_key)` (`factory.py`, `services/knowledge_runtime.py`).
- `agent_timeout_s` is capped at 30 seconds.
- The employee workspace has no authentication or roles. CORS allows only `GET`, `POST`, `DELETE`.
- Tables are created through SQLAlchemy `Base.metadata.create_all` (`backend/app/db/session.py`); there is no migration tool.

## 3. Decisions

| Topic | Decision |
| --- | --- |
| Primary goal | Local/offline/private operation, via Ollama |
| Who changes models | Admin only; one global configuration for the whole system |
| Access control | `ADMIN_TOKEN` in `.env`, sent as `X-Admin-Token`; real login is a later project |
| Switchable steps | intake, classify (Jev), extract, draft, embed |
| Model choices | Live discovery from each provider, filtered by step requirements |
| Architecture | In-app provider adapters + database-stored settings (approach A). LiteLLM proxy and "everything OpenAI-compatible" were rejected. |
| Secrets and endpoints | Stay in `.env`; never sent to the browser |
| When changes apply | New runs and new intake sessions only |
| Fallback on provider failure | None; fail visibly |

## 4. Backend design

### 4.1 Module layout

New package `backend/app/models_config/`:

| File | Responsibility |
| --- | --- |
| `steps.py` | The `Step` enum (`intake`, `classify`, `extract`, `draft`, `embed`), each step's required capabilities, and the `.env` default for each step |
| `types.py` | `ModelChoice` (provider, model, options), `CatalogEntry` (id, name, capabilities, prices, context length), `TestResult` |
| `providers/base.py` | `Provider` protocol (see 4.2) |
| `providers/openrouter.py` | OpenRouter chat, embeddings, catalog. Takes over `DraftChatOpenRouter`, `model_kwargs={"retries": None}`, `OpenRouterError` mapping, and cost from `response_metadata["cost"]` |
| `providers/ollama.py` | `ChatOllama` and `OllamaEmbeddings` from `langchain-ollama`; catalog from `/api/tags` + `/api/show` |
| `providers/typesafe.py` | Jev classifier construction; no catalog |
| `providers/registry.py` | Maps provider name to adapter; reports each provider's status (`ready`, `missing_key`, `unreachable`) |
| `store.py` | Read/write `model_settings`, write audit rows, merge with `.env` defaults |
| `resolver.py` | `ActiveModels`: a snapshot of the configuration, with `chat(step)`, `embedder()`, `classifier()`, `model_ids()`, and `prices(step)` |
| `probe.py` | Per-step live tests (see 4.5) |
| `catalog.py` | Per-provider catalog cache (5 minutes, manual refresh) and filtering by step requirements |

The pipeline and intake depend only on `ActiveModels`. No code outside `providers/` imports `langchain_openrouter`, `openrouter`, or `langchain_ollama`, and only `providers/` constructs provider clients. The classify stage (`jev.py`, `credentials.py`) and the classify probe keep importing `langchain_typesafe` question types (`Noul`, `Choice`, `Score`), because the classify step is TypeSafe-only.

Implementation notes fixed during planning:
- Ollama embeddings use Ollama's OpenAI-compatible `/v1/embeddings` endpoint through the existing validated embedder (generalized as `OpenAICompatibleEmbedder`), not `OllamaEmbeddings`. Behavior is the same and the existing vector validation is reused.
- Cost keeps coming from `response_metadata["cost"]` when a provider reports it (OpenRouter) and otherwise from `ActiveModels.token_prices(step)` (zero for local providers), so the protocol needs no `response_cost` method.
- Every model picker also accepts a typed model ID, gated by the same live test. This covers Jev (no catalog) and OpenRouter embeddings if its listing is unavailable.

### 4.2 Provider protocol

```python
class Provider(Protocol):
    name: str                      # "openrouter" | "ollama" | "typesafe"
    locality: Literal["local", "cloud"]

    def status(self) -> ProviderStatus: ...
    async def catalog(self) -> list[CatalogEntry]: ...
    def chat_model(self, model: str, *, temperature: float, timeout_s: float,
                   options: Mapping[str, object]) -> BaseChatModel: ...
    def embedder(self, model: str, *, dimensions: int) -> Embedder: ...
    def classifier(self, model: str) -> Classifier: ...
    def provider_errors(self) -> tuple[type[BaseException], ...]: ...
    def response_cost(self, message: AIMessage) -> float | None: ...
```

Adapters raise `UnsupportedOperation` for operations they do not offer (for example, `typesafe.chat_model`). `Embedder` is the existing embedder interface used by `kb/`; `Classifier` is the Jev runnable interface used by the classify stage.

The draft agent's provider-error tuple (`stage6_draft/agent.py`) and its cost callback stop importing OpenRouter types directly. They get them from `ActiveModels` (`provider_errors()`, `response_cost()`, `prices(step)`).

### 4.3 Storage

New SQLAlchemy models registered before `create_all`:

`model_settings`

| Column | Type | Notes |
| --- | --- | --- |
| `step` | string, primary key | One of the `Step` values |
| `provider` | string | `openrouter`, `ollama`, `typesafe` |
| `model` | string | Provider model ID, e.g. `qwen3:4b` |
| `options` | JSONB | `temperature`, `think` (bool), others reserved |
| `updated_at` | timestamptz | |
| `updated_by` | string | Free-text admin name entered in the UI |

`model_settings_audit`

| Column | Type |
| --- | --- |
| `id` | bigint primary key |
| `step` | string |
| `previous` | JSONB (provider, model, options) or null |
| `current` | JSONB |
| `changed_by` | string |
| `changed_at` | timestamptz |
| `test_latency_ms` | integer |

`embedding_switch` (one active job at most)

| Column | Type | Notes |
| --- | --- | --- |
| `id` | bigint primary key | |
| `target` | JSONB | The new embedding `ModelChoice` |
| `previous` | JSONB | The embedding `ModelChoice` before the switch |
| `status` | string | `running`, `completed`, `completed_with_errors`, `failed` |
| `total`, `done` | integer | Documents |
| `failed_document_ids` | JSONB list of integers | |
| `error` | text, nullable | |
| `started_by`, `started_at`, `finished_at` | | |

If a step has no row, `store.py` returns the `.env` default (today's `gemini_model`, `draft_model`, `intake_model`, `jev_model`, `embedding_model` rules, with provider `openrouter` or `typesafe`).

### 4.4 Snapshot semantics

- `services/batch_jobs.py` reads `ActiveModels` once when a batch starts and passes it to `build_pipeline`. The whole batch uses that snapshot.
- `services/intake_runtime.py` reads the intake `ModelChoice` when an intake session is created and stores it in a new nullable JSONB column `intake_sessions.model_choice`, so every turn of one customer conversation uses the same model. Sessions with a null value (created before this change) use the current setting. The column is added in `app/db/workspace_schema.py` (`ALTER TABLE ... ADD COLUMN IF NOT EXISTS`), because `create_all` does not alter existing tables.
- `RunRow.model_ids` becomes `{"intake"?: ..., "classify": "typesafe:jev-1.13.0", "extract": "openrouter:google/gemini-3.8-flash", "draft": "ollama:qwen3:4b", "embed": "ollama:nomic-embed-text"}`. Old runs keep their existing shape; readers accept both.
- Feature availability (`drafting.configured`, `knowledge.configured`, the `UnavailableDrafter` choice) is derived from the configured provider's status for that step, not from `openrouter_api_key`.

### 4.5 Step requirements and live tests

| Step | Required capabilities (hard block) | Live test |
| --- | --- | --- |
| intake | structured output, vision | Structured output on a tiny schema, with a 1×1 PNG image in the message |
| classify | (TypeSafe only) | Classify one fixed sample ticket |
| extract | structured output | Structured output on a tiny schema |
| draft | tool calling | Bind one dummy tool; the model must call it with valid arguments |
| embed | embeddings, 768 dimensions | Embed one string; the vector length must be 768 |

Capability sources:

- **OpenRouter:** `GET /api/v1/models` → `supported_parameters` (`tools`, `structured_outputs`/`response_format`), `architecture.input_modalities` (`image`), `pricing`. For embed, the adapter uses OpenRouter's embeddings model listing if the API offers one (verified during implementation). If it does not, the OpenRouter embed tab shows a text field for the model ID, and the 768-dimension live test is the only gate.
- **Ollama:** `GET /api/tags` for installed models, then `POST /api/show` per model → `capabilities` (`completion`, `tools`, `vision`, `thinking`, `embedding`). Prices are zero. Models whose `capabilities` are missing are shown as "unknown" and must pass the live test like any other model.

Tests have a 60-second ceiling and use the same construction path as production (`Provider.chat_model` and friends), so a passing test means the real step will build the same way.

### 4.6 Options

- `temperature`: per step, defaulting to today's values (draft 0.1, extract 0.0).
- `think`: only shown for models with the `thinking` capability. Default **off** for all pipeline steps. Ollama maps it to `reasoning=False`; OpenRouter maps it to its reasoning parameter.

### 4.7 Timeouts

`agent_timeout_s` keeps its 30-second cap for cloud providers. A new setting `local_agent_timeout_s` (default 180, maximum 600) applies when the draft provider is local. `intake_timeout_s` gets a matching `local_intake_timeout_s`. The admin page shows a warning that local models are slower.

### 4.8 Embedding switch (short pause)

The KB schema allows one index per document (section 2), so the switch is a short, guarded pause rather than a shadow index. The KB tables are not changed.

1. The admin picks a new embedding model; it must pass the embed test.
2. `POST /api/admin/models/embed/switch` is refused with `409` if any run has status `running` or another switch is `running`.
3. Otherwise, in one transaction: create an `embedding_switch` row (`running`, `total` = number of knowledge documents), update `model_settings` for `embed`, and write an audit row. From this point the KB embedder (4.9) uses the new model.
4. A background task re-indexes every document sequentially through the existing `KnowledgeService.index_document`, incrementing `done` after each one and recording failed document IDs.
5. When every document has been attempted, the job becomes `completed`, or `completed_with_errors` with `failed_document_ids`. Failed documents can be re-indexed from the existing Knowledge page.
6. While a switch is `running`, `POST /api/runs` returns `409 {"detail": "knowledge_switch_in_progress"}`. Intake-dispatched runs are **not** blocked, so customers notice nothing; their drafts get no KB results during the window and route to human review with the existing `no_kb_support` reason.
7. There is no cancel. Switching back is another switch.
8. On API startup, a switch left `running` is marked `failed` with "API restarted during switch; run the switch again" (the setting already points to the new model, so re-running re-indexes the remaining documents).

### 4.9 Runtime embedder

`KnowledgeService` is long-lived (`app.state.knowledge`), so it receives a `ConfiguredEmbedder` that implements the existing `Embedder` interface and, on every call, resolves the current `embed` choice through the store and delegates to that provider's embedder. Its `model` property returns the current model ID.

- `KnowledgeService._metadata` checks `embedder.dimensions == 768` and returns `(embedder.model, embedder.dimensions)`; it no longer compares against `settings.embedding_model`.
- `api/workspace.py` health and the draft trace's `embedding_model` use the current embed choice instead of `settings.embedding_model`.
- The existing "embedding model changed during indexing/search" checks remain and protect against a switch landing mid-operation.

## 5. Admin API

All routes live under `/api/admin`, in a new router `backend/app/api/admin.py`.

**Access:** dependency `require_admin` compares `X-Admin-Token` with `ADMIN_TOKEN` using `hmac.compare_digest`. If `ADMIN_TOKEN` is empty, every admin route returns `403 {"detail": "admin_disabled"}`. A wrong or missing token returns `401`. CORS adds `PUT` and allows the `X-Admin-Token` header.

| Method and path | Purpose |
| --- | --- |
| `POST /api/admin/session` | Validates the token; returns `204` or `401` |
| `GET /api/admin/models` | For each step: current choice, `source` (`env` or `admin`), `updated_at`, `updated_by`, requirements, provider locality and status |
| `GET /api/admin/models/catalog?step=<step>&refresh=<bool>` | For each provider: status and the entries that meet the step's requirements, plus "unknown" entries |
| `POST /api/admin/models/test` | Body `{step, provider, model, options}` → `{ok, latency_ms, error?}` |
| `PUT /api/admin/models/{step}` | Body `{provider, model, options, changed_by}`. Runs the live test on the server; saves and audits only on success. Returns `422` with the test error otherwise. Not allowed for `embed` (use the switch). |
| `POST /api/admin/models/embed/switch` | Body `{provider, model, options, changed_by}`. Runs the live test, then starts the switch (4.8) and returns the `embedding_switch` row. `409` if a run or another switch is running; `422` if the test fails. |
| `GET /api/admin/models/embed/switch` | Current or most recent switch job, or `null` |
| `GET /api/admin/models/audit?limit=50` | Recent audit rows |

`GET /api/health` (public) gains `ai: {locality: "local" | "cloud" | "mixed", steps: {<step>: {provider, model, locality, status}}}`. Model IDs are not secret; keys and URLs are never included.

## 6. Employee-frontend design

### 6.1 Route and access

- New route `/admin/models`, lazy-loaded in `src/App.tsx`, with an **Admin → Models** item in the sidebar.
- `src/lib/admin-token.ts` stores the token in `sessionStorage` (key `zaincash-admin-token`) through a `useSyncExternalStore` store, matching the pattern in `src/lib/locale.tsx`.
- `src/lib/api.ts` gains `adminRequest`, which adds `X-Admin-Token`, and an `adminApi` object for the endpoints in section 5. A `401` clears the token and returns the page to its locked state.
- Locked state: a token field plus an "admin name" field (used as `changed_by`, saved in the same session store).

### 6.2 Page

`src/features/admin/ModelsPage.tsx` shows one card per step in pipeline order (Intake → Classify → Extract → Draft → Embed). Each card shows the current model, a **Local** or **Cloud** badge, provider status, the source ("Default from .env" or "Set by {name} on {date}"), and a **Change** button.

Below the cards, `AuditList.tsx` shows recent changes.

### 6.3 Change dialog

`src/features/admin/ChangeModelDialog.tsx`:

1. Provider tabs (OpenRouter, Ollama; TypeSafe only for classify). An offline or unconfigured provider shows its status instead of a list.
2. A searchable list of eligible models, with capability chips (tools, vision, thinking, embedding), price per million tokens, and "unknown capabilities" marking where applicable. Classify shows a text field for the Jev version instead.
3. Options: temperature, and thinking on/off when supported.
4. **Test** shows pass/fail, latency, and the error. **Save** is enabled only after a passing test of the exact current selection; any change to provider, model, or options requires a new test.
5. For embed, the action is **Re-index and switch**, behind a confirmation that explains: knowledge search pauses for the duration, new workspace batches are blocked until it finishes, and it cannot start while a batch is running. The card then shows progress (`done/total`), polling the switch endpoint every 2 seconds, and the final status with any failed documents.

`NewBatchPage` shows the `knowledge_switch_in_progress` error from `POST /api/runs` as a readable message.

### 6.4 Visible to all employees

- `src/components/layout/AiLocalityChip.tsx` in the top bar next to `LanguageToggle`, reading `health.ai.locality`: **AI: Local**, **AI: Cloud**, or **AI: Mixed**, with a tooltip listing each step's model.
- `RunDetailPage` shows the run's `model_ids`. The `Run` type gains `model_ids`.

### 6.5 Text and direction

All new strings go in `src/locales/en.json` and `src/locales/ar.json`. Layout works right-to-left. Existing components are reused: `Card`, `Badge`, `Dialog`, `Tabs`, `Input`, `FilterSelect`, `Button`, `useResource`.

## 7. Error handling

| Situation | Behavior |
| --- | --- |
| Provider unreachable during a run (draft) | Drafting fails as today: the ticket goes to human review with reason `model_unavailable: <provider>:<model>` |
| Provider unreachable during a run (extract) | Extraction is skipped as with today's provider errors; missing fields stay missing |
| Provider unreachable during intake | The intake turn returns the existing "temporarily unavailable" response; the customer can retry |
| Provider unreachable for embed | KB search returns no results and records the error; drafting continues without KB evidence |
| Saved model removed from Ollama later | Same as unreachable; the admin page shows the model as "missing" |
| Catalog fetch fails | That provider's tab shows the error; other providers still work |
| Live test fails on save | `422` with the provider error; nothing is saved |
| Two admins save the same step | Last write wins; both are audited |
| Workspace batch started during an embedding switch | `409 knowledge_switch_in_progress`; the page explains why |
| Embedding switch requested while a run is running | `409`; nothing changes |
| Some documents fail to re-index during a switch | Job ends `completed_with_errors` listing them; the rest use the new model |

No step ever switches to another provider automatically.

## 8. Local model setup

- New `.env` settings: `ADMIN_TOKEN`, `OLLAMA_BASE_URL` (default `http://localhost:11434`), `LOCAL_AGENT_TIMEOUT_S`, `LOCAL_INTAKE_TIMEOUT_S`. All documented in `.env.example`.
- `docker-compose.yml`: the `api` service gets `extra_hosts: ["host.docker.internal:host-gateway"]`; `.env.example` documents `OLLAMA_BASE_URL=http://host.docker.internal:11434` for Docker.
- Running the API directly in WSL while Ollama runs on Windows: with WSL mirrored networking, `localhost` works; with the default NAT mode, Ollama on Windows must listen on all interfaces (`OLLAMA_HOST=0.0.0.0`) and `OLLAMA_BASE_URL` must use the Windows host IP.
- README gains a "Using local models" section: install and start Ollama, `ollama pull qwen3:4b` (draft, extract), `ollama pull nomic-embed-text` (embed, 768 dimensions), a vision model such as `gemma3:4b` or `qwen2.5vl` for intake, how to set `OLLAMA_BASE_URL`, and how to verify it from the admin page.
- `langchain-ollama` is added to `backend/pyproject.toml`.

Note: Jev (TypeSafe) always runs in the cloud, so "fully offline" is not possible while classification uses Jev. The locality chip will show **Mixed** in that case.

## 9. Testing

**Backend (pytest)**

- `tests/models_config/test_openrouter_provider.py`, `test_ollama_provider.py`: catalog parsing and capability mapping from recorded JSON responses (HTTP mocked as in `tests/test_llm.py`); chat model and embedder construction; option mapping (`think`, temperature, timeouts).
- `test_store.py`: `.env` defaults when no row exists; saves; audit rows.
- `test_resolver.py`: snapshot behavior; `model_ids` format; provider errors and cost come from the right adapter.
- `test_probe.py`: each step's test passes and fails correctly with fake chat models (`tests/rag_fakes.py` `ScriptedChat`, `tests/fakes.py`).
- `tests/api/test_admin.py`: `403` when disabled, `401` on a bad token, test-before-save, `422` on failed test, `PUT embed` rejected, audit listing.
- `test_embedding_switch.py` (marked `integration`, Postgres): refused while a run is running; setting flips and every document is re-indexed with the new model; a failing document yields `completed_with_errors` with its ID; `POST /api/runs` returns `409` while running; startup marks a leftover `running` switch `failed`.
- Existing tests in `test_factory.py`, `test_llm.py`, `test_draft_model.py`, `test_rag_drafter.py`, `tests/intake/test_model.py` are updated to the new construction path and keep their assertions on OpenRouter request shape.
- `tests/test_health.py` (or the existing health test): `ai.locality` values.

**Employee frontend (Vitest)**

- `src/lib/api.test.ts`: `adminRequest` sends `X-Admin-Token`; a `401` clears the token.
- `src/features/admin/ModelsPage.test.tsx`: locked state without a token; cards render from a fixture.
- `ChangeModelDialog.test.tsx`: Save disabled until a passing test; changing the selection after a test disables Save again.
- `AiLocalityChip.test.tsx`: Local, Cloud, and Mixed rendering.

**Manual smoke test**

1. Set `ADMIN_TOKEN` and `OLLAMA_BASE_URL`; start Ollama with `qwen3:4b` and `nomic-embed-text`.
2. In `/admin/models`, switch draft to `ollama:qwen3:4b` (thinking off) and run "Re-index and switch" for embed with `ollama:nomic-embed-text`.
3. Run a small batch from `/runs/new`; confirm the run detail shows the Ollama models and drafts are produced or routed to human review with a clear reason.

## 10. Out of scope

- Employee login and roles (the admin token is a stopgap).
- Per-employee or per-run model choice.
- Token streaming.
- Providers other than OpenRouter, Ollama, and TypeSafe (the adapter protocol allows them later).
- Editing Jev thresholds (`T_JEV`, `JEV_MIN_TOP_PROB`) in the UI.
- Fully offline classification.
- Zero-downtime embedding switches (would require one KB index per document per model).
- Cancelling an embedding switch.
