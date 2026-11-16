import "@fontsource/tajawal/arabic-400.css"
import "@fontsource/tajawal/arabic-500.css"
import { Check, Loader2 } from "lucide-react"
import { Card, CardContent } from "@/components/ui/card"
import { useLocale } from "@/lib/locale"
import type { Result } from "@/lib/types"
import { buildTicketFlow, type FlowStep, type TicketFlow as TicketFlowModel } from "./ticket-flow"

function statusFor(step: FlowStep, result: Result, steps: FlowStep[]) {
  if (result.status === "processing") {
    const used = steps.filter((item) => item.state === "used")
    const current = used.at(-1) ?? steps[0]
    if (current?.id === step.id) return "active" as const
  }
  return step.state === "used" ? ("done" as const) : ("pending" as const)
}

function StepMark({ status }: { status: "done" | "active" | "pending" }) {
  if (status === "active") {
    return (
      <span className="flow-rail-mark" data-status="active">
        <Loader2 size={15} />
      </span>
    )
  }
  if (status === "pending") return <span className="flow-rail-mark" data-status="pending" />
  return (
    <span className="flow-rail-mark" data-status="done">
      <Check size={11} strokeWidth={3} />
    </span>
  )
}

function HorizontalFlow({ result, flow }: { result: Result; flow: TicketFlowModel }) {
  const steps = flow.steps.filter((step) => step.state === "used")
  const progressLabel = flow.arabic ? "قيد التنفيذ" : "In progress"
  return (
    <ol className="flow-rail">
      {steps.map((step, index) => {
        const status = statusFor(step, result, flow.steps)
        const detail = status === "active" ? `${progressLabel} · ${step.produced}` : step.produced
        return (
          <li key={step.id} data-status={status} aria-current={status === "active" ? "step" : undefined}>
            <div className="flow-rail-top">
              <StepMark status={status} />
              <strong className="flow-rail-name">{step.name}</strong>
              {index < steps.length - 1 && <span className="flow-rail-line" aria-hidden="true" />}
            </div>
            <small className="flow-rail-detail" title={detail}>
              {detail}
            </small>
          </li>
        )
      })}
    </ol>
  )
}

export function TicketFlow({ result }: { result: Result }) {
  const { locale } = useLocale()
  const flow = buildTicketFlow(result, locale === "ar")
  const font = flow.arabic ? 'Tajawal, "Plus Jakarta Sans Variable", sans-serif' : undefined
  return (
    <Card size="sm">
      <CardContent className="path-card path-card-row" style={{ fontFamily: font }}>
        <HorizontalFlow result={result} flow={flow} />
      </CardContent>
    </Card>
  )
}
