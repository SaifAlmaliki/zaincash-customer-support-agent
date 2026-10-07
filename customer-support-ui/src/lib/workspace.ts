import { createContext, useContext } from "react"
import type { Health, Result, ReviewInput, WorkspaceMode } from "./types"

export type WorkspaceContextValue = {
  mode: WorkspaceMode; setMode: (mode: WorkspaceMode) => void; revision: number; refresh: () => void;
  health: Health | null; connectionError: string | null; preview: Result[];
  reviewPreview: (id: number, review: ReviewInput) => void;
  notify: (message: string, error?: boolean) => void;
}
export const WorkspaceContext = createContext<WorkspaceContextValue | null>(null)
export function useWorkspace() {
  const context = useContext(WorkspaceContext)
  if (!context) throw new Error("WorkspaceProvider is missing.")
  return context
}
