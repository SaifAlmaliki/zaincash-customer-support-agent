# ZainCash Support Workspace

A React + TypeScript + shadcn/ui back-office workspace for **Topic 06: Support Pipeline Automation**. Process batches of Iraqi-dialect tickets, inspect classification and extracted evidence, and record human review decisions.

## Open the right project

The implementation is in WSL Ubuntu-24.04:

```text
/home/cvzmh_saif/dev/zaincash-support/customer-support-ui
```

From Windows Explorer or an IDE:

```text
\\wsl.localhost\Ubuntu-24.04\home\cvzmh_saif\dev\zaincash-support
```

## Run locally

Run these commands **inside WSL**. Node 22.12+ is required by Vite 8.

Terminal 1, from the repository root:

```bash
docker compose up -d --wait db
uv --directory backend sync
export SSL_CERT_FILE=/etc/ssl/certs/ca-certificates.crt
uv --directory backend run uvicorn app.main:app --host 0.0.0.0 --port 8000
```

Terminal 2:

```bash
cd customer-support-ui
npm ci
npm run dev -- --port 5173
```

Open **http://localhost:5173**. Vite proxies `/api` requests to `127.0.0.1:8000`. Interactive API documentation is at **http://localhost:8000/api/docs**. PostgreSQL is exposed on host port **5433**, avoiding the other local project's database on 5432.

The API uses the repository-root `.env`. The current backend configuration requires `TYPESAFE_API_KEY` for Jev and `OPENROUTER_API_KEY` for Gemini through OpenRouter; cascade mode needs both. These keys remain server-side. Restart the API after changing configuration. Use one API worker for the local background-job runner.

Optional: seed the existing synthetic transaction fixtures before investigating tickets:

```bash
uv --directory backend run support seed-db \
  --transactions tests/fixtures/sample_transactions.jsonl \
  --incidents tests/fixtures/sample_incidents.jsonl
```

## Workspace modes

- **Live workspace** uses FastAPI and PostgreSQL. Runs, result progress, documents, and review decisions are persisted. Failed requests remain errors; the UI does not replace them with simulated success.
- **Preview workspace** uses the clearly labelled illustrative fixtures in `src/data/preview.ts`. Review edits are session-local and never issue live mutations. Preview data is not measured output and is not the held-out dataset required by the hackathon.

## Workflow

1. **New batch:** upload CSV/JSON/JSONL or paste a single ticket. Preview the input, choose an available model strategy, and start processing.
2. **Pipeline runs:** follow completed-ticket counts and inspect errors, escalation reasons and recorded cost/latency.
3. **Support queue:** filter/search the latest result for every ticket. API pages are all loaded before client-side filtering/export, including queues larger than 500 tickets.
4. **Knowledge base:** upload a fictional PDF/MD/TXT policy, follow indexing status, inspect passages and test Arabic retrieval. Acceptance is not completion; retry failures or re-request unclaimed work explicitly.
5. **Ticket review:** inspect the original message, source spans, transaction evidence, retained cited passages, draft checks and actual tool trace. Edit a reply, reassign, approve or reject. Changes are audited; stale edits receive a conflict response. Checks and citations describe the original generated draft, not later edits.
6. **Copy approved reply:** copy the saved, approved response. Approval never sends a message.

The **One pipeline. Every ticket.** strip is an informational stage-to-code map. Clicking a stage opens its description and implementation files. It does not execute the pipeline. Ticket details show actual stage-completion events when the API recorded them; no tool calls are invented.

## Current capability boundaries

| Area | Available now |
|---|---|
| Classification/extraction/lookup/routing | Live through the existing pipeline |
| Human review and reassignment | Persisted through the API; unsaved reply text survives reassignment |
| Generated drafts | Live bounded RAG agent for database-backed runs; citations, guardrails and original/final replies remain distinct. Explicit opt-out/no-DB runs skip drafting. |
| Knowledge documents | PDF/MD/TXT storage, deduplication, lifecycle status, index/retry, passage inspection, download and deletion |
| RAG indexing/retrieval | Live OpenRouter embeddings + pgvector; Arabic/category/top-k search and query cost. Health readiness describes configuration/index state, not a provider probe. |
| Weekly insights | Real category/escalation counts and complete-week volumes in Baghdad time |
| Evaluation | Validated import/display of user-provided held-out report JSON. Provenance is labelled unverified; no automatic evaluation runs. |

## Modular file map

```text
src/
  App.tsx                         Routes; secondary screens are lazy-loaded
  components/
    ui/                           shadcn/Base UI primitives
    layout/                       Sidebar, top bar, workspace context
    shared/                       Status, confidence, filters, dialogs, empty/error states
  features/
    queue/                        Queue filters, pagination and triage overview
    review/                       Source evidence, reply editor, audit and stage/tool trace
    runs/                         File/paste intake, batch progress and history
    knowledge/                    Index lifecycle, bounded polling, passage inspection and search
    insights/                     Weekly counts and imported evaluation reports
  hooks/use-resource.ts           Fetching, polling, cancellation and retry
  lib/
    api.ts                        Shared HTTP client and complete-queue loading
    types.ts                      Frontend data contracts
    imports.ts                    Ticket-file and evaluation-report validation
    stages.ts                     Stage labels and source file map
    format.ts                     Shared display/download helpers
  data/preview.ts                 Isolated illustrative fixtures
  styles/workspace.css           Shared semantic layout and responsive styling
```

Backend routes live in `backend/app/api/`; use cases live in `backend/app/services/`. Model execution reuses `pipeline/factory.py` and `pipeline/graph.py`. The UI does not implement its own classifier.

## shadcn conventions

This project uses the **base-nova** style and **Base UI**, not the Radix variant. Use the shared `components/ui` primitives; add domain-level wrappers under `components/shared`. A shadcn Button rendered as a Link or anchor must use `nativeButton={false}`.

```bash
npm exec shadcn -- add <component> --yes
```

If WSL uses corporate certificate authorities, point Node at the system trust bundle:

```bash
NODE_EXTRA_CA_CERTS=/etc/ssl/certs/ca-certificates.crt npm exec shadcn -- add <component> --yes
```

## Verification

```bash
npm test
npm run lint
npm run build
# From the repo root, with the database service running:
uv --directory backend run pytest -q
uv --directory backend run ruff check app tests
```

Backend integration tests use only the dedicated `support_test` database. Frontend unit tests also cover indexing admission/recovery across reloads and historical citation/tool projections.

The [2026-10-17 verification record](../docs/verification/2026-10-17-rag-drafting.md) separates real API/provider/browser checks from Task 7's controlled fake-response UI fault tests. Live checks covered empty knowledge, malformed-source failed indexing/retry, Arabic search, actual drafts, edit/approve/reload and historical citations after source deletion. A 390px review layout had no horizontal overflow. Task 8 independent review is pending.

Use [the demo runbook](../docs/demo-readiness.md) with `data/demo/rag_tickets.jsonl` and the 12 **fictional** policies. They are not real ZainCash terms or the future held-out evaluation set. Remaining work: Plan 2 evaluation; packaging/CI; disclosure, data card and broader failure evidence; weekly statistical reporting (stretch).
