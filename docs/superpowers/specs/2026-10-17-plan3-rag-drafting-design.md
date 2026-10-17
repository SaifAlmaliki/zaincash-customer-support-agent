# Plan 3 — Knowledge retrieval and grounded reply drafting

- Date: 2026-10-17
- Status: written specification approved by the user on 2026-10-17
- Parent: `2026-10-07-support-pipeline-design.md`, sections 5, 6.5–6.6 and 14
- User choice: full Plan 3, including the eight-tool bounded agent

## 1. Intent and acceptance criteria

The user wants real knowledge-grounded drafts in the existing support workspace and an accurate account of the remaining demo work. The selected milestone is:

**Upload a synthetic policy → index it → process an Iraqi-Arabic ticket → inspect the draft, citations and investigation trace → save a human review.**

Success means:

1. PDF, Markdown and UTF-8 text uploads become searchable only after successful indexing.
2. The production database-backed pipeline uses a real drafter in every classification mode when drafting is enabled and configured.
3. Drafts are Iraqi Arabic, at most 120 whitespace-delimited words, and cite retrieved policy passages.
4. The eight investigation/output tools are implemented, with a maximum of six executed tool calls and a 30-second overall drafting deadline per ticket.
5. The reviewer can see supporting passages, actual tool activity, guardrail findings and provider/timeout failures.
6. Existing classifications, transaction evidence and escalation reasons survive a drafting failure.
7. Duplicate indexing, concurrent tickets, reindexing and document deletion do not corrupt retrieval or historical review evidence.
8. Automated tests use fake model clients; a separate live smoke run verifies provider connectivity and actual retrieval/drafting.

All policies and demo cases are explicitly fictional. Human approval remains the final workflow step; copying approved text is the existing delivery mechanism.

## 2. Current implementation and integration points

- `pipeline/stage6_draft/drafting.py` defines the `Drafter` protocol and `NullDrafter`.
- `pipeline/factory.py` currently defaults to `NullDrafter`.
- `DraftResult` already carries text, citation IDs, trace entries, escalation reasons and cost.
- `api/knowledge.py` persists `UploadedDocument` bytes and always reports `awaiting_indexing`.
- PostgreSQL already enables the vector extension, but no chunk/embedding tables exist.
- The API and React workspace already support batches, queue review, document upload/download/deletion and trace display.
- The original direct-Google embedding proposal is superseded by the user's choice to use the existing OpenRouter setup.

Use the existing SQLAlchemy database/session conventions and stage-based backend layout. Store vectors with the Python `pgvector` SQLAlchemy integration in application-owned tables rather than introduce a second document store through LangChain PGVector. LangChain remains the agent/tool framework.

## 3. Provider and configuration

Draft generation uses `ChatOpenRouter` and the existing configured `GEMINI_MODEL`. Embeddings use OpenRouter's `/api/v1/embeddings` endpoint through a small injectable async adapter.

New settings:

- `RAG_ENABLED=true`: database-backed runs attempt real drafting by default.
- `EMBEDDING_MODEL=openai/text-embedding-3-small`.
- `EMBED_DIM=768`: the initial database schema supports exactly 768 dimensions; reject other dimensions clearly rather than silently alter a vector column.
- `KB_TOP_K=5`, bounded to 1–10.
- `KB_MIN_SIMILARITY=0.3`: initial cosine-similarity cutoff, validated within [-1, 1]; it is a retrieval filter, not a calibrated confidence score. Evaluate this initial setting on development queries before reporting retrieval quality.
- Chunk size is 1,200 Unicode characters with up to 180 characters of overlap, preferring paragraph boundaries.

Reuse `OPENROUTER_API_KEY`, `AGENT_MAX_TOOL_CALLS=6`, `AGENT_TIMEOUT_S=30` and the existing system-CA setup. Embedding model/dimension metadata is persisted with indexes and exposed to operators. Retrieval must not compare vectors from different embedding models.

The embedding adapter validates finite vectors, dimension, response indexes, missing/duplicate items and provider errors. Batch at most 32 input texts per request, with a 20-second request timeout. An indexing job has a 120-second total deadline; agent retrieval is also subject to the stricter overall drafting deadline. Credentials and raw provider error bodies are never included in API responses or traces.

Record drafting and embedding usage/cost where the provider supplies it, with explicit documented token-price estimates when needed. Never count the same model response twice. Historical run metadata identifies the drafting and embedding models as well as classifier models.

## 4. Knowledge ingestion and persistence

### Tables

Preserve `uploaded_documents` as the source-file store. Add:

**`kb_document_indexes`** — one row per uploaded document, foreign key with cascade deletion:

- document ID, status (`awaiting_indexing`, `indexing`, `indexed`, `failed`)
- embedding model/dimensions and category tags
- chunk count, bounded public error message, indexed/updated timestamps
- indexing attempt identity for guarding concurrent completion

**`kb_chunks`**:

- stable string ID, document ID, chunk index, text
- filename/source metadata and optional PDF page range
- category tags and embedding model
- `vector(768)` embedding, cosine HNSW index
- unique document/chunk identity

An old upload without an index row is projected as `awaiting_indexing`. New tables fit the existing idempotent schema initialization pattern without requiring destructive resets.

### Parsing and chunking

- Decode text with UTF-8 BOM support. Extract text from PDFs with `pypdf`.
- Reject empty/unextractable documents with an actionable message; scanned PDFs requiring OCR are unsupported in this slice.
- Retain headings and Arabic text. Split deterministically with overlap; reject more than 1,000,000 extracted characters, 300 PDF pages or 1,200 chunks, in addition to the existing 10 MB upload limit.
- Stable chunk identifiers incorporate document content and chunking identity so a reindex preserves IDs for unchanged passages.
- Optional category tags are validated against the taxonomy. Untagged documents remain available to all categories.
- Document text is evidence, never an instruction source for the agent.

### Index lifecycle

Upload persists the source and starts a bounded background index job when embeddings are configured. Existing uploads can be indexed manually or through the CLI. Each job uses its own database sessions.

Claim work atomically; concurrent duplicate requests must not duplicate chunks or embeddings work. Parse/embed outside an open database transaction. Publish the new chunks and successful status in one transaction only if the attempt still owns the document. An interrupted or failed job remains visibly retryable. Startup recovery marks abandoned local-process jobs as failed. This local demo uses one API worker; supporting distributed index-job recovery is outside this slice.

Only successfully indexed documents with compatible embedding metadata are searchable. Reindexing cannot expose half-built chunks. Deleting a document removes its source, index and chunks; an in-flight completion cannot resurrect it.

## 5. Retrieval and evidence

Embed the search query with the same model as the indexed documents, then perform cosine top-k retrieval. Category filters include matching tagged documents and untagged general policies. Return IDs, passage text, filename/page metadata, and similarity score.

Apply the configured relevance cutoff; an empty index or no qualifying passage is a normal unsupported-answer condition. Similarity is not represented as model confidence. Tests verify ranking and category filtering against known vectors; live demo queries check Arabic retrieval relevance.

Each ticket has an isolated retrieved-passage map. Citation validation consults only this map, not arbitrary existing database chunk IDs. Persist snapshots of retrieved evidence in the ticket's trace. Detail responses resolve `citation_sources` from these snapshots so deleting or reindexing a document cannot erase what supported a historical draft.

## 6. Bounded investigation agent

`RagDrafter` implements the existing `Drafter` protocol. Dependencies include a chat-model factory, knowledge retriever, read-only investigation repository and credential checker. Create isolated per-ticket agent state; no conversation memory or retrieved evidence is shared across tickets.

The prompt contains normalized ticket data, classification, extracted fields, existing lookup/decision and a clearly separated instruction to treat ticket/document contents as untrusted evidence. Truncate unbounded context. Use the existing configured Gemini model via OpenRouter and `langchain.agents.create_agent`.

### Tools

| Tool | Behavior |
|---|---|
| `lookup_transaction(txn_ref)` | Exact lookup of a transaction relevant to the ticket context. |
| `search_transactions(phone, amount_iqd, date_from, date_to)` | Bounded search; at most 10 candidates. |
| `get_customer_recent_transactions(phone, days=14)` | At most 10 records, days in 1–90, anchored to ticket receipt time. |
| `get_customer_ticket_history(phone, days=30)` | At most 10 earlier contacts, days in 1–90; exclude the current ticket and future tickets. |
| `check_service_status(service, at_time)` | Incidents whose time window overlaps the requested time. |
| `search_knowledge_base(query, category, k=5)` | Relevant policy passages and stable citation IDs; records retrieved evidence. |
| `flag_for_human(reason, note)` | Adds an escalation reason and bounded reviewer note. |
| `submit_draft(reply_ar, citations, used_txn_ref, internal_note)` | Validates output shape, records one final draft and terminates agent execution. |

Customer/transaction identifiers supplied by the model are constrained to the ticket and verified investigation context. Search candidates or recent unrelated transactions do not become a confirmed match automatically. All queries are parameterized.

The six-call budget includes `submit_draft` and `flag_for_human`. Enforce it at execution time, including multiple tool calls in a single model response. Once submitted, later tool calls cannot modify the result. The 30-second deadline covers retrieval, chat calls, tools and draft checks; nested retries cannot extend it. Use a graph recursion limit as an additional termination bound.

An assistant text response without `submit_draft` is not accepted as a draft. The agent may flag for human review and then submit a conservative draft, but it cannot remove an existing escalation.

### Trace

Persist actual tool name, bounded arguments/result, status and timing, plus retrieved evidence, final internal note, guardrail results, model identity and usage. Keep this compatible with the existing `kind=stage` entries added by the API batch runner. A trace contains execution evidence, not private model reasoning.

## 7. Draft guardrails and failure outcomes

Run deterministic checks after submission:

1. Nonempty reply with at least 50% of its alphabetic characters in Arabic script, at most 120 whitespace-delimited words. Identifiers and occasional Latin product names are allowed; this script check does not claim to establish Iraqi dialect quality.
2. At least one citation, with every citation present in this ticket's retrieved-passage map.
3. Any stated transaction reference, currency amount, phone or concrete date must agree with the ticket or confirmed matched transaction after normalization. A submitted `used_txn_ref` must identify that match. Evidence about search candidates does not satisfy this check.
4. Arabic/English detection of requests to disclose OTPs, PINs or passwords. Explicit warnings not to share credentials must remain valid.
5. Jev `requests_credentials` Noul below 0.2 when the checker is available, regardless of classification mode. Missing/unavailable Jev falls back to deterministic checks with an explicit degraded-check trace entry.

Do not claim that these checks prove every natural-language statement is correct. Policy grounding is enforced through the evidence-only prompt, valid citations, unsupported-answer escalation and demo/human review.

If a draft fails checks, retain its text for inspection, append `draft_failed_guardrail`, and expose specific findings to the reviewer. If knowledge is missing or irrelevant, return `no_kb_support` without inventing a reply. Model/embedding failures return `llm_unavailable` or `kb_unavailable`; deadline and tool-budget exhaustion return `draft_timeout` and `draft_tool_limit`. An agent that ends without submission returns `draft_not_submitted`. Preserve completed classification/extraction/lookup, trace and measured cost.

Add drafting findings to the decision note as appropriate. Report degraded credential checking in result trace and run summary. Unexpected programming/database faults remain distinguishable from provider unavailability.

## 8. Pipeline, API, CLI and UI integration

### Pipeline and CLI

Wire the real drafter into database-backed API/CLI execution through `pipeline/factory.py`. Support explicit `RAG_ENABLED=false` for classification-only operation; retain `NullDrafter` for explicit opt-out and injected unit-test dependencies. If RAG is enabled but its provider key is missing, preserve available classification stages and return an unavailable-drafting escalation. The existing `--no-db` flow remains classification-only and records a skipped-drafting trace rather than attempting an implicit database connection.

Add `support ingest-kb <path>` for a file/directory, using the same validation/indexing service as the API. Provide a way to retry previously stored documents. Record model choices in run metadata.

### API

Keep existing routes and add:

- `POST /api/knowledge/{document_id}/index`: request/retry indexing, with validated optional category tags.
- `GET /api/knowledge/{document_id}/chunks`: bounded passage inspection.
- `POST /api/knowledge/search`: bounded query, optional category and top-k.

Existing document list/upload responses gain real status, chunk count, indexing error and embedding metadata. Result detail responses gain `citation_sources` and guardrail/degraded-check information derived from persisted evidence. Health capabilities reflect configuration and database/index state, not hardcoded booleans; expose indexed-document count separately from whether indexing is configured.

### UI

- Knowledge page: real lifecycle statuses, index/retry action, visible error, chunk inspection and test search.
- Review page: cited passage cards with source metadata, guardrail findings, internal note and actual tool trace.
- Update capability labels and stage documentation to distinguish configured, ready, failed and explicitly disabled states.
- Preserve the current English navigation, Arabic RTL evidence/editor and preview/live separation.

## 9. Demo policies and verification

Add approximately 12 short Markdown policies under `data/kb/`, covering the taxonomy and marked synthetic. Include guidance for failed/pending transfers, disputes, login, agent issues, cards, bills, KYC, refunds, fraud, app issues and general enquiries. Avoid invented promises about real ZainCash terms.

Verification includes:

- Parser/chunker validation, duplicates, bounded input and deterministic IDs.
- Embedding response validation and provider failure handling.
- PostgreSQL indexing lifecycle, concurrency, deletion, reindexing, vector ranking and category filtering.
- Each tool's read behavior, limits and ticket-context constraints.
- Agent submission, parallel call budget, timeout, missing knowledge and trace/cost retention.
- Guardrail positive and negative cases, including Arabic digits, credential-warning negation and cross-ticket citation isolation.
- Existing backend tests/lint and frontend build/lint/tests.
- Browser smoke: upload/index/search → submit ticket → inspect sources → approve/edit → reload persisted review, plus empty-KB and failed-index UI states.
- Separate live OpenRouter embedding/drafting smoke with explicitly synthetic inputs. If an external service is unavailable, record that blocker rather than claim a live pass.

## 10. Remaining demo roadmap

This implementation completes RAG and connects its existing UI surfaces. Track remaining work accurately:

| Area | Remaining work |
|---|---|
| Plan 2 | 200+ synthetic Iraqi-dialect tickets, dev/test split and protected hash, evaluator, three-mode metrics, confusion cases and human draft ratings. |
| Plan 4 | Core workspace already exists; complete the RAG-specific evidence/indexing integration in this plan. |
| Plan 5 packaging | Backend/frontend Dockerfiles, full Compose stack and CI. |
| Plan 5 documentation | Disclosure, evidence-backed failure modes, data card, refreshed README and demo runbook. |
| Weekly report | Statistical spike detection, incident correlation and cited bilingual narrative beyond the existing weekly counts; stretch priority. |

Write a demo-readiness checklist that distinguishes implemented code, automated verification and live evidence. Do not represent the five smoke fixtures or illustrative UI data as the held-out evaluation dataset.
