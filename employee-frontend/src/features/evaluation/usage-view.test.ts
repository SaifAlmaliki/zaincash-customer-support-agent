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
