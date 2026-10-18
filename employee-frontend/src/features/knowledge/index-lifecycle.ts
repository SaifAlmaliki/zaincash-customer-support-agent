import type { IndexResponse, KnowledgeDocument } from "../../lib/types"

export type PendingIndexes = Map<
  number,
  { updatedAt: string; status: string; claimed: boolean }
>

const pendingKey = "zaincash.pending-indexes.v1"

export function canRequestIndex(
  document: Pick<KnowledgeDocument, "id" | "status">,
  pending: PendingIndexes
) {
  // Acceptance can outlive a background job that failed before a durable claim.
  // Explicit re-requests are safe because the API deduplicates active admission.
  return document.status !== "indexing" && !pending.get(document.id)?.claimed
}

export function restorePendingIndexes(storage?: Pick<Storage, "getItem">): PendingIndexes {
  const pending: PendingIndexes = new Map()
  try {
    const records: unknown = JSON.parse(
      (storage ?? globalThis.sessionStorage)?.getItem(pendingKey) ?? "[]"
    )
    if (!Array.isArray(records)) return pending
    for (const entry of records) {
      if (!Array.isArray(entry) || entry.length !== 2) continue
      const [id, value] = entry
      if (
        !Number.isSafeInteger(id) || id <= 0 ||
        !value || typeof value !== "object" ||
        typeof value.updatedAt !== "string" || !value.updatedAt ||
        !["awaiting_indexing", "indexing", "indexed", "failed"].includes(value.status) ||
        typeof value.claimed !== "boolean"
      ) continue
      pending.set(id, { updatedAt: value.updatedAt, status: value.status, claimed: value.claimed })
    }
  } catch {
    // Blocked or malformed storage must not prevent the workspace from loading.
  }
  return pending
}

export function persistPendingIndexes(pending: PendingIndexes, storage?: Pick<Storage, "setItem">) {
  try {
    (storage ?? globalThis.sessionStorage)?.setItem(pendingKey, JSON.stringify([...pending]))
  } catch {
    // Tracking still works in memory when session storage is unavailable.
  }
}

export function acceptIndexRequest(
  pending: PendingIndexes,
  document: IndexResponse
) {
  if (document.index_requested)
    pending.set(document.id, {
      updatedAt: document.updated_at,
      status: document.status,
      claimed: document.status === "indexing",
    })
}

type PollOptions = {
  pending: PendingIndexes
  load: (signal: AbortSignal) => Promise<KnowledgeDocument[]>
  onData: (documents: KnowledgeDocument[]) => void
  onError: (message: string) => void
  onPaused: () => void
}

export function pollKnowledge({
  pending,
  load,
  onData,
  onError,
  onPaused,
}: PollOptions) {
  const controller = new AbortController()
  let timer: ReturnType<typeof setTimeout> | undefined
  const deadline = setTimeout(() => {
    stop()
    onPaused()
  }, 180_000)
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
        if (
          (doc.status === "indexed" || doc.status === "failed") &&
          (accepted.claimed ||
            doc.updated_at !== accepted.updatedAt ||
            doc.status !== accepted.status)
        ) pending.delete(doc.id)
      }
      onData(documents)
      if (pending.size || documents.some((doc) => doc.status === "indexing"))
        timer = setTimeout(refresh, 2000)
      else stop()
    } catch (error) {
      if (controller.signal.aborted) return
      stop()
      onError(
        error instanceof Error ? error.message : "Could not refresh document status."
      )
    }
  }
  void refresh()
  return stop
}
