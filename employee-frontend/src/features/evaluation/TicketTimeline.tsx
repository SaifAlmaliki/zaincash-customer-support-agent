import { Button } from "@/components/ui/button"
import { Dialog, DialogContent, DialogFooter, DialogHeader, DialogTitle } from "@/components/ui/dialog"
import { ErrorState, LoadingState } from "@/components/shared/workspace-ui"
import { useResource } from "@/hooks/use-resource"
import { clockLabel, countLabel, msLabel, usd } from "@/lib/format"
import { fill, useCopy } from "@/lib/locale"
import type { TicketCalls } from "@/lib/types"
import { CostValue } from "./CostValue"
import { durationBars, processLabel, rejection } from "./usage-view"

export function TimelineView({ data }: { data: TicketCalls }) {
  const copy = useCopy().evaluation
  const tl = copy.timeline
  if (!data.calls.length) return <p className="muted small">{tl.empty}</p>
  const total = data.calls.reduce((sum, c) => sum + c.cost_usd, 0)
  return (
    <div className="usage-timeline">
      <p className="field-help">
        {fill(tl.total, { calls: data.calls.length, cost: usd(total), time: msLabel(data.result.ai_time_ms) })}
      </p>
      {durationBars(data.calls).map(({ call, width }, index) => {
        const rejected = rejection(data.calls, index)
        return (
          <div key={call.id} className="usage-timeline-row">
            <div className="usage-timeline-label">
              <strong>{processLabel(call.process, copy)}</strong>
              <small>
                <bdi dir="ltr">{call.model}</bdi>
                {call.attempt > 1 && <> · {fill(tl.attempt, { n: call.attempt })}</>}
              </small>
            </div>
            <bdi dir="ltr" className="usage-timeline-clock">{clockLabel(call.started_at)}</bdi>
            <div className="usage-track">
              <span className={call.status === "error" ? "usage-bar-error" : "usage-bar-ok"}
                    style={{ width: `${width}%` }} />
            </div>
            <div className="usage-timeline-meta">
              <strong>{msLabel(call.latency_ms)}</strong>
              <span>{fill(tl.tokens, { in: countLabel(call.input_tokens), out: countLabel(call.output_tokens) })}</span>
              <CostValue value={call.cost_usd} sources={{ [call.cost_source]: 1 }} />
              {call.error && (
                <span className={rejected ? "usage-rejected" : "error-text"}>
                  {rejected ? (rejected === "retried" ? `${tl.rejected} · ${tl.retried}` : tl.rejected) : tl.error}
                  {" "}(<bdi dir="ltr">{call.error}</bdi>)
                </span>
              )}
            </div>
          </div>
        )
      })}
    </div>
  )
}

export function TicketTimeline({ resultId, onClose }: { resultId: number | null; onClose: () => void }) {
  const copy = useCopy().evaluation.timeline
  const data = useResource<TicketCalls>(resultId === null ? null : `/ai-usage/tickets/${resultId}/calls`)
  return (
    <Dialog open={resultId !== null} onOpenChange={(open) => { if (!open) onClose() }}>
      <DialogContent className="usage-dialog" showCloseButton={false}>
        <DialogHeader>
          <DialogTitle>
            {data.data ? fill(copy.title, { id: data.data.result.external_id }) : copy.loading}
          </DialogTitle>
        </DialogHeader>
        {data.error ? (
          <ErrorState message={data.error} retry={data.reload} />
        ) : !data.data ? (
          <LoadingState />
        ) : (
          <TimelineView data={data.data} />
        )}
        <DialogFooter>
          <Button variant="outline" onClick={onClose}>{copy.close}</Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  )
}
