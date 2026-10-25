import { Workflow } from "lucide-react"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { stages } from "@/lib/stages"
import { duration } from "@/lib/format"
import { fill, useCopy } from "@/lib/locale"
import type { Result, TraceEvent } from "@/lib/types"
import { reviewEvidence } from "./review-evidence"
import { checkFact, stageFacts, toolFact } from "./trace-facts"

const STAGE_NODES: Record<string, string[]> = {
  prepare: ["prepare"],
  classify: ["jev_classify", "gemini_classify"],
  extract: ["extract"],
  lookup: ["lookup"],
  decide: ["decide", "escalate_empty"],
  draft: ["draft"],
}

function timing(events: TraceEvent[]) {
  const elapsed = events.map((event) => event.elapsed_ms).filter((value): value is number => typeof value === "number")
  if (!elapsed.length) return null
  return duration(Math.max(...elapsed))
}

export function PipelineTrace({ result, embedded = false }: { result: Result; embedded?: boolean }) {
  const copy = useCopy()
  const text = copy.trace
  const { stages: events, tools, otherEvents } = reviewEvidence(result)
  const checks = otherEvents.flatMap((event) => {
    const line = checkFact(event)
    return line ? [line] : []
  })
  const body = (
    <>
        <p className="muted small">
          {text.intro}
        </p>
        <div className="stage-trace">
          {stages.map((stage, index) => {
            const matching = events.filter((event) =>
              (STAGE_NODES[stage.id] ?? [stage.id]).includes(event.node || "")
            )
            const facts = stageFacts(stage.id, result)
            const when = timing(matching)
            return (
              <details key={stage.id}>
                <summary>
                  <span className="trace-number">{index + 1}</span>
                  <strong>{copy.stages[stage.id as keyof typeof copy.stages] || stage.label}</strong>
                  <small>{matching.length ? text.completed : text.notRecorded}</small>
                </summary>
                <div>
                  <ul className="trace-facts">
                    {facts.map((fact, factIndex) => (
                      <li key={factIndex}>{fact}</li>
                    ))}
                  </ul>
                  {when && <p>{fill(text.finished, { time: when })}</p>}
                </div>
              </details>
            )
          })}
        </div>
        <details className="tool-reference">
          <summary>
            <Workflow size={15} />
            {text.lookups}
            <span>{fill(text.recorded, { count: tools.length })}</span>
          </summary>
          {tools.length ? (
            <ul className="trace-facts">
              {tools.map((event, index) => (
                <li key={index}>{toolFact(event)}</li>
              ))}
            </ul>
          ) : (
            <p>{text.noLookup}</p>
          )}
        </details>
        {checks.length > 0 && (
          <details className="tool-reference">
            <summary>
              <Workflow size={15} />
              {text.checks}
              <span>{fill(text.recorded, { count: checks.length })}</span>
            </summary>
            <ul className="trace-facts">
              {checks.map((line, index) => (
                <li key={index}>{line}</li>
              ))}
            </ul>
          </details>
        )}
    </>
  )
  if (embedded) return <div className="flow-trace">{body}</div>
  return (
    <Card>
      <CardHeader>
        <CardTitle className="section-title">
          <Workflow size={17} />
          {text.title}
        </CardTitle>
      </CardHeader>
      <CardContent>{body}</CardContent>
    </Card>
  )
}
