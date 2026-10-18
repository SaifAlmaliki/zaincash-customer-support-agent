import type { IntakeApi } from "./api"
import type { IntakeCopy } from "./copy"
import type { Attachment, Credentials, CustomerReview } from "./types"
import { OwnedImage } from "./OwnedImage"

function factText(review: CustomerReview, key: string, unknown: string) {
  const fact = review.facts[key]
  if (!fact || fact.status === "unknown" || fact.status === "missing") return unknown
  if (fact.status === "conflicting") return fact.normalized || fact.value || unknown
  return fact.normalized || fact.value || unknown
}

export function ReviewPanel({
  review,
  attachments,
  credentials,
  api,
  copy,
  headingRef,
}: {
  review: CustomerReview
  attachments: Attachment[]
  credentials: Credentials | null
  api: IntakeApi
  copy: IntakeCopy
  headingRef: (node: HTMLHeadingElement | null) => void
}) {
  const selected = attachments.filter((item) => !item.removed && review.attachment_ids.includes(item.id))
  const keys = Object.keys(review.facts)
  return (
    <section className="intake-review" aria-labelledby="intake-review-heading">
      <h2 id="intake-review-heading" tabIndex={-1} ref={headingRef}>
        {copy.review}
      </h2>
      {review.quality === "partial_context" ? <p className="intake-partial">{copy.partial}</p> : null}
      <p dir="auto" lang={review.language}>
        {review.text}
      </p>
      <h3>{copy.facts}</h3>
      <dl>
        {keys.map((key) => (
          <div key={key}>
            <dt>{key}</dt>
            <dd>
              <bdi dir="ltr">{factText(review, key, copy.unknown)}</bdi>
            </dd>
          </div>
        ))}
      </dl>
      {review.unknown_keys.length ? (
        <ul>
          {review.unknown_keys.map((key) => (
            <li key={key}>
              {key}: {copy.unknown}
            </li>
          ))}
        </ul>
      ) : null}
      {review.additional_issues.length ? (
        <>
          <h3>{copy.issues}</h3>
          <ul>
            {review.additional_issues.map((issue) => (
              <li key={issue.key} dir="auto">
                {issue.key}: {issue.value || copy.unknown}
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
    </section>
  )
}
