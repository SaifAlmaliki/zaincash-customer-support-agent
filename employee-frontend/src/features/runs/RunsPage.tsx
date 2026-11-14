import { Link, useNavigate } from "react-router-dom"
import { Layers3, Plus } from "lucide-react"
import { Button } from "@/components/ui/button"
import { Card, CardHeader, CardTitle } from "@/components/ui/card"
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table"
import { EmptyState, ErrorState, LoadingState, PageHeader, StatusBadge } from "@/components/shared/workspace-ui"
import { useResource } from "@/hooks/use-resource"
import { useWorkspace } from "@/lib/workspace"
import { fill, useCopy } from "@/lib/locale"
import { dateLabel, timeLabel } from "@/lib/format"
import type { Run } from "@/lib/types"

export function RunsPage() {
  const copy = useCopy()
  const workspace = useWorkspace(),
    navigate = useNavigate()
  const query = useResource<Run[]>("/runs", workspace.revision, 5000)
  const runs = query.data || []
  return (
    <>
      <PageHeader title={copy.pages.runsTitle} description={copy.pages.runsDescription}>
        <Button size="lg" onClick={() => navigate("/runs/new")}>
          <Plus size={17} />
          {copy.runs.newBatch}
        </Button>
      </PageHeader>
      {query.error && <ErrorState message={query.error} retry={query.reload} />}
      <Card className="data-card">
        <CardHeader>
          <CardTitle className="section-title">
            <Layers3 size={17} />
            {copy.runs.history}
            <span className="muted small">{fill(copy.runs.count, { count: runs.length })}</span>
          </CardTitle>
        </CardHeader>
        {query.loading ? (
          <LoadingState />
        ) : !runs.length ? (
          <EmptyState title={copy.runs.emptyTitle} description={copy.runs.emptyBody}>
            <Button onClick={() => navigate("/runs/new")}>
              <Plus size={16} />
              {copy.runs.createFirst}
            </Button>
          </EmptyState>
        ) : (
          <RunsTable runs={runs} />
        )}
      </Card>
    </>
  )
}

export function RunsTable({ runs }: { runs: Run[] }) {
  const copy = useCopy()
  const navigate = useNavigate()
  return (
    <Table>
      <TableHeader>
        <TableRow>
          <TableHead>{copy.runs.colBatch}</TableHead>
          <TableHead>{copy.runs.colStarted}</TableHead>
          <TableHead>{copy.runs.colClassifier}</TableHead>
          <TableHead>{copy.runs.colTickets}</TableHead>
          <TableHead>{copy.runs.colStatus}</TableHead>
          <TableHead>{copy.runs.colCost}</TableHead>
        </TableRow>
      </TableHeader>
      <TableBody>
        {runs.map((run) => (
          <TableRow
            key={run.id}
            className="clickable-row"
            onClick={(event) => {
              if ((event.target as HTMLElement).closest("a, button")) return
              navigate(`/runs/${run.id}`)
            }}
          >
            <TableCell>
              <Link className="ticket-id" to={`/runs/${run.id}`}>
                {fill(copy.runs.batchName, { id: String(run.id).padStart(3, "0") })}
              </Link>
            </TableCell>
            <TableCell>
              {dateLabel(run.started_at)}
              <small className="block-muted">{timeLabel(run.started_at)}</small>
            </TableCell>
            <TableCell>{run.mode === "cascade" ? copy.runs.classifierCascade : copy.runs.classifierJev}</TableCell>
            <TableCell>
              {run.processed} / {run.total}
            </TableCell>
            <TableCell>
              <StatusBadge status={run.status} />
            </TableCell>
            <TableCell>{`$${run.total_cost_usd.toFixed(4)}`}</TableCell>
          </TableRow>
        ))}
      </TableBody>
    </Table>
  )
}
