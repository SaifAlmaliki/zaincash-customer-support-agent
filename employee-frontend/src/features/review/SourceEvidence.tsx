import {
  FileSearch,
  Hash,
  ShieldAlert,
} from "lucide-react"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Confidence } from "@/components/shared/workspace-ui"
import { categoryLabel, dateLabel, humanize, percentage, reasonLabel, timeLabel } from "@/lib/format"
import { useCopy, useLocale } from "@/lib/locale"
import type { Result } from "@/lib/types"
import { CitationEvidence } from "./CitationEvidence"

function ledgerValue(key: string, value: string | number, arabic: boolean): string {
  if ((key === "amount_iqd" || key === "amount") && Number.isFinite(Number(value))) {
    return `${Number(value).toLocaleString("en-US")} IQD`
  }
  if (key === "created_at") {
    const date = new Date(String(value))
    if (!Number.isNaN(date.getTime())) return `${dateLabel(String(value))} ${timeLabel(String(value))}`
  }
  const status = arabic
    ? { pending: "معلّقة", completed: "مكتملة", failed: "فاشلة" }
    : { pending: "Pending", completed: "Completed", failed: "Failed" }
  const type = arabic
    ? { p2p: "تحويل لشخص", bill: "فاتورة" }
    : { p2p: "Person to person", bill: "Bill" }
  if (key === "status") return status[String(value) as keyof typeof status] || String(value)
  if (key === "type") return type[String(value) as keyof typeof type] || String(value)
  return String(value)
}

export function TransactionCard({ result }: { result: Result }) {
  const { locale } = useLocale()
  const text = useCopy().evidence
  const labels = text.txn as Record<string, string>
  return (
    <Card className="compare-card">
      <CardHeader>
        <CardTitle className="section-title">
          <FileSearch size={17} />
          {text.transaction}
        </CardTitle>
      </CardHeader>
      <CardContent>
        {result.transaction ? (
          <dl className="compare-rows">
            {Object.entries(result.transaction)
              .filter(([, value]) => value !== null && value !== "")
              .map(([key, value]) => (
                <div key={key}>
                  <dt>{labels[key] || humanize(key)}</dt>
                  <dd><bdi dir="ltr">{ledgerValue(key, value as string | number, locale === "ar")}</bdi></dd>
                </div>
              ))}
          </dl>
        ) : (
          <p className="muted">
            {result.lookup_status === "not_applicable" ? text.lookupSkipped : text.lookupMissing}
          </p>
        )}
      </CardContent>
    </Card>
  )
}

export function SourceEvidence({ result, omitTransaction = false }: { result: Result, omitTransaction?: boolean }) {
  const copy = useCopy()
  const text = copy.evidence
  return (
    <div className="evidence-stack">
      {result.escalated && (
        <div className="escalation-callout">
          <ShieldAlert size={20} />
          <div>
            <strong>{copy.review.needsCloser}</strong>
            <p>{copy.review.held}</p>
            <div>
              {result.escalation_reasons.map((reason) => (
                <Badge key={reason} variant="outline">
                  {reasonLabel(reason)}
                </Badge>
              ))}
            </div>
          </div>
        </div>
      )}
      {result.error && (
        <div className="error-state" role="alert">
          {result.error}
        </div>
      )}
      <Card>
        <CardHeader>
          <CardTitle className="section-title">
            <Hash size={17} />
            {text.classification}
            <Confidence value={result.category_confidence} />
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="classification-heading">
            <strong>{categoryLabel(result.category)}</strong>
          </div>
          {Object.entries(result.category_probs).some(([category, probability]) => category !== result.category && probability > 0.005) ? (
            <div className="probability-list">
              {Object.entries(result.category_probs)
                .filter((entry): entry is [string, number] => entry[0] !== result.category && entry[1] > 0.005)
                .sort((a, b) => b[1] - a[1])
                .slice(0, 3)
                .map(([category, probability]) => (
                  <div key={category}>
                    <span>{categoryLabel(category)}</span>
                    <div>
                      <i style={{ width: `${probability * 100}%` }} />
                    </div>
                    <strong>{percentage(probability)}</strong>
                  </div>
                ))}
            </div>
          ) : null}
        </CardContent>
      </Card>
      {omitTransaction ? null : <TransactionCard result={result} />}
      <CitationEvidence result={result} />
    </div>
  )
}
