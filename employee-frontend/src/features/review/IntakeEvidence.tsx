import { useState } from "react"
import type { IntakeEvidenceData } from "@/lib/types"
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

export function IntakeEvidence({ intake }: { intake: IntakeEvidenceData | null | undefined }) {
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
      <h3>{text.details}</h3>
      <dl>
        {Object.entries(intake.facts).map(([key, fact]) => (
          <div key={key}>
            <dt>{key}</dt>
            <dd>
              <bdi dir="auto">{factValue(fact.status, fact.value, fact.normalized)}</bdi>
              {fact.evidence?.map((source, index) => (
                <p key={`${source.source_id}-${index}`} dir="auto">
                  <a href={`#intake-${source.kind}-${source.source_id}`}>{source.kind === "image" ? text.screenshot : text.message}</a>
                  {": "}{source.quote}
                </p>
              ))}
            </dd>
          </div>
        ))}
      </dl>
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
