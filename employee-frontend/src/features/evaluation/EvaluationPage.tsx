import { useEffect, useMemo, useState } from "react"
import { ErrorState, LoadingState, PageHeader } from "@/components/shared/workspace-ui"
import { useResource } from "@/hooks/use-resource"
import { useCopy } from "@/lib/locale"
import type { Run, UsageFilters as Filters, UsageSummary, UsageTicketPage } from "@/lib/types"
import { useWorkspace } from "@/lib/workspace"
import { DailyTrend } from "./DailyTrend"
import { GroupTable } from "./GroupTable"
import { TicketCostTable } from "./TicketCostTable"
import { TicketTimeline } from "./TicketTimeline"
import { UnattributedCard } from "./UnattributedCard"
import { UsageFilters } from "./UsageFilters"
import { UsageHeadline } from "./UsageHeadline"
import { periodRange, usageQuery } from "./usage-view"

const REFRESH_MS = 30_000
const PAGE_SIZE = 25

export function EvaluationPage() {
  const copy = useCopy()
  const workspace = useWorkspace()
  const [filters, setFilters] = useState<Filters>({ period: "7d", process: "all", model: "", runId: "" })
  const [sort, setSort] = useState<"recent" | "cost" | "time">("recent")
  const [offset, setOffset] = useState(0)
  const [open, setOpen] = useState<number | null>(null)
  const [now, setNow] = useState(() => Date.now())

  useEffect(() => {
    const timer = setInterval(() => setNow(Date.now()), REFRESH_MS)
    return () => clearInterval(timer)
  }, [])

  // The range only moves on refresh, so queries stay stable between refreshes.
  const range = useMemo(() => periodRange(filters.period, now), [filters.period, now])
  const query = usageQuery(filters, range)
  const summary = useResource<UsageSummary>(`/ai-usage/summary?${query}`, workspace.revision)
  const tickets = useResource<UsageTicketPage>(
    `/ai-usage/tickets?${usageQuery(filters, range, { sort, limit: PAGE_SIZE, offset })}`, workspace.revision)
  const runs = useResource<Run[]>("/runs", workspace.revision)

  const change = (next: Filters) => {
    setFilters(next)
    setOffset(0)
  }

  return (
    <>
      <PageHeader title={copy.pages.evaluationTitle} description={copy.pages.evaluationDescription} />
      <UsageFilters filters={filters} onChange={change}
                    models={(summary.data?.by_model ?? []).map((g) => g.key)}
                    runs={(runs.data ?? []).slice(0, 50).map((r) => r.id)}
                    onRefresh={() => setNow(Date.now())} />
      {summary.error && <ErrorState message={summary.error} retry={summary.reload} />}
      {!summary.data ? (
        !summary.error && <LoadingState />
      ) : (
        <>
          <UsageHeadline totals={summary.data.totals} />
          <div className="two-column">
            <GroupTable kind="process" groups={summary.data.by_process} />
            <DailyTrend days={summary.data.daily} />
          </div>
          <GroupTable kind="model" groups={summary.data.by_model} ai={workspace.health?.ai} />
        </>
      )}
      {tickets.error && <ErrorState message={tickets.error} retry={tickets.reload} />}
      {tickets.data && (
        <TicketCostTable page={tickets.data} sort={sort}
                         onSort={(value) => { setSort(value); setOffset(0) }}
                         offset={offset} limit={PAGE_SIZE} onPage={setOffset} onOpen={setOpen} />
      )}
      {summary.data && <UnattributedCard data={summary.data.unattributed} />}
      <TicketTimeline resultId={open} onClose={() => setOpen(null)} />
    </>
  )
}
