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
