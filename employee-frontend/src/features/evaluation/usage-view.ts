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

export type CostMark = "local" | "estimate" | "unknown" | "partial" | null

// "unknown": every call lacks a price; "partial": some do, so the shown cost is a lower bound.
export function sourceMark(sources: Partial<Record<CostSource, number>>): CostMark {
  const used = (Object.keys(sources) as CostSource[]).filter((s) => (sources[s] ?? 0) > 0)
  if (used.length && used.every((s) => s === "local")) return "local"
  if (used.length && used.every((s) => s === "unknown")) return "unknown"
  if (used.includes("unknown")) return "partial"
  if (used.includes("estimate")) return "estimate"
  return null
}

export function mergeModels(seen: string[], current: string[]) {
  const missing = current.filter((model) => !seen.includes(model))
  return missing.length ? [...seen, ...missing].sort() : seen
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
