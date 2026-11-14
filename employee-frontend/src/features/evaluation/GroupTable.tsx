import { Badge } from "@/components/ui/badge"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table"
import { countLabel, msLabel, percent1, usd } from "@/lib/format"
import { useCopy } from "@/lib/locale"
import type { AiSummary, UsageGroup } from "@/lib/types"
import { CostValue } from "./CostValue"
import { isInUse, processLabel, shareWidth } from "./usage-view"

export function GroupTable({ kind, groups, ai }: { kind: "process" | "model"; groups: UsageGroup[]; ai?: AiSummary }) {
  const copy = useCopy().evaluation
  const t = copy.table
  return (
    <Card className="data-card usage-groups">
      <CardHeader>
        <CardTitle>{kind === "process" ? copy.byProcess : copy.byModel}</CardTitle>
      </CardHeader>
      <CardContent>
        {!groups.length ? (
          <p className="muted small">{t.empty}</p>
        ) : (
          <div className="usage-scroll">
            <Table>
              <TableHeader>
                <TableRow>
                  <TableHead>{kind === "process" ? t.process : t.model}</TableHead>
                  {kind === "model" && <TableHead className="usage-col-mid">{t.serves}</TableHead>}
                  <TableHead>{t.calls}</TableHead>
                  <TableHead>{t.cost}</TableHead>
                  <TableHead title={copy.metricHelp.share}>{t.share}</TableHead>
                  <TableHead className="usage-col-wide">{t.perCall}</TableHead>
                  <TableHead title={copy.metricHelp.latency}>{t.latency}</TableHead>
                  <TableHead title={copy.metricHelp.errors}>{t.errors}</TableHead>
                  <TableHead className="usage-col-wide">{t.tokens}</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {groups.map((g) => (
                  <TableRow key={g.key}>
                    <TableCell className={kind === "model" ? "usage-wrap" : undefined}>
                      {kind === "process" ? (
                        processLabel(g.process ?? g.key, copy)
                      ) : (
                        <span className="usage-model">
                          <bdi dir="ltr">{g.key}</bdi>
                          {g.locality === "local" && <Badge variant="secondary">{t.local}</Badge>}
                          {isInUse(g, ai) && <Badge variant="outline">{t.inUse}</Badge>}
                        </span>
                      )}
                    </TableCell>
                    {kind === "model" && (
                      <TableCell className="usage-col-mid usage-wrap">
                        {(g.processes ?? []).map((p) => processLabel(p, copy)).join("، ")}
                      </TableCell>
                    )}
                    <TableCell>{countLabel(g.calls)}</TableCell>
                    <TableCell><CostValue value={g.cost_usd} sources={g.cost_sources} /></TableCell>
                    <TableCell>
                      <span className="usage-share"><span style={{ width: shareWidth(g.cost_share) }} /></span>
                      <small>{percent1(g.cost_share)}</small>
                    </TableCell>
                    <TableCell className="usage-col-wide">{usd(g.cost_per_call)}</TableCell>
                    <TableCell>{msLabel(g.latency_p50_ms)} / {msLabel(g.latency_p95_ms)}</TableCell>
                    <TableCell className={g.error_rate ? "error-text" : undefined}>{percent1(g.error_rate)}</TableCell>
                    <TableCell className="usage-col-wide">
                      {countLabel(g.input_tokens)} / {countLabel(g.output_tokens)}
                    </TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </div>
        )}
      </CardContent>
    </Card>
  )
}
