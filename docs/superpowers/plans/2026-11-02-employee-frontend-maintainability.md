# Employee Frontend Maintainability Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Remove reference-verified employee-frontend dead code, migrate active trace coverage before retiring legacy code, establish focused run/queue/knowledge boundaries, repair the two TypeScript fixture errors and false-green standalone typecheck, and update current employee documentation without changing appearance or user flows.

**Architecture:** Work cleanup-first, then perform behavior-preserving module extraction, then repair the recorded baseline failures and documentation. Keep `reviewEvidence`, `TicketFlow`, index-lifecycle orchestration, mutations, API contracts, and polling orchestration intact; introduce only a bounded run-result loader, a pure queue projection, presentational knowledge components, and a separate run-detail route module.

**Tech Stack:** React 19, TypeScript 6, Vite 8, Vitest 5, React Router 7, Base UI/Radix primitives, npm, ESLint.

**Spec:** `docs/superpowers/specs/2026-11-02-maintainability-refactor-design.md` (§§1-4, 6, 8.2 employee README requirements, 9-10).

## Global Constraints

The following constraints are copied exactly from the approved specification and apply to every task:

- "Perform a targeted maintainability pass across the repository. Remove reference-verified dead code, correct confirmed defects, and extract modules only where a clear responsibility boundary already exists. Preserve the current product, visual design, public compatibility contracts, and historical records."
- "Use a cleanup-first sweep with the recorded baseline as the comparison point:"
  1. "Remove confirmed dead code and safe stale artifacts."
  2. "Perform mechanical, behavior-preserving modularization."
  3. "Fix baseline failures and selected confirmed defects with regression tests."
- "Until baseline repair, intermediate verification may show only the three documented backend failures and two documented employee TypeScript errors. Any additional failure is a regression and must be resolved before continuing."
- "No git commits or other git mutations are part of this design."
- "This pass does not:"
  - "Rewrite the pipeline, intake architecture, API, or frontend applications."
  - "Change visual styling or user flows."
  - "Reformat unrelated files or make stylistic changes without a maintainability purpose."
  - "Remove public compatibility fields such as `fallback_rate`, `classifier_paths`, or `ClassifierOutput.degraded`."
  - "Broaden JSONL parsing, weaken TypeScript contracts, or add type-suppression comments."
  - "Perform broad localization consolidation or extract `ReviewEditor` in this pass."
  - "Delete historical material merely because it mentions retired cascade behavior."
  - "Delete generated UI primitive exports solely because they currently lack local consumers."
- "Do not change the current visual design or extract `ReviewEditor` in this pass."
- "Existing HTTP status codes, public messages, optimistic-concurrency protections, idempotency keys, revision rules, and safe secret-free responses remain unchanged unless a defect fix explicitly requires otherwise."
- "Dependency removal must be followed by lockfile regeneration and complete builds to catch transitive or tooling assumptions."
- "All existing tests must pass together with the new active TicketFlow, loader, queue, and knowledge-view tests."
- "Finish with a complete diff and status review. Only intended source, test, configuration, documentation, lockfile, and current generated-output changes are acceptable. No secret values or unrelated user changes may be included."

## Review Focus

- **Pre-aborted loader input:** an already-aborted run-result request should reject with `AbortError`, pass the same signal to the initial request, and issue no detail requests; owned by Task 3, test `rejects a pre-aborted request before loading detail items`.
- **Initial-list failure:** a failed result-list request should preserve the existing API error and issue zero detail requests; owned by Task 3, test `preserves a list failure without requesting details`.
- **Empty/no-match queue projection:** empty rows or combined filters with no matches and an out-of-range requested page should clamp to page zero with empty visible rows; owned by Task 4, test `clamps empty and no-match projections to page zero`.
- **Failed document with unclaimed acceptance:** a failed document whose accepted request is still pending should show previous-attempt guidance and the explicit `Request indexing again` action; owned by Task 5, test `renders a pending failed document as a recoverable previous attempt`.
- **Missing or disabled readiness:** missing health should remain unavailable, and disabled knowledge should say retrieval is disabled rather than implying indexed passages are ready; owned by Task 5, test `keeps missing and disabled readiness explicit`.

---

### Task 1: Remove reference-verified dead exports, components, and the Mermaid dependency

**Files:**
- Modify: `employee-frontend/src/lib/stages.ts:67-76`
- Modify: `employee-frontend/src/components/theme-provider.tsx:221-229`
- Delete: `employee-frontend/src/components/ui/skeleton.tsx`
- Delete: `employee-frontend/src/components/ui/separator.tsx`
- Modify: `employee-frontend/package.json:24`
- Modify: `employee-frontend/package-lock.json`
- Test: `employee-frontend/src/lib/api.test.ts` and the existing employee suite as regression coverage; no test-file changes

**Interfaces:**
- Consumes: Existing `stages` export for the legacy cluster, existing `ThemeProvider({ children, defaultTheme, storageKey, disableTransitionOnChange })`, and npm's lockfile generator.
- Produces: No `agentTools`, `Skeleton`, `Separator`, `useTheme`, or direct `mermaid` dependency; unchanged `ThemeProvider` and all remaining UI exports.

- [ ] **Step 1: Repeat reference searches before deleting anything**

Run from the repository root:

```bash
cd employee-frontend
rg -n "agentTools|useTheme|Skeleton|ui/skeleton|Separator|ui/separator" src --glob '*.{ts,tsx}'
rg -n "from ['\"]mermaid['\"]|import\(['\"]mermaid['\"]\)|require\(['\"]mermaid['\"]\)" src vite.config.ts eslint.config.js --glob '*.{ts,tsx,js}'
```

Expected: `agentTools` and `useTheme` occur only at their declarations; `Skeleton` and the standalone `Separator` occur only in their own files; the Mermaid import search returns no matches. `SelectSeparator` in `select.tsx` is not the standalone component and must remain.

- [ ] **Step 2: Remove only the confirmed dead TypeScript exports and component files**

Delete `src/components/ui/skeleton.tsx` and `src/components/ui/separator.tsx`. Remove the complete `agentTools` array from `src/lib/stages.ts`, leaving the existing `stages` array intact for the reference-checked legacy-migration task. Remove only this hook from `src/components/theme-provider.tsx`; retain the provider and context:

```tsx
  return (
    <ThemeProviderContext.Provider {...props} value={value}>
      {children}
    </ThemeProviderContext.Provider>
  )
}
```

Do not remove other generated primitive exports.

- [ ] **Step 3: Remove Mermaid and regenerate the npm lockfile**

Run:

```bash
cd employee-frontend
npm uninstall mermaid
```

Expected: npm removes the direct `mermaid` entry from `package.json`, regenerates `package-lock.json`, and reports no audit or dependency resolution failure. Do not manually edit lockfile package nodes.

- [ ] **Step 4: Run focused regression verification**

Run:

```bash
cd employee-frontend
npm test
npm run lint
./node_modules/.bin/tsc -p tsconfig.app.json --noEmit --incremental false
```

Expected: all 62 existing tests pass and lint exits zero. The standalone TypeScript command exits with exactly the two recorded TS2739 errors at `ticket-flow-view.test.tsx:27-28`; any additional error is a regression.

- [ ] **Step 5: Review the cleanup diff**

Run:

```bash
cd employee-frontend
git diff -- src/lib/stages.ts src/components/theme-provider.tsx src/components/ui/skeleton.tsx src/components/ui/separator.tsx package.json package-lock.json
git status --short
```

Expected: only the listed dead code/dependency changes appear. The pre-existing root `README.md` modification and unrelated user files remain untouched. No commit is created.

### Task 2: Migrate active TicketFlow coverage, then retire the legacy trace/chart cluster

**Files:**
- Modify: `employee-frontend/src/features/review/ticket-flow-view.test.tsx`
- Modify: `employee-frontend/src/features/review/malformed-trace.test.tsx`
- Modify: `employee-frontend/src/features/review/ticket-flow.test.ts`
- Modify: `employee-frontend/src/features/review/ticket-flow.ts:317-373`
- Delete: `employee-frontend/src/features/review/PipelineTrace.tsx`
- Delete: `employee-frontend/src/features/review/trace-facts.ts`
- Delete: `employee-frontend/src/lib/stages.ts`
- Test: `employee-frontend/src/features/review/ticket-flow-view.test.tsx`
- Test: `employee-frontend/src/features/review/malformed-trace.test.tsx`
- Test: `employee-frontend/src/features/review/ticket-flow.test.ts`
- Test: `employee-frontend/src/features/review/review-evidence.test.ts`

**Interfaces:**
- Consumes: `TicketFlow({ result }: { result: Result })`, `reviewEvidence(result)`, and the existing full `Result` fixture in `ticket-flow-view.test.tsx`.
- Produces: Active ThoughtChain coverage for citations/tools/malformed traces/secrets; `buildTicketFlow(result, arabic?)` and active `FlowStep` models remain; no `PipelineTrace`, `stageFacts`, `toolFact`, `mermaidText`, `pipelineChart`, `detailChart`, or `stages` module.

- [ ] **Step 1: Add the active TicketFlow regression test before deleting legacy code**

Add `Passage` to the type import in `ticket-flow-view.test.tsx` and append this test. It deliberately mixes malformed entries with a valid tool event and retains a citation snapshot:

```tsx
import type { Passage, Result } from "@/lib/types"

const retainedPassage: Passage = {
  id: "p1",
  document_id: 1,
  chunk_index: 0,
  filename: "saved.md",
  text: "دليل محفوظ",
  score: 0.9,
  page_start: null,
  page_end: null,
}

it("renders retained citations and valid tools while excluding malformed entries and secrets", () => {
  const rawTrace = [
    null,
    42,
    "bad",
    [],
    {
      kind: "tool",
      tool: "search_knowledge_base",
      status: "ok",
      arguments: { query: "refund", password: "secret" },
    },
    { kind: "stage", node: "decide", elapsed_ms: 5 },
  ]
  const html = renderToStaticMarkup(
    <TicketFlow
      result={result({
        citations: ["p1"],
        citation_sources: [retainedPassage],
        agent_trace: rawTrace,
        draft_text: "رد تجريبي",
        error: "PIN 1234 should stay hidden",
      })}
    />,
  )

  expect(html).toContain("بحث في قاعدة المعرفة")
  expect(html).toContain("اكتمل")
  expect(html).toContain("saved.md")
  expect(html).toContain("دليل محفوظ")
  expect(html).not.toContain("secret")
  expect(html).not.toContain("PIN 1234")
  expect(html).not.toContain(".py")
})
```

- [ ] **Step 2: Prove the new active coverage passes before legacy deletion**

Run:

```bash
cd employee-frontend
npx vitest run src/features/review/ticket-flow-view.test.tsx
```

Expected: 3 tests pass, including the new retained-citation/tool/malformed-entry test. Do not proceed to deletion if this test fails.

- [ ] **Step 3: Preserve useful model assertions while removing chart-only assertions**

In `ticket-flow.test.ts`, change the imports to active-only dependencies:

```ts
import { expect, it } from "vitest"
import type { Result } from "../../lib/types"
import { channelName, checkLines, fieldLabel, isArabicMessage, lookupSentence, sentence, toolLine } from "./ticket-flow-copy"
import { buildTicketFlow } from "./ticket-flow"
```

In `explains that an uncertain Jev-only result goes to human review`, replace the `detailChart` assertion with the active step model:

```ts
it("explains that an uncertain Jev-only result goes to human review", () => {
  const flow = buildTicketFlow(result({ escalated: true, escalation_reasons: ["low_confidence"] }))
  expect(step(flow, "jev_classify").produced).toBe(
    "Jev was unsure, so the ticket was flagged for human review.",
  )
  expect(step(flow, "jev_classify").produced).not.toContain("Gemini")
  expect(step(flow, "gemini_classify").reason).toBe("This Jev-only run did not use Gemini.")
})
```

In `describes the Empty ticket detail without mentioning a saved reply or policy passages`, derive detail text from the active step:

```ts
it("describes the Empty ticket detail without mentioning a saved reply or policy passages", () => {
  const flow = buildTicketFlow(result({ classifier_path: "jev", escalation_reasons: ["empty_ticket"] }, { text: "  " }))
  const emptyStep = step(flow, "escalate_empty")
  const detail = [emptyStep.received, ...emptyStep.events, emptyStep.produced].join("\n")
  expect(emptyStep.state).toBe("used")
  expect(emptyStep.received).toBe("The customer message was empty.")
  expect(emptyStep.produced).toBe("Held for a person because the message was empty.")
  expect(detail).not.toContain("reply")
  expect(detail).not.toContain("policy passage")
  expect(detail).not.toContain("policy passages")
})
```

In `does not call a legacy Gemini-unavailable result Jev-only`, keep the active flow assertion and remove the `getLocale`/`setLocale`/`stageFacts` block so the test ends here:

```ts
  expect(step(flow, "gemini_classify").reason).toBe(
    "Gemini was asked, but no classification was recorded.",
  )
})
```

Delete the three chart-only tests named `escapes text that could break a Mermaid node or inject a directive`, `draws the full pipeline with the taken step, the skip reason, and the selection`, and `draws the open step from received through events to produced`.

- [ ] **Step 4: Keep malformed evidence tests but remove their legacy renderer dependency**

Replace `malformed-trace.test.tsx` with this active-evidence version; the new TicketFlow test from Step 1 owns active rendering of valid tool events:

```tsx
import { renderToStaticMarkup } from "react-dom/server"
import { expect, it } from "vitest"
import type { Result } from "@/lib/types"
import { CitationEvidence } from "./CitationEvidence"
import { reviewEvidence } from "./review-evidence"

const source = { id: "p1", document_id: 1, chunk_index: 0, filename: "saved.md", text: "دليل محفوظ", score: 0.9, page_start: null, page_end: null }

it.each([null, {}, [null], [null, 42, "bad", [], { kind: "tool", tool: "search_knowledge_base" }, { kind: "stage", node: "decide", elapsed_ms: 5 }]].map((raw) => ({ raw })))(
  "retains citations and raw audit data for historical malformed traces: $raw", ({ raw }) => {
    const result = { citations: ["p1"], citation_sources: [source], agent_trace: raw } as Result
    const before = JSON.stringify(raw)
    const evidence = reviewEvidence(result)
    expect(evidence.sources).toEqual([source])
    expect(evidence.tools.length).toBe(Array.isArray(raw) && raw.length > 1 ? 1 : 0)
    expect(renderToStaticMarkup(<CitationEvidence result={result} />)).toContain("دليل محفوظ")
    expect(result.agent_trace).toBe(raw)
    expect(JSON.stringify(raw)).toBe(before)
  },
)
```

- [ ] **Step 5: Delete the legacy implementation and chart functions after active tests pass**

Delete `PipelineTrace.tsx`, `trace-facts.ts`, and the now-exclusive `src/lib/stages.ts`. In `ticket-flow.ts`, retain `buildTicketFlow` and delete everything from `export function mermaidText` through the end of `detailChart`, leaving this as the end of the active module:

```ts
  return { arabic, selectedId, steps }
}
```

Run reference searches:

```bash
cd employee-frontend
rg -n "PipelineTrace|trace-facts|stageFacts|checkFact|toolFact|mermaidText|pipelineChart|detailChart|lib/stages|agentTools" src --glob '*.{ts,tsx}'
```

Expected: no matches.

- [ ] **Step 6: Run focused review regression tests**

Run:

```bash
cd employee-frontend
npx vitest run src/features/review/ticket-flow-view.test.tsx src/features/review/ticket-flow.test.ts src/features/review/malformed-trace.test.tsx src/features/review/review-evidence.test.ts
npm run lint
```

Expected: all remaining and migrated tests pass; lint exits zero; no removed symbol is imported.

- [ ] **Step 7: Review the legacy-retirement diff**

Run:

```bash
cd employee-frontend
git diff -- src/features/review src/lib/stages.ts
git status --short
```

Expected: active `TicketFlow` and `reviewEvidence` remain, useful behavior assertions are migrated, and only the approved legacy cluster/chart assertions are removed. No commit is created.

### Task 3: Split RunDetailPage and introduce bounded run-result loading

**Files:**
- Create: `employee-frontend/src/features/runs/run-results.ts`
- Create: `employee-frontend/src/features/runs/run-results.test.ts`
- Create: `employee-frontend/src/features/runs/RunDetailPage.tsx`
- Modify: `employee-frontend/src/features/runs/RunsPage.tsx`
- Modify: `employee-frontend/src/App.tsx:18-21`
- Test: `employee-frontend/src/features/runs/run-results.test.ts`

**Interfaces:**
- Consumes: `request<T>(path: string, options?: RequestInit): Promise<T>`, `useResource<T>(path, revision, pollMs, loader)`, `Result`, `Run`, and the existing `RunDetailPage` JSX.
- Produces: `export const RUN_RESULT_CONCURRENCY = 8`; `export function loadRunResults(path: string, options: RequestInit): Promise<Result[]>`; `export function RunDetailPage()` imported by `App.tsx` from `@/features/runs/RunDetailPage`.

- [ ] **Step 1: Write failing bounded-loader tests**

Create `run-results.test.ts` with the following complete suite. The tests cover the required limit/order/fidelity behavior, empty results, detail and list failures, in-flight aborts, and the Review Focus pre-aborted case:

```ts
import { afterEach, expect, it, vi } from "vitest"
import { loadRunResults, RUN_RESULT_CONCURRENCY } from "./run-results"

function json(value: unknown, status = 200) {
  return new Response(JSON.stringify(value), {
    status,
    headers: { "Content-Type": "application/json" },
  })
}

function deferred<T>() {
  let resolve!: (value: T | PromiseLike<T>) => void
  let reject!: (reason?: unknown) => void
  const promise = new Promise<T>((res, rej) => {
    resolve = res
    reject = rej
  })
  return { promise, resolve, reject }
}

afterEach(() => {
  vi.unstubAllGlobals()
  vi.restoreAllMocks()
})

it("loads every detail once, preserves order, and respects the in-flight limit", async () => {
  const ids = Array.from({ length: 12 }, (_, index) => index + 1)
  const gate = deferred<void>()
  const detailUrls: string[] = []
  let active = 0
  let maximumActive = 0
  const fetchMock = vi.fn(async (input: RequestInfo | URL) => {
    const url = String(input)
    if (url.includes("run_id=")) return json({ items: ids.map((id) => ({ id })) })
    detailUrls.push(url)
    active += 1
    maximumActive = Math.max(maximumActive, active)
    await gate.promise
    active -= 1
    const id = Number(url.split("/").at(-1))
    return json({ id, ticket: { external_id: `T-${id}` } })
  })
  vi.stubGlobal("fetch", fetchMock)

  const pending = loadRunResults("/results?run_id=3&limit=500", {})
  await vi.waitFor(() => expect(active).toBe(RUN_RESULT_CONCURRENCY))
  gate.resolve()
  const results = await pending

  expect(maximumActive).toBe(RUN_RESULT_CONCURRENCY)
  expect(results.map((item) => item.id)).toEqual(ids)
  expect(detailUrls).toHaveLength(ids.length)
  expect(new Set(detailUrls).size).toBe(ids.length)
})

it("returns an empty result without requesting details", async () => {
  const fetchMock = vi.fn(async () => json({ items: [] }))
  vi.stubGlobal("fetch", fetchMock)
  await expect(loadRunResults("/results?run_id=3&limit=500", {})).resolves.toEqual([])
  expect(fetchMock).toHaveBeenCalledTimes(1)
})

it("preserves a detail failure through the existing request error path", async () => {
  vi.stubGlobal("fetch", vi.fn(async (input: RequestInfo | URL) => {
    const url = String(input)
    if (url.includes("run_id=")) return json({ items: [{ id: 1 }, { id: 2 }] })
    if (url.endsWith("/2")) return json({ detail: "detail failed" }, 500)
    return json({ id: 1 })
  }))
  await expect(loadRunResults("/results?run_id=3&limit=500", {})).rejects.toThrow("detail failed")
})

it("preserves a list failure without requesting details", async () => {
  const fetchMock = vi.fn(async () => json({ detail: "list failed" }, 503))
  vi.stubGlobal("fetch", fetchMock)
  await expect(loadRunResults("/results?run_id=3&limit=500", {})).rejects.toThrow("list failed")
  expect(fetchMock).toHaveBeenCalledTimes(1)
})

it("propagates the caller signal to detail requests and rejects on abort", async () => {
  const controller = new AbortController()
  let detailSignal: AbortSignal | null | undefined
  vi.stubGlobal("fetch", vi.fn(async (input: RequestInfo | URL, init?: RequestInit) => {
    if (String(input).includes("run_id=")) return json({ items: [{ id: 1 }] })
    detailSignal = init?.signal
    return new Promise<Response>((_resolve, reject) => {
      init?.signal?.addEventListener("abort", () => reject(new DOMException("Aborted", "AbortError")), { once: true })
    })
  }))

  const pending = loadRunResults("/results?run_id=3&limit=500", { signal: controller.signal })
  const rejection = expect(pending).rejects.toMatchObject({ name: "AbortError" })
  await vi.waitFor(() => expect(detailSignal).toBe(controller.signal))
  controller.abort()
  await rejection
})

it("rejects a pre-aborted request before loading detail items", async () => {
  const controller = new AbortController()
  controller.abort()
  const fetchMock = vi.fn(async (_input: RequestInfo | URL, init?: RequestInit) => {
    if (init?.signal?.aborted) throw new DOMException("Aborted", "AbortError")
    return json({ items: [{ id: 1 }] })
  })
  vi.stubGlobal("fetch", fetchMock)

  await expect(loadRunResults("/results?run_id=3&limit=500", {
    signal: controller.signal,
  })).rejects.toMatchObject({ name: "AbortError" })
  expect(fetchMock).toHaveBeenCalledTimes(1)
  expect(fetchMock.mock.calls[0][1]?.signal).toBe(controller.signal)
})
```

Run:

```bash
cd employee-frontend
npx vitest run src/features/runs/run-results.test.ts
```

Expected: FAIL because `./run-results` does not exist.

- [ ] **Step 2: Implement the minimal bounded loader**

Create `src/features/runs/run-results.ts`:

```ts
import { request } from "@/lib/api"
import type { Result } from "@/lib/types"

export const RUN_RESULT_CONCURRENCY = 8

export async function loadRunResults(
  path: string,
  options: RequestInit,
): Promise<Result[]> {
  const page = await request<{ items: Result[] }>(path, options)
  const results = new Array<Result>(page.items.length)
  let nextIndex = 0

  async function worker() {
    while (nextIndex < page.items.length) {
      const index = nextIndex
      nextIndex += 1
      options.signal?.throwIfAborted()
      results[index] = await request<Result>(
        `/results/${page.items[index].id}`,
        options,
      )
    }
  }

  await Promise.all(
    Array.from(
      { length: Math.min(RUN_RESULT_CONCURRENCY, page.items.length) },
      () => worker(),
    ),
  )
  return results
}
```

Run:

```bash
cd employee-frontend
npx vitest run src/features/runs/run-results.test.ts
```

Expected: all 6 loader tests pass; maximum concurrency is 8, result order is stable, empty input performs one request, and abort/failure tests reject through the original error path.

- [ ] **Step 3: Move RunDetailPage into its own module using the new loader**

Create `src/features/runs/RunDetailPage.tsx` with the existing JSX and polling arguments unchanged:

```tsx
import { Link, useParams } from "react-router-dom"
import { ArrowLeft, ArrowRight, CheckCheck, Clock3, Coins, Download, Layers3 } from "lucide-react"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { EmptyState, ErrorState, LoadingState, Metric, PageHeader, StatusBadge } from "@/components/shared/workspace-ui"
import { useResource } from "@/hooks/use-resource"
import { useWorkspace } from "@/lib/workspace"
import { categoryLabel, dateLabel, downloadJson, duration, humanize, timeLabel } from "@/lib/format"
import type { Result, Run } from "@/lib/types"
import { TicketFlow } from "@/features/review/TicketFlow"
import { loadRunResults } from "./run-results"

export function RunDetailPage() {
  const { id } = useParams(),
    workspace = useWorkspace()
  const query = useResource<Run>(`/runs/${id}`, workspace.revision, 2500)
  const run = query.data
  const results = useResource<Result[]>(
    run ? `/results?run_id=${run.id}&limit=500` : null,
    workspace.revision,
    run?.status === "running" ? 2500 : 0,
    loadRunResults,
  )
  if (query.error)
    return <ErrorState message={query.error} retry={query.reload} />
  if (!run)
    return query.loading ? (
      <LoadingState />
    ) : (
      <EmptyState
        title="Run not found"
        description="Choose a run from the pipeline history."
      />
    )
  const progress = run.total ? Math.round((run.processed / run.total) * 100) : 0
  return (
    <>
      <Link to="/runs" className="back-link">
        <ArrowLeft size={15} />
        All pipeline runs
      </Link>
      <PageHeader
        title={`Batch #${String(run.id).padStart(3, "0")}`}
        description={`Started ${dateLabel(run.started_at)} at ${timeLabel(run.started_at)} Baghdad · ${run.mode === "cascade" ? "Jev with Gemini fallback" : humanize(run.mode)}`}
      >
        <Button
          variant="outline"
          onClick={() => downloadJson(run, `batch-${run.id}-summary.json`)}
        >
          <Download size={16} />
          Export summary
        </Button>
        <Button nativeButton={false} render={<Link to={`/?run=${run.id}`} />}>
          Review tickets
          <ArrowRight size={16} />
        </Button>
      </PageHeader>
      <Card className="run-progress-card">
        <CardContent>
          <div>
            <h2>
              {run.status === "running"
                ? "Preparing your tickets"
                : run.status === "failed"
                  ? "Batch interrupted"
                  : "Batch processing finished"}
            </h2>
            <StatusBadge status={run.status} />
          </div>
          <p>
            {run.processed} of {run.total} tickets processed
          </p>
          <div
            className="run-progress"
            role="progressbar"
            aria-label="Batch progress"
            aria-valuenow={progress}
            aria-valuemin={0}
            aria-valuemax={100}
          >
            <span style={{ width: `${progress}%` }} />
          </div>
          {run.counts.error && <p className="error-text">{run.counts.error}</p>}
          {run.degraded && run.mode === "cascade" && (
            <p className="field-help">
              Jev was unavailable for part of this run. Gemini fallback is
              recorded in the results.
            </p>
          )}
        </CardContent>
      </Card>
      <div className="metrics-grid">
        <Metric
          label="Processed"
          value={run.processed}
          detail={`Of ${run.total} submitted tickets`}
          icon={<Layers3 size={18} />}
        />
        <Metric
          label="Needs human review"
          value={run.counts.by_status?.escalated || 0}
          detail="Review the escalation notes"
          icon={<CheckCheck size={18} />}
          tone="metric-amber"
        />
        <Metric
          label="Median latency"
          value={duration(run.counts.latency_p50_ms || 0)}
          detail="Per processed ticket"
          icon={<Clock3 size={18} />}
        />
        <Metric
          label="Estimated run cost"
          value={`$${run.total_cost_usd.toFixed(4)}`}
          detail="Based on recorded token usage"
          icon={<Coins size={18} />}
        />
      </div>
      <div className="two-column">
        <Card>
          <CardHeader>
            <CardTitle>Issue breakdown</CardTitle>
          </CardHeader>
          <CardContent>
            <Breakdown
              values={run.counts.by_category || {}}
              label={categoryLabel}
            />
          </CardContent>
        </Card>
        <Card>
          <CardHeader>
            <CardTitle>Escalation reasons</CardTitle>
          </CardHeader>
          <CardContent>
            <Breakdown
              values={run.counts.escalation_reasons || {}}
              label={humanize}
            />
          </CardContent>
        </Card>
      </div>
      <section className="run-flows">
        {results.error && <p className="error-text">{results.error}</p>}
        {results.data?.map((result) => (
          <div key={result.id}>
            <Link to={`/tickets/${result.id}`} className="run-flow-ticket">
              {result.ticket.external_id}
            </Link>
            <TicketFlow result={result} />
          </div>
        ))}
        {!results.data?.length && !results.loading && (
          <p className="muted small">
            {run.status === "running"
              ? "Steps appear here when a ticket finishes."
              : "No processed ticket to show yet."}
          </p>
        )}
      </section>
    </>
  )
}

function Breakdown({
  values,
  label,
}: {
  values: Record<string, number>
  label: (value: string) => string
}) {
  const entries = Object.entries(values)
  return entries.length ? (
    <div className="simple-breakdown">
      {entries.map(([key, count]) => (
        <div key={key}>
          <span>{label(key)}</span>
          <strong>{count}</strong>
        </div>
      ))}
    </div>
  ) : (
    <p className="muted small">No data reported for this section.</p>
  )
}
```

The final import set contains only symbols used by this module and passes `noUnusedLocals`.

- [ ] **Step 4: Leave RunsPage responsible only for run history and update the lazy route**

Delete `loadRunResults`, `RunDetailPage`, and `Breakdown` from `RunsPage.tsx`, retaining the existing `RunsPage` function unchanged. Its complete remaining import set is:

```tsx
import { Link, useNavigate } from "react-router-dom"
import { Layers3, Plus } from "lucide-react"
import { Button } from "@/components/ui/button"
import { Card, CardHeader, CardTitle } from "@/components/ui/card"
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table"
import { EmptyState, ErrorState, LoadingState, PageHeader, StatusBadge } from "@/components/shared/workspace-ui"
import { useResource } from "@/hooks/use-resource"
import { useWorkspace } from "@/lib/workspace"
import { useCopy } from "@/lib/locale"
import { dateLabel, humanize, timeLabel } from "@/lib/format"
import type { Run } from "@/lib/types"
```

Update `App.tsx`:

```tsx
const RunDetailPage = lazy(() =>
  import("@/features/runs/RunDetailPage").then((module) => ({
    default: module.RunDetailPage,
  }))
)
```

- [ ] **Step 5: Verify the runs slice and route references**

Run:

```bash
cd employee-frontend
npx vitest run src/features/runs/run-results.test.ts src/features/runs/NewBatchPage.test.tsx
npm run lint
rg -n "RunDetailPage|loadRunResults|RUN_RESULT_CONCURRENCY" src --glob '*.{ts,tsx}'
```

Expected: all 7 focused tests pass and lint exits zero. `RunDetailPage` is defined only in `RunDetailPage.tsx` and imported only by `App.tsx`; `loadRunResults` is defined only in `run-results.ts`, consumed by `RunDetailPage.tsx`, and tested by `run-results.test.ts`. The existing 2500 ms running poll and `0` terminal poll arguments remain unchanged.

- [ ] **Step 6: Review the runs diff**

Run:

```bash
cd employee-frontend
git diff -- src/App.tsx src/features/runs
git status --short
```

Expected: only the route split, bounded loader, and its tests appear; JSX and polling behavior are otherwise unchanged. No commit is created.

### Task 4: Extract and test the pure queue projection

**Files:**
- Create: `employee-frontend/src/features/queue/queue-projection.ts`
- Create: `employee-frontend/src/features/queue/queue-projection.test.ts`
- Modify: `employee-frontend/src/features/queue/QueuePage.tsx:1,56-115`
- Test: `employee-frontend/src/features/queue/queue-projection.test.ts`

**Interfaces:**
- Consumes: `Result[]` already loaded by `loadQueue`, and the current tab/team/category/search/page state.
- Produces: `QueueTab`, `QueueFilters`, `QueueProjection`, and `projectQueue(rows: Result[], filters: QueueFilters, requestedPage: number, pageSize?: number): QueueProjection`; `QueuePage` continues to render the same markup.

- [ ] **Step 1: Write failing projection tests**

Create `queue-projection.test.ts`:

```ts
import { expect, it } from "vitest"
import type { Result } from "@/lib/types"
import { projectQueue, type QueueFilters } from "./queue-projection"

const filters = (patch: Partial<QueueFilters> = {}): QueueFilters => ({
  tab: "all",
  team: "all",
  category: "all",
  search: "",
  ...patch,
})

function row(id: number, patch: Partial<Result> = {}): Result {
  return {
    id,
    ticket_id: id,
    run_id: 1,
    ticket: {
      id,
      external_id: `T-${id}`,
      text: `ticket ${id}`,
      received_at: "2026-10-12T10:00:00Z",
      channel: "app",
      customer_phone: null,
    },
    category: "failed_transfer",
    category_confidence: 0.8,
    category_probs: {},
    priority: "P2",
    priority_confidence: null,
    flags: {},
    classifier_path: "jev",
    extracted: {},
    lookup_status: "not_applicable",
    matched_txn_ref: null,
    team: "Payments Ops",
    escalated: false,
    escalation_reasons: [],
    escalation_note: null,
    draft_text: null,
    final_text: null,
    citations: [],
    agent_trace: [],
    status: "pending_review",
    error: null,
    latency_ms: 1,
    cost_usd: 0,
    updated_at: "2026-10-12T10:00:00Z",
    ...patch,
  }
}

it("groups approved and edited rows in counts, filters, and distribution", () => {
  const rows = [
    row(1, { status: "approved" }),
    row(2, { status: "edited" }),
    row(3, { status: "escalated", category: "login_access" }),
    row(4, { category: "login_access" }),
    row(5, { status: "processing", category: null }),
  ]
  const all = projectQueue(rows, filters(), 0)
  const approved = projectQueue(rows, filters({ tab: "approved" }), 0)

  expect(all.counts).toEqual({
    all: 5,
    pending_review: 1,
    escalated: 1,
    approved: 2,
    processing: 1,
  })
  expect(approved.filtered.map((item) => item.id)).toEqual([1, 2])
  expect(all.distribution).toEqual([
    ["failed_transfer", 2],
    ["login_access", 2],
    ["other", 1],
  ])
})

it("applies tab, team, category, and case-insensitive search together", () => {
  const first = row(1)
  const rows = [
    {
      ...first,
      ticket: { ...first.ticket, text: "Refund pending", external_id: "ZC-1001" },
    },
    row(2),
    row(3, { team: "Disputes" }),
    row(4, { status: "approved" }),
  ]
  const view = projectQueue(rows, filters({
    tab: "pending_review",
    team: "Payments Ops",
    category: "failed_transfer",
    search: "zc-1001",
  }), 0)
  expect(view.filtered.map((item) => item.id)).toEqual([1])
  expect(view.visible.map((item) => item.id)).toEqual([1])
})

it("sorts by the existing priority ordering without mutating input rows", () => {
  const rows = [
    row(1, { priority: null }),
    row(2, { priority: "P2" }),
    row(3, { priority: "P1" }),
  ]
  const originalOrder = rows.map((item) => item.id)
  const view = projectQueue(rows, filters(), 0)
  expect(view.filtered.map((item) => item.id)).toEqual([3, 2, 1])
  expect(rows.map((item) => item.id)).toEqual(originalOrder)
})

it("clamps the requested page and returns the final visible slice", () => {
  const rows = Array.from({ length: 12 }, (_, index) => row(index + 1))
  const view = projectQueue(rows, filters(), 99)
  expect(view.lastPage).toBe(1)
  expect(view.currentPage).toBe(1)
  expect(view.visible.map((item) => item.id)).toEqual([9, 10, 11, 12])
})

it("clamps empty and no-match projections to page zero", () => {
  const empty = projectQueue([], filters(), 99)
  const noMatch = projectQueue([row(1)], filters({ search: "missing" }), 99)
  for (const view of [empty, noMatch]) {
    expect(view.lastPage).toBe(0)
    expect(view.currentPage).toBe(0)
    expect(view.filtered).toEqual([])
    expect(view.visible).toEqual([])
  }
})
```

Run:

```bash
cd employee-frontend
npx vitest run src/features/queue/queue-projection.test.ts
```

Expected: FAIL because `./queue-projection` does not exist.

- [ ] **Step 2: Implement the projection with the current filtering and sorting semantics**

Create `src/features/queue/queue-projection.ts`:

```ts
import type { Result } from "@/lib/types"

export type QueueTab =
  | "all"
  | "pending_review"
  | "escalated"
  | "processing"
  | "approved"

export type QueueFilters = {
  tab: QueueTab
  team: string
  category: string
  search: string
}

export type QueueProjection = {
  counts: Record<QueueTab, number>
  filtered: Result[]
  visible: Result[]
  distribution: [string, number][]
  currentPage: number
  lastPage: number
}

export function projectQueue(
  rows: Result[],
  filters: QueueFilters,
  requestedPage: number,
  pageSize = 8,
): QueueProjection {
  const counts: Record<QueueTab, number> = {
    all: rows.length,
    pending_review: rows.filter((row) => row.status === "pending_review").length,
    escalated: rows.filter((row) => row.status === "escalated").length,
    approved: rows.filter((row) => ["approved", "edited"].includes(row.status)).length,
    processing: rows.filter((row) => row.status === "processing").length,
  }
  const filtered = rows
    .filter((row) =>
      (filters.tab === "all" ||
        (filters.tab === "approved"
          ? ["approved", "edited"].includes(row.status)
          : row.status === filters.tab)) &&
      (filters.team === "all" || row.team === filters.team) &&
      (filters.category === "all" || row.category === filters.category) &&
      `${row.ticket.text} ${row.ticket.external_id} ${row.ticket.display_name || ""}`
        .toLowerCase()
        .includes(filters.search.toLowerCase()),
    )
    .sort((a, b) => (a.priority || "P9").localeCompare(b.priority || "P9"))
  const lastPage = Math.max(0, Math.ceil(filtered.length / pageSize) - 1)
  const currentPage = Math.min(requestedPage, lastPage)
  const visible = filtered.slice(
    currentPage * pageSize,
    currentPage * pageSize + pageSize,
  )
  const distribution = Object.entries(
    rows.reduce<Record<string, number>>((acc, row) => {
      const key = row.category || "other"
      acc[key] = (acc[key] || 0) + 1
      return acc
    }, {}),
  )
    .sort((a, b) => b[1] - a[1])
    .slice(0, 5)

  return { counts, filtered, visible, distribution, currentPage, lastPage }
}
```

Run:

```bash
cd employee-frontend
npx vitest run src/features/queue/queue-projection.test.ts
```

Expected: all 5 projection tests pass.

- [ ] **Step 3: Replace derived QueuePage logic with the tested projection**

Add this import:

```ts
import { projectQueue, type QueueTab } from "./queue-projection"
```

Type the tab state and replace the current counts/filtered/page/distribution blocks at `QueuePage.tsx:77-115` with:

```tsx
  const [tab, setTab] = useState<QueueTab>("all"),
    [search, setSearch] = useState("")
  const [team, setTeam] = useState("all"),
    [category, setCategory] = useState("all"),
    [page, setPage] = useState(0)
  const query = useResource<{ items: Result[]; total: number }>(
    `/results?limit=500${runId ? `&run_id=${runId}` : ""}`,
    workspace.revision,
    10000,
    loadQueue
  )
  const rows = query.data?.items || EMPTY_RESULTS
  const { counts, filtered, visible, distribution, currentPage, lastPage } = useMemo(
    () => projectQueue(rows, { tab, team, category, search }, page),
    [rows, tab, team, category, search, page],
  )
```

Keep the existing `8` values in display-range arithmetic unchanged; the projection's default page size is also 8. Do not alter table, sidebar, or pagination JSX.

- [ ] **Step 4: Run queue and full regression checks**

Run:

```bash
cd employee-frontend
npx vitest run src/features/queue/queue-projection.test.ts src/lib/api.test.ts
npm test
npm run lint
```

Expected: all 7 focused tests pass, the full employee suite passes, and lint exits zero. The two known fixture errors may remain only in standalone TypeScript verification.

- [ ] **Step 5: Review the queue diff**

Run:

```bash
cd employee-frontend
git diff -- src/features/queue
git status --short
```

Expected: only the pure projection, its tests, and the `QueuePage` wiring appear; no visual markup changes. No commit is created.

### Task 5: Extract presentational DocumentList and KnowledgeReadiness components

**Files:**
- Create: `employee-frontend/src/features/knowledge/DocumentList.tsx`
- Create: `employee-frontend/src/features/knowledge/KnowledgeReadiness.tsx`
- Create: `employee-frontend/src/features/knowledge/knowledge-view.test.tsx`
- Modify: `employee-frontend/src/features/knowledge/KnowledgePage.tsx`
- Test: `employee-frontend/src/features/knowledge/knowledge-view.test.tsx`
- Test: `employee-frontend/src/features/knowledge/index-lifecycle.test.ts` unchanged

**Interfaces:**
- Consumes: `KnowledgeDocument`, `Health`, `useKnowledgeLibrary` return values, and the page's existing `indexDocument`, `setSelectedId`, and `setRemove` mutation/state functions.
- Produces: `DocumentList(props: DocumentListProps)` and `KnowledgeReadiness({ health, configured }: { health: Health | null; configured: boolean })`; no mutation or polling ownership moves out of `KnowledgePage`.

- [ ] **Step 1: Write failing knowledge-view rendering tests**

Create `knowledge-view.test.tsx`:

```tsx
import { renderToStaticMarkup } from "react-dom/server"
import { afterEach, beforeEach, expect, it } from "vitest"
import type { Health, KnowledgeDocument } from "@/lib/types"
import { getLocale, setLocale } from "@/lib/locale"
import { DocumentList, type DocumentListProps } from "./DocumentList"
import { KnowledgeReadiness } from "./KnowledgeReadiness"

const originalLocale = getLocale()

beforeEach(() => setLocale("en"))
afterEach(() => setLocale(originalLocale))

function knowledgeDocument(patch: Partial<KnowledgeDocument> = {}): KnowledgeDocument {
  return {
    id: 7,
    filename: "policy.md",
    size: 40,
    status: "awaiting_indexing",
    content_type: "text/markdown",
    sha256: "synthetic",
    created_at: "2026-10-17T00:00:00Z",
    updated_at: "2026-10-17T00:00:00Z",
    category_tags: [],
    chunk_count: 0,
    embedding_model: null,
    embedding_dimensions: null,
    chunking_version: null,
    indexed_at: null,
    error: null,
    cost_usd: 0,
    ...patch,
  }
}

function listProps(patch: Partial<DocumentListProps> = {}): DocumentListProps {
  return {
    documents: [knowledgeDocument()],
    storedCount: 1,
    search: "",
    loading: false,
    busy: false,
    configured: true,
    selectedId: null,
    pendingIds: [],
    canRequestIndex: () => true,
    onSearchChange: () => {},
    onRefresh: () => {},
    onIndex: () => {},
    onInspect: () => {},
    onDelete: () => {},
    ...patch,
  }
}

function health(patch: Partial<Health> = {}): Health {
  return {
    database: "connected",
    configured_modes: ["jev"],
    capabilities: { drafting: true, rag_indexing: true, evaluation: false },
    ...patch,
  }
}

it("renders a pending failed document as a recoverable previous attempt", () => {
  const document = knowledgeDocument({ status: "failed", error: "Embedding unavailable" })
  const html = renderToStaticMarkup(<DocumentList {...listProps({
    documents: [document],
    pendingIds: [7],
  })} />)
  expect(html).toContain("Request indexing again")
  expect(html).toContain("Previous attempt:")
  expect(html).toContain("Embedding unavailable")
  expect(html).toContain("Request accepted; waiting for the indexing worker")
})

it("keeps active and terminal document actions distinct", () => {
  const active = knowledgeDocument({ id: 1, status: "indexing" })
  const failed = knowledgeDocument({ id: 2, filename: "failed.md", status: "failed" })
  const indexed = knowledgeDocument({ id: 3, filename: "indexed.md", status: "indexed" })
  const activeHtml = renderToStaticMarkup(<DocumentList {...listProps({
    documents: [active],
    pendingIds: [1],
    canRequestIndex: () => false,
  })} />)
  const terminalHtml = renderToStaticMarkup(<DocumentList {...listProps({
    documents: [failed, indexed],
    storedCount: 2,
  })} />)

  expect(activeHtml).toContain("Index pending")
  expect(activeHtml).not.toContain("Request indexing again")
  expect(terminalHtml).toContain("Retry index")
  expect(terminalHtml).toContain("Reindex")
  expect(terminalHtml).toContain("/api/knowledge/3/download")
})

it("keeps missing and disabled readiness explicit", () => {
  const missing = renderToStaticMarkup(<KnowledgeReadiness health={null} configured={false} />)
  const disabled = renderToStaticMarkup(<KnowledgeReadiness
    configured={false}
    health={health({
      knowledge: {
        enabled: false,
        configured: false,
        ready: false,
        status: "disabled",
        indexed_document_count: 0,
        embedding_model: "embed-model",
        embedding_dimensions: 1536,
      },
    })}
  />)

  expect(missing).toContain("Readiness is unavailable")
  expect(disabled).toContain("Knowledge retrieval is disabled")
  expect(disabled).toContain("0 searchable documents")
  expect(disabled).toContain("disabled")
})

it("renders configured ready health without changing its status content", () => {
  const html = renderToStaticMarkup(<KnowledgeReadiness
    configured={true}
    health={health({
      knowledge: {
        enabled: true,
        configured: true,
        ready: true,
        status: "ready",
        indexed_document_count: 2,
        embedding_model: "embed-model",
        embedding_dimensions: 1536,
      },
    })}
  />)
  expect(html).toContain("2 searchable documents")
  expect(html).toContain("ready")
  expect(html).toContain("embed-model")
  expect(html).toContain("1536 dimensions")
})
```

Run:

```bash
cd employee-frontend
npx vitest run src/features/knowledge/knowledge-view.test.tsx
```

Expected: FAIL because `./DocumentList` does not exist.

- [ ] **Step 2: Extract DocumentList with the existing markup and action derivation**

Create `src/features/knowledge/DocumentList.tsx`:

```tsx
import { Download, FileText, RefreshCw, Search, Trash2 } from "lucide-react"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Input } from "@/components/ui/input"
import { EmptyState, LoadingState, StatusBadge } from "@/components/shared/workspace-ui"
import { fill, getLocale, useCopy } from "@/lib/locale"
import { dateLabel, sizeLabel } from "@/lib/format"
import type { KnowledgeDocument } from "@/lib/types"

export type DocumentListProps = {
  documents: KnowledgeDocument[]
  storedCount: number
  search: string
  loading: boolean
  busy: boolean
  configured: boolean
  selectedId: number | null
  pendingIds: number[]
  canRequestIndex: (document: KnowledgeDocument) => boolean
  onSearchChange: (value: string) => void
  onRefresh: () => void
  onIndex: (document: KnowledgeDocument) => void
  onInspect: (document: KnowledgeDocument) => void
  onDelete: (document: KnowledgeDocument) => void
}

export function DocumentList({
  documents,
  storedCount,
  search,
  loading,
  busy,
  configured,
  selectedId,
  pendingIds,
  canRequestIndex,
  onSearchChange,
  onRefresh,
  onIndex,
  onInspect,
  onDelete,
}: DocumentListProps) {
  const text = useCopy().knowledge
  const statusLabels = useCopy().status as Record<string, string>
  return (
    <Card>
      <CardHeader>
        <CardTitle className="section-title">
          <FileText size={15} />
          {text.documents}
          <span className="muted small">
            {fill(text.shown, { shown: documents.length, stored: storedCount })}
          </span>
        </CardTitle>
        <Button variant="ghost" size="sm" disabled={busy} onClick={onRefresh}>
          <RefreshCw size={14} />
          {text.refresh}
        </Button>
      </CardHeader>
      <CardContent>
        <div className="input-with-icon">
          <Search size={16} />
          <Input
            aria-label={text.searchDocuments}
            placeholder={text.findByName}
            value={search}
            onChange={(event) => onSearchChange(event.target.value)}
          />
        </div>
        {loading ? (
          <LoadingState />
        ) : documents.length ? (
          <div className="document-list">
            {documents.map((doc) => {
              const pending = pendingIds.includes(doc.id)
              const active = pending || doc.status === "indexing"
              const requestable = canRequestIndex(doc)
              const indexAction =
                pending && requestable
                  ? text.requestAgain
                  : active
                    ? text.indexPending
                    : doc.status === "failed"
                      ? text.retryIndex
                      : doc.status === "indexed"
                        ? text.reindex
                        : text.indexDocument
              return (
                <div className="document-item" key={doc.id}>
                  <span className="document-icon">
                    <FileText size={16} />
                  </span>
                  <div className="document-body">
                    <div className="document-heading">
                      <strong>{doc.filename}</strong>
                      <StatusBadge
                        status={pending && doc.status !== "indexing" ? "index_requested" : doc.status}
                      />
                      <span className="muted small">
                        {fill(text.passagesCount, { count: doc.chunk_count })}
                      </span>
                    </div>
                    <small>
                      {sizeLabel(doc.size)} · {fill(text.uploaded, { date: dateLabel(doc.created_at) })}
                    </small>
                    {pending && doc.status !== "indexing" && (
                      <p className="field-help">
                        {fill(text.pendingHelp, {
                          status: statusLabels[doc.status] || doc.status,
                        })}{" "}
                        {requestable && text.pendingRetry}
                      </p>
                    )}
                    {doc.error && (
                      <p className="document-error">
                        {pending ? text.previousAttempt : text.indexingFailed}
                        {doc.error} {!active && text.checkAndRetry}
                      </p>
                    )}
                    {doc.status === "awaiting_indexing" && !pending && (
                      <p className="field-help">
                        {text.awaitingHelp}{" "}
                        {configured ? text.awaitingConfigured : text.awaitingUnconfigured}
                      </p>
                    )}
                    {doc.embedding_model && (
                      <small>
                        {fill(text.dimensions, {
                          model: doc.embedding_model,
                          count: doc.embedding_dimensions ?? "",
                        })}
                        {doc.indexed_at
                          ? ` · ${fill(text.indexedOn, { date: dateLabel(doc.indexed_at) })}`
                          : ""}
                      </small>
                    )}
                    {!!doc.category_tags.length && (
                      <small>
                        {fill(text.categories, {
                          list: doc.category_tags.join(getLocale() === "ar" ? "، " : ", "),
                        })}
                      </small>
                    )}
                  </div>
                  <div className="document-actions">
                    <Button
                      variant="outline"
                      size="sm"
                      disabled={busy || !requestable || !configured}
                      onClick={() => onIndex(doc)}
                      aria-label={`${indexAction}: ${doc.filename}`}
                    >
                      {indexAction}
                    </Button>
                    <Button
                      variant="ghost"
                      size="sm"
                      aria-pressed={selectedId === doc.id}
                      onClick={() => onInspect(doc)}
                    >
                      {text.inspect}
                      <span className="sr-only">: {doc.filename}</span>
                    </Button>
                    <Button
                      variant="ghost"
                      size="icon"
                      nativeButton={false}
                      render={<a href={`/api/knowledge/${doc.id}/download`} />}
                      aria-label={fill(text.download, { name: doc.filename })}
                    >
                      <Download size={16} />
                    </Button>
                    <Button
                      variant="ghost"
                      size="icon"
                      aria-label={fill(text.deleteNamed, { name: doc.filename })}
                      disabled={busy || active}
                      onClick={() => onDelete(doc)}
                    >
                      <Trash2 size={15} />
                    </Button>
                  </div>
                </div>
              )
            })}
          </div>
        ) : (
          <EmptyState
            title={search ? text.noMatch : text.emptyLibrary}
            description={text.emptyHint}
          />
        )}
      </CardContent>
    </Card>
  )
}
```

- [ ] **Step 3: Extract KnowledgeReadiness with unchanged lifecycle and health presentation**

Create `src/features/knowledge/KnowledgeReadiness.tsx`:

```tsx
import { ArrowRight, Database, Info } from "lucide-react"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { fill, useCopy } from "@/lib/locale"
import type { Health } from "@/lib/types"

export function KnowledgeReadiness({
  health,
  configured,
}: {
  health: Health | null
  configured: boolean
}) {
  const text = useCopy().knowledge
  const readinessStatus: Record<string, string> = {
    disabled: text.statusDisabled,
    unconfigured: text.statusUnconfigured,
    ready: text.statusReady,
    indexing: text.statusIndexing,
    failed: text.statusFailed,
    empty: text.statusEmpty,
  }
  return (
    <aside className="evidence-stack">
      <Card>
        <CardHeader>
          <CardTitle className="section-title">
            <Database size={15} />
            {text.lifecycle}
          </CardTitle>
        </CardHeader>
        <CardContent>
          <ol className="document-lifecycle">
            <li>
              <span>1</span>
              <div>
                <strong>{text.stepStore}</strong>
                <p>{text.stepStoreBody}</p>
              </div>
              <BadgeLabel text={text.available} />
            </li>
            <li>
              <span>2</span>
              <div>
                <strong>{text.stepEmbed}</strong>
                <p>{text.stepEmbedBody}</p>
              </div>
              <BadgeLabel text={configured ? text.configured : text.needsSetup} />
            </li>
            <li>
              <span>3</span>
              <div>
                <strong>{text.stepCite}</strong>
                <p>{text.stepCiteBody}</p>
              </div>
              <BadgeLabel text={health?.knowledge?.ready ? text.ready : text.needsIndex} />
            </li>
          </ol>
        </CardContent>
      </Card>
      <Card className="knowledge-readiness">
        <CardHeader>
          <CardTitle className="section-title">{text.readiness}</CardTitle>
        </CardHeader>
        <CardContent>
          <p className="muted small">
            {health?.knowledge
              ? fill(text.searchable, {
                  count: health.knowledge.indexed_document_count,
                  status: readinessStatus[health.knowledge.status] || health.knowledge.status,
                })
              : text.readinessUnavailable}
          </p>
          {health?.knowledge && (
            <>
              <p className="field-help">
                {fill(text.dimensions, {
                  model: health.knowledge.embedding_model,
                  count: health.knowledge.embedding_dimensions,
                })}
              </p>
              <p className="field-help">
                {!health.knowledge.enabled
                  ? text.retrievalDisabled
                  : !configured
                    ? text.configureProvider
                    : health.knowledge.ready
                      ? text.passagesReady
                      : text.indexFirst}
              </p>
              <p className="field-help">
                {health.drafting?.credential_check_configured
                  ? text.credentialOn
                  : text.credentialOff}{" "}
                {text.readinessScope}
              </p>
            </>
          )}
        </CardContent>
      </Card>
      <div className="knowledge-note">
        <Info size={16} />
        <div>
          <strong>{text.noteTitle}</strong>
          <p>{text.noteBody}</p>
          <span>
            {text.flowUpload} <ArrowRight size={13} />
            {text.flowIndex} <ArrowRight size={13} />
            {text.flowGround}
          </span>
        </div>
      </div>
    </aside>
  )
}

function BadgeLabel({ text }: { text: string }) {
  return <small className="lifecycle-state">{text}</small>
}
```

- [ ] **Step 4: Wire the components without moving mutations or polling**

Add these imports to `KnowledgePage.tsx`:

```tsx
import { DocumentList } from "./DocumentList"
import { KnowledgeReadiness } from "./KnowledgeReadiness"
```

Remove the old `statusLabels` and `readinessStatus` constants and the old `BadgeLabel` helper. Replace the document card at current lines 210-369 with:

```tsx
          <DocumentList
            documents={documents}
            storedCount={query.documents.length}
            search={search}
            loading={query.loading}
            busy={busy}
            configured={configured}
            selectedId={selectedId}
            pendingIds={query.pendingIds}
            canRequestIndex={query.canRequestIndex}
            onSearchChange={setSearch}
            onRefresh={query.refresh}
            onIndex={(doc) => void indexDocument(doc)}
            onInspect={(doc) => setSelectedId(doc.id)}
            onDelete={setRemove}
          />
```

Replace the readiness aside at current lines 372-469 with:

```tsx
        <KnowledgeReadiness health={workspace.health} configured={configured} />
```

Keep `KnowledgeSearch`, `ConfirmDialog`, `upload`, `indexDocument`, `deleteDocument`, and `useKnowledgeLibrary` calls unchanged. Remove imports that are now exclusive to the extracted components: `Download`, `FileText`, `Search`, `RefreshCw`, `Database`, `ArrowRight`, `Info`, `Input`, `CardHeader`, `CardTitle`, `EmptyState`, `LoadingState`, `StatusBadge`, `getLocale`, `dateLabel`, and `sizeLabel`; retain `BookOpen`, `FileUp`, `Card`, `CardContent`, and all mutation/dialog imports actually used by the page.

- [ ] **Step 5: Run knowledge-view and unchanged lifecycle tests**

Run:

```bash
cd employee-frontend
npx vitest run src/features/knowledge/knowledge-view.test.tsx src/features/knowledge/index-lifecycle.test.ts
npm run lint
```

Expected: all 4 new view tests and all existing index-lifecycle tests pass; lint exits zero. No changes are made to `index-lifecycle.ts`, `use-knowledge-library.ts`, or its test expectations.

- [ ] **Step 6: Review the knowledge diff**

Run:

```bash
cd employee-frontend
git diff -- src/features/knowledge
git status --short
```

Expected: only presentational extraction, wiring, and focused tests appear; mutations, polling, storage, class names, and user flows are unchanged. No commit is created.

### Task 6: Repair ExtractedField fixtures and make standalone typecheck real

**Files:**
- Modify: `employee-frontend/src/features/review/ticket-flow-view.test.tsx:26-29`
- Modify: `employee-frontend/package.json:12`
- Test: `employee-frontend/src/features/review/ticket-flow-view.test.tsx`

**Interfaces:**
- Consumes: `ExtractedField` from `src/lib/types.ts:15-23` and TypeScript project references in `tsconfig.json`.
- Produces: Two type-complete test fixtures and `npm run typecheck` executing `tsc -b`; no production type changes.

- [ ] **Step 1: Reproduce the recorded defect immediately before the fix**

Run:

```bash
cd employee-frontend
./node_modules/.bin/tsc -p tsconfig.app.json --noEmit --incremental false
npm run typecheck
```

Expected: the direct project check fails with exactly TS2739 at `ticket-flow-view.test.tsx:27-28`, naming missing `start`, `end`, `method`, and `confidence`; the old `npm run typecheck` exits zero without checking the referenced project.

- [ ] **Step 2: Complete both fixtures without weakening the contract**

Replace the fixture block with:

```ts
    extracted: {
      amount: {
        value: 35000,
        currency: "IQD",
        span: "35,000 دينار",
        start: null,
        end: null,
        method: "test",
        confidence: 1,
      },
      date: {
        value: "01-10-2026",
        span: "يوم الخميس",
        start: null,
        end: null,
        method: "test",
        confidence: 1,
      },
    },
```

Do not change `src/lib/types.ts`, add `@ts-expect-error`, or suppress any compiler check.

- [ ] **Step 3: Make the standalone script build referenced projects**

Change only the `typecheck` script in `package.json`:

```json
{
  "scripts": {
    "typecheck": "tsc -b"
  }
}
```

Do not regenerate the lockfile for a script-only change.

- [ ] **Step 4: Verify the defect fix and active TicketFlow coverage**

Run:

```bash
cd employee-frontend
npm run typecheck
npx vitest run src/features/review/ticket-flow-view.test.tsx
```

Expected: `tsc -b` checks application, tests, and Vite configuration and exits zero; all 3 active TicketFlow view tests pass.

- [ ] **Step 5: Review the baseline-repair diff**

Run:

```bash
cd employee-frontend
git diff -- src/features/review/ticket-flow-view.test.tsx package.json
git status --short
```

Expected: only the two fixture completions, migrated active coverage from Task 2, and the one-script change appear. No commit is created.

### Task 7: Repair employee README paths/test-count guidance and run final acceptance

**Files:**
- Modify: `employee-frontend/README.md:10,35,79-102,120-135`
- Test: No test-file changes; run the complete employee verification matrix

**Interfaces:**
- Consumes: Final module layout from Tasks 2-5 and the verification commands required by spec §10.
- Produces: Current `employee-frontend` setup paths, a current module map, and command-based verification guidance without a hard-coded frontend test count.

- [ ] **Step 1: Update current setup paths and verification commands**

Replace both `customer-support-ui` occurrences with `employee-frontend`, yielding:

```text
/home/cvzmh_saif/dev/zaincash-support/employee-frontend
```

and:

```bash
cd employee-frontend
npm ci
npm run dev -- --port 5173
```

Update the frontend verification block to:

```bash
npm run typecheck
npm test
npm run lint
npm run build
# From the repo root, with the database service running:
uv --directory backend run pytest -q
uv --directory backend run ruff check app tests
```

- [ ] **Step 2: Keep the module map aligned with the final source layout**

Replace the relevant feature/lib entries with:

```text
    queue/                        Pure queue projection, filters, pagination and triage overview
    review/                       Source evidence, reply editor, audit and active stage/tool flow
    runs/                         Run history, RunDetailPage and bounded result loading
    knowledge/                    Index lifecycle, document/readiness views, passage inspection and search
```

Remove the deleted `stages.ts` line from the map. Leave the remaining map entries unchanged.

- [ ] **Step 3: Remove the stale hard-coded frontend count**

In the final-evidence paragraph, replace the sentence beginning `**25 frontend tests**` with:

```markdown
For current frontend verification, run the commands above; this guide does not duplicate a test count that can become outdated.
```

Preserve dated verification links and historical records. Do not edit the repository-root `README.md`.

- [ ] **Step 4: Check documentation and deleted references**

Run from the repository root:

```bash
rg -n "customer-support-ui|\*\*25 frontend tests\*\*|lib/stages|PipelineTrace|trace-facts|mermaid" employee-frontend/README.md employee-frontend/src employee-frontend/package.json
```

Expected: no matches. Historical documents outside the current employee README are not modified by this plan.

- [ ] **Step 5: Run the complete employee frontend acceptance matrix**

Run:

```bash
cd employee-frontend
npm run typecheck
npm test
npm run lint
npm run build
```

Expected: all four commands exit zero. Typechecking includes application, tests, and Vite configuration; every retained test plus the new active TicketFlow, 6 loader, 5 queue-projection, and 4 knowledge-view tests passes; production Vite build completes after `tsc -b`.

- [ ] **Step 6: Perform the final full diff and status review**

Run from the repository root:

```bash
git diff --check
git diff -- employee-frontend
git status --short
```

Expected: no whitespace errors; only the intended employee source, test, configuration, lockfile, and current README changes appear. Confirm there are no visual-only edits, no `ReviewEditor` extraction, no generated primitive cleanup beyond the two approved files, no type suppressions, no secrets, no commits, and no changes to the user's pre-existing root `README.md` modification or unrelated files.
