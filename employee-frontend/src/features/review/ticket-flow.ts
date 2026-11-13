import type { ExtractedField, Result } from "../../lib/types"
import { categoryLabel, percentage } from "../../lib/format"
import { channelName, checkLines, isArabicMessage, lookupSentence, reasonName, sentence, teamName, toolLine } from "./ticket-flow-copy"
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

const TXN_STATUS: Record<string, readonly [string, string]> = {
  pending: ["Pending", "معلّقة"],
  completed: ["Completed", "مكتملة"],
  failed: ["Failed", "فاشلة"],
}

function txnStatus(status: string, arabic: boolean): string {
  const labels = TXN_STATUS[status]
  return labels ? labels[arabic ? 1 : 0] : status
}

const NAMES: Record<FlowStepId, string> = {
  prepare: "Prepare",
  escalate_empty: "Empty ticket",
  jev_classify: "Classification",
  gemini_classify: "Second classification",
  extract: "Extract",
  lookup: "Investigate",
  decide: "Route",
  draft: "Draft",
}

const NAMES_AR: Record<FlowStepId, string> = {
  prepare: "تجهيز",
  escalate_empty: "تذكرة فارغة",
  jev_classify: "تصنيف",
  gemini_classify: "تصنيف ثانٍ",
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

function unusedReason(id: FlowStepId, result: Result, route: Route, arabic: boolean): string {
  if (route === "empty") return sentence("emptyEnded", arabic)
  if (id === "escalate_empty") return sentence("messageHadText", arabic)
  if (id === "jev_classify") return sentence("askedGeminiDirectly", arabic)
  if (route === "straight" && result.escalation_reasons.includes("low_confidence")) {
    return stageNodes(result).includes("gemini_classify")
      ? sentence("geminiUnavailable", arabic)
      : sentence("jevOnlyNoGemini", arabic)
  }
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
    .filter((entry): entry is [string, number] => typeof entry[1] === "number" && Number.isFinite(entry[1]) && entry[1] > 0.005)
    .filter(([id]) => id !== result.category)
    .sort((a, b) => b[1] - a[1])
    .slice(0, 3)
    .map(([id, value]) => sentence("probability", arabic, { category: categoryLabel(id), confidence: percentage(value) }))
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
    return { received: "", produced: received, events: [] }
  }
  if (id === "escalate_empty") {
    return { received: sentence("emptyReceived", arabic), produced: sentence("emptyProduced", arabic), events: message }
  }
  if (id === "jev_classify") {
    const produced = route !== "straight"
      ? sentence("jevUnsure", arabic)
      : result.escalation_reasons.includes("low_confidence")
        ? sentence("jevUnsureEscalated", arabic)
        : sentence("classified", arabic, { category, confidence, priority })
    return { received: "", produced, events: probabilityLines(result, arabic) }
  }
  if (id === "gemini_classify") {
    return {
      received: route === "gemini_direct" || route === "gemini_unknown" ? "" : sentence("geminiAfterJev", arabic),
      produced: sentence("classified", arabic, { category, confidence, priority }),
      events: probabilityLines(result, arabic),
    }
  }
  if (id === "extract") {
    const count = FIELD_KEYS.filter((key) => {
      const value = fieldValue(result.extracted[key], arabic)
      return value != null && value !== sentence("notStated", arabic)
    }).length
    return {
      received: "",
      produced: count ? sentence("extractCount", arabic, { count }) : sentence("nothingExtracted", arabic),
      events: [],
    }
  }
  if (id === "lookup") {
    const reference = result.matched_txn_ref?.trim()
    const status = result.transaction?.status
    const statusLabel = status ? txnStatus(String(status), arabic) : ""
    const outcome = [lookupSentence(result.lookup_status, arabic), reference, statusLabel].filter(Boolean).join(" · ")
    return { received: "", produced: outcome, events: [] }
  }
  if (id === "decide") {
    const reasons = result.escalation_reasons.map((reason) => reasonName(reason, arabic)).join(arabic ? "، " : ", ")
    const produced = result.escalated
      ? sentence("held", arabic, { reasons: reasons || sentence("notRecorded", arabic) })
      : `${sentence("assigned", arabic, { team })} ${sentence("noEscalation", arabic)}`
    return { received: "", produced, events: [] }
  }
  const evidence = reviewEvidence(result)
  const reply = result.draft_text?.trim()
  const passages = evidence.sources.flatMap((source) => {
    const text = excerpt(source.text)
    if (!text) return []
    return [sentence("citationExcerpt", arabic, { filename: source.filename, text })]
  })
  const events = [
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
  if (route === "empty" || id === "escalate_empty") return []
  if (id === "jev_classify" || id === "gemini_classify") {
    return [...verdict(result, arabic, category, confidence, priority), ...probabilityLines(result, arabic)]
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
    const reason = state === "unused" ? unusedReason(id, result, route, arabic) : null
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
