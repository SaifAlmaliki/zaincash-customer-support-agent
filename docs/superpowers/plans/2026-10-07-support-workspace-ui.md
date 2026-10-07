# Support Workspace UI and Live API Implementation Plan

> **For agentic workers:** Use the executing-plans skill for native execution. Steps use checkbox syntax. Read the approved project spec and this plan before implementing.

**Goal:** Turn `customer-support-ui/` into the Topic 06 back-office workspace, connected to the existing Python pipeline through FastAPI.

**Architecture:** Feature-based React screens share typed API access and UI primitives. FastAPI routes delegate to services that reuse the existing pipeline factory, graph, outcome serializer, and PostgreSQL repository. Live data and explicitly selected illustrative preview data are separate.

**Tech stack:** Existing React 19, TypeScript, Vite 8, Tailwind 4, shadcn/Base UI and Lucide; Python 3.11+, FastAPI, Uvicorn, Pydantic, existing SQLAlchemy/PostgreSQL and LangGraph.

**Spec:** `docs/superpowers/specs/2026-10-07-support-pipeline-design.md`, especially sections 5, 6 and 8. Latest user decisions: use `customer-support-ui/`, include the live API, and organize code by feature/stage for debugging.

## Global constraints

- Work in `/home/cvzmh_saif/dev/zaincash-support` on Ubuntu-24.04; create a local feature branch for this work.
- Use the existing `customer-support-ui/` starter and its installed UI stack.
- Navigation is English; customer messages and reply editors use Arabic RTL or automatic direction for Arabizi.
- Customer messages, extraction, confidence, escalation reasons, and human review remain the primary workflow.
- API keys stay in the backend environment. The browser never receives them.
- Reuse the pipeline; do not implement another classifier in JavaScript.
- Persist live runs, results and reviews in PostgreSQL. Human approval never sends a message.
- The current drafter is `NullDrafter`. Display `No generated draft` honestly; a reviewer may author a response. No synthetic draft is substituted into a live result.
- Show evaluation metrics only from an explicitly loaded report, with its provenance. Blank metrics mean no evaluation has run.
- Document uploads in this slice are stored and marked `Awaiting indexing`; embedding ingestion and RAG drafting remain the separate backend work described by the approved spec.
- Illustrative preview tickets support UI review only, are visibly labelled, and are not the 200+ ticket evaluation dataset required by the brief.
- Preserve existing unrelated work and commit history. No automatic push or git configuration changes.

## Review focus

1. Missing API keys or a disconnected backend: show actionable errors, never a simulated successful run.
2. Empty or conflicting review submissions: prevent blank approval and reject stale updates; retain an audit record.
3. Failed tickets and interrupted processing: keep already completed results, show accurate run counts, and terminate failed jobs visibly.
4. Mixed Arabic/Latin identifiers and dates: preserve source text and verify highlighted spans without changing stored values.
5. Duplicate uploads or imported ticket identifiers: reject conflicting content rather than associate new text with an existing ticket's results.

## Visual design

- Palette: workspace `#f6f7f9`, surface `#ffffff`, graphite `#252830`, muted `#707783`, action red `#da3345`, escalation amber `#a46316`.
- Typography: reuse the locally installed Geist font for navigation and data; Tahoma/Arabic-capable sans-serif fallback for Arabic text, with generous line-height.
- Layout: a restrained sidebar and top bar; ticket queue as the default working screen; full-width workflow strip links the six backend stages; detail view separates source evidence from the response editor.
- Distinctive element: the numbered pipeline strip corresponds to real processing stages and their source modules. It is functional navigation, not decoration.
- Responsive: sidebar collapses, wide tables scroll inside their region, review columns stack on narrow screens. Keyboard focus, labelled controls and reduced-motion behavior are required.

## File map

```text
backend/app/
  main.py                    FastAPI app factory and lifecycle
  api/
    schemas.py               request/response validation
    dependencies.py          per-request database access
    runs.py                  start/list/detail batches
    results.py               queue/detail/review endpoints
    knowledge.py             document upload/list/delete/download
    workspace.py             health, taxonomy, stage map, aggregate data
  services/
    batch_jobs.py            execute existing pipeline and persist progress
    reviews.py               atomic review and audit updates
    workspace_queries.py     queue queries and response projections
  db/document_models.py      uploaded document metadata/content

customer-support-ui/src/
  App.tsx                    route selection and page composition
  components/layout/         sidebar, top bar, workspace status
  components/shared/         status badge, confidence, empty/error states
  features/queue/             queue filters, table and counts
  features/review/            ticket evidence, editor, stage/tool trace
  features/runs/              batch input, progress and run summary
  features/knowledge/         document management
  features/insights/          real category/weekly counts and evaluation state
  lib/api.ts                 typed HTTP client and errors
  lib/types.ts               shared frontend contracts
  lib/stages.ts              flow labels and backend source map
  hooks/                     shared query/polling state
  data/preview.ts            clearly labelled illustrative UI fixtures
  index.css                  existing theme tokens and workspace styles
```

## Task 1: API contracts and persisted review workflow

- [ ] Add FastAPI/Uvicorn and multipart-upload dependencies to `backend/pyproject.toml`; lock with uv.
- [ ] Write `backend/tests/test_workspace_api.py` covering result list/detail, missing result 404, empty approval 422, atomic saved review, and stale-review 409.
- [ ] Run `uv run pytest tests/test_workspace_api.py -q` before implementation and verify the missing endpoints fail.
- [ ] Implement the app factory, dependency injection, schemas, queue projection and review service.

HTTP contracts:

```text
GET  /api/health                 { database, configured_modes, capabilities }
GET  /api/workspace              { taxonomy, stages, counts }
GET  /api/results                { items, total }, filters: status/team/category/priority/q/run_id
GET  /api/results/{id}           result + ticket + matched transaction + review history
POST /api/results/{id}/reviews   { action, reviewer, final_text, team, expected_updated_at }
```

Approval requires nonempty final text; editing alone does not approve. Reassignment is recorded as a distinct review action. Row locking and `expected_updated_at` guard concurrent edits. The original generated draft stays available beside the final reviewed text.

- [ ] Verify tests with the dedicated `support_test` database, not the application database.

## Task 2: Live batch submission and progress

- [ ] Write tests for malformed batch input, missing provider configuration, partial failure, duplicate external IDs, and summary totals.
- [ ] Add JSON and CSV ticket submission using the same ticket model and normalization as the CLI. Enforce a maximum of 500 tickets per request and a 10 MB upload limit.
- [ ] Add `POST /api/runs` returning 202 plus the persisted run ID; `GET /api/runs` and `GET /api/runs/{id}` expose state and result counts.
- [ ] Run jobs with independent sessions, bounded concurrency and the existing compiled graph. Reuse `outcome_from_state`, `summarize` and `save_outcomes`; preserve ticket ordering and per-ticket failure isolation.
- [ ] Persist each completed result and update progress. A finished batch with ticket failures is visibly `completed_with_errors`; a crashed job is `failed`.
- [ ] Expose actual stage completion metadata and source file labels without inventing tool execution traces. Empty `agent_trace` means no tool calls recorded.
- [ ] Run API tests and the existing pipeline suite.

## Task 3: Workspace shell, queue and review

- [ ] Build the layout using existing shadcn primitives and the visual tokens above.
- [ ] Implement typed HTTP calls, loading/error/retry states and polling cleanup. Live request failures stay errors rather than switching silently to preview fixtures.
- [ ] Build queue filtering and prioritization with computed counts and keyboard-accessible ticket links.
- [ ] Build the review screen: original RTL ticket, structured fields and source spans, confidence/distribution, transaction evidence, escalation note, response editor, audit history and stage/source map.
- [ ] Implement approve, edit-and-approve, reject and reassign against the real review API. Copy is available for approved final text.
- [ ] Include an explicit `Preview workspace` mode for layout exploration; local preview changes never call mutation endpoints.

## Task 4: Batch screens and live processing

- [ ] Add run history and run detail views with status, totals, category breakdown, latency and estimated cost as reported by the backend.
- [ ] Add `New batch`: paste a ticket or upload JSON/JSONL/CSV, validate and preview input, choose an available classifier mode, submit once, poll the returned run, and open its results.
- [ ] Use the same workflow for the judge's single-ticket input; do not introduce a conversational chatbot.
- [ ] Show setup instructions when no provider is configured. The UI names the missing configuration but never asks users to paste API keys into the browser.

## Task 5: Knowledge documents and evidence screens

- [ ] Add bounded PDF/MD/TXT upload, server-side validation and checksum-based duplicate detection. Store uploaded documents in PostgreSQL and support download and deletion.
- [ ] Show `Awaiting indexing` on uploaded documents and distinguish stored files from retrievable RAG sources.
- [ ] Build insights from real ticket/result counts; count a ticket once using its latest result and compare complete week windows in Baghdad time. Do not infer a confirmed root cause from correlation.
- [ ] Build an evaluation screen with an honest no-report state and a report import/viewer for sample size, model, split, classification/extraction metrics and confusion cases. Label imported reports and preview examples explicitly.
- [ ] Test file size/type rejection, duplicate uploads and empty-report behavior.

## Task 6: Verification and handoff

- [ ] Run `npm run build`, `npm run lint` and the frontend logic tests.
- [ ] Run the backend test suite against the test database and `uv run ruff check app tests`.
- [ ] Verify in the browser: queue filters, Arabic text, input validation, review/save/copy, preview/live isolation, run progress/errors, knowledge uploads, and evaluation empty/import states.
- [ ] Inspect desktop and mobile layouts, keyboard focus, horizontal overflow and browser console errors.
- [ ] Document WSL startup, API proxy configuration, real capability limits, preview provenance, and the feature-to-file map in `customer-support-ui/README.md`.
- [ ] Record which live checks were executed and any provider-key blocker. Commit only intended UI/API files locally if requested by the ongoing workflow.

## Plan review

The approved UI pages are covered by Tasks 3–5. The additional API scope explicitly chosen by the user is covered by Tasks 1–2. RAG generation and held-out evaluation are represented honestly as unavailable backend capabilities, not fabricated successful features. Interfaces are consolidated at the API schemas and `lib/types.ts`, and shared UI logic stays out of individual page components.
