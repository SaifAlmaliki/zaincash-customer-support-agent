import type { IntakeApi } from "./api"
import type { Attachment, Credentials } from "./types"
import { useEffect, useState } from "react"

export function OwnedImage({
  attachment,
  credentials,
  api,
  alt,
  unavailable,
}: {
  attachment: Attachment
  credentials: Credentials | null
  api: IntakeApi
  alt: string
  unavailable: string
}) {
  const [url, setUrl] = useState<string | null>(null)
  const [failed, setFailed] = useState(false)
  const [shownId, setShownId] = useState(attachment.id)
  if (shownId !== attachment.id) {
    setShownId(attachment.id)
    setUrl(null)
    setFailed(false)
  }

  useEffect(() => {
    if (!credentials) return
    const controller = new AbortController()
    let objectUrl: string | null = null
    let active = true
    void api
      .image(credentials, attachment.id, controller.signal)
      .then((blob) => {
        if (!active) return
        objectUrl = URL.createObjectURL(blob)
        setUrl(objectUrl)
      })
      .catch((error: unknown) => {
        if (!active || (error instanceof DOMException && error.name === "AbortError")) return
        setFailed(true)
      })
    return () => {
      active = false
      controller.abort()
      if (objectUrl) URL.revokeObjectURL(objectUrl)
    }
  }, [api, attachment.id, credentials])

  if (failed) return <p className="intake-muted">{unavailable}</p>
  if (!url) return <p className="intake-muted">{alt}</p>
  return <img src={url} alt={alt} />
}
