# Customer intake chat layout

Date: 2026-10-19

Status: Approved by the user on 2026-10-19. Implementation plan: `docs/superpowers/plans/2026-10-19-intake-chat-ui.md`.

## 1. Outcome

The customer intake page at the users frontend becomes one chat column in the support-workspace palette. The customer starts a conversation, the assistant keeps asking until the report is ready, and the customer confirms that summary in the thread before a ticket is raised.

This is a presentation change. Session behavior, the intake API, and the employee workspace stay as they are.

The user explicitly selected:

- Reshape the existing intake screen. Do not replace it with the sample `AgentChat` component.
- Use the support workspace look: light gray page, white surfaces, Zain red accent.
- Keep language switching, screenshot upload, review, submit, and the receipt.
- When the assistant is ready, show the summary as the next support message, with **Submit ticket** and **Keep talking**.
- After submit, show the receipt in the thread and remove the composer.

## 2. Scope

In scope:

- `users-frontend/apps/web/src/features/intake/` layout, styles, and the English label for continuing the conversation.
- Two additions to `IntakePage.test.tsx`.

Out of scope:

- Backend, intake controller, API client, and session storage.
- Employee frontend.
- A new `components/ui/agent-chat.tsx` file, and installing `clsx` or `tailwind-merge` for this work.
- Changing `ThemeProvider`. The intake page sets its own light palette on its shell.

## 3. Layout

The page is a full-height column on `#f6f7f9`, foreground `#252830`, muted text `#707783`, borders `#e5e8ee`, accent `#da3345`. Content is centered at a maximum width of 640px. Direction follows the selected language.

```text
zaincash                         العربية  English     Start a new report
Tell support what happened before a ticket is sent

        Support
        What amount was deducted?

                                              25,000 IQD
                                              You

        Review your report
        Transfer of 25,000 IQD on 7 Oct did not arrive.
        Amount          25,000 IQD
        Reference       Unknown
        [ Submit ticket ]  [ Keep talking ]

        [clip]  Describe what happened…            (send)
```

Header:

- Wordmark `zain` plus `cash` in `#da3345`, with the existing three-stroke red symbol used by the employee workspace brand.
- Subtitle remains `copy.subtitle`.
- Language controls and **Start a new report** sit in the header.
- No full-width red header rule, and no side column.

Thread:

- The thread is a log labeled with `copy.conversation` and fills the space above the composer.
- Customer messages are gray bubbles aligned to the end side. Support messages are plain text on the start side, with the speaker name.
- Each message keeps `dir="auto"` and its own `lang`.
- The latest assistant message stays announced for screen readers, as it is today.

Empty state:

- When there are no messages, no review, and no receipt, the composer is vertically centered in the column. Unsent screenshot chips still appear inside that composer.
- The visible prompt is `copy.empty`. The textbox accessible name stays `copy.message`.
- On a narrow viewport the header wraps, and the column uses the full width with the page padding.

Composer:

- A white rounded box (16px radius) with a 1px `#e5e8ee` ring.
- The textarea starts at one line, grows with the text up to 120px, then scrolls.
- Enter sends. Shift+Enter inserts a newline. Enter during IME composition does not send.
- The send control is a round button. It uses `#da3345` with white text when sending is allowed, and a muted fill when it is not. Its accessible name is `copy.send`.
- Screenshot chips and upload progress sit inside the box, above the textarea.
- The paperclip is the visible attach control. The file input keeps the accessible name `copy.attach` (`Attach screenshots` / `أرفق لقطات`).

Summary message:

- Rendered in the thread when `session.review` exists and `session.receipt` does not.
- Heading text remains `copy.review`, focused when a newly requested review arrives.
- Shows the partial-context notice, review text, fact list, unknown keys, additional issues, and attached screenshots, with the same fact wording as today.
- **Submit ticket** calls `controller.submit()`. **Keep talking** (`copy.continueChat`) only moves focus to `#intake-message`. It does not clear the review. A later customer message updates the session through the existing send path.

Receipt:

- Rendered after the messages once `session.receipt` exists.
- Shows `copy.receiptTitle`, the ticket reference, and the existing status sentence for `processing`, `ready_for_employee`, or `needs_attention`.
- The composer, attach control, and send control are not rendered.

Status strip, directly above the composer while it is visible:

- Processing or a busy turn: `copy.processing` as a status, plus **Refresh** when the turn is processing or polling is exhausted.
- Error or retryable failure: an alert using the existing Arabic/English error text, plus **Retry**.
- A failed upload still surfaces its message in an alert and leaves the unsent draft in the textarea.

New report:

- **Start a new report** starts immediately when there are no messages and no attachments still on the session.
- When either exists, the same confirmation as today appears: `copy.confirmNewBody`, **Start new report**, and **Cancel**.

## 4. Components

| Unit | Responsibility |
| --- | --- |
| `IntakePage` | Column shell, header, empty-state placement, status strip, confirmation, and the existing controller calls. |
| `ChatTranscript` | Message log. Renders the summary after the messages when a review is waiting, and the receipt after submit. |
| `ReviewPanel` | Summary content and the two actions. |
| `ReceiptPanel` | Reference and status. |
| `MessageComposer` | Growing textarea, send button, and the screenshot chips. |
| `ScreenshotPicker` | Hidden file input, paperclip label, chips, progress, and remove. |
| `intake.css` | The column, bubbles, composer, and light workspace colors, scoped to `.intake-shell`. |
| `copy.ts` | English `continueChat` becomes `Keep talking`. Arabic stays `كمّل المحادثة`. |

`IntakeController`, `api.ts`, and `types.ts` do not change. Send, upload, remove, review, submit, retry, refresh, and start-new keep their current call sites and guards, including one submit while a submit is in flight, keeping a draft when upload fails, and ignoring a late reply after a new report starts.

## 5. Checks

Existing `IntakePage` tests must pass with the accessible names in section 3.

Add:

- **Keep talking** focuses the message box.
- After the receipt is shown, the message box is absent.

Then check the running page in the browser, in English and Arabic: empty composer, a conversation, a summary in the thread, a receipt with no composer, and a narrow viewport.
