import { useEffect, useRef, useState } from "react"
import { request } from "@/lib/api"
import type { IndexResponse, KnowledgeDocument } from "@/lib/types"
import { acceptIndexRequest, pollKnowledge, type PendingIndexes } from "./index-lifecycle"

export function useKnowledgeLibrary(live: boolean, revision: number) {
  const pending = useRef<PendingIndexes>(new Map())
  const [reload, setReload] = useState(0)
  const [state, setState] = useState({
    documents: [] as KnowledgeDocument[], pendingIds: [] as number[],
    loading: live, error: "", paused: false,
  })
  useEffect(() => {
    if (!live) return
    return pollKnowledge({
      pending: pending.current,
      load: (signal) => request<KnowledgeDocument[]>("/knowledge", { signal }),
      onData: (documents) => setState({ documents, pendingIds: [...pending.current.keys()], loading: false, error: "", paused: false }),
      onError: (error) => setState((old) => ({ ...old, error, loading: false })),
      onPaused: () => setState((old) => ({ ...old, paused: true, loading: false })),
    })
  }, [live, revision, reload])
  function refresh() {
    setState((old) => ({ ...old, error: "", paused: false }))
    setReload((old) => old + 1)
  }
  return {
    ...state,
    refresh,
    accepted: (document: IndexResponse) => {
      acceptIndexRequest(pending.current, document)
      setState((old) => ({ ...old, pendingIds: [...pending.current.keys()], documents: [document, ...old.documents.filter((doc) => doc.id !== document.id)] }))
      refresh()
    },
    deleted: (id: number) => {
      pending.current.delete(id)
      setState((old) => ({ ...old, pendingIds: [...pending.current.keys()], documents: old.documents.filter((doc) => doc.id !== id) }))
      refresh()
    },
  }
}
