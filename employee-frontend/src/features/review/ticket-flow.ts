import type { ExtractedField, Result } from "../../lib/types"
import { categoryLabel, humanize, percentage } from "../../lib/format"
import { channelName, checkLines, fieldLabel, isArabicMessage, lookupSentence, sentence, toolLine } from "./ticket-flow-copy"
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
    return stageNodes(result).length === 0 ? "gemini_unknown" : "gemini_direct"
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

function story(id: FlowStepId, result: Result, arabic: boolean, route: Route): { received: string; produced: string; events: string[] } {
  const category = result.category ? categoryLabel(result.category) : sentence("noCategory", arabic)
  const confidence = percentage(result.category_confidence)
  const priority = result.priority || sentence("noPriority", arabic)
  const team = result.team || sentence("noTeam", arabic)
  if (id === "prepare") {
    const length = result.ticket.text.trim().length
    const received = length
      ? sentence("prepareReceived", arabic, { channel: channelName(result.ticket.channel, arabic), length: length.toLocaleString("en-US") })
      : sentence("prepareEmpty", arabic)
    return { received, produced: sentence("prepareProduced", arabic), events: [] }
  }
  if (id === "jev_classify") {
    const produced = route === "straight"
      ? sentence("jevSure", arabic, { category, confidence, priority })
      : sentence("jevUnsure", arabic)
    return { received: sentence("cleaned", arabic), produced, events: [] }
  }
  if (id === "gemini_classify") {
    const received = route === "gemini_direct" || route === "gemini_unknown"
      ? sentence("cleaned", arabic)
      : sentence("geminiAfterJev", arabic)
    return { received, produced: sentence("classified", arabic, { category, confidence, priority }), events: [] }
  }
  if (id === "extract") {
    const events = FIELD_KEYS.map((key) => {
      const label = fieldLabel(key, arabic)
      const field = result.extracted[key]
      const value = fieldValue(field, arabic)
      if (value == null) return sentence("fieldMissing", arabic, { label })
      return field?.span
        ? sentence("fieldFrom", arabic, { label, value, span: field.span })
        : sentence("fieldLine", arabic, { label, value })
    })
    return { received: sentence("extractReceived", arabic, { category }), produced: events[events.length - 1], events: events.slice(0, -1) }
  }
  if (id === "lookup") {
    return { received: sentence("lookupReceived", arabic), produced: lookupSentence(result.lookup_status, arabic), events: [] }
  }
  if (id === "decide") {
    const reasons = result.escalation_reasons.map(humanize).join(", ")
    const produced = result.escalated
      ? sentence("held", arabic, { reasons: reasons || sentence("notRecorded", arabic) })
      : `${sentence("assigned", arabic, { team })} ${sentence("noEscalation", arabic)}`
    return { received: sentence("decideReceived", arabic), produced, events: [] }
  }
  const evidence = reviewEvidence(result)
  const events = [
    ...evidence.tools.map((event) => toolLine(event, arabic)),
    ...checkLines(evidence.otherEvents, arabic),
  ]
  const citations = result.citations?.length ?? 0
  const produced = [
    result.draft_text ? sentence("draftSaved", arabic) : sentence("draftMissing", arabic),
    citations === 1 ? sentence("citationOne", arabic) : sentence("citations", arabic, { count: citations }),
  ].join(" ")
  return { received: sentence("draftReceived", arabic, { category, team }), produced, events }
}

export function buildTicketFlow(result: Result): TicketFlow {
  const arabic = isArabicMessage(result.ticket.text)
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
    const received = told?.received ?? sentence(state === "unused" ? "notAsked" : "notRecordedStep", arabic)
    const produced = reason ?? told?.produced ?? sentence("notRecordedStep", arabic)
    const events = told?.events ?? []
    return { id, name: NAMES[id], state, reason, received, produced, events }
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
          item.state = "used"
          item.reason = null
          item.produced = sentence("runStopped", arabic)
        } else if (itemIndex > index) {
          item.state = "unused"
          item.reason = sentence("runStopped", arabic)
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
    .replaceAll("`", "'")
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
    const selected = step.id === selectedId ? ",selected" : ""
    lines.push(`  class ${step.id} ${step.state}${selected}`)
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
