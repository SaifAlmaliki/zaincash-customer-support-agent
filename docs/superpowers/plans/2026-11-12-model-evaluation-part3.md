# Per-model Evaluation Implementation Plan — Part 3 of 3 (frontend, translations, verification)

> **Superseded (2026-11-14): do not execute.** Replaced by `docs/superpowers/specs/2026-11-14-ai-usage-dashboard-design.md` and its plan.

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Replace the import-only `/evaluation` page with a model comparison driven by stored runs (start, progress, cancel, comparison table, per-model detail, confusion drill-down), fully translated in Arabic and English, and translate the Runs and Run detail pages.

**Architecture:** Pure view helpers (`features/evaluation/eval-view.ts`) turn API runs or imported reports into an `EvaluationView` and comparison rows. Small presentational components render it; `EvaluationPage` wires data loading (`useResource` polling), the run dialog and the drawer. All text comes from `src/locales/{en,ar}.json`.

**Tech Stack:** React 19, TypeScript, Vite, base-ui/shadcn components in `src/components/ui`, lucide icons, Vitest with `renderToStaticMarkup` (the repo has no DOM testing library; interactive logic is tested through pure helpers and props).

**Spec:** `docs/superpowers/specs/2026-11-12-model-evaluation-design.md` §5. Parts 1 and 2 must be complete (the API in Part 2 Task 10 is what this part calls). Part 1's **Global Constraints** and **Review Focus** apply.

## Global Constraints

Same as Part 1. Repeated for the items this part touches:

- Every visible string comes from `en.json` / `ar.json`; both files keep identical keys (enforced by `src/locales/locales.test.ts`).
- Metric names render in the current language with the English term as a native `title` tooltip (e.g. Arabic "الاستدعاء", `title="Recall"`).
- Model IDs, hashes, prompt versions and the JSON example render with `dir="ltr"` (`<bdi dir="ltr">` inline, `dir="ltr"` on `<pre>`); ticket text renders with `dir="auto"`.
- `null` metric values render as "—", never 0.
- Local models show the badge **Local · $0**; Jev shows **Production**; failed models stay in the table with **Failed** and their error.
- Poll every 3000 ms while the selected run is `queued` or `running`.
- Frontend commands from `employee-frontend/`: `npm test`, `npm run lint`, `npm run typecheck`, `npm run build`.

---

### Task 12: Locale parity test and translated Runs pages

**Files:**
- Create: `employee-frontend/src/locales/locales.test.ts`
- Modify: `employee-frontend/src/locales/en.json`, `employee-frontend/src/locales/ar.json` (add `runs`, `runDetail`)
- Modify: `employee-frontend/src/features/runs/RunsPage.tsx` (export `RunsTable`, use copy)
- Modify: `employee-frontend/src/features/runs/RunDetailPage.tsx` (export `RunDetailView`, use copy)
- Test: `employee-frontend/src/features/runs/runs-i18n.test.tsx`

**Interfaces:**
- Consumes: `useCopy`, `fill` from `@/lib/locale`; `reasonLabel`, `categoryLabel` from `@/lib/format`.
- Produces: `export function RunsTable({ runs }: { runs: Run[] })`; `export function RunDetailView({ run, results, resultsError, resultsLoading }: { run: Run; results: Result[] | null; resultsError: string | null; resultsLoading: boolean })`.

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
  const arKeys = entries(ar).map(([key]) => key).sort()
  const enKeys = entries(en).map(([key]) => key).sort()
  expect(arKeys).toEqual(enKeys)
})

it("has no empty translations", () => {
  for (const [key, value] of [...entries(ar), ...entries(en)])
    expect(typeof value === "string" && value.trim().length > 0, key).toBe(true)
})
```

Run: `npm test -- src/locales/locales.test.ts`
Expected: PASS (both files currently match). It guards every later task.

- [ ] **Step 2: Add the `runs` and `runDetail` copy**

In `employee-frontend/src/locales/en.json`, add before the final `}` (after `"batch": {...}`, with a comma after its closing brace):

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

In `employee-frontend/src/locales/ar.json`, add in the same place:

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

const run: Run = {
  id: 7, started_at: "2026-11-01T09:00:00+03:00", finished_at: null, mode: "jev",
  status: "running", total: 4, processed: 2, degraded: false, total_cost_usd: 0.0123,
  counts: { by_status: { escalated: 1 }, by_category: { failed_transfer: 2 },
            escalation_reasons: { fraud_suspected: 1 }, latency_p50_ms: 1500 },
}

const ENGLISH = ["Batch #", "Started ·", "Classifier", "Estimated cost", "All pipeline runs",
  "Export summary", "Review tickets", "Preparing your tickets", "tickets processed",
  "Needs human review", "Median latency", "Issue breakdown", "Escalation reasons",
  "Steps appear here"]

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
  expect(markup).toContain("احتيال")
  for (const text of ENGLISH) expect(markup, text).not.toContain(text)
})

it("keeps the English copy in English", () => {
  setLocale("en")
  const markup = html()
  expect(markup).toContain("Batch #007")
  expect(markup).toContain("2 of 4 tickets processed")
})
```

Run: `npm test -- src/features/runs/runs-i18n.test.tsx`
Expected: FAIL (`RunsTable` / `RunDetailView` are not exported).

- [ ] **Step 4: Translate `RunsPage.tsx`**

Replace the body of `employee-frontend/src/features/runs/RunsPage.tsx` from `export function RunsPage()` to the end with:

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
            <TableCell>
              {run.mode === "cascade" ? copy.runs.classifierCascade : copy.runs.classifierJev}
            </TableCell>
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

Update imports in that file: `import { fill, useCopy } from "@/lib/locale"` and `import { dateLabel, timeLabel } from "@/lib/format"` (drop `humanize`).

- [ ] **Step 5: Translate `RunDetailPage.tsx`**

Replace `employee-frontend/src/features/runs/RunDetailPage.tsx` entirely with:

```tsx
import { Link, useParams } from "react-router-dom"
import { ArrowLeft, ArrowRight, CheckCheck, Clock3, Coins, Download, Layers3 } from "lucide-react"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { EmptyState, ErrorState, LoadingState, Metric, PageHeader, StatusBadge } from "@/components/shared/workspace-ui"
import { useResource } from "@/hooks/use-resource"
import { useWorkspace } from "@/lib/workspace"
import { fill, useCopy } from "@/lib/locale"
import { categoryLabel, dateLabel, downloadJson, duration, reasonLabel, timeLabel } from "@/lib/format"
import type { Result, Run } from "@/lib/types"
import { TicketFlow } from "@/features/review/TicketFlow"
import { loadRunResults } from "./run-results"

export function RunDetailPage() {
  const copy = useCopy()
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
  if (query.error) return <ErrorState message={query.error} retry={query.reload} />
  if (!run)
    return query.loading ? (
      <LoadingState />
    ) : (
      <EmptyState title={copy.runDetail.notFound} description={copy.runDetail.notFoundBody} />
    )
  return (
    <RunDetailView
      run={run}
      results={results.data}
      resultsError={results.error}
      resultsLoading={results.loading}
    />
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
  const batch = fill(copy.runs.batchName, { id: String(run.id).padStart(3, "0") })
  return (
    <>
      <Link to="/runs" className="back-link">
        <ArrowLeft size={15} />
        {text.back}
      </Link>
      <PageHeader
        title={batch}
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
            <h2>
              {run.status === "running"
                ? text.running
                : run.status === "failed"
                  ? text.interrupted
                  : text.finished}
            </h2>
            <StatusBadge status={run.status} />
          </div>
          <p>{fill(text.progress, { processed: run.processed, total: run.total })}</p>
          <div
            className="run-progress"
            role="progressbar"
            aria-label={text.progressLabel}
            aria-valuenow={progress}
            aria-valuemin={0}
            aria-valuemax={100}
          >
            <span style={{ width: `${progress}%` }} />
          </div>
          {run.counts.error && <p className="error-text">{run.counts.error}</p>}
          {run.degraded && run.mode === "cascade" && <p className="field-help">{text.degraded}</p>}
        </CardContent>
      </Card>
      <div className="metrics-grid">
        <Metric
          label={text.processed}
          value={run.processed}
          detail={fill(text.processedDetail, { total: run.total })}
          icon={<Layers3 size={18} />}
        />
        <Metric
          label={text.needsReview}
          value={run.counts.by_status?.escalated || 0}
          detail={text.needsReviewDetail}
          icon={<CheckCheck size={18} />}
          tone="metric-amber"
        />
        <Metric
          label={text.latency}
          value={duration(run.counts.latency_p50_ms || 0)}
          detail={text.latencyDetail}
          icon={<Clock3 size={18} />}
        />
        <Metric
          label={text.cost}
          value={`$${run.total_cost_usd.toFixed(4)}`}
          detail={text.costDetail}
          icon={<Coins size={18} />}
        />
      </div>
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

function Breakdown({
  values,
  label,
  empty,
}: {
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

`reasonLabel("fraud_suspected")` in Arabic comes from the existing `reasons` copy; check that `ar.json` `reasons.fraud_suspected` contains "احتيال" (it does in the current file — if the wording differs, change the test's `احتيال` expectation to a word from that value, not the copy).

- [ ] **Step 6: Run tests, lint and typecheck**

Run: `npm test && npm run lint && npm run typecheck`
Expected: all PASS.

- [ ] **Step 7: Commit**

```bash
git add employee-frontend/src/locales employee-frontend/src/features/runs
git commit -m "feat: translate pipeline run pages and enforce locale key parity"
```

---

### Task 13: Evaluation types, API client, formatters, copy and report import

**Files:**
- Modify: `employee-frontend/src/lib/types.ts`
- Modify: `employee-frontend/src/lib/api.ts`
- Modify: `employee-frontend/src/lib/format.ts`
- Modify: `employee-frontend/src/lib/imports.ts`
- Modify: `employee-frontend/src/locales/en.json`, `employee-frontend/src/locales/ar.json` (add `evaluation`)
- Test: `employee-frontend/src/lib/api.test.ts`, `employee-frontend/src/lib/imports.test.ts`, `employee-frontend/src/lib/format.test.ts`

**Interfaces:**
- Consumes: backend views from Part 2 Tasks 8 and 10.
- Produces:
  - Types: `EvalAvailability`, `EvalModel`, `EvalModelOption`, `Prf`, `EvalModelSummary`, `EvalModelStatus`, `EvalRun`, `EvalEstimate`, `EvalPrediction`, `EvalPredictionPage`, `EvaluationExportV2`, `ImportedReport` (shapes below). `Insights.evaluation` is removed.
  - `class ApiError extends Error { status: number; code?: string; detail?: { code?: string; model?: string | null; reason?: string | null; message?: string } }` thrown by `request` for non-2xx responses.
  - `evaluationsApi`: `models(signal?)`, `estimate(models, split)`, `start(models, split)`, `cancel(id)`, `predictions(id, query, signal?)`.
  - Formatters: `usd(value?: number | null) -> string`, `msLabel(value?: number | null) -> string`, `percent1(value?: number | null) -> string`, `countLabel(value?: number | null) -> string`.
  - `validateEvaluation(data: unknown): ImportedReport` with localized errors.
  - Copy keys under `evaluation.*` exactly as listed in Step 5.

- [ ] **Step 1: Write the failing tests**

Append to `employee-frontend/src/lib/api.test.ts`:

```ts
import { ApiError, evaluationsApi } from "./api"

it("exposes structured API error codes", async () => {
  vi.spyOn(globalThis, "fetch").mockResolvedValue(
    new Response(JSON.stringify({ detail: { code: "model_unavailable", message: "qwen down",
      model: "ollama:qwen3:4b", reason: "unreachable" } }), { status: 422 }),
  )
  const error = await evaluationsApi.start(["ollama:qwen3:4b"], "dev").catch((e) => e)
  expect(error).toBeInstanceOf(ApiError)
  expect(error).toMatchObject({ status: 422, code: "model_unavailable", message: "qwen down" })
  expect(error.detail.reason).toBe("unreachable")
})

it("builds prediction queries", async () => {
  const fetchMock = vi.spyOn(globalThis, "fetch").mockResolvedValue(
    new Response(JSON.stringify({ items: [], total: 0 }), { status: 200 }),
  )
  await evaluationsApi.predictions(4, { model: "ollama:qwen3:4b", gold: "app_bug", predicted: "error" })
  expect(String(fetchMock.mock.calls[0][0])).toBe(
    "/api/evaluations/4/predictions?model=ollama%3Aqwen3%3A4b&gold=app_bug&predicted=error&limit=50",
  )
})
```

(Move the new `import` line to the top of the file next to the existing import.)

Replace the `describe("evaluation evidence", ...)` block in `employee-frontend/src/lib/imports.test.ts` with:

```ts
describe("evaluation reports", () => {
  afterEach(() => setLocale(originalLocale))
  const v1 = {
    model: "test-model", split: "test", sample_size: 100, generated_at: "2026-10-07",
    classification_accuracy: 0.87, extraction_accuracy: 0.91, confusion_cases: [],
  }
  const v2 = {
    format: "zaincash-eval/v2", split: "test", sample_size: 100, generated_at: "2026-11-12",
    dataset_sha256: "abc", models: { jev: { classification: {}, system: {}, cost: {} } },
  }
  it("accepts the legacy and v2 formats", () => {
    expect(validateEvaluation(v1)).toMatchObject({ kind: "v1" })
    expect(validateEvaluation(v2)).toMatchObject({ kind: "v2" })
  })
  it("rejects invalid reports with translated messages", () => {
    setLocale("en")
    expect(() => validateEvaluation({ ...v1, classification_accuracy: 91 })).toThrow(/between 0 and 1/)
    expect(() => validateEvaluation({ ...v1, split: "dev" })).toThrow(/split: test/)
    expect(() => validateEvaluation({ ...v2, models: {} })).toThrow(/per-model results/)
    setLocale("ar")
    expect(() => validateEvaluation(null)).toThrow(/تقرير/)
  })
})
```

and add at the top of that file:

```ts
import { afterEach } from "vitest"
import { getLocale, setLocale } from "./locale"
const originalLocale = getLocale()
```

(merge `afterEach` into the existing `vitest` import.)

Create `employee-frontend/src/lib/format.test.ts`:

```ts
import { expect, it } from "vitest"
import { countLabel, msLabel, percent1, usd } from "./format"

it("formats evaluation numbers and keeps null as a dash", () => {
  expect(usd(null)).toBe("—")
  expect(usd(0)).toBe("$0")
  expect(usd(0.000412)).toBe("$0.00041")
  expect(usd(12.3456)).toBe("$12.35")
  expect(msLabel(undefined)).toBe("—")
  expect(msLabel(850)).toBe("850 ms")
  expect(msLabel(2500)).toBe("2.5 s")
  expect(percent1(0.8765)).toBe("87.7%")
  expect(percent1(null)).toBe("—")
  expect(countLabel(1534.4)).toBe("1,534")
})
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `npm test -- src/lib`
Expected: FAIL (missing exports `ApiError`, `evaluationsApi`, `usd`, ...; `validateEvaluation` returns no `kind`).

- [ ] **Step 3: Add the types**

In `employee-frontend/src/lib/types.ts`, delete the `evaluation: null` line from `Insights` and append:

```ts
export type EvalAvailability = "ready" | "missing_key" | "unreachable" | "model_missing"
export type EvalModel = {
  id: string
  provider: "typesafe" | "openrouter" | "ollama" | "imported"
  model: string
  locality: "cloud" | "local"
  price_in: number | null
  price_out: number | null
  concurrency: number
}
export type EvalModelOption = EvalModel & { availability: EvalAvailability }
export type Prf = {
  precision: number | null
  recall: number | null
  f1: number | null
  support: number
}
export type EvalModelSummary = {
  n: number
  classification: {
    accuracy: number | null
    accuracy_ci: [number, number] | null
    correct: number
    macro_precision: number | null
    macro_recall: number | null
    macro_f1: number | null
    per_category: Record<string, Prf>
    confusion: Record<string, Record<string, number>>
    priority_exact: number | null
    priority_within_one: number | null
  }
  flags: Record<string, Prf>
  extraction: {
    per_field: Record<string, Prf>
    micro_precision: number | null
    micro_recall: number | null
    micro_f1: number | null
    hallucination_rate: number | null
    missed_rate: number | null
  }
  escalation: {
    precision: number | null
    recall: number | null
    f1: number | null
    rate: number | null
    gold_rate: number | null
    coverage: number | null
    accuracy_not_escalated: number | null
  }
  system: {
    latency_p50_ms: number | null
    latency_p95_ms: number | null
    latency_mean_ms: number | null
    classifier_p50_ms: number | null
    classifier_p95_ms: number | null
    error_rate: number | null
    invalid_output_rate: number | null
    mean_input_tokens: number | null
    mean_output_tokens: number | null
    tokens_per_s: number | null
  }
  cost: {
    classifier_cost_per_request: number | null
    total_cost_per_request: number | null
    total_cost_usd: number
    cost_per_1k_tickets: number | null
    cost_sources: Record<string, number>
    local: boolean
  }
  slices: Record<string, { n: number; accuracy: number | null; error_rate: number | null }>
}
export type EvalModelStatus = {
  status: "pending" | "running" | "completed" | "failed" | "cancelled"
  error: string | null
}
export type EvalRun = {
  id: number
  status: "queued" | "running" | "completed" | "failed" | "cancelled"
  split: "dev" | "test"
  dataset_sha256: string
  prompt_version: string
  models: EvalModel[]
  model_status: Record<string, EvalModelStatus>
  progress: Record<string, { done: number; total: number }>
  estimated_cost_usd: number | null
  actual_cost_usd: number
  triggered_by: "ui" | "cli"
  cancel_requested: boolean
  error: string | null
  sample_size: number
  created_at: string
  started_at: string | null
  finished_at: string | null
  summary?: Record<string, EvalModelSummary>
}
export type EvalEstimate = {
  models: Record<string, { cost_usd: number | null; basis: string }>
  total_usd: number
  unknown: boolean
  approximate: boolean
  includes_gap_fill: boolean
  tickets: number
}
export type EvalLabels = {
  category: string
  priority: string
  escalated: boolean
  flags: Record<string, boolean>
  fields: Record<string, string | number | null>
  lookup: string | null
  reasons: string[]
}
export type EvalPrediction = {
  id: number
  ticket_id: string
  text: string
  tags: string[]
  gold: EvalLabels
  predicted: (EvalLabels & { confidence: number }) | null
  correct_category: boolean
  latency_ms: number
  cost_usd: number
  error: string | null
}
export type EvalPredictionPage = { items: EvalPrediction[]; total: number }
export type EvaluationExportV2 = {
  format: "zaincash-eval/v2"
  split: "dev" | "test"
  sample_size: number
  generated_at: string
  dataset_sha256: string
  prompt_version?: string
  models: Record<string, EvalModelSummary>
  model_info?: EvalModel[]
  model_status?: Record<string, EvalModelStatus>
}
export type ImportedReport =
  | { kind: "v1"; report: EvaluationReport }
  | { kind: "v2"; report: EvaluationExportV2 }
```

Search for other uses of `Insights["evaluation"]` / `.evaluation` on insights (`grep -rn "evaluation" src/features/insights/InsightsPage.tsx`) and remove them if any.

- [ ] **Step 4: Add `ApiError`, `evaluationsApi` and formatters**

In `employee-frontend/src/lib/api.ts`, add above `request`:

```ts
export class ApiError extends Error {
  status: number
  code?: string
  detail?: { code?: string; model?: string | null; reason?: string | null; message?: string }
  constructor(message: string, status: number, detail?: ApiError["detail"]) {
    super(message)
    this.status = status
    this.detail = detail
    this.code = detail?.code
  }
}
```

In `request`, replace the error branch with:

```ts
  if (!response.ok) {
    let message = `Request failed (${response.status}). Please retry.`
    let detail: ApiError["detail"]
    try {
      const body = await response.json()
      if (typeof body.detail === "string") message = body.detail
      else if (Array.isArray(body.detail))
        message = body.detail.map((error: { msg: string }) => error.msg).join(" ")
      else if (body.detail && typeof body.detail === "object") {
        detail = body.detail
        if (typeof body.detail.message === "string") message = body.detail.message
      }
    } catch {
      /* Proxies may return HTML when the API is offline. */
    }
    throw new ApiError(message, response.status, detail)
  }
```

Append to `api.ts` (and add the new types to its `import type` list):

```ts
export type PredictionQuery = {
  model: string
  gold?: string
  predicted?: string
  correct?: boolean
  limit?: number
  offset?: number
}

export const evaluationsApi = {
  models: (signal?: AbortSignal) =>
    request<EvalModelOption[]>("/evaluations/models", { signal }),
  estimate: (models: string[], split: "dev" | "test") =>
    request<EvalEstimate>("/evaluations/estimate", {
      method: "POST", body: JSON.stringify({ models, split }),
    }),
  start: (models: string[], split: "dev" | "test") =>
    request<EvalRun>("/evaluations", { method: "POST", body: JSON.stringify({ models, split }) }),
  cancel: (id: number) => request<EvalRun>(`/evaluations/${id}/cancel`, { method: "POST" }),
  predictions: (id: number, query: PredictionQuery, signal?: AbortSignal) => {
    const params = new URLSearchParams({ model: query.model })
    if (query.gold) params.set("gold", query.gold)
    if (query.predicted) params.set("predicted", query.predicted)
    if (query.correct !== undefined) params.set("correct", String(query.correct))
    params.set("limit", String(query.limit ?? 50))
    if (query.offset) params.set("offset", String(query.offset))
    return request<EvalPredictionPage>(`/evaluations/${id}/predictions?${params}`, { signal })
  },
}
```

In `employee-frontend/src/lib/format.ts`, append:

```ts
export const usd = (value?: number | null) =>
  value == null ? "—" : value === 0 ? "$0" : value < 0.01 ? `$${value.toFixed(5)}` : `$${value.toFixed(2)}`
export const msLabel = (value?: number | null) =>
  value == null ? "—" : duration(Math.round(value))
export const percent1 = (value?: number | null) =>
  value == null ? "—" : `${(value * 100).toFixed(1)}%`
export const countLabel = (value?: number | null) =>
  value == null ? "—" : Math.round(value).toLocaleString("en-US")
```

- [ ] **Step 5: Add the `evaluation` copy**

In `en.json`, add a top-level `"evaluation"` object (after `"runDetail"`):

```json
  "evaluation": {
    "run": "Run evaluation",
    "import": "Import report",
    "importLabel": "Import evaluation report",
    "importedNotice": "Imported report loaded. Its measurements come from the file and were not verified by this workspace.",
    "fileTooLarge": "Choose a report smaller than 2 MB.",
    "runSelect": "Evaluation run",
    "runOption": "#{id} · {split} · {date}",
    "importedOption": "Imported · {name}",
    "split": { "dev": "Development split", "test": "Held-out test split" },
    "status": { "queued": "Queued", "running": "Running", "completed": "Completed", "failed": "Failed", "cancelled": "Cancelled", "pending": "Waiting" },
    "intro": {
      "title": "A demo shows what’s possible. An evaluation shows what works.",
      "body": "No evaluation has been run yet. Run one to measure every model on the same held-out tickets, or import a measured report.",
      "briefTitle": "The Topic 06 brief asks for:",
      "brief1": "At least 200 synthetic Iraqi-dialect tickets",
      "brief2": "A labelled, held-out test split",
      "brief3": "Classification and extraction accuracy",
      "brief4": "A discussion of confusing and failed cases"
    },
    "provenance": {
      "tickets": "{count} tickets",
      "date": "{date} at {time} Baghdad",
      "dataset": "Dataset",
      "prompt": "Prompt",
      "fromUi": "Started from the workspace",
      "fromCli": "Started from the CLI",
      "imported": "Imported file {name} · not independently verified",
      "legacyExtraction": "Extraction accuracy in the report: {value}"
    },
    "headline": {
      "accuracy": "Best accuracy",
      "errors": "Lowest error rate",
      "cheapest": "Cheapest per request",
      "fastest": "Fastest response (p50)",
      "noData": "No results yet"
    },
    "table": {
      "title": "Model comparison",
      "model": "Model",
      "quality": "Task quality",
      "system": "System",
      "cost": "Cost",
      "accuracy": "Accuracy",
      "macroP": "Precision",
      "macroR": "Recall",
      "macroF1": "F1",
      "extractionF1": "Extraction F1",
      "escalationP": "Escalation precision",
      "escalationR": "Escalation recall",
      "fraudRecall": "Fraud recall",
      "p50": "p50",
      "p95": "p95",
      "errorRate": "Error rate",
      "tokens": "Tokens in / out",
      "tps": "Tokens/s",
      "costRequest": "$ / request",
      "cost1k": "$ / 1k tickets",
      "classifierCost": "classifier {value}",
      "production": "Production",
      "local": "Local · $0",
      "failed": "Failed",
      "best": "Best",
      "ciNote": "With {n} tickets, accuracy has a margin of about ±{points} points (95% confidence).",
      "costNote": "Cost uses provider-reported prices when available, otherwise tokens × configured prices. Local models run on your own hardware and are shown as $0.",
      "macroNote": "Precision, recall and F1 are averaged over issue categories."
    },
    "metricHelp": {
      "accuracy": "Accuracy",
      "macroP": "Macro precision",
      "macroR": "Macro recall",
      "macroF1": "Macro F1",
      "extractionF1": "Field extraction micro F1",
      "escalationP": "Escalation precision",
      "escalationR": "Escalation recall",
      "fraudRecall": "Fraud flag recall",
      "p50": "Median response time",
      "p95": "95th percentile response time",
      "errorRate": "Error rate",
      "tps": "Tokens per second",
      "costRequest": "Cost per request",
      "cost1k": "Cost per 1,000 tickets"
    },
    "detail": {
      "title": "Model detail",
      "model": "Model",
      "categories": "Categories",
      "confusion": "Confusion matrix",
      "flags": "Flags",
      "extraction": "Extraction",
      "slices": "Hard cases",
      "category": "Category",
      "flag": "Flag",
      "field": "Field",
      "slice": "Case type",
      "support": "Tickets",
      "precision": "Precision",
      "recall": "Recall",
      "f1": "F1",
      "accuracy": "Accuracy",
      "errorRate": "Error rate",
      "hallucination": "Invented values: {value}",
      "missed": "Missed values: {value}",
      "axes": "Correct ↓ · Predicted →",
      "error": "Error",
      "cellLabel": "{gold} predicted as {predicted}: {count} tickets",
      "matrixHelp": "Select a cell to see those tickets.",
      "selfReported": "Language-model confidence is self-reported and not calibrated.",
      "noSummary": "This model has no results."
    },
    "flagNames": {
      "fraud_suspected": "Fraud suspected",
      "money_lost": "Money lost",
      "multi_issue": "More than one issue",
      "urgent_or_angry": "Urgent or angry",
      "mentions_specific_transaction": "Mentions a transaction",
      "asks_for_human": "Asks for a person"
    },
    "fieldNames": {
      "txn_ref": "Transaction reference",
      "amount": "Amount",
      "phone": "Phone number",
      "date": "Date"
    },
    "tags": {
      "arabizi": "Arabizi",
      "mixed_english": "Arabic mixed with English",
      "multi_issue": "More than one issue",
      "missing_details": "Missing details",
      "prompt_injection": "Prompt injection",
      "angry": "Angry customer",
      "arabic_indic_digits": "Arabic-Indic digits",
      "amount_in_words": "Amount in words"
    },
    "drawer": {
      "title": "{gold} → {predicted}",
      "close": "Close",
      "loading": "Loading tickets…",
      "empty": "No tickets for this cell.",
      "gold": "Correct",
      "predicted": "Predicted",
      "escalated": "Escalated",
      "notEscalated": "Not escalated",
      "latency": "Response time",
      "cost": "Cost",
      "error": "Error",
      "shown": "{shown} of {total} shown"
    },
    "dialog": {
      "title": "Run an evaluation",
      "description": "Each selected model classifies the same tickets through the real pipeline. Drafting is skipped.",
      "models": "Models",
      "split": "Tickets",
      "testWarning": "Held-out tickets: do not tune prompts on these results.",
      "estimate": "Estimated cost",
      "estimating": "Estimating…",
      "total": "Total {value} (approximate, classification only)",
      "unknown": "Some prices are unknown and are not included in the total.",
      "start": "Start evaluation",
      "starting": "Starting…",
      "cancel": "Cancel",
      "noneSelected": "Choose at least one model.",
      "started": "Evaluation #{id} started.",
      "loadingModels": "Checking which models are available…"
    },
    "availability": {
      "ready": "Ready",
      "missing_key": "API key missing",
      "unreachable": "Not reachable",
      "model_missing": "Model not pulled"
    },
    "progress": {
      "title": "Evaluation #{id} in progress",
      "model": "{done} of {total}",
      "cancel": "Cancel evaluation",
      "cancelling": "Stopping after the current tickets…"
    },
    "errors": {
      "no_models": "Choose at least one model.",
      "unknown_model": "{model} is not configured for evaluation.",
      "model_unavailable": "{model} is not available: {reason}.",
      "dataset_missing": "The evaluation dataset has not been generated yet. Run “support eval-generate” in the backend.",
      "test_split_modified": "The held-out test file changed after it was locked. Restore it or regenerate the dataset.",
      "conflict": "An evaluation is already running.",
      "generic": "The evaluation could not be started."
    },
    "importErrors": {
      "object": "Choose a JSON evaluation report.",
      "v1Fields": "A report needs model, split: test, a positive sample_size and generated_at.",
      "accuracy": "Accuracy must be a number between 0 and 1.",
      "confusion": "confusion_cases must be a list of text descriptions.",
      "v2": "A v2 report needs split, sample_size, generated_at, dataset_sha256 and per-model results."
    },
    "schema": {
      "title": "Report format",
      "note": "Export a run in this format with “support eval --out report.json”. Imported files are not saved."
    },
    "notes": "Notes from the report"
  }
```

In `ar.json`, add the same keys:

```json
  "evaluation": {
    "run": "تشغيل التقييم",
    "import": "استيراد تقرير",
    "importLabel": "استيراد تقرير تقييم",
    "importedNotice": "تم تحميل التقرير المستورد. قياساته مأخوذة من الملف ولم تتحقق منها مساحة العمل.",
    "fileTooLarge": "اختر تقريراً أصغر من 2 ميغابايت.",
    "runSelect": "تشغيل التقييم",
    "runOption": "#{id} · {split} · {date}",
    "importedOption": "مستورد · {name}",
    "split": { "dev": "مجموعة التطوير", "test": "مجموعة الاختبار المحجوبة" },
    "status": { "queued": "في الانتظار", "running": "قيد التشغيل", "completed": "مكتمل", "failed": "فشل", "cancelled": "أُلغي", "pending": "بانتظار الدور" },
    "intro": {
      "title": "العرض التجريبي يُظهر ما هو ممكن. التقييم يُظهر ما ينجح فعلاً.",
      "body": "لم يُشغَّل أي تقييم بعد. شغّل تقييماً لقياس كل نموذج على نفس تذاكر الاختبار المحجوبة، أو استورد تقريراً مقاساً.",
      "briefTitle": "يطلب موجز الموضوع 06:",
      "brief1": "200 تذكرة اصطناعية على الأقل باللهجة العراقية",
      "brief2": "مجموعة اختبار محجوبة ومصنفة",
      "brief3": "دقة التصنيف واستخراج التفاصيل",
      "brief4": "مناقشة الحالات المربكة والفاشلة"
    },
    "provenance": {
      "tickets": "{count} تذكرة",
      "date": "{date} الساعة {time} بتوقيت بغداد",
      "dataset": "مجموعة البيانات",
      "prompt": "نص التعليمات",
      "fromUi": "بدأ من مساحة العمل",
      "fromCli": "بدأ من سطر الأوامر",
      "imported": "ملف مستورد {name} · لم يُتحقق منه بشكل مستقل",
      "legacyExtraction": "دقة الاستخراج في التقرير: {value}"
    },
    "headline": {
      "accuracy": "أعلى نسبة صواب",
      "errors": "أقل نسبة أخطاء",
      "cheapest": "الأرخص لكل طلب",
      "fastest": "الأسرع استجابة (الوسيط)",
      "noData": "لا توجد نتائج بعد"
    },
    "table": {
      "title": "مقارنة النماذج",
      "model": "النموذج",
      "quality": "جودة المهمة",
      "system": "النظام",
      "cost": "الكلفة",
      "accuracy": "نسبة الصواب",
      "macroP": "الدقة",
      "macroR": "الاستدعاء",
      "macroF1": "F1",
      "extractionF1": "F1 للاستخراج",
      "escalationP": "دقة التصعيد",
      "escalationR": "استدعاء التصعيد",
      "fraudRecall": "استدعاء الاحتيال",
      "p50": "الوسيط",
      "p95": "المئين 95",
      "errorRate": "نسبة الأخطاء",
      "tokens": "الرموز دخول / خروج",
      "tps": "رمز/ثانية",
      "costRequest": "$ / طلب",
      "cost1k": "$ / 1000 تذكرة",
      "classifierCost": "المصنِّف {value}",
      "production": "المعتمد حالياً",
      "local": "محلي · $0",
      "failed": "فشل",
      "best": "الأفضل",
      "ciNote": "مع {n} تذكرة، هامش الخطأ في نسبة الصواب حوالي ±{points} نقطة (ثقة 95%).",
      "costNote": "تُحسب الكلفة من أسعار المزوّد عند توفرها، وإلا من عدد الرموز × الأسعار المضبوطة. النماذج المحلية تعمل على أجهزتك وتظهر بكلفة $0.",
      "macroNote": "الدقة والاستدعاء و F1 هي متوسطات عبر فئات المشكلات."
    },
    "metricHelp": {
      "accuracy": "Accuracy",
      "macroP": "Macro precision",
      "macroR": "Macro recall",
      "macroF1": "Macro F1",
      "extractionF1": "Field extraction micro F1",
      "escalationP": "Escalation precision",
      "escalationR": "Escalation recall",
      "fraudRecall": "Fraud flag recall",
      "p50": "Median response time",
      "p95": "95th percentile response time",
      "errorRate": "Error rate",
      "tps": "Tokens per second",
      "costRequest": "Cost per request",
      "cost1k": "Cost per 1,000 tickets"
    },
    "detail": {
      "title": "تفاصيل النموذج",
      "model": "النموذج",
      "categories": "الفئات",
      "confusion": "مصفوفة الالتباس",
      "flags": "المؤشرات",
      "extraction": "الاستخراج",
      "slices": "الحالات الصعبة",
      "category": "الفئة",
      "flag": "المؤشر",
      "field": "الحقل",
      "slice": "نوع الحالة",
      "support": "التذاكر",
      "precision": "الدقة",
      "recall": "الاستدعاء",
      "f1": "F1",
      "accuracy": "نسبة الصواب",
      "errorRate": "نسبة الأخطاء",
      "hallucination": "قيم مختلقة: {value}",
      "missed": "قيم فائتة: {value}",
      "axes": "الصحيح ↓ · المتوقَّع ←",
      "error": "خطأ",
      "cellLabel": "{gold} صُنّفت كـ {predicted}: {count} تذكرة",
      "matrixHelp": "اختر خلية لعرض تذاكرها.",
      "selfReported": "ثقة النموذج اللغوي يقدّرها النموذج بنفسه وليست معايرة.",
      "noSummary": "لا توجد نتائج لهذا النموذج."
    },
    "flagNames": {
      "fraud_suspected": "اشتباه احتيال",
      "money_lost": "فقدان أموال",
      "multi_issue": "أكثر من مشكلة",
      "urgent_or_angry": "عاجل أو غاضب",
      "mentions_specific_transaction": "يذكر معاملة محددة",
      "asks_for_human": "يطلب موظفاً"
    },
    "fieldNames": {
      "txn_ref": "رقم المعاملة",
      "amount": "المبلغ",
      "phone": "رقم الهاتف",
      "date": "التاريخ"
    },
    "tags": {
      "arabizi": "عربيزي",
      "mixed_english": "عربي ممزوج بالإنجليزية",
      "multi_issue": "أكثر من مشكلة",
      "missing_details": "تفاصيل ناقصة",
      "prompt_injection": "محاولة حقن تعليمات",
      "angry": "عميل غاضب",
      "arabic_indic_digits": "أرقام هندية",
      "amount_in_words": "المبلغ بالكلمات"
    },
    "drawer": {
      "title": "{gold} ← {predicted}",
      "close": "إغلاق",
      "loading": "جارٍ تحميل التذاكر…",
      "empty": "لا توجد تذاكر لهذه الخلية.",
      "gold": "الصحيح",
      "predicted": "المتوقَّع",
      "escalated": "مُصعَّدة",
      "notEscalated": "غير مُصعَّدة",
      "latency": "زمن الاستجابة",
      "cost": "الكلفة",
      "error": "الخطأ",
      "shown": "عرض {shown} من {total}"
    },
    "dialog": {
      "title": "تشغيل تقييم",
      "description": "يصنّف كل نموذج مختار نفس التذاكر عبر خط المعالجة الحقيقي. تُتخطى صياغة الردود.",
      "models": "النماذج",
      "split": "التذاكر",
      "testWarning": "تذاكر محجوبة: لا تعدّل التعليمات بناءً على هذه النتائج.",
      "estimate": "الكلفة التقديرية",
      "estimating": "جارٍ التقدير…",
      "total": "الإجمالي {value} (تقريبي، للتصنيف فقط)",
      "unknown": "بعض الأسعار غير معروفة ولم تُحتسب في الإجمالي.",
      "start": "بدء التقييم",
      "starting": "جارٍ البدء…",
      "cancel": "إلغاء",
      "noneSelected": "اختر نموذجاً واحداً على الأقل.",
      "started": "بدأ التقييم #{id}.",
      "loadingModels": "جارٍ التحقق من النماذج المتاحة…"
    },
    "availability": {
      "ready": "جاهز",
      "missing_key": "مفتاح API مفقود",
      "unreachable": "تعذّر الوصول",
      "model_missing": "النموذج غير منزَّل"
    },
    "progress": {
      "title": "التقييم #{id} قيد التشغيل",
      "model": "{done} من {total}",
      "cancel": "إلغاء التقييم",
      "cancelling": "سيتوقف بعد التذاكر الحالية…"
    },
    "errors": {
      "no_models": "اختر نموذجاً واحداً على الأقل.",
      "unknown_model": "{model} غير مضبوط للتقييم.",
      "model_unavailable": "{model} غير متاح: {reason}.",
      "dataset_missing": "لم تُنشأ مجموعة بيانات التقييم بعد. شغّل الأمر “support eval-generate” في الخادم.",
      "test_split_modified": "تغيّر ملف الاختبار المحجوب بعد قفله. أرجعه أو أعد إنشاء مجموعة البيانات.",
      "conflict": "يوجد تقييم قيد التشغيل حالياً.",
      "generic": "تعذّر بدء التقييم."
    },
    "importErrors": {
      "object": "اختر تقرير تقييم بصيغة JSON.",
      "v1Fields": "يحتاج التقرير إلى model و split: test و sample_size موجب و generated_at.",
      "accuracy": "يجب أن تكون الدقة رقماً بين 0 و 1.",
      "confusion": "يجب أن تكون confusion_cases قائمة من الأوصاف النصية.",
      "v2": "يحتاج تقرير الإصدار 2 إلى split و sample_size و generated_at و dataset_sha256 ونتائج لكل نموذج."
    },
    "schema": {
      "title": "صيغة التقرير",
      "note": "صدّر أي تشغيل بهذه الصيغة عبر الأمر “support eval --out report.json”. الملفات المستوردة لا تُحفظ."
    },
    "notes": "ملاحظات من التقرير"
  }
```

`metricHelp` intentionally stays English in both files: it feeds the `title` tooltip with the English term.

- [ ] **Step 6: Rewrite `validateEvaluation`**

In `employee-frontend/src/lib/imports.ts`, change the import line to:

```ts
import { getCopy } from "./locale"
import type { EvaluationExportV2, EvaluationReport, ImportedReport, TicketInput } from "./types"
```

and replace `validateEvaluation` with:

```ts
function isObject(value: unknown): value is Record<string, unknown> {
  return Boolean(value) && typeof value === "object" && !Array.isArray(value)
}

function validDate(value: unknown) {
  return typeof value === "string" && !Number.isNaN(Date.parse(value))
}

export function validateEvaluation(data: unknown): ImportedReport {
  const errors = getCopy().evaluation.importErrors
  if (!isObject(data)) throw new Error(errors.object)
  if (data.format === "zaincash-eval/v2") {
    const models = data.models
    const valid =
      (data.split === "dev" || data.split === "test") &&
      Number.isInteger(data.sample_size) && Number(data.sample_size) > 0 &&
      validDate(data.generated_at) && typeof data.dataset_sha256 === "string" &&
      isObject(models) && Object.keys(models).length > 0 &&
      Object.values(models).every(
        (m) => isObject(m) && isObject(m.classification) && isObject(m.system) && isObject(m.cost)
      )
    if (!valid) throw new Error(errors.v2)
    return { kind: "v2", report: data as unknown as EvaluationExportV2 }
  }
  if (
    typeof data.model !== "string" || !data.model.trim() || data.split !== "test" ||
    !Number.isInteger(data.sample_size) || Number(data.sample_size) < 1 || !validDate(data.generated_at)
  )
    throw new Error(errors.v1Fields)
  for (const key of ["classification_accuracy", "extraction_accuracy"]) {
    const value = data[key]
    if (typeof value !== "number" || !Number.isFinite(value) || value < 0 || value > 1)
      throw new Error(errors.accuracy)
  }
  if (!Array.isArray(data.confusion_cases) || !data.confusion_cases.every((i) => typeof i === "string"))
    throw new Error(errors.confusion)
  return { kind: "v1", report: data as EvaluationReport }
}
```

- [ ] **Step 7: Run tests, lint and typecheck**

Run: `npm test && npm run lint && npm run typecheck`
Expected: all PASS. The old `EvaluationPage.tsx` still compiles? It uses `validateEvaluation(...)` as `EvaluationReport`; if `typecheck` fails there, change its line to `const parsed = validateEvaluation(...)` and `setReport(parsed.kind === "v1" ? parsed.report : null)` as a temporary bridge — Task 17 replaces the file.

- [ ] **Step 8: Commit**

```bash
git add employee-frontend/src/lib employee-frontend/src/locales employee-frontend/src/features/insights/EvaluationPage.tsx
git commit -m "feat: add evaluation API client, types, formatters and translated copy"
```

---

### Task 14: Evaluation view helpers

**Files:**
- Create: `employee-frontend/src/features/evaluation/eval-view.ts`
- Create: `employee-frontend/src/features/evaluation/fixtures.ts` (shared test data; importing one test file from another would register its tests twice)
- Test: `employee-frontend/src/features/evaluation/eval-view.test.ts`

**Interfaces:**
- Consumes: types and `ApiError` from Task 13; `fill`, `Copy` from `@/lib/locale`; `categories` from `@/lib/format`.
- Produces:
  - `type EvaluationView = { source: "run" | "import"; runId: number | null; models: EvalModel[]; summaries: Record<string, EvalModelSummary>; statuses: Record<string, EvalModelStatus>; sampleSize: number; split: "dev" | "test"; generatedAt: string | null; datasetSha: string | null; promptVersion: string | null; triggeredBy: "ui" | "cli" | null; filename: string | null; legacyExtractionAccuracy: number | null; notes: string[] }`
  - `viewFromRun(run: EvalRun): EvaluationView`; `viewFromImport(imported: ImportedReport, filename: string): EvaluationView`; `emptySummary(n: number): EvalModelSummary`
  - `type ComparisonRow = { model: EvalModel; status: EvalModelStatus | null; summary: EvalModelSummary | null; production: boolean; local: boolean; failed: boolean }`; `comparisonRows(view: EvaluationView): ComparisonRow[]`
  - `type ColumnKey = "accuracy" | "macroP" | "macroR" | "macroF1" | "extractionF1" | "escalationP" | "escalationR" | "fraudRecall" | "p50" | "p95" | "errorRate" | "tps" | "costRequest" | "cost1k"`; `COLUMNS: { key: ColumnKey; group: "quality" | "system" | "cost"; better: "high" | "low"; format: "percent" | "ms" | "usd" | "number"; value: (s: EvalModelSummary) => number | null }[]`
  - `bestByColumn(rows): Partial<Record<ColumnKey, string[]>>`; `headline(rows): Record<"accuracy" | "errors" | "cheapest" | "fastest", { model: EvalModel; value: number } | null>`
  - `ciHalfWidthPoints(n: number): number | null`
  - `matrixAxes(confusion, order?: string[]): { rows: string[]; columns: string[] }`
  - `modelLabel(model: EvalModel): string`
  - `isActive(run: EvalRun | null | undefined): boolean`
  - `evaluationErrorMessage(error: unknown, copy: Copy["evaluation"]): string`

- [ ] **Step 1: Write the shared fixtures and the failing tests**

Create `employee-frontend/src/features/evaluation/fixtures.ts`:

```ts
import type { EvalModel, EvalRun } from "@/lib/types"
import { emptySummary } from "./eval-view"

export const model = (id: string, locality: "cloud" | "local" = "cloud"): EvalModel => ({
  id, provider: id === "jev" ? "typesafe" : id.startsWith("ollama") ? "ollama" : "openrouter",
  model: id === "jev" ? "jev-1.13.0" : id.split(":").slice(1).join(":"), locality,
  price_in: 0, price_out: 0, concurrency: 1,
})

export function summary(accuracy: number, errorRate: number, cost: number | null, p50: number) {
  const s = emptySummary(100)
  s.classification.accuracy = accuracy
  s.system.error_rate = errorRate
  s.system.latency_p50_ms = p50
  s.cost.total_cost_per_request = cost
  return s
}

export const run: EvalRun = {
  id: 3, status: "completed", split: "test", dataset_sha256: "abcdef0123456789",
  prompt_version: "llm_classify_v1+jev-1.13.0",
  models: [model("jev"), model("openrouter:anthropic/claude-sonnet-5.5"), model("ollama:qwen3:4b", "local")],
  model_status: {
    jev: { status: "completed", error: null },
    "openrouter:anthropic/claude-sonnet-5.5": { status: "completed", error: null },
    "ollama:qwen3:4b": { status: "failed", error: "unreachable" },
  },
  progress: {}, estimated_cost_usd: 0.1, actual_cost_usd: 0.09, triggered_by: "ui",
  cancel_requested: false, error: null, sample_size: 100, created_at: "2026-11-12T10:00:00Z",
  started_at: null, finished_at: "2026-11-12T10:30:00Z",
  summary: {
    jev: summary(0.86, 0.0, 0.00008, 900),
    "openrouter:anthropic/claude-sonnet-5.5": summary(0.91, 0.01, 0.004, 2100),
  },
}
```

Create `employee-frontend/src/features/evaluation/eval-view.test.ts`:

```ts
import { expect, it } from "vitest"
import { ApiError } from "@/lib/api"
import { getCopy } from "@/lib/locale"
import {
  bestByColumn,
  ciHalfWidthPoints,
  comparisonRows,
  emptySummary,
  evaluationErrorMessage,
  headline,
  isActive,
  matrixAxes,
  modelLabel,
  viewFromImport,
  viewFromRun,
} from "./eval-view"
import { model, run } from "./fixtures"

it("comparisonRows keeps failed models without summary", () => {
  const rows = comparisonRows(viewFromRun(run))
  expect(rows.map((r) => r.model.id)).toEqual(["jev", "openrouter:anthropic/claude-sonnet-5.5", "ollama:qwen3:4b"])
  expect(rows[0].production).toBe(true)
  expect(rows[2]).toMatchObject({ failed: true, local: true, summary: null })
})

it("finds the best value per column, respecting direction and ties", () => {
  const best = bestByColumn(comparisonRows(viewFromRun(run)))
  expect(best.accuracy).toEqual(["openrouter:anthropic/claude-sonnet-5.5"])
  expect(best.errorRate).toEqual(["jev"])
  expect(best.costRequest).toEqual(["jev"])
  expect(best.p50).toEqual(["jev"])
  expect(best.tps).toBeUndefined()
})

it("builds headline winners", () => {
  const h = headline(comparisonRows(viewFromRun(run)))
  expect(h.accuracy?.model.id).toBe("openrouter:anthropic/claude-sonnet-5.5")
  expect(h.cheapest?.value).toBe(0.00008)
  expect(headline([]).fastest).toBeNull()
})

it("computes confidence interval width and matrix axes", () => {
  expect(ciHalfWidthPoints(100)).toBe(10)
  expect(ciHalfWidthPoints(0)).toBeNull()
  expect(matrixAxes({ app_bug: { app_bug: 2, error: 1 }, failed_transfer: { app_bug: 1 } }))
    .toEqual({ rows: ["failed_transfer", "app_bug"], columns: ["failed_transfer", "app_bug", "error"] })
})

it("converts imported reports", () => {
  const v1 = viewFromImport({ kind: "v1", report: {
    model: "legacy", split: "test", sample_size: 50, generated_at: "2026-10-07",
    classification_accuracy: 0.8, extraction_accuracy: 0.7, confusion_cases: ["a"] } }, "r.json")
  expect(v1.source).toBe("import")
  expect(v1.summaries.legacy.classification.accuracy).toBe(0.8)
  expect(v1.legacyExtractionAccuracy).toBe(0.7)
  expect(v1.notes).toEqual(["a"])
  const v2 = viewFromImport({ kind: "v2", report: {
    format: "zaincash-eval/v2", split: "dev", sample_size: 100, generated_at: "2026-11-12",
    dataset_sha256: "x", models: { "ollama:qwen3:4b": emptySummary(100) } } }, "r2.json")
  expect(v2.models[0]).toMatchObject({ id: "ollama:qwen3:4b", locality: "local" })
})

it("labels models, detects active runs and maps API errors", () => {
  expect(modelLabel(model("jev"))).toBe("Jev")
  expect(modelLabel(model("ollama:qwen3:4b", "local"))).toBe("qwen3:4b")
  expect(isActive({ ...run, status: "running" })).toBe(true)
  expect(isActive(run)).toBe(false)
  const copy = getCopy().evaluation
  expect(evaluationErrorMessage(new ApiError("x", 409), copy)).toBe(copy.errors.conflict)
  const unavailable = new ApiError("x", 422, { code: "model_unavailable", model: "ollama:qwen3:4b", reason: "unreachable" })
  expect(evaluationErrorMessage(unavailable, copy)).toContain("ollama:qwen3:4b")
  expect(evaluationErrorMessage(unavailable, copy)).toContain(copy.availability.unreachable)
  expect(evaluationErrorMessage(new Error("?"), copy)).toBe(copy.errors.generic)
})
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `npm test -- src/features/evaluation/eval-view.test.ts`
Expected: FAIL (`Cannot find module './eval-view'`).

- [ ] **Step 3: Implement `eval-view.ts`**

```ts
import { ApiError } from "@/lib/api"
import { categories } from "@/lib/format"
import { fill, type Copy } from "@/lib/locale"
import type {
  EvalModel,
  EvalModelStatus,
  EvalModelSummary,
  EvalRun,
  ImportedReport,
} from "@/lib/types"

export type EvaluationView = {
  source: "run" | "import"
  runId: number | null
  models: EvalModel[]
  summaries: Record<string, EvalModelSummary>
  statuses: Record<string, EvalModelStatus>
  sampleSize: number
  split: "dev" | "test"
  generatedAt: string | null
  datasetSha: string | null
  promptVersion: string | null
  triggeredBy: "ui" | "cli" | null
  filename: string | null
  legacyExtractionAccuracy: number | null
  notes: string[]
}

export function emptySummary(n: number): EvalModelSummary {
  return {
    n,
    classification: {
      accuracy: null, accuracy_ci: null, correct: 0, macro_precision: null, macro_recall: null,
      macro_f1: null, per_category: {}, confusion: {}, priority_exact: null, priority_within_one: null,
    },
    flags: {},
    extraction: {
      per_field: {}, micro_precision: null, micro_recall: null, micro_f1: null,
      hallucination_rate: null, missed_rate: null,
    },
    escalation: {
      precision: null, recall: null, f1: null, rate: null, gold_rate: null, coverage: null,
      accuracy_not_escalated: null,
    },
    system: {
      latency_p50_ms: null, latency_p95_ms: null, latency_mean_ms: null, classifier_p50_ms: null,
      classifier_p95_ms: null, error_rate: null, invalid_output_rate: null,
      mean_input_tokens: null, mean_output_tokens: null, tokens_per_s: null,
    },
    cost: {
      classifier_cost_per_request: null, total_cost_per_request: null, total_cost_usd: 0,
      cost_per_1k_tickets: null, cost_sources: {}, local: false,
    },
    slices: {},
  }
}

function importedModel(id: string): EvalModel {
  const [provider] = id.split(":")
  return {
    id, provider: "imported", model: id === "jev" ? "jev" : id.split(":").slice(1).join(":") || id,
    locality: provider === "ollama" ? "local" : "cloud", price_in: null, price_out: null, concurrency: 1,
  }
}

export function viewFromRun(run: EvalRun): EvaluationView {
  return {
    source: "run", runId: run.id, models: run.models, summaries: run.summary ?? {},
    statuses: run.model_status, sampleSize: run.sample_size, split: run.split,
    generatedAt: run.finished_at ?? run.created_at, datasetSha: run.dataset_sha256,
    promptVersion: run.prompt_version, triggeredBy: run.triggered_by, filename: null,
    legacyExtractionAccuracy: null, notes: [],
  }
}

export function viewFromImport(imported: ImportedReport, filename: string): EvaluationView {
  if (imported.kind === "v1") {
    const r = imported.report
    const summary = emptySummary(r.sample_size)
    summary.classification.accuracy = r.classification_accuracy
    return {
      source: "import", runId: null, models: [{ ...importedModel(r.model), model: r.model }],
      summaries: { [r.model]: summary }, statuses: {}, sampleSize: r.sample_size, split: r.split,
      generatedAt: r.generated_at, datasetSha: null, promptVersion: null, triggeredBy: null,
      filename, legacyExtractionAccuracy: r.extraction_accuracy, notes: r.confusion_cases,
    }
  }
  const r = imported.report
  return {
    source: "import", runId: null,
    models: r.model_info ?? Object.keys(r.models).map(importedModel),
    summaries: r.models, statuses: r.model_status ?? {}, sampleSize: r.sample_size, split: r.split,
    generatedAt: r.generated_at, datasetSha: r.dataset_sha256, promptVersion: r.prompt_version ?? null,
    triggeredBy: null, filename, legacyExtractionAccuracy: null, notes: [],
  }
}

export type ComparisonRow = {
  model: EvalModel
  status: EvalModelStatus | null
  summary: EvalModelSummary | null
  production: boolean
  local: boolean
  failed: boolean
}

export function comparisonRows(view: EvaluationView): ComparisonRow[] {
  return view.models.map((model) => {
    const status = view.statuses[model.id] ?? null
    return {
      model, status, summary: view.summaries[model.id] ?? null,
      production: model.id === "jev", local: model.locality === "local",
      failed: status?.status === "failed",
    }
  })
}

export type ColumnKey =
  | "accuracy" | "macroP" | "macroR" | "macroF1" | "extractionF1" | "escalationP"
  | "escalationR" | "fraudRecall" | "p50" | "p95" | "errorRate" | "tps" | "costRequest" | "cost1k"

type Column = {
  key: ColumnKey
  group: "quality" | "system" | "cost"
  better: "high" | "low"
  format: "percent" | "ms" | "usd" | "number"
  value: (s: EvalModelSummary) => number | null
}

export const COLUMNS: Column[] = [
  { key: "accuracy", group: "quality", better: "high", format: "percent", value: (s) => s.classification.accuracy },
  { key: "macroP", group: "quality", better: "high", format: "percent", value: (s) => s.classification.macro_precision },
  { key: "macroR", group: "quality", better: "high", format: "percent", value: (s) => s.classification.macro_recall },
  { key: "macroF1", group: "quality", better: "high", format: "percent", value: (s) => s.classification.macro_f1 },
  { key: "extractionF1", group: "quality", better: "high", format: "percent", value: (s) => s.extraction.micro_f1 },
  { key: "escalationP", group: "quality", better: "high", format: "percent", value: (s) => s.escalation.precision },
  { key: "escalationR", group: "quality", better: "high", format: "percent", value: (s) => s.escalation.recall },
  { key: "fraudRecall", group: "quality", better: "high", format: "percent", value: (s) => s.flags.fraud_suspected?.recall ?? null },
  { key: "p50", group: "system", better: "low", format: "ms", value: (s) => s.system.latency_p50_ms },
  { key: "p95", group: "system", better: "low", format: "ms", value: (s) => s.system.latency_p95_ms },
  { key: "errorRate", group: "system", better: "low", format: "percent", value: (s) => s.system.error_rate },
  { key: "tps", group: "system", better: "high", format: "number", value: (s) => s.system.tokens_per_s },
  { key: "costRequest", group: "cost", better: "low", format: "usd", value: (s) => s.cost.total_cost_per_request },
  { key: "cost1k", group: "cost", better: "low", format: "usd", value: (s) => s.cost.cost_per_1k_tickets },
]

function valuesFor(rows: ComparisonRow[], key: ColumnKey) {
  const column = COLUMNS.find((c) => c.key === key)!
  return rows.flatMap((row) => {
    const value = row.summary ? column.value(row.summary) : null
    return value == null ? [] : [{ row, value }]
  })
}

function bestValue(key: ColumnKey, values: number[]) {
  const column = COLUMNS.find((c) => c.key === key)!
  return column.better === "high" ? Math.max(...values) : Math.min(...values)
}

export function bestByColumn(rows: ComparisonRow[]): Partial<Record<ColumnKey, string[]>> {
  const best: Partial<Record<ColumnKey, string[]>> = {}
  for (const column of COLUMNS) {
    const values = valuesFor(rows, column.key)
    if (values.length < 2) continue
    const target = bestValue(column.key, values.map((v) => v.value))
    best[column.key] = values.filter((v) => v.value === target).map((v) => v.row.model.id)
  }
  return best
}

export function headline(rows: ComparisonRow[]) {
  const pick = (key: ColumnKey) => {
    const values = valuesFor(rows, key)
    if (!values.length) return null
    const target = bestValue(key, values.map((v) => v.value))
    const winner = values.find((v) => v.value === target)!
    return { model: winner.row.model, value: winner.value }
  }
  return { accuracy: pick("accuracy"), errors: pick("errorRate"), cheapest: pick("costRequest"), fastest: pick("p50") }
}

export function ciHalfWidthPoints(n: number): number | null {
  return n > 0 ? Math.round(1.96 * Math.sqrt(0.25 / n) * 100) : null
}

export function matrixAxes(
  confusion: Record<string, Record<string, number>>,
  order: string[] = Object.keys(categories)
) {
  const predicted = new Set(Object.values(confusion).flatMap((row) => Object.keys(row)))
  const rows = order.filter((c) => confusion[c])
  const columns = order.filter((c) => predicted.has(c) || confusion[c])
  if (predicted.has("error")) columns.push("error")
  return { rows, columns }
}

export function modelLabel(model: EvalModel) {
  return model.id === "jev" ? "Jev" : model.model
}

export function isActive(run: EvalRun | null | undefined) {
  return Boolean(run && (run.status === "queued" || run.status === "running"))
}

export function evaluationErrorMessage(error: unknown, copy: Copy["evaluation"]) {
  if (error instanceof ApiError) {
    if (error.status === 409) return copy.errors.conflict
    const code = error.code as keyof typeof copy.errors | undefined
    if (code && code in copy.errors) {
      const reason = error.detail?.reason ?? ""
      const reasonText = (copy.availability as Record<string, string>)[reason] ?? reason
      return fill(copy.errors[code], { model: error.detail?.model ?? "", reason: reasonText })
    }
  }
  return copy.errors.generic
}
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `npm test -- src/features/evaluation && npm run lint && npm run typecheck`
Expected: all PASS.

- [ ] **Step 5: Commit**

```bash
git add employee-frontend/src/features/evaluation
git commit -m "feat: add evaluation view helpers for comparison, winners and imports"
```

---

### Task 15: Provenance, headline metrics, comparison table and empty state

**Files:**
- Create: `employee-frontend/src/features/evaluation/ProvenanceStrip.tsx`
- Create: `employee-frontend/src/features/evaluation/HeadlineMetrics.tsx`
- Create: `employee-frontend/src/features/evaluation/ModelComparisonTable.tsx`
- Create: `employee-frontend/src/features/evaluation/EvaluationEmptyState.tsx`
- Create: `employee-frontend/src/features/evaluation/format-metric.ts`
- Test: `employee-frontend/src/features/evaluation/comparison.test.tsx`

**Interfaces:**
- Consumes: Task 14 helpers; formatters from Task 13; `Metric` from `workspace-ui`; `Badge`, `Table*`.
- Produces:
  - `formatMetric(value: number | null | undefined, format: "percent" | "ms" | "usd" | "number"): string`
  - `ProvenanceStrip({ view }: { view: EvaluationView })`
  - `HeadlineMetrics({ rows }: { rows: ComparisonRow[] })`
  - `ModelComparisonTable({ rows, sampleSize }: { rows: ComparisonRow[]; sampleSize: number })`
  - `EvaluationEmptyState({ onRun, canRun }: { onRun: () => void; canRun: boolean })`

- [ ] **Step 1: Write the failing tests**

Create `employee-frontend/src/features/evaluation/comparison.test.tsx`:

```tsx
import { renderToStaticMarkup } from "react-dom/server"
import { afterEach, expect, it } from "vitest"
import { getLocale, setLocale } from "@/lib/locale"
import { comparisonRows, viewFromRun } from "./eval-view"
import { EvaluationEmptyState } from "./EvaluationEmptyState"
import { run } from "./fixtures"
import { HeadlineMetrics } from "./HeadlineMetrics"
import { ModelComparisonTable } from "./ModelComparisonTable"
import { ProvenanceStrip } from "./ProvenanceStrip"

const originalLocale = getLocale()
afterEach(() => setLocale(originalLocale))

function render() {
  const view = viewFromRun(run)
  const rows = comparisonRows(view)
  return renderToStaticMarkup(
    <>
      <ProvenanceStrip view={view} />
      <HeadlineMetrics rows={rows} />
      <ModelComparisonTable rows={rows} sampleSize={view.sampleSize} />
    </>
  )
}

it("renders the comparison in English with badges, best values and dashes", () => {
  setLocale("en")
  const html = render()
  expect(html).toContain("Held-out test split")
  expect(html).toContain("Production")
  expect(html).toContain("Local · $0")
  expect(html).toContain("Failed")
  expect(html).toContain("unreachable")
  expect(html).toContain("91.0%")
  expect(html).toContain("eval-best")
  expect(html).toContain('title="Macro recall"')
  expect(html).toContain('dir="ltr"')
  expect(html).toContain("±10")
  expect(html).toContain("—")
})

it("renders the comparison in Arabic without English UI words", () => {
  setLocale("ar")
  const html = render()
  expect(html).toContain("مقارنة النماذج")
  expect(html).toContain("الاستدعاء")
  expect(html).toContain("محلي · $0")
  for (const english of ["Model comparison", "Production", "Error rate", "Best accuracy", "Held-out"])
    expect(html, english).not.toContain(`>${english}`)
})

it("renders the empty state with the Topic 06 checklist", () => {
  setLocale("ar")
  const html = renderToStaticMarkup(<EvaluationEmptyState onRun={() => {}} canRun />)
  expect(html).toContain("تشغيل التقييم")
  expect(html).toContain("200 تذكرة اصطناعية")
})
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `npm test -- src/features/evaluation/comparison.test.tsx`
Expected: FAIL (modules not found).

- [ ] **Step 3: Implement the components**

Create `employee-frontend/src/features/evaluation/format-metric.ts`:

```ts
import { countLabel, msLabel, percent1, usd } from "@/lib/format"

export function formatMetric(
  value: number | null | undefined,
  format: "percent" | "ms" | "usd" | "number"
) {
  if (format === "percent") return percent1(value)
  if (format === "ms") return msLabel(value)
  if (format === "usd") return usd(value)
  return countLabel(value)
}
```

Create `employee-frontend/src/features/evaluation/ProvenanceStrip.tsx`:

```tsx
import { FileCheck2 } from "lucide-react"
import { Badge } from "@/components/ui/badge"
import { dateLabel, percent1, timeLabel } from "@/lib/format"
import { fill, useCopy } from "@/lib/locale"
import type { EvaluationView } from "./eval-view"

export function ProvenanceStrip({ view }: { view: EvaluationView }) {
  const copy = useCopy().evaluation
  const p = copy.provenance
  return (
    <div className="report-provenance eval-provenance">
      <FileCheck2 size={18} />
      <div>
        <strong>
          {view.source === "import" ? fill(p.imported, { name: view.filename ?? "" }) : copy.split[view.split]}
        </strong>
        <span>
          {fill(p.tickets, { count: view.sampleSize })}
          {view.generatedAt && (
            <> · {fill(p.date, { date: dateLabel(view.generatedAt), time: timeLabel(view.generatedAt) })}</>
          )}
          {view.datasetSha && (
            <> · {p.dataset} <bdi dir="ltr">{view.datasetSha.slice(0, 12)}</bdi></>
          )}
          {view.promptVersion && (
            <> · {p.prompt} <bdi dir="ltr">{view.promptVersion}</bdi></>
          )}
          {view.triggeredBy && <> · {view.triggeredBy === "ui" ? p.fromUi : p.fromCli}</>}
          {view.legacyExtractionAccuracy != null && (
            <> · {fill(p.legacyExtraction, { value: percent1(view.legacyExtractionAccuracy) })}</>
          )}
        </span>
      </div>
      <Badge variant="outline">{copy.split[view.split]}</Badge>
    </div>
  )
}
```

Create `employee-frontend/src/features/evaluation/HeadlineMetrics.tsx`:

```tsx
import { Coins, Gauge, ShieldCheck, Target } from "lucide-react"
import { Metric } from "@/components/shared/workspace-ui"
import { msLabel, percent1, usd } from "@/lib/format"
import { useCopy } from "@/lib/locale"
import { headline, modelLabel, type ComparisonRow } from "./eval-view"

export function HeadlineMetrics({ rows }: { rows: ComparisonRow[] }) {
  const copy = useCopy().evaluation.headline
  const h = headline(rows)
  const detail = (winner: ReturnType<typeof headline>["accuracy"]) =>
    winner ? modelLabel(winner.model) : copy.noData
  return (
    <div className="metrics-grid">
      <Metric label={copy.accuracy} value={percent1(h.accuracy?.value)} detail={detail(h.accuracy)} icon={<Target size={19} />} />
      <Metric label={copy.errors} value={percent1(h.errors?.value)} detail={detail(h.errors)} icon={<ShieldCheck size={19} />} />
      <Metric label={copy.cheapest} value={usd(h.cheapest?.value)} detail={detail(h.cheapest)} icon={<Coins size={19} />} />
      <Metric label={copy.fastest} value={msLabel(h.fastest?.value)} detail={detail(h.fastest)} icon={<Gauge size={19} />} />
    </div>
  )
}
```

Create `employee-frontend/src/features/evaluation/ModelComparisonTable.tsx`:

```tsx
import { Badge } from "@/components/ui/badge"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table"
import { countLabel, usd } from "@/lib/format"
import { fill, useCopy } from "@/lib/locale"
import { bestByColumn, ciHalfWidthPoints, COLUMNS, modelLabel, type ComparisonRow } from "./eval-view"
import { formatMetric } from "./format-metric"

export function ModelComparisonTable({ rows, sampleSize }: { rows: ComparisonRow[]; sampleSize: number }) {
  const copy = useCopy().evaluation
  const best = bestByColumn(rows)
  const points = ciHalfWidthPoints(sampleSize)
  return (
    <Card className="data-card eval-comparison">
      <CardHeader>
        <CardTitle>{copy.table.title}</CardTitle>
      </CardHeader>
      <CardContent>
        <div className="eval-table-scroll">
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead>{copy.table.model}</TableHead>
                {COLUMNS.map((column) => (
                  <TableHead key={column.key} title={copy.metricHelp[column.key]} className={`eval-group-${column.group}`}>
                    {copy.table[column.key]}
                  </TableHead>
                ))}
                <TableHead>{copy.table.tokens}</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {rows.map((row) => (
                <TableRow key={row.model.id} className={row.failed ? "eval-row-failed" : undefined}>
                  <TableCell>
                    <div className="eval-model-cell">
                      <bdi dir="ltr">{modelLabel(row.model)}</bdi>
                      <span className="eval-badges">
                        {row.production && <Badge variant="outline">{copy.table.production}</Badge>}
                        {row.local && <Badge variant="secondary">{copy.table.local}</Badge>}
                        {row.failed && <Badge variant="destructive">{copy.table.failed}</Badge>}
                      </span>
                      {row.failed && row.status?.error && <small className="error-text">{row.status.error}</small>}
                    </div>
                  </TableCell>
                  {COLUMNS.map((column) => {
                    const value = row.summary ? column.value(row.summary) : null
                    const isBest = best[column.key]?.includes(row.model.id)
                    return (
                      <TableCell key={column.key} className={isBest ? "eval-best" : undefined}>
                        {formatMetric(value, column.format)}
                        {isBest && <span className="sr-only"> ({copy.table.best})</span>}
                        {column.key === "costRequest" && row.summary?.cost.classifier_cost_per_request != null && (
                          <small className="block-muted">
                            {fill(copy.table.classifierCost, { value: usd(row.summary.cost.classifier_cost_per_request) })}
                          </small>
                        )}
                      </TableCell>
                    )
                  })}
                  <TableCell>
                    {countLabel(row.summary?.system.mean_input_tokens)} / {countLabel(row.summary?.system.mean_output_tokens)}
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </div>
        <div className="eval-notes">
          {points != null && <p>{fill(copy.table.ciNote, { n: sampleSize, points })}</p>}
          <p>{copy.table.macroNote}</p>
          <p>{copy.table.costNote}</p>
        </div>
      </CardContent>
    </Card>
  )
}
```

Create `employee-frontend/src/features/evaluation/EvaluationEmptyState.tsx`:

```tsx
import { CheckCheck, FlaskConical, Play } from "lucide-react"
import { Button } from "@/components/ui/button"
import { useCopy } from "@/lib/locale"

export function EvaluationEmptyState({ onRun, canRun }: { onRun: () => void; canRun: boolean }) {
  const copy = useCopy().evaluation
  const intro = copy.intro
  return (
    <>
      <div className="evaluation-intro">
        <span className="evaluation-icon">
          <FlaskConical size={28} />
        </span>
        <div>
          <h2>{intro.title}</h2>
          <p>{intro.body}</p>
        </div>
        <Button onClick={onRun} disabled={!canRun}>
          <Play size={16} />
          {copy.run}
        </Button>
      </div>
      <div className="evaluation-checklist">
        <p>{intro.briefTitle}</p>
        {[intro.brief1, intro.brief2, intro.brief3, intro.brief4].map((item) => (
          <span key={item}>
            <CheckCheck size={16} />
            {item}
          </span>
        ))}
      </div>
    </>
  )
}
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `npm test -- src/features/evaluation && npm run lint && npm run typecheck`
Expected: all PASS.

- [ ] **Step 5: Commit**

```bash
git add employee-frontend/src/features/evaluation
git commit -m "feat: show model comparison, headline winners and provenance"
```

---

### Task 16: Model detail, confusion matrix and predictions drawer

**Files:**
- Create: `employee-frontend/src/features/evaluation/ModelDetail.tsx`
- Create: `employee-frontend/src/features/evaluation/ConfusionMatrix.tsx`
- Create: `employee-frontend/src/features/evaluation/PredictionsDrawer.tsx`
- Test: `employee-frontend/src/features/evaluation/detail.test.tsx`

**Interfaces:**
- Consumes: Task 14 (`matrixAxes`, `modelLabel`, `ComparisonRow`), Task 13 (`evaluationsApi`, `EvalPrediction`), `categoryLabel`, `useResource`, `Tabs*`, `Dialog*`, `FilterSelect`.
- Produces:
  - `ConfusionMatrix({ confusion, onSelect }: { confusion: Record<string, Record<string, number>>; onSelect?: (gold: string, predicted: string) => void })`
  - `PredictionsList({ items, total }: { items: EvalPrediction[]; total: number })`
  - `PredictionsDrawer({ runId, model, cell, onClose }: { runId: number; model: string; cell: { gold: string; predicted: string } | null; onClose: () => void })`
  - `ModelDetail({ rows, runId }: { rows: ComparisonRow[]; runId: number | null })`

- [ ] **Step 1: Write the failing tests**

Create `employee-frontend/src/features/evaluation/detail.test.tsx`:

```tsx
import { renderToStaticMarkup } from "react-dom/server"
import { afterEach, expect, it } from "vitest"
import { getLocale, setLocale } from "@/lib/locale"
import type { EvalPrediction } from "@/lib/types"
import { ConfusionMatrix } from "./ConfusionMatrix"
import { comparisonRows, viewFromRun } from "./eval-view"
import { run } from "./fixtures"
import { ModelDetail } from "./ModelDetail"
import { PredictionsList } from "./PredictionsDrawer"

const originalLocale = getLocale()
afterEach(() => setLocale(originalLocale))

it("renders matrix cells as labelled buttons when drill-down is available", () => {
  setLocale("en")
  const html = renderToStaticMarkup(
    <ConfusionMatrix confusion={{ failed_transfer: { failed_transfer: 7, app_bug: 2, error: 1 } }} onSelect={() => {}} />
  )
  expect(html).toContain('aria-label="Failed transfer predicted as App issue: 2 tickets"')
  expect(html).toContain(">7<")
  expect(html).toContain("Error")
  expect(html.match(/<button/g)?.length).toBe(3)
})

it("renders matrix counts as plain text without drill-down", () => {
  const html = renderToStaticMarkup(<ConfusionMatrix confusion={{ app_bug: { app_bug: 1 } }} />)
  expect(html).not.toContain("<button")
})

it("lists predictions with ticket text direction and errors", () => {
  setLocale("ar")
  const item: EvalPrediction = {
    id: 1, ticket_id: "E-0001", text: "حولت ٥٠ الف وما وصلت", tags: [],
    gold: { category: "failed_transfer", priority: "P2", escalated: false, flags: {}, fields: {}, lookup: null, reasons: [] },
    predicted: null, correct_category: false, latency_ms: 1200, cost_usd: 0, error: "timeout after 120s",
  }
  const html = renderToStaticMarkup(<PredictionsList items={[item]} total={3} />)
  expect(html).toContain('dir="auto"')
  expect(html).toContain("timeout after 120s")
  expect(html).toContain("عرض 1 من 3")
})

it("shows per-category metrics for the first model with results", () => {
  setLocale("en")
  const rows = comparisonRows(viewFromRun(run))
  rows[0].summary!.classification.per_category = {
    failed_transfer: { precision: 0.9, recall: 0.8, f1: 0.85, support: 9 },
  }
  const html = renderToStaticMarkup(<ModelDetail rows={rows} runId={3} />)
  expect(html).toContain("Model detail")
  expect(html).toContain("Failed transfer")
  expect(html).toContain("90.0%")
})
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `npm test -- src/features/evaluation/detail.test.tsx`
Expected: FAIL (modules not found).

- [ ] **Step 3: Implement `ConfusionMatrix.tsx`**

```tsx
import { categoryLabel } from "@/lib/format"
import { fill, useCopy } from "@/lib/locale"
import { matrixAxes } from "./eval-view"

export function ConfusionMatrix({
  confusion,
  onSelect,
}: {
  confusion: Record<string, Record<string, number>>
  onSelect?: (gold: string, predicted: string) => void
}) {
  const copy = useCopy().evaluation.detail
  const { rows, columns } = matrixAxes(confusion)
  const label = (id: string) => (id === "error" ? copy.error : categoryLabel(id))
  return (
    <div className="eval-table-scroll">
      <table className="eval-matrix">
        <caption>{copy.axes}</caption>
        <thead>
          <tr>
            <th scope="col" />
            {columns.map((c) => (
              <th scope="col" key={c}>{label(c)}</th>
            ))}
          </tr>
        </thead>
        <tbody>
          {rows.map((gold) => {
            const total = Object.values(confusion[gold]).reduce((a, b) => a + b, 0)
            return (
              <tr key={gold}>
                <th scope="row">{label(gold)}</th>
                {columns.map((predicted) => {
                  const count = confusion[gold][predicted] ?? 0
                  const share = total ? count / total : 0
                  const tone = gold === predicted ? "eval-cell-hit" : "eval-cell-miss"
                  const aria = fill(copy.cellLabel, { gold: label(gold), predicted: label(predicted), count })
                  return (
                    <td key={predicted} className={count ? tone : undefined} style={{ ["--share" as string]: share }}>
                      {count > 0 && onSelect ? (
                        <button type="button" aria-label={aria} onClick={() => onSelect(gold, predicted)}>
                          {count}
                        </button>
                      ) : count > 0 ? (
                        <span aria-label={aria}>{count}</span>
                      ) : null}
                    </td>
                  )
                })}
              </tr>
            )
          })}
        </tbody>
      </table>
      {onSelect && <p className="field-help">{copy.matrixHelp}</p>}
    </div>
  )
}
```

- [ ] **Step 4: Implement `PredictionsDrawer.tsx`**

```tsx
import { Button } from "@/components/ui/button"
import { Dialog, DialogContent, DialogFooter, DialogHeader, DialogTitle } from "@/components/ui/dialog"
import { LoadingState } from "@/components/shared/workspace-ui"
import { useResource } from "@/hooks/use-resource"
import { evaluationsApi } from "@/lib/api"
import { categoryLabel, duration, usd } from "@/lib/format"
import { fill, useCopy } from "@/lib/locale"
import type { EvalPrediction, EvalPredictionPage } from "@/lib/types"

export function PredictionsList({ items, total }: { items: EvalPrediction[]; total: number }) {
  const copy = useCopy().evaluation.drawer
  if (!items.length) return <p className="muted small">{copy.empty}</p>
  return (
    <div className="eval-predictions">
      {items.map((item) => (
        <article key={item.id}>
          <header>
            <bdi dir="ltr" className="ticket-id">{item.ticket_id}</bdi>
            <span>{copy.gold}: {categoryLabel(item.gold.category)}</span>
            <span>
              {copy.predicted}: {item.predicted ? categoryLabel(item.predicted.category) : "—"}
            </span>
          </header>
          <p dir="auto">{item.text}</p>
          <footer className="block-muted">
            {item.predicted && (item.predicted.escalated ? copy.escalated : copy.notEscalated)}
            {" · "}
            {copy.latency}: {duration(item.latency_ms)} · {copy.cost}: {usd(item.cost_usd)}
          </footer>
          {item.error && (
            <p className="error-text">
              {copy.error}: <bdi dir="ltr">{item.error}</bdi>
            </p>
          )}
        </article>
      ))}
      <p className="muted small">{fill(copy.shown, { shown: items.length, total })}</p>
    </div>
  )
}

export function PredictionsDrawer({
  runId,
  model,
  cell,
  onClose,
}: {
  runId: number
  model: string
  cell: { gold: string; predicted: string } | null
  onClose: () => void
}) {
  const copy = useCopy().evaluation
  const label = (id: string) => (id === "error" ? copy.detail.error : categoryLabel(id))
  const page = useResource<EvalPredictionPage>(
    cell ? `predictions:${runId}:${model}:${cell.gold}:${cell.predicted}` : null,
    0,
    0,
    (_path, options) =>
      evaluationsApi.predictions(runId, { model, gold: cell!.gold, predicted: cell!.predicted }, options.signal ?? undefined),
  )
  return (
    <Dialog open={cell !== null} onOpenChange={(open) => { if (!open) onClose() }}>
      <DialogContent className="eval-drawer" showCloseButton={false}>
        <DialogHeader>
          <DialogTitle>
            {cell ? fill(copy.drawer.title, { gold: label(cell.gold), predicted: label(cell.predicted) }) : ""}
          </DialogTitle>
        </DialogHeader>
        {page.loading ? (
          <LoadingState />
        ) : page.error ? (
          <p className="error-text">{page.error}</p>
        ) : (
          <PredictionsList items={page.data?.items ?? []} total={page.data?.total ?? 0} />
        )}
        <DialogFooter>
          <Button variant="outline" onClick={onClose}>{copy.drawer.close}</Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  )
}
```

`useResource` takes a loader `(path, options) => Promise<T>`; the path string is only the cache key here, so the loader ignores it. The loader identity changes every render, which would re-run the effect: wrap it in `useCallback` keyed on `runId, model, cell?.gold, cell?.predicted`:

```tsx
  const loader = useCallback(
    (_path: string, options: RequestInit) =>
      evaluationsApi.predictions(runId, { model, gold: cell!.gold, predicted: cell!.predicted },
        options.signal ?? undefined),
    // eslint-disable-next-line react-hooks/exhaustive-deps
    [runId, model, cell?.gold, cell?.predicted],
  )
```

and pass `loader` as the fourth argument (import `useCallback` from `react`).

- [ ] **Step 5: Implement `ModelDetail.tsx`**

```tsx
import { useState } from "react"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table"
import { FilterSelect } from "@/components/shared/workspace-ui"
import { categoryLabel, percent1 } from "@/lib/format"
import { fill, useCopy } from "@/lib/locale"
import type { Prf } from "@/lib/types"
import { ConfusionMatrix } from "./ConfusionMatrix"
import { modelLabel, type ComparisonRow } from "./eval-view"
import { PredictionsDrawer } from "./PredictionsDrawer"

function PrfTable({ title, values, label }: { title: string; values: Record<string, Prf>; label: (id: string) => string }) {
  const copy = useCopy().evaluation
  return (
    <Table>
      <TableHeader>
        <TableRow>
          <TableHead>{title}</TableHead>
          <TableHead title={copy.metricHelp.macroP}>{copy.detail.precision}</TableHead>
          <TableHead title={copy.metricHelp.macroR}>{copy.detail.recall}</TableHead>
          <TableHead>{copy.detail.f1}</TableHead>
          <TableHead>{copy.detail.support}</TableHead>
        </TableRow>
      </TableHeader>
      <TableBody>
        {Object.entries(values).map(([id, v]) => (
          <TableRow key={id}>
            <TableCell>{label(id)}</TableCell>
            <TableCell>{percent1(v.precision)}</TableCell>
            <TableCell>{percent1(v.recall)}</TableCell>
            <TableCell>{percent1(v.f1)}</TableCell>
            <TableCell>{v.support}</TableCell>
          </TableRow>
        ))}
      </TableBody>
    </Table>
  )
}

export function ModelDetail({ rows, runId }: { rows: ComparisonRow[]; runId: number | null }) {
  const copy = useCopy().evaluation
  const withResults = rows.filter((row) => row.summary)
  const [selected, setSelected] = useState<string | null>(null)
  const [cell, setCell] = useState<{ gold: string; predicted: string } | null>(null)
  const row = withResults.find((r) => r.model.id === selected) ?? withResults[0]
  if (!row?.summary) return null
  const s = row.summary
  const flagName = (id: string) => (copy.flagNames as Record<string, string>)[id] ?? id
  const fieldName = (id: string) => (copy.fieldNames as Record<string, string>)[id] ?? id
  const tagName = (id: string) => (copy.tags as Record<string, string>)[id] ?? id
  return (
    <Card className="data-card eval-detail">
      <CardHeader>
        <CardTitle>{copy.detail.title}</CardTitle>
        <FilterSelect
          label={copy.detail.model}
          value={row.model.id}
          options={withResults.map((r) => ({ value: r.model.id, label: modelLabel(r.model) }))}
          onChange={setSelected}
        />
      </CardHeader>
      <CardContent>
        {row.model.provider !== "typesafe" && <p className="field-help">{copy.detail.selfReported}</p>}
        <Tabs defaultValue="categories">
          <TabsList>
            <TabsTrigger value="categories">{copy.detail.categories}</TabsTrigger>
            <TabsTrigger value="confusion">{copy.detail.confusion}</TabsTrigger>
            <TabsTrigger value="flags">{copy.detail.flags}</TabsTrigger>
            <TabsTrigger value="extraction">{copy.detail.extraction}</TabsTrigger>
            <TabsTrigger value="slices">{copy.detail.slices}</TabsTrigger>
          </TabsList>
          <TabsContent value="categories">
            <PrfTable title={copy.detail.category} values={s.classification.per_category} label={categoryLabel} />
          </TabsContent>
          <TabsContent value="confusion">
            <ConfusionMatrix
              confusion={s.classification.confusion}
              onSelect={runId ? (gold, predicted) => setCell({ gold, predicted }) : undefined}
            />
          </TabsContent>
          <TabsContent value="flags">
            <PrfTable title={copy.detail.flag} values={s.flags} label={flagName} />
          </TabsContent>
          <TabsContent value="extraction">
            <PrfTable title={copy.detail.field} values={s.extraction.per_field} label={fieldName} />
            <p className="field-help">
              {fill(copy.detail.hallucination, { value: percent1(s.extraction.hallucination_rate) })}
              {" · "}
              {fill(copy.detail.missed, { value: percent1(s.extraction.missed_rate) })}
            </p>
          </TabsContent>
          <TabsContent value="slices">
            <Table>
              <TableHeader>
                <TableRow>
                  <TableHead>{copy.detail.slice}</TableHead>
                  <TableHead>{copy.detail.support}</TableHead>
                  <TableHead>{copy.detail.accuracy}</TableHead>
                  <TableHead>{copy.detail.errorRate}</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {Object.entries(s.slices).map(([tag, v]) => (
                  <TableRow key={tag}>
                    <TableCell>{tagName(tag)}</TableCell>
                    <TableCell>{v.n}</TableCell>
                    <TableCell>{percent1(v.accuracy)}</TableCell>
                    <TableCell>{percent1(v.error_rate)}</TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </TabsContent>
        </Tabs>
        {runId && <PredictionsDrawer runId={runId} model={row.model.id} cell={cell} onClose={() => setCell(null)} />}
      </CardContent>
    </Card>
  )
}
```

- [ ] **Step 6: Run tests to verify they pass**

Run: `npm test -- src/features/evaluation && npm run lint && npm run typecheck`
Expected: all PASS. If base-ui `Tabs` does not render the default panel in static markup, keep the test's `"Failed transfer"` assertion by rendering `PrfTable` directly in that test (export it) — do not remove the Tabs from the component.

- [ ] **Step 7: Commit**

```bash
git add employee-frontend/src/features/evaluation
git commit -m "feat: add per-model detail with confusion matrix drill-down"
```

---

### Task 17: Run dialog, progress, page assembly, route and styles

**Files:**
- Create: `employee-frontend/src/features/evaluation/RunEvaluationDialog.tsx`
- Create: `employee-frontend/src/features/evaluation/EvaluationProgress.tsx`
- Create: `employee-frontend/src/features/evaluation/EvaluationPage.tsx`
- Delete: `employee-frontend/src/features/insights/EvaluationPage.tsx`
- Modify: `employee-frontend/src/App.tsx` (import path)
- Modify: `employee-frontend/src/styles/workspace.css` (append evaluation styles)
- Test: `employee-frontend/src/features/evaluation/page.test.tsx`

**Interfaces:**
- Consumes: everything above; `useWorkspace().notify`, `health.capabilities.evaluation`.
- Produces:
  - `ModelChoiceList({ models, selected, onToggle }: { models: EvalModelOption[]; selected: string[]; onToggle: (id: string) => void })`
  - `RunEvaluationDialog({ open, onClose, onStarted }: { open: boolean; onClose: () => void; onStarted: (run: EvalRun) => void })`
  - `EvaluationProgress({ run, onCancel }: { run: EvalRun; onCancel: () => void })`
  - `EvaluationPage()` (route `/evaluation`)

- [ ] **Step 1: Write the failing tests**

Create `employee-frontend/src/features/evaluation/page.test.tsx`:

```tsx
import { renderToStaticMarkup } from "react-dom/server"
import { MemoryRouter } from "react-router-dom"
import { afterEach, expect, it } from "vitest"
import { getLocale, setLocale } from "@/lib/locale"
import type { EvalModelOption } from "@/lib/types"
import { WorkspaceContext } from "@/lib/workspace"
import { EvaluationPage } from "./EvaluationPage"
import { EvaluationProgress } from "./EvaluationProgress"
import { run } from "./fixtures"
import { ModelChoiceList } from "./RunEvaluationDialog"

const originalLocale = getLocale()
afterEach(() => setLocale(originalLocale))

const options: EvalModelOption[] = [
  { ...run.models[0], availability: "ready" },
  { ...run.models[2], availability: "unreachable" },
]

it("disables unavailable models and explains why", () => {
  setLocale("en")
  const html = renderToStaticMarkup(<ModelChoiceList models={options} selected={["jev"]} onToggle={() => {}} />)
  expect(html).toContain("Not reachable")
  expect(html.match(/disabled=""/g)?.length).toBe(1)
  expect(html).toContain("checked")
})

it("shows per-model progress for a running evaluation", () => {
  setLocale("ar")
  const running = { ...run, status: "running" as const,
    progress: { jev: { done: 40, total: 100 }, "openrouter:anthropic/claude-sonnet-5.5": { done: 0, total: 100 },
                "ollama:qwen3:4b": { done: 0, total: 100 } } }
  const html = renderToStaticMarkup(<EvaluationProgress run={running} onCancel={() => {}} />)
  expect(html).toContain("التقييم #3 قيد التشغيل")
  expect(html).toContain("40 من 100")
  expect(html).toContain("إلغاء التقييم")
})

it("renders the page shell in Arabic", () => {
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
  expect(html).toContain("تشغيل التقييم")
  expect(html).toContain("استيراد تقرير")
  expect(html).not.toContain("Import results")
  expect(html).not.toContain("Classification strategy")
})
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `npm test -- src/features/evaluation/page.test.tsx`
Expected: FAIL (modules not found).

- [ ] **Step 3: Implement `EvaluationProgress.tsx`**

```tsx
import { Button } from "@/components/ui/button"
import { Card, CardContent } from "@/components/ui/card"
import { StatusBadge } from "@/components/shared/workspace-ui"
import { fill, useCopy } from "@/lib/locale"
import type { EvalRun } from "@/lib/types"
import { modelLabel } from "./eval-view"

export function EvaluationProgress({ run, onCancel }: { run: EvalRun; onCancel: () => void }) {
  const copy = useCopy().evaluation
  return (
    <Card className="run-progress-card eval-progress">
      <CardContent>
        <div>
          <h2>{fill(copy.progress.title, { id: run.id })}</h2>
          <Button variant="outline" onClick={onCancel} disabled={run.cancel_requested}>
            {run.cancel_requested ? copy.progress.cancelling : copy.progress.cancel}
          </Button>
        </div>
        {run.models.map((model) => {
          const p = run.progress[model.id] ?? { done: 0, total: run.sample_size }
          const pct = p.total ? Math.round((p.done / p.total) * 100) : 0
          const status = run.model_status[model.id]?.status ?? "pending"
          return (
            <div key={model.id} className="eval-progress-row">
              <bdi dir="ltr">{modelLabel(model)}</bdi>
              <span className="muted small">{copy.status[status]}</span>
              <div className="run-progress" role="progressbar" aria-label={modelLabel(model)}
                   aria-valuenow={pct} aria-valuemin={0} aria-valuemax={100}>
                <span style={{ width: `${pct}%` }} />
              </div>
              <span className="muted small">{fill(copy.progress.model, { done: p.done, total: p.total })}</span>
            </div>
          )
        })}
        <StatusBadge status={run.status} />
      </CardContent>
    </Card>
  )
}
```

`StatusBadge` uses the global `status` copy (it already has `running`, `completed`, `failed`); add `"queued"` and `"cancelled"` to the top-level `status` object in both locale files (`"queued": "Queued"` / `"في الانتظار"`, `"cancelled": "Cancelled"` / `"أُلغي"`).

- [ ] **Step 4: Implement `RunEvaluationDialog.tsx`**

```tsx
import { useEffect, useState } from "react"
import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog"
import { useResource } from "@/hooks/use-resource"
import { evaluationsApi } from "@/lib/api"
import { usd } from "@/lib/format"
import { fill, useCopy } from "@/lib/locale"
import type { EvalEstimate, EvalModelOption, EvalRun } from "@/lib/types"
import { evaluationErrorMessage, modelLabel } from "./eval-view"

export function ModelChoiceList({
  models,
  selected,
  onToggle,
}: {
  models: EvalModelOption[]
  selected: string[]
  onToggle: (id: string) => void
}) {
  const copy = useCopy().evaluation
  return (
    <fieldset className="eval-choices">
      <legend>{copy.dialog.models}</legend>
      {models.map((m) => {
        const ready = m.availability === "ready"
        return (
          <label key={m.id} className={ready ? undefined : "muted"}>
            <input
              type="checkbox"
              checked={ready && selected.includes(m.id)}
              disabled={!ready}
              onChange={() => onToggle(m.id)}
            />
            <bdi dir="ltr">{modelLabel(m)}</bdi>
            {m.locality === "local" && <Badge variant="secondary">{copy.table.local}</Badge>}
            <Badge variant="outline">{copy.availability[m.availability]}</Badge>
          </label>
        )
      })}
    </fieldset>
  )
}

export function RunEvaluationDialog({
  open,
  onClose,
  onStarted,
}: {
  open: boolean
  onClose: () => void
  onStarted: (run: EvalRun) => void
}) {
  const copy = useCopy().evaluation
  const models = useResource<EvalModelOption[]>(open ? "/evaluations/models" : null)
  const [selected, setSelected] = useState<string[]>([])
  const [split, setSplit] = useState<"dev" | "test">("dev")
  const [estimate, setEstimate] = useState<EvalEstimate | null>(null)
  const [error, setError] = useState("")
  const [starting, setStarting] = useState(false)
  const ready = (models.data ?? []).filter((m) => m.availability === "ready").map((m) => m.id)
  const chosen = selected.filter((id) => ready.includes(id))

  useEffect(() => {
    if (models.data) setSelected(models.data.filter((m) => m.availability === "ready").map((m) => m.id))
  }, [models.data])

  useEffect(() => {
    if (!open || !chosen.length) {
      setEstimate(null)
      return
    }
    let cancelled = false
    evaluationsApi
      .estimate(chosen, split)
      .then((value) => { if (!cancelled) { setEstimate(value); setError("") } })
      .catch((e) => { if (!cancelled) { setEstimate(null); setError(evaluationErrorMessage(e, copy)) } })
    return () => { cancelled = true }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [open, split, chosen.join(",")])

  async function start() {
    if (!chosen.length) return setError(copy.dialog.noneSelected)
    setStarting(true)
    try {
      onStarted(await evaluationsApi.start(chosen, split))
    } catch (e) {
      setError(evaluationErrorMessage(e, copy))
    } finally {
      setStarting(false)
    }
  }

  return (
    <Dialog open={open} onOpenChange={(value) => { if (!value) onClose() }}>
      <DialogContent className="eval-dialog" showCloseButton={false}>
        <DialogHeader>
          <DialogTitle>{copy.dialog.title}</DialogTitle>
          <DialogDescription>{copy.dialog.description}</DialogDescription>
        </DialogHeader>
        {models.loading ? (
          <p className="muted small">{copy.dialog.loadingModels}</p>
        ) : (
          <ModelChoiceList
            models={models.data ?? []}
            selected={chosen}
            onToggle={(id) =>
              setSelected((old) => (old.includes(id) ? old.filter((x) => x !== id) : [...old, id]))
            }
          />
        )}
        <fieldset className="eval-choices">
          <legend>{copy.dialog.split}</legend>
          {(["dev", "test"] as const).map((value) => (
            <label key={value}>
              <input type="radio" name="eval-split" checked={split === value} onChange={() => setSplit(value)} />
              {copy.split[value]}
            </label>
          ))}
          {split === "test" && <p className="field-help">{copy.dialog.testWarning}</p>}
        </fieldset>
        <div className="eval-estimate">
          <strong>{copy.dialog.estimate}</strong>
          {estimate ? (
            <>
              <ul>
                {chosen.map((id) => (
                  <li key={id}>
                    <bdi dir="ltr">{id}</bdi> · {usd(estimate.models[id]?.cost_usd)}
                  </li>
                ))}
              </ul>
              <p>{fill(copy.dialog.total, { value: usd(estimate.total_usd) })}</p>
              {estimate.unknown && <p className="field-help">{copy.dialog.unknown}</p>}
            </>
          ) : chosen.length ? (
            <p className="muted small">{copy.dialog.estimating}</p>
          ) : null}
        </div>
        {error && <p className="error-text" role="alert">{error}</p>}
        <DialogFooter>
          <Button variant="outline" onClick={onClose}>{copy.dialog.cancel}</Button>
          <Button onClick={() => void start()} disabled={starting || !chosen.length}>
            {starting ? copy.dialog.starting : copy.dialog.start}
          </Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  )
}
```

- [ ] **Step 5: Implement `EvaluationPage.tsx`**

```tsx
import { useRef, useState } from "react"
import { FileUp, Play } from "lucide-react"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { ErrorState, FilterSelect, LoadingState, PageHeader } from "@/components/shared/workspace-ui"
import { useResource } from "@/hooks/use-resource"
import { evaluationsApi } from "@/lib/api"
import { dateLabel } from "@/lib/format"
import { validateEvaluation } from "@/lib/imports"
import { fill, useCopy } from "@/lib/locale"
import type { EvalRun, ImportedReport } from "@/lib/types"
import { useWorkspace } from "@/lib/workspace"
import { comparisonRows, evaluationErrorMessage, isActive, viewFromImport, viewFromRun } from "./eval-view"
import { EvaluationEmptyState } from "./EvaluationEmptyState"
import { EvaluationProgress } from "./EvaluationProgress"
import { HeadlineMetrics } from "./HeadlineMetrics"
import { ModelComparisonTable } from "./ModelComparisonTable"
import { ModelDetail } from "./ModelDetail"
import { ProvenanceStrip } from "./ProvenanceStrip"
import { RunEvaluationDialog } from "./RunEvaluationDialog"

const POLL_MS = 3000
const SCHEMA = `{
  "format": "zaincash-eval/v2",
  "split": "test",
  "sample_size": 100,
  "generated_at": "2026-11-12T10:30:00Z",
  "dataset_sha256": "…",
  "models": { "jev": { "classification": {…}, "system": {…}, "cost": {…} } }
}`

export function EvaluationPage() {
  const copy = useCopy()
  const text = copy.evaluation
  const workspace = useWorkspace()
  const input = useRef<HTMLInputElement>(null)
  const [dialogOpen, setDialogOpen] = useState(false)
  const [selectedId, setSelectedId] = useState<number | null>(null)
  const [imported, setImported] = useState<{ report: ImportedReport; filename: string } | null>(null)
  const [refresh, setRefresh] = useState(0)
  const runs = useResource<EvalRun[]>("/evaluations", workspace.revision + refresh)
  const currentId = selectedId ?? runs.data?.[0]?.id ?? null
  const [pollMs, setPollMs] = useState(0)
  const current = useResource<EvalRun>(
    currentId !== null && !imported ? `/evaluations/${currentId}` : null,
    refresh,
    pollMs,
  )
  const active = isActive(current.data)
  if (active !== (pollMs > 0)) setPollMs(active ? POLL_MS : 0)
  const canRun = Boolean(workspace.health?.capabilities.evaluation) && !active

  async function readReport(file?: File) {
    if (!file) return
    try {
      if (file.size > 2 * 1024 * 1024) throw new Error(text.fileTooLarge)
      setImported({ report: validateEvaluation(JSON.parse(await file.text())), filename: file.name })
      workspace.notify(text.importedNotice)
    } catch (error) {
      workspace.notify(error instanceof Error ? error.message : text.importErrors.object, true)
    } finally {
      if (input.current) input.current.value = ""
    }
  }

  async function cancel(run: EvalRun) {
    try {
      await evaluationsApi.cancel(run.id)
      setRefresh((v) => v + 1)
    } catch (error) {
      workspace.notify(evaluationErrorMessage(error, text), true)
    }
  }

  const view = imported
    ? viewFromImport(imported.report, imported.filename)
    : current.data
      ? viewFromRun(current.data)
      : null
  const rows = view ? comparisonRows(view) : []
  const hasResults = rows.some((row) => row.summary)
  const runOptions = [
    ...(imported ? [{ value: "import", label: fill(text.importedOption, { name: imported.filename }) }] : []),
    ...(runs.data ?? []).map((run) => ({
      value: String(run.id),
      label: fill(text.runOption, { id: run.id, split: text.split[run.split], date: dateLabel(run.created_at) }),
    })),
  ]

  return (
    <>
      <PageHeader title={copy.pages.evaluationTitle} description={copy.pages.evaluationDescription}>
        {runOptions.length > 0 && (
          <FilterSelect
            label={text.runSelect}
            value={imported ? "import" : String(currentId ?? "")}
            options={runOptions}
            onChange={(value) => {
              if (value === "import") return
              setImported(null)
              setSelectedId(Number(value))
            }}
          />
        )}
        <Button variant="outline" onClick={() => input.current?.click()}>
          <FileUp size={16} />
          {text.import}
        </Button>
        <input ref={input} type="file" className="sr-only" aria-label={text.importLabel} accept=".json"
               onChange={(e) => void readReport(e.target.files?.[0])} />
        <Button onClick={() => setDialogOpen(true)} disabled={!canRun}>
          <Play size={16} />
          {text.run}
        </Button>
      </PageHeader>
      {runs.error && <ErrorState message={runs.error} retry={runs.reload} />}
      {!imported && current.data && active && (
        <EvaluationProgress run={current.data} onCancel={() => void cancel(current.data!)} />
      )}
      {!imported && current.data?.error && <p className="error-text">{current.data.error}</p>}
      {runs.loading && !runs.data ? (
        <LoadingState />
      ) : view && hasResults ? (
        <>
          <ProvenanceStrip view={view} />
          <HeadlineMetrics rows={rows} />
          <ModelComparisonTable rows={rows} sampleSize={view.sampleSize} />
          <ModelDetail rows={rows} runId={view.runId} />
          {view.notes.length > 0 && (
            <Card>
              <CardHeader><CardTitle>{text.notes}</CardTitle></CardHeader>
              <CardContent>
                <ul className="confusion-list">
                  {view.notes.map((note, i) => <li key={i} dir="auto">{note}</li>)}
                </ul>
              </CardContent>
            </Card>
          )}
        </>
      ) : !active ? (
        <EvaluationEmptyState onRun={() => setDialogOpen(true)} canRun={canRun} />
      ) : null}
      <details className="report-schema">
        <summary>{text.schema.title}</summary>
        <pre dir="ltr">{SCHEMA}</pre>
        <p>{text.schema.note}</p>
      </details>
      <RunEvaluationDialog
        open={dialogOpen}
        onClose={() => setDialogOpen(false)}
        onStarted={(run) => {
          setDialogOpen(false)
          setImported(null)
          setSelectedId(run.id)
          setRefresh((v) => v + 1)
          workspace.notify(fill(text.dialog.started, { id: run.id }))
        }}
      />
    </>
  )
}
```

The `if (active !== (pollMs > 0)) setPollMs(...)` line is React's documented "adjust state during render" pattern; it switches polling on while a run is active and off when it finishes, without an effect. If the repo's lint rules reject it, move it into `useEffect(() => setPollMs(active ? POLL_MS : 0), [active])`.

- [ ] **Step 6: Route, cleanup and styles**

In `employee-frontend/src/App.tsx`, change the `EvaluationPage` lazy import path from `@/features/insights/EvaluationPage` to `@/features/evaluation/EvaluationPage`.

Delete the old page: `git rm employee-frontend/src/features/insights/EvaluationPage.tsx`.

Append to `employee-frontend/src/styles/workspace.css`:

```css
/* Evaluation */
.eval-table-scroll {
  overflow-x: auto;
}
.eval-comparison th,
.eval-comparison td {
  white-space: nowrap;
}
.eval-model-cell {
  display: flex;
  flex-direction: column;
  gap: 4px;
}
.eval-badges {
  display: flex;
  gap: 4px;
  flex-wrap: wrap;
}
.eval-best {
  font-weight: 700;
  color: var(--green);
}
.eval-row-failed td {
  color: var(--muted-foreground);
}
.eval-badge-failed {
  color: var(--accent-ink);
  border-color: var(--accent-ink);
}
.eval-notes {
  margin-top: 10px;
  display: grid;
  gap: 4px;
  font-size: 12px;
  color: var(--muted-foreground);
}
.eval-matrix {
  border-collapse: collapse;
  font-size: 12px;
}
.eval-matrix caption {
  caption-side: top;
  text-align: start;
  color: var(--muted-foreground);
  padding-bottom: 6px;
}
.eval-matrix th,
.eval-matrix td {
  border: 1px solid var(--border);
  padding: 4px 6px;
  text-align: center;
  min-width: 42px;
}
.eval-matrix th[scope="row"] {
  text-align: start;
  white-space: nowrap;
}
.eval-cell-hit {
  background: color-mix(in srgb, var(--green) calc(var(--share) * 45%), transparent);
}
.eval-cell-miss {
  background: color-mix(in srgb, var(--accent-ink) calc(var(--share) * 45%), transparent);
}
.eval-matrix button {
  all: unset;
  cursor: pointer;
  display: block;
  width: 100%;
}
.eval-matrix button:focus-visible {
  outline: 2px solid #da3345;
}
.eval-predictions {
  display: grid;
  gap: 10px;
  max-height: 60vh;
  overflow-y: auto;
}
.eval-predictions article {
  border: 1px solid var(--border);
  border-radius: 8px;
  padding: 8px 10px;
}
.eval-predictions header {
  display: flex;
  gap: 10px;
  flex-wrap: wrap;
  font-size: 12px;
}
.eval-drawer,
.eval-dialog {
  max-width: min(720px, calc(100% - 2rem)) !important;
}
.eval-choices {
  border: 0;
  padding: 0;
  margin: 0;
  display: grid;
  gap: 6px;
}
.eval-choices legend {
  font-weight: 600;
  margin-bottom: 4px;
}
.eval-choices label {
  display: flex;
  align-items: center;
  gap: 8px;
}
.eval-estimate ul {
  margin: 4px 0;
  padding-inline-start: 18px;
}
.eval-progress-row {
  display: grid;
  grid-template-columns: minmax(140px, 1fr) auto minmax(120px, 2fr) auto;
  align-items: center;
  gap: 10px;
  margin-top: 8px;
}
.report-schema pre[dir="ltr"] {
  text-align: left;
}
```

- [ ] **Step 7: Run all frontend checks**

Run: `npm test && npm run lint && npm run typecheck && npm run build`
Expected: all PASS.

- [ ] **Step 8: Commit**

```bash
git add -A employee-frontend/src
git commit -m "feat: rebuild evaluation page with runs, progress and model comparison"
```

---

### Task 18: Documentation, full verification and manual check

**Files:**
- Modify: `README.md` (evaluation section; remove "held-out evaluation" from remaining work)
- Generated later (manual, with approval): `data/eval/*`

**Interfaces:** none new.

- [ ] **Step 1: Document evaluation in the README**

Add a section to `README.md` (after the Ollama section from Task 1):

```markdown
### Evaluating models

The `/evaluation` page compares the models in `EVAL_MODELS` on the same labelled tickets through
the real pipeline (classification, extraction, transaction lookup and escalation rules; drafting is
skipped). It reports accuracy, precision, recall and F1 (categories, flags, extracted fields,
escalation), p50/p95 response time, error rate, tokens and cost per request. Local Ollama models
are shown as **Local · $0** with tokens per second.

1. Generate the dataset once (needs `OPENROUTER_API_KEY`; costs a few dollars):
   `cd backend && uv run support eval-generate` — then read 50 tickets, fill in the hand-check
   table in `data/eval/data-card.md`, and commit `data/eval/`.
2. Run an evaluation from the page (**Run evaluation**) or the CLI:
   `uv run support eval --models jev,ollama:qwen3:4b --split dev`.
3. Tune prompts on `dev` only. Run `--split test` once per frozen configuration and commit the
   export: `uv run support eval --split test --out eval/results/<date>.json`.
```

In the README's remaining-work list, remove the held-out evaluation item.

- [ ] **Step 2: Run the full automated verification**

From `backend/` (with `docker compose up -d db` running):

```bash
uv run pytest -q
uv run ruff check app tests
```

From `employee-frontend/`:

```bash
npm test
npm run lint
npm run typecheck
npm run build
```

Expected: every command passes. Record the pass counts in the commit message.

- [ ] **Step 3: Commit**

```bash
git add README.md
git commit -m "docs: explain dataset generation and model evaluation"
```

- [ ] **Step 4: Manual check (ask your human partner before spending money)**

These steps call paid APIs and the local Ollama; confirm with your human partner first.

1. `cd backend && uv run support eval-generate` → check `data/eval/generation.json` (300 tickets, 200/100), skim 50 tickets, fill in the data card, commit `data/eval/`.
2. Start Ollama with `qwen3:4b`; confirm `curl $OLLAMA_BASE_URL/api/tags` from WSL lists it.
3. Start the API and frontend (`uvicorn app.main:app --port 8000`, `npm run dev`), open `http://localhost:5173/evaluation`:
   - Arabic profile: no English UI text; switch to English and back.
   - **Run evaluation** → all four models show **Ready** (or a clear reason) → choose `dev` → check the estimate → start.
   - Watch per-model progress; cancel and restart once to see cancellation.
   - When finished: comparison table (Production / Local · $0 badges, best values), headline cards, model detail tabs, confusion cell drill-down showing ticket text right-to-left.
4. Run `uv run support eval --split test --out eval/results/2026-11-12-test.json` once and commit the export.
