import type { ReactNode } from "react"
import { FileSearch, Hash, ReceiptText, ShieldAlert, TextSearch } from "lucide-react"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Confidence } from "@/components/shared/workspace-ui"
import { categoryLabel, humanize, percentage } from "@/lib/format"
import type { Result } from "@/lib/types"

function highlightedText(result: Result): ReactNode[] {
  const characters = Array.from(result.ticket.text) // Python source spans count code points, not UTF-16 units.
  const spans = Object.values(result.extracted).filter((field) => field.start !== null && field.end !== null && field.start >= 0 && field.end <= characters.length && field.end > field.start).sort((a, b) => a.start! - b.start!)
  let cursor = 0
  const parts: ReactNode[] = []
  for (const [index, field] of spans.entries()) {
    if (field.start! < cursor) continue
    parts.push(characters.slice(cursor, field.start!).join(""))
    parts.push(<mark key={index} title={`Extracted: ${field.value}`}>{characters.slice(field.start!, field.end!).join("")}</mark>)
    cursor = field.end!
  }
  parts.push(characters.slice(cursor).join(""))
  return parts
}

export function SourceEvidence({ result }: { result: Result }) {
  return <div className="evidence-stack">
    {result.escalated && <div className="escalation-callout"><ShieldAlert size={20} /><div><strong>Needs a closer look</strong><p>{result.escalation_note}</p><div>{result.escalation_reasons.map((reason) => <Badge key={reason} variant="outline">{humanize(reason)}</Badge>)}</div></div></div>}
    {result.error && <div className="error-state" role="alert">{result.error}</div>}
    <Card><CardHeader><CardTitle className="section-title"><ReceiptText size={17} />Original customer message<Badge variant="outline">{humanize(result.ticket.channel)}</Badge></CardTitle></CardHeader><CardContent><div className="source-message" dir="auto" lang="ar">{highlightedText(result)}</div><p className="field-help"><span className="highlight-dot" />Highlighted details are linked to the original text.</p></CardContent></Card>
    <Card><CardHeader><CardTitle className="section-title"><TextSearch size={17} />Extracted details</CardTitle></CardHeader><CardContent><div className="extracted-grid">{[["txn_ref", "Transaction reference"], ["amount", "Amount"], ["date", "Date"], ["phone", "Phone number"]].map(([key, label]) => {
      const field = result.extracted[key]
      return <div className="extracted-field" key={key}><small>{label}</small><strong>{field?.value != null ? `${key === "amount" ? Number(field.value).toLocaleString("en-US") : field.value}${key === "amount" ? ` ${field.currency || "IQD"}` : ""}` : <span className="not-stated">Not stated</span>}</strong>{field?.span && <span dir="auto" lang="ar">“{field.span}”</span>}</div>
    })}</div></CardContent></Card>
    <Card><CardHeader><CardTitle className="section-title"><Hash size={17} />Classification<Confidence value={result.category_confidence} /></CardTitle></CardHeader><CardContent><div className="classification-heading"><strong>{categoryLabel(result.category)}</strong><Badge variant="secondary">{result.classifier_path === "gemini_fallback" ? "Gemini fallback" : humanize(result.classifier_path || "Unavailable")}</Badge></div><div className="probability-list">{Object.entries(result.category_probs).sort((a, b) => b[1] - a[1]).slice(0, 4).map(([category, probability]) => <div key={category}><span>{categoryLabel(category)}</span><div><i style={{ width: `${probability * 100}%` }} /></div><strong>{percentage(probability)}</strong></div>)}</div><p className="field-help">Confidence is a model signal, not a guarantee of correctness.</p></CardContent></Card>
    <Card><CardHeader><CardTitle className="section-title"><FileSearch size={17} />Transaction evidence</CardTitle></CardHeader><CardContent>{result.transaction ? <div className="transaction-evidence">{Object.entries(result.transaction).filter(([, value]) => value !== null).map(([key, value]) => <div key={key}><span>{humanize(key)}</span><strong>{String(value)}</strong></div>)}</div> : <p className="muted">{result.lookup_status === "not_applicable" ? "This issue does not require a transaction lookup." : "No matched transaction is available. Investigate before confirming transaction details."}</p>}</CardContent></Card>
  </div>
}
