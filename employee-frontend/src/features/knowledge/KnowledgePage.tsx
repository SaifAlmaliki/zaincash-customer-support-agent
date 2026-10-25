import { useEffect, useRef, useState } from "react"
import {
  BookOpen,
  Download,
  FileText,
  FileUp,
  Search,
  Trash2,
  Database,
  ArrowRight,
  Info,
  RefreshCw,
} from "lucide-react"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Input } from "@/components/ui/input"
import {
  ConfirmDialog,
  EmptyState,
  ErrorState,
  LoadingState,
  PageHeader,
  StatusBadge,
} from "@/components/shared/workspace-ui"
import { useWorkspace } from "@/lib/workspace"
import { fill, getLocale, useCopy } from "@/lib/locale"
import { api } from "@/lib/api"
import { dateLabel, sizeLabel } from "@/lib/format"
import type { KnowledgeDocument } from "@/lib/types"
import { useKnowledgeLibrary } from "./use-knowledge-library"
import { KnowledgeSearch } from "./KnowledgeSearch"

export function KnowledgePage() {
  const copy = useCopy()
  const text = copy.knowledge
  const statusLabels = copy.status as Record<string, string>
  const readinessStatus: Record<string, string> = {
    disabled: text.statusDisabled,
    unconfigured: text.statusUnconfigured,
    ready: text.statusReady,
    indexing: text.statusIndexing,
    failed: text.statusFailed,
    empty: text.statusEmpty,
  }
  const workspace = useWorkspace(),
    input = useRef<HTMLInputElement>(null)
  const query = useKnowledgeLibrary(workspace.revision)
  const mutation = useRef<AbortController | null>(null)
  useEffect(() => () => mutation.current?.abort(), [])
  const [search, setSearch] = useState(""),
    [busy, setBusy] = useState(false),
    [remove, setRemove] = useState<KnowledgeDocument | null>(null)
  const [selectedId, setSelectedId] = useState<number | null>(null)
  const [notice, setNotice] = useState("")
  const [actionError, setActionError] = useState("")
  const selected = query.documents.find((doc) => doc.id === selectedId) ?? null
  const configured = workspace.health?.knowledge?.configured ?? workspace.health?.capabilities.rag_indexing ?? false
  const documents = query.documents.filter((doc) =>
    doc.filename.toLowerCase().includes(search.toLowerCase())
  )
  function beginMutation() {
    if (mutation.current) return null
    const controller = new AbortController()
    mutation.current = controller
    setBusy(true)
    setActionError("")
    setNotice("")
    return controller
  }
  function finishMutation(controller: AbortController) {
    if (controller.signal.aborted) return
    mutation.current = null
    setBusy(false)
  }
  async function upload(file?: File) {
    if (!file) return
    const controller = beginMutation()
    if (!controller) return
    try {
      if (!file.size) throw new Error(text.emptyFile)
      if (file.size > 10 * 1024 * 1024) throw new Error(text.tooLarge)
      const document = await api.uploadDocument(file, controller.signal)
      if (controller.signal.aborted) return
      query.accepted(document)
      const name = document.filename
      setNotice(
        document.index_requested
          ? fill(text.noticeAccepted, { name })
          : document.status === "indexed"
            ? fill(text.noticeAlreadyIndexed, { name })
            : document.status === "failed"
              ? fill(text.noticeFailedStored, { name })
              : document.status === "indexing"
                ? fill(text.noticeAlreadyIndexing, { name })
                : configured
                  ? fill(text.noticeNotQueued, { name })
                  : fill(text.noticeStoredOnly, { name })
      )
    } catch (e) {
      if (!controller.signal.aborted)
        setActionError(e instanceof Error ? e.message : text.uploadFailed)
    } finally {
      finishMutation(controller)
      if (input.current) input.current.value = ""
    }
  }
  async function indexDocument(doc: KnowledgeDocument) {
    if (!configured || !query.canRequestIndex(doc)) return
    const rerequest = query.pendingIds.includes(doc.id)
    const controller = beginMutation()
    if (!controller) return
    try {
      const response = await api.indexDocument(doc.id, null, controller.signal)
      if (!controller.signal.aborted) {
        query.accepted(response)
        setNotice(
          response.status === "indexing"
            ? fill(text.indexRunning, { name: doc.filename })
            : fill(rerequest ? text.indexAcceptedAgain : text.indexAccepted, {
                name: doc.filename,
              })
        )
      }
    } catch (e) {
      if (!controller.signal.aborted)
        setActionError(
          `${doc.filename}: ${e instanceof Error ? e.message : text.indexFailed} ${rerequest ? text.indexFailedPending : text.indexFailedKept}`
        )
    } finally { finishMutation(controller) }
  }
  async function deleteDocument() {
    if (!remove) return
    const controller = beginMutation()
    if (!controller) return
    try {
      await api.deleteDocument(remove.id, controller.signal)
      if (controller.signal.aborted) return
      query.deleted(remove.id)
      if (selectedId === remove.id) setSelectedId(null)
      setRemove(null)
      setNotice(text.deleted)
    } catch (e) {
      if (!controller.signal.aborted)
        setActionError(e instanceof Error ? e.message : text.deleteFailed)
    } finally { finishMutation(controller) }
  }
  return (
    <>
      <PageHeader
        title={copy.pages.knowledgeTitle}
        description={copy.pages.knowledgeDescription}
      >
        <Button
          size="lg"
          disabled={busy}
          onClick={() => input.current?.click()}
        >
          <FileUp size={17} />
          {busy ? text.working : text.upload}
        </Button>
      </PageHeader>
      {notice && <p className="knowledge-message" role="status">{notice}</p>}
      {actionError && <div className="error-state" role="alert">{actionError}</div>}
      <div className="knowledge-layout">
        <div className="evidence-stack">
          <Card className="knowledge-upload">
            <CardContent>
              <div
                className="upload-zone compact"
                onDragOver={(e) => e.preventDefault()}
                onDrop={(e) => {
                  e.preventDefault()
                  void upload(e.dataTransfer.files[0])
                }}
              >
                <div className="upload-symbol">
                  <BookOpen size={16} strokeWidth={1.75} />
                </div>
                <div className="upload-copy">
                  <h3>{text.dropTitle}</h3>
                  <p>{text.dropBody}</p>
                </div>
                <Button
                  variant="outline"
                  disabled={busy}
                  onClick={() => input.current?.click()}
                >
                  {text.browse}
                </Button>
                <input
                  ref={input}
                  type="file"
                  className="sr-only"
                  aria-label={text.uploadLabel}
                  disabled={busy}
                  accept=".pdf,.md,.txt"
                  onChange={(e) => void upload(e.target.files?.[0])}
                />
              </div>
            </CardContent>
          </Card>
          {query.error && (
            <ErrorState message={query.error} retry={query.refresh} />
          )}
          {query.paused && (
            <p className="knowledge-message" role="status">
              {text.paused}
            </p>
          )}
          <Card>
            <CardHeader>
              <CardTitle className="section-title">
                <FileText size={15} />
                {text.documents}
                <span className="muted small">
                  {fill(text.shown, {
                    shown: documents.length,
                    stored: query.documents.length,
                  })}
                </span>
              </CardTitle>
              <Button variant="ghost" size="sm" disabled={busy} onClick={query.refresh}>
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
                  onChange={(e) => setSearch(e.target.value)}
                />
              </div>
              {query.loading ? (
                <LoadingState />
              ) : documents.length ? (
                <div className="document-list">
                  {documents.map((doc) => {
                    const pending = query.pendingIds.includes(doc.id)
                    const active = pending || doc.status === "indexing"
                    const requestable = query.canRequestIndex(doc)
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
                            status={
                              pending && doc.status !== "indexing"
                                ? "index_requested"
                                : doc.status
                            }
                          />
                          <span className="muted small">
                            {fill(text.passagesCount, { count: doc.chunk_count })}
                          </span>
                        </div>
                        <small>
                          {sizeLabel(doc.size)} ·{" "}
                          {fill(text.uploaded, { date: dateLabel(doc.created_at) })}
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
                            {configured
                              ? text.awaitingConfigured
                              : text.awaitingUnconfigured}
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
                              list: doc.category_tags.join(
                                getLocale() === "ar" ? "، " : ", "
                              ),
                            })}
                          </small>
                        )}
                      </div>
                      <div className="document-actions">
                        <Button
                          variant="outline"
                          size="sm"
                          disabled={busy || !requestable || !configured}
                          onClick={() => void indexDocument(doc)}
                          aria-label={`${indexAction}: ${doc.filename}`}
                        >
                          {indexAction}
                        </Button>
                        <Button
                          variant="ghost"
                          size="sm"
                          aria-pressed={selectedId === doc.id}
                          onClick={() => setSelectedId(doc.id)}
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
                          onClick={() => setRemove(doc)}
                        >
                          <Trash2 size={15} />
                        </Button>
                      </div>
                    </div>
                  )})}
                </div>
              ) : (
                <EmptyState
                  title={search ? text.noMatch : text.emptyLibrary}
                  description={text.emptyHint}
                />
              )}
            </CardContent>
          </Card>
          <KnowledgeSearch configured={configured} selected={selected} onClose={() => setSelectedId(null)} />
        </div>
        <aside className="evidence-stack">
          <Card>
            <CardHeader>
              <CardTitle className="section-title">
                <Database size={15} />
                {text.lifecycle}
              </CardTitle>
            </CardHeader>
            <CardContent>
              <ol className="document-lifecycle">
                <li>
                  <span>1</span>
                  <div>
                    <strong>{text.stepStore}</strong>
                    <p>{text.stepStoreBody}</p>
                  </div>
                  <BadgeLabel text={text.available} />
                </li>
                <li>
                  <span>2</span>
                  <div>
                    <strong>{text.stepEmbed}</strong>
                    <p>{text.stepEmbedBody}</p>
                  </div>
                  <BadgeLabel text={configured ? text.configured : text.needsSetup} />
                </li>
                <li>
                  <span>3</span>
                  <div>
                    <strong>{text.stepCite}</strong>
                    <p>{text.stepCiteBody}</p>
                  </div>
                  <BadgeLabel
                    text={
                      workspace.health?.knowledge?.ready
                        ? text.ready
                        : text.needsIndex
                    }
                  />
                </li>
              </ol>
            </CardContent>
          </Card>
          <Card className="knowledge-readiness">
            <CardHeader>
              <CardTitle className="section-title">{text.readiness}</CardTitle>
            </CardHeader>
            <CardContent>
              <p className="muted small">
                {workspace.health?.knowledge
                  ? fill(text.searchable, {
                      count: workspace.health.knowledge.indexed_document_count,
                      status:
                        readinessStatus[workspace.health.knowledge.status] ||
                        workspace.health.knowledge.status,
                    })
                  : text.readinessUnavailable}
              </p>
              {workspace.health?.knowledge && (
                <>
                  <p className="field-help">
                    {fill(text.dimensions, {
                      model: workspace.health.knowledge.embedding_model,
                      count: workspace.health.knowledge.embedding_dimensions,
                    })}
                  </p>
                  <p className="field-help">
                    {!workspace.health.knowledge.enabled
                      ? text.retrievalDisabled
                      : !configured
                        ? text.configureProvider
                        : workspace.health.knowledge.ready
                          ? text.passagesReady
                          : text.indexFirst}
                  </p>
                  <p className="field-help">
                    {workspace.health.drafting?.credential_check_configured
                      ? text.credentialOn
                      : text.credentialOff}{" "}
                    {text.readinessScope}
                  </p>
                </>
              )}
            </CardContent>
          </Card>
          <div className="knowledge-note">
            <Info size={16} />
            <div>
              <strong>{text.noteTitle}</strong>
              <p>{text.noteBody}</p>
              <span>
                {text.flowUpload} <ArrowRight size={13} />
                {text.flowIndex} <ArrowRight size={13} />
                {text.flowGround}
              </span>
            </div>
          </div>
        </aside>
      </div>
      <ConfirmDialog
        open={remove !== null}
        onClose={() => setRemove(null)}
        title={text.deleteTitle}
        description={fill(text.deleteBody, {
          name: remove?.filename || text.deleteFallback,
        })}
        action={text.deleteAction}
        onConfirm={() => void deleteDocument()}
      />
    </>
  )
}

function BadgeLabel({ text }: { text: string }) {
  return <small className="lifecycle-state">{text}</small>
}
