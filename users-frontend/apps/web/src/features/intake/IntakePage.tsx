import { useEffect, useRef, useState, useSyncExternalStore } from "react"
import { Button } from "@workspace/ui/components/button"
import { ChatTranscript } from "./ChatTranscript"
import { MessageComposer } from "./MessageComposer"
import { ReceiptPanel } from "./ReceiptPanel"
import { ReviewPanel } from "./ReviewPanel"
import { ScreenshotPicker } from "./ScreenshotPicker"
import { copy } from "./copy"
import type { IntakeController } from "./controller"
import type { Language } from "./types"
import "./intake.css"

export function IntakePage({ controller }: { controller: IntakeController }) {
  const snapshot = useSyncExternalStore(controller.subscribe, controller.getSnapshot)
  const session = snapshot.session
  const [selectedLocale, setLocale] = useState<Language | null>(null)
  const locale = selectedLocale ?? session?.language ?? "ar"
  const direction = locale === "ar" ? "rtl" : "ltr"
  const [draft, setDraft] = useState("")
  const [previews, setPreviews] = useState<{ name: string; url: string }[]>([])
  const [confirmNew, setConfirmNew] = useState(false)
  const reviewHeading = useRef<HTMLHeadingElement | null>(null)
  const reviewRequest = useRef(false)
  const previewUrls = useRef(new Set<string>())
  const text = copy[locale]
  const credentials = controller.access()
  const latestAssistant = session?.messages.filter((message) => message.role === "assistant").at(-1)

  useEffect(() => {
    if (!controller.getSnapshot().session) void controller.initialize("ar")
  }, [controller])

  useEffect(() => {
    document.documentElement.lang = locale
    document.documentElement.dir = direction
    document.title = text.title
  }, [direction, locale, text.title])

  useEffect(() => {
    if (reviewRequest.current && session?.review) {
      reviewHeading.current?.focus()
      reviewRequest.current = false
    }
  }, [session?.review])

  useEffect(() => {
    const urls = previewUrls.current
    return () => {
      for (const url of urls) URL.revokeObjectURL(url)
    }
  }, [])

  const unsent = session?.attachments.filter((item) => !item.removed && !item.message_id) ?? []
  const canSend = Boolean(session && session.phase !== "submitted" && (draft.trim() || unsent.length)) && !snapshot.busy && session?.turn_status !== "processing"
  const hasContent = Boolean(session?.messages.length || session?.attachments.some((item) => !item.removed))

  async function chooseLanguage(next: Language) {
    setLocale(next)
    if (session?.phase === "review_ready" && session.review) {
      reviewRequest.current = true
      await controller.requestReview(session.review.quality !== "sufficient_context", next)
    }
  }

  async function send() {
    if (!canSend) return
    const attachmentIds = unsent.map((item) => item.id)
    const body = draft
    await controller.send(body, locale, attachmentIds)
    if (!controller.getSnapshot().error) {
      setDraft((current) => current === body ? "" : current)
      setPreviews((current) => {
        for (const preview of current) URL.revokeObjectURL(preview.url)
        return []
      })
      document.getElementById("intake-message")?.focus()
    }
  }

  async function selectFiles(files: File[]) {
    const local = files.map((file) => ({ name: file.name, url: URL.createObjectURL(file) }))
    for (const item of local) previewUrls.current.add(item.url)
    setPreviews((current) => [...current, ...local])
    for (const file of files) {
      try {
        await controller.upload(file)
        setPreviews((current) => {
          const match = current.find((item) => item.name === file.name)
          if (match) URL.revokeObjectURL(match.url)
          return current.filter((item) => item.name !== file.name)
        })
      } catch {
        setPreviews((current) => {
          const match = current.find((item) => item.name === file.name)
          if (match) URL.revokeObjectURL(match.url)
          return current.filter((item) => item.name !== file.name)
        })
        break
      }
    }
  }

  return (
    <div className="intake-shell" dir={direction} lang={locale}>
      <header className="intake-header">
        <div className="intake-brand">
          <span className="intake-mark" aria-hidden="true" />
          <div>
            <p className="intake-title">{text.title}</p>
            <p className="intake-subtitle">{text.subtitle}</p>
          </div>
        </div>
        </header>
      <div className="lang-toggle" role="group" aria-label={text.language}>
        <button type="button" data-locale="ar" aria-pressed={locale === "ar"} aria-label={text.arabic} onClick={() => void chooseLanguage("ar")}>
          ع
        </button>
        <button type="button" data-locale="en" aria-pressed={locale === "en"} aria-label={text.english} onClick={() => void chooseLanguage("en")}>
          EN
        </button>
      </div>
      <main className="intake-layout">
        <div className="intake-conversation">
          {session ? (
            <ChatTranscript messages={session.messages} copy={text} announcedId={latestAssistant?.id ?? null} />
          ) : (
            <p className="intake-muted">{text.empty}</p>
          )}
          {session && !session.messages.length ? <p className="intake-muted">{text.empty}</p> : null}
          {session?.phase !== "submitted" ? <><ScreenshotPicker
            copy={text}
            attachments={session?.attachments ?? []}
            previews={previews}
            progress={snapshot.uploads}
            disabled={snapshot.busy || session?.turn_status === "processing"}
            onSelect={(files) => void selectFiles(files)}
            onRemove={(attachmentId) => void controller.remove(attachmentId).catch(() => undefined)}
            credentials={credentials}
            api={controller.transport()}
          />
          <MessageComposer copy={text} value={draft} sendDisabled={!canSend} onChange={setDraft} onSubmit={() => void send()} /></> : null}
        </div>
        <aside className="intake-side">
          {snapshot.busy || session?.turn_status === "processing" ? <p role="status">{text.processing}</p> : null}
          {snapshot.error || session?.turn_status === "retryable_failure" ? (
            <p role="alert" className="intake-alert" dir="auto">
              {locale === "ar" ? text.updateError : snapshot.error || text.updateError}
            </p>
          ) : null}
          {snapshot.resumeUnavailable ? <p className="intake-muted">{text.resumeUnavailable}</p> : null}
          {session?.receipt ? <ReceiptPanel receipt={session.receipt} copy={text} /> : null}
          {session?.review && !session.receipt && !snapshot.busy && session.turn_status === "idle" ? (
            <>
              <ReviewPanel
                review={session.review}
                attachments={session.attachments}
                credentials={credentials}
                api={controller.transport()}
                copy={text}
                headingRef={(node) => {
                  reviewHeading.current = node
                }}
              />
              <div className="intake-actions">
                <Button
                  type="button"
                  disabled={snapshot.busy}
                  onClick={() => {
                    document.getElementById("intake-message")?.focus()
                  }}
                >
                  {text.continueChat}
                </Button>
                <Button type="button" disabled={snapshot.busy} onClick={() => void controller.submit()}>
                  {text.submit}
                </Button>
              </div>
            </>
          ) : null}
          {session && !session.review && !session.receipt ? (
            <Button
              type="button"
              variant="outline"
              disabled={snapshot.busy || !hasContent}
              onClick={() => {
                reviewRequest.current = true
                void controller.requestReview(true, locale)
              }}
            >
              {text.reviewNow}
            </Button>
          ) : null}
          {session?.turn_status === "processing" || snapshot.pollingExhausted ? (
            <Button type="button" variant="outline" onClick={() => void controller.refresh()}>
              {text.refresh}
            </Button>
          ) : null}
          {session?.turn_status === "retryable_failure" || snapshot.error ? (
            <Button type="button" variant="outline" onClick={() => void controller.retry()}>
              {text.retry}
            </Button>
          ) : null}
          <Button type="button" variant="ghost" onClick={() => (hasContent ? setConfirmNew(true) : void controller.startNew(locale))}>
            {text.startNew}
          </Button>
          {confirmNew ? (
            <div role="dialog" aria-label={text.startNew}>
              <p>{text.confirmNewBody}</p>
              <Button
                type="button"
                onClick={() => {
                  setConfirmNew(false)
                  setDraft("")
                  void controller.startNew(locale)
                }}
              >
                {text.confirmNew}
              </Button>
              <Button type="button" variant="outline" onClick={() => setConfirmNew(false)}>
                {text.cancel}
              </Button>
            </div>
          ) : null}
        </aside>
      </main>
    </div>
  )
}
