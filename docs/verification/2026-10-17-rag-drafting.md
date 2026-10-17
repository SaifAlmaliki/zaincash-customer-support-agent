# RAG drafting verification — 2026-10-17

**Outcome:** real synthetic indexing, retrieval, supported drafting and persisted browser review demonstrated. Task 8/controller review is pending. One live credential-negation bug was fixed with focused RED→GREEN tests; one real provider-latency timeout is retained beside its successful retry.

## Environment and isolation

- Branch `feat/plan3-rag-drafting`, WSL Ubuntu-24.04, root `/home/cvzmh_saif/dev/zaincash-support`.
- Credentials consumed only through existing `Settings`/environment. No `.env` secret values read or printed; no model/key changed. `SSL_CERT_FILE=/etc/ssl/certs/ca-certificates.crt` set in every task-owned API/CLI process.
- Selected chat `google/gemini-3.8-flash`; embeddings `openai/text-embedding-3-small`, 768 dimensions, cutoff 0.3, top-k 5. Jev `jev-1.13.0` classification/checking; all seven ticket attempts took the Jev classification path, so cascade fallback was not exercised.
- Preflight asserted parsed and connected database names `support` / `support_test`; application DB had three synthetic transactions and no running jobs. No support reset, reseed or transaction mutation was needed. Ticket creation used known fixture IDs/upserts.
- Task-owned API port 8018 and Vite port 5188 were free before launch. Vite's task-local inline proxy pointed `/api` at 8018. Existing servers, including 8765 and both database ports, were preserved.
- Prior page/context routes were explicitly removed before live requests. Later checks used an isolated browser context with no route interception. No fake HTTP responses were used in Task 8. A passive HTTPX observer recorded only provider path/status/ID/model/usage/latency, returning responses unchanged and never logging headers or keys.

## Commands and automated verification

Commands below are WSL commands. From Windows the prefix was `wsl.exe -d Ubuntu-24.04 --cd <directory>`. `uv` executable: `/home/cvzmh_saif/.local/bin/uv`.

```bash
# Root, before source exploration
/home/cvzmh_saif/.local/share/uv/tools/graphifyy/bin/graphify query \
  'taxonomy synthetic transactions knowledge indexing RagDrafter API ticket approval demo readiness' --budget 1800

# Backend: focused reproduction and verification
uv run pytest -q tests/test_draft_guardrails.py -k 'live_draft_avoid or avoid_sharing_warning'
uv run pytest -q tests/test_draft_guardrails.py
uv run pytest -q tests/test_draft_guardrails.py -k avoid_sharing_warning
uv run pytest -q tests/test_draft_guardrails.py

# Backend: final suite / lint (support_test asserted before execution)
uv run pytest -q
uv run ruff check app tests

# customer-support-ui: final checks
npm test
npm run lint
npm run build
```

Focused results: first RED **3 failed / 3 passed** (literal live wording plus scoped warning cases), then **130 passed**. The unchanged-model retry exposed the adverb variant “تجنب تماماً”; second RED **1 failed / 7 passed**, then **132 passed**. Eight regression cases were added overall; later disclosure requests and “لا تتجنب…” remain unsafe. The production change only extends the existing locally scoped negation expression in `stage6_draft/guardrails.py`.

| Final command | Observed result |
|---|---|
| `uv run pytest -q` | **665 passed**, zero skipped/failed, 62.75s. Task-local `task8-tests.py` asserted parsed and connected `support_test` first, pinned that URL for the child process, and saved `task8-pytest.log`. |
| `uv run ruff check app tests` | Passed, no diagnostics. |
| `npm test` | **21 passed / 4 files**, 496ms. |
| `npm run lint` | Passed, no diagnostics. |
| `npm run build` | Passed: TypeScript + Vite 8.3.3, 2,229 modules, 720ms Vite build. |

These commands ran after the final application/test changes and documentation draft. Automated provider tests use controlled fakes, not paid model responses.

## Corpus and actual retrieval

Twelve `data/kb/*.md` files match the taxonomy exactly; parser validation produced one chunk each. API upload returned 200/admission, polling confirmed **all 12 indexed** with the selected model and 768 dimensions. Retained IDs: **4–15**, in this order: account_kyc, agent_dispute, app_bug, bill_payment, card_issue, failed_transfer, fraud_report, general_inquiry, login_access, other, refund_request, wrong_recipient. Corpus index cost: **$0.00010758**.

Each document says it is fictional and carries safe escalation/credential guidance; none asserts real fees, limits, compensation or account access. Database tags were left empty; the category line is descriptive metadata, not an implicit tag parser.

| Actual Arabic query | Passages | First relevant source | Similarity | Query cost USD |
|---|---:|---|---:|---:|
| حولت فلوس وانقطعت من رصيدي بس ما وصلت للمستلم والتحويل معلق شنو أسوي؟ | 2 | `failed_transfer.md` / doc 9 | 0.377686 | 0.00000102 |
| شلون أشرح مشكلتي للدعم بأمان وشنو المعلومات غير السرية اللي أذكرها؟ | 5 | `general_inquiry.md` / doc 11 | 0.402949 | 0.00000102 |
| واحد اتصل وطلب الرمز وبعدها انسحبت فلوسي شلون أتصرف؟ | 3 | `fraud_report.md` / doc 10 | 0.347926 | 0.00000086 |
| اشرح التشابك الكمي بين فوتونين داخل مختبر فيزياء | 0 | None | — | 0.00000068 |

These are nominal spot checks, not a relevance benchmark. Wrong-recipient content was a close second for the fraud query. The agent reformulates queries: its general-inquiry search ranked KYC first, then the general policy; it correctly cited the latter. For the unsupported ticket it searched for out-of-scope guidance, cited `other.md` and declined to answer physics, rather than returning a scientific answer.

## Real ticket outcomes

| Run / result | Fixture | Outcome before human review | Tools | Draft ms | Words / Arabic ratio | Jev credential score | Ticket cost USD |
|---|---|---|---:|---:|---|---:|---:|
| 39 / 55 | Browser general | Rejected: false `requests_credentials` on “تجنب مشاركة” | 2 | 9519.309 | 43 / 0.9684 | 0.04 | 0.006797 |
| 40 / 56 | Same browser fixture | Rejected: “تجنب تماماً مشاركة” variant; later edited/approved manually | 3 | 14163.905 | 63 / 0.9788 | 0.04 | 0.009767 |
| 41 / 57 | General inquiry | Submitted, no findings/reasons; later edited/approved | 2 | 10041.741 | 54 / 0.9748 | 0.04 | 0.007856 |
| 41 / 59 | Fraud | Submitted, no findings; **P1 + fraud_suspected preserved** | 3 | 13408.257 | 47 / 0.9330 | 0.03 | 0.013238 |
| 41 / 58 | Unsupported physics | Cited refusal; **no_kb_support**, escalated; no science answer | 3 | 12948.115 | 46 / 1.0000 | 0.03 | 0.012439 |
| 41 / 60 | Failed-transfer category | **draft_timeout**, no draft; matched `ZC2410000123` preserved | 1 | 30004.492 | — | Not run | 0.003239 |
| 42 / 61 | Same transfer, unchanged settings | Submitted, no findings/reasons; P2, pending review | 2 | 14300.071 | 56 / 0.9203 | 0.03 | 0.012694 |

Run 41: four results, no failed IDs, three escalated and one initially pending review; **$0.036772**, p50 13,778ms / p95 30,784ms. Run 42: one pending-review result, **$0.012694**, ticket latency 14,752ms. All submitted post-fix drafts met the six-tool / 120-word / Arabic-ratio constraints, cited a saved source and had non-degraded credential checks below 0.2. The timeout did not reach the checker; null is not a successful credential check.

Transfer result 61 accurately says the synthetic operation is **pending**, names only the matched 50,000 IQD / `07701234567` / `ZC2410000123`, advises against repeating the transfer, and routes review to Payments Ops. It gives no arrival/refund deadline or reimbursement guarantee. Fraud result 59 advises ending contact with the caller, sharing no further codes and using official channels; it claims no freeze/refund. Classification does not require a transaction match for fraud, so that result correctly has no matched reference despite the fixture's known synthetic sender.

### Citation IDs and provider evidence

| Result | Cited passage ID | Source |
|---|---|---|
| 55, 56 | `aa1a7fbbc54f9f5b9bb5fcbdb8b5da4b49c038f1063e98020e889950f0a3439d` | Temporary doc 2, later deleted |
| 57 | `c427dcaa00340dbd2e5fab8b3120b63bbd73f3b041b2c2e0e56c6b94f0b4f28e` | general_inquiry / 11 |
| 59 | `ba87f33e14f7c195f2d5757f93c2543986772de69e5b83edec294dd816e850cd` | fraud_report / 10 |
| 58 | `a82e6706b88dc7956fcb4f4659d888b2fcdfe7d233de70b0a8066ddd5cce6f9f` | other / 13 |
| 61 | `faa1f3293bf5e5942b59917a4ca8aa0a9cd19e4be8ce3262e3d0c135f92c3c5c` | failed_transfer / 9 |

All cited IDs existed in that result's retained `citation_sources`. Actual supported general model response IDs: `gen-1792261947-uTCjzGCwGpa34LkA6J0W`, `gen-1792261950-5cXcv3amqBjH07JS6pXa`; transfer: `gen-1792262019-qDoOsBo6PUj3hqWcWkIK`, `gen-1792262022-HJA21FSQJBeGa7aZLaBX`. First live embedding: `gen-emb-1792260684-oy03mh2P8LKEisddXpkz`, HTTP 200, 393 tokens, $0.00000786.

Passive accounting observed **16 chat HTTP 200 responses ($0.06440550)** and **29 embedding HTTP 200 responses ($0.00013488)**: **$0.06454038 OpenRouter reported cost**. These include the initial failures, temporary-source reindex, API searches and browser searches. Pipeline ticket totals across the seven attempts sum to **$0.066030**, including Jev estimates. Do not add these two totals together: they overlap. No provider response/usage was received for the cancelled in-flight transfer call; any subsequent provider-side charge is unknown, so this is not a reconciled billing total.

Result 61 draft cost components: model $0.01244775 + search $0.00000074 + Jev checker estimate $0.000024486 = **$0.012472976**. Result 57: $0.00762750 + $0.00000056 + $0.00002289 = **$0.00765095**. Trace aggregate draft cost is not counted again.

## Live browser and persistence evidence

1. Initial real health: `knowledge.status=empty`, count 0; UI showed **Your document library is empty**. No existing sources were deleted to create this state.
2. Browser uploaded own `task8-history-policy.md` as doc **2**, accepted then indexed; real Arabic search returned it at 0.417. Browser uploaded known synthetic ticket `RAG-DEMO-BROWSER-HISTORY`, creating runs **39/40**.
3. Result **56** displayed a retained source, original draft, actual three-tool trace and the genuine guardrail false-positive evidence. Browser edit/approve returned HTTP 200, review **2**, action `edit_approve`, reviewer `Task8 synthetic reviewer`. Reload retained distinct original/final texts.
4. Browser reindexed own doc 2: HTTP **202** carried the old indexed state; later `indexed_at` changed from `18:11:24.062561Z` to `18:28:11.685779Z`, cumulative source cost $0.00001572. Browser then deleted it (**204**). Its live chunks returned **404**. Reloaded result 56 still displayed the saved passage; API before/after assertions confirmed identical citation snapshots, tool trace, original/final texts and review history.
5. Controlled malformed PDF: no-header version rejected at upload (**422**). A `%PDF-1.7` header with intentionally invalid body was stored as own doc **3**, then genuinely failed parsing/indexing with a readable error and zero embedding cost. UI **Retry index** returned **202** and failed again. Only doc 3 was deleted after this check. This is a real parser-fault UI check, **not an external-provider outage**.
6. Useful corpus IDs 4–15 retained. Browser duplicate-uploaded `general_inquiry.md`, observed already-indexed/no-new-request, inspected its one passage, searched supported Arabic and unsupported physics through the real API.
7. Clean post-fix result **57** showed one relevant citation, no findings, Jev score 0.040 and two tools. Browser edited/approved (HTTP **200**, review **3**, `edit_approve`) and reloaded: original unchanged, final text persisted. Final reload made only GET health/result requests; no source lookup was needed to render citations.
8. Final isolated-page reload: **zero console errors/warnings**. 390×844 review viewport: **no horizontal overflow**. No UI application source was changed by Task 8.

Task 7's earlier saturation, network-error, stalled-polling, degraded-checker and preview isolation tests used **controlled fake API responses**. They remain separate automated/browser fault evidence, not live provider claims. Task 8 did not induce a provider outage or change credentials/models to manufacture one. Browser harness errors (stale selectors, nonexistent clock-uninstall helper, relative screenshot path and shared-tab navigation) were corrected using observed labels, absolute artifact paths and a dedicated context; they were not backend defects.

## Artifacts, servers and remaining concerns

Local task workspace: `.superpowers/sdd/2026-10-17-plan3-rag-drafting/`. `task8-smoke.py` operations were `preflight`, `start`, `health`, `capture 39 before`, `capture 40 before`, `capture 40 after`, `ingest`, `search`, `batch`, `capture 41 before`, `batch transfer`, `audit`, `stop`, launched from backend with `env SSL_CERT_FILE=/etc/ssl/certs/ca-certificates.crt PYTHONPATH=. uv run python ../.superpowers/sdd/2026-10-17-plan3-rag-drafting/task8-smoke.py <operation>`.

Raw local evidence: `task8-provider.jsonl`, `task8-corpus-index.json`, `task8-search.json`, `task8-run-39-before.json`, `task8-run-40-{before,after}.json`, `task8-run-41-before.json`, `task8-run-42.json`, `task8-audit.json`, API/Vite logs and `task8-servers.json`. The task-local provider observer is instrumentation only, not production code.

Screenshots under `.playwright-mcp/`: `task8-live-empty.png`, `task8-live-failed-index.png`, `task8-live-retained-evidence.png`, `task8-live-corpus-search.png`, `task8-live-approved.png`, `task8-live-mobile.png`.

API/Vite PID pairs: **509081/509082**, **519886/519887**, **534223/534224**. Restarts loaded each focused fix only after jobs finished. A port probe initially saw TIME_WAIT after shutdown; `ss` confirmed no listener and the task-only probe was adjusted for address reuse. No user process was stopped.

All task-owned servers were stopped at handoff; `ss -ltnp` confirmed **8018 and 5188 free**, and the existing 8765 process plus database listeners remained. The task's isolated browser context was closed.

Final graph refresh command (root): `/home/cvzmh_saif/.local/share/uv/tools/graphifyy/bin/python .superpowers/sdd/2026-10-17-plan3-rag-drafting/task8-graph.py`. It uses the installed graphify scoped AST/Markdown update, backs up existing graph artifacts, preserves unrelated source nodes and records counts in `task8-graph-summary.json`. It does not call an external semantic model. The intended source/doc diff was self-reviewed and `git diff --check` was clean; controller review remains separate.

Remaining: controller review of Task 8 and its narrow guardrail change; variable provider latency; broader Arabic retrieval/negation evaluation; the deferred CLI invalid-`EMBED_DIM` diagnostic. [Plan 2 evaluation, packaging/CI, disclosure/data card/broader failure evidence and the weekly-report stretch work](../demo-readiness.md#known-limitations-and-remaining-work) remain open. No commits, staging or pushes were made by this task.
