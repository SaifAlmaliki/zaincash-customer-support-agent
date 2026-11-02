import { renderToStaticMarkup } from "react-dom/server"
import { afterEach, beforeEach, expect, it } from "vitest"
import type { Health, KnowledgeDocument } from "@/lib/types"
import { getLocale, setLocale } from "@/lib/locale"
import { DocumentList, type DocumentListProps } from "./DocumentList"
import { KnowledgeReadiness } from "./KnowledgeReadiness"

const originalLocale = getLocale()

beforeEach(() => setLocale("en"))
afterEach(() => setLocale(originalLocale))

function knowledgeDocument(patch: Partial<KnowledgeDocument> = {}): KnowledgeDocument {
  return {
    id: 7,
    filename: "policy.md",
    size: 40,
    status: "awaiting_indexing",
    content_type: "text/markdown",
    sha256: "synthetic",
    created_at: "2026-10-17T00:00:00Z",
    updated_at: "2026-10-17T00:00:00Z",
    category_tags: [],
    chunk_count: 0,
    embedding_model: null,
    embedding_dimensions: null,
    chunking_version: null,
    indexed_at: null,
    error: null,
    cost_usd: 0,
    ...patch,
  }
}

function listProps(patch: Partial<DocumentListProps> = {}): DocumentListProps {
  return {
    documents: [knowledgeDocument()],
    storedCount: 1,
    search: "",
    loading: false,
    busy: false,
    configured: true,
    selectedId: null,
    pendingIds: [],
    canRequestIndex: () => true,
    onSearchChange: () => {},
    onRefresh: () => {},
    onIndex: () => {},
    onInspect: () => {},
    onDelete: () => {},
    ...patch,
  }
}

function health(patch: Partial<Health> = {}): Health {
  return {
    database: "connected",
    configured_modes: ["jev"],
    capabilities: { drafting: true, rag_indexing: true, evaluation: false },
    ...patch,
  }
}

it("renders a pending failed document as a recoverable previous attempt", () => {
  const document = knowledgeDocument({ status: "failed", error: "Embedding unavailable" })
  const html = renderToStaticMarkup(<DocumentList {...listProps({
    documents: [document],
    pendingIds: [7],
  })} />)
  expect(html).toContain("Request indexing again")
  expect(html).toContain("Previous attempt:")
  expect(html).toContain("Embedding unavailable")
  expect(html).toContain("Request accepted; waiting for the indexing worker")
})

it("keeps active and terminal document actions distinct", () => {
  const active = knowledgeDocument({ id: 1, status: "indexing" })
  const failed = knowledgeDocument({ id: 2, filename: "failed.md", status: "failed" })
  const indexed = knowledgeDocument({ id: 3, filename: "indexed.md", status: "indexed" })
  const activeHtml = renderToStaticMarkup(<DocumentList {...listProps({
    documents: [active],
    pendingIds: [1],
    canRequestIndex: () => false,
  })} />)
  const terminalHtml = renderToStaticMarkup(<DocumentList {...listProps({
    documents: [failed, indexed],
    storedCount: 2,
  })} />)

  expect(activeHtml).toContain("Index pending")
  expect(activeHtml).not.toContain("Request indexing again")
  expect(terminalHtml).toContain("Retry index")
  expect(terminalHtml).toContain("Reindex")
  expect(terminalHtml).toContain("/api/knowledge/3/download")
})

it("keeps missing and disabled readiness explicit", () => {
  const missing = renderToStaticMarkup(<KnowledgeReadiness health={null} configured={false} />)
  const disabled = renderToStaticMarkup(<KnowledgeReadiness
    configured={false}
    health={health({
      knowledge: {
        enabled: false,
        configured: false,
        ready: false,
        status: "disabled",
        indexed_document_count: 0,
        embedding_model: "embed-model",
        embedding_dimensions: 1536,
      },
    })}
  />)

  expect(missing).toContain("Readiness is unavailable")
  expect(disabled).toContain("Knowledge retrieval is disabled")
  expect(disabled).toContain("0 searchable documents")
  expect(disabled).toContain("disabled")
})

it("renders configured ready health without changing its status content", () => {
  const html = renderToStaticMarkup(<KnowledgeReadiness
    configured={true}
    health={health({
      knowledge: {
        enabled: true,
        configured: true,
        ready: true,
        status: "ready",
        indexed_document_count: 2,
        embedding_model: "embed-model",
        embedding_dimensions: 1536,
      },
    })}
  />)
  expect(html).toContain("2 searchable documents")
  expect(html).toContain("ready")
  expect(html).toContain("embed-model")
  expect(html).toContain("1536 dimensions")
})
