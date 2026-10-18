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
import { api } from "@/lib/api"
import { dateLabel, sizeLabel } from "@/lib/format"
import type { KnowledgeDocument } from "@/lib/types"
import { useKnowledgeLibrary } from "./use-knowledge-library"
import { KnowledgeSearch } from "./KnowledgeSearch"

export function KnowledgePage() {
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
      if (!file.size) throw new Error("Choose a document that contains text.")
      if (file.size > 10 * 1024 * 1024)
        throw new Error("Choose a document smaller than 10 MB.")
      const document = await api.uploadDocument(file, controller.signal)
      if (controller.signal.aborted) return
      query.accepted(document)
      setNotice(document.index_requested
        ? `${document.filename}: indexing request accepted. Follow its status below.`
        : document.status === "indexed" ? `${document.filename} is already indexed; no new indexing was requested.`
        : document.status === "failed" ? `${document.filename} is stored with a failed index. Review the error and choose Retry index.`
        : document.status === "indexing" ? `${document.filename} is already indexing.`
        : configured ? `${document.filename} is stored, but indexing was not queued. Capacity may be full; choose Index document to try again.`
        : `${document.filename} is stored. Enable and configure knowledge indexing, then choose Index document.`)
    } catch (e) {
      if (!controller.signal.aborted) setActionError(e instanceof Error ? e.message : "Upload failed.")
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
        setNotice(response.status === "indexing"
          ? `${doc.filename}: indexing is running. Status checks resumed.`
          : `${doc.filename}: indexing request accepted${rerequest ? " again" : ""}. Status checks resumed; waiting for a worker result.`)
      }
    } catch (e) {
      if (!controller.signal.aborted) setActionError(`${doc.filename}: ${e instanceof Error ? e.message : "Index request failed."} ${rerequest ? "The previous acceptance remains pending. Use Request indexing again when indexing is available." : "The stored source is retained. Retry when indexing is available."}`)
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
      setNotice("Document deleted. Saved citation evidence remains available in historical reviews.")
    } catch (e) {
      if (!controller.signal.aborted) setActionError(e instanceof Error ? e.message : "Could not delete document.")
    } finally { finishMutation(controller) }
  }
  return (
    <>
      <PageHeader
        title="Knowledge base"
        description="The source material behind a well-grounded response."
      >
        <Button
          size="lg"
          disabled={busy}
          onClick={() => input.current?.click()}
        >
          <FileUp size={17} />
          {busy ? "Working…" : "Upload document"}
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
                  <BookOpen size={27} strokeWidth={1.5} />
                </div>
                <h3>Give your team a shared source of truth</h3>
                <p>
                  Upload policies, FAQs and support procedures.
                  <br />
                  PDF, Markdown or text · up to 10 MB
                </p>
                <Button
                  variant="outline"
                  disabled={busy}
                  onClick={() => input.current?.click()}
                >
                  Browse files
                </Button>
                <input
                  ref={input}
                  type="file"
                  className="sr-only"
                  aria-label="Upload knowledge document"
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
          {query.paused && <p className="knowledge-message" role="status">Automatic status checks paused after 3 minutes. Accepted requests remain pending. Refresh status checks for a result; if no worker claim was recorded, use Request indexing again to request recovery.</p>}
          <Card>
            <CardHeader>
              <CardTitle className="section-title">
                <FileText size={17} />
                Documents
                <span className="muted small">{documents.length} shown / {query.documents.length} stored</span>
              </CardTitle>
              <Button variant="ghost" size="sm" disabled={busy} onClick={query.refresh}><RefreshCw size={14} />Refresh status</Button>
            </CardHeader>
            <CardContent>
              <div className="input-with-icon">
                <Search size={16} />
                <Input
                  aria-label="Search documents"
                  placeholder="Find a document by name…"
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
                    const indexAction = pending && requestable ? "Request indexing again" : active ? "Index pending" : doc.status === "failed" ? "Retry index" : doc.status === "indexed" ? "Reindex" : "Index document"
                    return (
                    <div className="document-item" key={doc.id}>
                      <span className="document-icon">
                        <FileText size={23} />
                      </span>
                      <div className="document-body">
                        <strong>{doc.filename}</strong>
                        <small>
                          {sizeLabel(doc.size)} · Uploaded{" "}
                          {dateLabel(doc.created_at)}
                        </small>
                        <div className="document-status" aria-live="polite">
                          <StatusBadge status={pending && doc.status !== "indexing" ? "index_requested" : doc.status} />
                          <span className="muted small">{doc.chunk_count} passages</span>
                        </div>
                        {pending && doc.status !== "indexing" && <p className="field-help">Request accepted; waiting for the indexing worker. Last stored state: {doc.status.replaceAll("_", " ")}. {requestable && "If indexing stalls, use Request indexing again. Active requests are deduplicated; this does not cancel existing work."}</p>}
                        {doc.error && <p className="document-error">{pending ? "Previous attempt: " : "Indexing failed: "}{doc.error} {!active && "Check the document and indexing configuration, then retry."}</p>}
                        {doc.status === "awaiting_indexing" && !pending && <p className="field-help">Stored; indexing has not started. {configured ? "Choose Index document to request indexing." : "Indexing needs to be enabled and configured."}</p>}
                        {doc.embedding_model && <small>{doc.embedding_model} · {doc.embedding_dimensions} dimensions{doc.indexed_at ? ` · Indexed ${dateLabel(doc.indexed_at)}` : ""}</small>}
                        {!!doc.category_tags.length && <small>Categories: {doc.category_tags.join(", ")}</small>}
                        <div className="document-actions">
                          <Button variant="outline" size="sm" disabled={busy || !requestable || !configured} onClick={() => void indexDocument(doc)} aria-label={`${indexAction}: ${doc.filename}`}>
                            {indexAction}
                          </Button>
                          <Button variant="ghost" size="sm" aria-pressed={selectedId === doc.id} onClick={() => setSelectedId(doc.id)}>Inspect passages<span className="sr-only">: {doc.filename}</span></Button>
                      <Button
                        variant="ghost"
                        size="icon"
                        nativeButton={false}
                        render={
                          <a href={`/api/knowledge/${doc.id}/download`} />
                        }
                        aria-label={`Download ${doc.filename}`}
                      >
                        <Download size={17} />
                      </Button>
                      <Button
                        variant="ghost"
                        size="icon"
                        aria-label={`Delete ${doc.filename}`}
                        disabled={busy || active}
                        onClick={() => setRemove(doc)}
                      >
                        <Trash2 size={16} />
                      </Button>
                        </div>
                      </div>
                    </div>
                  )})}
                </div>
              ) : (
                <EmptyState
                  title={
                    search
                      ? "No matching documents"
                      : "Your document library is empty"
                  }
                  description="Add your first synthetic support policy to get started."
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
                <Database size={17} />
                Document lifecycle
              </CardTitle>
            </CardHeader>
            <CardContent>
              <ol className="document-lifecycle">
                <li>
                  <span>1</span>
                  <div>
                    <strong>Upload & store</strong>
                    <p>Your files are saved in PostgreSQL with a checksum.</p>
                  </div>
                  <BadgeLabel text="Available" />
                </li>
                <li>
                  <span>2</span>
                  <div>
                    <strong>Chunk & embed</strong>
                    <p>Prepare searchable passages with pgvector.</p>
                  </div>
                  <BadgeLabel text={configured ? "Configured" : "Needs setup"} />
                </li>
                <li>
                  <span>3</span>
                  <div>
                    <strong>Retrieve & cite</strong>
                    <p>Ground the agent’s draft in relevant policy passages.</p>
                  </div>
                  <BadgeLabel text={workspace.health?.knowledge?.ready ? "Ready" : "Needs index"} />
                </li>
              </ol>
            </CardContent>
          </Card>
          <Card>
            <CardHeader><CardTitle className="section-title">Knowledge readiness</CardTitle></CardHeader>
            <CardContent>
              <p className="muted small">{workspace.health?.knowledge ? `${workspace.health.knowledge.indexed_document_count} searchable documents · ${workspace.health.knowledge.status}` : "Readiness is unavailable. Check the API connection."}</p>
              {workspace.health?.knowledge && <>
                <p className="field-help">{workspace.health.knowledge.embedding_model} · {workspace.health.knowledge.embedding_dimensions} dimensions</p>
                <p className="field-help">{!workspace.health.knowledge.enabled ? "Knowledge retrieval is disabled. Enable RAG to index and search." : !configured ? "Configure the embedding provider to index and search policies." : workspace.health.knowledge.ready ? "Indexed policy passages are available for grounded drafts." : "Index a policy successfully before expecting a grounded draft."}</p>
                <p className="field-help">{workspace.health.drafting?.credential_check_configured ? "Credential checking is configured." : "Credential checking is not configured; affected drafts are marked for review."} Readiness reflects configuration and stored indexes, not a live provider check.</p>
              </>}
            </CardContent>
          </Card>
          <div className="knowledge-note">
            <Info size={20} />
            <div>
              <strong>Stored does not mean indexed</strong>
              <p>
                Only successfully indexed documents can ground new drafts.
                Saved reviews retain their cited passages after a source is reindexed or deleted.
              </p>
              <span>
                Upload <ArrowRight size={13} />
                Index <ArrowRight size={13} />
                Ground
              </span>
            </div>
          </div>
        </aside>
      </div>
      <ConfirmDialog
        open={remove !== null}
        onClose={() => setRemove(null)}
        title="Delete this document?"
        description={`${remove?.filename || "This document"} and its searchable passages will be removed. Evidence already saved with a draft remains in that review.`}
        action="Delete document"
        onConfirm={() => void deleteDocument()}
      />
    </>
  )
}

function BadgeLabel({ text }: { text: string }) {
  return <small className="lifecycle-state">{text}</small>
}
