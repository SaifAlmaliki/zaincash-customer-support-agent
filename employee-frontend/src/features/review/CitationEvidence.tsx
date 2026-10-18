import { BookOpen } from "lucide-react"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import type { Result } from "@/lib/types"
import { reviewEvidence } from "./review-evidence"

export function CitationEvidence({ result }: { result: Result }) {
  const { sources, missingIds } = reviewEvidence(result)
  return <Card>
    <CardHeader><CardTitle className="section-title"><BookOpen size={17} />Cited policy evidence<Badge variant="outline">{sources.length} retained</Badge></CardTitle></CardHeader>
    <CardContent>
      <p className="muted small">Evidence saved with the original draft. These snapshots remain available if a source is reindexed or deleted; they do not validate later reply edits.</p>
      <div className="passage-list">
        {sources.map((source) => <article className="passage" key={source.id}>
          <strong className="passage-filename">{source.filename}</strong>
          <div className="passage-meta"><span>Document {source.document_id} · Passage {source.chunk_index + 1}{source.page_start == null ? " · No page metadata" : ` · Page ${source.page_start}${source.page_end !== source.page_start ? `–${source.page_end}` : ""}`}</span><span>Similarity {source.score.toFixed(3)}</span></div>
          <p className="passage-text" dir="auto">{source.text}</p>
          <code className="passage-id">{source.id}</code>
        </article>)}
      </div>
      {!!missingIds.length && <div className="knowledge-message"><strong>Missing saved evidence</strong><p>Passage snapshots are unavailable for these citation IDs. This can occur with legacy results; inspect the original source before relying on this draft.</p>{missingIds.map((id) => <code className="passage-id" key={id}>{id}</code>)}</div>}
      {!result.citations.length && <p className="field-help">No cited policy evidence was saved for this result.</p>}
      {!!sources.length && <p className="field-help">Similarity is a retrieval signal, not confidence that a reply is correct.</p>}
    </CardContent>
  </Card>
}
