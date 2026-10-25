import { useEffect, useRef, useState } from "react"
import "@fontsource/tajawal/arabic-400.css"
import "@fontsource/tajawal/arabic-500.css"
import { Workflow } from "lucide-react"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import type { Result } from "@/lib/types"
import { buildTicketFlow, detailChart, pipelineChart, type FlowStepId } from "./ticket-flow"
import { sentence } from "./ticket-flow-copy"

export function TicketFlow({ result }: { result: Result }) {
  const flow = buildTicketFlow(result)
  const [selectedId, setSelectedId] = useState<FlowStepId>(flow.selectedId)
  const [seenId, setSeenId] = useState(result.id)
  const [pipelineSvg, setPipelineSvg] = useState("")
  const [detailSvg, setDetailSvg] = useState("")
  const [chartError, setChartError] = useState(false)
  const renderCount = useRef(0)
  if (result.id !== seenId) {
    setSeenId(result.id)
    setSelectedId(flow.selectedId)
  }
  useEffect(() => {
    let cancelled = false
    const current = buildTicketFlow(result)
    renderCount.current += 1
    const suffix = `${result.id}-${renderCount.current}`
    ;(async () => {
      try {
        const mermaid = (await import("mermaid")).default
        const fontFamily = current.arabic
          ? 'Tajawal, "Plus Jakarta Sans Variable", sans-serif'
          : '"Plus Jakarta Sans Variable", sans-serif'
        mermaid.initialize({
          startOnLoad: false,
          securityLevel: "strict",
          htmlLabels: false,
          fontFamily,
        })
        const pipeline = await mermaid.render(`ticket-flow-pipeline-${suffix}`, pipelineChart(current, selectedId))
        const detail = await mermaid.render(`ticket-flow-detail-${suffix}`, detailChart(current, selectedId))
        if (!cancelled) {
          setPipelineSvg(pipeline.svg)
          setDetailSvg(detail.svg)
          setChartError(false)
        }
      } catch {
        if (!cancelled) setChartError(true)
      }
    })()
    return () => {
      cancelled = true
    }
  }, [result, selectedId])
  const font = flow.arabic
    ? 'Tajawal, "Plus Jakarta Sans Variable", sans-serif'
    : '"Plus Jakarta Sans Variable", sans-serif'
  return (
    <Card>
      <CardHeader>
        <CardTitle className="section-title">
          <Workflow size={17} />
          Pipeline flow
        </CardTitle>
      </CardHeader>
      <CardContent>
        <div className="flex flex-wrap gap-2">
          {flow.steps.map((step) => (
            <Button
              key={step.id}
              type="button"
              size="sm"
              variant={step.id === selectedId ? "default" : "outline"}
              aria-pressed={step.id === selectedId}
              onClick={() => setSelectedId(step.id)}
            >
              {step.name}
            </Button>
          ))}
        </div>
        {chartError ? (
          <p className="muted small">{sentence("chartFailed", false)}</p>
        ) : (
          <div style={{ fontFamily: font }}>
            <div dangerouslySetInnerHTML={{ __html: pipelineSvg }} />
            <div dangerouslySetInnerHTML={{ __html: detailSvg }} />
          </div>
        )}
      </CardContent>
    </Card>
  )
}
