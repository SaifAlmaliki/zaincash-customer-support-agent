import { useEffect, useRef, useState } from "react"
import { Button } from "@workspace/ui/components/button"
import { quietButton, solidButton } from "./buttons"
import { answerKind, composerHint } from "./composer"
import type { IntakeCopy } from "./copy"
import type { AnswerTo, PendingQuestion, ProgressItem } from "./types"

export function displayValue(item: ProgressItem, copy: IntakeCopy): string | null {
  if (item.display === "yes") return copy.choiceYes
  if (item.display === "no") return copy.choiceNo
  return item.display
}

function wideScreen() {
  return typeof window.matchMedia === "function" && window.matchMedia("(min-width: 721px)").matches
}

function fillable(item: ProgressItem) {
  return item.status === "missing" || item.status === "unknown" || item.status === "conflicting"
}

export function ProgressStrip({
  items,
  copy,
  reviewDisabled,
  pending,
  onReviewNow,
  onFill,
}: {
  items: ProgressItem[]
  copy: IntakeCopy
  reviewDisabled: boolean
  pending: PendingQuestion | null
  onReviewNow: () => void
  onFill: (text: string, answerTo?: AnswerTo) => void
}) {
  const [open, setOpen] = useState(wideScreen)
  const [openKey, setOpenKey] = useState<string | null>(null)
  const required = items.filter((item) => item.tier === "required")
  const done = required.filter((item) => item.status === "known" || item.status === "not_applicable").length
  const label = copy.progressLabel.replace("{done}", String(done)).replace("{total}", String(required.length))
  const selected = items.find((item) => item.key === openKey && fillable(item)) ?? null
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
            const canFill = fillable(item)
            return (
              <li
                key={item.key}
                data-status={item.status}
                className={[item.tier === "ask_once" ? "is-optional" : "", canFill ? "is-fillable" : ""].filter(Boolean).join(" ") || undefined}
              >
                {canFill ? (
                  <button
                    type="button"
                    className="intake-progress-chip"
                    aria-expanded={openKey === item.key}
                    aria-haspopup="dialog"
                    disabled={reviewDisabled}
                    onClick={() => setOpenKey((current) => (current === item.key ? null : item.key))}
                  >
                    <span aria-hidden="true" className="intake-progress-mark">{mark}</span>
                    {shown}
                    {item.status !== "unknown" ? <span className="sr-only"> {copy.stillNeeded}</span> : null}
                  </button>
                ) : (
                  <>
                    <span aria-hidden="true" className="intake-progress-mark">{mark}</span>
                    {shown}
                  </>
                )}
              </li>
            )
          })}
        </ul>
      ) : null}
      {open && selected ? (
        <DetailDialog
          item={selected}
          copy={copy}
          pending={pending}
          disabled={reviewDisabled}
          onClose={() => setOpenKey(null)}
          onFill={onFill}
        />
      ) : null}
    </div>
  )
}

function DetailDialog({
  item,
  copy,
  pending,
  disabled,
  onClose,
  onFill,
}: {
  item: ProgressItem
  copy: IntakeCopy
  pending: PendingQuestion | null
  disabled: boolean
  onClose: () => void
  onFill: (text: string, answerTo?: AnswerTo) => void
}) {
  const kind = answerKind(item.key)
  const name = copy.fieldLabels[item.key] || item.key
  const hint = composerHint(kind === "yes_no" ? "text" : kind, copy)
  const [value, setValue] = useState("")
  const fieldRef = useRef<HTMLInputElement>(null)
  useEffect(() => {
    fieldRef.current?.focus()
  }, [item.key])

  function send(text: string, choice?: AnswerTo["choice"]) {
    const trimmed = text.trim()
    if (!trimmed) return
    if (choice && pending?.key === item.key && pending.choices.includes(choice)) {
      onFill(trimmed, { message_id: pending.message_id, key: pending.key, choice })
    } else {
      onFill(`${name}: ${trimmed}`)
    }
    onClose()
  }

  return (
    <form
      className="intake-detail-dialog"
      role="dialog"
      aria-label={name}
      onSubmit={(event) => {
        event.preventDefault()
        send(value)
      }}
      onKeyDown={(event) => {
        if (event.key === "Escape") onClose()
      }}
    >
      <p>{name}</p>
      {kind === "yes_no" ? (
        <div className="intake-detail-actions">
          <Button type="button" size="sm" className={solidButton} disabled={disabled} onClick={() => send(copy.choiceYes, "yes")}>
            {copy.choiceYes}
          </Button>
          <Button type="button" variant="outline" size="sm" className={quietButton} disabled={disabled} onClick={() => send(copy.choiceNo, "no")}>
            {copy.choiceNo}
          </Button>
          <Button type="button" variant="outline" size="sm" className={quietButton} disabled={disabled} onClick={() => send(copy.choiceUnknown, "unknown")}>
            {copy.choiceUnknown}
          </Button>
          <Button type="button" variant="ghost" size="sm" onClick={onClose}>
            {copy.cancel}
          </Button>
        </div>
      ) : (
        <>
          <input
            ref={fieldRef}
            className="intake-gate-input"
            value={value}
            dir={kind === "text" || kind === "date" ? "auto" : "ltr"}
            inputMode={hint.inputMode}
            placeholder={hint.placeholder}
            aria-label={name}
            autoComplete="off"
            disabled={disabled}
            onChange={(event) => setValue(event.target.value)}
          />
          <div className="intake-detail-actions">
            <Button type="submit" size="sm" className={solidButton} disabled={disabled || !value.trim()}>
              {copy.detailSave}
            </Button>
            <Button
              type="button"
              variant="outline"
              size="sm"
              className={quietButton}
              disabled={disabled}
              onClick={() => send(kind === "reference" ? copy.choiceNoReference : copy.choiceUnknown, "unknown")}
            >
              {kind === "reference" ? copy.choiceNoReference : copy.choiceUnknown}
            </Button>
            <Button type="button" variant="ghost" size="sm" onClick={onClose}>
              {copy.cancel}
            </Button>
          </div>
        </>
      )}
    </form>
  )
}
