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
  expect(markup).toContain("1.5 s")
  expect(markup).not.toContain("مللي")
})

it("keeps English in English", () => {
  setLocale("en")
  expect(html()).toContain("2 of 4 tickets processed")
})
