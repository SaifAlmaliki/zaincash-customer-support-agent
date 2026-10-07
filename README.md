# ZainCash Support Pipeline

This is a back-office pipeline for ZainCash support tickets written in Iraqi dialect. For each ticket it decides the category, sets a priority, extracts the key details, finds the matching transaction, routes the ticket to the right team, and drafts a reply for a person to approve. It is not a chatbot, and it never sends anything on its own. If it is unsure about a ticket, it escalates it to a person with a note.

Built for the **Agentic AI Challenge Iraq, Topic 06: Support Pipeline Automation**.

## How a ticket flows

```mermaid
flowchart TD
    %% Nodes (declared first so every box shows its label)
    A([Support tickets arrive<br/>paste · CSV/JSON upload · CLI batch])
    B[Clean the text<br/>Arabic digits → 0-9, hide card numbers]
    C[Jev reads the ticket<br/>category · priority · red flags<br/>picks amount, date, phone, transaction ID]
    D{Is Jev confident?}
    E[Gemini gives a second opinion<br/>asked 3 times]
    F{Gemini confident<br/>and agrees?}
    G[Look up the transaction<br/>in ZainCash records]
    H[Route to the right team<br/>and set priority]
    I{Any red flags?<br/>fraud · several issues · missing info<br/>transaction not found · amount mismatch}
    J[AI agent drafts a reply in Iraqi Arabic<br/>using policy documents + transaction]
    K{Draft passes safety checks?<br/>cites policy · no invented numbers<br/>never asks for OTP/PIN}
    R[Ready for review]
    X[Escalate to a human<br/>with a short note explaining why]
    Q[Support agent reviews<br/>Approve · Edit · Reject]
    Z([Agent sends the approved reply<br/>nothing is sent automatically])

    %% Flow
    A --> B --> C --> D
    D -- Yes --> G
    D -- No --> E --> F
    F -- Yes --> G
    F -- No --> X
    G --> H --> I
    I -- Yes --> X
    I -- No --> J --> K
    K -- No --> X
    K -- Yes --> R
    X --> Q
    R --> Q
    Q --> Z

    classDef terminal fill:#e8f5c8,stroke:#6b8f3c,color:#1a1a1a
    classDef decision fill:#d6ecff,stroke:#3b82f6,color:#1a1a1a
    classDef action fill:#efe6ff,stroke:#8b7cc9,color:#1a1a1a
    classDef escalate fill:#f8e6df,stroke:#c4a090,color:#1a1a1a

    class A,Z terminal
    class D,F,I,K decision
    class B,C,E,G,H,J,R action
    class X,Q escalate
```

Colours in the diagram:
- **Green:** where tickets come in and where they finish.
- **Blue:** decisions the pipeline makes.
- **Purple:** automatic steps.
- **Orange:** steps a person handles.

Every path ends with a person approving the reply.

## Models

| Model | What it does here |
|---|---|
| **Jev** (TypeSafe System One) | Fast, cheap classification. Its confidence scores are calibrated, and it picks extracted values directly from the ticket text, so it cannot invent them. |
| **Gemini** | Second opinion on uncertain tickets, fallback extraction, the drafting agent, and the embeddings used to search the knowledge base |

## Design

The full design is in [`docs/superpowers/specs/2026-10-07-support-pipeline-design.md`](docs/superpowers/specs/2026-10-07-support-pipeline-design.md).

## Quickstart (WSL Ubuntu, Docker Engine, uv)

Run from the repository root in WSL:

```bash
test -f .env || cp .env.example .env
# Set GOOGLE_API_KEY and TYPESAFE_API_KEY in .env before continuing.
docker compose up -d db
cd backend
uv sync
uv run support seed-db --transactions tests/fixtures/sample_transactions.jsonl \
  --incidents tests/fixtures/sample_incidents.jsonl
uv run support run-batch tests/fixtures/sample_tickets.jsonl --mode cascade --out ../out/run.json
```

`seed-db` creates the schema and loads the synthetic records. Postgres is exposed on host port **5433**.

`--mode` is one of `jev`, `gemini` or `cascade` (the default). Add `--no-db --transactions <file>` to run without Postgres:

```bash
uv run support run-batch tests/fixtures/sample_tickets.jsonl --mode jev --no-db \
  --transactions tests/fixtures/sample_transactions.jsonl --out ../out/smoke-jev.json
```

Ticket files can be `.jsonl`, `.json` or `.csv`. Each row needs `text`; `external_id`, `channel`, `customer_phone` and `received_at` are optional. `cascade` needs both API keys; `gemini` needs `GOOGLE_API_KEY`. `jev` needs `TYPESAFE_API_KEY` and can also use `GOOGLE_API_KEY` for fallback extraction.

Run the checks from `backend/`:

```bash
uv run pytest -q
uv run ruff check app tests
```

The Postgres integration tests need the database service running; they use the separate `support_test` database.

### Corporate-network troubleshooting

If Gemini fails with `CERTIFICATE_VERIFY_FAILED` and your organization’s trusted CA is already installed in Ubuntu, point the SDK at the system CA bundle before running the CLI:

```bash
export SSL_CERT_FILE=/etc/ssl/certs/ca-certificates.crt
```

A subsequent HTTP 403 HTML response from Zscaler means the network policy is blocking `generativelanguage.googleapis.com`. Approved access to that endpoint is needed before the Gemini smoke run can pass.

## Status

The core pipeline and CLI are implemented. **Plan 1 Task 15 is partially verified:** the live Gemini check is blocked by the current network policy. Reply generation still uses `NullDrafter`; RAG drafting comes in Plan 3.

Live smoke results on 2026-10-07:

| Check | Result |
|---|---|
| Jev response shape (`jev-1.13.0`) | Passed; adapter and fake are compatible |
| In-memory `jev` | 5 tickets, no failures |
| In-memory `gemini` | All 5 failed TLS verification; a separate probe using the system CA bundle confirmed a Zscaler HTTP 403 policy block |
| In-memory `cascade` | 5 tickets, no failures; all used Jev, so Gemini fallback was not exercised |
| Database `cascade`, run twice | Runs 1 and 2 completed with 5 results each; 5 ticket rows total |

The cascade fixture checks passed: S-001 was `failed_transfer`, matched its transaction and extracted **50,000 IQD**; S-002 escalated for `fraud_suspected` at **P1**; S-005 was `general_inquiry` at **P4**. Per-ticket outputs are saved locally to `out/smoke-{jev,gemini,cascade}.json`.

After approved Gemini access is available, rerun the in-memory command above with `--mode gemini --out ../out/smoke-gemini.json` and confirm `total: 5` and `failed_ids: []` before closing Task 15.

The remaining plans cover synthetic data and evaluation, RAG drafting, the review workspace, and the weekly report. Disclosure and failure-mode documentation land with Plan 5.
