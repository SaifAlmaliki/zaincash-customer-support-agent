# Ticket flow charts

Date: 2026-10-25

Status: Approved by the user on 2026-10-25. Implementation plan: `docs/superpowers/plans/2026-10-25-ticket-flow.md`.

## 1. Outcome

On the employee ticket review page, the employee sees how the one open ticket moved through the pipeline. Two Mermaid charts sit above the existing written **Pipeline & tool trace** list. The list stays as it is.

The top chart is the full pipeline for this ticket. The path it took is highlighted. A step it skipped stays visible, marked not used, with the reason. The chart under it is the open step: what that step received, each choice or lookup it made, and what it produced. Step names are English. When the customer message contains Arabic letters, the received lines, produced lines, and skip reasons are Arabic and use Tajawal.

The employee changes the open step by choosing its English name. The pipeline chart highlights that step. The written list does not change.

Nothing new is stored. The page builds both charts from the result it already loads.

## 2. Scope

In scope:

- `employee-frontend/src/features/review/TicketFlow.tsx`, rendered by `TicketReviewPage` immediately above `PipelineTrace`.
- `employee-frontend/src/features/review/ticket-flow.ts`, a pure `buildTicketFlow(result)` function.
- `employee-frontend/src/features/review/ticket-flow-copy.ts`, the English and Arabic sentences.
- `employee-frontend/src/features/review/ticket-flow.test.ts`.
- The `mermaid` package, and `@fontsource/tajawal` for the Arabic lines.

Out of scope:

- Backend, API, and stored results.
- Rewriting `PipelineTrace` or its English sentences.
- The customer app, the queue, and any chart of more than the open ticket.
- A live chart while a run is still in progress.

## 3. What the employee sees

The steps, in order, with these English names:

| Node | Name |
| --- | --- |
| `prepare` | Prepare |
| `escalate_empty` | Empty ticket |
| `jev_classify` | Jev |
| `gemini_classify` | Gemini |
| `extract` | Extract |
| `lookup` | Investigate |
| `decide` | Route |
| `draft` | Draft |

The pipeline chart is a top-to-bottom Mermaid flowchart. A used step is highlighted. The selected step is highlighted again so it is obvious which detail is open. An unused step stays on the chart and carries the words "not used" plus the reason. A step whose route cannot be proven stays on the chart as "not recorded" and is not given a skip reason.

The detail chart is a second top-to-bottom flowchart for the selected step only:

```text
Received → each choice, lookup, or check, in order → Produced
```

Prepare states the channel and that the message was cleaned. It does not paste the customer message into a node. The message remains where the review page already shows it. Card numbers stay masked. The charts never show a password, PIN, or other secret. A credential check says only that it passed, failed, or was unavailable.

Draft's detail chart lists each recorded lookup and each recorded check, then what the draft produced. Those events come from the same `agent_trace` split that the written list already uses.

Under the charts, a row of buttons uses the English step names. Choosing one selects that step. The page does not depend on clicking inside the Mermaid picture.

## 4. Which step is open

The straight path is Prepare → Jev → Extract → Investigate → Route → Draft. On that path, Empty ticket and Gemini are not used, and Draft is open.

A choice is a departure from that straight path. The page opens the latest one:

- The message has no text, or the escalation reasons include `empty_ticket`. Prepare chose Empty ticket. Prepare is open. Jev, Gemini, Extract, Investigate, Route, and Draft are not used because the empty message ended the path. This rule wins over `classifier_path` and over the trace.
- `classifier_path` is `gemini_fallback` or `disagreement`. Jev sent the ticket to Gemini. Jev is open, even when the trace is missing. Empty ticket is not used because the message had text.
- `classifier_path` is `gemini`, and the trace shows `gemini_classify` and does not show `jev_classify`. Prepare sent the ticket to Gemini and did not ask Jev. Prepare is open. Jev is not used because this run asked Gemini directly.
- `classifier_path` is `jev`. There was no departure. Draft is open. Gemini is not used because Jev was already sure, even when a Gemini stage event is also present.

`classifier_path` wins when it disagrees with the trace.

If `status` is `failed` and the trace has stage events, the last of those events is where the run stopped. That step is open. Every step after it is not used because the run stopped. Its produced line is "The run stopped." If `status` is `failed` and the trace has no stage events, the open step from the rules above stays open and its produced line is "The run stopped." The raw `error` string is not copied into the chart.

If the trace is missing and `classifier_path` is `gemini`, Jev is "not recorded". The page does not invent a skip reason. Draft is open unless the empty-message rule applies.

## 5. Language

Arabic is used when `ticket.text` contains an Arabic letter (`\u0600`–`\u06FF` or `\u0750`–`\u077F`). An empty message uses English. The draft being Arabic does not switch the charts if the customer message is English.

English step names stay English in both languages. Received lines, produced lines, lookup lines, check lines, and skip reasons use the Arabic copy when the rule above matches, and the English copy otherwise. Arabic text uses Tajawal. English chart text uses the app font.

## 6. How a result becomes the charts

`buildTicketFlow` reads the result already loaded by `TicketReviewPage` at `/results/:id`. It returns the eight steps, whether each was used, not used, or not recorded, the skip reason, the received and produced lines, Draft's lookups and checks, the selected step, and whether the copy is Arabic.

Stage events, tool events, and check events come from `reviewEvidence`. A trace value that `reviewEvidence` already rejects is ignored.

Used steps without a saved field say that the field was not recorded. They are still used.

Mermaid is configured with `securityLevel: "strict"` and `htmlLabels: false`. Node text is plain text. Customer content is escaped so it cannot break the diagram or inject markup.

If Mermaid throws while drawing, `TicketFlow` shows one English sentence: the chart could not be drawn. `PipelineTrace` still renders under it.

## 7. Sentences

The copy module owns every sentence. The chart components do not assemble prose. Each step has a received sentence and a produced sentence in both languages. Skip reasons:

| Situation | English reason |
| --- | --- |
| Empty ticket skipped | The message had text. |
| Jev skipped | This run asked Gemini directly. |
| Gemini skipped | Jev was already sure. |
| Steps after an empty message | The empty message ended the path. |
| Steps after a failure | The run stopped. |

Arabic copy states the same facts. Names of categories, teams, priorities, and tool names stay as the employee app already shows them, including Arabic category labels that `categoryLabel` already returns. Amounts and references are included as stored. Phone numbers and transaction references may appear, as they already do in the written list.

## 8. Tests

`ticket-flow.test.ts` covers `buildTicketFlow` only:

- A straight Jev path opens Draft, marks Gemini not used because Jev was sure, and marks Empty ticket not used because the message had text.
- `gemini_fallback` and `disagreement` open Jev.
- A blank message opens Prepare and marks every later step not used because the empty message ended the path.
- A Gemini path whose trace has no Jev stage opens Prepare and marks Jev not used because this run asked Gemini directly.
- A Gemini path with no trace marks Jev not recorded and opens Draft.
- A failed Jev path with no stage events opens Draft and uses "The run stopped." as Draft's produced line. A failed result whose last stage event is `extract` opens Extract and marks Investigate, Route, and Draft not used. The raw error string is absent from both charts.
- A missing extracted field produces the not-recorded sentence for that field.
- An Arabic `ticket.text` selects the Arabic received and produced lines. An English message keeps the English lines.
- Tool arguments that are not a query, transaction reference, phone, service, or reason are omitted.

## 9. Files

```text
employee-frontend/src/features/review/TicketFlow.tsx
employee-frontend/src/features/review/ticket-flow.ts
employee-frontend/src/features/review/ticket-flow-copy.ts
employee-frontend/src/features/review/ticket-flow.test.ts
employee-frontend/src/features/review/TicketReviewPage.tsx   renders TicketFlow above PipelineTrace
```
