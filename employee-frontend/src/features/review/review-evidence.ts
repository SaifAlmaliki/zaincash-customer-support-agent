import type { Result, TraceEvent } from "../../lib/types"

function renderableTrace(raw: unknown): TraceEvent[] {
  if (!Array.isArray(raw)) return []
  return raw.filter((event): event is TraceEvent =>
    event !== null && typeof event === "object" && !Array.isArray(event) &&
    ["kind", "node", "status", "tool"].every((key) => event[key] === undefined || typeof event[key] === "string") &&
    (event.elapsed_ms === undefined || (typeof event.elapsed_ms === "number" && Number.isFinite(event.elapsed_ms)))
  )
}

export function reviewEvidence(
  result: Pick<Result, "citations" | "citation_sources" | "agent_trace">
) {
  const trace = renderableTrace(result.agent_trace)
  const ids = [...new Set(result.citations)]
  const snapshots = new Map(
    (result.citation_sources ?? []).map((source) => [source.id, source])
  )
  return {
    sources: ids.flatMap((id) =>
      snapshots.has(id) ? [snapshots.get(id)!] : []
    ),
    missingIds: ids.filter((id) => !snapshots.has(id)),
    stages: trace.filter((event) => event.kind === "stage"),
    tools: trace.filter((event) => event.kind === "tool"),
    otherEvents: trace.filter(
      (event) => event.kind !== "tool" && event.kind !== "stage"
    ),
  }
}
