# Intake Chat UI Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Turn the customer intake page into one centered chat column in the support-workspace palette, with the ticket summary and receipt inside the thread.

**Architecture:** Keep `IntakeController` and the intake API. `IntakePage` owns the column, header, status strip, and controller calls. `ChatTranscript` renders messages plus optional summary and receipt nodes. `MessageComposer` owns the rounded box and hosts the screenshot picker. `intake.css` scopes the light workspace palette to `.intake-shell`.

**Tech Stack:** Existing users-frontend Vite app, React 19, TypeScript, Vitest, Testing Library, the shared `Button`. No new packages.

**Spec:** `docs/superpowers/specs/2026-10-19-intake-chat-ui-design.md`

## Global Constraints

- Reshape the existing intake screen. Do not replace it with the sample `AgentChat` component.
- Do not add `components/ui/agent-chat.tsx`, and do not install `clsx` or `tailwind-merge` for this work.
- Do not change the backend, `IntakeController`, `api.ts`, `types.ts`, the employee frontend, or `ThemeProvider`.
- Page background `#f6f7f9`, foreground `#252830`, muted text `#707783`, borders `#e5e8ee`, accent `#da3345`. Column maximum width 640px.
- English `continueChat` becomes `Keep talking`. Arabic stays `كمّل المحادثة`.
- Accessible names that stay: message box `copy.message`, attach `copy.attach`, send `copy.send`, summary heading `copy.review`, buttons **Submit ticket**, **Remove**, **Refresh**, **Start a new report**, **Start new report**, **Cancel**, **Retry**.
- A summary never submits by itself. **Keep talking** only focuses `#intake-message`.
- After a receipt exists, the composer is not rendered.
- Enter sends. Shift+Enter inserts a newline. Enter during IME composition does not send.
- Work from `users-frontend/apps/web` for tests: `npm test -- src/features/intake/IntakePage.test.tsx`.

---

### Task 1: Put the summary and receipt in the thread

**Files:**
- Modify: `users-frontend/apps/web/src/features/intake/copy.ts` (English `continueChat`)
- Modify: `users-frontend/apps/web/src/features/intake/IntakePage.test.tsx`
- Modify: `users-frontend/apps/web/src/features/intake/ChatTranscript.tsx`
- Modify: `users-frontend/apps/web/src/features/intake/ReviewPanel.tsx`
- Modify: `users-frontend/apps/web/src/features/intake/IntakePage.tsx`

**Interfaces:**
- Consumes: existing `IntakePage` controller calls, `ReviewPanel` fact rendering, `ReceiptPanel` props.
- Produces: `ChatTranscript` accepts `review?: ReactNode` and `receipt?: ReactNode` and renders them inside `role="log"`. `ReviewPanel` accepts `onSubmit: () => void`, `onContinue: () => void`, and `actionsDisabled: boolean`, and renders **Submit ticket** then **Keep talking**.

- [ ] **Step 1: Write the failing test**

Add this import beside the existing Testing Library import in `IntakePage.test.tsx`:

```tsx
import { act, render, screen, waitFor, within } from "@testing-library/react"
```

Add this test after the existing `"requires explicit submission after summary review"` test:

```tsx
it("keeps the summary and receipt inside the conversation", async () => {
  const user = userEvent.setup()
  const { controller } = await readyController("en")
  render(<IntakePage controller={controller} />)
  const log = await screen.findByRole("log", { name: "Conversation" })
  expect(within(log).getByRole("heading", { name: "Review your report" })).toBeVisible()
  expect(within(log).getByRole("button", { name: "Keep talking" })).toBeVisible()
  expect(within(log).getByRole("button", { name: "Submit ticket" })).toBeVisible()
  expect(screen.queryByRole("complementary")).not.toBeInTheDocument()
  expect(document.querySelector(".intake-wordmark")?.textContent).toBe("zaincash")
  await user.click(screen.getByRole("button", { name: "Keep talking" }))
  expect(screen.getByRole("textbox", { name: "Your message" })).toHaveFocus()
  await user.click(screen.getByRole("button", { name: "Submit ticket" }))
  expect(await within(log).findByRole("heading", { name: "Ticket received" })).toBeVisible()
  expect(screen.queryByRole("textbox", { name: "Your message" })).not.toBeInTheDocument()
})
```

- [ ] **Step 2: Run the test to verify it fails**

Run from `users-frontend/apps/web`:

```bash
npm test -- src/features/intake/IntakePage.test.tsx -t "keeps the summary and receipt inside the conversation"
```

Expected: FAIL because the review heading is outside the log, the button is named `Continue conversation`, and an `<aside>` exposes `complementary`.

- [ ] **Step 3: Update the English label**

In `copy.ts`, change the English value only:

```ts
continueChat: "Keep talking",
```

Leave the Arabic value as `كمّل المحادثة`.

- [ ] **Step 4: Render summary actions inside the review**

Replace `ReviewPanel.tsx` with:

```tsx
import type { IntakeApi } from "./api"
import type { IntakeCopy } from "./copy"
import type { Attachment, Credentials, CustomerReview } from "./types"
import { OwnedImage } from "./OwnedImage"
import { Button } from "@workspace/ui/components/button"

function factText(review: CustomerReview, key: string, copy: IntakeCopy) {
  const fact = review.facts[key]
  if (!fact || fact.status === "unknown" || fact.status === "missing") return copy.unknown
  if (fact.status === "not_applicable") return copy.notApplicable
  if (fact.status === "conflicting") return `${copy.conflicting}: ${fact.value || copy.unknown}`
  return fact.normalized || fact.value || copy.unknown
}

export function ReviewPanel({
  review,
  attachments,
  credentials,
  api,
  copy,
  headingRef,
  onSubmit,
  onContinue,
  actionsDisabled,
}: {
  review: CustomerReview
  attachments: Attachment[]
  credentials: Credentials | null
  api: IntakeApi
  copy: IntakeCopy
  headingRef: (node: HTMLHeadingElement | null) => void
  onSubmit: () => void
  onContinue: () => void
  actionsDisabled: boolean
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
            <dt>{copy.fieldLabels[key] || key}</dt>
            <dd>
              <bdi dir="auto">{factText(review, key, copy)}</bdi>
            </dd>
          </div>
        ))}
      </dl>
      {review.unknown_keys.length ? (
        <ul>
          {review.unknown_keys.map((key) => (
            <li key={key}>
              {copy.fieldLabels[key] || key}: {factText(review, key, copy)}
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
      <div className="intake-actions">
        <Button type="button" disabled={actionsDisabled} onClick={onSubmit}>
          {copy.submit}
        </Button>
        <Button type="button" variant="outline" disabled={actionsDisabled} onClick={onContinue}>
          {copy.continueChat}
        </Button>
      </div>
    </section>
  )
}
```

- [ ] **Step 5: Render those nodes inside the log**

Replace `ChatTranscript.tsx` with:

```tsx
import type { ReactNode } from "react"
import type { IntakeMessage } from "./types"
import type { IntakeCopy } from "./copy"

export function ChatTranscript({
  messages,
  copy,
  announcedId,
  review = null,
  receipt = null,
}: {
  messages: IntakeMessage[]
  copy: IntakeCopy
  announcedId: string | null
  review?: ReactNode
  receipt?: ReactNode
}) {
  const announced = messages.find((message) => message.id === announcedId)
  return (
    <section className="intake-thread" aria-label={copy.conversation} role="log" aria-relevant="additions">
      {announced && announced.role === "assistant" ? (
        <p className="intake-announce" aria-live="polite">
          {announced.text}
        </p>
      ) : null}
      {messages.map((message) => (
        <article key={message.id} dir="auto" lang={message.language} className={`intake-bubble intake-${message.role}`}>
          <span className="intake-speaker">{message.role === "user" ? copy.you : copy.assistant}</span>
          <p>{message.text}</p>
        </article>
      ))}
      {review}
      {receipt}
    </section>
  )
}
```

- [ ] **Step 6: Replace the page shell**

Replace the `return` of `IntakePage` (leave the state, effects, and handlers above it unchanged) with:

```tsx
  const isEmpty = !session?.messages.length && !session?.review && !session?.receipt
  const showComposer = session?.phase !== "submitted"

  return (
    <div className={`intake-shell${isEmpty ? " intake-empty" : ""}`} dir={locale === "ar" ? "rtl" : "ltr"} lang={locale}>
      <header className="intake-header">
        <div className="intake-brand">
          <span className="intake-symbol" aria-hidden="true">
            <span />
            <span />
            <span />
          </span>
          <div>
            <p className="intake-wordmark">
              zain<span>cash</span>
            </p>
            <p className="intake-subtitle">{text.subtitle}</p>
          </div>
        </div>
        <div className="intake-header-actions">
          <div className="intake-languages" role="group" aria-label={text.english}>
            <Button type="button" variant={locale === "en" ? "default" : "outline"} onClick={() => void chooseLanguage("en")}>
              {text.english}
            </Button>
            <Button type="button" variant={locale === "ar" ? "default" : "outline"} onClick={() => void chooseLanguage("ar")}>
              {text.arabic}
            </Button>
          </div>
          <Button type="button" variant="ghost" onClick={() => (hasContent ? setConfirmNew(true) : void controller.startNew(locale))}>
            {text.startNew}
          </Button>
        </div>
      </header>
      <main className="intake-layout">
        <div className="intake-conversation">
          <ChatTranscript
            messages={session?.messages ?? []}
            copy={text}
            announcedId={latestAssistant?.id ?? null}
            review={
              session?.review && !session.receipt && !snapshot.busy && session.turn_status === "idle" ? (
                <ReviewPanel
                  review={session.review}
                  attachments={session.attachments}
                  credentials={credentials}
                  api={controller.transport()}
                  copy={text}
                  actionsDisabled={snapshot.busy}
                  onSubmit={() => void controller.submit()}
                  onContinue={() => document.getElementById("intake-message")?.focus()}
                  headingRef={(node) => {
                    reviewHeading.current = node
                  }}
                />
              ) : null
            }
            receipt={session?.receipt ? <ReceiptPanel receipt={session.receipt} copy={text} /> : null}
          />
          {showComposer ? (
            <>
              {snapshot.busy || session?.turn_status === "processing" ? <p role="status">{text.processing}</p> : null}
              {snapshot.error || session?.turn_status === "retryable_failure" ? (
                <p role="alert" className="intake-alert" dir="auto">
                  {locale === "ar" ? text.updateError : snapshot.error || text.updateError}
                </p>
              ) : null}
              {snapshot.resumeUnavailable ? <p className="intake-muted">{text.resumeUnavailable}</p> : null}
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
              <ScreenshotPicker
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
              <MessageComposer copy={text} value={draft} sendDisabled={!canSend} onChange={setDraft} onSubmit={() => void send()} />
            </>
          ) : null}
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
        </div>
      </main>
    </div>
  )
```

Delete the old `<aside>` and the duplicate empty-state paragraphs. The visible empty prompt arrives in Task 2 as the textarea placeholder.

- [ ] **Step 7: Run the intake page tests**

```bash
npm test -- src/features/intake/IntakePage.test.tsx
```

Expected: PASS, including the new test and the existing submission, language, upload, and new-report tests.

- [ ] **Step 8: Commit**

```bash
git add users-frontend/apps/web/src/features/intake/copy.ts users-frontend/apps/web/src/features/intake/IntakePage.test.tsx users-frontend/apps/web/src/features/intake/ChatTranscript.tsx users-frontend/apps/web/src/features/intake/ReviewPanel.tsx users-frontend/apps/web/src/features/intake/IntakePage.tsx
git commit -m "$(cat <<'EOF'
Move intake review and receipt into the chat thread.

EOF
)"
```

---

### Task 2: Put screenshots inside the composer

**Files:**
- Modify: `users-frontend/apps/web/src/features/intake/IntakePage.test.tsx`
- Modify: `users-frontend/apps/web/src/features/intake/MessageComposer.tsx`
- Modify: `users-frontend/apps/web/src/features/intake/ScreenshotPicker.tsx`
- Modify: `users-frontend/apps/web/src/features/intake/IntakePage.tsx`

**Interfaces:**
- Consumes: `ScreenshotPicker` props from Task 1, textbox id `intake-message`, file input id `intake-shots`.
- Produces: `MessageComposer` accepts `attach?: ReactNode` and renders it inside the `<form>`. The file input's accessible name remains `copy.attach`. The submit button's accessible name remains `copy.send`. The textarea placeholder is `copy.empty`.

- [ ] **Step 1: Write the failing test**

Add this test to `IntakePage.test.tsx`:

```tsx
it("puts screenshot upload inside the message form", async () => {
  const { controller } = await collectingController("en")
  render(<IntakePage controller={controller} />)
  const input = await screen.findByRole("textbox", { name: "Your message" })
  expect(input).toHaveAttribute("placeholder", "Describe what happened, or attach a screenshot of the error.")
  const form = input.closest("form")
  expect(form).not.toBeNull()
  expect(within(form as HTMLElement).getByLabelText("Attach screenshots")).toBeInTheDocument()
})
```

- [ ] **Step 2: Run the test to verify it fails**

```bash
npm test -- src/features/intake/IntakePage.test.tsx -t "puts screenshot upload inside the message form"
```

Expected: FAIL because the file input is outside the form and the textarea has no placeholder.

- [ ] **Step 3: Replace the composer**

Replace `MessageComposer.tsx` with:

```tsx
import { useEffect, useRef, type FormEvent, type ReactNode } from "react"
import { Button } from "@workspace/ui/components/button"
import type { IntakeCopy } from "./copy"

function SendIcon() {
  return (
    <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <line x1="12" y1="19" x2="12" y2="5" />
      <polyline points="5 12 12 5 19 12" />
    </svg>
  )
}

export function MessageComposer({
  copy,
  value,
  sendDisabled,
  onChange,
  onSubmit,
  attach = null,
}: {
  copy: IntakeCopy
  value: string
  sendDisabled: boolean
  onChange: (value: string) => void
  onSubmit: () => void
  attach?: ReactNode
}) {
  const ref = useRef<HTMLTextAreaElement>(null)

  useEffect(() => {
    const el = ref.current
    if (!el) return
    el.style.height = "0"
    const next = Math.min(el.scrollHeight, 120)
    el.style.height = `${next}px`
    el.style.overflowY = el.scrollHeight > 120 ? "auto" : "hidden"
  }, [value])

  function submit(event?: FormEvent) {
    event?.preventDefault()
    if (!sendDisabled) onSubmit()
  }

  return (
    <form className="intake-composer" onSubmit={submit}>
      {attach}
      <label className="intake-sr" htmlFor="intake-message">
        {copy.message}
      </label>
      <textarea
        ref={ref}
        id="intake-message"
        name="message"
        dir="auto"
        rows={1}
        placeholder={copy.empty}
        value={value}
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
      <div className="intake-composer-bar">
        <Button type="submit" size="icon" className="intake-send" aria-label={copy.send} disabled={sendDisabled}>
          <SendIcon />
        </Button>
      </div>
    </form>
  )
}
```

- [ ] **Step 4: Make the paperclip the file label**

Replace `ScreenshotPicker.tsx` with:

```tsx
import type { IntakeCopy } from "./copy"
import type { Attachment, Credentials } from "./types"
import type { IntakeApi } from "./api"
import { Button } from "@workspace/ui/components/button"
import { OwnedImage } from "./OwnedImage"

function PaperclipIcon() {
  return (
    <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <path d="M21.44 11.05l-9.19 9.19a6 6 0 01-8.49-8.49l9.19-9.19a4 4 0 015.66 5.66l-9.2 9.19a2 2 0 01-2.83-2.83l8.49-8.48" />
    </svg>
  )
}

export function ScreenshotPicker({
  copy,
  attachments,
  previews,
  progress,
  disabled,
  onSelect,
  onRemove,
  credentials,
  api,
}: {
  copy: IntakeCopy
  attachments: Attachment[]
  previews: { name: string; url: string }[]
  progress: Record<string, number>
  disabled: boolean
  onSelect: (files: File[]) => void
  onRemove: (attachmentId: string) => void
  credentials: Credentials | null
  api: IntakeApi
}) {
  const visible = attachments.filter((item) => !item.removed)
  return (
    <div className="intake-shots">
      <label className="intake-clip" htmlFor="intake-shots">
        <span className="intake-sr">{copy.attach}</span>
        <PaperclipIcon />
      </label>
      <input
        id="intake-shots"
        className="intake-file"
        type="file"
        accept="image/png,image/jpeg,image/webp"
        multiple
        disabled={disabled}
        onChange={(event) => {
          const files = Array.from(event.target.files ?? [])
          if (files.length) onSelect(files)
          event.target.value = ""
        }}
      />
      {previews.length || visible.length ? (
        <ul className="intake-shot-list">
          {previews.map((preview) => (
            <li key={preview.url}>
              <img src={preview.url} alt={preview.name} />
              <progress value={progress[preview.name] ?? 0} max={1} aria-label={`${copy.uploadProgress} ${preview.name}`} />
            </li>
          ))}
          {visible.map((attachment) => (
            <li key={attachment.id}>
              <OwnedImage attachment={attachment} credentials={credentials} api={api} alt={attachment.filename} unavailable={copy.imageUnavailable} />
              <Button type="button" variant="outline" disabled={disabled} onClick={() => onRemove(attachment.id)}>
                {copy.remove}
              </Button>
            </li>
          ))}
        </ul>
      ) : null}
    </div>
  )
}
```

The `Array.from` copy before clearing `event.target.value` keeps the existing "copies selected files" test passing.

- [ ] **Step 5: Pass the picker into the form**

In `IntakePage.tsx`, replace the sibling `<ScreenshotPicker ... />` plus `<MessageComposer ... />` with:

```tsx
              <MessageComposer
                copy={text}
                value={draft}
                sendDisabled={!canSend}
                onChange={setDraft}
                onSubmit={() => void send()}
                attach={
                  <ScreenshotPicker
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
                }
              />
```

- [ ] **Step 6: Run the intake page tests**

```bash
npm test -- src/features/intake/IntakePage.test.tsx
```

Expected: PASS. Upload, remove, image-only send, IME Enter, and Shift+Enter still pass.

- [ ] **Step 7: Commit**

```bash
git add users-frontend/apps/web/src/features/intake/IntakePage.test.tsx users-frontend/apps/web/src/features/intake/MessageComposer.tsx users-frontend/apps/web/src/features/intake/ScreenshotPicker.tsx users-frontend/apps/web/src/features/intake/IntakePage.tsx
git commit -m "$(cat <<'EOF'
Place screenshot upload inside the intake composer.

EOF
)"
```

---

### Task 3: Apply the workspace chat styles

**Files:**
- Modify: `users-frontend/apps/web/src/features/intake/intake.css`

**Interfaces:**
- Consumes: class names from Tasks 1 and 2: `intake-shell`, `intake-empty`, `intake-header`, `intake-brand`, `intake-symbol`, `intake-wordmark`, `intake-subtitle`, `intake-header-actions`, `intake-languages`, `intake-layout`, `intake-conversation`, `intake-thread`, `intake-bubble`, `intake-user`, `intake-assistant`, `intake-speaker`, `intake-review`, `intake-receipt`, `intake-actions`, `intake-composer`, `intake-composer-bar`, `intake-send`, `intake-shots`, `intake-clip`, `intake-file`, `intake-shot-list`, `intake-sr`, `intake-alert`, `intake-partial`, `intake-muted`, `intake-announce`.
- Produces: the light column described in the spec. No new class names.

- [ ] **Step 1: Replace `intake.css`**

```css
.intake-shell {
  min-height: 100svh;
  display: flex;
  flex-direction: column;
  background: #f6f7f9;
  color: #252830;
  font-family: "Geist Variable", "Figtree Variable", "Segoe UI", "Noto Naskh Arabic", Tahoma, sans-serif;
}
.intake-header,
.intake-header-actions,
.intake-languages,
.intake-brand,
.intake-actions,
.intake-shot-list,
.intake-composer-bar {
  display: flex;
  align-items: center;
  gap: 12px;
}
.intake-header {
  justify-content: space-between;
  width: min(640px, 100%);
  margin: 0 auto;
  padding: 20px 16px 8px;
}
.intake-header-actions,
.intake-actions,
.intake-shot-list {
  flex-wrap: wrap;
}
.intake-brand {
  align-items: center;
  gap: 10px;
}
.intake-symbol {
  position: relative;
  width: 35px;
  height: 37px;
  display: block;
  flex-shrink: 0;
  transform: rotate(-8deg);
}
.intake-symbol span {
  position: absolute;
  border: 3px solid #da3345;
  border-radius: 45%;
  width: 27px;
  height: 17px;
  transform: rotate(-28deg);
}
.intake-symbol span:nth-child(1) { top: 1px; left: 7px; }
.intake-symbol span:nth-child(2) { top: 10px; left: 3px; }
.intake-symbol span:nth-child(3) { top: 19px; left: 0; }
.intake-wordmark {
  margin: 0;
  font-size: 26px;
  font-weight: 700;
  letter-spacing: -1.2px;
  line-height: 1;
}
.intake-wordmark span { color: #da3345; }
.intake-subtitle,
.intake-muted,
.intake-speaker { color: #707783; }
.intake-subtitle,
.intake-speaker,
.intake-muted { margin: 0; }
.intake-subtitle { margin-top: 7px; font-size: 13px; }
.intake-layout {
  flex: 1;
  min-height: 0;
  width: min(640px, 100%);
  margin: 0 auto;
  padding: 0 16px 16px;
}
.intake-conversation {
  height: 100%;
  min-height: 0;
  display: flex;
  flex-direction: column;
  gap: 12px;
}
.intake-empty .intake-conversation { justify-content: center; }
.intake-thread {
  flex: 1;
  min-height: 0;
  overflow-y: auto;
  display: flex;
  flex-direction: column;
  gap: 16px;
  padding: 24px 0;
}
.intake-empty .intake-thread { flex: 0; overflow: visible; padding: 0; }
.intake-bubble { max-width: 90%; }
.intake-bubble p,
.intake-review p,
.intake-receipt p { margin: 0; white-space: pre-wrap; }
.intake-user {
  margin-inline-start: auto;
  max-width: 80%;
  padding: 8px 14px;
  border-radius: 16px;
  background: #eceef2;
}
.intake-assistant { padding-inline: 2px; }
.intake-speaker { display: block; margin-bottom: 4px; font-size: 12px; }
.intake-review,
.intake-receipt {
  display: flex;
  flex-direction: column;
  gap: 12px;
  padding: 16px;
  border: 1px solid #e5e8ee;
  border-radius: 12px;
  background: #fff;
}
.intake-review h2,
.intake-receipt h2 { margin: 0; font-size: 1.05rem; }
.intake-review h3 { margin: 0; font-size: 0.95rem; }
.intake-partial,
.intake-alert { margin: 0; padding: 10px 12px; border-radius: 12px; }
.intake-partial { background: color-mix(in oklch, #da3345 10%, #fff); }
.intake-alert { background: color-mix(in oklch, var(--destructive) 12%, #fff); }
.intake-review dl { display: grid; gap: 8px; margin: 0; }
.intake-review dl div {
  display: grid;
  grid-template-columns: minmax(7rem, 0.4fr) minmax(0, 1fr);
  gap: 8px;
}
.intake-review dt { color: #707783; }
.intake-review dd { margin: 0; }
.intake-composer {
  position: sticky;
  bottom: 0;
  display: flex;
  flex-direction: column;
  gap: 8px;
  padding: 12px 12px 8px;
  border: 1px solid #e5e8ee;
  border-radius: 16px;
  background: #fff;
}
.intake-composer textarea {
  width: 100%;
  min-height: 24px;
  max-height: 120px;
  padding: 0;
  border: 0;
  resize: none;
  background: transparent;
  color: #252830;
  font: inherit;
  line-height: 1.6;
}
.intake-composer textarea:focus { outline: none; }
.intake-composer textarea::placeholder { color: #9aa1ad; }
.intake-composer-bar { justify-content: space-between; }
.intake-shots { display: flex; flex-wrap: wrap; align-items: center; gap: 8px; }
.intake-clip {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 32px;
  height: 32px;
  border-radius: 999px;
  color: #707783;
  cursor: pointer;
}
.intake-clip:hover { background: #f3f4f6; }
.intake-file {
  position: absolute;
  width: 1px;
  height: 1px;
  overflow: hidden;
  clip: rect(0 0 0 0);
}
.intake-shot-list { margin: 0; padding: 0; list-style: none; align-items: stretch; }
.intake-shot-list img,
.intake-review img {
  width: 48px;
  height: 48px;
  object-fit: cover;
  border-radius: 8px;
}
.intake-send {
  margin-inline-start: auto;
  border-radius: 999px;
  background: #da3345;
  color: #fff;
}
.intake-send:disabled { background: #e5e8ee; color: #9aa1ad; opacity: 1; }
.intake-sr,
.intake-announce {
  position: absolute;
  width: 1px;
  height: 1px;
  overflow: hidden;
  clip: rect(0 0 0 0);
}
@media (max-width: 720px) {
  .intake-header,
  .intake-header-actions,
  .intake-languages { align-items: stretch; flex-direction: column; }
}
```

- [ ] **Step 2: Run the intake page tests**

```bash
npm test -- src/features/intake/IntakePage.test.tsx
```

Expected: PASS. Styles do not change the accessible names.

- [ ] **Step 3: Commit**

```bash
git add users-frontend/apps/web/src/features/intake/intake.css
git commit -m "$(cat <<'EOF'
Style the intake page as a ZainCash chat column.

EOF
)"
```

---

### Task 4: Check the page in the browser

**Files:**
- None

**Interfaces:**
- Consumes: the page served by `users-frontend/apps/web` on port 5174.

- [ ] **Step 1: Start the users frontend**

From `users-frontend/apps/web`, if port 5174 is already serving this app, reuse it. Otherwise:

```bash
npm run dev
```

Expected: Vite reports `http://localhost:5174/`.

- [ ] **Step 2: Check the empty English column**

Open `http://localhost:5174/`. Confirm:

- Light gray page, white rounded composer, red round send button, `zain` plus red `cash`, no red header bar, no side panel.
- Placeholder: `Describe what happened, or attach a screenshot of the error.`
- The composer sits in the middle of the column.
- Clicking the paperclip opens a file chooser. The send button is muted while the box is empty.

- [ ] **Step 3: Check Arabic direction**

Click `العربية`. Confirm the column direction is right to left, the subtitle is Arabic, and the message box name is `رسالتك`. Click `English` and confirm the direction returns to left to right.

- [ ] **Step 4: Check a narrow viewport**

Set the viewport to 390px wide. Confirm the header wraps, the column uses the width, and the composer remains usable.

- [ ] **Step 5: Check a live turn only if the intake API responds**

If sending a message returns an assistant reply, confirm the customer text is a gray bubble on the end side and the assistant text is plain on the start side. If a summary appears, confirm **Submit ticket** and **Keep talking** are inside the thread and **Keep talking** focuses the box. If submit returns a reference, confirm the receipt is in the thread and the composer is gone.

If the API is down, record that the shell was checked and the live turn was not. Do not fake a ticket.

- [ ] **Step 6: Commit the spec status only if it is still uncommitted**

```bash
git add docs/superpowers/specs/2026-10-19-intake-chat-ui-design.md docs/superpowers/plans/2026-10-19-intake-chat-ui.md
git commit -m "$(cat <<'EOF'
Record the approved intake chat layout plan.

EOF
)"
```

Skip this commit if those docs are already committed. Do not commit unrelated files.
