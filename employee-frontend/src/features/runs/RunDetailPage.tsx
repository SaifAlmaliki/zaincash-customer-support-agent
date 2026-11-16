import { Link, useParams } from "react-router-dom"
import { ArrowLeft, ArrowRight, CheckCheck, Clock3, Coins, Download, Layers3 } from "lucide-react"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { EmptyState, ErrorState, LoadingState, Metric, PageHeader, StatusBadge } from "@/components/shared/workspace-ui"
import { useResource } from "@/hooks/use-resource"
import { fill, useCopy } from "@/lib/locale"
import { useWorkspace } from "@/lib/workspace"
import { categoryLabel, dateLabel, downloadJson, duration, reasonLabel, timeLabel } from "@/lib/format"
import type { Result, Run } from "@/lib/types"
import { TicketFlow } from "@/features/review/TicketFlow"
import { runModelRows } from "./run-models"
import { loadRunResults } from "./run-results"

export function RunDetailPage() {
  const { id } = useParams(),
    workspace = useWorkspace()
  const copy = useCopy()
  const query = useResource<Run>(`/runs/${id}`, workspace.revision, 2500)
  const run = query.data
  const results = useResource<Result[]>(
    run ? `/results?run_id=${run.id}&limit=500` : null,
    workspace.revision,
    run?.status === "running" ? 2500 : 0,
    loadRunResults,
  )
  if (query.error) return <ErrorState message={query.error} retry={query.reload} />
  if (!run)
    return query.loading ? (
      <LoadingState />
    ) : (
      <EmptyState title={copy.runDetail.notFound} description={copy.runDetail.notFoundBody} />
    )
  return (
    <RunDetailView run={run} results={results.data} resultsError={results.error} resultsLoading={results.loading} />
  )
}

export function RunDetailView({
  run,
  results,
  resultsError,
  resultsLoading,
}: {
  run: Run
  results: Result[] | null
  resultsError: string | null
  resultsLoading: boolean
}) {
  const copy = useCopy()
  const text = copy.runDetail
  const progress = run.total ? Math.round((run.processed / run.total) * 100) : 0
  const models = runModelRows(run.model_ids)
  return (
    <>
      <Link to="/runs" className="back-link">
        <ArrowLeft size={15} />
        {text.back}
      </Link>
      <PageHeader
        title={fill(copy.runs.batchName, { id: String(run.id).padStart(3, "0") })}
        description={fill(text.started, {
          date: dateLabel(run.started_at),
          time: timeLabel(run.started_at),
          mode: run.mode === "cascade" ? text.modeCascade : copy.runs.classifierJev,
        })}
      >
        <Button variant="outline" onClick={() => downloadJson(run, `batch-${run.id}-summary.json`)}>
          <Download size={16} />
          {text.export}
        </Button>
        <Button nativeButton={false} render={<Link to={`/?run=${run.id}`} />}>
          {text.review}
          <ArrowRight size={16} />
        </Button>
      </PageHeader>
      <Card className="run-progress-card">
        <CardContent>
          <div>
            <h2>{run.status === "running" ? text.running : run.status === "failed" ? text.interrupted : text.finished}</h2>
            <StatusBadge status={run.status} />
          </div>
          <p>{fill(text.progress, { processed: run.processed, total: run.total })}</p>
          <div className="run-progress" role="progressbar" aria-label={text.progressLabel}
               aria-valuenow={progress} aria-valuemin={0} aria-valuemax={100}>
            <span style={{ width: `${progress}%` }} />
          </div>
          {run.counts.error && <p className="error-text">{run.counts.error}</p>}
          {run.degraded && run.mode === "cascade" && <p className="field-help">{text.degraded}</p>}
        </CardContent>
      </Card>
      <div className="metrics-grid">
        <Metric label={text.processed} value={run.processed}
                detail={fill(text.processedDetail, { total: run.total })} icon={<Layers3 size={18} />} />
        <Metric label={text.needsReview} value={run.counts.by_status?.escalated || 0}
                detail={text.needsReviewDetail} icon={<CheckCheck size={18} />} tone="metric-amber" />
        <Metric label={text.latency} value={duration(run.counts.latency_p50_ms || 0)}
                detail={text.latencyDetail} icon={<Clock3 size={18} />} />
        <Metric label={text.cost} value={`$${run.total_cost_usd.toFixed(4)}`}
                detail={text.costDetail} icon={<Coins size={18} />} />
      </div>
      {models.length > 0 && (
        <Card className="run-models-card">
          <CardHeader>
            <CardTitle>{copy.models.usedTitle}</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="simple-breakdown">
              {models.map((row) => (
                <div key={row.step}>
                  <span>{copy.models.steps[row.step]}</span>
                  <strong dir="ltr">{row.provider ? `${row.provider} · ${row.model}` : row.model}</strong>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>
      )}
      <div className="two-column">
        <Card>
          <CardHeader>
            <CardTitle>{text.issues}</CardTitle>
          </CardHeader>
          <CardContent>
            <Breakdown values={run.counts.by_category || {}} label={categoryLabel} empty={text.noData} />
          </CardContent>
        </Card>
        <Card>
          <CardHeader>
            <CardTitle>{text.reasons}</CardTitle>
          </CardHeader>
          <CardContent>
            <Breakdown values={run.counts.escalation_reasons || {}} label={reasonLabel} empty={text.noData} />
          </CardContent>
        </Card>
      </div>
      <section className="run-flows">
        {resultsError && <p className="error-text">{resultsError}</p>}
        {results?.map((result) => (
          <div key={result.id}>
            <Link to={`/tickets/${result.id}`} className="run-flow-ticket">
              {result.ticket.external_id}
            </Link>
            <TicketFlow result={result} layout="horizontal" />
          </div>
        ))}
        {!results?.length && !resultsLoading && (
          <p className="muted small">{run.status === "running" ? text.stepsPending : text.noTickets}</p>
        )}
      </section>
    </>
  )
}

function Breakdown({ values, label, empty }: {
  values: Record<string, number>
  label: (value: string) => string
  empty: string
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
    <p className="muted small">{empty}</p>
  )
}
