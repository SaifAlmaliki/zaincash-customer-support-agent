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
  teams,
  timeLabel,
} from "@/lib/format"
import type { Result } from "@/lib/types"

const EMPTY_RESULTS: Result[] = []

export function QueuePage() {
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
        title={runId ? `Batch #${runId} · Support queue` : "Support queue"}
        description="Less time sorting. More time helping people."
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
          Export results
        </Button>
        <Button size="lg" onClick={() => navigate("/runs/new")}>
          <Plus size={17} />
          New batch
        </Button>
      </PageHeader>
      <div className="metrics-grid">
        <Metric
          label="Tickets in queue"
          value={counts.all}
          detail="Latest result for each ticket"
          icon={<Inbox size={19} />}
        />
        <Metric
          label="Ready for your review"
          value={counts.pending_review}
          detail="Prepared for a support agent"
          icon={<CheckCheck size={19} />}
          tone="metric-blue"
        />
        <Metric
          label="Need a closer look"
          value={counts.escalated}
          detail="Escalated with a reason"
          icon={<CircleAlert size={19} />}
          tone="metric-amber"
        />
        <Metric
          label="Human-approved"
          value={counts.approved}
          detail="Reviewed, never auto-sent"
          icon={<ShieldCheck size={19} />}
          tone="metric-green"
        />
      </div>
      {query.error && (
        <ErrorState message={query.error} retry={query.reload} />
      )}
      <div className="queue-layout">
        <Card className="queue-card">
          <div className="queue-tabs" role="tablist" aria-label="Queue status">
            {(
              [
                ["all", "All tickets"],
                ["pending_review", "Needs review"],
                ["escalated", "Escalated"],
                ["processing", "Processing"],
                ["approved", "Approved"],
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
                aria-label="Search tickets"
                placeholder="Search ticket ID or message…"
                value={search}
                onChange={(e) => {
                  setSearch(e.target.value)
                  setPage(0)
                }}
              />
            </div>
            <FilterSelect
              label="Filter by team"
              value={team}
              options={[
                { value: "all", label: "All teams" },
                ...teams.map((value) => ({ value, label: value })),
              ]}
              onChange={(value) => {
                setTeam(value)
                setPage(0)
              }}
            />
            <FilterSelect
              label="Filter by category"
              value={category}
              options={[
                { value: "all", label: "All categories" },
                ...Object.entries(categories).map(([value, label]) => ({
                  value,
                  label,
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
                aria-label="Clear filters"
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
                  <TableHead>Ticket / Customer</TableHead>
                  <TableHead>Issue & message</TableHead>
                  <TableHead>Priority</TableHead>
                  <TableHead>Confidence</TableHead>
                  <TableHead>Status</TableHead>
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
                          {row.team || "Unassigned"}
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
              title={
                rows.length
                  ? "No tickets match these filters"
                  : "Your next batch starts here"
              }
              description={
                rows.length
                  ? "Try a different category, team or search term."
                  : "Upload support tickets to classify and route them."
              }
            >
              {!rows.length && (
                <Button onClick={() => navigate("/runs/new")}>
                  <Plus size={16} />
                  Add tickets
                </Button>
              )}
            </EmptyState>
          )}
          <div className="table-footer">
            <span>
              {filtered.length
                ? `${currentPage * 8 + 1}–${Math.min((currentPage + 1) * 8, filtered.length)} of ${filtered.length} tickets`
                : "0 tickets"}
            </span>
            <div>
              <span>
                Page {currentPage + 1} of {lastPage + 1}
              </span>
              <Button
                variant="outline"
                size="icon-sm"
                disabled={currentPage === 0}
                aria-label="Previous page"
                onClick={() => setPage(currentPage - 1)}
              >
                <ChevronLeft size={15} />
              </Button>
              <Button
                variant="outline"
                size="icon-sm"
                disabled={currentPage >= lastPage}
                aria-label="Next page"
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
                Triage overview
              </CardTitle>
            </CardHeader>
            <CardContent>
              <p className="muted small">What people need help with</p>
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
                    Category totals appear after your first batch.
                  </p>
                )}
              </div>
              <Link to="/insights" className="text-link">
                View insights <ArrowUpRight size={14} />
              </Link>
            </CardContent>
          </Card>
          <Card className="attention-card">
            <CardHeader>
              <CardTitle className="aside-title">
                <CircleAlert size={17} />A human touch needed
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
                        ? "Possible fraud · prioritize review"
                        : "Low confidence · confirm the issue"}
                    </small>
                  </Link>
                ))}
              {counts.escalated === 0 && (
                <p className="muted small">No escalations in this queue.</p>
              )}
            </CardContent>
          </Card>
          <div className="human-note">
            <ShieldCheck size={21} />
            <p>
              <strong>Always a person in the loop.</strong> Replies are prepared
              for review. Approval is a human decision.
            </p>
          </div>
        </aside>
      </div>
    </>
  )
}
