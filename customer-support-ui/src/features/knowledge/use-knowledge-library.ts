import { useEffect, useRef, useState } from "react"
import { request } from "@/lib/api"
import type { IndexResponse, KnowledgeDocument } from "@/lib/types"
import { acceptIndexRequest, pollKnowledge, type PendingIndexes } from "./index-lifecycle"

// Keep accepted IDs across route/mode remounts, but never poll them in preview.
// Only terminal results or explicit deletion release an accepted request.
const pending: PendingIndexes = new Map()

export function useKnowledgeLibrary(live: boolean, revision: number) {
  const stopPolling = useRef<(() => void) | null>(null)
  const [reload, setReload] = useState(0)
  const [state, setState] = useState({
    documents: [] as KnowledgeDocument[], pendingIds: live ? [...pending.keys()] : [],
    loading: live, error: "", paused: false,
  })
  useEffect(() => {
    if (!live) return
    const stop = pollKnowledge({
      pending,
      load: (signal) => request<KnowledgeDocument[]>("/knowledge", { signal }),
      onData: (documents) => setState({ documents, pendingIds: [...pending.keys()], loading: false, error: "", paused: false }),
      onError: (error) => setState((old) => ({ ...old, error, loading: false })),
      onPaused: () => setState((old) => ({ ...old, paused: true, loading: false })),
    })
    stopPolling.current = stop
    return stop
  }, [live, revision, reload])
  function refresh() {
    setState((old) => ({ ...old, error: "", paused: false }))
    setReload((old) => old + 1)
  }
  return {
    ...state,
    refresh,
    accepted: (document: IndexResponse) => {
      // A list requested before the mutation must not settle the new attempt.
      stopPolling.current?.()
      acceptIndexRequest(pending, document)
      setState((old) => ({ ...old, pendingIds: [...pending.keys()], documents: [document, ...old.documents.filter((doc) => doc.id !== document.id)] }))
      refresh()
    },
    deleted: (id: number) => {
      stopPolling.current?.()
      pending.delete(id)
      setState((old) => ({ ...old, pendingIds: [...pending.keys()], documents: old.documents.filter((doc) => doc.id !== id) }))
      refresh()
    },
  }
}
