# Show the transactions the drafting agent found

## Why

A ticket without a reference number (for example `RAG-DEMO-CARD`, "الماستر كارد مالتي ترفض بكل موقع من امس") gets no stage-4 match, so the reviewer sees "this issue does not need a transaction lookup" and nothing else. The customer's phone is the reference. The drafting agent should list that customer's recent transactions, and the reviewer should see the rows it found: why each attempt failed, when, and with whom.

## Goals

- The agent lists the customer's recent transactions whenever no confirmed match is supplied and the ticket is about money, a payment or a card.
- **دليل العملية** shows the rows the agent's searches returned when there is no confirmed match, clearly labelled as found by the AI search and not confirmed.
- The demo data contains declined card attempts for the `RAG-DEMO-CARD` customer.

## Non-goals and anti-goals

- No change to stage 4, the taxonomy (`card_issue` stays `needs_transaction: false`), the database schema or the tool set.
- Found rows never become a confirmed match. `used_txn_ref` and the guardrails still accept only the stage-4 match, so the customer reply cannot state the found amounts or dates.
- Failure: the panel shows rows the agent did not retrieve for this ticket, or presents them as confirmed.

## Approaches

| Approach | Trade-off |
|---|---|
| A. Seed data and prompt only | Cheapest. The reviewer sees only the agent's prose in the internal note. |
| **B. A, plus show the agent's found rows (chosen)** | The reviewer sees the exact database rows. Empty if the agent skips the search or times out. |
| C. System always lists the phone's last 14 days | Most reliable, but the search is not the agent's. |

The user chose B.

## Design

1. **Data.** Add three declined card attempts for `07851110004` before the ticket (2026-10-07 15:00 Baghdad) to both `docker/db/seed_demo.sql` and `backend/tests/fixtures/sample_transactions.jsonl`. The existing sync test keeps the two files equal. My proposal: `ZC2410001005`–`1007`, `type` `card`, `status` `declined`, three fictional merchants in `receiver_name`, one consistent `failure_reason` such as `الدفع الإلكتروني غير مفعّل على البطاقة`, on 2026-10-06 evening and 2026-10-07. Update `data/demo/README.md`.
2. **Prompt.** New `draft_v2.md`, a copy of v1 plus one rule: if the supplied lookup is not `matched` and the ticket concerns money, a payment or a card, call `get_customer_recent_transactions` for the ticket customer's phone before submitting, and summarize relevant rows (time, counterparty, status, reason) in `internal_note`. `PROMPT_VERSION` becomes `draft_v2`. v1 stays for history.
3. **API.** `draft_evidence` also returns `investigated_transactions`: rows from successful `lookup_transaction`, `search_transactions` and `get_customer_recent_transactions` trace results. Each row is validated (malformed rows dropped), deduplicated by `txn_ref` and sorted newest first.
4. **UI.** `TransactionCard` keeps today's view when a confirmed transaction exists. Otherwise, if found rows exist, it shows a "found by the AI search, not confirmed" heading and one row per transaction: time, counterparty (`receiver_name`, else `receiver_phone`), amount, type, status and failure reason. Otherwise it shows today's message. Add labels for type `card` and status `declined` in both languages.

## Left to the builder

Exact merchant names, amounts and times; the Arabic and English copy; row layout within the existing card styles.
