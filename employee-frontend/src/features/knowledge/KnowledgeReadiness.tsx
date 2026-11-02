import { ArrowRight, Database, Info } from "lucide-react"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { fill, useCopy } from "@/lib/locale"
import type { Health } from "@/lib/types"

export function KnowledgeReadiness({
  health,
  configured,
}: {
  health: Health | null
  configured: boolean
}) {
  const text = useCopy().knowledge
  const readinessStatus: Record<string, string> = {
    disabled: text.statusDisabled,
    unconfigured: text.statusUnconfigured,
    ready: text.statusReady,
    indexing: text.statusIndexing,
    failed: text.statusFailed,
    empty: text.statusEmpty,
  }
  return (
    <aside className="evidence-stack">
      <Card>
        <CardHeader>
          <CardTitle className="section-title">
            <Database size={15} />
            {text.lifecycle}
          </CardTitle>
        </CardHeader>
        <CardContent>
          <ol className="document-lifecycle">
            <li>
              <span>1</span>
              <div>
                <strong>{text.stepStore}</strong>
                <p>{text.stepStoreBody}</p>
              </div>
              <BadgeLabel text={text.available} />
            </li>
            <li>
              <span>2</span>
              <div>
                <strong>{text.stepEmbed}</strong>
                <p>{text.stepEmbedBody}</p>
              </div>
              <BadgeLabel text={configured ? text.configured : text.needsSetup} />
            </li>
            <li>
              <span>3</span>
              <div>
                <strong>{text.stepCite}</strong>
                <p>{text.stepCiteBody}</p>
              </div>
              <BadgeLabel text={health?.knowledge?.ready ? text.ready : text.needsIndex} />
            </li>
          </ol>
        </CardContent>
      </Card>
      <Card className="knowledge-readiness">
        <CardHeader>
          <CardTitle className="section-title">{text.readiness}</CardTitle>
        </CardHeader>
        <CardContent>
          <p className="muted small">
            {health?.knowledge
              ? fill(text.searchable, {
                  count: health.knowledge.indexed_document_count,
                  status: readinessStatus[health.knowledge.status] || health.knowledge.status,
                })
              : text.readinessUnavailable}
          </p>
          {health?.knowledge && (
            <>
              <p className="field-help">
                {fill(text.dimensions, {
                  model: health.knowledge.embedding_model,
                  count: health.knowledge.embedding_dimensions,
                })}
              </p>
              <p className="field-help">
                {!health.knowledge.enabled
                  ? text.retrievalDisabled
                  : !configured
                    ? text.configureProvider
                    : health.knowledge.ready
                      ? text.passagesReady
                      : text.indexFirst}
              </p>
              <p className="field-help">
                {health.drafting?.credential_check_configured
                  ? text.credentialOn
                  : text.credentialOff}{" "}
                {text.readinessScope}
              </p>
            </>
          )}
        </CardContent>
      </Card>
      <div className="knowledge-note">
        <Info size={16} />
        <div>
          <strong>{text.noteTitle}</strong>
          <p>{text.noteBody}</p>
          <span>
            {text.flowUpload} <ArrowRight size={13} />
            {text.flowIndex} <ArrowRight size={13} />
            {text.flowGround}
          </span>
        </div>
      </div>
    </aside>
  )
}

function BadgeLabel({ text }: { text: string }) {
  return <small className="lifecycle-state">{text}</small>
}
