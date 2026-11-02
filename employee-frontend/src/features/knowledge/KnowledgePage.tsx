import { useEffect, useRef, useState } from "react"
import { BookOpen, FileUp } from "lucide-react"
import { Button } from "@/components/ui/button"
import { Card, CardContent } from "@/components/ui/card"
import {
  ConfirmDialog,
  ErrorState,
  PageHeader,
} from "@/components/shared/workspace-ui"
import { useWorkspace } from "@/lib/workspace"
import { fill, useCopy } from "@/lib/locale"
import { api } from "@/lib/api"
import type { KnowledgeDocument } from "@/lib/types"
import { useKnowledgeLibrary } from "./use-knowledge-library"
import { KnowledgeSearch } from "./KnowledgeSearch"
import { DocumentList } from "./DocumentList"
import { KnowledgeReadiness } from "./KnowledgeReadiness"

export function KnowledgePage() {
  const copy = useCopy()
  const text = copy.knowledge
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
          <DocumentList
            documents={documents}
            storedCount={query.documents.length}
            search={search}
            loading={query.loading}
            busy={busy}
            configured={configured}
            selectedId={selectedId}
            pendingIds={query.pendingIds}
            canRequestIndex={query.canRequestIndex}
            onSearchChange={setSearch}
            onRefresh={query.refresh}
            onIndex={(doc) => void indexDocument(doc)}
            onInspect={(doc) => setSelectedId(doc.id)}
            onDelete={setRemove}
          />
          <KnowledgeSearch configured={configured} selected={selected} onClose={() => setSelectedId(null)} />
        </div>
        <KnowledgeReadiness health={workspace.health} configured={configured} />
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
