import type { ExtractedField, Result } from "../../lib/types"
import { categoryLabel, percentage } from "../../lib/format"
import { channelName, checkLines, fieldLabel, isArabicMessage, lookupSentence, reasonName, sentence, teamName, toolLine, transactionLabel } from "./ticket-flow-copy"
import { reviewEvidence } from "./review-evidence"

export const STEP_ORDER = [
  "prepare",
  "escalate_empty",
  "jev_classify",
  "gemini_classify",
  "extract",
  "lookup",
  "decide",
  "draft",
] as const

export type FlowStepId = (typeof STEP_ORDER)[number]
export type FlowStepState = "used" | "unused" | "unrecorded"

export type FlowStep = {
  id: FlowStepId
  name: string
  state: FlowStepState
  reason: string | null
  received: string
  produced: string
  events: string[]
}

export type TicketFlow = {
  arabic: boolean
  selectedId: FlowStepId
  steps: FlowStep[]
}

const NAMES: Record<FlowStepId, string> = {
  prepare: "Prepare",
  escalate_empty: "Empty ticket",
  jev_classify: "Jev",
  gemini_classify: "Gemini",
  extract: "Extract",
  lookup: "Investigate",
  decide: "Route",
  draft: "Draft",
}

const NAMES_AR: Record<FlowStepId, string> = {
  prepare: "تجهيز",
  escalate_empty: "تذكرة فارغة",
  jev_classify: "جيف",
  gemini_classify: "جيميناي",
  extract: "استخراج",
  lookup: "تحقق",
  decide: "توجيه",
  draft: "مسودة",
}

function stepName(id: FlowStepId, arabic: boolean) {
  return arabic ? NAMES_AR[id] : NAMES[id]
}

type Route = "empty" | "straight" | "cascade" | "gemini_direct" | "gemini_unknown" | "unknown"

function isStep(value: string | undefined): value is FlowStepId {
  return STEP_ORDER.includes(value as FlowStepId)
}

function stageNodes(result: Result): FlowStepId[] {
  return reviewEvidence(result).stages.map((event) => event.node).filter(isStep)
}

function routeOf(result: Result): Route {
  const blank = !result.ticket.text.trim()
  if (blank || result.escalation_reasons.includes("empty_ticket")) return "empty"
  if (result.classifier_path === "jev") return "straight"
  if (result.classifier_path === "gemini_fallback" || result.classifier_path === "disagreement") return "cascade"
  if (result.classifier_path === "gemini") {
    const stages = stageNodes(result)
    return stages.includes("gemini_classify") && !stages.includes("jev_classify") ? "gemini_direct" : "gemini_unknown"
  }
  const stages = stageNodes(result)
  if (stages.includes("jev_classify") && stages.includes("gemini_classify")) return "cascade"
  return "unknown"
}

function usedIds(route: Route, stages: FlowStepId[]): FlowStepId[] {
  if (route === "empty") return ["prepare", "escalate_empty"]
  if (route === "cascade") return ["prepare", "jev_classify", "gemini_classify", "extract", "lookup", "decide", "draft"]
  if (route === "gemini_direct" || route === "gemini_unknown") {
    return ["prepare", "gemini_classify", "extract", "lookup", "decide", "draft"]
  }
  if (route === "unknown") return stages
  return ["prepare", "jev_classify", "extract", "lookup", "decide", "draft"]
}

function unusedReason(id: FlowStepId, route: Route, arabic: boolean): string {
  if (route === "empty") return sentence("emptyEnded", arabic)
  if (id === "escalate_empty") return sentence("messageHadText", arabic)
  if (id === "jev_classify") return sentence("askedGeminiDirectly", arabic)
  return sentence("jevWasSure", arabic)
}

function defaultSelected(route: Route): FlowStepId {
  if (route === "empty" || route === "gemini_direct") return "prepare"
  if (route === "cascade") return "jev_classify"
  return "draft"
}

const FIELD_KEYS = ["txn_ref", "amount", "date", "phone"] as const

function fieldValue(field: ExtractedField | undefined, arabic: boolean): string | null {
  if (!field) return null
  if (field.value == null || field.value === "") return sentence("notStated", arabic)
  if (typeof field.value === "number" || field.currency) {
    const amount = Number(field.value)
    const shown = Number.isFinite(amount) ? amount.toLocaleString("en-US") : String(field.value)
    return `${shown} ${field.currency || "IQD"}`
  }
  return String(field.value)
}

function customerMessage(result: Result, arabic: boolean): string[] {
  const text = result.ticket.text.trim()
  if (!text) return []
  return [sentence("messageBody", arabic, { text })]
}

function probabilityLines(result: Result, arabic: boolean): string[] {
  return Object.entries(result.category_probs ?? {})
    .filter((entry): entry is [string, number] => typeof entry[1] === "number" && Number.isFinite(entry[1]))
    .sort((a, b) => b[1] - a[1])
    .slice(0, 4)
    .map(([id, value]) => sentence("probability", arabic, { category: categoryLabel(id), confidence: percentage(value) }))
}

function presentValue(value: string | number): string {
  return typeof value === "number" && Number.isFinite(value) ? value.toLocaleString("en-US") : String(value)
}

function transactionLines(result: Result, arabic: boolean): string[] {
  const rows = Object.entries(result.transaction ?? {}).filter((entry): entry is [string, string | number] => {
    const value = entry[1]
    return value != null && value !== ""
  })
  return rows.map(([key, value]) => sentence("lookupDetail", arabic, { label: transactionLabel(key, arabic), value: presentValue(value) }))
}

function excerpt(text: string): string {
  const flat = text.replace(/\s+/g, " ").trim()
  return flat.length > 180 ? `${flat.slice(0, 177)}…` : flat
}

function verdict(result: Result, arabic: boolean, category: string, confidence: string, priority: string): string[] {
  return result.category ? [sentence("classified", arabic, { category, confidence, priority })] : []
}

function story(id: FlowStepId, result: Result, arabic: boolean, route: Route): { received: string; produced: string; events: string[] } {
  const category = result.category ? categoryLabel(result.category) : sentence("noCategory", arabic)
  const confidence = percentage(result.category_confidence)
  const priority = result.priority || sentence("noPriority", arabic)
  const team = result.team ? teamName(result.team, arabic) : sentence("noTeam", arabic)
  const message = customerMessage(result, arabic)
  if (id === "prepare") {
    const length = result.ticket.text.trim().length
    const received = length
      ? sentence("prepareReceived", arabic, { channel: channelName(result.ticket.channel, arabic), length: length.toLocaleString("en-US") })
      : sentence("prepareEmpty", arabic)
    const phone = result.ticket.customer_phone?.trim()
    return {
      received,
      produced: sentence("prepareProduced", arabic),
      events: [...message, ...(phone ? [sentence("customerPhone", arabic, { phone })] : [])],
    }
  }
  if (id === "escalate_empty") {
    return { received: sentence("emptyReceived", arabic), produced: sentence("emptyProduced", arabic), events: message }
  }
  if (id === "jev_classify") {
    const produced = route === "straight"
      ? sentence("jevSure", arabic, { category, confidence, priority })
      : sentence("jevUnsure", arabic)
    return { received: sentence("cleaned", arabic), produced, events: [...message, ...probabilityLines(result, arabic)] }
  }
  if (id === "gemini_classify") {
    const received = route === "gemini_direct" || route === "gemini_unknown"
      ? sentence("cleaned", arabic)
      : sentence("geminiAfterJev", arabic)
    return { received, produced: sentence("classified", arabic, { category, confidence, priority }), events: [...message, ...probabilityLines(result, arabic)] }
  }
  if (id === "extract") {
    const fields = FIELD_KEYS.map((key) => {
      const label = fieldLabel(key, arabic)
      const field = result.extracted[key]
      const value = fieldValue(field, arabic)
      if (value == null) return sentence("fieldMissing", arabic, { label })
      return field?.span
        ? sentence("fieldFrom", arabic, { label, value, span: field.span })
        : sentence("fieldLine", arabic, { label, value })
    })
    return { received: sentence("extractReceived", arabic, { category }), produced: fields[fields.length - 1], events: [...message, ...fields.slice(0, -1)] }
  }
  if (id === "lookup") {
    const available = FIELD_KEYS.flatMap((key) => {
      const value = fieldValue(result.extracted[key], arabic)
      if (value == null || value === sentence("notStated", arabic)) return []
      return [sentence("lookupDetail", arabic, { label: fieldLabel(key, arabic), value })]
    })
    const reference = result.matched_txn_ref?.trim()
    const alreadyListed = Boolean(result.transaction?.txn_ref)
    const matched = reference && !alreadyListed ? [sentence("lookupDetail", arabic, { label: fieldLabel("txn_ref", arabic), value: reference })] : []
    return { received: sentence("lookupReceived", arabic), produced: lookupSentence(result.lookup_status, arabic), events: [...available, ...transactionLines(result, arabic), ...matched] }
  }
  if (id === "decide") {
    const reasons = result.escalation_reasons.map((reason) => reasonName(reason, arabic)).join(arabic ? "، " : ", ")
    const produced = result.escalated
      ? sentence("held", arabic, { reasons: reasons || sentence("notRecorded", arabic) })
      : `${sentence("assigned", arabic, { team })} ${sentence("noEscalation", arabic)}`
    const note = result.escalation_note?.trim()
    return {
      received: sentence("decideReceived", arabic),
      produced,
      events: [
        sentence("decideContext", arabic, { category, confidence, priority }),
        ...(note ? [sentence("noteLine", arabic, { text: note })] : []),
      ],
    }
  }
  const evidence = reviewEvidence(result)
  const reply = result.draft_text?.trim()
  const passages = evidence.sources.flatMap((source) => {
    const text = excerpt(source.text)
    if (!text) return []
    return [sentence("citationExcerpt", arabic, { filename: source.filename, text })]
  })
  const events = [
    ...message,
    ...evidence.tools.map((event) => toolLine(event, arabic)),
    ...checkLines(evidence.otherEvents, arabic),
    ...(reply ? [sentence("draftBody", arabic, { text: reply })] : []),
    ...passages,
  ]
  const citations = result.citations?.length ?? 0
  const produced = [
    result.draft_text ? sentence("draftSaved", arabic) : sentence("draftMissing", arabic),
    citations === 1 ? sentence("citationOne", arabic) : sentence("citations", arabic, { count: citations }),
  ].join(" ")
  return { received: sentence("draftReceived", arabic, { category, team }), produced, events }
}

function skipEvents(id: FlowStepId, result: Result, arabic: boolean, route: Route, category: string, confidence: string, priority: string): string[] {
  if (route === "empty") return []
  if (id === "escalate_empty") return customerMessage(result, arabic)
  if (id === "jev_classify" || id === "gemini_classify") {
    return [...customerMessage(result, arabic), ...verdict(result, arabic, category, confidence, priority), ...probabilityLines(result, arabic)]
  }
  return []
}

export function buildTicketFlow(result: Result, arabic = isArabicMessage(result.ticket.text)): TicketFlow {
  const route = routeOf(result)
  const used = new Set(usedIds(route, stageNodes(result)))
  let selectedId = defaultSelected(route)
  const steps: FlowStep[] = STEP_ORDER.map((id) => {
    const state: FlowStepState = route === "unknown"
      ? (used.has(id) ? "used" : "unrecorded")
      : route === "gemini_unknown" && id === "jev_classify"
        ? "unrecorded"
        : used.has(id) ? "used" : "unused"
    const reason = state === "unused" ? unusedReason(id, route, arabic) : null
    const told = state === "used" ? story(id, result, arabic, route) : null
    const category = result.category ? categoryLabel(result.category) : sentence("noCategory", arabic)
    const confidence = percentage(result.category_confidence)
    const priority = result.priority || sentence("noPriority", arabic)
    const received = told?.received ?? sentence(state === "unused" ? "notAsked" : "notRecordedStep", arabic)
    const produced = reason ?? told?.produced ?? sentence("notRecordedStep", arabic)
    const events = told?.events ?? (state === "unused" ? skipEvents(id, result, arabic, route, category, confidence, priority) : [])
    return { id, name: stepName(id, arabic), state, reason, received, produced, events }
  })
  if (result.status === "failed") {
    const stages = stageNodes(result)
    if (stages.length === 0) {
      const open = steps.find((item) => item.id === selectedId)
      if (open) open.produced = sentence("runStopped", arabic)
    } else {
      const last = stages[stages.length - 1]
      const index = STEP_ORDER.indexOf(last)
      selectedId = last
      for (const item of steps) {
        const itemIndex = STEP_ORDER.indexOf(item.id)
        if (item.id === last) {
          const wasUsed = item.state === "used"
          item.state = "used"
          item.reason = null
          item.received = wasUsed ? story(item.id, result, arabic, route).received : sentence("notRecordedStep", arabic)
          if (!wasUsed) item.events = []
          item.produced = sentence("runStopped", arabic)
        } else if (itemIndex > index) {
          item.state = "unused"
          item.reason = sentence("runStopped", arabic)
          item.received = sentence("notAsked", arabic)
          item.events = []
          item.produced = sentence("runStopped", arabic)
        }
      }
    }
  }
  return { arabic, selectedId, steps }
}

export function mermaidText(value: string): string {
  return value
    .replace(/[<>]/g, "")
    .replaceAll('"', "'")
    .replaceAll("[", "(")
    .replaceAll("]", ")")
    .replaceAll("{", "(")
    .replaceAll("}", ")")
    .replaceAll("%", "")
    .replaceAll("`", "'")
    .replaceAll("\r", " ")
    .replaceAll("\n", " ")
}

function nodeLabel(step: FlowStep, arabic: boolean): string {
  if (step.state === "used") return step.name
  if (step.state === "unrecorded") return `${step.name} — ${sentence("notRecorded", arabic)}`
  return `${step.name} — ${sentence("notUsed", arabic)} — ${step.reason ?? sentence("notRecorded", arabic)}`
}

export function pipelineChart(flow: TicketFlow, selectedId: FlowStepId): string {
  const byId = new Map(flow.steps.map((step) => [step.id, step]))
  const lines = [
    "flowchart TD",
    "  classDef used fill:#eef7f0,stroke:#3d7a4a,color:#173222",
    "  classDef unused fill:#f7f7f8,stroke:#999999,color:#666666,stroke-dasharray:4 3",
    "  classDef unrecorded fill:#ffffff,stroke:#bbbbbb,color:#666666",
    "  classDef selected stroke-width:3px,stroke:#1d4e89",
  ]
  for (const step of flow.steps) {
    lines.push(`  ${step.id}["${mermaidText(nodeLabel(step, flow.arabic))}"]`)
  }
  const used = flow.steps.filter((step) => step.state === "used").map((step) => step.id)
  for (let index = 0; index < used.length - 1; index += 1) {
    lines.push(`  ${used[index]} --> ${used[index + 1]}`)
  }
  const unused = (id: FlowStepId) => byId.get(id)?.state === "unused"
  if (unused("escalate_empty")) lines.push("  prepare -.-> escalate_empty")
  if (unused("jev_classify")) lines.push("  prepare -.-> jev_classify")
  if (unused("gemini_classify")) {
    lines.push(`  ${byId.get("jev_classify")?.state === "used" ? "jev_classify" : "prepare"} -.-> gemini_classify`)
  }
  for (const step of flow.steps) {
    lines.push(`  class ${step.id} ${step.state}`)
    if (step.id === selectedId) lines.push(`  class ${step.id} selected`)
  }
  return lines.join("\n")
}

export function detailChart(flow: TicketFlow, selectedId: FlowStepId): string {
  const step = flow.steps.find((item) => item.id === selectedId) ?? flow.steps[0]
  const parts = [step.received, ...step.events, step.produced]
  const lines = ["flowchart TD"]
  parts.forEach((part, index) => lines.push(`  n${index}["${mermaidText(part)}"]`))
  for (let index = 0; index < parts.length - 1; index += 1) lines.push(`  n${index} --> n${index + 1}`)
  return lines.join("\n")
}
