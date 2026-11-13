import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { dateLabel } from "@/lib/format"
import { fill, useCopy } from "@/lib/locale"
import type { AuditEntry } from "@/lib/types"

export function AuditList({ items, error }: { items: AuditEntry[]; error: string | null }) {
  const text = useCopy().models
  return (
    <Card className="audit-card" size="sm">
      <CardHeader>
        <CardTitle>{text.auditTitle}</CardTitle>
      </CardHeader>
      <CardContent>
        {error && <p className="error-text">{error}</p>}
        {!error && items.length === 0 && <p className="muted small">{text.auditEmpty}</p>}
        {items.length > 0 && (
          <ul className="audit-list">
            {items.map((item) => (
              <li key={item.id}>
                <strong>{text.steps[item.step]}</strong>
                <span dir="ltr">
                  {item.previous ? `${item.previous.provider}:${item.previous.model}` : "—"} →{" "}
                  {item.current.provider}:{item.current.model}
                </span>
                <span className="muted small">
                  {fill(text.auditBy, { name: item.changed_by, date: dateLabel(item.changed_at) })}
                </span>
              </li>
            ))}
          </ul>
        )}
      </CardContent>
    </Card>
  )
}
