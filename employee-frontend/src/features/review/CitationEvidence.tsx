import { BookOpen } from "lucide-react"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import type { Result } from "@/lib/types"
import { reviewEvidence } from "./review-evidence"
import { fill, useCopy } from "@/lib/locale"

export function CitationEvidence({ result }: { result: Result }) {
  const text = useCopy().citations
  const { sources, missingIds } = reviewEvidence(result)
  return <Card>
    <CardHeader><CardTitle className="section-title"><BookOpen size={17} />{text.title}<Badge variant="outline">{fill(text.retained, { count: sources.length })}</Badge></CardTitle></CardHeader>
    <CardContent>
      <p className="muted small">{text.intro}</p>
      <div className="passage-list">
        {sources.map((source) => <article className="passage" key={source.id}>
          <strong className="passage-filename">{source.filename}</strong>
          <div className="passage-meta"><span>{fill(text.document, { id: source.document_id, passage: source.chunk_index + 1 })}{source.page_start == null ? ` · ${text.noPage}` : ` · ${fill(text.page, { page: source.page_end !== source.page_start ? `${source.page_start}–${source.page_end}` : source.page_start })}`}</span><span>{fill(text.similarity, { score: source.score.toFixed(3) })}</span></div>
          <p className="passage-text" dir="auto">{source.text}</p>
          <code className="passage-id">{source.id}</code>
        </article>)}
      </div>
      {!!missingIds.length && <div className="knowledge-message"><strong>{text.missingTitle}</strong><p>{text.missingBody}</p>{missingIds.map((id) => <code className="passage-id" key={id}>{id}</code>)}</div>}
      {!result.citations.length && <p className="field-help">{text.none}</p>}
      {!!sources.length && <p className="field-help">{text.help}</p>}
    </CardContent>
  </Card>
}
