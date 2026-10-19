import { useState } from "react"
import type { IntakeEvidenceData } from "@/lib/types"

function factValue(status: string, value: string | null | undefined, normalized: string | null | undefined) {
  if (status === "not_applicable") return "Not applicable"
  if (status === "conflicting") return `Conflicting: ${value || "Unknown"}`
  if (status === "unknown" || status === "missing" || value == null || value === "") return "Unknown"
  return normalized || value
}

function Screenshot({ url, filename }: { url: string; filename: string }) {
  const [failed, setFailed] = useState(false)
  return failed ? <span>Image unavailable: {filename}</span> : <img src={url} alt={filename} loading="lazy" onError={() => setFailed(true)} />
}

export function IntakeEvidence({ intake }: { intake: IntakeEvidenceData | null | undefined }) {
  if (!intake) return null
  return (
    <section className="intake-evidence" aria-labelledby="intake-heading">
      <h2 id="intake-heading">Customer intake</h2>
      <div lang="ar" dir="rtl">
        <h3>ملخص المشكلة</h3>
        <p>{intake.summary_ar}</p>
      </div>
      {intake.quality ? <p className="intake-quality">{intake.quality === "sufficient_context" ? "Sufficient context" : "Partial context"}</p> : null}
      <h3>Reported details</h3>
      <dl>
        {Object.entries(intake.facts).map(([key, fact]) => (
          <div key={key}>
            <dt>{key}</dt>
            <dd>
              <bdi dir="auto">{factValue(fact.status, fact.value, fact.normalized)}</bdi>
              {fact.evidence?.map((source, index) => (
                <p key={`${source.source_id}-${index}`} dir="auto">
                  <a href={`#intake-${source.kind}-${source.source_id}`}>{source.kind === "image" ? "Screenshot" : "Customer message"}</a>
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
            <li key={key}>{key}: Unknown</li>
          ))}
        </ul>
      ) : null}
      {intake.additional_issues.length ? (
        <>
          <h3>Additional issues</h3>
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
        <summary>Original conversation</summary>
        {intake.messages.map((message) => (
          <p key={message.id} id={`intake-message-${message.id}`} dir="auto" lang={message.language}>
            {message.text}
          </p>
        ))}
      </details>
    </section>
  )
}
