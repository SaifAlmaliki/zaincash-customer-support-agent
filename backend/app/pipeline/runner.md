# Pipeline stage map

This map lives in the root [README](../../../README.md), in **Where each step lives**. Update that section when a stage, node, or tool moves.

The executed graph is `prepare → jev_classify/gemini_classify → extract → lookup → decide → draft` (classification path depends on mode). Escalation reasons survive drafting; producing a helpful draft does not clear fraud or other flags. Human approval is a separate persisted API action, never an automatic send.

Stage 6 uses `stage6_draft/agent.py`, `model.py`, `context.py`, `tools.py`, `investigation.py`, `guardrails.py`, `credentials.py` and `prompts/draft_v1.md`. The eight tools live in **one `tools.py` file**, not separate tool modules. `drafting.py` retains the drafter interface and explicit skipped/unavailable behavior.

Source ingestion runs outside the ticket graph through `app/kb/{documents,parse,embeddings,service}.py`, `app/services/{knowledge_runtime,knowledge_ingest}.py`, the knowledge API and `support ingest-kb`. Database-backed configured runs use the real RAG drafter. `--no-db` or `RAG_ENABLED=false` skips drafting explicitly.

Trace `kind=tool` counts executed tools; model, stage, guardrail and aggregate draft events are separate. Do not add an aggregate draft cost to its component costs. Historical citation snapshots are persisted with results and survive current-source reindex/deletion.

See [demo readiness](../../../docs/demo-readiness.md) and [live verification](../../../docs/verification/2026-10-17-rag-drafting.md); Task 8 review remains pending.
