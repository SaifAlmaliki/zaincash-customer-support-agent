import { createContext, useContext } from "react"
import type { Health } from "./types"

export type WorkspaceContextValue = {
  revision: number
  refresh: () => void
  health: Health | null
  connectionError: string | null
  notify: (message: string, error?: boolean) => void
}
export const WorkspaceContext = createContext<WorkspaceContextValue | null>(
  null
)
export function useWorkspace() {
  const context = useContext(WorkspaceContext)
  if (!context) throw new Error("WorkspaceProvider is missing.")
  return context
}
