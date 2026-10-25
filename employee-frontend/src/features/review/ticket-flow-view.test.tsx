import { renderToStaticMarkup } from "react-dom/server"
import { expect, it } from "vitest"
import type { Result } from "@/lib/types"
import { TicketFlow } from "./TicketFlow"

function result(patch: Partial<Result> = {}): Result {
  return {
    id: 10,
    ticket_id: 1,
    run_id: 3,
    ticket: {
      id: 1,
      external_id: "T-1",
      text: "التحويل لم يصل",
      received_at: "2026-10-12T10:00:00Z",
      channel: "app",
      customer_phone: null,
    },
    category: "bill_payment",
    category_confidence: 1,
    category_probs: {},
    priority: "P2",
    priority_confidence: null,
    flags: {},
    classifier_path: "jev",
    extracted: {
      amount: { value: 35000, currency: "IQD", span: "35,000 دينار" },
      date: { value: "01-10-2026", span: "يوم الخميس" },
    },
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

it("renders the pipeline as a thought chain with step names and findings", () => {
  const html = renderToStaticMarkup(<TicketFlow result={result()} />)
  expect(html).toContain("تجهيز")
  expect(html).toContain("جيف")
  expect(html).toContain("جيميناي")
  expect(html).toContain("مسودة")
  expect(html).toContain("قُرئت رسالة تطبيق زين كاش")
  expect(html).toContain("لم يُحفظ رد")
  expect(html).not.toContain("ما وجده كل خطوة")
})

it("marks the latest used step as in progress while the run is still processing", () => {
  const html = renderToStaticMarkup(<TicketFlow result={result({ status: "processing" })} />)
  expect(html).toContain("قيد التنفيذ")
})
