import { Button } from "@workspace/ui/components/button"
import type { IntakeApi } from "./api"
import { quietButton, solidButton } from "./buttons"
import type { IntakeCopy } from "./copy"
import type { Attachment, Credentials, CustomerReview, Fact } from "./types"
import { OwnedImage } from "./OwnedImage"

function factText(fact: Fact, copy: IntakeCopy) {
  if (fact.status === "unknown" || fact.status === "missing") return copy.unknown
  if (fact.status === "not_applicable") return copy.notApplicable
  if (fact.status === "conflicting") return `${copy.conflicting}: ${fact.value || copy.unknown}`
  if (fact.normalized === "yes") return copy.choiceYes
  if (fact.normalized === "no") return copy.choiceNo
  return fact.normalized || fact.value || copy.unknown
}

function statusSuffix(fact: Fact, copy: IntakeCopy) {
  if (fact.status === "known") return ""
  if (fact.status === "conflicting") return ` (${copy.conflicting})`
  if (fact.status === "not_applicable") return ` (${copy.notApplicable})`
  return ` (${copy.unknown})`
}

export function ReviewPanel({
  review,
  attachments,
  credentials,
  api,
  copy,
  headingRef,
  askable,
  busy,
  submitting,
  onAsk,
  onSubmit,
  onContinue,
}: {
  review: CustomerReview
  attachments: Attachment[]
  credentials: Credentials | null
  api: IntakeApi
  copy: IntakeCopy
  headingRef: (node: HTMLHeadingElement | null) => void
  askable: string[]
  busy: boolean
  submitting: boolean
  onAsk: (key: string) => void
  onSubmit: () => void
  onContinue: () => void
}) {
  const selected = attachments.filter((item) => !item.removed && review.attachment_ids.includes(item.id))
  const facts = Object.values(review.facts).filter((fact) => fact.key !== "customer_phone")
  const known = facts.filter((fact) => fact.status === "known" || fact.status === "not_applicable")
  const missing = facts.filter((fact) => fact.status === "missing" || fact.status === "conflicting")
  const unknown = facts.filter((fact) => fact.status === "unknown")
  const label = (key: string) => copy.fieldLabels[key] || key
  const banner = review.quality === "sufficient_context"
    ? null
    : missing.length
      ? copy.missingList.replace("{items}", missing.map((fact) => label(fact.key)).join(copy.listSeparator))
      : copy.partial
  return (
    <section className="intake-review" aria-labelledby="intake-review-heading">
      <h2 id="intake-review-heading" tabIndex={-1} ref={headingRef}>
        {copy.review}
      </h2>
      {review.quality === "sufficient_context" ? (
        <p className="intake-complete">{copy.complete}</p>
      ) : (
        <p className="intake-partial">{banner}</p>
      )}
      <p dir="auto" lang={review.language}>
        {review.text}
      </p>
      {known.length ? (
        <>
          <h3>{copy.groupKnown}</h3>
          <dl>
            {known.map((fact) => (
              <div key={fact.key}>
                <dt>{label(fact.key)}</dt>
                <dd>
                  <bdi dir="auto">{factText(fact, copy)}</bdi>
                </dd>
              </div>
            ))}
          </dl>
        </>
      ) : null}
      {missing.length ? (
        <>
          <h3>{copy.groupMissing}</h3>
          <ul className="intake-gaps">
            {missing.map((fact) => (
              <li key={fact.key}>
                <span>{label(fact.key)}</span>
                {fact.status === "conflicting" ? <bdi dir="auto">{factText(fact, copy)}</bdi> : null}
                {askable.includes(fact.key) ? (
                  <Button type="button" variant="outline" size="sm" className={quietButton} disabled={busy}
                    aria-label={`${copy.answer}: ${label(fact.key)}`} onClick={() => onAsk(fact.key)}>
                    {copy.answer}
                  </Button>
                ) : null}
              </li>
            ))}
          </ul>
        </>
      ) : null}
      {unknown.length ? (
        <>
          <h3>{copy.groupUnknown}</h3>
          <ul className="intake-gaps">
            {unknown.map((fact) => (
              <li key={fact.key}>
                <span>{label(fact.key)}</span>
                <span className="intake-muted">{copy.unknown}</span>
                {askable.includes(fact.key) ? (
                  <Button type="button" variant="outline" size="sm" className={quietButton} disabled={busy}
                    aria-label={`${copy.answerRemembered}: ${label(fact.key)}`} onClick={() => onAsk(fact.key)}>
                    {copy.answerRemembered}
                  </Button>
                ) : null}
              </li>
            ))}
          </ul>
        </>
      ) : null}
      {review.additional_issues.length ? (
        <>
          <h3>{copy.issues}</h3>
          <ul>
            {review.additional_issues.map((issue) => (
              <li key={issue.key} dir="auto">
                {issue.value || copy.unknown}
                {statusSuffix(issue, copy)}
              </li>
            ))}
          </ul>
        </>
      ) : null}
      {selected.length ? (
        <div>
          <h3>{copy.screenshots}</h3>
          {selected.map((attachment) => (
            <OwnedImage
              key={attachment.id}
              attachment={attachment}
              credentials={credentials}
              api={api}
              alt={attachment.filename}
              unavailable={copy.imageUnavailable}
            />
          ))}
        </div>
      ) : null}
      <div className="intake-actions intake-review-actions">
        <Button type="button" variant="outline" className={quietButton} disabled={busy} onClick={onContinue}>
          {copy.continueChat}
        </Button>
        <Button type="button" className={solidButton} disabled={busy} aria-busy={submitting} onClick={onSubmit}>
          {submitting ? <span className="intake-spinner" aria-hidden="true" /> : null}
          {copy.submit}
        </Button>
      </div>
    </section>
  )
}
