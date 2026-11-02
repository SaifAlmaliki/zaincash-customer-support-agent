import { Link, useParams } from "react-router-dom"
import { ArrowLeft, ArrowRight, CheckCheck, Clock3, Coins, Download, Layers3 } from "lucide-react"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { EmptyState, ErrorState, LoadingState, Metric, PageHeader, StatusBadge } from "@/components/shared/workspace-ui"
import { useResource } from "@/hooks/use-resource"
import { useWorkspace } from "@/lib/workspace"
import { categoryLabel, dateLabel, downloadJson, duration, humanize, timeLabel } from "@/lib/format"
import type { Result, Run } from "@/lib/types"
import { TicketFlow } from "@/features/review/TicketFlow"
import { loadRunResults } from "./run-results"

export function RunDetailPage() {
  const { id } = useParams(),
    workspace = useWorkspace()
  const query = useResource<Run>(`/runs/${id}`, workspace.revision, 2500)
  const run = query.data
  const results = useResource<Result[]>(
    run ? `/results?run_id=${run.id}&limit=500` : null,
    workspace.revision,
    run?.status === "running" ? 2500 : 0,
    loadRunResults,
  )
  if (query.error)
    return <ErrorState message={query.error} retry={query.reload} />
  if (!run)
    return query.loading ? (
      <LoadingState />
    ) : (
      <EmptyState
        title="Run not found"
        description="Choose a run from the pipeline history."
      />
    )
  const progress = run.total ? Math.round((run.processed / run.total) * 100) : 0
  return (
    <>
      <Link to="/runs" className="back-link">
        <ArrowLeft size={15} />
        All pipeline runs
      </Link>
      <PageHeader
        title={`Batch #${String(run.id).padStart(3, "0")}`}
        description={`Started ${dateLabel(run.started_at)} at ${timeLabel(run.started_at)} Baghdad · ${run.mode === "cascade" ? "Jev with Gemini fallback" : humanize(run.mode)}`}
      >
        <Button
          variant="outline"
          onClick={() => downloadJson(run, `batch-${run.id}-summary.json`)}
        >
          <Download size={16} />
          Export summary
        </Button>
        <Button nativeButton={false} render={<Link to={`/?run=${run.id}`} />}>
          Review tickets
          <ArrowRight size={16} />
        </Button>
      </PageHeader>
      <Card className="run-progress-card">
        <CardContent>
          <div>
            <h2>
              {run.status === "running"
                ? "Preparing your tickets"
                : run.status === "failed"
                  ? "Batch interrupted"
                  : "Batch processing finished"}
            </h2>
            <StatusBadge status={run.status} />
          </div>
          <p>
            {run.processed} of {run.total} tickets processed
          </p>
          <div
            className="run-progress"
            role="progressbar"
            aria-label="Batch progress"
            aria-valuenow={progress}
            aria-valuemin={0}
            aria-valuemax={100}
          >
            <span style={{ width: `${progress}%` }} />
          </div>
          {run.counts.error && <p className="error-text">{run.counts.error}</p>}
          {run.degraded && run.mode === "cascade" && (
            <p className="field-help">
              Jev was unavailable for part of this run. Gemini fallback is
              recorded in the results.
            </p>
          )}
        </CardContent>
      </Card>
      <div className="metrics-grid">
        <Metric
          label="Processed"
          value={run.processed}
          detail={`Of ${run.total} submitted tickets`}
          icon={<Layers3 size={18} />}
        />
        <Metric
          label="Needs human review"
          value={run.counts.by_status?.escalated || 0}
          detail="Review the escalation notes"
          icon={<CheckCheck size={18} />}
          tone="metric-amber"
        />
        <Metric
          label="Median latency"
          value={duration(run.counts.latency_p50_ms || 0)}
          detail="Per processed ticket"
          icon={<Clock3 size={18} />}
        />
        <Metric
          label="Estimated run cost"
          value={`$${run.total_cost_usd.toFixed(4)}`}
          detail="Based on recorded token usage"
          icon={<Coins size={18} />}
        />
      </div>
      <div className="two-column">
        <Card>
          <CardHeader>
            <CardTitle>Issue breakdown</CardTitle>
          </CardHeader>
          <CardContent>
            <Breakdown
              values={run.counts.by_category || {}}
              label={categoryLabel}
            />
          </CardContent>
        </Card>
        <Card>
          <CardHeader>
            <CardTitle>Escalation reasons</CardTitle>
          </CardHeader>
          <CardContent>
            <Breakdown
              values={run.counts.escalation_reasons || {}}
              label={humanize}
            />
          </CardContent>
        </Card>
      </div>
      <section className="run-flows">
        {results.error && <p className="error-text">{results.error}</p>}
        {results.data?.map((result) => (
          <div key={result.id}>
            <Link to={`/tickets/${result.id}`} className="run-flow-ticket">
              {result.ticket.external_id}
            </Link>
            <TicketFlow result={result} />
          </div>
        ))}
        {!results.data?.length && !results.loading && (
          <p className="muted small">
            {run.status === "running"
              ? "Steps appear here when a ticket finishes."
              : "No processed ticket to show yet."}
          </p>
        )}
      </section>
    </>
  )
}

function Breakdown({
  values,
  label,
}: {
  values: Record<string, number>
  label: (value: string) => string
}) {
  const entries = Object.entries(values)
  return entries.length ? (
    <div className="simple-breakdown">
      {entries.map(([key, count]) => (
        <div key={key}>
          <span>{label(key)}</span>
          <strong>{count}</strong>
        </div>
      ))}
    </div>
  ) : (
    <p className="muted small">No data reported for this section.</p>
  )
}
