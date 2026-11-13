import { Card, CardContent } from "@/components/ui/card"
import { fill, useCopy } from "@/lib/locale"
import type { EmbeddingSwitch } from "@/lib/types"

export function EmbeddingSwitchStatus({ value }: { value: EmbeddingSwitch }) {
  const text = useCopy().models
  const progress = value.total ? Math.round((value.done / value.total) * 100) : 100
  const title = {
    running: text.switchRunning,
    completed: text.switchDone,
    completed_with_errors: text.switchErrors,
    failed: text.switchFailed,
  }[value.status]
  return (
    <Card className="switch-card" size="sm" role="status">
      <CardContent>
        <h2>{title}</h2>
        <p dir="ltr">
          {value.previous.model} → {value.target.model}
        </p>
        <p>{fill(text.switchProgress, { done: value.done, total: value.total })}</p>
        <div
          className="run-progress"
          role="progressbar"
          aria-label={text.switchTitle}
          aria-valuenow={progress}
          aria-valuemin={0}
          aria-valuemax={100}
        >
          <span style={{ width: `${progress}%` }} />
        </div>
        {value.failed_document_ids.length > 0 && (
          <p className="error-text">
            {fill(text.switchFailedDocs, { ids: value.failed_document_ids.join(", ") })}
          </p>
        )}
        {value.error && <p className="error-text">{value.error}</p>}
      </CardContent>
    </Card>
  )
}
