import type { Copy } from "@/lib/locale"

export function runStartError(error: unknown, text: Copy["batch"]) {
  if (error instanceof Error && error.message === "knowledge_switch_in_progress") return text.switchInProgress
  return error instanceof Error ? error.message : text.startFailed
}
