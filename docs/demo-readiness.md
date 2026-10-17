# Synthetic demo readiness

As of **2026-10-17**: Plan 1 and the workspace are implemented; Plan 3 RAG has real provider/API/browser smoke evidence. **Task 8 and its live-discovered guardrail fix await controller review.** This is a local synthetic demo, not a production-readiness or accuracy claim.

## Evidence by layer

| Layer | Observed status |
|---|---|
| Corpus | 12 fictional Markdown policies, one per taxonomy category; 12 live indexed documents / 12 passages retained. |
| Arabic judge pack | [13 localized sources](../data/test-kb/README.md), including recovered temporary doc2, plus a [single-upload bundle](../data/test-kb/judge-demo.ar.md). New copies: offline parser/integrity validated only; earlier live evidence below refers to the original bytes. |
| Automated | **665 backend tests**, Ruff, **21 frontend tests**, lint and build passed. Exact commands are in the [verification record](verification/2026-10-17-rag-drafting.md). Providers are controlled fakes in automated tests; PostgreSQL integration uses only `support_test`. |
| Real retrieval | OpenRouter `openai/text-embedding-3-small`, 768 dimensions. Intended policy ranked first for three supported Arabic queries; physics query returned zero passages. |
| Real drafting | `google/gemini-3.8-flash`; supported general/transfer drafts passed checks, fraud stayed P1/escalated, unsupported topic received a refusal and `no_kb_support`. |
| Browser/API | Upload/index/search, passage inspection, ticket submission, citations/tool trace, edit/approve/reload, temporary-source reindex/delete history, empty knowledge and failed indexing exercised. |
| Reliability | One transfer attempt timed out at the 30-second drafting budget; unchanged-settings retry succeeded. Preserve failed run 41/result 60 alongside successful run 42/result 61. |
| Guardrails | Live warnings using “تجنب مشاركة” and “تجنب تماماً مشاركة” exposed false positives; focused tests reproduced both and the local negation fix passed. Original failure evidence remains immutable. |

All `data/kb/` material is **fictional demo guidance**, not real ZainCash policy, fees, limits, reimbursement promises, response deadlines or account access. All ticket/transaction examples are synthetic. Nothing moves funds, changes an account or sends a reply.

## Repeatable local walkthrough

For the judge presentation, use the [Arabic pack walkthrough](../data/test-kb/README.md): upload **either** `data/test-kb/judge-demo.ar.md` **or** the 13 files in `data/test-kb/ar/`. Skip the `ingest-kb ../data/kb` command below when using that pack. Do not ingest all of `data/test-kb/`; its guide, provenance and negative samples are not valid KB inputs. The commands below retain the original 12-policy smoke path for reproducibility; the Arabic pack has its own [provenance manifest](../data/test-kb/provenance.json).

From the repository root in WSL, configure keys using `.env`/environment through backend `Settings`. Do not display key values. Keep the selected model unless intentionally changing it. Check `ss -ltnp` before starting servers; use free ports and preserve existing processes. The commands below use the normal documented ports when free:

```bash
export SSL_CERT_FILE=/etc/ssl/certs/ca-certificates.crt
docker compose up -d --wait db
uv --directory backend sync
# Idempotent fixture upsert; never reset the support database.
uv --directory backend run support seed-db \
  --transactions tests/fixtures/sample_transactions.jsonl \
  --incidents tests/fixtures/sample_incidents.jsonl
uv --directory backend run support ingest-kb ../data/kb
uv --directory backend run uvicorn app.main:app --host 0.0.0.0 --port 8000
```

In another terminal:

```bash
cd customer-support-ui
npm ci
npm run dev -- --port 5173 --strictPort
```

1. Open `http://localhost:5173`, select **Live workspace**, then **Knowledge base**. Confirm each document is actually **Indexed**, not just accepted. Uploads automatically request indexing when configured; duplicates retain the existing source. Index/retry acceptance is HTTP 202 and may still contain an old durable status: poll until a new terminal outcome.
2. Inspect a passage. Search: `حولت فلوس وانقطعت من رصيدي بس ما وصلت للمستلم والتحويل معلق شنو أسوي؟`. Check source relevance, not just similarity. The file's `Category:` line does **not** set database tags; optional API `category_tags` are explicit. Untagged documents remain eligible for category-filtered retrieval.
3. Upload `data/demo/rag_tickets.jsonl` in **New batch**, choose cascade, start processing. Fixed timestamps align “yesterday” with the existing pending transfer. Reuse unchanged IDs/content; the API rejects conflicting content for an existing ID.
4. Inspect the transfer/general/fraud/unsupported results. General and transfer need grounded Arabic replies, valid citations and no invented financial facts/promises. Fraud must remain P1/escalated. The physics question must not receive a scientific answer; a cited out-of-scope refusal is acceptable and still escalated.
5. Expand **Agent tools** and **Draft & check events** separately. Verify no more than six executed tools, at most 120 reply words, Arabic alphabetic ratio at least 0.5, and the credential-check status. Similarity is not confidence; a clean check does not prove correctness.
6. Edit a synthetic reply, enter a reviewer name, **Save & approve**, then reload. Confirm the original draft, final reviewed text and audit entry stay distinct. Approval saves; it never sends.
7. For destructive-source verification, create a uniquely named temporary synthetic source of your own, generate a cited draft, capture its evidence, reindex that source, then delete **only that temporary source**. Reload the old result: its citations and review must remain. Keep the 12 useful demo policies.

CLI batch alternative (paid calls, persisted run):

```bash
uv --directory backend run support run-batch ../data/demo/rag_tickets.jsonl \
  --mode cascade --out ../out/rag-demo.json
```

`support ingest-kb --retry-stored` retries awaiting/failed stored sources; inspect the library first because it is not scoped to one source. The live Task 8 run used the API instead, preserving per-source IDs. Scanned PDFs need OCR before ingestion. Keep only one API worker for the local background runner; avoid restarting while a batch/index job is active.

## Known limitations and remaining work

- Provider latency varies: a run can complete with an escalated `draft_timeout` result. Retry intentionally and keep the original evidence. Recorded costs include observed completed calls; a cancelled remote request may still be billed by the provider.
- Retrieval is sensitive to query wording. The agent's general-inquiry query ranked KYC first, but selected the relevant general-inquiry citation. Broader relevance/quality measurement remains open.
- Credential heuristics and Jev complement human review. The Task 8 fix handles the two observed “avoid sharing” forms, not arbitrary Arabic semantic negation. Guardrails do not certify a later human edit.
- Deferred Task 6 minor: invalid `EMBED_DIM` reaches `get_settings()` before the CLI configuration handler, producing exit 1 without its friendly config diagnostic. It did not block this demo; final review owns it.

| Follow-up | Still required |
|---|---|
| Plan 2 evaluation | 200+ synthetic Iraqi-dialect tickets, dev/test split and protected test hash, evaluator, Jev/Gemini/cascade metrics, confusion analysis and human draft ratings. The four demo tickets and five earlier smoke fixtures are not held-out data. |
| Packaging / CI | Backend/frontend Dockerfiles, full Compose application stack and CI. Current Compose primarily supplies the local database. |
| Disclosure / data card / failure evidence | Formal AI/data disclosures, data card, systematic failure catalogue and evidence beyond these smoke cases. This record contributes observed failure evidence but does not finish those deliverables. |
| Weekly report — stretch | Statistical spike detection, incident correlation and cited bilingual narrative. Existing weekly counts are not this report. |

Task 8 independent review and the narrow production fix are still pending; do not mark the plan fully reviewed from the implementer's self-check alone.
