import { ApiError } from "@/lib/api"
import type { Copy } from "@/lib/locale"

export function adminErrorMessage(error: unknown, text: Copy["models"]): string {
  if (error instanceof ApiError) {
    if (error.status === 403) return text.disabled
    if (error.status === 401) return text.wrongToken
    if (error.status === 404) return text.apiMissing
    if (error.message === "run_in_progress") return text.runInProgress
    if (error.message === "switch_in_progress") return text.switchInProgress
    return error.message
  }
  return error instanceof Error ? error.message : text.genericError
}
