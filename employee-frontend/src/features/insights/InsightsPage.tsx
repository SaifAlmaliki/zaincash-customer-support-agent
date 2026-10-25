import {
  BarChart3,
  CalendarDays,
  CircleAlert,
  Download,
  TrendingUp,
} from "lucide-react"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import {
  EmptyState,
  ErrorState,
  PageHeader,
} from "@/components/shared/workspace-ui"
import { useResource } from "@/hooks/use-resource"
import { useWorkspace } from "@/lib/workspace"
import { useCopy } from "@/lib/locale"
import { categoryLabel, dateLabel, downloadJson, humanize } from "@/lib/format"
import type { Insights } from "@/lib/types"

export function InsightsPage() {
  const copy = useCopy()
  const workspace = useWorkspace()
  const query = useResource<Insights>("/insights", workspace.revision)
  const counts = query.data?.categories || {}
  const categories = Object.entries(counts).sort((a, b) => b[1] - a[1])
  const max = Math.max(...Object.values(counts), 1)
  const weeks = query.data?.weeks || []
  const reasons = query.data?.reasons || {}
  return (
    <>
      <PageHeader
        title={copy.pages.insightsTitle}
        description={copy.pages.insightsDescription}
      >
        <Button
          variant="outline"
          disabled={!query.data}
          onClick={() => downloadJson(query.data, "support-insights.json")}
        >
          <Download size={16} />
          Export report
        </Button>
      </PageHeader>
      {query.error && (
        <ErrorState message={query.error} retry={query.reload} />
      )}
      <div className="insights-hero">
        <div>
          <TrendingUp size={23} />
          <h2>A wider view of the queue</h2>
          <p>
            Issue counts come from the latest result for each ticket. Weekly
            comparisons use complete Monday–Sunday periods in Baghdad time.
          </p>
        </div>
        <div>
          <strong>
            {query.data?.total || 0}
          </strong>
          <span>unique tickets analyzed</span>
        </div>
      </div>
      <div className="two-column">
        <Card>
          <CardHeader>
            <CardTitle className="section-title">
              <BarChart3 size={17} />
              Issues by category
            </CardTitle>
          </CardHeader>
          <CardContent>
            {categories.length ? (
              <div className="insights-bars">
                {categories.map(([category, count]) => (
                  <div key={category}>
                    <span>{categoryLabel(category)}</span>
                    <div>
                      <i style={{ width: `${(count / max) * 100}%` }} />
                    </div>
                    <strong>{count}</strong>
                  </div>
                ))}
              </div>
            ) : (
              <EmptyState
                title="No processed tickets yet"
                description="Run a batch to see which support issues occur most often."
              />
            )}
          </CardContent>
        </Card>
        <Card>
          <CardHeader>
            <CardTitle className="section-title">
              <CalendarDays size={17} />
              Weekly ticket volume
            </CardTitle>
          </CardHeader>
          <CardContent>
            {weeks.some((week) => week.total) ? (
              <div className="weekly-chart">
                {weeks.map((week) => (
                  <div key={week.start}>
                    <strong>{week.total}</strong>
                    <div>
                      <span
                        style={{
                          height: `${Math.max(3, (week.total / Math.max(...weeks.map((w) => w.total), 1)) * 100)}%`,
                        }}
                      />
                    </div>
                    <small>{dateLabel(week.start)}</small>
                  </div>
                ))}
              </div>
            ) : (
              <EmptyState
                title="Waiting for a weekly baseline"
                description="Tickets from completed weeks will appear here. We don’t manufacture trends from an empty period."
              />
            )}
          </CardContent>
        </Card>
      </div>
      <Card className="insights-bottom">
        <CardHeader>
          <CardTitle className="section-title">
            <CircleAlert size={17} />
            Why tickets need a person
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="reason-tiles">
            {Object.entries(reasons).map(([reason, count]) => (
              <div key={reason}>
                <strong>{count}</strong>
                <span>{humanize(reason)}</span>
              </div>
            ))}
          </div>
          {!Object.keys(reasons).length && (
            <p className="muted">No escalation reasons recorded yet.</p>
          )}
          <p className="field-help">
            A repeated issue is a signal for investigation, not proof of a
            common root cause.
          </p>
        </CardContent>
      </Card>
    </>
  )
}
