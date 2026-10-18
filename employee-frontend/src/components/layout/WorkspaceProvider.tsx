import { useState, type ReactNode } from "react"
import { CheckCircle2, CircleAlert, X } from "lucide-react"
import { WorkspaceContext } from "@/lib/workspace"
import { useResource } from "@/hooks/use-resource"
import type { Health } from "@/lib/types"
import { Button } from "@/components/ui/button"

export function WorkspaceProvider({ children }: { children: ReactNode }) {
  const [revision, setRevision] = useState(0)
  const [notice, setNotice] = useState<{
    message: string
    error: boolean
  } | null>(null)
  const health = useResource<Health>("/health", revision, 15000)
  return (
    <WorkspaceContext.Provider
      value={{
        revision,
        refresh: () => setRevision((v) => v + 1),
        health: health.data,
        connectionError: health.error,
        notify: (message, error = false) => setNotice({ message, error }),
      }}
    >
      {children}
      {notice && (
        <div
          className={`workspace-toast ${notice.error ? "toast-error" : ""}`}
          role={notice.error ? "alert" : "status"}
        >
          {notice.error ? (
            <CircleAlert size={18} />
          ) : (
            <CheckCircle2 size={18} />
          )}
          <span>{notice.message}</span>
          <Button
            size="icon-sm"
            variant="ghost"
            aria-label="Dismiss notification"
            onClick={() => setNotice(null)}
          >
            <X size={16} />
          </Button>
        </div>
      )}
    </WorkspaceContext.Provider>
  )
}
