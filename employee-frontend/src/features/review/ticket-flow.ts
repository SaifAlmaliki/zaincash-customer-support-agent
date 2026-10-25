import type { Result } from "../../lib/types"
import { isArabicMessage, sentence } from "./ticket-flow-copy"
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
    const received = state === "used" ? sentence("recorded", arabic) : sentence(state === "unused" ? "notAsked" : "notRecordedStep", arabic)
    const produced = reason ?? (state === "used" ? sentence("recorded", arabic) : sentence("notRecordedStep", arabic))
    return { id, name: NAMES[id], state, reason, received, produced, events: [] }
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
