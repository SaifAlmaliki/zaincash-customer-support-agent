import type {
  ReviewInput,
  Result,
  Run,
  TicketInput,
  IndexResponse,
  ChunkPage,
  KnowledgeSearchResult,
  AuditEntry,
  CatalogProvider,
  EmbeddingSwitch,
  ModelChoiceInput,
  ModelStep,
  ProbeResult,
  StepModel,
} from "./types"
import { getAdminSession, setAdminSession } from "./admin-session"

export class ApiError extends Error {
  status: number

  constructor(message: string, status: number) {
    super(message)
    this.name = "ApiError"
    this.status = status
  }
}

export async function request<T>(
  path: string,
  options: RequestInit = {}
): Promise<T> {
  const response = await fetch(`/api${path}`, {
    ...options,
    headers:
      options.body instanceof FormData
        ? options.headers
        : { "Content-Type": "application/json", ...options.headers },
  })
  if (!response.ok) {
    let message = `Request failed (${response.status}). Please retry.`
    try {
      const body = await response.json()
      if (typeof body.detail === "string") message = body.detail
      else if (Array.isArray(body.detail))
        message = body.detail
          .map((error: { msg: string }) => error.msg)
          .join(" ")
    } catch {
      /* Proxies may return HTML when the API is offline. */
    }
    throw new ApiError(message, response.status)
  }
  if (response.status === 204) return undefined as T
  try {
    return (await response.json()) as T
  } catch {
    throw new Error(
      "The API returned an invalid response. Check that the backend is running on port 8000."
    )
  }
}

export async function loadQueue(path: string, options: RequestInit = {}) {
  const [pathname, search = ""] = path.split("?")
  const params = new URLSearchParams(search)
  params.set("limit", "500")
  const items = new Map<number, Result>()
  let offset = 0
  let total: number
  do {
    params.set("offset", String(offset))
    const page = await request<{ items: Result[]; total: number }>(
      `${pathname}?${params}`,
      options
    )
    total = page.total
    for (const item of page.items) items.set(item.id, item)
    if (page.items.length === 0 && items.size < total)
      throw new Error("The queue changed while loading. Please retry.")
    offset += page.items.length
  } while (offset < total)
  if (items.size !== total)
    throw new Error("The queue changed while loading. Please retry.")
  return { items: [...items.values()], total }
}

export const api = {
  startRun: (tickets: TicketInput[]) =>
    request<Run>("/runs", {
      method: "POST",
      body: JSON.stringify({ mode: "jev", tickets }),
    }),
  review: (id: number, review: ReviewInput) =>
    request<Result>(`/results/${id}/reviews`, {
      method: "POST",
      body: JSON.stringify(review),
    }),
  uploadDocument: (file: File, signal?: AbortSignal) => {
    const body = new FormData()
    body.append("file", file)
    return request<IndexResponse>("/knowledge", { method: "POST", body, signal })
  },
  indexDocument: (id: number, categoryTags?: string[] | null, signal?: AbortSignal) =>
    request<IndexResponse>(`/knowledge/${id}/index`, {
      method: "POST", body: JSON.stringify({ category_tags: categoryTags ?? null }), signal,
    }),
  documentChunks: (id: number, offset = 0, limit = 50, signal?: AbortSignal) =>
    request<ChunkPage>(`/knowledge/${id}/chunks?offset=${offset}&limit=${limit}`, { signal }),
  searchKnowledge: (query: string, category: string | null = null, k = 5, signal?: AbortSignal) =>
    request<KnowledgeSearchResult>("/knowledge/search", {
      method: "POST", body: JSON.stringify({ query, category, k }), signal,
    }),
  deleteDocument: (id: number, signal?: AbortSignal) =>
    request<void>(`/knowledge/${id}`, { method: "DELETE", signal }),
}

export async function adminRequest<T>(path: string, options: RequestInit = {}): Promise<T> {
  try {
    return await request<T>(`/admin${path}`, {
      ...options,
      headers: {
        ...(options.headers as Record<string, string> | undefined),
        "X-Admin-Token": getAdminSession()?.token ?? "",
      },
    })
  } catch (error) {
    // A changed or disabled token must return the page to its locked state.
    if (error instanceof ApiError && (error.status === 401 || error.status === 403))
      setAdminSession(null)
    throw error
  }
}

export const adminApi = {
  verify: (token: string) =>
    request<void>("/admin/session", { method: "POST", headers: { "X-Admin-Token": token } }),
  models: (options?: RequestInit) => adminRequest<{ steps: StepModel[] }>("/models", options),
  catalog: (step: ModelStep, refresh = false) =>
    adminRequest<{ step: ModelStep; providers: CatalogProvider[] }>(
      `/models/catalog?step=${step}&refresh=${refresh}`,
    ),
  test: (step: ModelStep, choice: ModelChoiceInput) =>
    adminRequest<ProbeResult>("/models/test", {
      method: "POST",
      body: JSON.stringify({ step, ...choice }),
    }),
  save: (step: ModelStep, choice: ModelChoiceInput, changedBy: string) =>
    adminRequest<StepModel>(`/models/${step}`, {
      method: "PUT",
      body: JSON.stringify({ ...choice, changed_by: changedBy }),
    }),
  startEmbeddingSwitch: (choice: ModelChoiceInput, changedBy: string) =>
    adminRequest<EmbeddingSwitch>("/models/embed/switch", {
      method: "POST",
      body: JSON.stringify({ ...choice, changed_by: changedBy }),
    }),
  embeddingSwitch: (options?: RequestInit) =>
    adminRequest<EmbeddingSwitch | null>("/models/embed/switch", options),
  audit: (options?: RequestInit) => adminRequest<{ items: AuditEntry[] }>("/models/audit?limit=50", options),
}
