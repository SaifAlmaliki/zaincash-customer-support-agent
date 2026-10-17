import { Code2, Workflow } from "lucide-react"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { stages, agentTools } from "@/lib/stages"
import { duration } from "@/lib/format"
import type { Result } from "@/lib/types"
import { reviewEvidence } from "./review-evidence"

export function PipelineTrace({ result }: { result: Result }) {
  const events = result.agent_trace.filter((event) => event.kind === "stage")
  const { tools, otherEvents } = reviewEvidence(result)
  return (
    <Card>
      <CardHeader>
        <CardTitle className="section-title">
          <Workflow size={17} />
          Pipeline & tool trace
        </CardTitle>
      </CardHeader>
      <CardContent>
        <p className="muted small">
          Follow a result back to the step that produced it.
        </p>
        <div className="stage-trace">
          {stages.map((stage, index) => {
            const matching = events.filter(
              (event) =>
                event.node === stage.id ||
                (stage.id === "classify" &&
                  ["jev_classify", "gemini_classify"].includes(
                    event.node || ""
                  ))
            )
            return (
              <details key={stage.id}>
                <summary>
                  <span className="trace-number">{index + 1}</span>
                  <strong>{stage.label}</strong>
                  <small>{matching.length ? "Completed" : "Source map"}</small>
                </summary>
                <div>
                  <p>{stage.description}</p>
                  {stage.files.map((file) => (
                    <code key={file}>pipeline/{file}</code>
                  ))}
                  {matching.map((event, i) => (
                    <p key={i}>
                      {event.node} finished at +
                      {duration(event.elapsed_ms || 0)}
                    </p>
                  ))}
                </div>
              </details>
            )
          })}
        </div>
        <details className="tool-reference">
          <summary>
            <Code2 size={15} />
            Agent tools <span>{tools.length} recorded</span>
          </summary>
          {tools.length ? (
            tools.map((event, i) => (
              <pre key={i}>{JSON.stringify(event, null, 2)}</pre>
            ))
          ) : (
            <>
              <p>
                 No agent tool calls were recorded for this result. Available tools
                 are listed below for reference.
              </p>
              {agentTools.map((tool) => (
                <code key={tool}>{tool}</code>
              ))}
            </>
          )}
        </details>
        <details className="tool-reference">
          <summary><Code2 size={15} />Draft & check events <span>{otherEvents.length} recorded</span></summary>
          <p>Model, guardrail, draft and skipped events are not tool calls.</p>
          {otherEvents.map((event, i) => <pre key={i}>{JSON.stringify(event, null, 2)}</pre>)}
        </details>
      </CardContent>
    </Card>
  )
}
