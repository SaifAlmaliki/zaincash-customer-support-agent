# Maintainability and stale-code refactor — design specification

- **Date:** 2026-11-02
- **Status:** Written specification approved by the user on 2026-11-02; implementation plans awaiting user review
- **Repository state at audit:** `cae9244` on `main`
- **Scope:** Backend, employee frontend, customer frontend, current documentation, and safe generated-artifact cleanup

## 1. Outcome and success criteria

Perform a targeted maintainability pass across the repository. Remove reference-verified dead code, correct confirmed defects, and extract modules only where a clear responsibility boundary already exists. Preserve the current product, visual design, public compatibility contracts, and historical records.

The user selected a **targeted full pass** and a **cleanup-first sweep**. Safe generated-artifact cleanup is included; old Archify provenance working sets and historical records are excluded from deletion.

Success means:

1. Confirmed dead code and approved stale artifacts are removed without breaking consumers.
2. Selected modules have clearer ownership and can be tested independently.
3. Existing failures and selected confirmed defects are fixed with focused regression coverage.
4. Current behavior is preserved except for the explicit defect fixes in this specification.
5. Backend and frontend tests, lint, standalone type-checks, and production builds pass.
6. Current setup and processing documentation agrees with the Jev-only implementation.
7. Historical specifications, verification records, dated Graphify snapshots, Archify provenance, demo data, and the user's existing root `README.md` modification remain intact.

## 2. Audit baseline

The audit used current source rather than relying solely on Graphify because the existing graph was built at `1c5ccce3`, two commits behind the audited HEAD.

Initial verification produced:

| Area | Baseline |
| --- | --- |
| Backend lint | Ruff passed |
| Backend tests | 758 passed, 3 failed |
| Employee frontend tests | 62 passed |
| Employee frontend lint | Passed |
| Employee frontend build | Failed with 2 TypeScript errors in `ticket-flow-view.test.tsx` |
| Customer frontend tests | 40 passed |
| Customer frontend lint | Passed |
| Customer frontend standalone typecheck | Exited successfully, but the web script checked no files |
| Customer frontend build | Passed |

The three backend failures share one root cause: `backend/tests/fixtures/sample_tickets.jsonl` contains pretty-printed, multiline records and an extra closing brace instead of one complete JSON object per line. The parser's JSONL contract is correct and must not be broadened.

The employee build failure comes from two `ExtractedField` fixtures missing `start`, `end`, `method`, and `confidence`. Vitest transpiles without type checking, and plain `tsc --noEmit` does not build the referenced projects, allowing tests and the standalone typecheck script to remain false-green.

The root `README.md` had a pre-existing user modification. It is not part of this refactor and must not be overwritten.

## 3. Selected approach and sequence

Use a cleanup-first sweep with the recorded baseline as the comparison point:

1. Remove confirmed dead code and safe stale artifacts.
2. Perform mechanical, behavior-preserving modularization.
3. Fix baseline failures and selected confirmed defects with regression tests.
4. Repair current documentation and regenerate current Graphify outputs.
5. Run focused checks for each slice, full subsystem checks after each subsystem, and the complete verification matrix at the end.

Until baseline repair, intermediate verification may show only the three documented backend failures and two documented employee TypeScript errors. Any additional failure is a regression and must be resolved before continuing.

Alternatives considered:

- **Verification-first slices:** Lowest regression-attribution risk, but not selected by the user.
- **Subsystem restructuring:** Cohesive by domain, but produces larger diffs and mixes necessary fixes with optional churn.

No git commits or other git mutations are part of this design.

## 4. Boundaries and non-goals

This pass does not:

- Rewrite the pipeline, intake architecture, API, or frontend applications.
- Change visual styling or user flows.
- Reformat unrelated files or make stylistic changes without a maintainability purpose.
- Split cohesive functions merely because of line count; `RagDrafter.draft`, `build_tools`, and `AgentChat` internals remain intact unless required by an approved change.
- Remove public compatibility fields such as `fallback_rate`, `classifier_paths`, or `ClassifierOutput.degraded`.
- Broaden JSONL parsing, weaken TypeScript contracts, or add type-suppression comments.
- Add a runtime schema-validation library to the customer frontend.
- Perform broad localization consolidation or extract `ReviewEditor` in this pass.
- Optimize every database N+1 pattern; only the result-list work specified below is included.
- Delete historical material merely because it mentions retired cascade behavior.
- Delete generated UI primitive exports solely because they currently lack local consumers.

## 5. Backend design

### 5.1 Dead-code cleanup

Remove the following after repeating reference searches against current source:

- Unused settings `gemini_strong_model`, `gemini_embed_model`, `price_gemini_pro_in`, and `price_gemini_pro_out`, including the validator reference to the removed strong-model setting.
- `Taxonomy.render()` and its test-only assertion; correct the stale `Category.describe()` docstring.
- `current_session_view()` and its exclusive `session_view` import.
- The unused dynamic `IntakeService.submission` assignment and import in `intake_runtime.py`; retain the real `app.state.submission` path.
- The unused `ModelBudget.timeout_s` instance attribute while retaining the constructor argument used for the deadline.

Keep `classifier_disagreement` available for historical result display, but separate legacy reason text from the explicit reasons current drafting tools may introduce. Add a drafting-tool test proving the retired reason is rejected.

### 5.2 Extraction ownership

Move extraction-owned code out of Stage 2:

- Move `GeminiExtractor` and its extraction prompt into `stage3_extract`.
- Move `FieldExtractor` beside its extraction consumer.
- Update `PROMPT_VERSION` imports so extraction metadata has a clear owner.
- Update composition-root and test imports without changing extraction behavior.

Retain Jev as the only classifier. Do not recreate a Gemini classification path.

### 5.3 Knowledge-service boundary

Extract `_DatabaseCall` and its small database concurrency/commit-handoff helpers from `kb/service.py` into an internal KB database module. Keep indexing, publication, retrieval, and cancellation orchestration unchanged initially.

The existing deadline, commit, cancellation, and concurrent-index interleaving tests are mandatory. This is a mechanical separation, not a redesign of KB transaction behavior.

### 5.4 Shared backend boundaries

- Move genuinely shared digit/card normalization, datetime parsing, and Baghdad-timezone primitives to neutral modules. Leave pipeline-specific normalization and lookup behavior in their stages.
- Replace upward FastAPI/API-schema dependencies in the review application service with a small set of domain exceptions. Map those exceptions in the API layer to the existing 404, 409, and 422 responses with unchanged messages and concurrency behavior.
- Consolidate duplicated attachment row-to-contract mapping in one projection helper and use it from both current locations.
- Use one shared initialization function for API and CLI startup that includes both `init_db()` and `upgrade_workspace_schema()`. Add an integration test starting with the old 16-character `runs.status` column and verify both entry points expand it to 32 while preserving rows. Do not introduce a migration framework.

### 5.5 Confirmed backend defect fixes

1. **JSONL fixture:** Restore all five current fixture records as one complete JSON object per nonblank line, preserving their values. Do not change `load_jsonl()`.
2. **Jev paid-call retry:** Disable whole-node retry for `jev_classify` so a failed order-check cannot repeat a successful sibling request. Preserve the existing per-ticket failure outcome. Add a regression fake in which the main request succeeds and the order-check fails once; assert each request is attempted once and the ticket follows the existing failure path.
3. **Draft fallback pricing:** Select fallback token prices for the actual configured drafting model. Provider-reported cost continues to take precedence. Do not apply Gemini prices to Anthropic usage.
4. **Result-list database work:** Apply SQL offset/limit pagination with a separate count query. Skip intake projection when `detail=False`. Add pagination/filter/run-ID coverage and a statement-count test proving list responses do not query intake submissions.
5. **Attachment removal replay:** When a completed removal operation is replayed, finish the idempotent physical unlink before returning. Do not advance the session revision. Test a first unlink failure followed by a successful replay.
6. **Knowledge-search diagnostics:** Catch expected retrieval/provider/timeout failures explicitly and preserve safe public 503 responses. Log only safe diagnostic type names for unexpected faults; do not expose exception text or secrets to clients.

## 6. Employee frontend design

### 6.1 Verification and cleanup

- Add `start: null`, `end: null`, `method: "test"`, and `confidence: 1` to both incomplete `ExtractedField` test fixtures. Do not weaken the shared type.
- Change standalone typecheck to build referenced projects with `tsc -b`.
- Remove confirmed-unused `agentTools`, `skeleton.tsx`, `separator.tsx`, and `useTheme`; retain `ThemeProvider`.
- Remove the unused `mermaid` direct dependency and regenerate the lockfile through npm.

### 6.2 Retire the legacy trace/chart cluster

Before deletion, add active `TicketFlow` coverage for retained citations, valid tool events, malformed entries, and secret/raw-error exclusion. Then remove:

- `PipelineTrace.tsx` and `trace-facts.ts`.
- Test-only `mermaidText`, `pipelineChart`, and `detailChart` functions and their obsolete assertions.
- Imports and tests that exist only for this legacy cluster.

Keep `reviewEvidence`, which remains actively shared. Migrate useful behavior coverage rather than deleting it with the legacy implementation.

### 6.3 Runs and request loading

- Move `RunDetailPage` into its own module and update the lazy route import.
- Extract run-result loading into a focused module.
- Replace unrestricted `Promise.all` detail fetching with bounded concurrency while preserving abort signals and complete detail fidelity.
- Test that every item loads once, the in-flight limit is respected, aborts propagate, rejected requests follow the existing error path, and empty results complete correctly.
- Preserve the existing polling behavior for running runs and cleanup for terminal runs.

### 6.4 Focused view extraction

- Extract a pure queue projection for counts, filtering, sorting, and pagination. Test approved/edited grouping, combined filters, search, priority ordering, and page clamping.
- Extract presentational `DocumentList` and `KnowledgeReadiness` components while keeping mutations in `KnowledgePage`.
- Reuse existing index-lifecycle logic and tests unchanged; add focused rendering tests for document action states and readiness configuration.

Do not change the current visual design or extract `ReviewEditor` in this pass.

## 7. Customer frontend design

### 7.1 Verification and cleanup

- Change web standalone typecheck to `tsc -b` so referenced projects are checked.
- Include `vitest.config.ts` in the node TypeScript project.
- Add a root `test` script and Turbo test task that run the existing web tests.
- Remove the unreachable retry branch, unused `useTheme`, and redundant default `AgentChat` export.
- Remove unused Hugeicons dependencies from web and UI, direct UI `zod`, UI `@tailwindcss/vite`, and UI `@turbo/gen`; regenerate the lockfile through npm.
- Retain reusable `AgentChat` capabilities and shadcn configuration aliases unless a listed defect fix requires a small change.

### 7.2 Runtime contracts and persisted operations

Extract API/storage guards into a focused intake contract module without adding a dependency:

- Validate all required `SessionView` fields, nested message/readiness/review fields, evidence entries, and credential string types.
- Make `Fact.value` and `Fact.evidence` required, matching the parser's existing runtime requirements.
- Reuse runtime guards for persisted browser sessions instead of casting arbitrary JSON.
- Make `PendingOperation` a discriminated union tying each operation kind to its command payload.
- Use `payload.request_id` as the single request-identity source and remove unchecked kind/payload casts.

Add table-driven malformed nested-response, credential, corrupted-storage, mismatched-payload, request-ID, and valid-replay tests.

### 7.3 Upload lifecycle

Extract preview and upload sequencing from `IntakePage` into `useIntakeUploads`:

- Give every selected file a stable client ID and use it for preview and progress identity.
- Preserve sequential uploads and stop-on-first-failure behavior.
- On failure, remove previews for later files that were never attempted.
- Preserve object-URL cleanup and existing accessible UI behavior.

Test duplicate filenames, independent progress, first-of-two failure, removal of unattempted previews, and object-URL revocation.

### 7.4 Controller, chat, and tests

- Preserve `resumeUnavailable` and its error code when `startNew` resets state after a storage-clear failure.
- Disable the streaming Stop button when no `onStop` handler is supplied; do not change current ready-state intake behavior.
- Centralize `vi.unstubAllGlobals()` and fake-timer restoration in `afterEach` hooks.
- Move duplicated intake test fixtures into a shared test fixture module.

## 8. Repository hygiene and current documentation

### 8.1 Approved deletions

- Tracked contents of `graphify-out/cache/`; add `graphify-out/cache/` to `.gitignore` so regenerated cache files remain untracked.
- `docs/architecture.html`, which is unreferenced and superseded by the current Jev-only `docs/pipeline-architecture.html`.
- The six confirmed stale Superpowers brainstorm server-state files, after rechecking that no replacement server is active:
  - `.superpowers/brainstorm/59043-1792924854/state/server.pid`
  - `.superpowers/brainstorm/59043-1792924854/state/server-info`
  - `.superpowers/brainstorm/59043-1792924854/state/server-instance-id`
  - `.superpowers/brainstorm/59043-1792924854/state/server.log`
  - `.superpowers/brainstorm/.last-port`
  - `.superpowers/brainstorm/.last-token`
- Local ignored duplicate `out/architecture-desktop-v3.png`; retain `out/architecture-verified-desktop.png`.

Do not delete `.superpowers/brainstorm/.../content/`, Archify working sets, dated Graphify snapshots, Playwright verification evidence, or current generated architecture receipts.

### 8.2 Docker and documentation

Add Docker build-context exclusions for virtual environments, dependencies, build outputs, and local tool/output directories: `**/.venv/`, `**/node_modules/`, `**/dist/`, `out/`, `.superpowers/`, `.playwright-mcp/`, `.archify/`, and `.cursor/`. This changes context hygiene only; do not delete local installed dependencies.

Update current guides to:

- Replace nonexistent `customer-support-ui` paths with `employee-frontend`.
- Replace the cascade selection in `data/test-kb/README.md` with Jev-only processing.
- Describe Compose as starting both PostgreSQL and the API.
- Remove the employee frontend's stale hard-coded 25-test statement and point readers to the verification commands instead of a count that will become outdated.

Preserve historical cascade references in specifications and verification records. Do not alter the user's pre-existing root `README.md` modification.

### 8.3 Graphify outputs

Regenerate current `graphify-out/graph.json`, `graph.html`, `GRAPH_REPORT.md`, and manifest after source changes so they no longer describe deleted cascade files. Keep dated snapshots unchanged and keep regenerated cache contents ignored.

## 9. Error handling and compatibility

- Existing HTTP status codes, public messages, optimistic-concurrency protections, idempotency keys, revision rules, and safe secret-free responses remain unchanged unless a defect fix explicitly requires otherwise.
- Model and tool execution limits remain in place. The Jev retry change prevents duplicate paid sibling calls rather than adding another retry layer.
- Database changes are limited to query/initialization behavior; no new schema or migration framework is introduced.
- Frontend runtime validation rejects malformed server or persisted data through the existing error paths rather than allowing invalid typed state to propagate.
- Upload failure behavior remains sequential and stop-on-first-failure; only stale preview handling and identity are corrected.
- Dependency removal must be followed by lockfile regeneration and complete builds to catch transitive or tooling assumptions.

## 10. Verification and acceptance

Run focused regression tests before and after each defect fix, then run the relevant full subsystem checks.

### Backend

```bash
cd backend
uv run pytest -q
uv run ruff check app tests
```

The repaired baseline is expected to contain 761 previously passing tests plus any new regression tests. Required focus areas include Jev retries, draft pricing, extraction/factory wiring, KB interleavings, result pagination, attachment replay, API/CLI schema initialization, review HTTP behavior, and knowledge-search diagnostics.

### Employee frontend

```bash
cd employee-frontend
npm run typecheck
npm test
npm run lint
npm run build
```

All existing tests must pass together with the new active TicketFlow, loader, queue, and knowledge-view tests.

### Customer frontend

```bash
cd users-frontend
npm test
npm run typecheck
npm run lint
npm run build
npm --workspace web test
```

The root and workspace test commands must execute the same web suite. Typechecking must include application, tests, and Vite/Vitest configuration.

### Repository and Docker

```bash
docker compose config --quiet
docker compose build api
```

Run the API image build when the local Docker environment is available; report any environmental limitation rather than claiming it passed. Confirm current documentation has no stale `customer-support-ui` or current-cascade instructions, Graphify metadata matches the new source state, and `graphify-out/cache/` is ignored.

Finish with a complete diff and status review. Only intended source, test, configuration, documentation, lockfile, and current generated-output changes are acceptable. No secret values or unrelated user changes may be included.
