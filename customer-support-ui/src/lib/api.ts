import type { ReviewInput, Result, Run, Mode, TicketInput, KnowledgeDocument } from "./types"

export async function request<T>(path: string, options: RequestInit = {}): Promise<T> {
  const response = await fetch(`/api${path}`, {
    ...options,
    headers: options.body instanceof FormData ? options.headers : { "Content-Type": "application/json", ...options.headers },
  })
  if (!response.ok) {
    let message = `Request failed (${response.status}). Please retry.`
    try {
      const body = await response.json()
      if (typeof body.detail === "string") message = body.detail
      else if (Array.isArray(body.detail)) message = body.detail.map((error: { msg: string }) => error.msg).join(" ")
    } catch { /* Proxies may return HTML when the API is offline. */ }
    throw new Error(message)
  }
  if (response.status === 204) return undefined as T
  try { return await response.json() as T }
  catch { throw new Error("The API returned an invalid response. Check that the backend is running on port 8000.") }
}

export const api = {
  startRun: (mode: Mode, tickets: TicketInput[]) => request<Run>("/runs", { method: "POST", body: JSON.stringify({ mode, tickets }) }),
  review: (id: number, review: ReviewInput) => request<Result>(`/results/${id}/reviews`, { method: "POST", body: JSON.stringify(review) }),
  uploadDocument: (file: File) => {
    const body = new FormData(); body.append("file", file)
    return request<KnowledgeDocument>("/knowledge", { method: "POST", body })
  },
  deleteDocument: (id: number) => request<void>(`/knowledge/${id}`, { method: "DELETE" }),
}
