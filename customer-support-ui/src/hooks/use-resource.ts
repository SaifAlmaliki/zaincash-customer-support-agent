import { useEffect, useReducer, useState } from "react"
import { request } from "@/lib/api"

type Resource<T> = { data: T | null; error: string | null; loading: boolean; path: string | null }
export function useResource<T>(path: string | null, revision = 0, pollMs = 0) {
  const [state, update] = useReducer((old: Resource<T>, next: Partial<Resource<T>>) => ({ ...old, ...next }),
    { data: null, error: null, loading: Boolean(path), path: null })
  const [retry, setRetry] = useState(0)
  useEffect(() => {
    if (path === null) return
    const controller = new AbortController()
    let timer: ReturnType<typeof setTimeout> | undefined
    async function load() {
      try {
        const data = await request<T>(path!, { signal: controller.signal })
        if (!controller.signal.aborted) update({ data, loading: false, error: null, path })
      } catch (error) {
        if (!controller.signal.aborted) update({ loading: false, path, error: error instanceof Error ? error.message : "Could not load data." })
      }
      if (pollMs && !controller.signal.aborted) timer = setTimeout(load, pollMs)
    }
    update({ loading: true, error: null })
    void load()
    return () => { controller.abort(); clearTimeout(timer) }
  }, [path, revision, retry, pollMs])
  return { ...state, data: path === state.path ? state.data : null, reload: () => setRetry((value) => value + 1) }
}
