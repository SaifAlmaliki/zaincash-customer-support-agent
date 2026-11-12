import { useState, type FormEvent } from "react"
import { KeyRound } from "lucide-react"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Input } from "@/components/ui/input"
import { setAdminSession } from "@/lib/admin-session"
import { adminApi } from "@/lib/api"
import { useCopy } from "@/lib/locale"
import { adminErrorMessage } from "./admin-errors"

export function AdminUnlock() {
  const text = useCopy().models
  const [name, setName] = useState("")
  const [token, setToken] = useState("")
  const [busy, setBusy] = useState(false)
  const [error, setError] = useState("")
  const ready = name.trim() !== "" && token.trim() !== ""

  async function unlock(event: FormEvent) {
    event.preventDefault()
    if (!ready || busy) return
    setBusy(true)
    setError("")
    try {
      await adminApi.verify(token.trim())
      setAdminSession({ token: token.trim(), name: name.trim() })
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
            {text.nameLabel}
            <Input value={name} onChange={(e) => setName(e.target.value)} autoComplete="name" maxLength={64} />
          </label>
          <label className="model-field">
            {text.tokenLabel}
            <Input type="password" value={token} onChange={(e) => setToken(e.target.value)} autoComplete="current-password" />
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
