import type { TicketCalls, UsageGroup, UsageSummary, UsageTicketPage } from "@/lib/types"

const group = (patch: Partial<UsageGroup>): UsageGroup => ({
  key: "x", calls: 1, cost_usd: 0, cost_share: 0, cost_per_call: 0, latency_p50_ms: 100,
  latency_p95_ms: 200, error_rate: 0, input_tokens: 100, output_tokens: 10, cost_sources: { provider: 1 },
  ...patch,
})

export const summaryFixture: UsageSummary = {
  period: { from: "2026-11-07T09:00:00Z", to: "2026-11-14T09:00:00Z" },
  totals: {
    cost_usd: 0.0144, calls: 7, errors: 1, error_rate: 1 / 7, unknown_cost_calls: 1, tickets: 3,
    cost_per_ticket_avg: 0.17, cost_per_ticket_p95: 0.47, ai_time_p50_ms: 2000, ai_time_p95_ms: 5600,
    draft_time_p50_ms: 1500, draft_time_p95_ms: 1500,
  },
  by_process: [
    group({ key: "draft", process: "draft", cost_usd: 0.01, cost_share: 0.69, latency_p50_ms: 1200 }),
    group({ key: "intake", process: "intake", cost_usd: 0.004, cost_share: 0.28 }),
    group({ key: "classify", process: "classify", calls: 2, cost_usd: 0.0002, cost_share: 0.01,
            cost_sources: { estimate: 2 } }),
    group({ key: "extract", process: "extract", cost_usd: 0, cost_share: 0, error_rate: 1,
            latency_p95_ms: 4000, cost_sources: { local: 1 } }),
  ],
  by_model: [
    group({ key: "openrouter:anthropic/claude-sonnet-5.5", provider: "openrouter",
            model: "anthropic/claude-sonnet-5.5", locality: "cloud", processes: ["draft"], cost_usd: 0.01 }),
    group({ key: "ollama:qwen3:4b", provider: "ollama", model: "qwen3:4b", locality: "local",
            processes: ["extract"], cost_sources: { local: 1 } }),
    group({ key: "typesafe:jev-1.13.0", provider: "typesafe", model: "jev-1.13.0", locality: "cloud",
            processes: ["classify"], calls: 2, cost_usd: 0.0002, cost_sources: { estimate: 2 } }),
  ],
  daily: [
    { date: "2026-11-13", cost_usd: 0.004, calls: 3, errors: 0, latency_p95_ms: 900 },
    { date: "2026-11-14", cost_usd: 0.0104, calls: 4, errors: 1, latency_p95_ms: 4000 },
  ],
  unattributed: {
    cost_usd: 0.0002, calls: 2,
    by_process: [group({ key: "kb_index", process: "kb_index", cost_usd: 0.0002 }),
                 group({ key: "probe", process: "probe", cost_sources: { unknown: 1 } })],
  },
}

export const emptySummary: UsageSummary = {
  period: summaryFixture.period,
  totals: { cost_usd: 0, calls: 0, errors: 0, error_rate: null, unknown_cost_calls: 0, tickets: 0,
            cost_per_ticket_avg: null, cost_per_ticket_p95: null, ai_time_p50_ms: null, ai_time_p95_ms: null,
            draft_time_p50_ms: null, draft_time_p95_ms: null },
  by_process: [], by_model: [], daily: [], unattributed: { cost_usd: 0, calls: 0, by_process: [] },
}

export const ticketPage: UsageTicketPage = {
  total: 2,
  items: [
    { result_id: 11, ticket_id: 1, external_id: "INTAKE-ab12", run_id: 4, received_at: "2026-11-14T08:00:00Z",
      processed_at: "2026-11-14T08:00:05Z", status: "pending_review", category: "failed_transfer",
      cost_usd: 0.012, intake_cost_usd: 0.004, total_cost_usd: 0.016,
      cost_by_process: { intake: 0.004, classify: 0.0001, draft: 0.01 }, ai_time_ms: 2000, draft_time_ms: 1500,
      intake_time_ms: 800, calls: 3, errors: 0, detail_recorded: true },
    { result_id: 12, ticket_id: 2, external_id: "T-OLD", run_id: 1, received_at: "2026-11-10T08:00:00Z",
      processed_at: null, status: "escalated", category: "other", cost_usd: 0.5, intake_cost_usd: 0,
      total_cost_usd: 0.5, cost_by_process: {}, ai_time_ms: 1000, draft_time_ms: null, intake_time_ms: 0,
      calls: 0, errors: 0, detail_recorded: false },
  ],
}

export const ticketCalls: TicketCalls = {
  result: ticketPage.items[0],
  calls: [
    { id: 1, process: "intake", provider: "openrouter", model: "google/gemini-3.8-flash", locality: "cloud",
      started_at: "2026-11-14T07:59:00.000Z", latency_ms: 800, input_tokens: 1200, output_tokens: 300,
      cost_usd: 0.004, cost_source: "provider", status: "ok", error: null, attempt: 1, detail: { kind: "analyze" } },
    { id: 2, process: "classify", provider: "typesafe", model: "jev-1.13.0", locality: "cloud",
      started_at: "2026-11-14T08:00:00.000Z", latency_ms: 900, input_tokens: 1000, output_tokens: null,
      cost_usd: 0.0001, cost_source: "estimate", status: "ok", error: null, attempt: 1, detail: { check: "main" } },
    { id: 3, process: "extract", provider: "ollama", model: "qwen3:4b", locality: "local",
      started_at: "2026-11-14T08:00:01.000Z", latency_ms: 1000, input_tokens: null, output_tokens: null,
      cost_usd: 0, cost_source: "local", status: "error", error: "TimeoutError", attempt: 2, detail: {} },
  ],
}
