# ZainCash Support Pipeline

Back-office automation for Iraqi Arabic support tickets. Each ticket is classified, its details are extracted, the transaction is looked up, the ticket is routed to a team, and a reply is drafted from the knowledge base.

Built for the **Agentic AI Challenge Iraq, Topic 06: Support Pipeline Automation**.

> **A person approves every reply.** The system never sends messages, moves money, or changes accounts. Anything uncertain or unsafe is escalated with a reason.

## How it works

```mermaid
flowchart LR
  intake["Customer intake app :5174"] --> api["API :8000"]
  workspace["Employee workspace :5173"] --> api
  api --> pipeline["Ticket pipeline"]
  pipeline --> models["AI models<br/>OpenRouter (cloud) · Ollama (local) · TypeSafe Jev (cloud)"]
  pipeline --> db[("PostgreSQL + pgvector :5433")]
  pipeline --> review["Employee reviews"]
```

| Step | What happens | Default model |
|---|---|---|
| Intake | The customer describes the problem in a chat and can attach screenshots. | `anthropic/claude-sonnet-5.5` |
| Classify | Category, priority, flags, and the text spans for each field. | `jev-1.13.0` (TypeSafe) |
| Extract | Normalizes the fields. A model is asked only when a required field is missing. | `google/gemini-3.8-flash` |
| Lookup | Matches the transaction in the database. | none |
| Decide | Picks the team and priority from [`data/taxonomy.yaml`](data/taxonomy.yaml), or escalates. | none |
| Draft | Searches the knowledge base, writes a cited Arabic reply, and runs safety checks. | `anthropic/claude-sonnet-5.5` · embeddings `openai/text-embedding-3-small` |
| Review | An employee approves, edits, rejects, or reassigns. Nothing is sent automatically. | none |

An empty ticket skips straight to review as an escalation.

## Choosing models

The defaults above come from `.env`. An admin can change the model of any step while the system runs:

1. Set `ADMIN_TOKEN` in `.env` and restart the API.
2. In the employee workspace, open **Admin → AI models** and enter the token.
3. Click **Change model** on a step, pick a provider and a model, click **Test model**, then **Save**.

What to know:

- **Providers:** OpenRouter (cloud) and Ollama (local) for intake, extract, draft, and embeddings. Classification always uses Jev on TypeSafe.
- **Only suitable models are listed.** Drafting needs tool calling, intake needs vision, and embeddings must be 768 dimensions. You can also type any model ID.
- **A model is saved only after a live test passes.**
- **Changes apply to new batches and new customer chats.** Customers never see a change, and a chat keeps one model from start to finish.
- **No silent fallback (Intentional).** If the chosen provider is down, the step fails and the ticket goes to a person with the reason. Nothing switches to another provider on its own.
- **Changing the embedding model re-indexes the knowledge base.** New batches wait until it finishes, and the switch cannot start while a batch is running.
- The top bar shows **AI: Local**, **AI: Cloud**, or **AI: Mixed**, so everyone can see where ticket data goes. Each run page lists the models it used.

### AI usage and performance (`/evaluation`)

Every AI call is recorded in the `ai_calls` table:

- customer intake, Jev classification, detail extraction and reply drafting;
- knowledge search during drafting and the credential check;
- knowledge indexing, manual knowledge search and admin model tests.

Each row holds the model, start time, latency, tokens, cost, cost source (provider-reported,
estimated, local or unknown) and errors. Prompts and ticket text are never stored.

The Evaluation page shows, for a chosen period, process, model or batch run:

- total AI cost, cost per ticket and AI time per ticket;
- cost and time by process and by model, with local models shown as **Local · $0**;
- a daily trend;
- every ticket with its cost split and a timeline of its AI calls.

Estimates use the price saved with the admin's model choice (taken from the OpenRouter
catalog), or the `.env` prices for the default models; any other model shows "Price unknown".
Results processed before tracking began show only their totals.

## Quick start

You need WSL Ubuntu, Docker, `uv`, Node.js, a TypeSafe key, and an OpenRouter key.

1. **Configure.** Create a `.env` file in the repository root (it is gitignored). Copy the block below in full: it is the file the demo and the test suite run with. Replace the three secrets and keep the other values so your run matches this repository.

   ```bash
   # --- Providers (required to process a ticket) ---
   OPENROUTER_API_KEY=...
   TYPESAFE_API_KEY=...

   # --- Models ---
   # Drafting uses ANTHROPIC_MODEL when set, otherwise GEMINI_MODEL
   # (default google/gemini-3.8-flash, also the extraction model).
   ANTHROPIC_MODEL=anthropic/claude-sonnet-5.5
   # Intake uses this model. It must support vision and structured output.
   # Empty falls back to GEMINI_MODEL.
   INTAKE_MODEL=anthropic/claude-sonnet-5.5

   # --- Classification and pipeline ---
   JEV_MODEL=jev-1.13.0
   T_JEV=0.6
   JEV_MIN_TOP_PROB=0.60
   PIPELINE_CONCURRENCY=20
   MAX_STATE_CHARS=6000
   AGENT_MAX_TOOL_CALLS=6
   AGENT_TIMEOUT_S=30

   # --- Embeddings ---
   # Must stay 768 to match the knowledge index schema.
   EMBED_DIM=768

   # --- Tests (host pytest only; Compose clears this inside the API container) ---
   TEST_DATABASE_URL=postgresql+psycopg://support:support@localhost:5433/support_test

   # --- Local models and admin ---
   OLLAMA_BASE_URL=http://localhost:11434
   # Empty disables the admin page. Any non-empty value turns it on.
   ADMIN_TOKEN=...
   ```

   `OPENROUTER_API_KEY` and `TYPESAFE_API_KEY` have to be real keys before a batch or a customer chat can call a model. `ADMIN_TOKEN` is the password for **Admin → AI models**. `TEST_DATABASE_URL` is what `uv run pytest` connects to on the host; its user and password must match `secrets/` (the examples are `support` / `support`). The database name stays `support_test`.

   Anything not listed here has a default in [`backend/app/config.py`](backend/app/config.py). Add a line only to override one. Leave `DATABASE_URL` unset: the API container builds it from the Compose secrets. Those secrets are the tracked files `secrets/postgres_user.example`, `secrets/postgres_password.example`, and `secrets/postgres_db.example` (each is `support`).
2. **Start the database and API:**
   ```bash
     docker compose up --build -d
   ```
3. **Start the employee workspace:**
   ```bash
     cd employee-frontend && npm ci && npm run dev
   ```
4. **Start the customer intake app** (optional):
   ```bash
     cd users-frontend && npm ci && npm --workspace web run dev
   ```

| App | Address |
|---|---|
| Employee workspace | http://localhost:5173 |
| Customer intake | http://localhost:5174 |
| API docs | http://localhost:8000/api/docs |
| PostgreSQL | `localhost:5433` |

After you change `.env`, restart the API (`docker compose up -d --build api`). Changes made on the admin page apply without a restart.

### Reset the demo database

Customers are identified by their phone number (`07XXXXXXXXX`), and every ticket and customer conversation belongs to one. A database created before this change cannot be upgraded in place: the API stops at startup and asks for a reset. To reset:

```bash
docker compose down -v
docker compose up --build -d
```

`docker compose down -v` also deletes uploaded knowledge-base documents, saved admin model choices and all tickets, runs and reviews.

Then load the demo data: in pgAdmin (database `support`, `localhost:5433`), run `docker/db/cleanup.sql` and then `docker/db/seed_demo.sql`.

## Local models with Ollama

1. Pull the models:
   ```bash
     ollama pull qwen3:4b          # extract and draft
     ollama pull nomic-embed-text  # embeddings (768 dimensions)
     ollama pull gemma3:4b         # intake (needs vision; qwen3:4b has none)
   ```
2. Make Ollama reachable from the API and set `OLLAMA_BASE_URL` in `.env`:
   - **Ollama on Windows, API in WSL or Docker inside WSL:** set the Windows user variable `OLLAMA_HOST=0.0.0.0:11434`, restart Ollama, and use `http://<windows-ip>:11434`. Run `ip route show default` in WSL to get the IP. Alternatively, enable WSL mirrored networking and use `http://localhost:11434`.
   - **Docker Desktop:** `http://host.docker.internal:11434`.
3. Choose the Ollama models on **Admin → AI models**.

Local models are slower. The settings `LOCAL_AGENT_TIMEOUT_S`, `LOCAL_INTAKE_TIMEOUT_S`, `LOCAL_NUM_CTX` (context window), and `LOCAL_PIPELINE_CONCURRENCY` (tickets processed at once) control them. Because Jev runs in the cloud, an all-Ollama setup shows **AI: Mixed**.

## Assumptions

Routing follows the [FAZAA design brief](presentation/SaifAlmaliki_Topic06_FAZAA_Design_Brief.pptx). [`data/taxonomy.yaml`](data/taxonomy.yaml) is the source of truth for categories, teams, and priority minimums. The classifier names the issue. Code in [`backend/app/pipeline/stage5_decide/rules.py`](backend/app/pipeline/stage5_decide/rules.py) assigns the team and the final urgency. A person reviews every outcome.

- One ticket has one category, and that category belongs to one team.
- The model proposes the category and an urgency. The team comes from the category.
- The final priority is the most urgent of the model's proposal, the category minimum, and the risk rules below. Those rules only raise urgency.
- A fraud flag keeps the category's team. The reviewer can reassign.
- Escalation is a review status. The ticket keeps its team, and the reason is saved with it.
- Failed transfer, wrong recipient, agent dispute, bill payment, and refund request need a transaction match. The other seven categories do not.

### Priorities

P1 is the most urgent. The values below are minimums. A ticket's final priority can be more urgent.

| Priority | Meaning |
|---|---|
| P1 | Money at risk now, or fraud |
| P2 | Money lost or stuck |
| P3 | A service is blocked |
| P4 | A request for information |

A fraud score above 0.5 sets the priority to P1. A fraud report is already P1, and it is always escalated. A money-lost score above 0.5 raises the priority to at least P2, so a card issue that starts at P3 becomes P2 when money is missing. Low confidence, several issues in one ticket, a request for a person, missing details, or a transaction that is missing, ambiguous, or inconsistent escalates the ticket and leaves the category's team in place.

### Teams

Seven teams. Each one is assumed to own one kind of work, and the categories are assigned on that basis.

| Team | Assumed ownership | Categories |
|---|---|---|
| Payments Ops | Money movement that did not complete: transfers and bills | Failed transfer, bill payment |
| Disputes | Money that went to the wrong place, or that a merchant should return | Wrong recipient, refund request |
| Account & Security | The account itself: access, identity, and fraud | Login / access, account / KYC, fraud report |
| Agent Network | A ZainCash agent or shop | Agent dispute |
| Cards | The Mastercard or virtual card | Card issue |
| Tech Support | The app, when no money is missing | App bug |
| General Care | Questions, and anything that fits nowhere else | General inquiry, other |

### Categories

Twelve categories. Each row is the assumption the classifier and the rulebook share: what the category covers, who owns it, and the lowest priority it can have.

| Category | Team | Minimum | What it covers |
|---|---|---|---|
| Failed transfer | Payments Ops | P2 | A transfer that failed, is pending, or left the wallet and did not arrive |
| Bill payment | Payments Ops | P3 | A bill or top-up that failed, or that the biller did not apply |
| Wrong recipient | Disputes | P2 | Money sent to the wrong number or person by mistake |
| Refund request | Disputes | P3 | Money back from a merchant or a cancelled service |
| Login / access | Account & Security | P3 | Cannot log in, a forgotten PIN, a missing verification code, or a locked account |
| Account / KYC | Account & Security | P4 | Verification, account level, ID documents, limits, or a change of account details |
| Fraud report | Account & Security | P1 | A scam, a request for the OTP or PIN, an unauthorized transaction, or a hacked account |
| Agent dispute | Agent Network | P2 | Cash-in or cash-out not credited, an extra fee, or a refused service at an agent |
| Card issue | Cards | P3 | A card declined, blocked, not delivered, or charged twice for one purchase |
| App bug | Tech Support | P3 | A crash, an error, or a feature that does not work, with no money lost |
| General inquiry | General Care | P4 | Fees, limits, how to do something, agent locations, or promotions |
| Other | General Care | P4 | Anything else, including a complaint with no clear request |

Neighboring categories stay separate. A transfer that failed technically is a failed transfer. A number the customer typed wrong is a wrong recipient. A bill or top-up is a bill payment. Someone else inside the account is a fraud report. An app error that also lost money stays with the money category. A question with no incident is a general inquiry.

## Try the demo

1. This architecture uses retrieval-augmented generation (RAG) to index ZainCash policy, then search that index when it drafts a reply. Index the twelve policy PDFs in [`data/kb-pdf`](data/kb-pdf) first:
   ```bash
     uv --directory backend run support ingest-kb ../data/kb-pdf
   ```

   Wait until each file is **Indexed**.
2. Start the API and the employee workspace if they are not already running (Quick start steps 2 and 3). The customer intake app is not needed for this step. In the browser, open http://localhost:5173, click **New batch**, upload [`data/demo/rag_tickets.jsonl`](data/demo/rag_tickets.jsonl), and click **Start processing**.
3. Open the results. Edit a reply and choose **Save & approve**.

The demo data and the files in `data/kb-pdf/` are fictional, not real ZainCash policies. See the [demo walkthrough](docs/demo-readiness.md).

## Test cases

Load the demo database first (`docker/db/cleanup.sql`, then `docker/db/seed_demo.sql`). Open the customer app at http://localhost:5174, enter the phone, and send the message. In the employee workspace, **دليل العملية** should show the seeded transaction.

1. **Pending transfer that left the wallet.** Phone `07809876543`. Matches pending `ZC2410000123`, 50,000 IQD to علي حسين on 2026-10-06.

   حولت 50,000 دينار يوم 2026-10-06 على رقم 07701234567 باسم علي حسين وانقطعت من رصيدي بس ما وصلتله. رقم العملية ZC2410000123 والتحويل للحين معلق.
2. **Receiver never got that transfer.** Phone `07701234567`. Same pending transfer, from the receiver's side.

   انا علي حسين. في تحويل 50,000 دينار يوم 2026-10-06 من رقم 07809876543 وما وصلني. رقم العملية ZC2410000123.
3. **Electricity bill marked paid but not posted.** Phone `07723334455`. Matches completed bill `ZC2410000456`, 35,000 IQD on 2026-10-01.

   دفعت فاتورة الكهرباء 35,000 دينار يوم 2026-10-01 وطلعت ناجحة بالتطبيق بس ما انحسبت عند الكهرباء. رقم العملية ZC2410000456.
4. **Completed transfer the sender did not make.** Phone `07501112233`. Fraud report that still matches completed `ZC2410000789`, 200,000 IQD on 2026-10-07.

   ما حولت اني. انسحب من حسابي 200,000 دينار يوم 2026-10-07 على رقم 07901234567 بعد ما اتصل بيه شخص وطلب رمز التحقق. رقم العملية ZC2410000789.
5. **Receiver got money from someone they do not know.** Phone `07901234567`. Same completed transfer, from the receiver's side.

   وصلني تحويل 200,000 دينار يوم 2026-10-07 من رقم 07501112233 وانا ما اعرف المرسل. رقم العملية ZC2410000789.

## Checks

```bash
cd backend && uv run pytest -q && uv run ruff check app tests
cd employee-frontend && npm test && npm run lint && npm run build
```

Backend integration tests use the separate `support_test` database at `TEST_DATABASE_URL` from `.env`. Start the database first (`docker compose up -d db`) so that URL can connect. To process a file of tickets from the command line:

```bash
uv --directory backend run support run-batch ../data/demo/rag_tickets.jsonl --out ../out/run.json
```

## More documentation

- [Demo walkthrough and open work](docs/demo-readiness.md)
- [Pipeline design](docs/superpowers/specs/2026-10-07-support-pipeline-design.md)
- [Admin model configuration design](docs/superpowers/specs/2026-11-12-admin-model-config-design.md)
- Verification records: [RAG drafting](docs/verification/2026-10-17-rag-drafting.md), [customer intake](docs/verification/2026-10-18-customer-intake.md)

## License

This project is proprietary. The [license](LICENSE) lets a recipient read and study the source and ask the copyright holder questions. Publishing, selling, sharing it outside that recipient, or reusing it requires Saif Almaliki's prior written approval.
