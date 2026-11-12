import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
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
  return (
    <Card className="model-card">
      <CardHeader>
        <CardTitle className="section-title">
          {text.steps[value.step]}
          <Badge variant={value.locality === "local" ? "secondary" : "outline"}>
            {text.locality[value.locality]}
          </Badge>
        </CardTitle>
      </CardHeader>
      <CardContent>
        <p className="field-help">{text.stepHelp[value.step]}</p>
        <div className="model-current">
          <span className="muted small" dir="ltr">{value.provider}</span>
          <strong dir="ltr">{value.model}</strong>
        </div>
        <p className={`model-status status-${value.status}`}>
          {text.status[value.status]}
          {value.status_detail ? ` · ${value.status_detail}` : ""}
        </p>
        <p className="muted small">
          {value.source === "admin" && value.updated_at
            ? fill(text.sourceAdmin, { name: value.updated_by ?? "", date: dateLabel(value.updated_at) })
            : text.sourceEnv}
        </p>
        <Button variant="outline" onClick={onChange} disabled={disabled}>
          {text.change}
        </Button>
      </CardContent>
    </Card>
  )
}
