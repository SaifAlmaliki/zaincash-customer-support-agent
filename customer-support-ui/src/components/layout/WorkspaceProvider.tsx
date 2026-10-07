import { useState, type ReactNode } from "react"
import { CheckCircle2, CircleAlert, X } from "lucide-react"
import { WorkspaceContext } from "@/lib/workspace"
import { useResource } from "@/hooks/use-resource"
import { previewResults } from "@/data/preview"
import type { Health, ReviewInput, WorkspaceMode } from "@/lib/types"
import { Button } from "@/components/ui/button"

export function WorkspaceProvider({ children }: { children: ReactNode }) {
  const [mode, setMode] = useState<WorkspaceMode>("live")
  const [revision, setRevision] = useState(0)
  const [preview, setPreview] = useState(previewResults)
  const [notice, setNotice] = useState<{
    message: string
    error: boolean
  } | null>(null)
  const health = useResource<Health>("/health", revision, 15000)
  function reviewPreview(id: number, review: ReviewInput) {
    setPreview((rows) =>
      rows.map((row) =>
        row.id !== id
          ? row
          : {
              ...row,
              status:
                review.action === "reassign"
                  ? row.status
                  : review.action === "reject"
                    ? "rejected"
                    : review.action === "edit_approve"
                      ? "edited"
                      : "approved",
              team: review.team || row.team,
              final_text: ["approve", "edit_approve"].includes(review.action)
                ? review.final_text || null
                : row.final_text,
              updated_at: new Date().toISOString(),
              reviews: [
                {
                  id: Date.now(),
                  reviewer: review.reviewer,
                  action: review.action,
                  final_text: review.final_text || null,
                  created_at: new Date().toISOString(),
                },
                ...(row.reviews || []),
              ],
            }
      )
    )
  }
  return (
    <WorkspaceContext.Provider
      value={{
        mode,
        setMode,
        revision,
        refresh: () => setRevision((v) => v + 1),
        health: health.data,
        connectionError: health.error,
        preview,
        reviewPreview,
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
