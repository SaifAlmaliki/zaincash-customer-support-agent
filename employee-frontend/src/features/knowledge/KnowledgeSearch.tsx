import { useCallback, useEffect, useRef, useState, type FormEvent } from "react"
import { Search, TextSearch, X } from "lucide-react"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Input } from "@/components/ui/input"
import { EmptyState, ErrorState, FilterSelect, LoadingState } from "@/components/shared/workspace-ui"
import { useResource } from "@/hooks/use-resource"
import { api } from "@/lib/api"
import { categories, categoryLabel } from "@/lib/format"
import { fill, getLocale, useCopy } from "@/lib/locale"
import type { ChunkPage, KnowledgeDocument, KnowledgeSearchResult } from "@/lib/types"

function pageLabel(
  text: ReturnType<typeof useCopy>["knowledge"],
  start: number | null,
  end: number | null
) {
  if (start == null) return text.noPage
  if (end != null && end !== start) return fill(text.pageRange, { start, end })
  return fill(text.page, { page: start })
}

function ChunkInspection({ document, onClose }: { document: KnowledgeDocument; onClose: () => void }) {
  const text = useCopy().knowledge
  const [offset, setOffset] = useState(0)
  const loader = useCallback((_path: string, options: RequestInit) => api.documentChunks(document.id, offset, 50, options.signal ?? undefined), [document.id, offset])
  const query = useResource<ChunkPage>(`/knowledge/${document.id}/chunks?offset=${offset}`, 0, 0, loader)
  return <Card>
    <CardHeader>
      <CardTitle className="section-title"><TextSearch size={15} />{text.chunksTitle}</CardTitle>
      <Button variant="ghost" size="icon-sm" aria-label={text.closeChunks} onClick={onClose}><X size={16} /></Button>
    </CardHeader>
    <CardContent>
      <p className="passage-filename">{document.filename}</p>
      {document.status !== "indexed" && <p className="field-help">{text.chunksStale}</p>}
      {query.error ? <ErrorState message={query.error} retry={query.reload} /> : query.loading ? <LoadingState /> : !query.data?.items.length ? <EmptyState title={text.noChunks} description={text.noChunksHint} /> : <>
        <div className="passage-list">
          {query.data.items.map((chunk) => <article className="passage" key={chunk.id}>
            <div className="passage-meta"><strong>{fill(text.passage, { number: chunk.chunk_index + 1 })}</strong><span>{pageLabel(text, chunk.page_start, chunk.page_end)}</span></div>
            <p className="passage-text" dir="auto">{chunk.text}</p>
            <small className="muted">{chunk.embedding_model}{chunk.category_tags.length ? ` · ${chunk.category_tags.map(categoryLabel).join(getLocale() === "ar" ? "، " : ", ")}` : ""}</small>
            <code className="passage-id">{chunk.id}</code>
          </article>)}
        </div>
        <div className="passage-pagination">
          <Button variant="outline" size="sm" disabled={offset === 0} onClick={() => setOffset((value) => Math.max(0, value - 50))}>{text.previous}</Button>
          <span className="muted small">{fill(text.range, { start: offset + 1, end: offset + query.data.items.length, total: query.data.total })}</span>
          <Button variant="outline" size="sm" disabled={offset + query.data.items.length >= query.data.total} onClick={() => setOffset((value) => value + 50)}>{text.next}</Button>
        </div>
      </>}
    </CardContent>
  </Card>
}

export function KnowledgeSearch({ configured, selected, onClose }: {
  configured: boolean; selected: KnowledgeDocument | null; onClose: () => void
}) {
  const text = useCopy().knowledge
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
    if (!configured || active.current || !query.trim() || !Number.isInteger(Number(k)) || Number(k) < 1 || Number(k) > 10) return
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
      if (!controller.signal.aborted) setError(error instanceof Error ? error.message : text.searchFailed)
    } finally {
      if (!controller.signal.aborted) { active.current = null; setBusy(false) }
    }
  }
  return <>
    {selected && <ChunkInspection key={`${selected.id}-${selected.updated_at}`} document={selected} onClose={onClose} />}
    <Card>
      <CardHeader><CardTitle className="section-title"><Search size={15} />{text.searchTitle}</CardTitle></CardHeader>
      <CardContent>
        <p className="muted small">{text.searchIntro}</p>
        <form onSubmit={(event) => void search(event)} className="knowledge-search-form">
          <label className="field-label" htmlFor="policy-query">{text.question}</label>
          <Input id="policy-query" dir="auto" placeholder={text.questionPlaceholder} value={query} onChange={(event) => setQuery(event.target.value)} maxLength={2000} required disabled={busy || !configured} />
          <div className="knowledge-search-controls">
            <div><span className="field-label">{text.category}</span><FilterSelect label={text.categoryLabel} value={category} onChange={setCategory} options={[{ value: "", label: text.allCategories }, ...Object.keys(categories).map((value) => ({ value, label: categoryLabel(value) }))]} /></div>
            <label className="field-label" htmlFor="policy-k">{text.maxPassages}<Input id="policy-k" type="number" min={1} max={10} step={1} required value={k} onChange={(event) => setK(event.target.value)} disabled={busy || !configured} /></label>
            <Button type="submit" disabled={!configured || busy || !query.trim()}><Search size={15} />{busy ? text.searching : text.searchPolicies}</Button>
          </div>
        </form>
        {!configured ? <p className="field-help">{text.searchDisabled}</p> : null}
        {error && <div className="error-state" role="alert">{error} {text.searchFailedHint}</div>}
        {busy && <div role="status" className="loading-state">{text.searchingPassages}</div>}
        {result && <div aria-live="polite">
          <p className="field-help search-result-label">
            {text.resultsFor.split("{query}")[0]}
            <bdi>{searchedFor}</bdi>
            {fill(text.resultsFor.split("{query}")[1] || "", {
              cost: `$${result.cost_usd.toFixed(6)}`,
            })}
          </p>
          {!result.passages.length ? <EmptyState title={text.noResults} description={text.noResultsHint} /> : <div className="passage-list">
            {result.passages.map((passage) => <article className="passage" key={passage.id}>
              <strong className="passage-filename">{passage.filename}</strong>
              <div className="passage-meta"><span>{fill(text.resultMeta, { document: passage.document_id, passage: passage.chunk_index + 1 })}{passage.page_start == null ? "" : ` · ${pageLabel(text, passage.page_start, passage.page_end)}`}</span><span>{fill(text.similarity, { score: passage.score.toFixed(3) })}</span></div>
              <p className="passage-text" dir="auto">{passage.text}</p>
              <code className="passage-id">{passage.id}</code>
            </article>)}
            <p className="field-help">{text.similarityHelp}</p>
          </div>}
        </div>}
      </CardContent>
    </Card>
  </>
}
