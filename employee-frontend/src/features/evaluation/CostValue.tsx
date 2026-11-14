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
