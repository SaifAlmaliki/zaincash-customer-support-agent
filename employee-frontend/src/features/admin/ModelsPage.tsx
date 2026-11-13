import { useState } from "react"
import { Lock } from "lucide-react"
import { Button } from "@/components/ui/button"
import { Card } from "@/components/ui/card"
import { ErrorState, LoadingState, PageHeader } from "@/components/shared/workspace-ui"
import { useResource } from "@/hooks/use-resource"
import { setAdminSession, useAdminSession, type AdminSession } from "@/lib/admin-session"
import { adminRequest } from "@/lib/api"
import { useCopy } from "@/lib/locale"
import type { AuditEntry, EmbeddingSwitch, StepModel } from "@/lib/types"
import { useWorkspace } from "@/lib/workspace"
import { AdminUnlock } from "./AdminUnlock"
import { AuditList } from "./AuditList"
import { ChangeModelDialog } from "./ChangeModelDialog"
import { EmbeddingSwitchStatus } from "./EmbeddingSwitchStatus"
import { ModelStepCard } from "./ModelStepCard"

export function ModelsPage() {
  const text = useCopy().models
  const session = useAdminSession()
  return (
    <>
      <PageHeader title={text.title} description={text.description}>
        {session && (
          <Button variant="outline" onClick={() => setAdminSession(null)}>
            <Lock size={15} />
            {text.lock}
          </Button>
        )}
      </PageHeader>
      {session ? <UnlockedModels session={session} /> : <AdminUnlock />}
    </>
  )
}

function UnlockedModels({ session }: { session: AdminSession }) {
  const workspace = useWorkspace()
  const [revision, setRevision] = useState(0)
  const [editing, setEditing] = useState<StepModel | null>(null)
  const models = useResource<{ steps: StepModel[] }>("/models", revision, 0, adminRequest)
  const audit = useResource<{ items: AuditEntry[] }>("/models/audit?limit=50", revision, 0, adminRequest)
  // One-row status read, polled like RunDetailPage polls its run.
  const embedSwitch = useResource<EmbeddingSwitch | null>("/models/embed/switch", revision, 3000, adminRequest)
  const switching = embedSwitch.data?.status === "running"
  if (models.error) return <ErrorState message={models.error} retry={models.reload} />
  if (!models.data) return <LoadingState />
  return (
    <>
      {embedSwitch.data && <EmbeddingSwitchStatus value={embedSwitch.data} />}
      <Card className="models-panel" size="sm">
        <ul className="models-list">
          {models.data.steps.map((step) => (
            <ModelStepCard
              key={step.step}
              value={step}
              disabled={step.step === "embed" && switching}
              onChange={() => setEditing(step)}
            />
          ))}
        </ul>
      </Card>
      <AuditList items={audit.data?.items ?? []} error={audit.error} />
      {editing && (
        <ChangeModelDialog
          step={editing}
          changedBy={session.name}
          onClose={() => setEditing(null)}
          onSaved={() => {
            setEditing(null)
            setRevision((value) => value + 1)
            workspace.refresh()
          }}
        />
      )}
    </>
  )
}
