import type { FormEvent } from "react"
import { Button } from "@workspace/ui/components/button"
import type { IntakeCopy } from "./copy"

export function MessageComposer({
  copy,
  value,
  disabled,
  onChange,
  onSubmit,
}: {
  copy: IntakeCopy
  value: string
  disabled: boolean
  onChange: (value: string) => void
  onSubmit: () => void
}) {
  function submit(event?: FormEvent) {
    event?.preventDefault()
    if (!disabled) onSubmit()
  }

  return (
    <form className="intake-composer" onSubmit={submit}>
      <label className="intake-label" htmlFor="intake-message">
        {copy.message}
      </label>
      <textarea
        id="intake-message"
        name="message"
        dir="auto"
        rows={3}
        value={value}
        disabled={disabled}
        onChange={(event) => onChange(event.target.value)}
        onCompositionStart={(event) => {
          event.currentTarget.dataset.composing = "true"
        }}
        onCompositionEnd={(event) => {
          delete event.currentTarget.dataset.composing
        }}
        onKeyDown={(event) => {
          if (event.key !== "Enter" || event.shiftKey || event.currentTarget.dataset.composing === "true") return
          event.preventDefault()
          submit()
        }}
      />
      <Button type="submit" disabled={disabled}>
        {copy.send}
      </Button>
    </form>
  )
}
