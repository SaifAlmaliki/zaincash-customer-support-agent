# Repository Hygiene Maintainability Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Remove only the approved stale repository artifacts, correct current setup documentation and Docker context hygiene, regenerate current Graphify outputs after all source plans finish, and verify the complete maintainability refactor without touching protected history or user work.

**Architecture:** This is the final repository-hygiene slice of the approved maintainability design. It uses reference-, process-, and hash-based safety gates before each deletion; makes small configuration and documentation edits; performs Graphify regeneration as the last mutating task; then runs the full backend, employee frontend, customer frontend, Docker, diff, and secret-safety acceptance matrix.

**Tech Stack:** Git tracked-file and diff inspection, POSIX shell, Markdown, Docker Compose and `.dockerignore`, Graphify CLI, Python/`uv`/Ruff/pytest, Node.js/npm/Turbo/Vitest/TypeScript.

**Spec:** `docs/superpowers/specs/2026-11-02-maintainability-refactor-design.md`

## Global Constraints

- Perform a targeted maintainability pass across the repository. Remove reference-verified dead code, correct confirmed defects, and extract modules only where a clear responsibility boundary already exists. Preserve the current product, visual design, public compatibility contracts, and historical records.
- The user selected a **targeted full pass** and a **cleanup-first sweep**. Safe generated-artifact cleanup is included; old Archify provenance working sets and historical records are excluded from deletion.
- Historical specifications, verification records, dated Graphify snapshots, Archify provenance, demo data, and the user's existing root `README.md` modification remain intact.
- Until baseline repair, intermediate verification may show only the three documented backend failures and two documented employee TypeScript errors. Any additional failure is a regression and must be resolved before continuing.
- No git commits or other git mutations are part of this design.
- The root `README.md` had a pre-existing user modification. It is not part of this refactor and must not be overwritten.
- This pass does not:
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
- Existing HTTP status codes, public messages, optimistic-concurrency protections, idempotency keys, revision rules, and safe secret-free responses remain unchanged unless a defect fix explicitly requires otherwise.
- Model and tool execution limits remain in place. The Jev retry change prevents duplicate paid sibling calls rather than adding another retry layer.
- Database changes are limited to query/initialization behavior; no new schema or migration framework is introduced.
- Frontend runtime validation rejects malformed server or persisted data through the existing error paths rather than allowing invalid typed state to propagate.
- Upload failure behavior remains sequential and stop-on-first-failure; only stale preview handling and identity are corrected.
- Dependency removal must be followed by lockfile regeneration and complete builds to catch transitive or tooling assumptions.
- Preserve historical cascade references in specifications and verification records. Do not alter the user's pre-existing root `README.md` modification.
- Run the API image build when the local Docker environment is available; report any environmental limitation rather than claiming it passed.
- Finish with a complete diff and status review. Only intended source, test, configuration, documentation, lockfile, and current generated-output changes are acceptable. No secret values or unrelated user changes may be included.

## Review Focus

1. **A replacement Superpowers brainstorm server or an unrelated listener now owns the recorded PID/port:** expected behavior is to stop before deleting any server state; owned by Task 3, Steps 1–2.
2. **A new current-source reference to an approved deletion appeared after the audit:** expected behavior is to retain the artifact and re-review instead of deleting it; owned by Task 1, Step 2 and Task 2, Step 1.
3. **A Docker build needs a path excluded by the new context rules:** expected behavior is a visible failed API image build, with no claim of success and no deletion of installed dependencies; owned by Task 5, Steps 2–4.
4. **Graphify regeneration leaves deleted cascade files in current metadata or recreates tracked cache files:** expected behavior is acceptance failure until current outputs are refreshed and `graphify-out/cache/` remains ignored and untracked; owned by Task 6, Steps 5–6.
5. **The dirty worktree contains the user's root README edit, unrelated changes, or secret-bearing files:** expected behavior is byte-for-byte preservation of unrelated work and exclusion of secret values from the final diff; owned by Task 1, Step 1 and Task 7, Steps 6–8.

---

### Task 1: Establish the safety baseline and remove tracked Graphify cache contents

**Files:**
- Create: none
- Modify: `.gitignore`
- Delete: tracked contents of `graphify-out/cache/`
- Test: none; command-based repository checks only

**Interfaces:**
- Consumes: completed backend, employee frontend, and customer frontend plan changes; spec §§1–4, 8.1, and 10; the current tracked-file list.
- Produces: `.gitignore` rule `graphify-out/cache/`; an empty `git ls-files graphify-out/cache` result for Tasks 6–7; the recorded root README checksum used by Task 7.

- [ ] **Step 1: Confirm the execution boundary and record pre-existing user work**

Run from the repository root:

```bash
git status --short
sha256sum README.md
```

Expected: the worktree shows only changes from the user and predecessor plans; no hygiene work has started. Record the README checksum in the execution notes. Do not restore, stage, commit, or rewrite any existing change. All remaining tasks assume the backend and both frontend implementation plans are complete; only their verification and this hygiene work remain.

- [ ] **Step 2: Recheck that application and current configuration files do not consume the cache as source**

Run:

```bash
git grep -n 'graphify-out/cache' -- \
  ':!docs/superpowers' ':!graphify-out' ':!.superpowers' || true
git ls-files graphify-out/cache
```

Expected: the search prints no application/configuration consumer. The second command lists only generated Graphify cache entries. If a current consumer appears, stop and reconcile it before deletion; do not treat a reference in this plan, the approved spec, historical snapshots, or `.superpowers/` as an application consumer.

- [ ] **Step 3: Add the exact cache ignore rule**

Set `.gitignore` to the following complete content, retaining every existing rule and appending only the final line:

```gitignore
.venv/
__pycache__/
*.pyc
.pytest_cache/
.ruff_cache/
.env
.env.*
!.env.example
secrets/*
!secrets/*.example
node_modules/
dist/
*.log
out/
data/intake-uploads/
graphify-out/cache/
```

Verify:

```bash
tail -n 3 .gitignore
```

Expected output:

```text
out/
data/intake-uploads/
graphify-out/cache/
```

- [ ] **Step 4: Delete only tracked cache files, leaving any unrelated untracked local files alone**

Run:

```bash
git ls-files -z graphify-out/cache | xargs -0 -r rm --
```

Expected: every previously tracked file under `graphify-out/cache/` is removed. This command does not delete dated Graphify snapshots or current `graph.json`, `graph.html`, `GRAPH_REPORT.md`, or `manifest.json`.

- [ ] **Step 5: Verify the cache is untracked and ignored without deleting current graph outputs**

Run:

```bash
git ls-files graphify-out/cache
git check-ignore -v graphify-out/cache/last_query_stamp
test -f graphify-out/graph.json
test -f graphify-out/graph.html
test -f graphify-out/GRAPH_REPORT.md
test -f graphify-out/manifest.json
```

Expected: `git ls-files` prints nothing; `git check-ignore` identifies `.gitignore` and `graphify-out/cache/`; all four `test` commands exit 0. No cache entry may appear as an unignored untracked file in `git status`.

### Task 2: Delete the superseded architecture HTML after a fresh reference check

**Files:**
- Create: none
- Modify: none
- Delete: `docs/architecture.html`
- Test: `docs/pipeline-architecture.html` existence and current-link checks

**Interfaces:**
- Consumes: the approved replacement `docs/pipeline-architecture.html` and current source references after predecessor plans.
- Produces: no `docs/architecture.html` file and no stale current-document link to it; Archify provenance remains untouched.

- [ ] **Step 1: Prove the replacement exists and no current document links to the obsolete file**

Run:

```bash
test -f docs/pipeline-architecture.html
rg -n 'docs/architecture\.html' \
  README.md docs/demo-readiness.md employee-frontend/README.md \
  users-frontend/README.md data docker backend employee-frontend users-frontend || true
rg -n '\]\(architecture\.html\)' docs \
  -g '!superpowers/**' -g '!verification/**' || true
```

Expected: the replacement exists and both searches print nothing. If either finds a current reference, stop and update the reference review before deleting anything. Historical references under `docs/superpowers/` and `docs/verification/` are not deletion blockers and must not be rewritten for this cleanup.

- [ ] **Step 2: Delete only the approved obsolete HTML file**

Run:

```bash
rm -- docs/architecture.html
```

Expected: the command exits 0 and removes no other file.

- [ ] **Step 3: Verify deletion and preservation of the current architecture artifact and provenance**

Run:

```bash
test ! -e docs/architecture.html
test -f docs/pipeline-architecture.html
test -f docs/pipeline-architecture.delivery.json
test -f docs/pipeline-architecture.finalize.json
test -f docs/pipeline-architecture.finalize-summary.json
test -f .archify/explainer-support-pipeline-20261102-162407/candidate.archify.md
git diff --name-only -- .archify
```

Expected: every `test` exits 0 and the final diff command prints nothing. Do not delete any Archify working set or current generated architecture receipt.

### Task 3: Remove confirmed stale local runtime state and the duplicate screenshot

**Files:**
- Create: none
- Modify: none
- Delete:
  - `.superpowers/brainstorm/59043-1792924854/state/server.pid`
  - `.superpowers/brainstorm/59043-1792924854/state/server-info`
  - `.superpowers/brainstorm/59043-1792924854/state/server-instance-id`
  - `.superpowers/brainstorm/59043-1792924854/state/server.log`
  - `.superpowers/brainstorm/.last-port`
  - `.superpowers/brainstorm/.last-token`
  - `out/architecture-desktop-v3.png`
- Test: `out/architecture-verified-desktop.png` and `.superpowers/brainstorm/59043-1792924854/content/` preservation checks

**Interfaces:**
- Consumes: the recorded brainstorm PID/port and current process/listener state; current SHA-256 values of both screenshot files.
- Produces: six fewer stale server-state files and one fewer duplicate ignored screenshot; brainstorm content and the verified screenshot remain.

- [ ] **Step 1: Recheck the recorded process and port without reading the token**

Run:

```bash
pid="$(cat .superpowers/brainstorm/59043-1792924854/state/server.pid)"
port="$(cat .superpowers/brainstorm/.last-port)"
printf 'Recorded brainstorm PID=%s port=%s\n' "$pid" "$port"
ps -p "$pid" -o pid=,args= || true
ss -ltnp "sport = :$port" || true
```

Expected: no brainstorm server is running and no listener requiring preservation owns the recorded port. If a replacement server, an active recorded process, or an ambiguous listener is present, stop this task and keep all six state files. Never print or inspect `.last-token`.

- [ ] **Step 2: Recheck for external consumers of the session-specific state**

Run:

```bash
git grep -n -e '59043-1792924854' \
  -e 'brainstorm/.last-port' -e 'brainstorm/.last-token' -- \
  ':!.superpowers' ':!docs/superpowers' || true
```

Expected: no external consumer is printed. A new consumer blocks deletion until its lifecycle is understood.

- [ ] **Step 3: Delete exactly the six approved stale state files**

Run:

```bash
rm -- \
  .superpowers/brainstorm/59043-1792924854/state/server.pid \
  .superpowers/brainstorm/59043-1792924854/state/server-info \
  .superpowers/brainstorm/59043-1792924854/state/server-instance-id \
  .superpowers/brainstorm/59043-1792924854/state/server.log \
  .superpowers/brainstorm/.last-port \
  .superpowers/brainstorm/.last-token
```

Expected: the command exits 0. Do not remove the session directory or its `content/` subtree.

- [ ] **Step 4: Verify stale state is gone and brainstorm content remains**

Run:

```bash
for path in \
  .superpowers/brainstorm/59043-1792924854/state/server.pid \
  .superpowers/brainstorm/59043-1792924854/state/server-info \
  .superpowers/brainstorm/59043-1792924854/state/server-instance-id \
  .superpowers/brainstorm/59043-1792924854/state/server.log \
  .superpowers/brainstorm/.last-port \
  .superpowers/brainstorm/.last-token
do
  test ! -e "$path" || { printf 'Unexpected remaining state: %s\n' "$path"; exit 1; }
done
test -d .superpowers/brainstorm/59043-1792924854/content
```

Expected: no remaining-state message, and the content-directory test exits 0.

- [ ] **Step 5: Reprove that the two local screenshots are byte-identical**

Run:

```bash
sha256sum out/architecture-desktop-v3.png out/architecture-verified-desktop.png
```

Expected: both lines report the same hash. If they differ, do not delete either screenshot.

- [ ] **Step 6: Delete only the duplicate and retain the verified image**

Run:

```bash
rm -- out/architecture-desktop-v3.png
test ! -e out/architecture-desktop-v3.png
test -f out/architecture-verified-desktop.png
git check-ignore -v out/architecture-verified-desktop.png
```

Expected: both tests exit 0, the verified image remains, and Git identifies the existing `out/` ignore rule. This local ignored deletion produces no tracked `out/` diff.

### Task 4: Repair only current setup and processing documentation

**Files:**
- Create: none
- Modify:
  - `docs/demo-readiness.md`
  - `data/test-kb/README.md`
- Delete: none
- Test: current-document searches and protected-history diff checks

**Interfaces:**
- Consumes: Jev-only CLI/UI behavior, existing `employee-frontend/` directory, and Compose `db` plus `api` services.
- Produces: current guides with valid paths, Jev-only instructions, and accurate Compose scope; the employee plan owns `employee-frontend/README.md`, while the root README and historical records remain unchanged.

- [ ] **Step 1: Correct the employee path and Compose statement in the demo guide**

In `docs/demo-readiness.md`, use this exact terminal snippet in place of the `customer-support-ui` snippet:

```bash
cd employee-frontend
npm ci
npm run dev -- --port 5173 --strictPort
```

Replace the Packaging / CI table row with:

```markdown
| Packaging / CI | Frontend Dockerfiles, frontend Compose services and CI. Current Compose starts PostgreSQL and the API. |
```

Verify:

```bash
rg -n 'cd employee-frontend|Current Compose starts PostgreSQL and the API' docs/demo-readiness.md
```

Expected: both new statements are printed; no surrounding historical evidence or walkthrough steps are changed.

- [ ] **Step 2: Replace only the current Arabic cascade instruction with Jev-only processing**

In `data/test-kb/README.md`, replace the first step under `## توليد مسودة ومراجعتها` with:

```markdown
١. من **New batch** ارفع [تذاكر العرض](../demo/rag_tickets.jsonl)، وابدأ المعالجة باستخدام تصنيف Jev فقط. هذه بيانات مصطنعة بتواريخ ثابتة؛ راجع [دليل التذاكر](../demo/README.md) لمطابقتها بسجلات المعاملات التجريبية. لا تغيّر معرّفات التذاكر ومحتواها المعاد رفعه بلا حاجة.
```

Verify:

```bash
sed -n '53,57p' data/test-kb/README.md
```

Expected: the step instructs `Jev` only and retains every other part of the Arabic guide.

- [ ] **Step 3: Scan current guides and prove protected documentation was not edited**

Run:

```bash
rg -n 'customer-support-ui|cascade' \
  README.md docs/demo-readiness.md employee-frontend/README.md \
  users-frontend/README.md data/test-kb/README.md || true
git diff --name-only -- docs/superpowers/specs docs/verification
sha256sum README.md
```

Expected: the current-guide search prints nothing; the protected-history diff prints nothing; the README checksum equals the value recorded in Task 1, Step 1. Historical cascade references elsewhere are intentionally preserved.

### Task 5: Restrict Docker build context without deleting installed dependencies

**Files:**
- Create: none
- Modify: `.dockerignore`
- Delete: none
- Test: `docker-compose.yml` via `docker compose config --quiet` and the `api` image build

**Interfaces:**
- Consumes: root Docker build context and `backend/Dockerfile` inputs.
- Produces: exact spec-approved Docker exclusions for local environments, dependencies, outputs, and tool directories; unchanged local installations and a validated API image when Docker is available.

- [ ] **Step 1: Write the complete Docker ignore configuration**

Set `.dockerignore` to:

```dockerignore
.env
.env.*
!.env.example
secrets
.git
graphify-out
**/.venv/
**/node_modules/
**/dist/
out/
.superpowers/
.playwright-mcp/
.archify/
.cursor/
```

Verify:

```bash
cat .dockerignore
for path in backend/pyproject.toml backend/uv.lock backend/app backend/tests/fixtures data/taxonomy.yaml docker/api-entrypoint.sh
do
  test -e "$path" || { printf 'Missing required build input: %s\n' "$path"; exit 1; }
done
```

Expected: the file contains exactly the six existing rules followed by the eight new rules, and every required build input still exists. This task changes context selection only; it does not delete `.venv`, `node_modules`, or `dist` directories.

- [ ] **Step 2: Validate the Compose model**

Run:

```bash
docker compose config --quiet
```

Expected: exit 0 with no output. A configuration error must be fixed before attempting the image build.

- [ ] **Step 3: Build the API image with the reduced context**

Run:

```bash
docker compose build api
```

Expected: the build succeeds and the resulting image contains the backend application, locked Python dependencies, test fixtures required at startup, and `data/taxonomy.yaml`. If Docker is unavailable or the environment prevents a build, record the exact environmental error and report the build as not verified; never claim it passed.

- [ ] **Step 4: Confirm local dependency directories were not removed**

Run:

```bash
for path in backend/.venv employee-frontend/node_modules users-frontend/node_modules
do
  if test -d "$path"; then printf 'Preserved local directory: %s\n' "$path"; fi
done
```

Expected: every local dependency directory that existed before this task is printed as preserved. No package installation or deletion is part of this task.

### Task 6: Regenerate current Graphify outputs as the final mutating task

**Files:**
- Create: regenerated ignored files under `graphify-out/cache/` only
- Modify:
  - `graphify-out/graph.json`
  - `graphify-out/graph.html`
  - `graphify-out/GRAPH_REPORT.md`
  - `graphify-out/manifest.json`
  - Graphify-managed current label/metadata sidecars only when the CLI changes them
- Delete: none
- Test: current manifest/report freshness, deleted-cascade absence, cache ignore status, and dated-snapshot/Archify diff checks

**Interfaces:**
- Consumes: the final source, test, configuration, lockfile, and documentation state from every predecessor task and plan; Task 1's cache ignore rule.
- Produces: current Graphify navigation outputs that match the final source tree, with no tracked regenerated cache and no changed dated snapshot. No intentional source, configuration, documentation, or Graphify-output mutation is permitted after this task except correcting a failed verification and rerunning this task.

- [ ] **Step 1: Confirm this is the last source-affecting task**

Run:

```bash
git status --short
```

Expected: all intended backend, frontend, hygiene, configuration, documentation, and lockfile changes are present. Review the list before regeneration. If another source edit is needed, complete it first and then repeat the relevant predecessor checks; do not regenerate Graphify early.

- [ ] **Step 2: Establish that dated snapshots and Archify provenance begin unchanged**

Run:

```bash
git diff --name-only -- .archify graphify-out/2026-*
find graphify-out -mindepth 2 -maxdepth 2 -type f \
  -path 'graphify-out/2026-*/*' -print0 | sort -z | xargs -0 sha256sum
```

Expected: the diff command prints nothing. Record the dated-snapshot checksum output in the execution notes for comparison after regeneration.

- [ ] **Step 3: Update the graph from the final repository state**

Run:

```bash
graphify update .
```

Expected: Graphify completes successfully and refreshes current extraction, graph, report, and manifest data from the final source. It must not write into any dated `graphify-out/2026-*` directory. If the command fails, fix the reported source/tooling issue and rerun it before continuing.

- [ ] **Step 4: Regenerate the current interactive HTML from the updated graph**

Run:

```bash
graphify export html
```

Expected: `graphify-out/graph.html` is regenerated successfully from the updated `graph.json`; no dated HTML snapshot is created or modified.

- [ ] **Step 5: Verify deleted cascade files are absent and current metadata is fresh**

Run:

```bash
rg -n 'backend/app/pipeline/stage2_classify/cascade\.py|backend/tests/test_cascade\.py' \
  graphify-out/manifest.json graphify-out/GRAPH_REPORT.md || true
git rev-parse --short HEAD
sed -n '13,16p' graphify-out/GRAPH_REPORT.md
graphify update .
```

Expected: the search prints nothing; the report's `Built from commit` identifies the same HEAD printed by Git; the second update reports that no changed source files require extraction and does not alter the content of the current outputs. Historical cascade concepts extracted from historical documents may remain, but deleted source/test file entries may not.

- [ ] **Step 6: Verify regenerated cache contents are ignored and untracked**

Run:

```bash
git ls-files graphify-out/cache
git check-ignore -v graphify-out/cache/last_query_stamp
git status --short -- graphify-out/cache
```

Expected: `git ls-files` and `git status` print nothing; `git check-ignore` identifies the `.gitignore` rule `graphify-out/cache/`. If the regeneration did not recreate `last_query_stamp`, use an existing regenerated cache path in the `git check-ignore` command and expect the same rule.

- [ ] **Step 7: Prove all protected generated history and current architecture provenance are unchanged**

Run:

```bash
git diff --exit-code -- \
  .archify graphify-out/2026-* \
  docs/pipeline-architecture.html \
  docs/pipeline-architecture.delivery.json \
  docs/pipeline-architecture.finalize.json \
  docs/pipeline-architecture.finalize-summary.json
find graphify-out -mindepth 2 -maxdepth 2 -type f \
  -path 'graphify-out/2026-*/*' -print0 | sort -z | xargs -0 sha256sum
```

Expected: `git diff --exit-code` exits 0 with no output, and the dated-snapshot checksums match Task 6, Step 2 exactly. Do not delete Archify working sets, current architecture receipts, Playwright evidence, or dated Graphify snapshots.

### Task 7: Run the complete acceptance matrix and review the final diff and secrets boundary

**Files:**
- Create: none
- Modify: none unless a failed check requires a focused correction followed by Task 6 regeneration
- Delete: none
- Test: all backend, employee frontend, customer frontend, Docker, documentation, Graphify, protected-history, and diff checks listed below

**Interfaces:**
- Consumes: every predecessor plan and Tasks 1–6, including the Task 1 README checksum and Task 6 dated-snapshot checksums.
- Produces: a verified final worktree with only intended source, test, configuration, documentation, lockfile, hygiene-deletion, and current generated-output changes; no commits and no secret values included.

- [ ] **Step 1: Run the complete backend acceptance checks**

Run:

```bash
cd backend
uv run pytest -q
uv run ruff check app tests
cd ..
```

Expected: all backend tests and Ruff pass, including the repaired baseline and every new regression test from the backend plan. The original three fixture-related failures are gone; no failure may be waived as an accepted baseline failure.

- [ ] **Step 2: Run the complete employee frontend acceptance checks**

Run:

```bash
cd employee-frontend
npm run typecheck
npm test
npm run lint
npm run build
cd ..
```

Expected: all four commands pass. Typechecking builds referenced projects, all existing and new tests pass, and the production build has no TypeScript errors.

- [ ] **Step 3: Run the complete customer frontend acceptance checks**

Run:

```bash
cd users-frontend
npm test
npm run typecheck
npm run lint
npm run build
npm --workspace web test
cd ..
```

Expected: all commands pass. The root and workspace test commands execute the same web suite; typechecking covers application, tests, and Vite/Vitest configuration.

- [ ] **Step 4: Recheck Docker acceptance**

Run:

```bash
docker compose config --quiet
docker compose build api
```

Expected: Compose validation and the API build succeed. If the environment still prevents the image build, report the exact limitation and keep it explicitly unverified rather than treating Task 5's configuration-only success as a build pass.

- [ ] **Step 5: Recheck current documentation, deleted artifacts, and Graphify cache acceptance**

Run:

```bash
rg -n 'customer-support-ui|cascade' \
  README.md docs/demo-readiness.md employee-frontend/README.md \
  users-frontend/README.md data/test-kb/README.md || true
test ! -e docs/architecture.html
test ! -e out/architecture-desktop-v3.png
test -f out/architecture-verified-desktop.png
git ls-files graphify-out/cache
git check-ignore -v graphify-out/cache/last_query_stamp
rg -n 'backend/app/pipeline/stage2_classify/cascade\.py|backend/tests/test_cascade\.py' \
  graphify-out/manifest.json graphify-out/GRAPH_REPORT.md || true
```

Expected: both searches print nothing; all four artifact tests exit 0; `git ls-files` prints nothing; `git check-ignore` prints the cache ignore rule. Current guides contain no retired processing instruction, while historical documents remain unchanged.

- [ ] **Step 6: Review the complete worktree and diff**

Run:

```bash
git status --short
git diff --stat
git diff --name-only
git diff --check
git diff -- . ':!.env' ':!secrets'
```

Expected: only intended source, test, configuration, documentation, lockfile, approved hygiene-deletion, and current Graphify-output changes appear. `git diff --check` reports no new whitespace error. The full diff excludes secret-bearing paths and is reviewed in its entirety, including every current generated-output change. There are no untracked cache files, local dependency changes, local screenshot changes, or unrelated generated artifacts. No command in this plan stages or commits anything.

- [ ] **Step 7: Prove protected history and user artifacts were not deleted or overwritten**

Run:

```bash
git diff --name-only --diff-filter=D -- \
  .archify .playwright-mcp docs/superpowers docs/verification graphify-out/2026-*
test -d .superpowers/brainstorm/59043-1792924854/content
test -f presentation/SaifAlmaliki_Topic06_FAZAA_Design_Brief.pptx
sha256sum README.md
find graphify-out -mindepth 2 -maxdepth 2 -type f \
  -path 'graphify-out/2026-*/*' -print0 | sort -z | xargs -0 sha256sum
```

Expected: the deletion-filtered diff prints nothing; both artifact tests exit 0; the README checksum matches Task 1, Step 1; and every dated-snapshot checksum matches Task 6, Step 2. Historical cascade references in specs and verification records are expected and are not failures.

- [ ] **Step 8: Perform the final secret and unrelated-change review without printing secret files**

Run:

```bash
git diff --name-only -- .env secrets/
git diff -- . ':!.env' ':!secrets' | \
  rg '^\+.*(TYPESAFE_API_KEY|OPENROUTER_API_KEY|DATABASE_URL)\s*=\s*\S+' || true
```

Expected: neither command prints a newly changed secret-bearing file or a newly added concrete credential/database assignment. Do not open `.env`, `.last-token`, or real files under `secrets/` to perform this review. Manually inspect the remaining complete diff for unintended user changes and generated noise. Acceptance requires no secret values and no unrelated user modifications; any such finding blocks completion until removed through a focused, non-destructive correction and the affected checks are rerun.
