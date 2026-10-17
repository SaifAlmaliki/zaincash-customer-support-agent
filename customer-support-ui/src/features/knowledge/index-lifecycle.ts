import type { IndexResponse, KnowledgeDocument } from "../../lib/types"

export type PendingIndexes = Map<number, { updatedAt: string; status: string; claimed: boolean }>

export function acceptIndexRequest(pending: PendingIndexes, document: IndexResponse) {
  if (document.index_requested) pending.set(document.id, { updatedAt: document.updated_at, status: document.status, claimed: document.status === "indexing" })
}

type PollOptions = {
  pending: PendingIndexes
  load: (signal: AbortSignal) => Promise<KnowledgeDocument[]>
  onData: (documents: KnowledgeDocument[]) => void
  onError: (message: string) => void
  onPaused: () => void
}

export function pollKnowledge({ pending, load, onData, onError, onPaused }: PollOptions) {
  const controller = new AbortController()
  let timer: ReturnType<typeof setTimeout> | undefined
  const deadline = setTimeout(() => { stop(); onPaused() }, 180_000)
  function stop() {
    controller.abort()
    clearTimeout(timer)
    clearTimeout(deadline)
  }
  async function refresh() {
    try {
      const documents = await load(controller.signal)
      if (controller.signal.aborted) return
      for (const doc of documents) {
        const accepted = pending.get(doc.id)
        if (!accepted) continue
        if (doc.status === "indexing") accepted.claimed = true
        // Acceptance returns the old durable state, including failed/indexed on retry.
        // A terminal result must belong to the new attempt, not that old snapshot.
        if ((doc.status === "indexed" || doc.status === "failed") &&
          (accepted.claimed || doc.updated_at !== accepted.updatedAt || doc.status !== accepted.status)) pending.delete(doc.id)
      }
      onData(documents)
      if (pending.size || documents.some((doc) => doc.status === "indexing")) timer = setTimeout(refresh, 2000)
      else stop()
    } catch (error) {
      if (controller.signal.aborted) return
      stop()
      onError(error instanceof Error ? error.message : "Could not refresh document status.")
    }
  }
  void refresh()
  return stop
}
