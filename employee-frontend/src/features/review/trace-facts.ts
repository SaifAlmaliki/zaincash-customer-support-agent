import { categoryLabel, humanize, percentage } from "@/lib/format"
import { getCopy, getLocale } from "@/lib/locale"
import { buildTicketFlow } from "./ticket-flow"
import { checkLines, reasonName } from "./ticket-flow-copy"
import type { ExtractedField, Result, TraceEvent } from "@/lib/types"

const FIELD_LABELS: Record<string, string> = {
  txn_ref: "Transaction reference",
  amount: "Amount",
  date: "Date",
  phone: "Phone number",
}

const LOOKUP: Record<string, string> = {
  matched: "One transaction matched.",
  amount_mismatch: "A transaction was found, but the amount in the message does not match the record.",
  date_mismatch: "A transaction was found, but the date does not match the record.",
  not_found: "No transaction matched the details in the message.",
  ambiguous: "Several transactions matched, so none was selected.",
  not_applicable: "This issue does not need a transaction lookup.",
}

const TOOLS: Record<string, string> = {
  lookup_transaction: "Looked up a transaction reference",
  search_transactions: "Searched transactions",
  get_customer_recent_transactions: "Listed recent transactions",
  get_customer_ticket_history: "Checked earlier tickets for this customer",
  check_service_status: "Checked whether a service was disrupted",
  search_knowledge_base: "Searched the knowledge base",
  flag_for_human: "Flagged the ticket for a person",
  submit_draft: "Submitted a draft reply",
}

function text(value: unknown) {
  return typeof value === "string" && value.trim() ? value.trim() : null
}

function record(value: unknown): Record<string, unknown> | null {
  return value !== null && typeof value === "object" && !Array.isArray(value)
    ? (value as Record<string, unknown>)
    : null
}

function fieldValue(field: ExtractedField | undefined) {
  if (!field || field.value == null || field.value === "") return "Not stated"
  if (typeof field.value === "number" || field.currency) {
    const amount = Number(field.value)
    const shown = Number.isFinite(amount) ? amount.toLocaleString("en-US") : String(field.value)
    return `${shown} ${field.currency || "IQD"}`
  }
  return String(field.value)
}

function quoted(field: ExtractedField | undefined) {
  return field?.span ? ` from “${field.span}”` : ""
}

function classifySentence(result: Partial<Result>) {
  if (result.classifier_path === "gemini_fallback")
    return "Jev was unsure, so Gemini gave a second opinion."
  if (result.classifier_path === "gemini") return "Gemini classified this ticket."
  if (result.classifier_path === "jev") return "Jev classified this ticket. Gemini was not asked."
  return result.category ? "A category was recorded." : "No classification was recorded."
}

const FLOW_STAGES: Record<string, string[]> = {
  prepare: ["prepare"],
  classify: ["jev_classify", "gemini_classify"],
  extract: ["extract"],
  lookup: ["lookup"],
  decide: ["escalate_empty", "decide"],
  draft: ["draft"],
}

export function stageFacts(stageId: string, result: Partial<Result>): string[] {
  if (getLocale() === "ar" && result.ticket && typeof result.ticket.text === "string") {
    const flow = buildTicketFlow(result as Result, true)
    const lines = (FLOW_STAGES[stageId] ?? []).flatMap((id) => {
      const step = flow.steps.find((item) => item.id === id && item.state === "used")
      if (!step) return []
      return [step.received, ...step.events, step.produced].filter(Boolean)
    })
    if (lines.length) return lines
  }
  const extracted = result.extracted ?? {}
  const ticket = result.ticket
  if (stageId === "prepare") {
    const channels: Record<string, string> = {
      app: "ZainCash app",
      whatsapp: "WhatsApp",
      call_note: "call note",
    }
    const channel = ticket?.channel ? channels[ticket.channel] || humanize(ticket.channel) : "support"
    const length = ticket?.text?.trim().length
    return [
      length
        ? `Read the ${channel} message (${length.toLocaleString("en-US")} characters).`
        : "No customer message was recorded for this step.",
      "Arabic digits were converted to 0–9, and card numbers were hidden before the message was read.",
    ]
  }
  if (stageId === "classify") {
    const category = result.category ? categoryLabel(result.category) : "Unclassified"
    const confidence = percentage(result.category_confidence)
    const priority = result.priority || "no priority"
    return [
      classifySentence(result),
      result.category
        ? `${category}, ${confidence} confidence, priority ${priority}.`
        : "Category, confidence and priority were not recorded.",
    ]
  }
  if (stageId === "extract") {
    return Object.entries(FIELD_LABELS).map(([key, label]) => {
      const field = extracted[key]
      return `${label}: ${fieldValue(field)}${quoted(field)}.`
    })
  }
  if (stageId === "lookup") {
    const status = result.lookup_status
    const lines = [status ? LOOKUP[status] || humanize(status) : "Lookup was not recorded."]
    const ref = text(extracted.txn_ref?.value)
    const phone = text(extracted.phone?.value)
    const customer = text(ticket?.customer_phone)
    if (ref) lines.push(`The ledger was opened by reference ${ref}.`)
    else if (customer || phone)
      lines.push(`No reference was given. The search used phone ${customer || phone}.`)
    const txn = result.transaction
    if (txn) {
      const amount = txn.amount_iqd == null ? "an unstated amount" : `${Number(txn.amount_iqd).toLocaleString("en-US")} IQD`
      const txnStatus = text(txn.status) || "unknown status"
      lines.push(`Recorded transfer ${text(txn.txn_ref) || "without a reference"}: ${amount}, ${txnStatus}.`)
    }
    return lines
  }
  if (stageId === "decide") {
    const team = result.team || "no team"
    const reasons = result.escalation_reasons ?? []
    return [
      `Assigned to ${team}.`,
      result.escalated
        ? `Held for a person: ${reasons.map(humanize).join(", ") || "a review reason was not recorded"}.`
        : "No escalation. Ready for review.",
    ]
  }
  const findings = result.guardrail_findings ?? []
  return [
    result.draft_text ? "A reply was saved for a person to review." : "No reply was saved.",
    findings.length
      ? `Safety checks flagged ${findings.map(humanize).join(", ")}.`
      : "No safety-check findings were recorded.",
    `${result.citations?.length ?? 0} policy ${result.citations?.length === 1 ? "passage was" : "passages were"} cited.`,
  ]
}

export function checkFact(event: TraceEvent) {
  return checkLines([event], getLocale() === "ar")[0] ?? null
}

export function toolFact(event: TraceEvent) {
  const labels = getCopy().tools as Record<string, string>
  const name = text(event.tool) || "a lookup"
  const args = record(event.arguments)
  const detail =
    text(args?.query) ||
    text(args?.txn_ref) ||
    text(args?.phone) ||
    text(args?.service) ||
    (text(args?.reason) ? reasonName(text(args?.reason)!, getLocale() === "ar") : null)
  const action = `${labels[name] || TOOLS[name] || humanize(name)}${detail ? `: ${detail}` : ""}`
  if (event.status === "ok") return `${action}. ${getCopy().trace.completed}.`
  if (event.status === "cancelled") return `${action}. ${labels.cancelled}.`
  if (event.status) return `${action}. ${labels.incomplete}.`
  return `${action}.`
}
