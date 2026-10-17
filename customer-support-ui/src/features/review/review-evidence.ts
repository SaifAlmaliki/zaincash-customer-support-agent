import type { Result } from "../../lib/types"

export function reviewEvidence(
  result: Pick<Result, "citations" | "citation_sources" | "agent_trace">
) {
  const ids = [...new Set(result.citations)]
  const snapshots = new Map(
    (result.citation_sources ?? []).map((source) => [source.id, source])
  )
  return {
    sources: ids.flatMap((id) =>
      snapshots.has(id) ? [snapshots.get(id)!] : []
    ),
    missingIds: ids.filter((id) => !snapshots.has(id)),
    tools: result.agent_trace.filter((event) => event.kind === "tool"),
    otherEvents: result.agent_trace.filter(
      (event) => event.kind !== "tool" && event.kind !== "stage"
    ),
  }
}
