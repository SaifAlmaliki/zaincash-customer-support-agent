# Fictional RAG walkthrough inputs

The policy reference is [`data/kb-pdf`](../kb-pdf): twelve fictional PDFs, one per category in `data/taxonomy.yaml`. Index that folder before running these tickets. Category text inside a PDF is descriptive; ingestion does not infer database category tags from it. Untagged documents stay eligible for category-filtered retrieval.

Everything in `../kb-pdf/` and `rag_tickets.jsonl` is **synthetic, fictional demo material**. It is not a statement of real ZainCash policy, fees, limits, reimbursement guarantees, response deadlines or account access. The assistant cannot move funds, freeze accounts or send replies.

| Fixture | Intended observation (verify actual output) |
|---|---|
| `RAG-DEMO-FAILED-TRANSFER` | Existing synthetic `ZC2410000123`, 50,000 IQD, **pending**, sent on 2026-10-06; relevant pending-transfer citation, no completion/refund promise. |
| `RAG-DEMO-GENERAL` | Safe, non-secret support information; Arabic draft grounded in `general_inquiry.pdf`. |
| `RAG-DEMO-FRAUD` | Existing synthetic sender `07501112233` / `ZC2410000789`, 200,000 IQD; preserve `fraud_suspected` and P1 regardless of whether a draft is produced. |
| `RAG-DEMO-UNSUPPORTED` | Quantum-entanglement question outside this corpus; no invented scientific answer. Record actual rejection/escalation and any irrelevant retrieval. |
| `RAG-DEMO-WRONG-RECIPIENT` | Money sent to the wrong number on purpose by mistake; the customer wants it back. |
| `RAG-DEMO-LOGIN` | Forgotten PIN and a verification code that never arrives. No stolen money. |
| `RAG-DEMO-AGENT` | Cash given to an agent for a top-up that never landed in the wallet. |
| `RAG-DEMO-CARD` | Mastercard declined at merchants, with no wallet debit. |
| `RAG-DEMO-BILL` | Asia mobile top-up marked successful, credit not applied. |
| `RAG-DEMO-KYC` | Identity document rejected while raising the account level. |
| `RAG-DEMO-REFUND` | Cancelled merchant purchase; the customer wants the money back. |
| `RAG-DEMO-APP-BUG` | App closes on open after an update. Balance unchanged. |
| `RAG-DEMO-OTHER` | Vague service complaint with no specific request. |

Dates are fixed so “امس” in the transfer fixture resolves to the existing transaction. The original five Plan 1 smoke inputs remain under `backend/tests/fixtures/`. These inputs are deliberately visible development/demo examples, **not held-out evaluation data** and not an accuracy benchmark. The first four IDs and their text stay fixed so a re-upload matches the seeded rows. The later rows cover the remaining taxonomy categories and do not have their own seeded transactions.

See [the readiness runbook](../../docs/demo-readiness.md) for safe upserts, ingestion and browser steps. Seed fixtures only through the idempotent seed command; never reset the application database.
