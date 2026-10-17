import { useCallback, useEffect, useRef, useState, type FormEvent } from "react"
import { Search, TextSearch, X } from "lucide-react"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Input } from "@/components/ui/input"
import { EmptyState, ErrorState, FilterSelect, LoadingState } from "@/components/shared/workspace-ui"
import { useResource } from "@/hooks/use-resource"
import { api } from "@/lib/api"
import { categories, categoryLabel } from "@/lib/format"
import type { ChunkPage, KnowledgeDocument, KnowledgeSearchResult } from "@/lib/types"

function ChunkInspection({ document, onClose }: { document: KnowledgeDocument; onClose: () => void }) {
  const [offset, setOffset] = useState(0)
  const loader = useCallback((_path: string, options: RequestInit) => api.documentChunks(document.id, offset, 50, options.signal ?? undefined), [document.id, offset])
  const query = useResource<ChunkPage>(`/knowledge/${document.id}/chunks?offset=${offset}`, 0, 0, loader)
  return <Card>
    <CardHeader>
      <CardTitle className="section-title"><TextSearch size={17} />Stored passages</CardTitle>
      <Button variant="ghost" size="icon-sm" aria-label="Close passage inspection" onClick={onClose}><X size={16} /></Button>
    </CardHeader>
    <CardContent>
      <p className="passage-filename">{document.filename}</p>
      {document.status !== "indexed" && <p className="field-help">These may be passages from an earlier index. New drafts only use successfully published indexes.</p>}
      {query.error ? <ErrorState message={query.error} retry={query.reload} /> : query.loading ? <LoadingState /> : !query.data?.items.length ? <EmptyState title="No stored passages" description="Index this document successfully to inspect its passages." /> : <>
        <div className="passage-list">
          {query.data.items.map((chunk) => <article className="passage" key={chunk.id}>
            <div className="passage-meta"><strong>Passage {chunk.chunk_index + 1}</strong><span>{chunk.page_start == null ? "No page metadata" : `Page ${chunk.page_start}${chunk.page_end !== chunk.page_start ? `–${chunk.page_end}` : ""}`}</span></div>
            <p className="passage-text" dir="auto">{chunk.text}</p>
            <small className="muted">{chunk.embedding_model}{chunk.category_tags.length ? ` · ${chunk.category_tags.map(categoryLabel).join(", ")}` : ""}</small>
            <code className="passage-id">{chunk.id}</code>
          </article>)}
        </div>
        <div className="passage-pagination">
          <Button variant="outline" size="sm" disabled={offset === 0} onClick={() => setOffset((value) => Math.max(0, value - 50))}>Previous passages</Button>
          <span className="muted small">{offset + 1}–{offset + query.data.items.length} of {query.data.total}</span>
          <Button variant="outline" size="sm" disabled={offset + query.data.items.length >= query.data.total} onClick={() => setOffset((value) => value + 50)}>Next passages</Button>
        </div>
      </>}
    </CardContent>
  </Card>
}

export function KnowledgeSearch({ live, configured, selected, onClose }: {
  live: boolean; configured: boolean; selected: KnowledgeDocument | null; onClose: () => void
}) {
  const [query, setQuery] = useState("")
  const [category, setCategory] = useState("")
  const [k, setK] = useState("5")
  const [busy, setBusy] = useState(false)
  const [error, setError] = useState("")
  const [result, setResult] = useState<KnowledgeSearchResult | null>(null)
  const [searchedFor, setSearchedFor] = useState("")
  const active = useRef<AbortController | null>(null)
  useEffect(() => () => active.current?.abort(), [])
  async function search(event: FormEvent) {
    event.preventDefault()
    if (!live || !configured || active.current || !query.trim() || !Number.isInteger(Number(k)) || Number(k) < 1 || Number(k) > 10) return
    const controller = new AbortController()
    active.current = controller
    setBusy(true)
    setError("")
    setResult(null)
    setSearchedFor(query.trim())
    try {
      const response = await api.searchKnowledge(query.trim(), category || null, Number(k), controller.signal)
      if (!controller.signal.aborted) setResult(response)
    } catch (error) {
      if (!controller.signal.aborted) setError(error instanceof Error ? error.message : "Policy search failed. Try again.")
    } finally {
      if (!controller.signal.aborted) { active.current = null; setBusy(false) }
    }
  }
  return <>
    {live && selected && <ChunkInspection key={`${selected.id}-${selected.updated_at}`} document={selected} onClose={onClose} />}
    <Card>
      <CardHeader><CardTitle className="section-title"><Search size={17} />Test policy search</CardTitle></CardHeader>
      <CardContent>
        <p className="muted small">Find passages a drafting agent could use. Each live search uses the configured embedding provider.</p>
        <form onSubmit={(event) => void search(event)} className="knowledge-search-form">
          <label className="field-label" htmlFor="policy-query">Policy question</label>
          <Input id="policy-query" dir="auto" placeholder="Ask about a support policy…" value={query} onChange={(event) => setQuery(event.target.value)} maxLength={2000} required disabled={!live || busy || !configured} />
          <div className="knowledge-search-controls">
            <div><span className="field-label">Category</span><FilterSelect label="Search category" value={category} onChange={setCategory} options={[{ value: "", label: "All categories" }, ...Object.entries(categories).map(([value, label]) => ({ value, label }))]} /></div>
            <label className="field-label" htmlFor="policy-k">Maximum passages<Input id="policy-k" type="number" min={1} max={10} step={1} required value={k} onChange={(event) => setK(event.target.value)} disabled={!live || busy || !configured} /></label>
            <Button type="submit" disabled={!live || !configured || busy || !query.trim()}><Search size={15} />{busy ? "Searching…" : "Search policies"}</Button>
          </div>
        </form>
        {!live || !configured ? <p className="field-help">{!live ? "Policy search is available in the live workspace." : "Enable and configure knowledge indexing to test search."}</p> : null}
        {error && <div className="error-state" role="alert">{error} Review the query or provider configuration, then search again.</div>}
        {busy && <div role="status" className="loading-state">Searching indexed policy passages…</div>}
        {result && <div aria-live="polite">
          <p className="field-help">Results for “<bdi>{searchedFor}</bdi>” · Query cost ${result.cost_usd.toFixed(6)}</p>
          {!result.passages.length ? <EmptyState title="No matching passages" description="Try another question or category, and check that a relevant policy is indexed." /> : <div className="passage-list">
            {result.passages.map((passage) => <article className="passage" key={passage.id}>
              <strong className="passage-filename">{passage.filename}</strong>
              <div className="passage-meta"><span>Document {passage.document_id} · Passage {passage.chunk_index + 1}{passage.page_start == null ? "" : ` · Page ${passage.page_start}${passage.page_end !== passage.page_start ? `–${passage.page_end}` : ""}`}</span><span>Similarity {passage.score.toFixed(3)}</span></div>
              <p className="passage-text" dir="auto">{passage.text}</p>
              <code className="passage-id">{passage.id}</code>
            </article>)}
            <p className="field-help">Similarity measures retrieval relevance, not confidence or correctness.</p>
          </div>}
        </div>}
      </CardContent>
    </Card>
  </>
}
