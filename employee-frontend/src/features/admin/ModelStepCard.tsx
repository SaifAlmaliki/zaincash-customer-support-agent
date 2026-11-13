import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import { dateLabel } from "@/lib/format"
import { fill, useCopy } from "@/lib/locale"
import type { StepModel } from "@/lib/types"

export function ModelStepCard({
  value,
  disabled,
  onChange,
}: {
  value: StepModel
  disabled: boolean
  onChange: () => void
}) {
  const text = useCopy().models
  const source =
    value.source === "admin" && value.updated_at
      ? fill(text.sourceAdmin, { name: value.updated_by ?? "", date: dateLabel(value.updated_at) })
      : text.sourceEnv
  return (
    <li className="model-row">
      <div className="model-row-main">
        <div className="model-row-title">
          <h2>{text.steps[value.step]}</h2>
          <Badge variant={value.locality === "local" ? "secondary" : "outline"}>
            {text.locality[value.locality]}
          </Badge>
        </div>
        <p className="model-row-help" title={text.stepHelp[value.step]}>
          {text.stepHelp[value.step]}
        </p>
      </div>
      <div className="model-current">
        <span className="muted" dir="ltr">{value.provider}</span>
        <strong dir="ltr" title={value.model}>{value.model}</strong>
      </div>
      <div className="model-row-meta">
        <p className={`model-status status-${value.status}`}>
          {text.status[value.status]}
          {value.status_detail ? ` · ${value.status_detail}` : ""}
        </p>
        <p className="muted" title={source}>{source}</p>
      </div>
      <Button variant="outline" size="sm" onClick={onChange} disabled={disabled}>
        {text.change}
      </Button>
    </li>
  )
}
