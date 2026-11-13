import { useState } from "react"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import type { IntakeEvidenceData } from "@/lib/types"
import { humanize } from "@/lib/format"
import { getCopy, useCopy } from "@/lib/locale"

function factValue(status: string, value: string | null | undefined, normalized: string | null | undefined) {
  const intake = getCopy().intake
  if (status === "not_applicable") return intake.notApplicable
  if (status === "conflicting") return `${intake.conflicting}: ${value || intake.unknown}`
  if (status === "unknown" || status === "missing" || value == null || value === "") return intake.unknown
  return normalized || value
}

function Screenshot({ url, filename }: { url: string; filename: string }) {
  const [failed, setFailed] = useState(false)
  const copy = useCopy()
  return failed ? <span>{copy.intake.imageUnavailable}: {filename}</span> : <img src={url} alt={filename} loading="lazy" onError={() => setFailed(true)} />
}

export function ReportedDetails({ intake }: { intake: IntakeEvidenceData | null | undefined }) {
  const text = useCopy().intake
  if (!intake || Object.keys(intake.facts).length === 0) return null
  const labels = text.fields as Record<string, string>
  return (
    <Card className="compare-card">
      <CardHeader>
        <CardTitle className="section-title">{text.details}</CardTitle>
      </CardHeader>
      <CardContent>
        <dl className="compare-rows">
          {Object.entries(intake.facts).map(([key, fact]) => (
            <div key={key}>
              <dt>{labels[key] || humanize(key)}</dt>
              <dd><bdi dir="auto">{factValue(fact.status, fact.value, fact.normalized)}</bdi></dd>
            </div>
          ))}
        </dl>
      </CardContent>
    </Card>
  )
}

export function IntakeEvidence({ intake, omitDetails = false }: { intake: IntakeEvidenceData | null | undefined, omitDetails?: boolean }) {
  const copy = useCopy()
  const text = copy.intake
  if (!intake) return null
  return (
    <section className="intake-evidence" aria-labelledby="intake-heading">
      <h2 id="intake-heading">{text.heading}</h2>
      <div lang="ar" dir="rtl">
        <h3>{text.summary}</h3>
        <p>{intake.summary_ar}</p>
      </div>
      {intake.quality ? <p className="intake-quality">{intake.quality === "sufficient_context" ? text.sufficient : text.partial}</p> : null}
      {omitDetails ? null : <ReportedDetails intake={intake} />}
      {intake.unknown_keys.length ? (
        <ul>
          {intake.unknown_keys.map((key) => (
            <li key={key}>{key}: {text.unknown}</li>
          ))}
        </ul>
      ) : null}
      {intake.additional_issues.length ? (
        <>
          <h3>{text.issues}</h3>
          <ul>
            {intake.additional_issues.map((issue) => (
              <li key={issue.key} dir="auto">
                {issue.key}: {factValue(issue.status, issue.value, issue.normalized)}
              </li>
            ))}
          </ul>
        </>
      ) : null}
      {intake.attachments.length ? (
        <ul className="intake-shots">
          {intake.attachments.map((attachment) => (
            <li key={attachment.id} id={`intake-image-${attachment.id}`}>
              <a href={attachment.download_url}>
                <Screenshot url={attachment.download_url} filename={attachment.filename} />
              </a>
            </li>
          ))}
        </ul>
      ) : null}
      <details>
        <summary>{text.conversation}</summary>
        {intake.messages.map((message) => (
          <p key={message.id} id={`intake-message-${message.id}`} dir="auto" lang={message.language}>
            {message.text}
          </p>
        ))}
      </details>
    </section>
  )
}
