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
  dateLabel,
  downloadJson,
  teamLabel,
  teams,
  timeLabel,
} from "@/lib/format"
import { fill, useCopy } from "@/lib/locale"
import type { Result } from "@/lib/types"

const EMPTY_RESULTS: Result[] = []

export function QueuePage() {
  const copy = useCopy()
  const text = copy.queue
  const workspace = useWorkspace(),
    navigate = useNavigate()
  const [params] = useSearchParams()
  const runId = params.get("run")
  const [tab, setTab] = useState("all"),
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
  const counts = {
    all: rows.length,
    pending_review: rows.filter((row) => row.status === "pending_review")
      .length,
    escalated: rows.filter((row) => row.status === "escalated").length,
    approved: rows.filter((row) => ["approved", "edited"].includes(row.status))
      .length,
    processing: rows.filter((row) => row.status === "processing").length,
  }
  const filtered = useMemo(
    () =>
      rows
        .filter(
          (row) =>
            (tab === "all" ||
              (tab === "approved"
                ? ["approved", "edited"].includes(row.status)
                : row.status === tab)) &&
            (team === "all" || row.team === team) &&
            (category === "all" || row.category === category) &&
            `${row.ticket.text} ${row.ticket.external_id} ${row.ticket.display_name || ""}`
              .toLowerCase()
              .includes(search.toLowerCase())
        )
        .sort((a, b) => (a.priority || "P9").localeCompare(b.priority || "P9")),
    [rows, tab, team, category, search]
  )
  const lastPage = Math.max(0, Math.ceil(filtered.length / 8) - 1),
    currentPage = Math.min(page, lastPage)
  const visible = filtered.slice(currentPage * 8, currentPage * 8 + 8)
  const distribution = Object.entries(
    rows.reduce<Record<string, number>>((acc, row) => {
      const key = row.category || "other"
      acc[key] = (acc[key] || 0) + 1
      return acc
    }, {})
  )
    .sort((a, b) => b[1] - a[1])
    .slice(0, 5)
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
        <Metric
          label={text.inQueue}
          value={counts.all}
          detail={text.inQueueDetail}
          icon={<Inbox size={19} />}
        />
        <Metric
          label={text.ready}
          value={counts.pending_review}
          detail={text.readyDetail}
          icon={<CheckCheck size={19} />}
          tone="metric-blue"
        />
        <Metric
          label={text.closer}
          value={counts.escalated}
          detail={text.closerDetail}
          icon={<CircleAlert size={19} />}
          tone="metric-amber"
        />
        <Metric
          label={text.approved}
          value={counts.approved}
          detail={text.approvedDetail}
          icon={<ShieldCheck size={19} />}
          tone="metric-green"
        />
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
                      <div className="ticket-identity">
                        <span className={`ticket-avatar avatar-${index % 4}`}>
                          {row.ticket.display_name ? (
                            row.ticket.display_name.slice(0, 1)
                          ) : (
                            <Smartphone size={17} />
                          )}
                        </span>
                        <div>
                          <Link to={`/tickets/${row.id}`} className="ticket-id">
                            {row.ticket.external_id}
                          </Link>
                          <small>
                            {row.ticket.display_name ||
                              `${dateLabel(row.ticket.received_at)}, ${timeLabel(row.ticket.received_at)}`}
                          </small>
                        </div>
                      </div>
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
                  distribution.map(([id, count], index) => (
                    <div key={id}>
                      <div>
                        <span>{categoryLabel(id)}</span>
                        <strong>{count}</strong>
                      </div>
                      <div className="distribution-track">
                        <i
                          style={{
                            width: `${(count / rows.length) * 100}%`,
                            opacity: 1 - index * 0.12,
                          }}
                        />
                      </div>
                    </div>
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
                    <span>{row.ticket.external_id}</span>
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
