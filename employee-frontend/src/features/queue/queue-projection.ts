import type { Result } from "@/lib/types"

export type QueueTab =
  | "all"
  | "pending_review"
  | "escalated"
  | "processing"
  | "approved"

export type QueueFilters = {
  tab: QueueTab
  team: string
  category: string
  search: string
}

export type QueueProjection = {
  counts: Record<QueueTab, number>
  filtered: Result[]
  visible: Result[]
  distribution: [string, number][]
  currentPage: number
  lastPage: number
}

export function projectQueue(
  rows: Result[],
  filters: QueueFilters,
  requestedPage: number,
  pageSize = 8,
): QueueProjection {
  const counts: Record<QueueTab, number> = {
    all: rows.length,
    pending_review: rows.filter((row) => row.status === "pending_review").length,
    escalated: rows.filter((row) => row.status === "escalated").length,
    approved: rows.filter((row) => ["approved", "edited"].includes(row.status)).length,
    processing: rows.filter((row) => row.status === "processing").length,
  }
  const filtered = rows
    .filter((row) =>
      (filters.tab === "all" ||
        (filters.tab === "approved"
          ? ["approved", "edited"].includes(row.status)
          : row.status === filters.tab)) &&
      (filters.team === "all" || row.team === filters.team) &&
      (filters.category === "all" || row.category === filters.category) &&
      `${row.ticket.text} ${row.ticket.external_id} ${row.ticket.display_name || ""}`
        .toLowerCase()
        .includes(filters.search.toLowerCase()),
    )
    .sort((a, b) => (a.priority || "P9").localeCompare(b.priority || "P9"))
  const lastPage = Math.max(0, Math.ceil(filtered.length / pageSize) - 1)
  const currentPage = Math.min(requestedPage, lastPage)
  const visible = filtered.slice(
    currentPage * pageSize,
    currentPage * pageSize + pageSize,
  )
  const distribution = Object.entries(
    rows.reduce<Record<string, number>>((acc, row) => {
      const key = row.category || "other"
      acc[key] = (acc[key] || 0) + 1
      return acc
    }, {}),
  )
    .sort((a, b) => b[1] - a[1])
    .slice(0, 5)

  return { counts, filtered, visible, distribution, currentPage, lastPage }
}
