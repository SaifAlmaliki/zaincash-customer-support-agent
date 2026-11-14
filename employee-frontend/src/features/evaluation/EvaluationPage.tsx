import { useEffect, useMemo, useState } from "react"
import { ErrorState, LoadingState, PageHeader } from "@/components/shared/workspace-ui"
import { useLastData } from "@/hooks/use-last-data"
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
import { mergeModels, periodRange, usageQuery } from "./usage-view"

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

  // A refresh moves the range, so `data` is briefly null; keep showing the last result meanwhile.
  const lastSummary = useLastData(summary.data)
  const lastTickets = useLastData(tickets.data)
  const summaryData = summary.error ? null : lastSummary
  const ticketData = tickets.error ? null : lastTickets
  const [seenModels, setSeenModels] = useState<string[]>([])
  const models = mergeModels(seenModels, (lastSummary?.by_model ?? []).map((g) => g.key))
  if (models !== seenModels) setSeenModels(models)

  const change = (next: Filters) => {
    setFilters(next)
    setOffset(0)
  }

  return (
    <>
      <PageHeader title={copy.pages.evaluationTitle} description={copy.pages.evaluationDescription} />
      <UsageFilters filters={filters} onChange={change}
                    models={models}
                    runs={(runs.data ?? []).slice(0, 50).map((r) => r.id)}
                    onRefresh={() => setNow(Date.now())} />
      {summary.error && <ErrorState message={summary.error} retry={summary.reload} />}
      {!summaryData ? (
        !summary.error && <LoadingState />
      ) : (
        <>
          <UsageHeadline totals={summaryData.totals} />
          <GroupTable kind="process" groups={summaryData.by_process} />
          <GroupTable kind="model" groups={summaryData.by_model} ai={workspace.health?.ai} />
          <div className="usage-pair">
            <DailyTrend days={summaryData.daily} />
            <UnattributedCard data={summaryData.unattributed} />
          </div>
        </>
      )}
      {tickets.error && <ErrorState message={tickets.error} retry={tickets.reload} />}
      {ticketData && (
        <TicketCostTable page={ticketData} sort={sort}
                         onSort={(value) => { setSort(value); setOffset(0) }}
                         offset={offset} limit={PAGE_SIZE} onPage={setOffset} onOpen={setOpen} />
      )}
      <TicketTimeline resultId={open} onClose={() => setOpen(null)} />
    </>
  )
}
