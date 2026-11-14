import { expect, it } from "vitest"
import type { Result } from "@/lib/types"
import { projectQueue, type QueueFilters } from "./queue-projection"

const filters = (patch: Partial<QueueFilters> = {}): QueueFilters => ({
  tab: "all",
  team: "all",
  category: "all",
  search: "",
  ...patch,
})

function row(id: number, patch: Partial<Result> = {}): Result {
  return {
    id,
    ticket_id: id,
    run_id: 1,
    ticket: {
      id,
      external_id: `T-${id}`,
      text: `ticket ${id}`,
      received_at: "2026-10-12T10:00:00Z",
      channel: "app",
      customer_phone: "07701234567",
    },
    category: "failed_transfer",
    category_confidence: 0.8,
    category_probs: {},
    priority: "P2",
    priority_confidence: null,
    flags: {},
    classifier_path: "jev",
    extracted: {},
    lookup_status: "not_applicable",
    matched_txn_ref: null,
    team: "Payments Ops",
    escalated: false,
    escalation_reasons: [],
    escalation_note: null,
    draft_text: null,
    final_text: null,
    citations: [],
    agent_trace: [],
    status: "pending_review",
    error: null,
    latency_ms: 1,
    cost_usd: 0,
    updated_at: "2026-10-12T10:00:00Z",
    ...patch,
  }
}

it("groups approved and edited rows in counts, filters, and distribution", () => {
  const rows = [
    row(1, { status: "approved" }),
    row(2, { status: "edited" }),
    row(3, { status: "escalated", category: "login_access" }),
    row(4, { category: "login_access" }),
    row(5, { status: "processing", category: null }),
  ]
  const all = projectQueue(rows, filters(), 0)
  const approved = projectQueue(rows, filters({ tab: "approved" }), 0)

  expect(all.counts).toEqual({
    all: 5,
    pending_review: 1,
    escalated: 1,
    approved: 2,
    processing: 1,
  })
  expect(approved.filtered.map((item) => item.id)).toEqual([1, 2])
  expect(all.distribution).toEqual([
    ["failed_transfer", 2],
    ["login_access", 2],
    ["other", 1],
  ])
})

it("applies tab, team, category, and case-insensitive search together", () => {
  const first = row(1)
  const rows = [
    {
      ...first,
      ticket: { ...first.ticket, text: "Refund pending", external_id: "ZC-1001" },
    },
    row(2),
    row(3, { team: "Disputes" }),
    row(4, { status: "approved" }),
  ]
  const view = projectQueue(rows, filters({
    tab: "pending_review",
    team: "Payments Ops",
    category: "failed_transfer",
    search: "zc-1001",
  }), 0)
  expect(view.filtered.map((item) => item.id)).toEqual([1])
  expect(view.visible.map((item) => item.id)).toEqual([1])
})

it("finds a customer's tickets by phone in any accepted format", () => {
  const mine = row(1)
  const rows = [
    { ...mine, ticket: { ...mine.ticket, customer_phone: "07809876543" } },
    row(2),
  ]
  for (const search of ["07809876543", "+964 780 987 6543", "0780987"]) {
    expect(projectQueue(rows, filters({ search }), 0).filtered.map((item) => item.id)).toEqual([1])
  }
})

it("filters unclassified tickets together with the other category", () => {
  const rows = [
    row(1, { category: null }),
    row(2, { category: "other" }),
    row(3, { category: "fraud_report" }),
  ]
  const view = projectQueue(rows, filters({ category: "other" }), 0)
  expect(view.filtered.map((item) => item.id)).toEqual([1, 2])
})

it("keeps the latest tickets on top without mutating input rows", () => {
  const received = (id: number, received_at: string, priority: string | null) => {
    const item = row(id, { priority })
    return { ...item, ticket: { ...item.ticket, received_at } }
  }
  const rows = [
    received(1, "2026-10-10T10:00:00Z", "P1"),
    received(2, "2026-10-12T10:00:00Z", "P3"),
    received(3, "2026-10-11T08:00:00Z", "P2"),
  ]
  const originalOrder = rows.map((item) => item.id)
  const view = projectQueue(rows, filters(), 0)
  expect(view.filtered.map((item) => item.id)).toEqual([2, 3, 1])
  expect(view.visible.map((item) => item.id)).toEqual([2, 3, 1])
  expect(rows.map((item) => item.id)).toEqual(originalOrder)
})

it("clamps the requested page and returns the final visible slice", () => {
  const rows = Array.from({ length: 12 }, (_, index) => row(index + 1))
  const view = projectQueue(rows, filters(), 99)
  expect(view.lastPage).toBe(1)
  expect(view.currentPage).toBe(1)
  expect(view.visible.map((item) => item.id)).toEqual([9, 10, 11, 12])
})

it("clamps empty and no-match projections to page zero", () => {
  const empty = projectQueue([], filters(), 99)
  const noMatch = projectQueue([row(1)], filters({ search: "missing" }), 99)
  for (const view of [empty, noMatch]) {
    expect(view.lastPage).toBe(0)
    expect(view.currentPage).toBe(0)
    expect(view.filtered).toEqual([])
    expect(view.visible).toEqual([])
  }
})
