import { useState, type FormEvent } from "react"
import { Button } from "@workspace/ui/components/button"
import { solidButton } from "./buttons"
import type { IntakeCopy } from "./copy"
import { normalizeCustomerPhone } from "./phone"

export function PhoneGate({
  copy,
  busy,
  serverError,
  onSubmit,
}: {
  copy: IntakeCopy
  busy: boolean
  serverError: "invalid" | "failed" | null
  onSubmit: (phone: string) => void
}) {
  const [value, setValue] = useState("")
  const [checked, setChecked] = useState(false)
  const [sent, setSent] = useState<string | null>(null)
  const phone = normalizeCustomerPhone(value)
  const serverMessage =
    sent === value && serverError
      ? serverError === "invalid" ? copy.phoneInvalid : copy.updateError
      : null
  const error = checked && !phone ? copy.phoneInvalid : serverMessage

  function submit(event: FormEvent) {
    event.preventDefault()
    setChecked(true)
    if (!phone || busy) return
    setSent(value)
    onSubmit(phone)
  }

  return (
    <form className="intake-gate" onSubmit={submit} noValidate>
      <h1 className="intake-gate-title">{copy.phoneTitle}</h1>
      <p className="intake-muted">{copy.phoneHelp}</p>
      <input
        id="intake-phone"
        className="intake-gate-input"
        dir="ltr"
        inputMode="tel"
        autoComplete="tel"
        autoFocus
        placeholder="07XXXXXXXXX"
        aria-label={copy.phoneLabel}
        value={value}
        aria-invalid={Boolean(error)}
        aria-describedby={error ? "intake-phone-error" : undefined}
        onChange={(event) => {
          setValue(event.target.value)
          setChecked(false)
        }}
      />
      {error ? (
        <p id="intake-phone-error" role="alert" className="intake-gate-error">
          {error}
        </p>
      ) : null}
      <Button type="submit" className={solidButton} disabled={busy}>
        {copy.phoneContinue}
      </Button>
    </form>
  )
}
