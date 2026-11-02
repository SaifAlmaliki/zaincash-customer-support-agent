import { Download, FileText, RefreshCw, Search, Trash2 } from "lucide-react"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Input } from "@/components/ui/input"
import { EmptyState, LoadingState, StatusBadge } from "@/components/shared/workspace-ui"
import { fill, getLocale, useCopy } from "@/lib/locale"
import { dateLabel, sizeLabel } from "@/lib/format"
import type { KnowledgeDocument } from "@/lib/types"

export type DocumentListProps = {
  documents: KnowledgeDocument[]
  storedCount: number
  search: string
  loading: boolean
  busy: boolean
  configured: boolean
  selectedId: number | null
  pendingIds: number[]
  canRequestIndex: (document: KnowledgeDocument) => boolean
  onSearchChange: (value: string) => void
  onRefresh: () => void
  onIndex: (document: KnowledgeDocument) => void
  onInspect: (document: KnowledgeDocument) => void
  onDelete: (document: KnowledgeDocument) => void
}

export function DocumentList({
  documents,
  storedCount,
  search,
  loading,
  busy,
  configured,
  selectedId,
  pendingIds,
  canRequestIndex,
  onSearchChange,
  onRefresh,
  onIndex,
  onInspect,
  onDelete,
}: DocumentListProps) {
  const text = useCopy().knowledge
  const statusLabels = useCopy().status as Record<string, string>
  return (
    <Card>
      <CardHeader>
        <CardTitle className="section-title">
          <FileText size={15} />
          {text.documents}
          <span className="muted small">
            {fill(text.shown, { shown: documents.length, stored: storedCount })}
          </span>
        </CardTitle>
        <Button variant="ghost" size="sm" disabled={busy} onClick={onRefresh}>
          <RefreshCw size={14} />
          {text.refresh}
        </Button>
      </CardHeader>
      <CardContent>
        <div className="input-with-icon">
          <Search size={16} />
          <Input
            aria-label={text.searchDocuments}
            placeholder={text.findByName}
            value={search}
            onChange={(event) => onSearchChange(event.target.value)}
          />
        </div>
        {loading ? (
          <LoadingState />
        ) : documents.length ? (
          <div className="document-list">
            {documents.map((doc) => {
              const pending = pendingIds.includes(doc.id)
              const active = pending || doc.status === "indexing"
              const requestable = canRequestIndex(doc)
              const indexAction =
                pending && requestable
                  ? text.requestAgain
                  : active
                    ? text.indexPending
                    : doc.status === "failed"
                      ? text.retryIndex
                      : doc.status === "indexed"
                        ? text.reindex
                        : text.indexDocument
              return (
                <div className="document-item" key={doc.id}>
                  <span className="document-icon">
                    <FileText size={16} />
                  </span>
                  <div className="document-body">
                    <div className="document-heading">
                      <strong>{doc.filename}</strong>
                      <StatusBadge
                        status={pending && doc.status !== "indexing" ? "index_requested" : doc.status}
                      />
                      <span className="muted small">
                        {fill(text.passagesCount, { count: doc.chunk_count })}
                      </span>
                    </div>
                    <small>
                      {sizeLabel(doc.size)} · {fill(text.uploaded, { date: dateLabel(doc.created_at) })}
                    </small>
                    {pending && doc.status !== "indexing" && (
                      <p className="field-help">
                        {fill(text.pendingHelp, {
                          status: statusLabels[doc.status] || doc.status,
                        })}{" "}
                        {requestable && text.pendingRetry}
                      </p>
                    )}
                    {doc.error && (
                      <p className="document-error">
                        {pending ? text.previousAttempt : text.indexingFailed}
                        {doc.error} {!active && text.checkAndRetry}
                      </p>
                    )}
                    {doc.status === "awaiting_indexing" && !pending && (
                      <p className="field-help">
                        {text.awaitingHelp}{" "}
                        {configured ? text.awaitingConfigured : text.awaitingUnconfigured}
                      </p>
                    )}
                    {doc.embedding_model && (
                      <small>
                        {fill(text.dimensions, {
                          model: doc.embedding_model,
                          count: doc.embedding_dimensions ?? "",
                        })}
                        {doc.indexed_at
                          ? ` · ${fill(text.indexedOn, { date: dateLabel(doc.indexed_at) })}`
                          : ""}
                      </small>
                    )}
                    {!!doc.category_tags.length && (
                      <small>
                        {fill(text.categories, {
                          list: doc.category_tags.join(getLocale() === "ar" ? "، " : ", "),
                        })}
                      </small>
                    )}
                  </div>
                  <div className="document-actions">
                    <Button
                      variant="outline"
                      size="sm"
                      disabled={busy || !requestable || !configured}
                      onClick={() => onIndex(doc)}
                      aria-label={`${indexAction}: ${doc.filename}`}
                    >
                      {indexAction}
                    </Button>
                    <Button
                      variant="ghost"
                      size="sm"
                      aria-pressed={selectedId === doc.id}
                      onClick={() => onInspect(doc)}
                    >
                      {text.inspect}
                      <span className="sr-only">: {doc.filename}</span>
                    </Button>
                    <Button
                      variant="ghost"
                      size="icon"
                      nativeButton={false}
                      render={<a href={`/api/knowledge/${doc.id}/download`} />}
                      aria-label={fill(text.download, { name: doc.filename })}
                    >
                      <Download size={16} />
                    </Button>
                    <Button
                      variant="ghost"
                      size="icon"
                      aria-label={fill(text.deleteNamed, { name: doc.filename })}
                      disabled={busy || active}
                      onClick={() => onDelete(doc)}
                    >
                      <Trash2 size={15} />
                    </Button>
                  </div>
                </div>
              )
            })}
          </div>
        ) : (
          <EmptyState
            title={search ? text.noMatch : text.emptyLibrary}
            description={text.emptyHint}
          />
        )}
      </CardContent>
    </Card>
  )
}
