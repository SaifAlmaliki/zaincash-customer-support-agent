# Guided intake interview — design

Date: 2026-11-13. Builds on `2026-10-18-customer-intake-design.md` and `2026-10-19-intake-chat-ui-design.md`.

## Goal

The customer app (`users-frontend`, served on 5174) must collect as much context as possible before a ticket is created. A customer who starts with a vague message such as `حولت فلوس وما وصلت` should be interviewed until the report is as complete as:

> حولت 50000 دينار لعلي حسين على رقم 07701234567 بتاريخ 2026-10-06 وانقطعت من رصيدي بس ما وصلتله. رقم العملية ZC2410000123

A customer who sends that complete message first should go straight to review, with no questions asked.

## Evaluation of the current implementation (2026-11-13)

A live run on 5174 (model `google/gemini-2.5-flash`) and a code review found these problems.

- **Wrong or missing questions.**
  - "What did you expect?" is asked for transfers, even after the complete message.
  - "Did it arrive?" is asked after "it didn't arrive". The answer "I don't know" then contradicts the first message.
  - For `failed_transfer` the recipient number can never be asked: it is not a material or high-value key. The reference and the error text are asked only if the model lists them.
  - There is no recipient-name detail.
- **Each key gets one ask.** An off-topic answer (the debited question answered with "yesterday") leaves the key missing for good. The report goes to review as partial after four answers.
- **Backend knowledge is dropped.**
  - `Question.reason` is discarded in `graph.py::_ask`.
  - `readiness.missing` reaches the UI but is not used.
  - The facts collected so far are visible only inside a review.
  - There are no quick replies, no "I don't know" button and no progress indicator.
- **Waiting feels stalled.**
  - The customer's message stays in the composer until the turn finishes, which takes 4.5–16 s.
  - The only activity signal is a small toolbar line, and it always says "Reviewing your information…".
- **The review card is confusing.**
  - The model summary lists every field, then the details list repeats them, then an unlabelled list repeats the unknowns.
  - Missing and unknown share one label, and there is no way to fill a gap.
  - The card disappears while the ticket is being submitted.

## Approach

The fixed question rules choose every question. The model writes the question text and reads typed answers. Quick-reply answers are recorded without the model.

## 1. Question rules (backend)

### Field plan

Each category has a **required** list and an **ask-once** list.

- **Required:** keep asking until the detail is known, explicitly unknown, or its ask limit is reached.
- **Ask-once:** asked once, after the required details. A missing or unknown answer does not stop the report from being complete (`sufficient_context`).

| Category | Required | Ask-once |
|---|---|---|
| failed_transfer | issue, amount, date, debited, recipient_outcome, recipient_phone | recipient_name, txn_ref |
| wrong_recipient | issue, amount, date, recipient_phone | recipient_name, txn_ref |
| bill_payment | issue, biller, amount, date | txn_ref, debited |
| agent_dispute | issue, amount, agent_location, date | txn_ref |
| refund_request | issue, merchant, amount, date | txn_ref |
| app_bug | issue, failed_step, expected | exact_error, device, app_version |
| login_access | issue, failed_step, expected | exact_error, device, app_version |
| card_issue | issue, card_symptom, expected | exact_error |
| account_kyc | issue, kyc_step, expected | exact_error |
| fraud_report | issue, date | amount, recipient_phone, txn_ref |
| general_inquiry | issue | — |
| other | issue, desired_outcome | — |

- `actual` and `expected` are no longer required for money categories, because the expected outcome is implied there. The model may still record them.
- `exact_error` is not on the failed_transfer ask-once list. Asking "what error appeared?" after a complete transfer report would stop that report from going straight to review. The model can still request it through `additional_needed` when the customer mentions an error.
- The `required_fields` for each category in the taxonomy are still merged into the required list, as they are today.
- `additional_needed` keys from `HIGH_VALUE` stay ask-once additions.

### New fact key `recipient_name`

- It matches `receiver_name` in the transactions table.
- Add it to:
  - the prompt vocabulary in `intake_v1.md`
  - the question templates in `policy.py` (ar/en)
  - the review labels in `review.py` (ar)
  - the customer locales (ar/en)
  - the employee reported-details labels

### Implied facts (prompt)

Add these rules to `intake_v1.md`:
- "ما وصلت / ما وصلتله / didn't arrive" records `recipient_outcome` = not received.
- "انقطعت / انخصمت من رصيدي / was deducted" records `debited` = yes.

Each fact quotes the customer's words. Never ask about a detail the customer has already stated.

### Re-ask once

- The rule: if a required key was asked, the next customer turn did not resolve it, and the customer did not say "I don't know", the key may be asked once more. The re-ask is reworded.
- Count the asks per key from `QuestionRecord`. Once a key has been asked twice it is never asked again, and it counts as not provided.
- A conflicting precise value (amount, phone, date, reference) follows the same two-ask limit.

### Question metadata

- `answer_kind` is derived from the key by the rules, never by the model:
  - `yes_no`: debited, recipient_outcome, repeats
  - `amount`: amount
  - `phone`: recipient_phone
  - `reference`: txn_ref
  - `date`: date
  - `text`: every other key
- `choices`:
  - `yes_no` → `["yes", "no", "unknown"]`
  - `reference` → `["unknown", "attach"]`
  - every other kind → `["unknown"]`
  - `attach` is handled on the screen only; it opens the file picker.
- `QuestionRecord` gains `reason` and `attempt`. Existing stored records without these fields stay valid; defaults are applied when they are read.
- `answer_kind` and `choices` are always derived from the key and are never stored, so older records get them too. The question text is the text of the assistant message.
- The question that is actually asked becomes `readiness.next_key` again, so the two can no longer disagree.

### Quick-reply answers

- A message may carry `answer_to = {message_id, key, choice}`.
- Validation: `message_id` and `key` must match the waiting question, and `choice` must be one of its choices. Otherwise the request fails with `RevisionConflict`.
- Recording, with evidence that quotes the full message text:
  - `unknown` → a fact with status `unknown`
  - `yes` / `no` → a `known` fact, value = message text, normalized = `yes` / `no`
- The turn skips the model's analyze step and goes straight to merge, then ask or review. If the report becomes ready, review still calls the model for the summary.
- The fingerprint check that prevents duplicate processing covers `answer_to`.

## 2. API contract

### `SessionView` additions

```jsonc
"pending_question": null | {
  "key": "debited", "message_id": "uuid", "reason": "…", "text": "…",
  "answer_kind": "yes_no", "choices": ["yes", "no", "unknown"], "attempt": 1
},
"progress": [
  { "key": "amount", "tier": "required", "status": "known", "display": "50000" },
  { "key": "txn_ref", "tier": "ask_once", "status": "unknown", "display": null }
]
```

- `pending_question` is the latest question, but only when the newest assistant message asked it and the phase is `collecting`.
- `progress`:
  - It is built on every read from the field plan for the current category and the stored facts.
  - `display` is the normalized value, or else the value, and only for known facts.
  - `progress` is an empty list until a customer turn has been analyzed (no stored facts yet). After that it follows the current category, including `other`.
  - `customer_phone` is excluded.

### Message request

The new optional field `answer_to`. Its validation and recording are covered under "Quick-reply answers" in section 1.

### `POST /api/intake/sessions/{id}/ask`

- Body: `{request_id, expected_revision, key}`.
- It runs through the existing operation claim, which handles idempotency, conflicts and busy turns. The operation kind is `ask`.
- No model call. It:
  - drops the open review and sets the phase to `collecting`
  - appends the template question for `key` as an assistant message
  - records a `QuestionRecord`
- `key` must appear in `progress`. Otherwise it fails with `InvalidEvidence`.
- The two-ask limit does not apply, because the customer chose to answer.

### Unchanged

The existing message, review and submit request fields. Older clients ignore the new response fields.

## 3. Chat screen

### Optimistic customer bubble

- On send, the message is shown in the thread as pending and the composer clears.
- On a retryable failure the bubble shows "ما انرسلت · إعادة المحاولة" ("not sent · try again"). The retry reuses the same request.
- Text typed while a request is in flight is still preserved.

### Typing bubble and status

- A three-dot assistant bubble shows while a message or ask operation is processing.
- The toolbar status matches the operation: sending, uploading, removing or submitting.

### Question bubble

- The latest pending question shows its reason in muted text: "ليش نسأل: …" ("why we ask: …").
- Older questions show text only.

### Quick replies

- The latest pending question shows chips for its `choices`:
  - yes → `اي` / `Yes`
  - no → `لا` / `No`
  - unknown → `ما أعرف` / `I don't know`
  - unknown for `reference` → `ما عندي رقم` / `I don't have the number`
  - attach → `أرفق لقطة الوصل` / `Attach the receipt`
- A chip sends its localized label as `text`, together with `answer_to`. The attach chip opens the file picker instead.

### Composer hints

| answer_kind | Placeholder | inputMode |
|---|---|---|
| phone | `07XXXXXXXXX` | `tel` |
| amount | "مثلاً 50000" | `numeric` |
| reference | "مثلاً ZC2410000123" | default |
| date | "مثلاً 2026-10-06 أو امس" | default |
| text | default placeholder | default |

The composer font size becomes 16px, which stops iOS from zooming on focus.

### Progress strip

- Placed above the composer, and shown when `progress` is not empty.
- Collapsed: `التفاصيل: 4 من 7` ("details: 4 of 7"), counting resolved required details, plus a "Review what I have" button. The button moves here from the header.
- Expanded, one chip per detail:
  - ✓ known, with its display value
  - ○ missing or conflicting
  - – unknown
- Ask-once details are lighter and are not counted.
- Collapsed by default under 720px, expanded otherwise.

### Copy

- New ar/en keys go in `locales/ar.json` and `locales/en.json` as additions only.
- `copy.ts` gets the matching types.

## 4. Review card

### Status

- Sufficient: the badge "التفاصيل كاملة" ("details complete").
- Partial: the banner names the missing required details, for example "ناقص: رقم المستلم" ("missing: recipient number").

### Summary

- `review_v1.md`: `customer_text` is a short neutral narrative of what happened, two or three sentences. It does not list every field as label/value pairs, because the details list is shown separately.
- The narrative is neutral, not addressed to the customer, because the Arabic customer text and the employee text must stay identical (`review.py`). The existing number-grounding validation still applies.

### Details, each shown once

- **اللي عرفناه** ("what we know"): label and value.
- **ناقص** ("missing"): each item has an `جاوب` ("answer") button that calls `/ask`.
- **ما معروف** ("not known"): each item has a `تذكرت؟ جاوب` ("remembered? answer") button that calls `/ask`.

The grouping comes from `progress`. Facts outside the plan are listed under "what we know" when they are known. Remove the duplicate unknown list and the customer phone row.

### Additional issues

They show a localized label and their status.

### Actions

- Submit and Continue move inside the card.
- During submit the card stays visible and the Submit button shows a spinner.

## Error handling

- `answer_to` mismatch → `RevisionConflict` → the screen reloads the session, as it does for this error today.
- `/ask` with a key that is not in the plan → `InvalidEvidence`. The screen only offers keys from `progress`.
- Quick replies make no model call. A summary call made after a quick reply keeps the existing retryable-failure path.

## Testing

Tests are written first and must fail before the change.

### Backend (pytest, guarded `support_test`)

- Unit tests:
  - the field plan for each category
  - expected/actual not asked for money categories
  - one re-ask, then the key is never asked again
  - ask-once keys do not block `sufficient_context`
  - `answer_kind` and `choices`
  - a quick reply is recorded with no analyze call (from the scripted model's call log)
  - an `answer_to` mismatch is rejected
  - `/ask` and its validation
  - the `progress` projection
  - `QuestionRecord` back-compatibility
- Multi-turn API scenarios with the scripted model:
  1. The vague start ends in review with `50000`, `07701234567`, `علي حسين`, a date of `2026-10-06`, `ZC2410000123`, debited yes and not received. No key is asked more than twice.
  2. The complete message goes straight to review with zero questions.
  3. Answering `ما عندي رقم` for the reference still gives `sufficient_context`.

### Frontend (vitest)

- The optimistic bubble and the typing bubble.
- Chips send `answer_to`.
- The placeholder and inputMode follow the answer kind.
- The progress counts.
- The review card groups, and its answer buttons call `/ask`.
- Submit sits inside the card and the card stays visible while submitting.

### Live and browser checks

- `tests.intake.live_probe` gets the vague and the complete Arabic messages against the configured model. These are paid calls with synthetic data.
- Playwright on 5174 runs the full scenario through to an employee ticket: Arabic at 390px and English on desktop.

### Gates

The existing backend, `users-frontend` and `employee-frontend` test, typecheck, lint and build commands all pass.

## Out of scope

- The UI language switching on its own from the model-detected language.
- Duplicate review invitations when the language is switched.
- Specific error messages.
- A readable ticket reference.
- Polling the receipt status.
