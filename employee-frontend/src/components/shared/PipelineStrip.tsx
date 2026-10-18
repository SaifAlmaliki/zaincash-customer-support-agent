import { useState } from "react"
import { ChevronRight, Workflow } from "lucide-react"
import { queueStepStatus, stageOutcomes, stages } from "@/lib/stages"
import type { Result } from "@/lib/types"
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog"

export function PipelineStrip({ results }: { results?: Result[] }) {
  const [selected, setSelected] = useState<(typeof stages)[number] | null>(null)
  const outcome = selected ? stageOutcomes[selected.id] : null
  const statuses = selected
    ? queueStepStatus(selected.id, results || []).filter((row) => row.count > 0)
    : []
  return (
    <section className="pipeline-strip" aria-label="Ticket processing workflow">
      <div className="pipeline-caption">
        <Workflow size={16} />
        <span>One pipeline. Every ticket.</span>
        <span className="pipeline-help">Select a step to see its outcome</span>
      </div>
      <div className="pipeline-steps">
        {stages.map((stage, index) => (
          <div className="pipeline-step-wrap" key={stage.id}>
            <button
              className="pipeline-step"
              onClick={() => setSelected(stage)}
            >
              <span className="step-icon">
                <stage.icon size={18} />
              </span>
              <span>
                <strong>
                  <small>{String(index + 1).padStart(2, "0")}</small>
                  {stage.label}
                </strong>
                <span>{stage.subtitle}</span>
              </span>
            </button>
            {index < stages.length - 1 && (
              <ChevronRight className="step-chevron" size={14} />
            )}
          </div>
        ))}
      </div>
      <Dialog
        open={selected !== null}
        onOpenChange={(open) => {
          if (!open) setSelected(null)
        }}
      >
        <DialogContent className="stage-dialog">
          <DialogHeader>
            <DialogTitle>{selected?.label}</DialogTitle>
            <DialogDescription>{outcome?.summary}</DialogDescription>
          </DialogHeader>
          <div className="stage-outcome">
            <h4>{results ? "This queue" : "What this step decides"}</h4>
            {results && !results.length ? (
              <p>No tickets in this queue yet.</p>
            ) : (
              <ul>
                {(results ? statuses : outcome?.statuses || []).map((row) => (
                  <li key={row.label}>
                    <span>{row.label}</span>
                    {"count" in row && <strong>{row.count}</strong>}
                  </li>
                ))}
              </ul>
            )}
          </div>
        </DialogContent>
      </Dialog>
    </section>
  )
}
