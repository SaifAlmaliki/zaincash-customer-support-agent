# AI Usage and Performance Dashboard Implementation Plan — Part 2 of 2 (frontend, docs, verification)

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Rebuild `/evaluation` as the single, fully translated page for AI cost and response time: headline cards, per-process and per-model tables, a daily trend, every ticket with its cost split and AI time, a per-ticket call timeline, and costs not tied to a ticket. Translate the remaining English on the Runs and Run detail pages.

**Architecture:** Pure helpers in `src/features/evaluation/usage-view.ts` turn API data into display values (query strings, period ranges, share bars, waterfall geometry). Small presentational components render them; `EvaluationPage` owns filter state and loads `/api/ai-usage/*` through `useResource`. All text lives in `src/locales/{en,ar}.json`.

**Tech Stack:** React 19, TypeScript, Vite, base-ui/shadcn components in `src/components/ui`, lucide icons, Vitest with `renderToStaticMarkup` (no DOM testing library in this app; interaction logic is tested through pure helpers and props).

**Spec:** `docs/superpowers/specs/2026-11-14-ai-usage-dashboard-design.md` §5. Part 1 (`2026-11-14-ai-usage-dashboard.md`) provides the API; its response shapes (Task 10 "Interfaces") are the contract for this part.

## Global Constraints

- Commands run from `employee-frontend/`: `npm test`, `npm run lint`, `npm run typecheck`, `npm run build`.
- Every visible string comes from `en.json` / `ar.json`; both keep identical keys (`src/locales/locales.test.ts`).
- Model IDs, ticket IDs and run numbers render inside `<bdi dir="ltr">`; numbers use Latin digits (existing formatters).
- `null` values render as "—", never 0. Costs show their source: `est.` marker for estimates, **Local · $0** for local, "Price unknown" for unknown.
- Process names come from `evaluation.processes.*`, in this order: intake, classify, extract, draft, draft_search, credential_check, kb_index, kb_search, probe.
- The page refreshes every 30 seconds and on the refresh button; it does not poll faster.
- No new npm dependencies (the trend chart is plain SVG).

## Deviation from the spec

The spec lists an `aiUsageApi` client in `src/lib/api.ts`. All three endpoints are plain GETs, so the page loads them with the existing `useResource(path)` hook instead; no client object is added (YAGNI).

## Review Focus

Same as Part 1. The frontend parts are pinned by `UsageHeadline renders dashes for an empty period` (Task 14) and `TicketCostTable marks rows without recorded detail` (Task 15).

---

### Task 11: Locale parity test and translated Runs pages

**Files:**
- Create: `employee-frontend/src/locales/locales.test.ts`
- Modify: `employee-frontend/src/locales/en.json`, `employee-frontend/src/locales/ar.json` (add `runs`, `runDetail`)
- Modify: `employee-frontend/src/features/runs/RunsPage.tsx` (export `RunsTable`)
- Modify: `employee-frontend/src/features/runs/RunDetailPage.tsx` (export `RunDetailView`)
- Test: `employee-frontend/src/features/runs/runs-i18n.test.tsx`

**Interfaces:**
- Produces: `RunsTable({ runs }: { runs: Run[] })`; `RunDetailView({ run, results, resultsError, resultsLoading })`.

- [ ] **Step 1: Write the parity test**

Create `employee-frontend/src/locales/locales.test.ts`:

```ts
import { expect, it } from "vitest"
import ar from "./ar.json"
import en from "./en.json"

function entries(value: unknown, prefix = ""): [string, unknown][] {
  if (value && typeof value === "object" && !Array.isArray(value))
    return Object.entries(value).flatMap(([key, child]) =>
      entries(child, prefix ? `${prefix}.${key}` : key)
    )
  return [[prefix, value]]
}

it("Arabic and English define exactly the same keys", () => {
  expect(entries(ar).map(([k]) => k).sort()).toEqual(entries(en).map(([k]) => k).sort())
})

it("has no empty translations", () => {
  for (const [key, value] of [...entries(ar), ...entries(en)])
    expect(typeof value === "string" && value.trim().length > 0, key).toBe(true)
})
```

Run: `npm test -- src/locales/locales.test.ts` — Expected: PASS (it guards every later task).

- [ ] **Step 2: Add the copy**

Add to `en.json` (top level, after `"batch"`):

```json
  "runs": {
    "newBatch": "New batch",
    "history": "Run history",
    "count": "{count} runs",
    "emptyTitle": "Let’s clear the next batch",
    "emptyBody": "Add a CSV or JSON ticket file and follow the results here.",
    "createFirst": "Create your first batch",
    "colBatch": "Batch",
    "colStarted": "Started · Baghdad",
    "colClassifier": "Classifier",
    "colTickets": "Tickets",
    "colStatus": "Status",
    "colCost": "Estimated cost",
    "batchName": "Batch #{id}",
    "classifierJev": "Jev",
    "classifierCascade": "Jev then Gemini"
  },
  "runDetail": {
    "back": "All pipeline runs",
    "notFound": "Run not found",
    "notFoundBody": "Choose a run from the pipeline history.",
    "started": "Started {date} at {time} Baghdad · {mode}",
    "modeCascade": "Jev with Gemini fallback",
    "export": "Export summary",
    "review": "Review tickets",
    "running": "Preparing your tickets",
    "interrupted": "Batch interrupted",
    "finished": "Batch processing finished",
    "progress": "{processed} of {total} tickets processed",
    "progressLabel": "Batch progress",
    "degraded": "Jev was unavailable for part of this run. Gemini fallback is recorded in the results.",
    "processed": "Processed",
    "processedDetail": "Of {total} submitted tickets",
    "needsReview": "Needs human review",
    "needsReviewDetail": "Review the escalation notes",
    "latency": "Median latency",
    "latencyDetail": "Per processed ticket",
    "cost": "Estimated run cost",
    "costDetail": "Based on recorded token usage",
    "issues": "Issue breakdown",
    "reasons": "Escalation reasons",
    "noData": "No data reported for this section.",
    "stepsPending": "Steps appear here when a ticket finishes.",
    "noTickets": "No processed ticket to show yet."
  }
```

Add to `ar.json` in the same place:

```json
  "runs": {
    "newBatch": "دفعة جديدة",
    "history": "سجل التشغيلات",
    "count": "{count} تشغيل",
    "emptyTitle": "لنبدأ الدفعة التالية",
    "emptyBody": "أضف ملف تذاكر بصيغة CSV أو JSON وتابع النتائج هنا.",
    "createFirst": "أنشئ دفعتك الأولى",
    "colBatch": "الدفعة",
    "colStarted": "وقت البدء · بغداد",
    "colClassifier": "المصنِّف",
    "colTickets": "التذاكر",
    "colStatus": "الحالة",
    "colCost": "الكلفة التقديرية",
    "batchName": "الدفعة #{id}",
    "classifierJev": "Jev",
    "classifierCascade": "Jev ثم Gemini"
  },
  "runDetail": {
    "back": "كل تشغيلات المعالجة",
    "notFound": "التشغيل غير موجود",
    "notFoundBody": "اختر تشغيلاً من سجل المعالجة.",
    "started": "بدأ {date} الساعة {time} بتوقيت بغداد · {mode}",
    "modeCascade": "Jev مع Gemini كبديل",
    "export": "تصدير الملخص",
    "review": "مراجعة التذاكر",
    "running": "جارٍ تجهيز تذاكرك",
    "interrupted": "توقفت الدفعة",
    "finished": "اكتملت معالجة الدفعة",
    "progress": "تمت معالجة {processed} من {total} تذكرة",
    "progressLabel": "تقدم الدفعة",
    "degraded": "لم يكن Jev متاحاً لجزء من هذا التشغيل. استخدام Gemini البديل مسجل في النتائج.",
    "processed": "تمت معالجتها",
    "processedDetail": "من أصل {total} تذكرة مرسلة",
    "needsReview": "تحتاج مراجعة بشرية",
    "needsReviewDetail": "راجع ملاحظات التصعيد",
    "latency": "الوسيط لزمن المعالجة",
    "latencyDetail": "لكل تذكرة معالجة",
    "cost": "الكلفة التقديرية للتشغيل",
    "costDetail": "حسب استهلاك الرموز المسجل",
    "issues": "توزيع المشكلات",
    "reasons": "أسباب التصعيد",
    "noData": "لا توجد بيانات لهذا القسم.",
    "stepsPending": "تظهر الخطوات هنا عند انتهاء كل تذكرة.",
    "noTickets": "لا توجد تذكرة معالجة لعرضها بعد."
  }
```

- [ ] **Step 3: Write the failing page test**

Create `employee-frontend/src/features/runs/runs-i18n.test.tsx`:

```tsx
import { renderToStaticMarkup } from "react-dom/server"
import { MemoryRouter } from "react-router-dom"
import { afterEach, expect, it } from "vitest"
import { getLocale, setLocale } from "@/lib/locale"
import type { Run } from "@/lib/types"
import { RunDetailView } from "./RunDetailPage"
import { RunsTable } from "./RunsPage"

const originalLocale = getLocale()
afterEach(() => setLocale(originalLocale))

const run = {
  id: 7, started_at: "2026-11-01T09:00:00+03:00", finished_at: null, mode: "jev",
  status: "running", total: 4, processed: 2, degraded: false, total_cost_usd: 0.0123,
  model_ids: {}, counts: { by_status: { escalated: 1 }, by_category: { failed_transfer: 2 },
    escalation_reasons: { fraud_suspected: 1 }, latency_p50_ms: 1500 },
} as unknown as Run

const ENGLISH = ["Batch #", "Started ·", "Classifier", "Estimated cost", "All pipeline runs",
  "Export summary", "Review tickets", "Preparing your tickets", "tickets processed",
  "Needs human review", "Median latency", "Issue breakdown", "Escalation reasons", "Steps appear here"]

function html() {
  return renderToStaticMarkup(
    <MemoryRouter>
      <RunsTable runs={[run]} />
      <RunDetailView run={run} results={[]} resultsError={null} resultsLoading={false} />
    </MemoryRouter>
  )
}

it("renders the runs pages in Arabic without English UI text", () => {
  setLocale("ar")
  const markup = html()
  expect(markup).toContain("الدفعة #007")
  expect(markup).toContain("تمت معالجة 2 من 4 تذكرة")
  expect(markup).toContain("احتيال محتمل")
  for (const text of ENGLISH) expect(markup, text).not.toContain(text)
})

it("keeps English in English", () => {
  setLocale("en")
  expect(html()).toContain("2 of 4 tickets processed")
})
```

Run: `npm test -- src/features/runs/runs-i18n.test.tsx` — Expected: FAIL (`RunsTable`/`RunDetailView` not exported).

- [ ] **Step 4: Translate `RunsPage.tsx`**

Replace everything from `export function RunsPage()` to the end of `employee-frontend/src/features/runs/RunsPage.tsx` with:

```tsx
export function RunsPage() {
  const copy = useCopy()
  const workspace = useWorkspace(),
    navigate = useNavigate()
  const query = useResource<Run[]>("/runs", workspace.revision, 5000)
  const runs = query.data || []
  return (
    <>
      <PageHeader title={copy.pages.runsTitle} description={copy.pages.runsDescription}>
        <Button size="lg" onClick={() => navigate("/runs/new")}>
          <Plus size={17} />
          {copy.runs.newBatch}
        </Button>
      </PageHeader>
      {query.error && <ErrorState message={query.error} retry={query.reload} />}
      <Card className="data-card">
        <CardHeader>
          <CardTitle className="section-title">
            <Layers3 size={17} />
            {copy.runs.history}
            <span className="muted small">{fill(copy.runs.count, { count: runs.length })}</span>
          </CardTitle>
        </CardHeader>
        {query.loading ? (
          <LoadingState />
        ) : !runs.length ? (
          <EmptyState title={copy.runs.emptyTitle} description={copy.runs.emptyBody}>
            <Button onClick={() => navigate("/runs/new")}>
              <Plus size={16} />
              {copy.runs.createFirst}
            </Button>
          </EmptyState>
        ) : (
          <RunsTable runs={runs} />
        )}
      </Card>
    </>
  )
}

export function RunsTable({ runs }: { runs: Run[] }) {
  const copy = useCopy()
  const navigate = useNavigate()
  return (
    <Table>
      <TableHeader>
        <TableRow>
          <TableHead>{copy.runs.colBatch}</TableHead>
          <TableHead>{copy.runs.colStarted}</TableHead>
          <TableHead>{copy.runs.colClassifier}</TableHead>
          <TableHead>{copy.runs.colTickets}</TableHead>
          <TableHead>{copy.runs.colStatus}</TableHead>
          <TableHead>{copy.runs.colCost}</TableHead>
        </TableRow>
      </TableHeader>
      <TableBody>
        {runs.map((run) => (
          <TableRow
            key={run.id}
            className="clickable-row"
            onClick={(event) => {
              if ((event.target as HTMLElement).closest("a, button")) return
              navigate(`/runs/${run.id}`)
            }}
          >
            <TableCell>
              <Link className="ticket-id" to={`/runs/${run.id}`}>
                {fill(copy.runs.batchName, { id: String(run.id).padStart(3, "0") })}
              </Link>
            </TableCell>
            <TableCell>
              {dateLabel(run.started_at)}
              <small className="block-muted">{timeLabel(run.started_at)}</small>
            </TableCell>
            <TableCell>{run.mode === "cascade" ? copy.runs.classifierCascade : copy.runs.classifierJev}</TableCell>
            <TableCell>
              {run.processed} / {run.total}
            </TableCell>
            <TableCell>
              <StatusBadge status={run.status} />
            </TableCell>
            <TableCell>{`$${run.total_cost_usd.toFixed(4)}`}</TableCell>
          </TableRow>
        ))}
      </TableBody>
    </Table>
  )
}
```

Change the imports: `import { fill, useCopy } from "@/lib/locale"` and `import { dateLabel, timeLabel } from "@/lib/format"` (drop `humanize`).

- [ ] **Step 5: Translate `RunDetailPage.tsx`**

Replace the whole file with:

```tsx
import { Link, useParams } from "react-router-dom"
import { ArrowLeft, ArrowRight, CheckCheck, Clock3, Coins, Download, Layers3 } from "lucide-react"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { EmptyState, ErrorState, LoadingState, Metric, PageHeader, StatusBadge } from "@/components/shared/workspace-ui"
import { useResource } from "@/hooks/use-resource"
import { fill, useCopy } from "@/lib/locale"
import { useWorkspace } from "@/lib/workspace"
import { categoryLabel, dateLabel, downloadJson, duration, reasonLabel, timeLabel } from "@/lib/format"
import type { Result, Run } from "@/lib/types"
import { TicketFlow } from "@/features/review/TicketFlow"
import { runModelRows } from "./run-models"
import { loadRunResults } from "./run-results"

export function RunDetailPage() {
  const { id } = useParams(),
    workspace = useWorkspace()
  const copy = useCopy()
  const query = useResource<Run>(`/runs/${id}`, workspace.revision, 2500)
  const run = query.data
  const results = useResource<Result[]>(
    run ? `/results?run_id=${run.id}&limit=500` : null,
    workspace.revision,
    run?.status === "running" ? 2500 : 0,
    loadRunResults,
  )
  if (query.error) return <ErrorState message={query.error} retry={query.reload} />
  if (!run)
    return query.loading ? (
      <LoadingState />
    ) : (
      <EmptyState title={copy.runDetail.notFound} description={copy.runDetail.notFoundBody} />
    )
  return (
    <RunDetailView run={run} results={results.data} resultsError={results.error} resultsLoading={results.loading} />
  )
}

export function RunDetailView({
  run,
  results,
  resultsError,
  resultsLoading,
}: {
  run: Run
  results: Result[] | null
  resultsError: string | null
  resultsLoading: boolean
}) {
  const copy = useCopy()
  const text = copy.runDetail
  const progress = run.total ? Math.round((run.processed / run.total) * 100) : 0
  const models = runModelRows(run.model_ids)
  return (
    <>
      <Link to="/runs" className="back-link">
        <ArrowLeft size={15} />
        {text.back}
      </Link>
      <PageHeader
        title={fill(copy.runs.batchName, { id: String(run.id).padStart(3, "0") })}
        description={fill(text.started, {
          date: dateLabel(run.started_at),
          time: timeLabel(run.started_at),
          mode: run.mode === "cascade" ? text.modeCascade : copy.runs.classifierJev,
        })}
      >
        <Button variant="outline" onClick={() => downloadJson(run, `batch-${run.id}-summary.json`)}>
          <Download size={16} />
          {text.export}
        </Button>
        <Button nativeButton={false} render={<Link to={`/?run=${run.id}`} />}>
          {text.review}
          <ArrowRight size={16} />
        </Button>
      </PageHeader>
      <Card className="run-progress-card">
        <CardContent>
          <div>
            <h2>{run.status === "running" ? text.running : run.status === "failed" ? text.interrupted : text.finished}</h2>
            <StatusBadge status={run.status} />
          </div>
          <p>{fill(text.progress, { processed: run.processed, total: run.total })}</p>
          <div className="run-progress" role="progressbar" aria-label={text.progressLabel}
               aria-valuenow={progress} aria-valuemin={0} aria-valuemax={100}>
            <span style={{ width: `${progress}%` }} />
          </div>
          {run.counts.error && <p className="error-text">{run.counts.error}</p>}
          {run.degraded && run.mode === "cascade" && <p className="field-help">{text.degraded}</p>}
        </CardContent>
      </Card>
      <div className="metrics-grid">
        <Metric label={text.processed} value={run.processed}
                detail={fill(text.processedDetail, { total: run.total })} icon={<Layers3 size={18} />} />
        <Metric label={text.needsReview} value={run.counts.by_status?.escalated || 0}
                detail={text.needsReviewDetail} icon={<CheckCheck size={18} />} tone="metric-amber" />
        <Metric label={text.latency} value={duration(run.counts.latency_p50_ms || 0)}
                detail={text.latencyDetail} icon={<Clock3 size={18} />} />
        <Metric label={text.cost} value={`$${run.total_cost_usd.toFixed(4)}`}
                detail={text.costDetail} icon={<Coins size={18} />} />
      </div>
      {models.length > 0 && (
        <Card className="run-models-card">
          <CardHeader>
            <CardTitle>{copy.models.usedTitle}</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="simple-breakdown">
              {models.map((row) => (
                <div key={row.step}>
                  <span>{copy.models.steps[row.step]}</span>
                  <strong dir="ltr">{row.provider ? `${row.provider} · ${row.model}` : row.model}</strong>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>
      )}
      <div className="two-column">
        <Card>
          <CardHeader>
            <CardTitle>{text.issues}</CardTitle>
          </CardHeader>
          <CardContent>
            <Breakdown values={run.counts.by_category || {}} label={categoryLabel} empty={text.noData} />
          </CardContent>
        </Card>
        <Card>
          <CardHeader>
            <CardTitle>{text.reasons}</CardTitle>
          </CardHeader>
          <CardContent>
            <Breakdown values={run.counts.escalation_reasons || {}} label={reasonLabel} empty={text.noData} />
          </CardContent>
        </Card>
      </div>
      <section className="run-flows">
        {resultsError && <p className="error-text">{resultsError}</p>}
        {results?.map((result) => (
          <div key={result.id}>
            <Link to={`/tickets/${result.id}`} className="run-flow-ticket">
              {result.ticket.external_id}
            </Link>
            <TicketFlow result={result} />
          </div>
        ))}
        {!results?.length && !resultsLoading && (
          <p className="muted small">{run.status === "running" ? text.stepsPending : text.noTickets}</p>
        )}
      </section>
    </>
  )
}

function Breakdown({ values, label, empty }: {
  values: Record<string, number>
  label: (value: string) => string
  empty: string
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
    <p className="muted small">{empty}</p>
  )
}
```

- [ ] **Step 6: Run checks**

Run: `npm test && npm run lint && npm run typecheck` — Expected: all PASS.

- [ ] **Step 7: Commit**

```bash
git add employee-frontend/src/locales employee-frontend/src/features/runs
git commit -m "feat: translate pipeline run pages and enforce locale key parity"
```

---

### Task 12: Usage types, formatters and evaluation copy

**Files:**
- Modify: `employee-frontend/src/lib/types.ts` (usage types; remove `Insights.evaluation`)
- Modify: `employee-frontend/src/lib/format.ts` (`usd`, `msLabel`, `percent1`, `countLabel`)
- Modify: `employee-frontend/src/locales/en.json`, `employee-frontend/src/locales/ar.json` (`evaluation`, `pages.evaluationDescription`)
- Test: `employee-frontend/src/lib/format.test.ts`

**Interfaces:**
- Produces types: `AiProcess`, `CostSource`, `UsageGroup`, `UsageDay`, `UsageTotals`, `UsageSummary`, `UsageTicket`, `UsageTicketPage`, `AiCallView`, `TicketCalls`, `UsagePeriod = "24h" | "7d" | "30d"`, `UsageFilters = { period: UsagePeriod; process: AiProcess | "all"; model: string; runId: string }` (`"all"` / `""` mean no filter).
- Produces formatters: `usd(v?: number | null)` (`$0`; 5 decimals below $0.01; 4 decimals below $1; else 2), `msLabel(v?: number | null)`, `percent1(v?: number | null)`, `countLabel(v?: number | null)`.
- Produces copy keys under `evaluation.*` exactly as in Step 4.

- [ ] **Step 1: Write the failing test**

Create `employee-frontend/src/lib/format.test.ts`:

```ts
import { expect, it } from "vitest"
import { countLabel, msLabel, percent1, usd } from "./format"

it("formats usage numbers and keeps null as a dash", () => {
  expect(usd(null)).toBe("—")
  expect(usd(0)).toBe("$0")
  expect(usd(0.000412)).toBe("$0.00041")
  expect(usd(0.0144)).toBe("$0.0144")
  expect(usd(12.3456)).toBe("$12.35")
  expect(msLabel(undefined)).toBe("—")
  expect(msLabel(850)).toBe("850 ms")
  expect(msLabel(2500)).toBe("2.5 s")
  expect(percent1(0.8765)).toBe("87.7%")
  expect(percent1(null)).toBe("—")
  expect(countLabel(1534.4)).toBe("1,534")
})
```

Run: `npm test -- src/lib/format.test.ts` — Expected: FAIL (missing exports).

- [ ] **Step 2: Add formatters**

Append to `employee-frontend/src/lib/format.ts`:

```ts
export const usd = (value?: number | null) =>
  value == null ? "—"
    : value === 0 ? "$0"
      : value < 0.01 ? `$${value.toFixed(5)}`
        : value < 1 ? `$${value.toFixed(4)}`
          : `$${value.toFixed(2)}`
export const msLabel = (value?: number | null) =>
  value == null ? "—" : duration(Math.round(value))
export const percent1 = (value?: number | null) =>
  value == null ? "—" : `${(value * 100).toFixed(1)}%`
export const countLabel = (value?: number | null) =>
  value == null ? "—" : Math.round(value).toLocaleString("en-US")
```

- [ ] **Step 3: Add the types**

In `employee-frontend/src/lib/types.ts`, delete `evaluation: null` from `Insights` (and its use, if any: `grep -rn "\.evaluation" src`), and append:

```ts
export type AiProcess =
  | "intake" | "classify" | "extract" | "draft" | "draft_search"
  | "credential_check" | "kb_index" | "kb_search" | "probe"
export type CostSource = "provider" | "estimate" | "local" | "unknown"
export type UsageGroup = {
  key: string
  process?: AiProcess
  provider?: string
  model?: string
  locality?: "local" | "cloud"
  processes?: AiProcess[]
  calls: number
  cost_usd: number
  cost_share: number | null
  cost_per_call: number | null
  latency_p50_ms: number | null
  latency_p95_ms: number | null
  error_rate: number | null
  input_tokens: number
  output_tokens: number
  cost_sources: Partial<Record<CostSource, number>>
}
export type UsageDay = {
  date: string
  cost_usd: number
  calls: number
  errors: number
  latency_p95_ms: number | null
}
export type UsageTotals = {
  cost_usd: number
  calls: number
  errors: number
  error_rate: number | null
  unknown_cost_calls: number
  tickets: number
  cost_per_ticket_avg: number | null
  cost_per_ticket_p95: number | null
  ai_time_p50_ms: number | null
  ai_time_p95_ms: number | null
  draft_time_p50_ms: number | null
  draft_time_p95_ms: number | null
}
export type UsageSummary = {
  period: { from: string; to: string }
  totals: UsageTotals
  by_process: UsageGroup[]
  by_model: UsageGroup[]
  daily: UsageDay[]
  unattributed: { cost_usd: number; calls: number; by_process: UsageGroup[] }
}
export type UsageTicket = {
  result_id: number
  ticket_id: number
  external_id: string
  run_id: number
  received_at: string
  processed_at: string | null
  status: string
  category: string | null
  cost_usd: number
  intake_cost_usd: number
  total_cost_usd: number
  cost_by_process: Partial<Record<AiProcess, number>>
  ai_time_ms: number
  draft_time_ms: number | null
  intake_time_ms: number
  calls: number
  errors: number
  detail_recorded: boolean
}
export type UsageTicketPage = { items: UsageTicket[]; total: number }
export type AiCallView = {
  id: number
  process: AiProcess
  provider: string
  model: string
  locality: "local" | "cloud"
  started_at: string
  latency_ms: number
  input_tokens: number | null
  output_tokens: number | null
  cost_usd: number
  cost_source: CostSource
  status: "ok" | "error"
  error: string | null
  attempt: number
  detail: Record<string, unknown>
}
export type TicketCalls = { result: UsageTicket; calls: AiCallView[] }
export type UsagePeriod = "24h" | "7d" | "30d"
export type UsageFilters = { period: UsagePeriod; process: AiProcess | "all"; model: string; runId: string }
```

- [ ] **Step 4: Add the copy**

In `en.json`, set `pages.evaluationDescription` to `"Cost and response time of every AI process."` and add a top-level `"evaluation"` object:

```json
  "evaluation": {
    "refresh": "Refresh",
    "filters": {
      "period": "Period", "day": "Last 24 hours", "week": "Last 7 days", "month": "Last 30 days",
      "process": "AI process", "allProcesses": "All processes",
      "model": "Model", "allModels": "All models",
      "run": "Batch run", "allRuns": "All runs", "runOption": "Batch #{id}"
    },
    "headline": {
      "cost": "Total AI cost", "costDetail": "{calls} AI calls",
      "perTicket": "Cost per ticket", "perTicketDetail": "average · p95 {value}",
      "time": "AI time per ticket", "timeDetail": "median · p95 {value}",
      "errors": "AI error rate", "errorsDetail": "{count} failed calls",
      "tickets": "Tickets", "ticketsDetail": "{count} calls without a known price"
    },
    "byProcess": "Cost and time by AI process",
    "byModel": "Cost and time by model",
    "table": {
      "process": "AI process", "model": "Model", "calls": "Calls", "cost": "Cost", "share": "Share",
      "perCall": "Per call", "p50": "p50", "p95": "p95", "errors": "Errors", "tokens": "Tokens in / out",
      "serves": "Used for", "inUse": "In use", "local": "Local · $0", "empty": "No AI calls in this period."
    },
    "metricHelp": {
      "share": "Share of total AI cost", "p50": "Median latency", "p95": "95th percentile latency",
      "errors": "Share of calls that failed"
    },
    "trend": {
      "title": "Daily cost and slowest responses", "cost": "Cost", "p95": "p95 latency", "date": "Day",
      "empty": "No daily data in this period."
    },
    "tickets": {
      "title": "Every ticket", "ticket": "Ticket", "received": "Received", "status": "Status",
      "category": "Issue", "cost": "AI cost", "breakdown": "Cost by process", "aiTime": "AI time",
      "draftTime": "Drafting", "errors": "Errors", "sort": "Sort by", "sortRecent": "Most recent",
      "sortCost": "Highest cost", "sortTime": "Slowest",
      "notRecorded": "Detail not recorded (processed before tracking)", "open": "Open the AI timeline of {id}",
      "empty": "No processed tickets in this period.", "range": "{from}–{to} of {total}",
      "previous": "Previous page", "next": "Next page", "intake": "incl. intake {value}"
    },
    "timeline": {
      "title": "AI timeline · {id}", "close": "Close", "loading": "Loading calls…",
      "empty": "No AI calls were recorded for this ticket.",
      "total": "{calls} calls · {cost} · AI time {time}", "tokens": "{in} in / {out} out",
      "attempt": "attempt {n}", "error": "Error"
    },
    "unattributed": {
      "title": "Not tied to a ticket",
      "body": "Knowledge indexing, manual knowledge searches and model tests.",
      "empty": "None in this period."
    },
    "processes": {
      "intake": "Customer intake", "classify": "Classification (Jev)", "extract": "Detail extraction",
      "draft": "Reply drafting", "draft_search": "Knowledge search (drafting)",
      "credential_check": "Credential check (Jev)", "kb_index": "Knowledge indexing",
      "kb_search": "Knowledge search (manual)", "probe": "Model test"
    },
    "sources": {
      "provider": "Reported by the provider", "estimate": "Estimated from tokens",
      "local": "Local · $0", "unknown": "Price unknown"
    },
    "estimated": "est."
  }
```

In `ar.json`, set `pages.evaluationDescription` to `"تكلفة وزمن استجابة كل عملية ذكاء اصطناعي."` and add:

```json
  "evaluation": {
    "refresh": "تحديث",
    "filters": {
      "period": "الفترة", "day": "آخر 24 ساعة", "week": "آخر 7 أيام", "month": "آخر 30 يوماً",
      "process": "عملية الذكاء الاصطناعي", "allProcesses": "كل العمليات",
      "model": "النموذج", "allModels": "كل النماذج",
      "run": "تشغيل الدفعة", "allRuns": "كل التشغيلات", "runOption": "الدفعة #{id}"
    },
    "headline": {
      "cost": "إجمالي كلفة الذكاء الاصطناعي", "costDetail": "{calls} استدعاء",
      "perTicket": "الكلفة لكل تذكرة", "perTicketDetail": "المتوسط · المئين 95: {value}",
      "time": "زمن الذكاء الاصطناعي لكل تذكرة", "timeDetail": "الوسيط · المئين 95: {value}",
      "errors": "نسبة أخطاء الذكاء الاصطناعي", "errorsDetail": "{count} استدعاء فاشل",
      "tickets": "التذاكر", "ticketsDetail": "{count} استدعاء بسعر غير معروف"
    },
    "byProcess": "الكلفة والزمن حسب العملية",
    "byModel": "الكلفة والزمن حسب النموذج",
    "table": {
      "process": "العملية", "model": "النموذج", "calls": "الاستدعاءات", "cost": "الكلفة", "share": "الحصة",
      "perCall": "لكل استدعاء", "p50": "الوسيط", "p95": "المئين 95", "errors": "الأخطاء",
      "tokens": "الرموز دخول / خروج", "serves": "يُستخدم في", "inUse": "قيد الاستخدام",
      "local": "محلي · $0", "empty": "لا توجد استدعاءات ذكاء اصطناعي في هذه الفترة."
    },
    "metricHelp": {
      "share": "Share of total AI cost", "p50": "Median latency", "p95": "95th percentile latency",
      "errors": "Share of calls that failed"
    },
    "trend": {
      "title": "الكلفة اليومية وأبطأ الاستجابات", "cost": "الكلفة", "p95": "زمن المئين 95", "date": "اليوم",
      "empty": "لا توجد بيانات يومية في هذه الفترة."
    },
    "tickets": {
      "title": "كل التذاكر", "ticket": "التذكرة", "received": "وقت الاستلام", "status": "الحالة",
      "category": "المشكلة", "cost": "كلفة الذكاء الاصطناعي", "breakdown": "الكلفة حسب العملية",
      "aiTime": "زمن الذكاء الاصطناعي", "draftTime": "صياغة الرد", "errors": "الأخطاء", "sort": "الترتيب حسب",
      "sortRecent": "الأحدث", "sortCost": "الأعلى كلفة", "sortTime": "الأبطأ",
      "notRecorded": "التفاصيل غير مسجلة (عولجت قبل بدء التتبع)", "open": "فتح خط زمن الذكاء الاصطناعي للتذكرة {id}",
      "empty": "لا توجد تذاكر معالجة في هذه الفترة.", "range": "{from}–{to} من {total}",
      "previous": "الصفحة السابقة", "next": "الصفحة التالية", "intake": "يشمل الاستقبال {value}"
    },
    "timeline": {
      "title": "خط زمن الذكاء الاصطناعي · {id}", "close": "إغلاق", "loading": "جارٍ تحميل الاستدعاءات…",
      "empty": "لم تُسجل أي استدعاءات ذكاء اصطناعي لهذه التذكرة.",
      "total": "{calls} استدعاء · {cost} · زمن الذكاء الاصطناعي {time}", "tokens": "{in} دخول / {out} خروج",
      "attempt": "المحاولة {n}", "error": "خطأ"
    },
    "unattributed": {
      "title": "غير مرتبطة بتذكرة",
      "body": "فهرسة قاعدة المعرفة، والبحث اليدوي فيها، واختبارات النماذج.",
      "empty": "لا شيء في هذه الفترة."
    },
    "processes": {
      "intake": "استقبال العميل", "classify": "التصنيف (Jev)", "extract": "استخراج التفاصيل",
      "draft": "صياغة الرد", "draft_search": "البحث في المعرفة (أثناء الصياغة)",
      "credential_check": "فحص طلب البيانات السرية (Jev)", "kb_index": "فهرسة قاعدة المعرفة",
      "kb_search": "البحث في المعرفة (يدوي)", "probe": "اختبار نموذج"
    },
    "sources": {
      "provider": "حسب المزوّد", "estimate": "تقدير من عدد الرموز",
      "local": "محلي · $0", "unknown": "السعر غير معروف"
    },
    "estimated": "تقديري"
  }
```

`metricHelp` stays English in both files on purpose: it feeds `title` tooltips with the standard English metric term.

- [ ] **Step 5: Run checks**

Run: `npm test && npm run lint && npm run typecheck` — Expected: all PASS (the old `EvaluationPage.tsx` is untouched and still compiles; Task 16 replaces it).

- [ ] **Step 6: Commit**

```bash
git add employee-frontend/src/lib employee-frontend/src/locales
git commit -m "feat: add AI usage types, formatters and translated dashboard copy"
```

---

### Task 13: Dashboard view helpers

**Files:**
- Create: `employee-frontend/src/features/evaluation/usage-view.ts`
- Create: `employee-frontend/src/features/evaluation/fixtures.ts`
- Test: `employee-frontend/src/features/evaluation/usage-view.test.ts`

**Interfaces:**
- Consumes: Task 12 types; `AiSummary` from `types.ts`; `Copy` from `@/lib/locale`.
- Produces:
  - `PROCESS_ORDER: AiProcess[]`
  - `periodRange(period: UsagePeriod, now: number): { from: string; to: string }`
  - `usageQuery(filters: UsageFilters, range: { from: string; to: string }, extra?: Record<string, string | number>): string`
  - `shareWidth(value?: number | null): string` (e.g. `"37%"`, clamped 0–100, `"0%"` for null)
  - `sourceMark(sources: Partial<Record<CostSource, number>>): CostSource | null` (`local` if all local; `unknown` if any unknown; `estimate` if any estimate; `null` if all provider)
  - `isInUse(group: UsageGroup, ai?: AiSummary): boolean`
  - `costSegments(costs: Partial<Record<AiProcess, number>>): { process: AiProcess; share: number }[]` (ordered by `PROCESS_ORDER`, zero costs dropped)
  - `waterfall(calls: AiCallView[]): { call: AiCallView; left: number; width: number }[]` (percent of the ticket's span; min width 1)
  - `trendGeometry(days: UsageDay[], height?: number): { bars: { day: UsageDay; x: number; y: number; h: number }[]; line: string; width: number; height: number }`
  - `processLabel(process: string, copy: Copy["evaluation"]): string`
- Fixtures (`fixtures.ts`): `summaryFixture: UsageSummary`, `emptySummary: UsageSummary`, `ticketPage: UsageTicketPage`, `ticketCalls: TicketCalls`.

- [ ] **Step 1: Write fixtures and failing tests**

Create `employee-frontend/src/features/evaluation/fixtures.ts`:

```ts
import type { TicketCalls, UsageGroup, UsageSummary, UsageTicketPage } from "@/lib/types"

const group = (patch: Partial<UsageGroup>): UsageGroup => ({
  key: "x", calls: 1, cost_usd: 0, cost_share: 0, cost_per_call: 0, latency_p50_ms: 100,
  latency_p95_ms: 200, error_rate: 0, input_tokens: 100, output_tokens: 10, cost_sources: { provider: 1 },
  ...patch,
})

export const summaryFixture: UsageSummary = {
  period: { from: "2026-11-07T09:00:00Z", to: "2026-11-14T09:00:00Z" },
  totals: {
    cost_usd: 0.0144, calls: 7, errors: 1, error_rate: 1 / 7, unknown_cost_calls: 1, tickets: 3,
    cost_per_ticket_avg: 0.17, cost_per_ticket_p95: 0.47, ai_time_p50_ms: 2000, ai_time_p95_ms: 5600,
    draft_time_p50_ms: 1500, draft_time_p95_ms: 1500,
  },
  by_process: [
    group({ key: "draft", process: "draft", cost_usd: 0.01, cost_share: 0.69, latency_p50_ms: 1200 }),
    group({ key: "intake", process: "intake", cost_usd: 0.004, cost_share: 0.28 }),
    group({ key: "classify", process: "classify", calls: 2, cost_usd: 0.0002, cost_share: 0.01,
            cost_sources: { estimate: 2 } }),
    group({ key: "extract", process: "extract", cost_usd: 0, cost_share: 0, error_rate: 1,
            latency_p95_ms: 4000, cost_sources: { local: 1 } }),
  ],
  by_model: [
    group({ key: "openrouter:anthropic/claude-sonnet-5.5", provider: "openrouter",
            model: "anthropic/claude-sonnet-5.5", locality: "cloud", processes: ["draft"], cost_usd: 0.01 }),
    group({ key: "ollama:qwen3:4b", provider: "ollama", model: "qwen3:4b", locality: "local",
            processes: ["extract"], cost_sources: { local: 1 } }),
    group({ key: "typesafe:jev-1.13.0", provider: "typesafe", model: "jev-1.13.0", locality: "cloud",
            processes: ["classify"], calls: 2, cost_usd: 0.0002, cost_sources: { estimate: 2 } }),
  ],
  daily: [
    { date: "2026-11-13", cost_usd: 0.004, calls: 3, errors: 0, latency_p95_ms: 900 },
    { date: "2026-11-14", cost_usd: 0.0104, calls: 4, errors: 1, latency_p95_ms: 4000 },
  ],
  unattributed: {
    cost_usd: 0.0002, calls: 2,
    by_process: [group({ key: "kb_index", process: "kb_index", cost_usd: 0.0002 }),
                 group({ key: "probe", process: "probe", cost_sources: { unknown: 1 } })],
  },
}

export const emptySummary: UsageSummary = {
  period: summaryFixture.period,
  totals: { cost_usd: 0, calls: 0, errors: 0, error_rate: null, unknown_cost_calls: 0, tickets: 0,
            cost_per_ticket_avg: null, cost_per_ticket_p95: null, ai_time_p50_ms: null, ai_time_p95_ms: null,
            draft_time_p50_ms: null, draft_time_p95_ms: null },
  by_process: [], by_model: [], daily: [], unattributed: { cost_usd: 0, calls: 0, by_process: [] },
}

export const ticketPage: UsageTicketPage = {
  total: 2,
  items: [
    { result_id: 11, ticket_id: 1, external_id: "INTAKE-ab12", run_id: 4, received_at: "2026-11-14T08:00:00Z",
      processed_at: "2026-11-14T08:00:05Z", status: "pending_review", category: "failed_transfer",
      cost_usd: 0.012, intake_cost_usd: 0.004, total_cost_usd: 0.016,
      cost_by_process: { intake: 0.004, classify: 0.0001, draft: 0.01 }, ai_time_ms: 2000, draft_time_ms: 1500,
      intake_time_ms: 800, calls: 3, errors: 0, detail_recorded: true },
    { result_id: 12, ticket_id: 2, external_id: "T-OLD", run_id: 1, received_at: "2026-11-10T08:00:00Z",
      processed_at: null, status: "escalated", category: "other", cost_usd: 0.5, intake_cost_usd: 0,
      total_cost_usd: 0.5, cost_by_process: {}, ai_time_ms: 1000, draft_time_ms: null, intake_time_ms: 0,
      calls: 0, errors: 0, detail_recorded: false },
  ],
}

export const ticketCalls: TicketCalls = {
  result: ticketPage.items[0],
  calls: [
    { id: 1, process: "intake", provider: "openrouter", model: "google/gemini-3.8-flash", locality: "cloud",
      started_at: "2026-11-14T07:59:00.000Z", latency_ms: 800, input_tokens: 1200, output_tokens: 300,
      cost_usd: 0.004, cost_source: "provider", status: "ok", error: null, attempt: 1, detail: { kind: "analyze" } },
    { id: 2, process: "classify", provider: "typesafe", model: "jev-1.13.0", locality: "cloud",
      started_at: "2026-11-14T08:00:00.000Z", latency_ms: 900, input_tokens: 1000, output_tokens: null,
      cost_usd: 0.0001, cost_source: "estimate", status: "ok", error: null, attempt: 1, detail: { check: "main" } },
    { id: 3, process: "extract", provider: "ollama", model: "qwen3:4b", locality: "local",
      started_at: "2026-11-14T08:00:01.000Z", latency_ms: 1000, input_tokens: null, output_tokens: null,
      cost_usd: 0, cost_source: "local", status: "error", error: "TimeoutError", attempt: 2, detail: {} },
  ],
}
```

Create `employee-frontend/src/features/evaluation/usage-view.test.ts`:

```ts
import { expect, it } from "vitest"
import { getCopy } from "@/lib/locale"
import type { AiSummary } from "@/lib/types"
import { summaryFixture, ticketCalls } from "./fixtures"
import {
  costSegments,
  isInUse,
  periodRange,
  processLabel,
  shareWidth,
  sourceMark,
  trendGeometry,
  usageQuery,
  waterfall,
} from "./usage-view"

const NOW = Date.parse("2026-11-14T09:00:00Z")

it("builds period ranges and query strings", () => {
  expect(periodRange("24h", NOW)).toEqual({ from: "2026-11-13T09:00:00.000Z", to: "2026-11-14T09:00:00.000Z" })
  expect(periodRange("7d", NOW).from).toBe("2026-11-07T09:00:00.000Z")
  const range = periodRange("30d", NOW)
  expect(usageQuery({ period: "30d", process: "all", model: "", runId: "" }, range)).toBe(
    `from=${encodeURIComponent(range.from)}&to=${encodeURIComponent(range.to)}`)
  expect(usageQuery({ period: "7d", process: "draft", model: "ollama:qwen3:4b", runId: "4" }, range,
                    { sort: "cost", limit: 25 }))
    .toContain("process=draft&model=ollama%3Aqwen3%3A4b&run_id=4&sort=cost&limit=25")
})

it("clamps share bars and summarizes cost sources", () => {
  expect(shareWidth(0.374)).toBe("37.4%")
  expect(shareWidth(1.4)).toBe("100%")
  expect(shareWidth(null)).toBe("0%")
  expect(sourceMark({ provider: 3 })).toBeNull()
  expect(sourceMark({ local: 2 })).toBe("local")
  expect(sourceMark({ provider: 1, estimate: 1 })).toBe("estimate")
  expect(sourceMark({ estimate: 1, unknown: 1 })).toBe("unknown")
})

it("detects models in use from health.ai", () => {
  const ai = { locality: "mixed", steps: { draft: { provider: "openrouter", model: "anthropic/claude-sonnet-5.5",
    locality: "cloud", status: "ready" } } } as AiSummary
  expect(isInUse(summaryFixture.by_model[0], ai)).toBe(true)
  expect(isInUse(summaryFixture.by_model[1], ai)).toBe(false)
  expect(isInUse(summaryFixture.by_model[0], undefined)).toBe(false)
})

it("orders cost segments by process and drops zeros", () => {
  expect(costSegments({ draft: 0.01, intake: 0.004, extract: 0, classify: 0.0001 }).map((s) => s.process))
    .toEqual(["intake", "classify", "draft"])
  expect(costSegments({}).length).toBe(0)
  const total = costSegments({ draft: 0.03, intake: 0.01 }).reduce((sum, s) => sum + s.share, 0)
  expect(total).toBeCloseTo(1)
})

it("lays out a waterfall from start times and latencies", () => {
  const bars = waterfall(ticketCalls.calls)
  expect(bars.map((b) => b.call.id)).toEqual([1, 2, 3])
  expect(bars[0].left).toBe(0)
  expect(bars[2].left + bars[2].width).toBeCloseTo(100)
  expect(waterfall([])).toEqual([])
})

it("draws the trend and names processes", () => {
  const g = trendGeometry(summaryFixture.daily, 120)
  expect(g.bars).toHaveLength(2)
  expect(g.bars[1].h).toBeCloseTo(100)
  expect(g.line.startsWith("M")).toBe(true)
  expect(trendGeometry([]).bars).toEqual([])
  expect(processLabel("draft_search", getCopy().evaluation)).toBe(getCopy().evaluation.processes.draft_search)
  expect(processLabel("future_process", getCopy().evaluation)).toBe("future_process")
})
```

Run: `npm test -- src/features/evaluation` — Expected: FAIL (`Cannot find module './usage-view'`).

- [ ] **Step 2: Implement `usage-view.ts`**

```ts
import type { Copy } from "@/lib/locale"
import type {
  AiCallView,
  AiProcess,
  AiSummary,
  CostSource,
  UsageDay,
  UsageFilters,
  UsageGroup,
  UsagePeriod,
} from "@/lib/types"

export const PROCESS_ORDER: AiProcess[] = [
  "intake", "classify", "extract", "draft", "draft_search", "credential_check", "kb_index", "kb_search", "probe",
]
const PERIOD_MS: Record<UsagePeriod, number> = { "24h": 86_400_000, "7d": 7 * 86_400_000, "30d": 30 * 86_400_000 }

export function periodRange(period: UsagePeriod, now: number) {
  return { from: new Date(now - PERIOD_MS[period]).toISOString(), to: new Date(now).toISOString() }
}

export function usageQuery(
  filters: UsageFilters,
  range: { from: string; to: string },
  extra: Record<string, string | number> = {}
) {
  const params = new URLSearchParams({ from: range.from, to: range.to })
  if (filters.process !== "all") params.set("process", filters.process)
  if (filters.model) params.set("model", filters.model)
  if (filters.runId) params.set("run_id", filters.runId)
  for (const [key, value] of Object.entries(extra)) params.set(key, String(value))
  return params.toString()
}

export function shareWidth(value?: number | null) {
  const pct = Math.min(100, Math.max(0, (value ?? 0) * 100))
  return `${Number(pct.toFixed(1))}%`
}

export function sourceMark(sources: Partial<Record<CostSource, number>>): CostSource | null {
  const used = (Object.keys(sources) as CostSource[]).filter((s) => (sources[s] ?? 0) > 0)
  if (used.length && used.every((s) => s === "local")) return "local"
  if (used.includes("unknown")) return "unknown"
  if (used.includes("estimate")) return "estimate"
  return null
}

export function isInUse(group: UsageGroup, ai?: AiSummary) {
  return Object.values(ai?.steps ?? {}).some(
    (step) => step && step.provider === group.provider && step.model === group.model
  )
}

export function costSegments(costs: Partial<Record<AiProcess, number>>) {
  const present = PROCESS_ORDER.filter((p) => (costs[p] ?? 0) > 0)
  const total = present.reduce((sum, p) => sum + (costs[p] ?? 0), 0)
  return present.map((process) => ({ process, share: total ? (costs[process] ?? 0) / total : 0 }))
}

export function waterfall(calls: AiCallView[]) {
  if (!calls.length) return []
  const spans = calls.map((call) => {
    const start = Date.parse(call.started_at)
    return { call, start, end: start + call.latency_ms }
  })
  const first = Math.min(...spans.map((s) => s.start))
  const last = Math.max(...spans.map((s) => s.end))
  const total = Math.max(1, last - first)
  return spans.map(({ call, start, end }) => {
    const left = ((start - first) / total) * 100
    return { call, left, width: Math.max(1, Math.min(100 - left, ((end - start) / total) * 100)) }
  })
}

export function trendGeometry(days: UsageDay[], height = 120) {
  const width = Math.max(1, days.length) * 40
  if (!days.length) return { bars: [], line: "", width, height }
  const maxCost = Math.max(...days.map((d) => d.cost_usd), 1e-12)
  const maxLatency = Math.max(...days.map((d) => d.latency_p95_ms ?? 0), 1)
  const bars = days.map((day, i) => {
    const h = (day.cost_usd / maxCost) * 100
    return { day, x: i * 40 + 8, y: height - (h / 100) * height, h }
  })
  const line = days
    .map((d, i) => `${i ? "L" : "M"}${i * 40 + 20},${height - ((d.latency_p95_ms ?? 0) / maxLatency) * height}`)
    .join(" ")
  return { bars, line, width, height }
}

export function processLabel(process: string, copy: Copy["evaluation"]) {
  return (copy.processes as Record<string, string>)[process] ?? process
}
```

- [ ] **Step 3: Run checks**

Run: `npm test -- src/features/evaluation && npm run lint && npm run typecheck` — Expected: all PASS.

- [ ] **Step 4: Commit**

```bash
git add employee-frontend/src/features/evaluation
git commit -m "feat: add AI usage view helpers and fixtures"
```

---

### Task 14: Filters, headline, breakdown tables, trend and unattributed card

**Files:**
- Create: `employee-frontend/src/features/evaluation/UsageFilters.tsx`, `UsageHeadline.tsx`, `GroupTable.tsx`, `DailyTrend.tsx`, `UnattributedCard.tsx`, `CostValue.tsx`
- Test: `employee-frontend/src/features/evaluation/summary.test.tsx`

**Interfaces:**
- Consumes: Tasks 12–13; `FilterSelect`, `Metric` from `workspace-ui`; `Table*`, `Card*`, `Badge`.
- Produces:
  - `CostValue({ value, sources }: { value: number | null | undefined; sources?: Partial<Record<CostSource, number>> })` — formatted cost plus a source marker
  - `UsageFilters({ filters, onChange, models, runs, onRefresh }: { filters: UsageFilters; onChange: (f: UsageFilters) => void; models: string[]; runs: number[]; onRefresh: () => void })`
  - `UsageHeadline({ totals }: { totals: UsageTotals })`
  - `GroupTable({ kind, groups, ai }: { kind: "process" | "model"; groups: UsageGroup[]; ai?: AiSummary })`
  - `DailyTrend({ days }: { days: UsageDay[] })`
  - `UnattributedCard({ data }: { data: UsageSummary["unattributed"] })`

- [ ] **Step 1: Write the failing tests**

Create `employee-frontend/src/features/evaluation/summary.test.tsx`:

```tsx
import { renderToStaticMarkup } from "react-dom/server"
import { afterEach, expect, it } from "vitest"
import { getLocale, setLocale } from "@/lib/locale"
import type { AiSummary } from "@/lib/types"
import { DailyTrend } from "./DailyTrend"
import { emptySummary, summaryFixture } from "./fixtures"
import { GroupTable } from "./GroupTable"
import { UnattributedCard } from "./UnattributedCard"
import { UsageFilters } from "./UsageFilters"
import { UsageHeadline } from "./UsageHeadline"

const originalLocale = getLocale()
afterEach(() => setLocale(originalLocale))
const AI = { locality: "mixed", steps: { draft: { provider: "openrouter", model: "anthropic/claude-sonnet-5.5",
  locality: "cloud", status: "ready" } } } as AiSummary

function all() {
  const s = summaryFixture
  return renderToStaticMarkup(
    <>
      <UsageFilters filters={{ period: "7d", process: "all", model: "", runId: "" }} onChange={() => {}}
                    models={s.by_model.map((g) => g.key)} runs={[4]} onRefresh={() => {}} />
      <UsageHeadline totals={s.totals} />
      <GroupTable kind="process" groups={s.by_process} />
      <GroupTable kind="model" groups={s.by_model} ai={AI} />
      <DailyTrend days={s.daily} />
      <UnattributedCard data={s.unattributed} />
    </>
  )
}

it("renders the summary in English with sources, badges and ltr model IDs", () => {
  setLocale("en")
  const html = all()
  expect(html).toContain("Total AI cost")
  expect(html).toContain("$0.0144")
  expect(html).toContain("Reply drafting")
  expect(html).toContain("Local · $0")
  expect(html).toContain("In use")
  expect(html).toContain('dir="ltr"')
  expect(html).toContain("est.")
  expect(html).toContain('title="Median latency"')
  expect(html).toContain("<svg")
  expect(html).toContain("Model test")
})

it("renders the summary in Arabic without English UI text", () => {
  setLocale("ar")
  const html = all()
  expect(html).toContain("إجمالي كلفة الذكاء الاصطناعي")
  expect(html).toContain("صياغة الرد")
  expect(html).toContain("محلي · $0")
  for (const english of ["Total AI cost", "Reply drafting", "In use", "Cost and time by", "Not tied to a ticket"])
    expect(html, english).not.toContain(english)
})

it("UsageHeadline renders dashes for an empty period", () => {
  setLocale("en")
  const html = renderToStaticMarkup(
    <>
      <UsageHeadline totals={emptySummary.totals} />
      <GroupTable kind="process" groups={[]} />
      <DailyTrend days={[]} />
    </>
  )
  expect(html).toContain("—")
  expect(html).toContain("No AI calls in this period.")
  expect(html).toContain("No daily data in this period.")
})
```

Run: `npm test -- src/features/evaluation/summary.test.tsx` — Expected: FAIL (modules not found).

- [ ] **Step 2: Implement `CostValue.tsx` and `UsageFilters.tsx`**

```tsx
// CostValue.tsx
import { usd } from "@/lib/format"
import { useCopy } from "@/lib/locale"
import type { CostSource } from "@/lib/types"
import { sourceMark } from "./usage-view"

export function CostValue({ value, sources = {} }: {
  value: number | null | undefined
  sources?: Partial<Record<CostSource, number>>
}) {
  const copy = useCopy().evaluation
  const mark = sourceMark(sources)
  if (mark === "local") return <span className="usage-local">{copy.sources.local}</span>
  return (
    <span title={mark ? copy.sources[mark] : copy.sources.provider}>
      {usd(value)}
      {mark === "estimate" && <small className="usage-mark"> {copy.estimated}</small>}
      {mark === "unknown" && <small className="usage-mark"> {copy.sources.unknown}</small>}
    </span>
  )
}
```

```tsx
// UsageFilters.tsx
import { RefreshCw } from "lucide-react"
import { Button } from "@/components/ui/button"
import { FilterSelect } from "@/components/shared/workspace-ui"
import { fill, useCopy } from "@/lib/locale"
import type { AiProcess, UsageFilters as Filters, UsagePeriod } from "@/lib/types"
import { PROCESS_ORDER, processLabel } from "./usage-view"

export function UsageFilters({ filters, onChange, models, runs, onRefresh }: {
  filters: Filters
  onChange: (filters: Filters) => void
  models: string[]
  runs: number[]
  onRefresh: () => void
}) {
  const copy = useCopy().evaluation
  const f = copy.filters
  return (
    <div className="usage-filters">
      <FilterSelect label={f.period} value={filters.period}
        options={[{ value: "24h", label: f.day }, { value: "7d", label: f.week }, { value: "30d", label: f.month }]}
        onChange={(value) => onChange({ ...filters, period: value as UsagePeriod })} />
      <FilterSelect label={f.process} value={filters.process}
        options={[{ value: "all", label: f.allProcesses },
                  ...PROCESS_ORDER.map((p) => ({ value: p, label: processLabel(p, copy) }))]}
        onChange={(value) => onChange({ ...filters, process: value as AiProcess | "all" })} />
      <FilterSelect label={f.model} value={filters.model || "all"}
        options={[{ value: "all", label: f.allModels }, ...models.map((m) => ({ value: m, label: m }))]}
        onChange={(value) => onChange({ ...filters, model: value === "all" ? "" : value })} />
      <FilterSelect label={f.run} value={filters.runId || "all"}
        options={[{ value: "all", label: f.allRuns },
                  ...runs.map((id) => ({ value: String(id), label: fill(f.runOption, { id: String(id).padStart(3, "0") }) }))]}
        onChange={(value) => onChange({ ...filters, runId: value === "all" ? "" : value })} />
      <Button variant="outline" onClick={onRefresh}>
        <RefreshCw size={15} />
        {copy.refresh}
      </Button>
    </div>
  )
}
```

- [ ] **Step 3: Implement `UsageHeadline.tsx` and `GroupTable.tsx`**

```tsx
// UsageHeadline.tsx
import { AlertTriangle, Clock3, Coins, Receipt, Ticket } from "lucide-react"
import { Metric } from "@/components/shared/workspace-ui"
import { msLabel, percent1, usd } from "@/lib/format"
import { fill, useCopy } from "@/lib/locale"
import type { UsageTotals } from "@/lib/types"

export function UsageHeadline({ totals }: { totals: UsageTotals }) {
  const h = useCopy().evaluation.headline
  return (
    <div className="metrics-grid usage-headline">
      <Metric label={h.cost} value={usd(totals.calls ? totals.cost_usd : null)}
              detail={fill(h.costDetail, { calls: totals.calls })} icon={<Coins size={19} />} />
      <Metric label={h.perTicket} value={usd(totals.cost_per_ticket_avg)}
              detail={fill(h.perTicketDetail, { value: usd(totals.cost_per_ticket_p95) })} icon={<Receipt size={19} />} />
      <Metric label={h.time} value={msLabel(totals.ai_time_p50_ms)}
              detail={fill(h.timeDetail, { value: msLabel(totals.ai_time_p95_ms) })} icon={<Clock3 size={19} />} />
      <Metric label={h.errors} value={percent1(totals.error_rate)}
              detail={fill(h.errorsDetail, { count: totals.errors })} icon={<AlertTriangle size={19} />} />
      <Metric label={h.tickets} value={totals.tickets}
              detail={fill(h.ticketsDetail, { count: totals.unknown_cost_calls })} icon={<Ticket size={19} />} />
    </div>
  )
}
```

```tsx
// GroupTable.tsx
import { Badge } from "@/components/ui/badge"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table"
import { countLabel, msLabel, percent1, usd } from "@/lib/format"
import { useCopy } from "@/lib/locale"
import type { AiSummary, UsageGroup } from "@/lib/types"
import { CostValue } from "./CostValue"
import { isInUse, processLabel, shareWidth } from "./usage-view"

export function GroupTable({ kind, groups, ai }: { kind: "process" | "model"; groups: UsageGroup[]; ai?: AiSummary }) {
  const copy = useCopy().evaluation
  const t = copy.table
  return (
    <Card className="data-card usage-groups">
      <CardHeader>
        <CardTitle>{kind === "process" ? copy.byProcess : copy.byModel}</CardTitle>
      </CardHeader>
      <CardContent>
        {!groups.length ? (
          <p className="muted small">{t.empty}</p>
        ) : (
          <div className="usage-scroll">
            <Table>
              <TableHeader>
                <TableRow>
                  <TableHead>{kind === "process" ? t.process : t.model}</TableHead>
                  {kind === "model" && <TableHead>{t.serves}</TableHead>}
                  <TableHead>{t.calls}</TableHead>
                  <TableHead>{t.cost}</TableHead>
                  <TableHead title={copy.metricHelp.share}>{t.share}</TableHead>
                  <TableHead>{t.perCall}</TableHead>
                  <TableHead title={copy.metricHelp.p50}>{t.p50}</TableHead>
                  <TableHead title={copy.metricHelp.p95}>{t.p95}</TableHead>
                  <TableHead title={copy.metricHelp.errors}>{t.errors}</TableHead>
                  <TableHead>{t.tokens}</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {groups.map((g) => (
                  <TableRow key={g.key}>
                    <TableCell>
                      {kind === "process" ? (
                        processLabel(g.process ?? g.key, copy)
                      ) : (
                        <span className="usage-model">
                          <bdi dir="ltr">{g.key}</bdi>
                          {g.locality === "local" && <Badge variant="secondary">{t.local}</Badge>}
                          {isInUse(g, ai) && <Badge variant="outline">{t.inUse}</Badge>}
                        </span>
                      )}
                    </TableCell>
                    {kind === "model" && (
                      <TableCell>{(g.processes ?? []).map((p) => processLabel(p, copy)).join("، ")}</TableCell>
                    )}
                    <TableCell>{countLabel(g.calls)}</TableCell>
                    <TableCell><CostValue value={g.cost_usd} sources={g.cost_sources} /></TableCell>
                    <TableCell>
                      <span className="usage-share"><span style={{ width: shareWidth(g.cost_share) }} /></span>
                      <small>{percent1(g.cost_share)}</small>
                    </TableCell>
                    <TableCell>{usd(g.cost_per_call)}</TableCell>
                    <TableCell>{msLabel(g.latency_p50_ms)}</TableCell>
                    <TableCell>{msLabel(g.latency_p95_ms)}</TableCell>
                    <TableCell className={g.error_rate ? "error-text" : undefined}>{percent1(g.error_rate)}</TableCell>
                    <TableCell>{countLabel(g.input_tokens)} / {countLabel(g.output_tokens)}</TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </div>
        )}
      </CardContent>
    </Card>
  )
}
```

The separator `"، "` is the Arabic comma; it reads acceptably in English too. If the reviewer prefers, add `evaluation.table.separator` to both locale files (`", "` / `"، "`) and use it.

- [ ] **Step 4: Implement `DailyTrend.tsx` and `UnattributedCard.tsx`**

```tsx
// DailyTrend.tsx
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { msLabel, usd } from "@/lib/format"
import { useCopy } from "@/lib/locale"
import type { UsageDay } from "@/lib/types"
import { trendGeometry } from "./usage-view"

export function DailyTrend({ days }: { days: UsageDay[] }) {
  const copy = useCopy().evaluation.trend
  const g = trendGeometry(days)
  return (
    <Card className="data-card usage-trend">
      <CardHeader>
        <CardTitle>{copy.title}</CardTitle>
      </CardHeader>
      <CardContent>
        {!days.length ? (
          <p className="muted small">{copy.empty}</p>
        ) : (
          <>
            <svg viewBox={`0 0 ${g.width} ${g.height + 20}`} role="img" aria-label={copy.title} dir="ltr">
              {g.bars.map((bar) => (
                <g key={bar.day.date}>
                  <rect className="usage-bar" x={bar.x} y={bar.y} width={24} height={g.height - bar.y}>
                    <title>{`${bar.day.date} · ${usd(bar.day.cost_usd)}`}</title>
                  </rect>
                  <text x={bar.x + 12} y={g.height + 14} textAnchor="middle">{bar.day.date.slice(5)}</text>
                </g>
              ))}
              <path className="usage-line" d={g.line} fill="none" />
            </svg>
            <table className="sr-only">
              <thead>
                <tr><th>{copy.date}</th><th>{copy.cost}</th><th>{copy.p95}</th></tr>
              </thead>
              <tbody>
                {days.map((d) => (
                  <tr key={d.date}><td>{d.date}</td><td>{usd(d.cost_usd)}</td><td>{msLabel(d.latency_p95_ms)}</td></tr>
                ))}
              </tbody>
            </table>
            <p className="usage-legend">
              <span className="usage-legend-bar" /> {copy.cost} <span className="usage-legend-line" /> {copy.p95}
            </p>
          </>
        )}
      </CardContent>
    </Card>
  )
}
```

```tsx
// UnattributedCard.tsx
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { countLabel } from "@/lib/format"
import { useCopy } from "@/lib/locale"
import type { UsageSummary } from "@/lib/types"
import { CostValue } from "./CostValue"
import { processLabel } from "./usage-view"

export function UnattributedCard({ data }: { data: UsageSummary["unattributed"] }) {
  const copy = useCopy().evaluation
  return (
    <Card className="data-card">
      <CardHeader>
        <CardTitle>{copy.unattributed.title}</CardTitle>
      </CardHeader>
      <CardContent>
        <p className="field-help">{copy.unattributed.body}</p>
        {!data.by_process.length ? (
          <p className="muted small">{copy.unattributed.empty}</p>
        ) : (
          <div className="simple-breakdown">
            {data.by_process.map((g) => (
              <div key={g.key}>
                <span>{processLabel(g.process ?? g.key, copy)} · {countLabel(g.calls)}</span>
                <strong><CostValue value={g.cost_usd} sources={g.cost_sources} /></strong>
              </div>
            ))}
          </div>
        )}
      </CardContent>
    </Card>
  )
}
```

- [ ] **Step 5: Run checks**

Run: `npm test -- src/features/evaluation && npm run lint && npm run typecheck` — Expected: all PASS.

- [ ] **Step 6: Commit**

```bash
git add employee-frontend/src/features/evaluation
git commit -m "feat: show AI cost and time by process, model and day"
```

---

### Task 15: Ticket cost table and AI timeline

**Files:**
- Create: `employee-frontend/src/features/evaluation/TicketCostTable.tsx`, `TicketTimeline.tsx`
- Test: `employee-frontend/src/features/evaluation/tickets.test.tsx`

**Interfaces:**
- Consumes: Tasks 12–14 (`CostValue`, `costSegments`, `waterfall`, `processLabel`); `StatusBadge`, `FilterSelect`, `LoadingState`; `Dialog*`; `useResource`; `categoryLabel`, `dateLabel`, `timeLabel`.
- Produces:
  - `TicketCostTable({ page, sort, onSort, offset, limit, onPage, onOpen }: { page: UsageTicketPage; sort: "recent" | "cost" | "time"; onSort: (s) => void; offset: number; limit: number; onPage: (offset: number) => void; onOpen: (resultId: number) => void })`
  - `TimelineView({ data }: { data: TicketCalls })`
  - `TicketTimeline({ resultId, onClose }: { resultId: number | null; onClose: () => void })`

- [ ] **Step 1: Write the failing tests**

Create `employee-frontend/src/features/evaluation/tickets.test.tsx`:

```tsx
import { renderToStaticMarkup } from "react-dom/server"
import { afterEach, expect, it } from "vitest"
import { getLocale, setLocale } from "@/lib/locale"
import { ticketCalls, ticketPage } from "./fixtures"
import { TicketCostTable } from "./TicketCostTable"
import { TimelineView } from "./TicketTimeline"

const originalLocale = getLocale()
afterEach(() => setLocale(originalLocale))

function table() {
  return renderToStaticMarkup(
    <TicketCostTable page={ticketPage} sort="cost" onSort={() => {}} offset={0} limit={25}
                     onPage={() => {}} onOpen={() => {}} />
  )
}

it("lists tickets with cost split, AI time and an open button", () => {
  setLocale("en")
  const html = table()
  expect(html).toContain("INTAKE-ab12")
  expect(html).toContain("$0.0160")
  expect(html).toContain("incl. intake $0.00400")
  expect(html).toContain("2.0 s")
  expect(html).toContain('aria-label="Open the AI timeline of INTAKE-ab12"')
  expect(html).toContain("1–2 of 2")
})

it("TicketCostTable marks rows without recorded detail", () => {
  setLocale("ar")
  const html = table()
  expect(html).toContain("التفاصيل غير مسجلة")
  expect(html).not.toContain("Detail not recorded")
})

it("renders the timeline in order with errors and local cost", () => {
  setLocale("en")
  const html = renderToStaticMarkup(<TimelineView data={ticketCalls} />)
  const order = ["Customer intake", "Classification (Jev)", "Detail extraction"].map((label) => html.indexOf(label))
  expect(order).toEqual([...order].sort((a, b) => a - b))
  expect(html).toContain("TimeoutError")
  expect(html).toContain("attempt 2")
  expect(html).toContain("Local · $0")
  expect(html).toContain("usage-bar-error")
  expect(html).toContain("1,200 in / 300 out")
})
```

Run: `npm test -- src/features/evaluation/tickets.test.tsx` — Expected: FAIL (modules not found).

- [ ] **Step 2: Implement `TicketCostTable.tsx`**

```tsx
import { ChevronLeft, ChevronRight, ListTree } from "lucide-react"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table"
import { FilterSelect, StatusBadge } from "@/components/shared/workspace-ui"
import { categoryLabel, dateLabel, msLabel, timeLabel, usd } from "@/lib/format"
import { fill, useCopy } from "@/lib/locale"
import type { UsageTicketPage } from "@/lib/types"
import { costSegments, processLabel } from "./usage-view"

type Sort = "recent" | "cost" | "time"

export function TicketCostTable({ page, sort, onSort, offset, limit, onPage, onOpen }: {
  page: UsageTicketPage
  sort: Sort
  onSort: (sort: Sort) => void
  offset: number
  limit: number
  onPage: (offset: number) => void
  onOpen: (resultId: number) => void
}) {
  const copy = useCopy().evaluation
  const t = copy.tickets
  return (
    <Card className="data-card usage-tickets">
      <CardHeader className="usage-tickets-header">
        <CardTitle>{t.title}</CardTitle>
        <FilterSelect label={t.sort} value={sort}
          options={[{ value: "recent", label: t.sortRecent }, { value: "cost", label: t.sortCost },
                    { value: "time", label: t.sortTime }]}
          onChange={(value) => onSort(value as Sort)} />
      </CardHeader>
      <CardContent>
        {!page.items.length ? (
          <p className="muted small">{t.empty}</p>
        ) : (
          <>
            <div className="usage-scroll">
              <Table>
                <TableHeader>
                  <TableRow>
                    <TableHead>{t.ticket}</TableHead>
                    <TableHead>{t.received}</TableHead>
                    <TableHead>{t.status}</TableHead>
                    <TableHead>{t.category}</TableHead>
                    <TableHead>{t.cost}</TableHead>
                    <TableHead>{t.breakdown}</TableHead>
                    <TableHead>{t.aiTime}</TableHead>
                    <TableHead>{t.draftTime}</TableHead>
                    <TableHead>{t.errors}</TableHead>
                    <TableHead />
                  </TableRow>
                </TableHeader>
                <TableBody>
                  {page.items.map((item) => (
                    <TableRow key={item.result_id}>
                      <TableCell><bdi dir="ltr" className="ticket-id">{item.external_id}</bdi></TableCell>
                      <TableCell>
                        {dateLabel(item.received_at)}
                        <small className="block-muted">{timeLabel(item.received_at)}</small>
                      </TableCell>
                      <TableCell><StatusBadge status={item.status} /></TableCell>
                      <TableCell>{categoryLabel(item.category)}</TableCell>
                      <TableCell>
                        {usd(item.total_cost_usd)}
                        {item.intake_cost_usd > 0 && (
                          <small className="block-muted">{fill(t.intake, { value: usd(item.intake_cost_usd) })}</small>
                        )}
                      </TableCell>
                      <TableCell>
                        {item.detail_recorded ? (
                          <span className="usage-stack">
                            {costSegments(item.cost_by_process).map((s) => (
                              <span key={s.process} className={`usage-seg usage-seg-${s.process}`}
                                    style={{ width: `${s.share * 100}%` }}
                                    title={`${processLabel(s.process, copy)} · ${usd(item.cost_by_process[s.process])}`} />
                            ))}
                          </span>
                        ) : (
                          <small className="muted">{t.notRecorded}</small>
                        )}
                      </TableCell>
                      <TableCell>{msLabel(item.ai_time_ms)}</TableCell>
                      <TableCell>{msLabel(item.draft_time_ms)}</TableCell>
                      <TableCell className={item.errors ? "error-text" : undefined}>{item.errors}</TableCell>
                      <TableCell>
                        <Button variant="ghost" size="icon-sm" onClick={() => onOpen(item.result_id)}
                                aria-label={fill(t.open, { id: item.external_id })}>
                          <ListTree size={15} />
                        </Button>
                      </TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            </div>
            <div className="usage-pager">
              <span>{fill(t.range, { from: offset + 1, to: offset + page.items.length, total: page.total })}</span>
              <Button variant="outline" size="icon-sm" aria-label={t.previous} disabled={offset === 0}
                      onClick={() => onPage(Math.max(0, offset - limit))}>
                <ChevronRight className="rtl-flip" size={15} />
              </Button>
              <Button variant="outline" size="icon-sm" aria-label={t.next}
                      disabled={offset + page.items.length >= page.total} onClick={() => onPage(offset + limit)}>
                <ChevronLeft className="rtl-flip" size={15} />
              </Button>
            </div>
          </>
        )}
      </CardContent>
    </Card>
  )
}
```

If `size="icon-sm"` is not a `Button` size in `src/components/ui/button.tsx`, use the smallest icon size it defines (check the `size` variants there).

- [ ] **Step 3: Implement `TicketTimeline.tsx`**

```tsx
import { Button } from "@/components/ui/button"
import { Dialog, DialogContent, DialogFooter, DialogHeader, DialogTitle } from "@/components/ui/dialog"
import { ErrorState, LoadingState } from "@/components/shared/workspace-ui"
import { useResource } from "@/hooks/use-resource"
import { countLabel, msLabel, usd } from "@/lib/format"
import { fill, useCopy } from "@/lib/locale"
import type { TicketCalls } from "@/lib/types"
import { CostValue } from "./CostValue"
import { processLabel, waterfall } from "./usage-view"

export function TimelineView({ data }: { data: TicketCalls }) {
  const copy = useCopy().evaluation
  const tl = copy.timeline
  if (!data.calls.length) return <p className="muted small">{tl.empty}</p>
  const total = data.calls.reduce((sum, c) => sum + c.cost_usd, 0)
  return (
    <div className="usage-timeline">
      <p className="field-help">
        {fill(tl.total, { calls: data.calls.length, cost: usd(total), time: msLabel(data.result.ai_time_ms) })}
      </p>
      {waterfall(data.calls).map(({ call, left, width }) => (
        <div key={call.id} className="usage-timeline-row">
          <div className="usage-timeline-label">
            <strong>{processLabel(call.process, copy)}</strong>
            <bdi dir="ltr">{call.model}</bdi>
            {call.attempt > 1 && <small>{fill(tl.attempt, { n: call.attempt })}</small>}
          </div>
          <div className="usage-track" dir="ltr">
            <span className={call.status === "error" ? "usage-bar-error" : "usage-bar-ok"}
                  style={{ left: `${left}%`, width: `${width}%` }} />
          </div>
          <div className="usage-timeline-meta">
            <span>{msLabel(call.latency_ms)}</span>
            <span>{fill(tl.tokens, { in: countLabel(call.input_tokens), out: countLabel(call.output_tokens) })}</span>
            <CostValue value={call.cost_usd} sources={{ [call.cost_source]: 1 }} />
            {call.error && <span className="error-text">{tl.error}: <bdi dir="ltr">{call.error}</bdi></span>}
          </div>
        </div>
      ))}
    </div>
  )
}

export function TicketTimeline({ resultId, onClose }: { resultId: number | null; onClose: () => void }) {
  const copy = useCopy().evaluation.timeline
  const data = useResource<TicketCalls>(resultId === null ? null : `/ai-usage/tickets/${resultId}/calls`)
  return (
    <Dialog open={resultId !== null} onOpenChange={(open) => { if (!open) onClose() }}>
      <DialogContent className="usage-dialog" showCloseButton={false}>
        <DialogHeader>
          <DialogTitle>
            {data.data ? fill(copy.title, { id: data.data.result.external_id }) : copy.loading}
          </DialogTitle>
        </DialogHeader>
        {data.error ? (
          <ErrorState message={data.error} retry={data.reload} />
        ) : !data.data ? (
          <LoadingState />
        ) : (
          <TimelineView data={data.data} />
        )}
        <DialogFooter>
          <Button variant="outline" onClick={onClose}>{copy.close}</Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  )
}
```

In `TimelineView`, the cost-source marker for a single local call renders `Local · $0` (via `CostValue`), which the test expects.

- [ ] **Step 4: Run checks**

Run: `npm test -- src/features/evaluation && npm run lint && npm run typecheck` — Expected: all PASS.

- [ ] **Step 5: Commit**

```bash
git add employee-frontend/src/features/evaluation
git commit -m "feat: list every ticket's AI cost and show its call timeline"
```

---

### Task 16: Page assembly, route, styles

**Files:**
- Create: `employee-frontend/src/features/evaluation/EvaluationPage.tsx`
- Delete: `employee-frontend/src/features/insights/EvaluationPage.tsx`
- Modify: `employee-frontend/src/App.tsx` (lazy import path)
- Modify: `employee-frontend/src/styles/workspace.css` (append usage styles)
- Test: `employee-frontend/src/features/evaluation/page.test.tsx`

**Interfaces:**
- Consumes: everything above; `useWorkspace().health?.ai`.
- Produces: `EvaluationPage()` at `/evaluation`.

- [ ] **Step 1: Write the failing test**

Create `employee-frontend/src/features/evaluation/page.test.tsx`:

```tsx
import { renderToStaticMarkup } from "react-dom/server"
import { MemoryRouter } from "react-router-dom"
import { afterEach, expect, it } from "vitest"
import { getLocale, setLocale } from "@/lib/locale"
import { WorkspaceContext } from "@/lib/workspace"
import { EvaluationPage } from "./EvaluationPage"

const originalLocale = getLocale()
afterEach(() => setLocale(originalLocale))

it("renders the page shell in Arabic without the old placeholder", () => {
  setLocale("ar")
  const html = renderToStaticMarkup(
    <MemoryRouter>
      <WorkspaceContext.Provider value={{
        revision: 0, refresh: () => {}, connectionError: null, notify: () => {},
        health: { database: "connected", configured_modes: ["jev"],
                  capabilities: { drafting: false, rag_indexing: false, evaluation: true } },
      }}>
        <EvaluationPage />
      </WorkspaceContext.Provider>
    </MemoryRouter>
  )
  expect(html).toContain("التقييم")
  expect(html).toContain("تكلفة وزمن استجابة كل عملية ذكاء اصطناعي.")
  expect(html).toContain("تحديث")
  for (const old of ["Import results", "Classification strategy", "Not run", "Expected report format"])
    expect(html, old).not.toContain(old)
})
```

Run: `npm test -- src/features/evaluation/page.test.tsx` — Expected: FAIL (module not found).

- [ ] **Step 2: Implement `EvaluationPage.tsx`**

```tsx
import { useEffect, useMemo, useState } from "react"
import { ErrorState, LoadingState, PageHeader } from "@/components/shared/workspace-ui"
import { useResource } from "@/hooks/use-resource"
import { useCopy } from "@/lib/locale"
import type { Run, UsageFilters as Filters, UsageSummary, UsageTicketPage } from "@/lib/types"
import { useWorkspace } from "@/lib/workspace"
import { DailyTrend } from "./DailyTrend"
import { GroupTable } from "./GroupTable"
import { TicketCostTable } from "./TicketCostTable"
import { TicketTimeline } from "./TicketTimeline"
import { UnattributedCard } from "./UnattributedCard"
import { UsageFilters } from "./UsageFilters"
import { UsageHeadline } from "./UsageHeadline"
import { periodRange, usageQuery } from "./usage-view"

const REFRESH_MS = 30_000
const PAGE_SIZE = 25

export function EvaluationPage() {
  const copy = useCopy()
  const workspace = useWorkspace()
  const [filters, setFilters] = useState<Filters>({ period: "7d", process: "all", model: "", runId: "" })
  const [sort, setSort] = useState<"recent" | "cost" | "time">("recent")
  const [offset, setOffset] = useState(0)
  const [open, setOpen] = useState<number | null>(null)
  const [now, setNow] = useState(() => Date.now())

  useEffect(() => {
    const timer = setInterval(() => setNow(Date.now()), REFRESH_MS)
    return () => clearInterval(timer)
  }, [])

  // The range only moves on refresh, so queries stay stable between refreshes.
  const range = useMemo(() => periodRange(filters.period, now), [filters.period, now])
  const query = usageQuery(filters, range)
  const summary = useResource<UsageSummary>(`/ai-usage/summary?${query}`, workspace.revision)
  const tickets = useResource<UsageTicketPage>(
    `/ai-usage/tickets?${usageQuery(filters, range, { sort, limit: PAGE_SIZE, offset })}`, workspace.revision)
  const runs = useResource<Run[]>("/runs", workspace.revision)

  const change = (next: Filters) => {
    setFilters(next)
    setOffset(0)
  }

  return (
    <>
      <PageHeader title={copy.pages.evaluationTitle} description={copy.pages.evaluationDescription} />
      <UsageFilters filters={filters} onChange={change}
                    models={(summary.data?.by_model ?? []).map((g) => g.key)}
                    runs={(runs.data ?? []).slice(0, 50).map((r) => r.id)}
                    onRefresh={() => setNow(Date.now())} />
      {summary.error && <ErrorState message={summary.error} retry={summary.reload} />}
      {!summary.data ? (
        !summary.error && <LoadingState />
      ) : (
        <>
          <UsageHeadline totals={summary.data.totals} />
          <div className="two-column">
            <GroupTable kind="process" groups={summary.data.by_process} />
            <DailyTrend days={summary.data.daily} />
          </div>
          <GroupTable kind="model" groups={summary.data.by_model} ai={workspace.health?.ai} />
        </>
      )}
      {tickets.error && <ErrorState message={tickets.error} retry={tickets.reload} />}
      {tickets.data && (
        <TicketCostTable page={tickets.data} sort={sort}
                         onSort={(value) => { setSort(value); setOffset(0) }}
                         offset={offset} limit={PAGE_SIZE} onPage={setOffset} onOpen={setOpen} />
      )}
      {summary.data && <UnattributedCard data={summary.data.unattributed} />}
      <TicketTimeline resultId={open} onClose={() => setOpen(null)} />
    </>
  )
}
```

- [ ] **Step 3: Route, cleanup and styles**

In `employee-frontend/src/App.tsx`, change the `EvaluationPage` lazy import path from `@/features/insights/EvaluationPage` to `@/features/evaluation/EvaluationPage`.

Delete the placeholder and its now-unused helpers:

```bash
git rm employee-frontend/src/features/insights/EvaluationPage.tsx
```

Then `grep -rn "validateEvaluation\|EvaluationReport" employee-frontend/src`. If nothing else uses them, remove `validateEvaluation` from `src/lib/imports.ts`, its test block in `src/lib/imports.test.ts`, and the `EvaluationReport` type from `src/lib/types.ts`. Remove the CSS rules that only served the old page (`.evaluation-intro`, `.evaluation-icon`, `.model-comparison`, `.evaluation-checklist`, `.report-schema`, `.report-provenance`, `.confusion-list`) after confirming with `grep -rn "<class>" employee-frontend/src --include=*.tsx` that no other component uses them.

Append to `employee-frontend/src/styles/workspace.css`:

```css
/* AI usage dashboard (/evaluation) */
.usage-filters {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  align-items: center;
  margin-bottom: 12px;
}
.usage-headline {
  grid-template-columns: repeat(auto-fit, minmax(170px, 1fr));
}
.usage-scroll {
  overflow-x: auto;
}
.usage-groups th,
.usage-groups td,
.usage-tickets th,
.usage-tickets td {
  white-space: nowrap;
}
.usage-model {
  display: inline-flex;
  gap: 6px;
  align-items: center;
}
.usage-share {
  display: inline-block;
  width: 64px;
  height: 6px;
  border-radius: 3px;
  background: var(--border);
  margin-inline-end: 6px;
  vertical-align: middle;
  overflow: hidden;
}
.usage-share > span {
  display: block;
  height: 100%;
  background: var(--accent-ink);
}
.usage-mark {
  color: var(--muted-foreground);
}
.usage-local {
  color: var(--green);
  font-weight: 600;
}
.usage-trend svg {
  width: 100%;
  max-height: 180px;
}
.usage-trend text {
  font-size: 9px;
  fill: var(--muted-foreground);
}
.usage-bar {
  fill: color-mix(in srgb, var(--accent-ink) 60%, transparent);
}
.usage-line {
  stroke: var(--blue);
  stroke-width: 2;
}
.usage-legend {
  display: flex;
  gap: 6px;
  align-items: center;
  font-size: 12px;
  color: var(--muted-foreground);
}
.usage-legend-bar,
.usage-legend-line {
  display: inline-block;
  width: 12px;
  height: 8px;
  background: color-mix(in srgb, var(--accent-ink) 60%, transparent);
}
.usage-legend-line {
  height: 2px;
  background: var(--blue);
}
.usage-tickets-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.usage-stack {
  display: flex;
  width: 120px;
  height: 8px;
  border-radius: 4px;
  overflow: hidden;
  background: var(--border);
}
.usage-seg-intake { background: #7c5cc4; }
.usage-seg-classify { background: var(--blue); }
.usage-seg-extract { background: #2f9aa0; }
.usage-seg-draft { background: var(--accent-ink); }
.usage-seg-draft_search { background: var(--amber); }
.usage-seg-credential_check { background: var(--green); }
.usage-pager {
  display: flex;
  justify-content: flex-end;
  align-items: center;
  gap: 8px;
  margin-top: 8px;
  font-size: 12px;
}
html[dir="rtl"] .rtl-flip {
  transform: scaleX(-1);
}
.usage-dialog {
  max-width: min(760px, calc(100% - 2rem)) !important;
}
.usage-timeline {
  display: grid;
  gap: 8px;
  max-height: 60vh;
  overflow-y: auto;
}
.usage-timeline-row {
  display: grid;
  grid-template-columns: minmax(150px, 1fr) 2fr;
  gap: 4px 12px;
  align-items: center;
}
.usage-timeline-label {
  display: flex;
  flex-direction: column;
  font-size: 12px;
}
.usage-timeline-meta {
  grid-column: 1 / -1;
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  font-size: 12px;
  color: var(--muted-foreground);
}
.usage-track {
  position: relative;
  height: 10px;
  background: var(--border);
  border-radius: 5px;
}
.usage-track > span {
  position: absolute;
  top: 0;
  bottom: 0;
  border-radius: 5px;
}
.usage-bar-ok { background: var(--blue); }
.usage-bar-error { background: var(--accent-ink); }
```

The `rtl-flip` class makes the pager chevrons point the right way in Arabic. If the workspace already has an equivalent class (`grep -n "scaleX(-1)" src/styles/workspace.css`), reuse it instead.

- [ ] **Step 4: Run all frontend checks**

Run: `npm test && npm run lint && npm run typecheck && npm run build` — Expected: all PASS.

- [ ] **Step 5: Commit**

```bash
git add -A employee-frontend/src
git commit -m "feat: rebuild /evaluation as the AI cost and response time dashboard"
```

---

### Task 17: Documentation, full verification and manual check

**Files:**
- Modify: `README.md`

- [ ] **Step 1: Document the dashboard**

Add to `README.md` (near the workspace pages description):

```markdown
### AI usage and performance (`/evaluation`)

Every AI call is recorded in the `ai_calls` table:
- customer intake, Jev classification, detail extraction and reply drafting;
- knowledge search during drafting and the credential check;
- knowledge indexing, manual knowledge search and admin model tests.

Each row holds the model, start time, latency, tokens, cost, cost source (provider-reported,
estimated, local or unknown) and errors. Prompts and ticket text are never stored.

The Evaluation page shows, for a chosen period, process, model or batch run:
- total AI cost, cost per ticket and AI time per ticket;
- cost and time by process and by model, with local models shown as **Local · $0**;
- a daily trend;
- every ticket with its cost split and a timeline of its AI calls.

Estimates use the price saved with the admin's model choice (taken from the OpenRouter
catalog), or the `.env` prices for the default models; any other model shows "Price unknown".
Results processed before tracking began show only their totals.
```

- [ ] **Step 2: Full automated verification**

From `backend/` (with `docker compose up -d db`): `uv run pytest -q` and `uv run ruff check app tests`.
From `employee-frontend/`: `npm test`, `npm run lint`, `npm run typecheck`, `npm run build`.
Expected: every command passes. Note the pass counts in the commit message.

- [ ] **Step 3: Commit**

```bash
git add README.md
git commit -m "docs: describe the AI usage and performance dashboard"
```

- [ ] **Step 4: Manual check (with your human partner)**

These steps use real providers; confirm with your human partner before running them.

1. Start the stack (`docker compose up -d db`, API on 8000, `npm run dev` for both frontends).
2. Run a small batch from `/runs/new` and complete one customer intake conversation through to submission.
3. Open `http://localhost:5173/evaluation` in Arabic:
   - no English UI text is left;
   - the headline totals match the run's cost on `/runs/<id>` plus the intake cost;
   - the intake ticket's row shows "incl. intake …" and its timeline lists intake, classify, extract (if it ran) and draft calls in order.
4. In `/admin/models`, switch extract or draft to `ollama:qwen3:4b`, run another batch, and confirm that model appears in "by model" with **Local · $0** and its latency.
5. Upload and index one knowledge document, run a manual knowledge search, and run one model test. Confirm all three appear under "Not tied to a ticket".
6. Switch to English and back; check that the pager arrows point the right way in both directions.
