# Customer conversation intake for ZainCash support

Date: 2026-10-18

Status: Written specification approved by the user on 2026-10-18; implementation plan awaiting user review.

## 1. Outcome and agreed requirements

Customers often submit tickets without enough information for employees to understand the problem. Add a customer-facing intake conversation that gathers relevant evidence, resolves ambiguity, and produces a customer-reviewed ticket for the existing employee workflow.

Success means an employee can quickly identify what happened, when it happened, the relevant transaction or application details, and what still needs investigation, without reconstructing the entire conversation.

The user explicitly selected:

- A ticket becomes visible to employees only after the customer reviews its summary and submits it.
- Direct demo access without customer sign-in; a browser can resume its own saved draft.
- Iraqi Arabic and English conversations, including mixed-language messages.
- Screenshot uploads that the AI can read and use for follow-up questions.
- Intake gathers customer-provided context. Transaction, incident, and policy investigation stays in the existing submitted-ticket pipeline.
- Employees receive an Iraqi Arabic summary, alongside the original conversation and screenshots.
- Adaptive questioning continues until the issue is sufficiently understood, rather than ending after a fixed number of questions.
- Customers can review and submit the information they have, with unknowns explicitly recorded.

The customer-facing review uses the customer's current language. The Iraqi Arabic employee summary represents the same reviewed facts. Neither intake nor submission sends a final support response; employees retain the existing response-review workflow.

## 2. Current implementation and integration points

- `users-frontend/apps/web/src/App.tsx` is a starter React screen in a Vite/shadcn monorepo.
- `employee-frontend/src/features/review/TicketReviewPage.tsx` displays processed tickets, evidence, drafts, and employee review actions.
- `backend/app/api/runs.py` persists uploaded tickets and starts processing through `backend/app/services/batch_jobs.py`.
- `backend/app/pipeline/graph.py` runs classification, extraction, lookup, routing, and drafting.
- `backend/app/pipeline/stage6_draft/agent.py` creates a bounded LangChain agent for one ticket. It is not a customer conversation session.
- `backend/app/taxonomy.py` defines existing categories and category-specific required fields.
- `backend/app/db/models.py` contains tickets, runs, results, and reviews. `workspace_queries.py` projects result rows into employee list/detail responses.
- The API uses one local worker and marks interrupted runs failed during startup recovery.

The intake flow is a separate module in the existing backend, with a submission adapter into the current pipeline. Existing batch ingestion remains a supported entry point.

## 3. Approach and boundaries

### Selected: guided LangGraph conversation

Use LangGraph to orchestrate one intake turn at a time, with LangChain model calls for multimodal understanding, structured extraction, and natural-language questions. Explicit application state and readiness rules govern the conversation.

Alternatives considered:

| Approach | Trade-off |
| --- | --- |
| Free-form agent chat | Flexible, but harder to control repeated questions, evidence tracking, and premature completion. |
| Fixed questionnaire with AI summary | Predictable, but less responsive to screenshots, ambiguous answers, and issue-specific follow-ups. |
| Guided graph with structured facts | Combines flexible questions with inspectable progress, durable state, and a precise submission boundary. |

### Responsibilities

| Unit | Responsibility | Dependencies |
| --- | --- | --- |
| Customer UI | Chat, uploads, review/corrections, submission receipt | Intake API and shared user-frontend UI components |
| Intake API/service | Session ownership, validation, turn coordination, persistence, submission | Database, attachment store, graph |
| Intake graph | Update facts, assess gaps, produce next question or review | Typed state, category requirements, model adapter |
| Vision/model adapter | Interpret text/images and return validated structured output | Existing OpenRouter credentials; configured vision-capable model |
| Attachment store | Validate, retain, and retrieve session-linked images | Configured persistent local directory and database metadata |
| Submission adapter | Freeze a reviewed snapshot and create exactly one ticket/run | Existing ticket, run, result, and processing functions |
| Employee intake panel | Present summary, facts, unknowns, transcript, screenshots | Submitted intake projection on ticket detail |

This first version covers intake through employee handoff. It does not add customer accounts, a customer-to-employee messaging channel, or automated financial actions.

## 4. Conversation state and turn flow

### Durable state

The database is authoritative. Persist messages and the structured state after each completed turn; do not rely on process-local memory or browser message history. Each request loads the latest state and invokes the graph for one customer turn. A second independent LangGraph checkpoint store is unnecessary for this version.

Session state contains:

- Session ID, hashed access token, timestamps, revision, and current language.
- Phase: `collecting`, `review_ready`, or `submitted`.
- Turn execution state: idle, processing, or retryable failure, with a durable attempt identifier.
- Provisional issue category and descriptions of any distinct additional issues.
- Structured facts, evidence references, missing details, contradictions, and question history.
- Readiness assessment and concrete reasons for that assessment.
- Versioned customer-language review and Iraqi Arabic employee summary.
- Submission references once committed.

Persist sessions, messages, attachments, and immutable submission snapshots in separate tables, following existing schema-upgrade conventions. Constraints enforce one message request ID per session and one submission per session.

### Turn flow

```text
Customer message and/or screenshots
  -> validate ownership and expected revision
  -> persist customer message and claim turn
  -> interpret new text/images with existing facts and relevant history
  -> validate and merge facts, corrections, and evidence
  -> evaluate missing information and contradictions
       -> ask one focused question -> persist state -> wait for customer
       -> prepare review -> persist state -> wait for review/submission
```

The graph does not repeatedly generate questions without a new customer answer. Internal retries have execution limits; the number of customer turns is driven by useful missing context.

Concurrent turns for the same session are rejected with a recoverable conflict. Model execution happens outside a long-running database transaction. Committing a model result requires a matching session revision and attempt identifier, so a late response cannot overwrite newer state.

## 5. Facts, evidence, and readiness

### Shared context

Gather the details relevant to the reported issue:

- What the customer was trying to do.
- What happened instead, including the exact displayed message when available.
- When the issue happened, whether it is ongoing, and whether it repeats.
- Steps already attempted and their outcomes.
- The customer's requested outcome when it is not already clear.

### Issue-specific context

Use the existing category taxonomy as the starting point and add intake-specific guidance separately, without changing the meaning of current classifier fields.

For a transfer or payment issue, useful details include the reference, amount and currency, timing, whether funds were deducted, and what the recipient or merchant observed. For a login or app problem, ask about the failing step, exact message, and relevant device/app details. General inquiries do not require a transaction reference or an artificial incident timeline.

Do not ask for every possible field. Ask only when the answer can materially improve understanding or downstream handling. If the category changes, retain collected evidence and reevaluate which gaps matter.

### Fact representation

Each fact records a field name, reported value, optional normalized value, source message/image IDs, and a status: `known`, `missing`, `unknown`, `conflicting`, or `not_applicable`.

- Text-derived facts retain a supporting quote or span.
- Image-derived facts identify the attachment and visible evidence. Model interpretation is not treated as transaction-system verification.
- Corrections retain earlier evidence while selecting the customer's corrected value.
- An explicit unknown is not silently filled by the model.
- Phone numbers have a role; a recipient number must not become `customer_phone` without customer evidence that it is their own.
- Relative dates use the source message timestamp and Baghdad timezone. Ambiguous dates or times receive a clarifying question rather than an invented precise timestamp.

### Meaning of confident enough

Offer the normal review step when:

1. The issue and expected/actual outcome are sufficiently clear for that kind of request.
2. Material, applicable details are supported by customer messages or readable screenshots.
3. No unresolved material contradiction remains.
4. The agent identifies no further high-value clarification necessary for an actionable handoff.

Model judgment can propose gaps and next questions, but a self-reported numeric confidence score cannot independently declare readiness. The service verifies evidence references and the declared field statuses before accepting a readiness decision.

If a useful detail is missing, ask one targeted question. If the customer says they do not know, an alternative route is allowed when genuinely helpful, such as asking for a receipt instead of repeating the reference question. Do not repeatedly ask the same unanswerable question.

When useful questions are exhausted but important unknowns remain, offer an explicitly partial review. Distinguish `sufficient_context` from `partial_context` in the snapshot. The customer can also select **Review what I have** at any point after providing content. This does not label the report complete or bypass final confirmation.

## 6. Language and screenshot behavior

### Language

- Initially use Iraqi Arabic UI copy with a visible Arabic/English switch.
- Follow the customer's language in subsequent conversation; handle mixed Arabic/English and English error text without losing its original wording.
- Apply directionality per message and field, keeping numbers and transaction references readable.
- Customer review uses the selected conversation language.
- Employee summary always uses Iraqi Arabic. Preserve identifiers, amounts, dates, and quoted error messages exactly through translation.

### Screenshots

- Accept JPEG, PNG, and WebP, verified by decoding the actual bytes.
- Initial configurable limits: 5 MiB and 20 megapixels per image, three images per message, ten per session.
- Store images under server-generated names in a configured persistent directory, with ownership and attachment metadata in Postgres. Exclude uploaded data from version control.
- Customer image retrieval requires ownership of the session; attachments are not published as static public URLs.
- Send image content with MIME type through the server-side model adapter. Preserve the source image for employee viewing.
- Retain image-derived observations so earlier images do not need to be resent on every turn. Reinspect a referenced image when a follow-up actually requires it.
- Unclear digits, cropped messages, or conflicting image/text evidence trigger clarification. An unreadable image can still remain attached for employee review.
- Removing a draft attachment invalidates facts supported only by that attachment and invalidates any existing review. Submitted evidence is immutable.
- Treat image text and customer messages as evidence, not instructions that can change the workflow or trigger submission.
- The assistant must not request PINs, OTPs, passwords, or full payment-card numbers. Reuse existing text sanitization where applicable; do not claim that image contents have been automatically redacted.

Vision capability is a deployment requirement to verify, not something inferred from the existing configured model name. Add an intake model setting that can use the existing OpenRouter configuration with an explicitly vision-capable selection.

## 7. Review and submission

### Review

The review displays the issue, relevant facts, exact errors, timing, attempted steps, attachments, and remaining unknowns. It offers **Submit ticket**, **Correct details**, and **Continue conversation**.

Corrections enter the same evidence/fact-update path as conversation answers. Every correction or new message invalidates the old review and produces a new revision before submission. The service stores a review identifier tied to the exact session revision and reviewed facts.

Generate both language presentations from the same validated fact snapshot. The customer-language version is the confirmation surface; the Iraqi Arabic translation cannot introduce additional facts. Numeric and identifier consistency is checked before accepting the paired summaries.

### Submission transaction

Submission requires a session-owned, current review identifier and explicit customer confirmation. Inside one database transaction:

1. Lock and verify the session and review revision.
2. Return the existing receipt if this session was already submitted.
3. Freeze the reviewed facts, summaries, transcript boundary, attachment references, and readiness reason.
4. Create a ticket with a stable `INTAKE-` external reference, `source="intake"`, and `channel="app"`.
5. Create its processing run and a result placeholder with `status="processing"`.
6. Link the session/snapshot to the ticket, run, and result; mark it submitted.
7. Commit before scheduling the existing processing job.

The placeholder makes submitted tickets visible in the employee workspace immediately, including before AI processing completes. Draft sessions never appear there.

The pipeline ticket body is an Iraqi Arabic rendering of the reviewed facts and explicit unknowns, labelled as customer intake. Keep it within the existing ticket size limit without dropping material facts; if it cannot fit, block submission with a recoverable request to narrow the issue. Retain the full transcript separately. Existing extraction spans refer to this frozen ticket body; the intake evidence panel refers to the original message/image sources.

Resolve confirmed relative dates before rendering the ticket body. Preserve the intake start time and source message timestamps in the snapshot; use the submission time as the ticket's `received_at`. This avoids changing the meaning of "yesterday" when a draft spans multiple days.

The provisional intake category assists questioning, while the existing pipeline still makes the final category, priority, lookup, routing, and drafting decisions.

### Processing lifecycle

Reuse `run_job` and `save_outcomes`; the result upsert replaces the processing placeholder for the same ticket/run. Employee result views and run counts must treat placeholders as unprocessed and disable review actions until an outcome is available.

On setup failure, processing exception, or interrupted-run recovery, turn any remaining intake processing placeholders into visible failed results with a retryable processing explanation. A crash between submission commit and job scheduling is therefore observable and cannot lose the submitted report. Recovery follows the existing local single-worker failure semantics rather than silently starting a duplicate run.

The customer receipt distinguishes **submitted** from subsequent processing status. Resending the submission request returns the same receipt; it never creates another ticket or reruns processing. Operators can retry through the existing batch API using the stored ticket ID, body, and customer fields, which reuses that ticket in a new run. A dedicated employee retry button is not part of this change. The receipt's processing status follows the latest result for the submitted ticket, while the original submission reference remains stable.

## 8. API and UI surfaces

### Intake API

Use a separate `/api/intake` namespace. The logical operations are:

- Create an anonymous session; return the session ID and a cryptographically random access token once.
- Read/resume the owned session and its current turn/review/receipt state.
- Upload, retrieve, and remove owned draft attachments.
- Submit a message with a client-generated request ID, expected revision, and attachment IDs.
- Retry a failed turn without duplicating its customer message.
- Request a review, including explicit partial-review intent.
- Submit the current review and return the durable receipt.

Persist only the access-token hash server-side. The customer UI stores its session credentials locally and sends the token in an authorization header, never in a URL. Validate ownership on every customer operation; a session ID alone grants no access. Update the API's explicit development CORS origins and allowed headers for the user UI. Keep the employee development UI on port 5173 and use port 5174 for the customer UI, with strict port selection to prevent accidental switching.

Session-bound mutations validate request IDs and expected revisions. A lost response is recovered by reading session state or retrying the same request. A stale review yields a conflict, with the client loading the current review. Intake responses expose only customer conversation, review, and receipt information, not internal employee drafts, provider errors, or investigation records.

Use ordinary request/response interactions for this version, with a visible processing state and bounded polling when resuming an in-flight turn. Token-by-token streaming is not required for the approved behavior.

### Customer UI

Build within `users-frontend/apps/web`, reusing `packages/ui` components:

- Responsive Arabic/English chat with an accessible message composer.
- Screenshot picker, previews, upload progress, and clear validation errors.
- Saved-session resume and a deliberate start-new-report action.
- Visible assistant activity, retry, and connection-error states.
- **Review what I have** and a review screen that clearly separates known facts from unknowns.
- Receipt with ticket reference and submission/processing state.

Do not show a fabricated confidence percentage. Progress copy describes what has been understood or what still needs clarification.

### Employee UI

Extend the existing ticket detail with an optional intake projection:

- Iraqi Arabic summary and whether context is sufficient or partial.
- Structured facts and unresolved questions/contradictions.
- Expandable original conversation with message language/direction preserved.
- Linked screenshots and source references.

Support the new processing state in lists, detail views, filters, and review-action availability. Older tickets without intake data continue to render normally. Reprocessing a submitted ticket retains the same intake snapshot.

Employee attachment retrieval follows the existing local employee API access model and requires an attachment linked to a submitted ticket/result. It never serves draft-session attachments or exposes customer session tokens. Customer session ownership checks do not introduce an employee authentication system.

## 9. Failure handling and execution limits

- Persist the customer message before model execution. A timeout retains it and its attachments, records retryable turn failure, and keeps the existing facts intact.
- Retry only transient provider failures. Default execution limits are a 60-second deadline and at most three provider requests per turn or review-generation operation, including retries and output repair; make these limits configurable. A retry must not duplicate an assistant reply or fact update.
- Invalid structured output receives a bounded repair attempt; exhaustion leaves the turn retryable rather than declaring readiness.
- After API restart, interrupted turns become retryable. Attempt fencing prevents late responses from overwriting recovered state.
- Reject unsupported/oversized images before model execution. An image upload failure does not silently discard a typed message.
- A database failure cannot be reported as saved, reviewed, or submitted. The UI retains unsent local input and retries with the same operation ID.
- A failed translation or summary consistency check keeps the conversation saved and makes review generation retryable.
- Record model identifier, latency, token usage, and provider-reported cost when available. Do not invent image costs or treat missing cost data as free usage.
- Build prompts from validated facts, open questions, relevant source evidence, and recent messages, while retaining the full transcript durably. Any context-budget limit produces an explicit recoverable state or partial-review option, not silent fact deletion or false completeness.

## 10. Verification and acceptance criteria

### Agent and service tests

Use scripted/fake model responses to verify decisions rather than exact prose:

1. A vague failed-transfer complaint triggers a relevant question; later answers populate facts and change the next question.
2. An initially complete report reaches review without unnecessary questioning.
3. Arabic, English, and mixed-language conversations retain identifiers and exact error text.
4. A question answered in an earlier turn is not repeated; explicit unknowns remain unknown.
5. Corrections and conflicting answers invalidate the old review and preserve source evidence.
6. A category change recalculates relevant gaps without discarding earlier facts.
7. Screenshot observations can supply facts; unreadable or contradictory values cause clarification.
8. The model cannot bypass the readiness rules, invent evidence IDs, or submit a ticket through message/image instructions.
9. Partial review is labelled partial, permits unknowns, and still requires explicit submission.
10. Relative dates remain stable across midnight, refresh, and delayed submission.
11. Customer/employee summary versions preserve the same material facts, amounts, references, and dates.

### Database and API integration tests

- Refresh/resume restores persisted conversation and the current review.
- A different session token cannot read or change messages, attachments, reviews, or receipts through the intake API; employee endpoints never expose unsubmitted drafts.
- Duplicate message requests and turn retries do not duplicate customer/assistant messages.
- Concurrent turns and stale reviews fail cleanly without overwriting current facts.
- Double submission and a lost submission response create one ticket, one initial run, and one receipt.
- Submission persistence is atomic; employee queries contain no draft sessions.
- Processing placeholders are visible only after submission, excluded from processed counts, and cannot be approved.
- Normal outcomes replace placeholders; job setup failures and restart recovery leave visible failed results with intact intake evidence.
- Image size/type validation and attachment ownership are enforced server-side.

### Frontend and end-to-end checks

- Exercise chat, upload/remove screenshot, correction, partial review, submission, and receipt/resume states.
- Check Arabic RTL and English LTR on mobile and desktop, keyboard access, and readable mixed-direction identifiers.
- Submit from the customer UI, then open the corresponding employee ticket and verify its summary, unknowns, transcript, and screenshots.
- Verify older employee tickets and existing review actions remain compatible.
- Run targeted backend tests and Ruff, then the affected backend regression suite; run both frontend type/lint/build checks and meaningful interaction tests.

### Live model check

With the configured vision-capable provider, use synthetic screenshots and sample Arabic/English conversations to verify that image content is actually interpreted and ambiguous content generates a clarification. Record model/settings and observed results separately from deterministic test results. If provider access is unavailable, report the live check as unverified rather than substituting fake-model evidence.

## 11. Delivery and review

The implementation plan should organize work around persisted intake contracts, graph/vision behavior, API/submission integration, customer UI, employee presentation, and end-to-end verification. Keep those boundaries independently testable within this single intake feature.

The new user frontend currently contains its own Git metadata inside the main repository. Preserve it while planning; repository integration must be resolved explicitly before staging or committing frontend work.

This specification records the approved conversational design. Implementation starts after the user reviews this file, approves the resulting written implementation plan, and selects its execution method.
