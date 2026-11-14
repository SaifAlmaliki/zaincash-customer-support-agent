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

// A ticket's calls span minutes (intake, then the pipeline), so wall-clock positions leave
// each bar ~1% wide; bars instead compare each call's latency with the slowest call.
export function durationBars(calls: AiCallView[]) {
  const slowest = Math.max(1, ...calls.map((c) => c.latency_ms))
  return calls.map((call) => ({ call, width: Math.max(2, Math.round((call.latency_ms / slowest) * 100)) }))
}

const REJECTED_OUTPUT = new Set(["InvalidEvidence", "ValidationError", "ParsingError", "OutputParserException"])

export function rejection(calls: AiCallView[], index: number): "retried" | "rejected" | null {
  const call = calls[index]
  if (!call || call.status !== "error" || !REJECTED_OUTPUT.has(call.error ?? "")) return null
  return calls.slice(index + 1).some((c) => c.process === call.process) ? "retried" : "rejected"
}

export function trendGeometry(days: UsageDay[], height = 120, minSlots = 7) {
  const width = Math.max(minSlots, days.length) * 40
  if (!days.length) return { bars: [], line: "", points: [], width, height }
  const maxCost = Math.max(...days.map((d) => d.cost_usd), 1e-12)
  const maxLatency = Math.max(...days.map((d) => d.latency_p95_ms ?? 0), 1)
  const bars = days.map((day, i) => {
    const h = (day.cost_usd / maxCost) * 100
    return { day, x: i * 40 + 8, y: height - (h / 100) * height, h }
  })
  const points = days.map((d, i) => ({ x: i * 40 + 20, y: height - ((d.latency_p95_ms ?? 0) / maxLatency) * height }))
  const line = points.map((p, i) => `${i ? "L" : "M"}${p.x},${p.y}`).join(" ")
  return { bars, line, points, width, height }
}

export function processLabel(process: string, copy: Copy["evaluation"]) {
  return (copy.processes as Record<string, string>)[process] ?? process
}
