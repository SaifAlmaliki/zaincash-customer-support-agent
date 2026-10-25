import { useState } from "react"
import "@fontsource/tajawal/arabic-400.css"
import "@fontsource/tajawal/arabic-500.css"
import { Card, CardContent } from "@/components/ui/card"
import { useLocale } from "@/lib/locale"
import type { Result } from "@/lib/types"
import { PipelineTrace } from "./PipelineTrace"
import { buildTicketFlow, STEP_ORDER, type FlowStep, type FlowStepId } from "./ticket-flow"
import { sentence } from "./ticket-flow-copy"

const SPINE_ANCHOR: Partial<Record<FlowStepId, FlowStepId>> = {
  escalate_empty: "prepare",
  jev_classify: "prepare",
}

function anchorOf(id: FlowStepId, used: Set<FlowStepId>): FlowStepId {
  if (id === "gemini_classify") return used.has("jev_classify") ? "jev_classify" : "prepare"
  const fixed = SPINE_ANCHOR[id]
  if (fixed) return fixed
  const index = STEP_ORDER.indexOf(id)
  for (let cursor = index - 1; cursor >= 0; cursor -= 1) {
    if (used.has(STEP_ORDER[cursor])) return STEP_ORDER[cursor]
  }
  return "prepare"
}

function notesFor(anchor: FlowStepId, steps: FlowStep[], used: Set<FlowStepId>): FlowStep[][] {
  const groups: FlowStep[][] = []
  for (const step of steps) {
    if (step.state === "used" || anchorOf(step.id, used) !== anchor) continue
    const last = groups[groups.length - 1]
    if (last && last[0].reason === step.reason && last[0].state === step.state) last.push(step)
    else groups.push([step])
  }
  return groups
}

function Story({ step, arabic }: { step: FlowStep; arabic: boolean }) {
  const lines = [step.received, ...step.events, step.produced].filter(Boolean)
  return (
    <div className="path-story" lang={arabic ? "ar" : "en"}>
      {lines.map((line, index) => (
        <p key={`${index}-${line}`}>{line}</p>
      ))}
    </div>
  )
}

export function TicketFlow({ result }: { result: Result }) {
  const { locale } = useLocale()
  const flow = buildTicketFlow(result, locale === "ar")
  const [selectedId, setSelectedId] = useState<FlowStepId>(flow.selectedId)
  const [seenId, setSeenId] = useState(result.id)
  if (result.id !== seenId) {
    setSeenId(result.id)
    setSelectedId(flow.selectedId)
  }
  const used = new Set(flow.steps.filter((step) => step.state === "used").map((step) => step.id))
  const spine = used.size ? flow.steps.filter((step) => step.state === "used") : flow.steps
  const side = flow.steps.filter((step) => !spine.some((item) => item.id === step.id))
  const font = flow.arabic ? 'Tajawal, "Plus Jakarta Sans Variable", sans-serif' : undefined
  return (
    <Card>
      <CardContent className="path-card">
        <ol className="path-spine" style={{ fontFamily: font }}>
          {spine.map((step) => {
            const notes = notesFor(step.id, side, used)
            return (
              <li key={step.id} data-state={step.state} className={step.id === selectedId ? "is-open" : undefined}>
                <button
                  type="button"
                  className="path-step"
                  aria-pressed={step.id === selectedId}
                  onClick={() => setSelectedId(step.id)}
                >
                  <span className="path-mark" aria-hidden="true" />
                  <span className="path-name">{step.name}</span>
                </button>
                {notes.map((group) => {
                  const open = group.some((item) => item.id === selectedId)
                  const shown = group.find((item) => item.id === selectedId) ?? group[0]
                  return (
                    <div key={group.map((item) => item.id).join("-")} className={open ? "path-note is-open" : "path-note"}>
                      <button
                        type="button"
                        className="path-note-button"
                        aria-pressed={open}
                        onClick={() => setSelectedId(shown.id)}
                      >
                        <strong>{group.map((item) => item.name).join(" · ")}</strong>
                        <span>
                          {sentence(group[0].state === "unrecorded" ? "notRecorded" : "notUsed", flow.arabic)}
                          {group[0].reason ? ` — ${group[0].reason}` : ""}
                        </span>
                      </button>
                      {open && <Story step={shown} arabic={flow.arabic} />}
                    </div>
                  )
                })}
                {step.id === selectedId && <Story step={step} arabic={flow.arabic} />}
              </li>
            )
          })}
        </ol>
        <PipelineTrace result={result} embedded />
      </CardContent>
    </Card>
  )
}
