import { useRef, useState } from "react"
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
import { useResource } from "@/hooks/use-resource"
import { useWorkspace } from "@/lib/workspace"
import { api } from "@/lib/api"
import { dateLabel, sizeLabel } from "@/lib/format"
import type { KnowledgeDocument } from "@/lib/types"

export function KnowledgePage() {
  const workspace = useWorkspace(),
    input = useRef<HTMLInputElement>(null)
  const query = useResource<KnowledgeDocument[]>(
    workspace.mode === "preview" ? null : "/knowledge",
    workspace.revision
  )
  const [search, setSearch] = useState(""),
    [busy, setBusy] = useState(false),
    [remove, setRemove] = useState<KnowledgeDocument | null>(null)
  const documents = (query.data || []).filter((doc) =>
    doc.filename.toLowerCase().includes(search.toLowerCase())
  )
  async function upload(file?: File) {
    if (!file || busy || workspace.mode !== "live") return
    setBusy(true)
    try {
      if (file.size > 10 * 1024 * 1024)
        throw new Error("Choose a document smaller than 10 MB.")
      await api.uploadDocument(file)
      workspace.notify("Document stored. RAG indexing is not connected yet.")
      query.reload()
    } catch (e) {
      workspace.notify(e instanceof Error ? e.message : "Upload failed.", true)
    } finally {
      setBusy(false)
      if (input.current) input.current.value = ""
    }
  }
  async function deleteDocument() {
    if (!remove) return
    try {
      await api.deleteDocument(remove.id)
      setRemove(null)
      query.reload()
      workspace.notify("Document deleted.")
    } catch (e) {
      workspace.notify(
        e instanceof Error ? e.message : "Could not delete document.",
        true
      )
    }
  }
  return (
    <>
      <PageHeader
        title="Knowledge base"
        description="The source material behind a well-grounded response."
      >
        <Button
          size="lg"
          disabled={workspace.mode === "preview" || busy}
          onClick={() => input.current?.click()}
        >
          <FileUp size={17} />
          {busy ? "Uploading…" : "Upload document"}
        </Button>
      </PageHeader>
      <div className="knowledge-layout">
        <div className="evidence-stack">
          <Card className="knowledge-upload">
            <CardContent>
              <div
                className="upload-zone compact"
                onDragOver={(e) => e.preventDefault()}
                onDrop={(e) => {
                  e.preventDefault()
                  if (workspace.mode === "live")
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
                  disabled={workspace.mode === "preview" || busy}
                  onClick={() => input.current?.click()}
                >
                  Browse files
                </Button>
                <input
                  ref={input}
                  type="file"
                  className="sr-only"
                  aria-label="Upload knowledge document"
                  disabled={workspace.mode !== "live" || busy}
                  accept=".pdf,.md,.txt"
                  onChange={(e) => void upload(e.target.files?.[0])}
                />
              </div>
            </CardContent>
          </Card>
          {query.error && workspace.mode === "live" && (
            <ErrorState message={query.error} retry={query.reload} />
          )}
          <Card>
            <CardHeader>
              <CardTitle className="section-title">
                <FileText size={17} />
                Documents
                <span className="muted small">{documents.length} stored</span>
              </CardTitle>
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
              {query.loading && workspace.mode === "live" ? (
                <LoadingState />
              ) : documents.length ? (
                <div className="document-list">
                  {documents.map((doc) => (
                    <div className="document-item" key={doc.id}>
                      <span className="document-icon">
                        <FileText size={23} />
                      </span>
                      <div>
                        <strong>{doc.filename}</strong>
                        <small>
                          {sizeLabel(doc.size)} · Uploaded{" "}
                          {dateLabel(doc.created_at)}
                        </small>
                        <StatusBadge status={doc.status} />
                      </div>
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
                        onClick={() => setRemove(doc)}
                      >
                        <Trash2 size={16} />
                      </Button>
                    </div>
                  ))}
                </div>
              ) : (
                <EmptyState
                  title={
                    search
                      ? "No matching documents"
                      : "Your document library is empty"
                  }
                  description={
                    workspace.mode === "preview"
                      ? "Switch to the live workspace to upload and store policy documents."
                      : "Add your first synthetic support policy to get started."
                  }
                />
              )}
            </CardContent>
          </Card>
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
                  <BadgeLabel text="Not connected" />
                </li>
                <li>
                  <span>3</span>
                  <div>
                    <strong>Retrieve & cite</strong>
                    <p>Ground the agent’s draft in relevant policy passages.</p>
                  </div>
                  <BadgeLabel text="Not connected" />
                </li>
              </ol>
            </CardContent>
          </Card>
          <div className="knowledge-note">
            <Info size={20} />
            <div>
              <strong>Stored does not mean indexed</strong>
              <p>
                Uploaded files are awaiting the RAG ingestion stage. The UI
                never marks them searchable before indexing succeeds.
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
        description={`${remove?.filename || "This document"} will be removed from the stored document library.`}
        action="Delete document"
        onConfirm={() => void deleteDocument()}
      />
    </>
  )
}

function BadgeLabel({ text }: { text: string }) {
  return <small className="lifecycle-state">{text}</small>
}
