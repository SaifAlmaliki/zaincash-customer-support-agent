import {
  useEffect,
  useMemo,
  useRef,
  useState,
  useSyncExternalStore,
} from "react"
import { Button } from "@workspace/ui/components/button"
import { AgentChat, type AgentMessage } from "@/components/ui/agent-chat"
import { quietButton, solidButton } from "./buttons"
import { PhoneGate } from "./PhoneGate"
import { ReceiptPanel } from "./ReceiptPanel"
import { ReviewPanel } from "./ReviewPanel"
import { OwnedImage } from "./OwnedImage"
import { QuestionExtras } from "./QuestionExtras"
import { activityText, composerHint } from "./composer"
import { copy } from "./copy"
import type { IntakeController } from "./controller"
import { useIntakeUploads } from "./useIntakeUploads"
import type { AnswerTo, Language } from "./types"
import "./intake.css"

export function IntakePage({ controller }: { controller: IntakeController }) {
  const snapshot = useSyncExternalStore(
    controller.subscribe,
    controller.getSnapshot
  )
  const session = snapshot.session
  const [selectedLocale, setLocale] = useState<Language | null>(null)
  const locale = selectedLocale ?? session?.language ?? "ar"
  const direction = locale === "ar" ? "rtl" : "ltr"
  const [draft, setDraft] = useState("")
  const { previews, selectFiles, clearPreviews } = useIntakeUploads(controller)
  const [confirmNew, setConfirmNew] = useState(false)
  const [confirmChange, setConfirmChange] = useState(false)
  const reviewHeading = useRef<HTMLHeadingElement | null>(null)
  const reviewRequest = useRef(false)
  const text = copy[locale]
  const credentials = controller.access()
  const needsPhone = snapshot.needsPhone
  const latestAssistant = session?.messages
    .filter((message) => message.role === "assistant")
    .at(-1)

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

  const unsent =
    session?.attachments.filter((item) => !item.removed && !item.message_id) ??
    []
  const awaitingResend = Boolean(snapshot.outgoing) && !snapshot.busy
  const canSend =
    Boolean(
      session &&
      session.phase !== "submitted" &&
      (draft.trim() || unsent.length)
    ) &&
    !snapshot.busy &&
    !awaitingResend &&
    session?.turn_status !== "processing"
  const hasContent = Boolean(
    session?.messages.length ||
    session?.attachments.some((item) => !item.removed)
  )
  const inProgress = hasContent && session?.phase !== "submitted"
  const pending = session?.pending_question ?? null
  const interactive = Boolean(
    pending &&
    session?.phase === "collecting" &&
    session.turn_status === "idle" &&
    !snapshot.busy &&
    !awaitingResend
  )
  const hint = composerHint(interactive && pending ? pending.answer_kind : null, text)
  const outgoing = snapshot.outgoing
  const showOutgoing = Boolean(
    outgoing?.text &&
    session &&
    session.phase !== "submitted" &&
    session.revision === outgoing.expected_revision
  )
  const outgoingFailed = showOutgoing && !snapshot.busy && Boolean(snapshot.error)
  const typing =
    (snapshot.busy && (snapshot.activity === "message" || snapshot.activity === "ask")) ||
    session?.turn_status === "processing"

  function changeNumber() {
    setConfirmChange(false)
    setConfirmNew(false)
    setDraft("")
    clearPreviews()
    setLocale(locale) // keep the language the customer chose
    void controller.changeNumber()
  }

  const showReview = Boolean(
    session?.review &&
    !session.receipt &&
    !snapshot.busy &&
    session.turn_status === "idle"
  )
  const attachingDisabled =
    snapshot.busy ||
    session?.turn_status === "processing" ||
    session?.phase === "submitted"

  const chatMessages = useMemo<AgentMessage[]>(() => {
    const history = session?.messages ?? []
    const items: AgentMessage[] =
      !history.length && !session?.review && !session?.receipt
        ? [
            {
              id: "welcome",
              role: "assistant",
              parts: [{ type: "text", text: text.empty }],
            },
          ]
        : history.map((message) => ({
            id: message.id,
            role: message.role,
            parts: [{ type: "text" as const, text: message.text }],
          }))
    if (showOutgoing && outgoing) {
      items.push({ id: "outgoing", role: "user", pending: !outgoingFailed, parts: [{ type: "text", text: outgoing.text }] })
    }
    if (typing) items.push({ id: "typing", role: "assistant", parts: [{ type: "typing", label: text.typing }] })
    return items
  }, [session?.messages, session?.receipt, session?.review, text.empty, text.typing, showOutgoing, outgoing, outgoingFailed, typing])

  const failure =
    snapshot.error || session?.turn_status === "retryable_failure"
      ? locale === "ar"
        ? text.updateError
        : snapshot.error || text.updateError
      : null

  async function chooseLanguage(next: Language) {
    setLocale(next)
    if (session?.phase === "review_ready" && session.review) {
      reviewRequest.current = true
      await controller.requestReview(
        session.review.quality !== "sufficient_context",
        next
      )
    }
  }

  async function send(content: string) {
    if (!canSend) return
    const attachmentIds = unsent.map((item) => item.id)
    setDraft("")
    await controller.send(content, locale, attachmentIds)
    const after = controller.getSnapshot()
    if (after.error && !after.outgoing) {
      setDraft((current) => current || content)
      return
    }
    if (!after.error) {
      clearPreviews()
      document.getElementById("intake-message")?.focus()
    }
  }

  function answer(label: string, answerTo: AnswerTo) {
    void controller.send(label, locale, [], answerTo)
  }

  const threadFooter = (
    <>
      {session?.receipt ? (
        <ReceiptPanel
          receipt={session.receipt}
          customerPhone={session.customer_phone}
          copy={text}
        />
      ) : null}
      {showReview && session?.review ? (
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
      ) : null}
    </>
  )

  const statusText = activityText(snapshot.activity, snapshot.busy, session?.turn_status === "processing", text)
  const showRefresh =
    session?.turn_status === "processing" || snapshot.pollingExhausted
  const showRetry =
    session?.turn_status === "retryable_failure" || Boolean(snapshot.error)
  const showReviewNow = Boolean(session && !session.review && !session.receipt)

  return (
    <div className="intake-shell" dir={direction} lang={locale}>
      <div className="intake-frame">
        <header className="intake-header">
          <div className="intake-brand">
            <span className="intake-mark" aria-hidden="true" />
            <p className="intake-title">{text.title}</p>
          </div>
          <div className="intake-header-actions">
            {needsPhone ? null : (
              <>
                {showReviewNow && hasContent ? (
                  <Button
                    type="button"
                    variant="outline"
                    size="sm"
                    className={quietButton}
                    disabled={snapshot.busy}
                    onClick={() => {
                      reviewRequest.current = true
                      void controller.requestReview(true, locale)
                    }}
                  >
                    {text.reviewNow}
                  </Button>
                ) : null}
                {showRefresh ? (
                  <Button
                    type="button"
                    variant="outline"
                    size="sm"
                    className={quietButton}
                    onClick={() => void controller.refresh()}
                  >
                    {text.refresh}
                  </Button>
                ) : null}
                {showRetry ? (
                  <Button
                    type="button"
                    variant="outline"
                    size="sm"
                    className={quietButton}
                    onClick={() => void controller.retry()}
                  >
                    {text.retry}
                  </Button>
                ) : null}
                <Button
                  type="button"
                  variant="outline"
                  size="sm"
                  className={quietButton}
                  onClick={() =>
                    hasContent
                      ? setConfirmNew(true)
                      : void controller.startNew(locale)
                  }
                >
                  {text.startNew}
                </Button>
              </>
            )}
            {session ? (
              <div
                className="intake-profile"
                role="group"
                aria-label={text.profileLabel}
              >
                <span className="intake-muted">{text.profileLabel}</span>
                <bdi dir="ltr" className="intake-profile-phone">
                  {session.customer_phone}
                </bdi>
                <Button
                  type="button"
                  variant="outline"
                  size="sm"
                  className={quietButton}
                  onClick={() =>
                    inProgress ? setConfirmChange(true) : changeNumber()
                  }
                >
                  {text.changeNumber}
                </Button>
              </div>
            ) : null}
            <div
              className="lang-toggle"
              role="group"
              aria-label={text.language}
            >
              <Button
                type="button"
                size="sm"
                variant={locale === "ar" ? "default" : "ghost"}
                data-locale="ar"
                aria-pressed={locale === "ar"}
                aria-label={text.arabic}
                className={locale === "ar" ? solidButton : "text-foreground"}
                onClick={() => void chooseLanguage("ar")}
              >
                ع
              </Button>
              <Button
                type="button"
                size="sm"
                variant={locale === "en" ? "default" : "ghost"}
                data-locale="en"
                aria-pressed={locale === "en"}
                aria-label={text.english}
                className={locale === "en" ? solidButton : "text-foreground"}
                onClick={() => void chooseLanguage("en")}
              >
                EN
              </Button>
            </div>
          </div>
        </header>
        {confirmNew ? (
          <div
            className="intake-confirm"
            role="dialog"
            aria-label={text.startNew}
          >
            <p>{text.confirmNewBody}</p>
            <div className="intake-actions">
              <Button
                type="button"
                className={solidButton}
                onClick={() => {
                  setConfirmNew(false)
                  setDraft("")
                  void controller.startNew(locale)
                }}
              >
                {text.confirmNew}
              </Button>
              <Button
                type="button"
                variant="outline"
                className={quietButton}
                onClick={() => setConfirmNew(false)}
              >
                {text.cancel}
              </Button>
            </div>
          </div>
        ) : null}
        {confirmChange ? (
          <div
            className="intake-confirm"
            role="dialog"
            aria-label={text.changeNumber}
          >
            <p>{text.confirmChangeBody}</p>
            <div className="intake-actions">
              <Button
                type="button"
                className={solidButton}
                onClick={changeNumber}
              >
                {text.confirmChange}
              </Button>
              <Button
                type="button"
                variant="outline"
                className={quietButton}
                onClick={() => setConfirmChange(false)}
              >
                {text.cancel}
              </Button>
            </div>
          </div>
        ) : null}
        <p className="intake-announce" aria-live="polite">
          {latestAssistant?.text ?? ""}
        </p>
        <main className="intake-chat">
          {needsPhone ? (
            <PhoneGate
              copy={text}
              busy={snapshot.busy}
              serverError={snapshot.phoneError}
              onSubmit={(phone) => void controller.initialize(locale, phone)}
            />
          ) : (
            <>
                <input
                  id="intake-shots"
                  className="intake-file"
                  type="file"
                  accept="image/png,image/jpeg,image/webp"
                  multiple
                  disabled={attachingDisabled}
                  onChange={(event) => {
                    const picked = event.target.files
                    if (picked?.length) void selectFiles(Array.from(picked))
                    event.target.value = ""
                  }}
                />
                <AgentChat
                  messages={chatMessages}
                  status="ready"
                  placeholder={hint.placeholder}
                  inputMode={hint.inputMode}
                  inputLabel={text.message}
                  inputId="intake-message"
                  sendLabel={text.send}
                  sendDisabled={!canSend}
                  allowEmptySend={unsent.length > 0}
                  hideComposer={session?.phase === "submitted"}
                  conversationLabel={text.conversation}
                  speakers={{ user: text.you, assistant: text.assistant }}
                  value={draft}
                  onValueChange={setDraft}
                  onSend={(message) => void send(message.content)}
                  error={
                    failure ? { title: text.errorTitle, message: failure } : undefined
                  }
                  attachments={{
                    attachInputId: "intake-shots",
                    attachLabel: text.attach,
                    removeLabel: text.remove,
                    disabled: Boolean(attachingDisabled),
                    images: previews.map((preview) => ({
                      id: preview.id,
                      filename: preview.name,
                      url: preview.url,
                    })),
                    files: unsent.map((item) => ({
                      id: item.id,
                      filename: item.filename,
                      size: item.size,
                    })),
                    onRemoveFile: (attachmentId) =>
                      void controller.remove(attachmentId).catch(() => undefined),
                  }}
                  renderAfter={(message) => {
                    if (message.id === "outgoing") {
                      return outgoingFailed ? (
                        <div className="intake-outgoing-failed">
                          <span>{text.notSent}</span>
                          <Button type="button" variant="outline" size="sm" className={quietButton} onClick={() => void controller.retry()}>
                            {text.resend}
                          </Button>
                        </div>
                      ) : null
                    }
                    if (pending && message.id === pending.message_id && message.role === "assistant") {
                      return (
                        <QuestionExtras
                          question={pending}
                          copy={text}
                          interactive={interactive}
                          attachInputId="intake-shots"
                          attachDisabled={Boolean(attachingDisabled)}
                          onAnswer={answer}
                        />
                      )
                    }
                    const source = session?.messages.find(
                      (item) => item.id === message.id
                    )
                    if (!source || message.role !== "user") return null
                    const shots = session?.attachments.filter(
                      (item) =>
                        !item.removed && source.attachment_ids.includes(item.id)
                    )
                    if (!shots?.length) return null
                    return (
                      <div className="intake-inline-shot is-user">
                        {shots.map((attachment) => (
                          <OwnedImage
                            key={attachment.id}
                            attachment={attachment}
                            credentials={credentials}
                            api={controller.transport()}
                            alt={attachment.filename}
                            unavailable={text.imageUnavailable}
                          />
                        ))}
                      </div>
                    )
                  }}
                  threadFooter={threadFooter}
                  toolbar={
                    previews.length ||
                    statusText ||
                    snapshot.resumeUnavailable ||
                    showReview ? (
                      <>
                        {previews.map((preview) => (
                          <progress
                            key={preview.id}
                            className="intake-progress"
                            value={snapshot.uploads[preview.id] ?? 0}
                            max={1}
                            aria-label={`${text.uploadProgress} ${preview.name}`}
                          />
                        ))}
                        {statusText ? (
                          <p role="status" className="intake-typing">
                            {statusText}
                          </p>
                        ) : null}
                        {snapshot.resumeUnavailable ? (
                          <p className="intake-muted">{text.resumeUnavailable}</p>
                        ) : null}
                        {showReview ? (
                          <div className="intake-actions">
                            <Button
                              type="button"
                              variant="outline"
                              className={quietButton}
                              disabled={snapshot.busy}
                              onClick={() => {
                                document.getElementById("intake-message")?.focus()
                              }}
                            >
                              {text.continueChat}
                            </Button>
                            <Button
                              type="button"
                              className={solidButton}
                              disabled={snapshot.busy}
                              onClick={() => void controller.submit()}
                            >
                              {text.submit}
                            </Button>
                          </div>
                        ) : null}
                      </>
                    ) : undefined
                  }
                />
            </>
          )}
        </main>
      </div>
    </div>
  )
}
