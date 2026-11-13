import { useState, type FormEvent } from "react"
import { Eye, EyeOff, KeyRound } from "lucide-react"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Input } from "@/components/ui/input"
import { setAdminSession } from "@/lib/admin-session"
import { adminApi } from "@/lib/api"
import { useCopy } from "@/lib/locale"
import { adminErrorMessage } from "./admin-errors"

// The token is shared, so the change history records every change under one name.
const ADMIN_NAME = "admin"

export function AdminUnlock() {
  const text = useCopy().models
  const [token, setToken] = useState("")
  const [visible, setVisible] = useState(false)
  const [busy, setBusy] = useState(false)
  const [error, setError] = useState("")
  const ready = token.trim() !== ""

  async function unlock(event: FormEvent) {
    event.preventDefault()
    if (!ready || busy) return
    setBusy(true)
    setError("")
    try {
      await adminApi.verify(token.trim())
      setAdminSession({ token: token.trim(), name: ADMIN_NAME })
    } catch (e) {
      setError(adminErrorMessage(e, text))
    } finally {
      setBusy(false)
    }
  }

  return (
    <Card className="admin-unlock">
      <CardHeader>
        <CardTitle className="section-title">
          <KeyRound size={18} />
          {text.unlockTitle}
        </CardTitle>
      </CardHeader>
      <CardContent>
        <p className="field-help">{text.unlockDescription}</p>
        <form className="admin-unlock-form" onSubmit={unlock}>
          <label className="model-field">
            {text.tokenLabel}
            <span className="secret-field" dir="ltr">
              <Input
                type={visible ? "text" : "password"}
                value={token}
                onChange={(e) => setToken(e.target.value)}
                autoComplete="current-password"
              />
              <button
                type="button"
                className="secret-toggle"
                aria-label={visible ? text.hideToken : text.showToken}
                aria-pressed={visible}
                onClick={() => setVisible((value) => !value)}
              >
                {visible ? <EyeOff size={16} /> : <Eye size={16} />}
              </button>
            </span>
          </label>
          {error && <p className="error-text" role="alert">{error}</p>}
          <Button type="submit" disabled={!ready || busy}>
            {busy ? text.unlocking : text.unlock}
          </Button>
        </form>
      </CardContent>
    </Card>
  )
}
