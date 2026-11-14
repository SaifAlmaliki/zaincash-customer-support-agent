import { useMemo, useState } from "react"
import { Link, useNavigate, useSearchParams } from "react-router-dom"
import {
  CheckCheck,
  ChevronLeft,
  ChevronRight,
  CircleAlert,
  Download,
  Inbox,
  Plus,
  Search,
  ShieldCheck,
  SlidersHorizontal,
  Smartphone,
  MessageCircle,
  ArrowUpRight,
  X,
} from "lucide-react"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Input } from "@/components/ui/input"
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table"
import {
  Confidence,
  EmptyState,
  ErrorState,
  FilterSelect,
  LoadingState,
  Metric,
  PageHeader,
  PriorityBadge,
  StatusBadge,
} from "@/components/shared/workspace-ui"
import { useResource } from "@/hooks/use-resource"
import { loadQueue } from "@/lib/api"
import { useWorkspace } from "@/lib/workspace"
import {
  categories,
  categoryLabel,
  downloadJson,
  teamLabel,
  teams,
} from "@/lib/format"
import { fill, useCopy } from "@/lib/locale"
import type { Result } from "@/lib/types"
import { projectQueue, type QueueTab } from "./queue-projection"
import { TicketIdentity } from "./TicketIdentity"

const EMPTY_RESULTS: Result[] = []

export function QueuePage() {
  const copy = useCopy()
  const text = copy.queue
  const workspace = useWorkspace(),
    navigate = useNavigate()
  const [params] = useSearchParams()
  const runId = params.get("run")
  const [tab, setTab] = useState<QueueTab>("all"),
    [search, setSearch] = useState("")
  const [team, setTeam] = useState("all"),
    [category, setCategory] = useState("all"),
    [page, setPage] = useState(0)
  const query = useResource<{ items: Result[]; total: number }>(
    `/results?limit=500${runId ? `&run_id=${runId}` : ""}`,
    workspace.revision,
    10000,
    loadQueue
  )
  const rows = query.data?.items || EMPTY_RESULTS
  const { counts, filtered, visible, distribution, currentPage, lastPage } = useMemo(
    () => projectQueue(rows, { tab, team, category, search }, page),
    [rows, tab, team, category, search, page],
  )
  return (
    <>
      <PageHeader
        title={runId ? fill(text.batchTitle, { id: runId }) : text.title}
        description={text.description}
      >
        <Button
          variant="outline"
          size="lg"
          disabled={!rows.length}
          onClick={() =>
            downloadJson(
              rows,
              "support-results.json"
            )
          }
        >
          <Download size={16} />
          {text.export}
        </Button>
        <Button size="lg" onClick={() => navigate("/runs/new")}>
          <Plus size={17} />
          {text.newBatch}
        </Button>
      </PageHeader>
      <div className="metrics-grid">
        {(
          [
            ["all", text.inQueue, counts.all, text.inQueueDetail, <Inbox size={19} />, ""],
            ["pending_review", text.ready, counts.pending_review, text.readyDetail, <CheckCheck size={19} />, "metric-blue"],
            ["escalated", text.closer, counts.escalated, text.closerDetail, <CircleAlert size={19} />, "metric-amber"],
            ["approved", text.approved, counts.approved, text.approvedDetail, <ShieldCheck size={19} />, "metric-green"],
          ] as const
        ).map(([value, label, count, detail, icon, tone]) => (
          <Metric
            key={value}
            label={label}
            value={count}
            detail={detail}
            icon={icon}
            tone={tone}
            pressed={tab === value}
            onClick={() => {
              setTab(tab === value && value !== "all" ? "all" : value)
              setPage(0)
            }}
          />
        ))}
      </div>
      {query.error && (
        <ErrorState message={query.error} retry={query.reload} />
      )}
      <div className="queue-layout">
        <Card className="queue-card">
          <div className="queue-tabs" role="tablist" aria-label={text.tabs}>
            {(
              [
                ["all", text.all],
                ["pending_review", copy.status.pending_review],
                ["escalated", copy.status.escalated],
                ["processing", copy.status.processing],
                ["approved", copy.status.approved],
              ] as const
            ).map(([value, label]) => (
              <button
                key={value}
                role="tab"
                aria-selected={tab === value}
                className={tab === value ? "queue-tab-active" : ""}
                onClick={() => {
                  setTab(value)
                  setPage(0)
                }}
              >
                {label}
                <span>{counts[value]}</span>
              </button>
            ))}
          </div>
          <div className="queue-filters">
            <div className="input-with-icon">
              <Search size={16} />
              <Input
                aria-label={text.search}
                placeholder={text.searchPlaceholder}
                value={search}
                onChange={(e) => {
                  setSearch(e.target.value)
                  setPage(0)
                }}
              />
            </div>
            <FilterSelect
              label={text.filterTeam}
              value={team}
              options={[
                { value: "all", label: text.allTeams },
                ...teams.map((value) => ({ value, label: teamLabel(value) })),
              ]}
              onChange={(value) => {
                setTeam(value)
                setPage(0)
              }}
            />
            <FilterSelect
              label={text.filterCategory}
              value={category}
              options={[
                { value: "all", label: text.allCategories },
                ...Object.keys(categories).map((value) => ({
                  value,
                  label: categoryLabel(value),
                })),
              ]}
              onChange={(value) => {
                setCategory(value)
                setPage(0)
              }}
            />
            {(search || team !== "all" || category !== "all") && (
              <Button
                variant="ghost"
                size="icon"
                aria-label={text.clear}
                onClick={() => {
                  setSearch("")
                  setTeam("all")
                  setCategory("all")
                }}
              >
                <X size={16} />
              </Button>
            )}
          </div>
          {query.loading && !query.data ? (
            <LoadingState />
          ) : visible.length ? (
            <Table className="ticket-table">
              <TableHeader>
                <TableRow>
                  <TableHead>{text.colTicket}</TableHead>
                  <TableHead>{text.colIssue}</TableHead>
                  <TableHead>{text.colPriority}</TableHead>
                  <TableHead>{text.colConfidence}</TableHead>
                  <TableHead>{text.colStatus}</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {visible.map((row, index) => (
                  <TableRow
                    key={row.id}
                    className="ticket-row clickable-row"
                    onClick={(event) => {
                      if ((event.target as HTMLElement).closest("a, button"))
                        return
                      navigate(`/tickets/${row.id}`)
                    }}
                  >
                    <TableCell>
                      <TicketIdentity
                        ticket={row.ticket}
                        index={index}
                        ticketPath={`/tickets/${row.id}`}
                      />
                    </TableCell>
                    <TableCell>
                      <div className="ticket-subject">
                        <strong>{categoryLabel(row.category)}</strong>
                        <p dir="auto" lang="ar">
                          {row.ticket.text}
                        </p>
                        <small>
                          {row.ticket.channel === "whatsapp" ? (
                            <MessageCircle size={11} />
                          ) : (
                            <Smartphone size={11} />
                          )}
                          {teamLabel(row.team)}
                        </small>
                      </div>
                    </TableCell>
                    <TableCell>
                      <PriorityBadge priority={row.priority} />
                    </TableCell>
                    <TableCell>
                      <Confidence value={row.category_confidence} />
                    </TableCell>
                    <TableCell>
                      <StatusBadge status={row.status} />
                    </TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          ) : (
            <EmptyState
              title={rows.length ? text.noMatch : text.emptyTitle}
              description={rows.length ? text.noMatchDetail : text.emptyDetail}
            >
              {!rows.length && (
                <Button onClick={() => navigate("/runs/new")}>
                  <Plus size={16} />
                  {text.add}
                </Button>
              )}
            </EmptyState>
          )}
          <div className="table-footer">
            <span>
              {filtered.length
                ? fill(text.range, {
                    from: currentPage * 8 + 1,
                    to: Math.min((currentPage + 1) * 8, filtered.length),
                    total: filtered.length,
                  })
                : text.none}
            </span>
            <div>
              <span>
                {fill(text.page, { page: currentPage + 1, pages: lastPage + 1 })}
              </span>
              <Button
                variant="outline"
                size="icon-sm"
                disabled={currentPage === 0}
                aria-label={text.previous}
                onClick={() => setPage(currentPage - 1)}
              >
                <ChevronLeft size={15} />
              </Button>
              <Button
                variant="outline"
                size="icon-sm"
                disabled={currentPage >= lastPage}
                aria-label={text.next}
                onClick={() => setPage(currentPage + 1)}
              >
                <ChevronRight size={15} />
              </Button>
            </div>
          </div>
        </Card>
        <aside className="queue-aside">
          <Card>
            <CardHeader>
              <CardTitle className="aside-title">
                <SlidersHorizontal size={16} />
                {text.triage}
              </CardTitle>
            </CardHeader>
            <CardContent>
              <p className="muted small">{text.needs}</p>
              <div className="category-bars">
                {distribution.length ? (
                  distribution.map(([id, count]) => (
                    <button
                      key={id}
                      type="button"
                      className="category-filter"
                      aria-pressed={category === id}
                      style={{ "--share": `${(count / distribution[0][1]) * 100}%` }}
                      onClick={() => {
                        setCategory(category === id ? "all" : id)
                        setPage(0)
                      }}
                    >
                      <i className="category-fill" aria-hidden="true" />
                      <span className="category-filter-name">{categoryLabel(id)}</span>
                      <strong>{count}</strong>
                    </button>
                  ))
                ) : (
                  <p className="muted small">
                    {text.emptyCategories}
                  </p>
                )}
              </div>
              <Link to="/insights" className="text-link">
                {text.insights} <ArrowUpRight size={14} />
              </Link>
            </CardContent>
          </Card>
          <Card className="attention-card">
            <CardHeader>
              <CardTitle className="aside-title">
                <CircleAlert size={17} />{text.attention}
              </CardTitle>
            </CardHeader>
            <CardContent>
              {rows
                .filter((row) => row.status === "escalated")
                .slice(0, 3)
                .map((row) => (
                  <Link
                    className="attention-ticket"
                    to={`/tickets/${row.id}`}
                    key={row.id}
                  >
                    <span dir="ltr">{row.ticket.customer_phone}</span>
                    <strong>{categoryLabel(row.category)}</strong>
                    <small>
                      {row.escalation_reasons.includes("fraud_suspected")
                        ? text.fraud
                        : text.lowConfidence}
                    </small>
                  </Link>
                ))}
              {counts.escalated === 0 && (
                <p className="muted small">{text.noEscalations}</p>
              )}
            </CardContent>
          </Card>
          <div className="human-note">
            <ShieldCheck size={21} />
            <p>
              <strong>{text.humanTitle}</strong> {text.humanBody}
            </p>
          </div>
        </aside>
      </div>
    </>
  )
}
