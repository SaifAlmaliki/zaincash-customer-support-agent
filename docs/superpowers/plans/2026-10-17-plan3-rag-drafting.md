# Plan 3 RAG Drafting Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development or superpowers:executing-plans to implement this plan task-by-task after the user selects the execution method. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Complete document indexing, eight-tool investigation, grounded Iraqi-Arabic drafting and the existing workspace's RAG evidence flow.

**Architecture:** Application-owned SQLAlchemy/pgvector tables extend the existing uploaded-document store. Injectable embedding, retrieval, investigation and credential-checking interfaces support an isolated LangChain agent for each ticket. Existing API/CLI pipeline entry points receive the same real drafter and persist its evidence using `DraftResult`.

**Tech Stack:** Existing Python/uv, FastAPI, SQLAlchemy 2, psycopg, LangChain 1.x, LangGraph and ChatOpenRouter; add pgvector and pypdf. Existing React/TypeScript/Vite workspace and Vitest.

**Spec:** `docs/superpowers/specs/2026-10-17-plan3-rag-drafting-design.md` (approved).

## Global Constraints

- Workspace: `/home/cvzmh_saif/dev/zaincash-support` inside WSL Ubuntu-24.04. Windows tool calls use `wsl.exe -d Ubuntu-24.04 --cd <directory> <command>`.
- Graph orientation has already identified the integration points. Consult `graphify query` before new codebase exploration; refresh the graph after code changes.
- `RAG_ENABLED=true`, `EMBEDDING_MODEL=openai/text-embedding-3-small`, `EMBED_DIM=768`, `KB_TOP_K=5`, `KB_MIN_SIMILARITY=0.3`.
- Chunk size 1,200 Unicode characters, overlap up to 180; maximum 1,000,000 extracted characters, 300 PDF pages, 1,200 chunks and 10 MB source upload.
- Embedding batches at most 32 inputs, per-request timeout 20 seconds, indexing deadline 120 seconds.
- Eight tools; at most six executed calls including output tools; 30-second overall drafting deadline.
- Arabic alphabetic-character share at least 50%, reply at most 120 whitespace-delimited words, citations required.
- Preserve classifier/extraction/transaction outcomes and existing escalation reasons on drafting failures.
- Automated model calls are fakes. Live checks use explicitly synthetic content and the configured providers.
- Retain existing unrelated changes. Commit/push only when explicitly requested.

## Review Focus

1. A model cites a real chunk retrieved by another ticket: reject it and preserve each ticket's independent evidence map (Tasks 4–5).
2. A document is deleted or reindexed while an embedding call is running: reject stale publication and preserve old result evidence (Tasks 2, 6).
3. A model returns seven tool calls in one response, or submits then calls another tool: enforce the execution budget and terminal submission even within that batch (Tasks 3, 5).
4. Arabic “do not share your PIN” is safe, whereas a second sentence asking for the PIN is unsafe: scope negation locally (Task 4).
5. The embedding provider returns reordered, missing, duplicate, nonfinite or wrong-dimension vectors: map by response index or fail visibly; never index corrupt vectors (Task 1).

## File map and shared interfaces

| Files | Responsibility |
|---|---|
| `backend/app/kb/contracts.py`, `parse.py`, `embeddings.py` | Knowledge contracts, deterministic parsing/chunking, OpenRouter embeddings |
| `backend/app/kb/models.py`, `service.py`, `documents.py` | Vector/index tables, atomic indexing/retrieval, shared upload validation/storage |
| `backend/app/pipeline/stage6_draft/context.py`, `tools.py`, `investigation.py` | Per-ticket tool state, eight tools, bounded read-only database queries |
| `backend/app/pipeline/stage6_draft/guardrails.py`, `credentials.py` | Deterministic draft checks and Jev adapter |
| `backend/app/pipeline/stage6_draft/agent.py`, `prompts/draft_v1.md` | Bounded agent invocation, accounting, result/failure conversion |
| Existing factory/graph/config/CLI/API files | Wire real dependencies and expose indexing/evidence |
| Existing knowledge/review UI plus `KnowledgeSearch.tsx` and `CitationEvidence.tsx` | Index/retry/search/chunks, citations and guardrail findings |
| `data/kb/*.md`, `docs/demo-readiness.md`, verification record | Fictional policy corpus and demo status |

Define these dataclasses in `kb/contracts.py`:

```python
from dataclasses import dataclass

@dataclass(frozen=True)
class TextChunk:
    index: int
    text: str
    page_start: int | None = None
    page_end: int | None = None

@dataclass(frozen=True)
class EmbeddingBatch:
    vectors: tuple[tuple[float, ...], ...]
    cost_usd: float = 0.0

@dataclass(frozen=True)
class Passage:
    id: str
    document_id: int
    chunk_index: int
    text: str
    filename: str
    score: float
    page_start: int | None = None
    page_end: int | None = None

@dataclass(frozen=True)
class SearchResult:
    passages: tuple[Passage, ...]
    cost_usd: float = 0.0
```

Public method signatures:

- `parse_document(filename: str, content: bytes) -> list[TextChunk]`.
- `Embedder.embed(texts: list[str]) -> EmbeddingBatch` (async); embedder also exposes `model: str` and `dimensions: int`.
- `KnowledgeService(session_factory, settings, embedder)`.
- `KnowledgeService.index_document(document_id: int, *, category_tags: list[str] | None = None) -> dict` (async; returns the document projection).
- `KnowledgeService.search(query: str, *, category: str | None = None, k: int = 5) -> SearchResult` (async).
- `store_document(session, filename: str, content: bytes) -> UploadedDocument`; shared validation and checksum deduplication.
- `document_view(session, document: UploadedDocument) -> dict`; projects actual index state.
- `CredentialCheck(requests_credentials: float | None, degraded: bool, cost_usd: float)` and async `CredentialChecker.check(reply: str) -> CredentialCheck`.
- `check_draft(reply: str, citations: list[str], used_txn_ref: str | None, state: PipelineState, retrieved: dict[str, Passage]) -> list[str]`.
- `RagDrafter(settings, *, model_factory, knowledge, investigation, credential_checker)` implements `draft(state) -> DraftResult`.

## Task 1: Testable parsing and embedding boundary

**Files:** Create `kb/__init__.py`, `kb/contracts.py`, `kb/parse.py`, `kb/embeddings.py`, `tests/test_kb_parse.py`, `tests/test_embeddings.py`. Modify `config.py`, `pyproject.toml`, `uv.lock`, `.env.example`.

**Produces:** `TextChunk`, `EmbeddingBatch`, `Passage`, `SearchResult`, `parse_document`, `OpenRouterEmbedder` and configuration validation.

- [ ] Write parsing tests before implementation. The minimal acceptance case is:

```python
from app.kb.parse import parse_document

def test_arabic_text_and_bom_are_preserved():
    chunks = parse_document("policy.md", "\ufeff# سياسة تجريبية\nلا تشارك الرقم السري.".encode())
    assert chunks[0].index == 0
    assert "لا تشارك الرقم السري" in chunks[0].text
    assert "\ufeff" not in chunks[0].text
```

Add generated in-memory blank/encrypted PDF cases, empty/invalid UTF-8 text, oversized extraction, deterministic repeated chunking, overlap without infinite loops and preserved PDF page metadata. Assert failure messages tell the operator when OCR is needed.

- [ ] Run `uv run pytest tests/test_kb_parse.py -q`; confirm failure is missing implementation, then add pypdf/pgvector dependencies with uv in `backend/`.
- [ ] Implement parsing with paragraph-preferred bounded character slicing. Advance by at least one character each iteration; strip a BOM once at decode, retain internal Arabic text and page identity. Check limits before costly processing and while accumulating PDF pages.
- [ ] Write `httpx.MockTransport` embedding tests for each Review Focus response defect. A valid reordered response must restore input order:

```python
response = {"data": [
    {"index": 1, "embedding": [0.0] * 767 + [1.0]},
    {"index": 0, "embedding": [1.0] + [0.0] * 767},
]}
assert response["data"][0]["index"] != 0
```

Use this response in the transport and assert returned vector zero is `[1.0, 0.0, ...]` by testing its first element and sum. Test nonfinite entries, zero vectors, duplicate/missing indexes, empty input, 33-input batching, a 401 and a timeout. Client construction accepts an injected transport so no network is used.

- [ ] Implement the async adapter with `httpx.AsyncClient`, float encoding, model/dimensions in the body, finite/nonzero/dimension validation and bounded public exceptions. Collect reported usage/cost once per successful request; make the fallback embedding token price configurable and document its source.
- [ ] Run `uv run pytest tests/test_kb_parse.py tests/test_embeddings.py -q` and `uv run ruff check app/kb app/config.py tests/test_kb_parse.py tests/test_embeddings.py`.

## Task 2: Atomic pgvector indexing and retrieval

**Files:** Create `kb/models.py`, `kb/service.py`, `kb/documents.py`, `tests/test_kb_service.py`, `tests/kb_fakes.py`. Modify `db/session.py` to register the new models before create/reset operations. Move existing upload validation into the shared document service and retain its API behavior.

**Consumes:** Task 1 interfaces and existing `UploadedDocument`/session factory.
**Produces:** `KnowledgeService`, `store_document`, `document_view`, startup recovery and chunk inspection helpers.

- [ ] Add a `support_test` fixture with a database-name assertion, schema reset and engine disposal. Never reset the application database. Define the deterministic embedder in `tests/kb_fakes.py`:

```python
from app.kb.contracts import EmbeddingBatch

class FakeEmbedder:
    model = "test/embedding"
    dimensions = 768

    async def embed(self, texts):
        vectors = tuple(
            tuple([1.0, 0.0] + [0.0] * 766)
            if "تحويل" in text else tuple([0.0, 1.0] + [0.0] * 766)
            for text in texts
        )
        return EmbeddingBatch(vectors)
```

- [ ] Write tests that upload two distinct policies, index them, and search for `تحويل`. Assert rank, text, source name, stable IDs, cutoff and category/untagged filtering. Assert a duplicate upload/index leaves chunk count unchanged. Run the test file and observe missing-service failures.
- [ ] Create index/chunk models with cascade foreign keys, unique document/chunk identities, per-attempt ownership and a cosine HNSW index:

```python
Index("ix_kb_chunks_embedding", "embedding", postgresql_using="hnsw",
      postgresql_ops={"embedding": "vector_cosine_ops"})
```

Register models on both API and CLI schema initialization. Use a `Vector(768)` mapped column; construct stable chunk IDs from SHA-256(document digest + chunking version + chunk index + text).

- [ ] Implement claim/read → parse/embed → publish using short sessions. Lock the source row when claiming; refuse an active attempt; no transaction spans an embedding await. Publish only when source and attempt still exist and match. Replace chunks and mark indexed in one transaction. On failure preserve source and record a retryable error.
- [ ] Add deterministic interleaving tests with events: two index callers, deletion during embedding, stale attempt completion, provider failure and process-recovery state. Ensure model changes prevent searches against incompatible old vectors. Source deletion must cascade but never affect evidence already copied into a ticket result.
- [ ] Use `embedding.cosine_distance(query_vector)` and parameterized SQLAlchemy predicates for retrieval. Include only indexed/compatible chunks; category means requested category OR empty tags. Compute score as `1 - distance`, apply cutoff, limit 1–10, return `SearchResult` with query embedding cost.
- [ ] Run `uv run pytest tests/test_kb_service.py -q` with Postgres running, then the Task 1 tests and targeted ruff checks.

## Task 3: Ticket-scoped investigation and all eight tools

**Files:** Create `stage6_draft/context.py`, `investigation.py`, `tools.py`, `tests/test_draft_tools.py`.

**Consumes:** `PipelineState`, `Passage`, `KnowledgeService`, existing transaction/ticket/incident tables.
**Produces:** `DraftContext`, `SqlInvestigationRepo` and `build_tools(context, knowledge, investigation)`.

- [ ] Define `DraftContext` with pipeline state, isolated retrieved map, trace list, accumulated cost, tool count, reasons, submission and an async execution lock. Define a validated submission schema with `reply_ar`, citations, optional transaction reference and bounded internal note.
- [ ] Write tests for transaction exact/fuzzy search, recent records anchored to receipt time, prior ticket history excluding current/future contacts, open/closed incident windows and maximum 10 returned records. Seed explicit rows in `support_test` with unrelated customer records to verify context restrictions.
- [ ] Implement SQL queries in the read-only repository using fresh sessions and the existing record conversion conventions. All async tools call blocking database work through `asyncio.to_thread`; hard-limit dates, text/argument sizes and result counts.
- [ ] Build eight `@tool` definitions with documented schemas. All tools execute through one per-ticket guard. Its state transition is:

```python
async with context.lock:
    if context.submission is not None:
        raise DraftAlreadySubmitted()
    if context.tool_count >= context.max_tool_calls:
        raise DraftToolLimit()
    context.tool_count += 1
    result = await operation()
    context.trace.append(result_trace)
    return result
```

Define these exception types in `context.py`. Keep the lock around operation execution to serialize parallel calls for a single ticket. Always append a bounded failed-call trace in an exception path. `submit_draft` uses `return_direct=True`; it writes the one validated submission. `flag_for_human` only adds a reason/note.

- [ ] Test tools directly with `ainvoke`: seven concurrent invocations execute at most six operations; submit followed by another call cannot mutate state. A retrieved passage populates only its own context. Reject unrelated identifiers and unknown category/reason shapes, preserving a readable trace.
- [ ] Run `uv run pytest tests/test_draft_tools.py -q` and targeted ruff checks.

## Task 4: Deterministic checks and Jev credential review

**Files:** Create `stage6_draft/guardrails.py`, `credentials.py`, `tests/test_draft_guardrails.py`, `tests/test_credential_check.py`.

**Consumes:** Existing normalization/candidate/date/extraction helpers, pipeline state and retrieved passages.
**Produces:** `check_draft`, `CredentialCheck`, `JevCredentialChecker` and an explicit degraded checker for unavailable Jev.

- [ ] Write parameterized credential tests before implementation:

```python
@pytest.mark.parametrize(("reply", "unsafe"), [
    ("لا تشارك الرقم السري ويا أي شخص.", False),
    ("دزلي الرقم السري حتى أساعدك.", True),
    ("لا تشارك الرمز ويا غيرنا. أرسل لنا رمز OTP.", True),
    ("Never share your PIN.", False),
    ("Please send your password.", True),
])
def test_credential_requests_respect_local_negation(reply, unsafe):
    assert requests_credentials(reply) is unsafe
```

- [ ] Add fixtures for citation IDs from another run, no citations, invalid `used_txn_ref`, invented amounts/dates/phones/references, Arabic-Indic equivalents, matched transaction evidence, safe numbered nonfinancial steps, 121-word text and non-Arabic output. Assert each exact finding identifier.
- [ ] Implement focused finding functions and a single aggregation function. Normalize digits/Arabic variants with existing utilities; compare semantic financial/date/phone/reference values, not arbitrary character substrings. Evaluate credential negation at a local clause boundary so one safe sentence cannot suppress an unsafe request elsewhere.
- [ ] Wrap Jev's existing runnable shape in a checker that asks a single `requests_credentials` Noul. Parse finite output in [0,1], return token-based cost, and treat invalid/unavailable responses as degraded rather than a safe numerical zero:

```python
questions = {"requests_credentials": Noul(
    instructions="Does reply_ar ask the customer to disclose an OTP, PIN or password? Warnings not to disclose do not count.",
    criteria=NoulCriteria(true="Requests disclosure of a secret.",
                          false="No disclosure request; may warn against sharing secrets."),
)}
response = await runnable.ainvoke({"state": {"reply_ar": reply}, "questions": questions})
```

- [ ] Run `uv run pytest tests/test_draft_guardrails.py tests/test_credential_check.py -q` and targeted ruff checks. Ensure malformed Jev output and provider errors are covered with fakes.

## Task 5: Agent, failure conversion and pipeline wiring

**Files:** Create `stage6_draft/agent.py`, `stage6_draft/prompts/draft_v1.md`, `tests/test_rag_drafter.py`. Modify `drafting.py`, `factory.py`, `graph.py`, `tests/test_factory.py`, `tests/test_graph.py` and model/cost helpers in `llm.py` only where needed.

**Consumes:** Tasks 1–4; produces `RagDrafter` and database-backed factory wiring.

- [ ] Use a scripted LangChain chat-model fake that returns real `AIMessage.tool_calls`, supports `bind_tools`, and supplies deterministic usage. Script search → submit with an Arabic reply; prove the actual `create_agent` loop executes tools and returns `DraftResult`, not merely a mocked agent wrapper.
- [ ] Write failure cases for empty retrieval, valid/invalid citations, retained earlier fraud escalation, plain assistant text without submission, timeout during retrieval/model/checker, invalid tool arguments, seven tool calls in one response and submission followed by mutation. Concurrent two-ticket runs must not exchange citations, state or cost.
- [ ] Implement isolated agent creation with the existing ChatOpenRouter model and request retry conventions. Use explicit tools, a low-temperature versioned prompt and bounded recursion:

```python
agent = create_agent(model=model_factory(), tools=build_tools(context, knowledge, investigation),
                     system_prompt=system_prompt)
async with asyncio.timeout(settings.agent_timeout_s):
    await agent.ainvoke({"messages": [{"role": "user", "content": ticket_context}]},
                       config={"recursion_limit": 2 * settings.agent_max_tool_calls + 6})
    findings = check_draft(submission.reply_ar, submission.citations,
                           submission.used_txn_ref, state, context.retrieved)
    credential_result = await credential_checker.check(submission.reply_ar)
```

Convert timeout, no submission, no knowledge, provider and budget failures to the exact spec reasons. Preserve completed evidence/cost. Collect model responses during execution so a later exception does not discard earlier usage. Deduplicate response IDs when aggregating usage. Retain rejected draft text and append findings to trace.

- [ ] Add `knowledge`/`investigation` dependencies through explicit factory parameters or a documented public session factory accessor on `SqlTransactionRepo`; do not inspect its private `_sf` field from unrelated modules. Existing injected drafter wins. Database-backed configured runs use `RagDrafter`; explicit disabled/no-db runs use a skipped trace. Enabled but unconfigured drafting returns an unavailable escalation.
- [ ] Merge reviewer findings into decision notes and include degraded credential checks in run summaries. Keep existing classification semantics and use the existing dataclass serialization paths. Add drafting and embedding model IDs to run metadata.
- [ ] Run `uv run pytest tests/test_rag_drafter.py tests/test_factory.py tests/test_graph.py -q`, then the Task 3–4 suites and targeted ruff checks.

## Task 6: API/CLI indexing and persisted citation projection

**Files:** Modify `api/knowledge.py`, `api/schemas.py`, `api/workspace.py`, `services/workspace_queries.py`, `main.py`, `cli.py`, `services/batch_jobs.py` where dependency injection is needed. Create `tests/test_rag_api.py`, extend `tests/test_cli.py` and existing API tests.

**Consumes:** Shared document service, `KnowledgeService`, real drafter and stored evidence. Produces routes/CLI/status/evidence defined by the spec.

- [ ] Add app-level injectable knowledge service construction so API tests cannot accidentally call paid providers. Write API tests with fake embeddings and real PostgreSQL: upload, automatic index, duplicate, explicit retry, chunk inspection, category search, disabled provider and safe failures.
- [ ] Keep `GET/POST /api/knowledge` and download/delete compatibility. Implement `POST /{id}/index` with 202 acceptance, `GET /{id}/chunks` with bounded pagination and `POST /search` with validated query/category/k. Invalid file/query/category input returns 422; missing document 404; unavailable provider 503. Concurrent active index requests return its existing state instead of duplicate work.
- [ ] Use `BackgroundTasks` with independent sessions and the service's 120-second deadline. Initialize/recover jobs in the local single-worker lifespan. Auto-index only after source commit. Project real status and error text on polling.
- [ ] Persist retrieved passage snapshots in trace and resolve only cited IDs for detail responses:

```python
sources = {item["id"]: item
           for event in result.agent_trace
           for item in event.get("retrieved_passages", [])}
value["citation_sources"] = [sources[c] for c in result.citations if c in sources]
```

Use typed/validated projection helpers for old/malformed trace entries. Expose guardrail findings/internal note separately and preserve them after the source document is deleted.

- [ ] Add `support ingest-kb PATH` with file/directory support, `--retry-stored` for old uploads, deterministic extension filtering and per-document status output. Reuse source validation/store/index functions. Test a temporary Markdown directory, duplicate invocation and failure exit status using `CliRunner` and injected fakes.
- [ ] Replace hardcoded capability flags with configured/readiness indicators and indexed-document count. Update stage descriptions. Test keys never appear in responses, and missing/empty index is not reported ready.
- [ ] Run `uv run pytest tests/test_rag_api.py tests/test_workspace_api.py tests/test_cli.py -q`, followed by targeted ruff checks.

## Task 7: Knowledge and review workspace integration

**Files:** Modify `lib/types.ts`, `lib/api.ts`, `lib/stages.ts`, `features/knowledge/KnowledgePage.tsx`, `features/review/PipelineTrace.tsx`, `SourceEvidence.tsx` and capability copy where used. Create `features/knowledge/KnowledgeSearch.tsx`, `features/review/CitationEvidence.tsx`; add a focused projection/response test only for substantive logic.

**Consumes:** Task 6 response contracts. Produces the full upload/search/review interface using existing styling/components.

- [ ] Extend types for document status/count/error/model, passage/source metadata and guardrail findings. Add API methods for index, chunks and search with the existing request/error wrapper.
- [ ] Replace storage-only upload copy with actual returned indexing state. Poll only while an index is running; clean up timers on unmount and preview-mode changes. Add index/retry controls and show actionable failures.
- [ ] Implement chunk inspection and policy test search in a focused component. Use existing Cards, Inputs and Buttons; disable mutations in preview. Render passage text with `dir="auto"`, source metadata and similarity as similarity, not confidence.
- [ ] Add citation cards in review and distinguish real tool calls from guardrail/model/skipped trace entries:

```tsx
const tools = result.agent_trace.filter((event) => event.kind === "tool")
const findings = result.guardrail_findings ?? []
```

Keep original draft and final reviewed reply separate. Show retained evidence when a source document has been deleted, and an explicit missing-evidence state for legacy results.
- [ ] Verify pending/failed/indexed and zero-results states in the browser, including mobile width and preview/live isolation. Use network evidence to confirm preview controls do not submit mutations.
- [ ] Run `npm test`, `npm run lint` and `npm run build` from `customer-support-ui/`.

## Task 8: Demo corpus, full verification and readiness record

**Files:** Create 12 Markdown policy documents under `data/kb/`; create `docs/demo-readiness.md` and `docs/verification/2026-10-17-rag-drafting.md`. Update root/UI README, `pipeline/runner.md`, `.env.example` and this plan's checkboxes based on observed results.

**Execution record (2026-10-17):** Tasks 1–7 are implemented and independently reviewed (see the execution ledger). Task 8 corpus, live verification and readiness documentation have implementer evidence in [the verification record](../../verification/2026-10-17-rag-drafting.md): 665 backend tests, 21 frontend tests, both lints/build and real provider/browser checks. Task 8's checkboxes below remain unchecked until the controller reviews that evidence and the live-discovered credential-negation fix. Implementation/testing evidence alone does not imply independent review approval.

- [ ] Write one clearly labelled fictional document per taxonomy category, with Iraqi-Arabic guidance and a short English title. Include safe escalation and credential warnings, but no claimed real ZainCash fees, reimbursement guarantees or account access.
- [ ] Add demo inputs aligned with existing synthetic transactions: supported failed transfer, supported general inquiry, fraud escalation and an unsupported question. Keep these separate from the future held-out evaluation data.
- [ ] Run the existing and new backend suite against `support_test`:

```bash
uv run pytest -q
uv run ruff check app tests
```

- [ ] Run frontend checks once after the final UI changes:

```bash
npm test
npm run lint
npm run build
```

- [ ] Perform a live embedding/index/search check and at least one supported drafting run with synthetic inputs using the configured OpenRouter model. Check actual source relevance, tool count, citation existence, preserved escalation, draft language, provider usage and latency. Do not infer quality from connectivity alone.
- [ ] Run browser upload/index/search → ticket → citations/trace → edit/approve → reload. Exercise failed indexing and empty knowledge with test fixtures or controlled documents. Capture commands, counts and observed outcomes in the verification record.
- [ ] Refresh graphify after source changes, inspect the intended diff and `git diff --check`, and review changed code against the specification. Fix findings and rerun only affected checks.
- [ ] Update README status: Plan 1 and the workspace are implemented; Plan 3 status depends on verified outcomes. List Plan 2 evaluation, packaging/CI, disclosure/data card/failure evidence and the stretch weekly report as remaining. Separate automated passes from live provider verification and any unresolved blocker.

## Plan self-review

- Spec sections 3–5 map to Tasks 1–2; section 6 to Tasks 3/5; section 7 to Task 4/5; section 8 to Tasks 5–7; sections 9–10 to Task 8.
- Review Focus items have owning tests in Tasks 1, 2, 3, 4, 5 and 6.
- Shared names and return types above apply throughout; use those interfaces when tasks are executed independently.
- Indexing and drafting are one end-to-end deliverable. The evaluation dataset/evaluator, full deployment packaging and statistical weekly report remain separately scoped follow-up work.

## Execution handoff

The user authorized full implementation and live synthetic verification. Tasks 1–7 have independent review evidence. Task 8 and the final whole-plan review remain pending controller sign-off; remaining evaluation, packaging and disclosure work is tracked in [demo readiness](../../demo-readiness.md).
