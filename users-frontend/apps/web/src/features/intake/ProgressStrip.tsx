import { useState } from "react"
import { Button } from "@workspace/ui/components/button"
import { quietButton } from "./buttons"
import type { IntakeCopy } from "./copy"
import type { ProgressItem } from "./types"

export function displayValue(item: ProgressItem, copy: IntakeCopy): string | null {
  if (item.display === "yes") return copy.choiceYes
  if (item.display === "no") return copy.choiceNo
  return item.display
}

function wideScreen() {
  return typeof window.matchMedia === "function" && window.matchMedia("(min-width: 721px)").matches
}

export function ProgressStrip({
  items,
  copy,
  reviewDisabled,
  onReviewNow,
}: {
  items: ProgressItem[]
  copy: IntakeCopy
  reviewDisabled: boolean
  onReviewNow: () => void
}) {
  const [open, setOpen] = useState(wideScreen)
  const required = items.filter((item) => item.tier === "required")
  const done = required.filter((item) => item.status === "known" || item.status === "not_applicable").length
  const label = copy.progressLabel.replace("{done}", String(done)).replace("{total}", String(required.length))
  return (
    <div className="intake-progress-strip">
      <div className="intake-progress-head">
        {items.length ? (
          <Button
            type="button"
            variant="ghost"
            size="sm"
            aria-expanded={open}
            aria-controls="intake-progress-list"
            onClick={() => setOpen((value) => !value)}
          >
            {label}
          </Button>
        ) : null}
        <Button type="button" variant="outline" size="sm" className={quietButton} disabled={reviewDisabled} onClick={onReviewNow}>
          {copy.reviewNow}
        </Button>
      </div>
      {open && items.length ? (
        <ul id="intake-progress-list" className="intake-progress-list" aria-label={label}>
          {items.map((item) => {
            const name = copy.fieldLabels[item.key] || item.key
            const value = displayValue(item, copy)
            const known = item.status === "known" || item.status === "not_applicable"
            const mark = known ? "✓" : item.status === "unknown" ? "–" : "○"
            const shown = known && value ? `${name} · ${value}` : item.status === "unknown" ? `${name} · ${copy.notKnown}` : name
            return (
              <li key={item.key} data-status={item.status} className={item.tier === "ask_once" ? "is-optional" : undefined}>
                <span aria-hidden="true" className="intake-progress-mark">{mark}</span>
                {shown}
                {!known && item.status !== "unknown" ? <span className="sr-only"> {copy.stillNeeded}</span> : null}
              </li>
            )
          })}
        </ul>
      ) : null}
    </div>
  )
}
