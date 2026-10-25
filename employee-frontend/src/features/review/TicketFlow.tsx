import "@fontsource/tajawal/arabic-400.css"
import "@fontsource/tajawal/arabic-500.css"
import { Card, CardContent } from "@/components/ui/card"
import {
  ThoughtChain,
  ThoughtChainContent,
  ThoughtChainItem,
  ThoughtChainStep,
  ThoughtChainTrigger,
} from "@/components/ui/components-ai-thought-chain"
import { useLocale } from "@/lib/locale"
import type { Result } from "@/lib/types"
import { buildTicketFlow, type FlowStep } from "./ticket-flow"

function statusFor(step: FlowStep, result: Result, steps: FlowStep[]) {
  if (result.status === "processing") {
    const used = steps.filter((item) => item.state === "used")
    const current = used.at(-1) ?? steps[0]
    if (current?.id === step.id) return "active" as const
  }
  return step.state === "used" ? ("done" as const) : ("pending" as const)
}

function linesFor(step: FlowStep) {
  return [step.received, ...step.events, step.produced].filter((line) => line.trim())
}

export function TicketFlow({ result }: { result: Result }) {
  const { locale } = useLocale()
  const flow = buildTicketFlow(result, locale === "ar")
  const font = flow.arabic ? 'Tajawal, "Plus Jakarta Sans Variable", sans-serif' : undefined
  return (
    <Card>
      <CardContent className="path-card" style={{ fontFamily: font }}>
        <ThoughtChain key={result.id}>
          {flow.steps.map((step) => {
            const status = statusFor(step, result, flow.steps)
            return (
              <ThoughtChainStep
                key={`${step.id}-${status}`}
                status={status}
                defaultOpen={status !== "pending"}
              >
                <ThoughtChainTrigger progressLabel={flow.arabic ? "قيد التنفيذ" : "In progress"}>
                  {step.name}
                </ThoughtChainTrigger>
                <ThoughtChainContent>
                  {linesFor(step).map((line, index) => (
                    <ThoughtChainItem key={`${step.id}-${index}`}>{line}</ThoughtChainItem>
                  ))}
                </ThoughtChainContent>
              </ThoughtChainStep>
            )
          })}
        </ThoughtChain>
      </CardContent>
    </Card>
  )
}
