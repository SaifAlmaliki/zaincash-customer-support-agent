import { useState } from "react"
import { ChevronRight, Code2, Workflow } from "lucide-react"
import { stages } from "@/lib/stages"
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog"

export function PipelineStrip() {
  const [selected, setSelected] = useState<(typeof stages)[number] | null>(null)
  return (
    <section className="pipeline-strip" aria-label="Ticket processing workflow">
      <div className="pipeline-caption">
        <Workflow size={16} />
        <span>One pipeline. Every ticket.</span>
        <span className="pipeline-help">Select a step to see its code</span>
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
            <DialogDescription>{selected?.description}</DialogDescription>
          </DialogHeader>
          <div className="source-files">
            <h4>
              <Code2 size={16} />
              Implementation files
            </h4>
            {selected?.files.map((file) => (
              <code key={file}>backend/app/pipeline/{file}</code>
            ))}
          </div>
        </DialogContent>
      </Dialog>
    </section>
  )
}
