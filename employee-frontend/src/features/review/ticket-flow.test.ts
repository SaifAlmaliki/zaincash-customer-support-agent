import { expect, it } from "vitest"
import type { Result } from "../../lib/types"
import { channelName, checkLines, fieldLabel, isArabicMessage, lookupSentence, sentence, toolLine } from "./ticket-flow-copy"
import { buildTicketFlow } from "./ticket-flow"

it("treats Arabic letters as an Arabic message and a blank message as English", () => {
  expect(isArabicMessage("التحويل لم يصل")).toBe(true)
  expect(isArabicMessage("The transfer failed")).toBe(false)
  expect(isArabicMessage("   ")).toBe(false)
})

it("returns the English skip reasons verbatim and the Arabic reasons for the same ids", () => {
  expect(sentence("messageHadText", false)).toBe("The message had text.")
  expect(sentence("askedGeminiDirectly", false)).toBe("This run asked Gemini directly.")
  expect(sentence("jevWasSure", false)).toBe("Jev was already sure.")
  expect(sentence("emptyEnded", false)).toBe("The empty message ended the path.")
  expect(sentence("runStopped", false)).toBe("The run stopped.")
  expect(sentence("chartFailed", false)).toBe("The chart could not be drawn.")
  expect(sentence("messageHadText", true)).toBe("الرسالة تحتوي على نص.")
  expect(sentence("runStopped", true)).toBe("توقف التشغيل.")
})

it("names channels and fields in the selected language", () => {
  expect(channelName("whatsapp", false)).toBe("WhatsApp")
  expect(channelName("whatsapp", true)).toBe("واتساب")
  expect(fieldLabel("txn_ref", false)).toBe("Transaction reference")
  expect(fieldLabel("txn_ref", true)).toBe("الرقم المرجعي")
})

it("fills a sentence template and describes a lookup", () => {
  expect(sentence("prepareReceived", false, { channel: "WhatsApp", length: "180" })).toBe(
    "Read the WhatsApp message (180 characters).",
  )
  expect(lookupSentence("matched", false)).toBe("One transaction matched.")
  expect(lookupSentence("matched", true)).toBe("تطابق تحويل واحد.")
  expect(lookupSentence(null, false)).toBe("Lookup was not recorded.")
})

it("keeps only safe tool details and states credential checks without secrets", () => {
  expect(toolLine({ tool: "lookup_transaction", status: "ok", arguments: { txn_ref: "ZC-1044", pin: "1234" } }, false)).toBe(
    "Looked up a transaction reference: ZC-1044. Completed.",
  )
  expect(toolLine({ tool: "lookup_transaction", status: "ok", arguments: { txn_ref: "ZC-1044", pin: "1234" } }, false)).not.toContain("1234")
  expect(checkLines([{ kind: "guardrail", status: "passed", findings: [], credential_check_degraded: true }], false)).toEqual([
    "The credential check was unavailable.",
  ])
  expect(checkLines([{ kind: "guardrail", status: "passed", findings: [] }], false)).toEqual([
    "The credential check passed.",
    "No safety-check findings were recorded.",
  ])
})

function result(patch: Partial<Result> = {}, ticket: Partial<Result["ticket"]> = {}): Result {
  return {
    id: 10,
    ticket_id: 1,
    run_id: 3,
    ticket: {
      id: 1,
      external_id: "T-1",
      text: "The transfer failed",
      received_at: "2026-10-12T10:00:00Z",
      channel: "whatsapp",
      customer_phone: null,
      ...ticket,
    },
    category: "failed_transfer",
    category_confidence: 0.82,
    category_probs: {},
    priority: "high",
    priority_confidence: null,
    flags: {},
    classifier_path: "jev",
    extracted: {},
    lookup_status: "matched",
    matched_txn_ref: "ZC-1044",
    team: "Payments Ops",
    escalated: false,
    escalation_reasons: [],
    escalation_note: null,
    draft_text: "reply",
    final_text: null,
    citations: [],
    agent_trace: [],
    status: "pending_review",
    error: "PIN 1234 should stay hidden",
    latency_ms: 1,
    cost_usd: 0,
    updated_at: "2026-10-12T10:00:00Z",
    ...patch,
  }
}

function step(flow: ReturnType<typeof buildTicketFlow>, id: string) {
  const found = flow.steps.find((item) => item.id === id)
  if (!found) throw new Error(`missing ${id}`)
  return found
}

it("opens Draft on a straight Jev path and explains the skipped steps", () => {
  const flow = buildTicketFlow(result())
  expect(flow.selectedId).toBe("draft")
  expect(step(flow, "gemini_classify")).toMatchObject({ state: "unused", reason: "Jev was already sure." })
  expect(step(flow, "escalate_empty")).toMatchObject({ state: "unused", reason: "The message had text." })
  expect(step(flow, "jev_classify").state).toBe("used")
})

it("opens Jev when Gemini gave the second opinion", () => {
  expect(buildTicketFlow(result({ classifier_path: "gemini_fallback" })).selectedId).toBe("jev_classify")
  expect(buildTicketFlow(result({ classifier_path: "disagreement" })).selectedId).toBe("jev_classify")
})

it("opens Prepare for an empty message and stops the later steps", () => {
  const flow = buildTicketFlow(result({ classifier_path: "jev", escalation_reasons: [] }, { text: "  " }))
  expect(flow.selectedId).toBe("prepare")
  expect(flow.arabic).toBe(false)
  for (const id of ["jev_classify", "gemini_classify", "extract", "lookup", "decide", "draft"]) {
    expect(step(flow, id)).toMatchObject({ state: "unused", reason: "The empty message ended the path." })
  }
})

it("opens Prepare when Gemini was asked directly", () => {
  const flow = buildTicketFlow(result({
    classifier_path: "gemini",
    agent_trace: [{ kind: "stage", node: "gemini_classify" }],
  }))
  expect(flow.selectedId).toBe("prepare")
  expect(step(flow, "jev_classify")).toMatchObject({ state: "unused", reason: "This run asked Gemini directly." })
})

it("does not invent a Jev skip reason when a Gemini path has no trace", () => {
  const flow = buildTicketFlow(result({ classifier_path: "gemini", agent_trace: [] }))
  expect(flow.selectedId).toBe("draft")
  expect(step(flow, "jev_classify")).toMatchObject({ state: "unrecorded", reason: null })
})

it("lets a Jev path ignore a stray Gemini stage event", () => {
  const flow = buildTicketFlow(result({
    classifier_path: "jev",
    agent_trace: [{ kind: "stage", node: "gemini_classify" }],
  }))
  expect(flow.selectedId).toBe("draft")
  expect(step(flow, "gemini_classify").reason).toBe("Jev was already sure.")
})

it("stops a failed run at its last stage event and hides the raw error", () => {
  const flow = buildTicketFlow(result({
    status: "failed",
    classifier_path: "jev",
    agent_trace: [{ kind: "stage", node: "extract" }],
  }))
  expect(flow.selectedId).toBe("extract")
  expect(step(flow, "extract").produced).toBe("The run stopped.")
  expect(step(flow, "lookup")).toMatchObject({ state: "unused", reason: "The run stopped." })
  expect(step(flow, "draft").state).toBe("unused")
  expect(JSON.stringify(flow)).not.toContain("PIN 1234")
})

it("uses the run-stopped sentence on Draft when a failed Jev path has no stage events", () => {
  const flow = buildTicketFlow(result({ status: "failed", classifier_path: "jev", agent_trace: [] }))
  expect(flow.selectedId).toBe("draft")
  expect(step(flow, "draft").produced).toBe("The run stopped.")
  expect(JSON.stringify(flow)).not.toContain("PIN 1234")
})

it("describes Prepare without pasting the customer message", () => {
  const flow = buildTicketFlow(result({}, { text: "The transfer failed", channel: "whatsapp" }))
  expect(step(flow, "prepare").received).toBe("Read the WhatsApp message (19 characters).")
  expect(step(flow, "prepare").produced).toBe("Arabic digits were converted to 0–9, and card numbers were hidden.")
  expect(step(flow, "prepare").received).not.toContain("The transfer failed")
})

it("says a missing extracted field was not recorded", () => {
  const flow = buildTicketFlow(result({ extracted: {} }))
  expect(step(flow, "extract").events).toContain("Transaction reference: This field was not recorded.")
})

it("uses Arabic received and produced lines when the message is Arabic", () => {
  const flow = buildTicketFlow(result({}, { text: "التحويل لم يصل", channel: "whatsapp" }))
  expect(flow.arabic).toBe(true)
  expect(step(flow, "prepare").received).toContain("واتساب")
  expect(step(flow, "prepare").produced).toBe("حُوّلت الأرقام العربية إلى 0–9، وأُخفيت أرقام البطاقات.")
})

it("omits unsafe tool arguments from the Draft events", () => {
  const flow = buildTicketFlow(result({
    agent_trace: [{ kind: "tool", tool: "search_knowledge_base", status: "ok", arguments: { query: "refund", password: "secret" } }],
  }))
  expect(step(flow, "draft").events.join("\n")).toContain("Searched the knowledge base: refund. Completed.")
  expect(step(flow, "draft").events.join("\n")).not.toContain("secret")
})
