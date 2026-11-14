import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { countLabel } from "@/lib/format"
import { useCopy } from "@/lib/locale"
import type { UsageSummary } from "@/lib/types"
import { CostValue } from "./CostValue"
import { processLabel } from "./usage-view"

export function UnattributedCard({ data }: { data: UsageSummary["unattributed"] }) {
  const copy = useCopy().evaluation
  return (
    <Card className="data-card">
      <CardHeader>
        <CardTitle>{copy.unattributed.title}</CardTitle>
      </CardHeader>
      <CardContent>
        <p className="field-help">{copy.unattributed.body}</p>
        {!data.by_process.length ? (
          <p className="muted small">{copy.unattributed.empty}</p>
        ) : (
          <div className="simple-breakdown">
            {data.by_process.map((g) => (
              <div key={g.key}>
                <span>{processLabel(g.process ?? g.key, copy)} · {countLabel(g.calls)}</span>
                <strong><CostValue value={g.cost_usd} sources={g.cost_sources} /></strong>
              </div>
            ))}
          </div>
        )}
      </CardContent>
    </Card>
  )
}
