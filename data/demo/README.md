# Fictional RAG walkthrough inputs

The policy reference is [`data/kb-pdf`](../kb-pdf): twelve fictional PDFs, one per category in `data/taxonomy.yaml`. Index that folder before running these tickets. Category text inside a PDF is descriptive; ingestion does not infer database category tags from it. Untagged documents stay eligible for category-filtered retrieval.

Everything in `../kb-pdf/` and `rag_tickets.jsonl` is **synthetic, fictional demo material**. It is not a statement of real ZainCash policy, fees, limits, reimbursement guarantees, response deadlines or account access. The assistant cannot move funds, freeze accounts or send replies.

| Fixture | Intended observation (verify actual output) |
|---|---|
| `RAG-DEMO-FAILED-TRANSFER` | Existing synthetic `ZC2410000123`, 50,000 IQD, **pending**, sent on 2026-10-06; relevant pending-transfer citation, no completion/refund promise. |
| `RAG-DEMO-GENERAL` | Safe, non-secret support information; Arabic draft grounded in `general_inquiry.pdf`. |
| `RAG-DEMO-FRAUD` | Existing synthetic sender `07501112233` / `ZC2410000789`, 200,000 IQD; preserve `fraud_suspected` and P1 regardless of whether a draft is produced. |
| `RAG-DEMO-UNSUPPORTED` | Quantum-entanglement question outside this corpus; no invented scientific answer. Record actual rejection/escalation and any irrelevant retrieval. |
| `RAG-DEMO-WRONG-RECIPIENT` | Completed `ZC2410001001`, 100,000 IQD from `07821110001` to `07706543210` on 2026-10-07. |
| `RAG-DEMO-LOGIN` | Forgotten PIN and a verification code that never arrives. No stolen money. |
| `RAG-DEMO-AGENT` | Failed cash-in `ZC2410001002`, 200,000 IQD, agent `AG-JU`, on the morning of 2026-10-07. |
| `RAG-DEMO-CARD` | Mastercard declined at merchants, with no wallet debit. |
| `RAG-DEMO-BILL` | Completed Asia top-up `ZC2410001003`, 10,000 IQD, on 2026-10-07. |
| `RAG-DEMO-KYC` | Identity document rejected while raising the account level. |
| `RAG-DEMO-REFUND` | Completed merchant purchase `ZC2410001004`, 25,000 IQD at متجر النور, on 2026-10-07. |
| `RAG-DEMO-APP-BUG` | App closes on open after an update. Balance unchanged. |
| `RAG-DEMO-OTHER` | Vague service complaint with no specific request. |

Dates are fixed so “امس” in the transfer fixture resolves to the existing transaction. The original five Plan 1 smoke inputs remain under `backend/tests/fixtures/`. These inputs are deliberately visible development/demo examples, **not held-out evaluation data** and not an accuracy benchmark. The first four IDs and their text stay fixed so a re-upload matches the seeded rows. The later rows cover the remaining taxonomy categories. The four that report a payment have matching rows in `docker/db/seed_demo.sql` and in `backend/tests/fixtures/sample_transactions.jsonl`, which the API seeds at startup. `backend/tests/test_seed_demo.py` and `backend/tests/test_demo_data.py` keep these files in step. Login, card, account verification, the app crash, the general question, and the vague complaint do not name a payment, so lookup stays skipped.

See [the readiness runbook](../../docs/demo-readiness.md) for safe upserts, ingestion and browser steps. Seed fixtures only through the idempotent seed command; never reset the application database.
