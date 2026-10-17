# Fictional RAG walkthrough inputs

For the judge demo, use the [Arabic KB pack and walkthrough](../test-kb/README.md): **[one upload file](../test-kb/judge-demo.ar.md)** containing all 13 valid tested sources, or the [13 individual Arabic files](../test-kb/ar/) (choose one format, not both). This includes the recovered temporary source from runs 39/40. [Provenance hashes](../test-kb/provenance.json) distinguish the newly localized, offline-parser-validated copies from the live-tested originals. The tickets below work as demonstration inputs for either corpus format; verify actual retrieval and draft output for the new pack.

Everything in `../kb/` and `rag_tickets.jsonl` is **synthetic, fictional demo material**. It is not a statement of real ZainCash policy, fees, limits, reimbursement guarantees, response deadlines or account access. The assistant cannot move funds, freeze accounts or send replies.

The 12 Markdown files correspond one-to-one with `data/taxonomy.yaml`. Category text in a file is descriptive; upload/CLI ingestion does not infer database category tags from it. Use the index API's `category_tags` when you need filtered retrieval.

| Fixture | Intended observation (verify actual output) |
|---|---|
| `RAG-DEMO-FAILED-TRANSFER` | Existing synthetic `ZC2410000123`, 50,000 IQD, **pending**, sent on 2026-10-06; relevant pending-transfer citation, no completion/refund promise. |
| `RAG-DEMO-GENERAL` | Safe, non-secret support information; Arabic draft grounded in `general_inquiry.md`. |
| `RAG-DEMO-FRAUD` | Existing synthetic sender `07501112233` / `ZC2410000789`, 200,000 IQD; preserve `fraud_suspected` and P1 regardless of whether a draft is produced. |
| `RAG-DEMO-UNSUPPORTED` | Quantum-entanglement question outside this corpus; no invented scientific answer. Record actual rejection/escalation and any irrelevant retrieval. |

Dates are fixed so “امس” in the transfer fixture resolves to the existing transaction. The original five Plan 1 smoke inputs remain under `backend/tests/fixtures/`. These four inputs are deliberately visible development/demo examples, **not held-out evaluation data** and not an accuracy benchmark.

See [the readiness runbook](../../docs/demo-readiness.md) for safe upserts, ingestion and browser steps. Seed fixtures only through the idempotent seed command; never reset the application database.
