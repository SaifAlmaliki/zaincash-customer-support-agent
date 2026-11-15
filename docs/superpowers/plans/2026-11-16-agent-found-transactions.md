# Agent-Found Transactions Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** When a ticket has no confirmed transaction match, the drafting agent lists the customer's recent transactions by phone, and دليل العملية shows the rows it found (why, when, with whom), labelled as not confirmed.

**Architecture:** Demo data gains declined card attempts. A new drafting prompt `draft_v2` makes the recent-transactions search a rule. The result detail API derives `investigated_transactions` from the persisted `agent_trace` tool results. `TransactionCard` renders them only when there is no confirmed `transaction`.

**Tech Stack:** Python 3.11, FastAPI, Pydantic v2, pytest (run in WSL with `uv`); React 19 + TypeScript, Vitest.

**Spec:** `docs/superpowers/specs/2026-11-16-agent-found-transactions-design.md`

## Global Constraints

- No change to stage 4, `data/taxonomy.yaml` (`card_issue` stays `needs_transaction: false`), the database schema or the agent's tool set.
- Found rows never become a confirmed match: `used_txn_ref`, `check_draft` and the `transaction` field are unchanged.
- `docker/db/seed_demo.sql` and `backend/tests/fixtures/sample_transactions.jsonl` must hold identical transactions (enforced by `tests/test_seed_demo.py::test_seed_transactions_equal_the_startup_fixture`).
- Keep `draft_v1.md` on disk; history traces reference it.
- Backend commands: `wsl -d Ubuntu --cd /mnt/c/Dev/zaincash-customer-support-agent/backend -- bash -lc "uv run --frozen pytest <args>"`. Frontend commands: run in `employee-frontend/`.

## Review Focus

1. A trace entry with `status` `error` or `cancelled` must contribute no rows (Task 3 test `test_failed_tool_calls_contribute_nothing`).
2. The same `txn_ref` returned by two tools appears once (Task 3 test `test_rows_are_deduplicated_and_newest_first`).
3. `lookup_transaction` returns a single object or `null`, not a list; both must work (Task 3 test `test_lookup_single_and_null_results`).
4. Bounded or legacy rows (missing `txn_ref`, non-integer amount, truncated strings) are dropped, never crash the detail endpoint (Task 3 test `test_malformed_rows_are_dropped`).
5. A result with a confirmed `transaction` must not also show the found list (Task 4 test `shows the confirmed transaction instead of found rows`).

---

### Task 1: Declined card attempts in the demo data

**Files:**
- Modify: `docker/db/seed_demo.sql` (transactions `VALUES`)
- Modify: `backend/tests/fixtures/sample_transactions.jsonl`
- Modify: `data/demo/README.md` (`RAG-DEMO-CARD` row)
- Test: `backend/tests/test_demo_data.py`

**Interfaces:**
- Produces: transactions `ZC2410001005`, `ZC2410001006`, `ZC2410001007` for sender `07851110004`, `type` `card`, `status` `declined`, `receiver_phone` null, a fictional merchant in `receiver_name`, `failure_reason` `الدفع الإلكتروني غير مفعّل على البطاقة`, `created_at` between `2026-10-06T18:00:00+03:00` and `2026-10-07T14:59:00+03:00`, increasing with the ref (`1005` earliest). Amounts: 45000, 12000, 8000.

- [ ] **Step 1: Write the failing test** in `backend/tests/test_demo_data.py`

```python
def test_card_ticket_customer_has_declined_card_attempts():
    ticket = {t.external_id: t for t in load_tickets(RAG_TICKETS)}["RAG-DEMO-CARD"]
    repo = InMemoryTransactionRepo(txn_from_dict(r) for r in load_jsonl(FIXTURES / "sample_transactions.jsonl"))
    rows = repo.search(phone=ticket.customer_phone, amount_min=None, amount_max=None,
                       start=ticket.received_at - timedelta(days=14), end=ticket.received_at)
    assert [r.txn_ref for r in rows] == ["ZC2410001007", "ZC2410001006", "ZC2410001005"]
    assert {(r.type, r.status, r.failure_reason) for r in rows} == {
        ("card", "declined", "الدفع الإلكتروني غير مفعّل على البطاقة")}
    assert all(r.receiver_name for r in rows)
```

- [ ] **Step 2: Run it and confirm it fails**

Run: `uv run --frozen pytest tests/test_demo_data.py -q`. Expected: the new test FAILS (empty list).

- [ ] **Step 3: Add the three rows** to `sample_transactions.jsonl` and, with identical values, to the `seed_demo.sql` transactions insert (the `07851110004` customer already exists there). Update the `RAG-DEMO-CARD` README row to name the three declined attempts and their reason.

- [ ] **Step 4: Run the data and seed tests**

Run: `uv run --frozen pytest tests/test_demo_data.py tests/test_seed_demo.py -q`. Expected: all PASS.

- [ ] **Step 5: Commit** (includes the earlier transaction-sync changes already in the working tree)

```bash
git add docker/db/seed_demo.sql backend/tests/fixtures/sample_transactions.jsonl data/demo/README.md data/demo/rag_tickets.jsonl backend/tests/test_demo_data.py backend/tests/test_seed_demo.py docs/superpowers/specs/2026-11-16-agent-found-transactions-design.md docs/superpowers/plans/2026-11-16-agent-found-transactions.md
git commit -m "feat(demo): seed declined card attempts and keep demo transactions in sync"
```

### Task 2: Drafting prompt v2

**Files:**
- Create: `backend/app/pipeline/stage6_draft/prompts/draft_v2.md`
- Modify: `backend/app/pipeline/stage6_draft/agent.py:38` (`PROMPT_VERSION`)
- Test: `backend/tests/test_rag_drafter.py`

**Interfaces:**
- Produces: `agent.PROMPT_VERSION == "draft_v2"`; drafted traces carry `"prompt_version": "draft_v2"`.

- [ ] **Step 1: Write the failing test** in `backend/tests/test_rag_drafter.py`

```python
def test_prompt_v2_requires_recent_transactions_without_a_confirmed_match():
    from pathlib import Path

    from app.pipeline.stage6_draft import agent

    assert agent.PROMPT_VERSION == "draft_v2"
    assert "get_customer_recent_transactions" in agent.SYSTEM_PROMPT
    assert "not `matched`" in agent.SYSTEM_PROMPT
    assert (Path(agent.__file__).with_name("prompts") / "draft_v1.md").exists()
```

- [ ] **Step 2: Run it and confirm it fails**

Run: `uv run --frozen pytest tests/test_rag_drafter.py -q -k prompt_v2`. Expected: FAIL on `"draft_v1" == "draft_v2"`.

- [ ] **Step 3: Create `draft_v2.md`** as a copy of v1 with this paragraph inserted after the "Investigated candidates…" sentence:

```
If the supplied lookup status is not `matched` and the ticket concerns money, a
payment or a card, call get_customer_recent_transactions for the ticket customer's
phone before submitting. In internal_note, summarize the relevant rows for the
reviewer: time, counterparty, amount, status and failure reason. These rows stay
unconfirmed: do not state their amounts, dates or references in reply_ar.
```

Set `PROMPT_VERSION = "draft_v2"`.

- [ ] **Step 4: Run the drafter tests**

Run: `uv run --frozen pytest tests/test_rag_drafter.py tests/test_rag_api.py -q`. Expected: all PASS.

- [ ] **Step 5: Commit**

```bash
git add backend/app/pipeline/stage6_draft/prompts/draft_v2.md backend/app/pipeline/stage6_draft/agent.py backend/tests/test_rag_drafter.py
git commit -m "feat(draft): list recent transactions when no confirmed match (draft_v2)"
```

### Task 3: `investigated_transactions` in the result detail

**Files:**
- Modify: `backend/app/services/draft_evidence.py`
- Test: create `backend/tests/test_draft_evidence.py`; extend `backend/tests/test_rag_api.py::test_old_or_invalid_traces_have_safe_unknown_defaults`

**Interfaces:**
- Produces: `draft_evidence(trace, citations)` adds key `"investigated_transactions": list[dict]`. Each dict has exactly the `TxnRecord` fields: `txn_ref`, `sender_phone`, `receiver_phone`, `receiver_name`, `amount_iqd`, `type`, `status`, `created_at` (ISO string as stored), `biller`, `agent_id`, `failure_reason`. Sources: trace events with `kind == "tool"`, `status == "ok"`, `tool` in `{"lookup_transaction", "search_transactions", "get_customer_recent_transactions"}`; `result` may be a list, a single object or `null`. Rows are validated by a new `_TraceModel` subclass `InvestigatedTransaction` (`txn_ref` 1–32 chars, `amount_iqd` int ≥ 0, `created_at` parseable by `app.datetime.parse_dt`), deduplicated by `txn_ref` (first wins), sorted by `created_at` newest first.

- [ ] **Step 1: Write the failing tests** in `backend/tests/test_draft_evidence.py`, built from a helper `row(ref, at, **extra)` that returns a full valid row dict and a helper `tool(name, result, status="ok")`:

- `test_rows_are_deduplicated_and_newest_first`: recent → `[row("A", "2026-10-06T20:00:00+03:00"), row("B", "2026-10-07T09:00:00+03:00")]`, search → `[row("B", ...)]`; assert refs `== ["B", "A"]`.
- `test_failed_tool_calls_contribute_nothing`: same recent result with `status="error"` and `status="cancelled"`; assert `== []`.
- `test_lookup_single_and_null_results`: `tool("lookup_transaction", row("C", ...))` and `tool("lookup_transaction", None)`; assert refs `== ["C"]`.
- `test_malformed_rows_are_dropped`: rows missing `txn_ref`, with `amount_iqd: "45000"`, with `created_at: "…"`, plus `None` and `"x"`, alongside one valid row; assert only the valid ref remains.
- `test_other_tools_are_ignored`: `search_knowledge_base` result shaped like a row; assert `== []`.

In `test_rag_api.py`, add `assert detail["investigated_transactions"] == []` to `test_old_or_invalid_traces_have_safe_unknown_defaults`.

- [ ] **Step 2: Run them and confirm they fail**

Run: `uv run --frozen pytest tests/test_draft_evidence.py -q`. Expected: FAIL with `KeyError: 'investigated_transactions'`.

- [ ] **Step 3: Implement** the model and collection inside `draft_evidence`'s existing single pass over `trace`; return the new key.

- [ ] **Step 4: Run the evidence and API tests**

Run: `uv run --frozen pytest tests/test_draft_evidence.py tests/test_rag_api.py tests/test_workspace_api.py -q`. Expected: all PASS.

- [ ] **Step 5: Commit**

```bash
git add backend/app/services/draft_evidence.py backend/tests/test_draft_evidence.py backend/tests/test_rag_api.py
git commit -m "feat(api): expose transactions the drafting agent found"
```

### Task 4: Found rows in دليل العملية

**Files:**
- Modify: `employee-frontend/src/lib/types.ts` (`Result`)
- Modify: `employee-frontend/src/features/review/SourceEvidence.tsx` (`ledgerValue`, `TransactionCard`)
- Modify: `employee-frontend/src/locales/ar.json`, `employee-frontend/src/locales/en.json` (`evidence`)
- Test: create `employee-frontend/src/features/review/transaction-card.test.tsx`

**Interfaces:**
- Consumes: `investigated_transactions` from Task 3.
- Produces: `export type InvestigatedTransaction = Record<string, string | number | null>`; `Result.investigated_transactions?: InvestigatedTransaction[]`. New copy keys: `evidence.found` ("عمليات وجدها البحث (غير مؤكدة)" / "Found by the AI search (not confirmed)"), `evidence.foundHelp` ("وجدها المساعد بالبحث برقم الزبون. تحقق منها قبل تأكيد أي تفصيل للزبون." / "The assistant found these by the customer's phone. Verify before confirming any detail to the customer."), `evidence.txn.failure_reason` ("سبب الفشل" / "Failure reason"). `ledgerValue` labels: status `declined` → "مرفوضة" / "Declined"; type `card` → "دفع بالبطاقة" / "Card payment".

- [ ] **Step 1: Write the failing tests** (style of `customer-message.test.tsx`, `renderToStaticMarkup` + `resultFixture`)

- `shows found rows when there is no confirmed transaction`: `transaction: null`, `lookup_status: "not_applicable"`, two rows (`ZC2410001006` at `متجر الرافدين` 12000 declined card with the spec reason; `ZC2410001005`). Assert the HTML contains "عمليات وجدها البحث (غير مؤكدة)", "متجر الرافدين", "12,000 IQD", "مرفوضة", "دفع بالبطاقة", "الدفع الإلكتروني غير مفعّل على البطاقة", and does not contain "هذه المشكلة لا تحتاج البحث عن عملية".
- `shows the confirmed transaction instead of found rows`: a `transaction` plus one found row; assert the found heading is absent.
- `keeps the skipped message when nothing was found`: no `transaction`, `investigated_transactions: []`; assert "هذه المشكلة لا تحتاج البحث عن عملية" is present.

- [ ] **Step 2: Run them and confirm they fail**

Run: `npm test -- src/features/review/transaction-card.test.tsx`. Expected: the first test FAILS.

- [ ] **Step 3: Implement.** In `TransactionCard`: confirmed `transaction` → today's `<dl>`. Else non-empty `investigated_transactions` → the `found` heading, `foundHelp` as `muted`, then one `compare-rows` block per row showing `created_at`, `receiver_name` (falling back to `receiver_phone`), `amount_iqd`, `type`, `status`, `failure_reason`, `txn_ref`, using `ledgerValue` and skipping empty values. Else today's message.

- [ ] **Step 4: Run the frontend checks**

Run: `npm test`, `npm run typecheck`, `npm run lint`. Expected: all pass.

- [ ] **Step 5: Commit**

```bash
git add employee-frontend/src/lib/types.ts employee-frontend/src/features/review/SourceEvidence.tsx employee-frontend/src/locales/ar.json employee-frontend/src/locales/en.json employee-frontend/src/features/review/transaction-card.test.tsx
git commit -m "feat(review): show transactions the AI search found"
```

### Task 5: Full verification

- [ ] **Step 1:** Run the full backend suite: `uv run --frozen pytest -q`. Expected: all pass.
- [ ] **Step 2:** Rebuild the API (`docker compose up -d --build api`), apply `cleanup.sql` then `seed_demo.sql`, re-index `data/kb-pdf`, upload `data/demo/rag_tickets.jsonl`. Open `RAG-DEMO-CARD`: دليل العملية lists `ZC2410001005`–`1007` as declined card payments with merchant, time and reason, and the internal note summarizes them. Paid calls: confirm with the user before this step.
