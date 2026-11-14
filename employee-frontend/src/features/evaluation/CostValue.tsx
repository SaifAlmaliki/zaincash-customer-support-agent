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
  if (mark === "unknown") return <span title={copy.sources.unknown}>—</span>
  return (
    <span title={mark === "partial" ? copy.partlyUnknown : mark ? copy.sources[mark] : copy.sources.provider}>
      {usd(value)}
      {mark === "estimate" && <small className="usage-mark"> {copy.estimated}</small>}
      {mark === "partial" && <small className="usage-mark"> {copy.partlyUnknown}</small>}
    </span>
  )
}
