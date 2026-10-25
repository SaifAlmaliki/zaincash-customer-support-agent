# Ticket Flow Charts Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Show the employee two Mermaid charts for the one ticket they opened: the full pipeline, and the received, choices, and produced story of the open step.

**Architecture:** `ticket-flow-copy.ts` owns every English and Arabic sentence. `ticket-flow.ts` reads the result already loaded on the review page and returns eight steps plus two Mermaid source strings. `TicketFlow.tsx` draws those strings and lets the employee switch steps. `PipelineTrace` stays unchanged underneath.

**Tech Stack:** employee-frontend, React 19, TypeScript, Vitest, Mermaid, `@fontsource/tajawal`.

**Spec:** `docs/superpowers/specs/2026-10-25-ticket-flow-design.md`

## Global Constraints

- One ticket only: the result `TicketReviewPage` already loads from `/results/:id`. No backend, API, or stored-result changes.
- Charts sit immediately above `<PipelineTrace result={result} />`. Do not edit `PipelineTrace` or its English sentences.
- Eight steps, in order: `prepare` Prepare, `escalate_empty` Empty ticket, `jev_classify` Jev, `gemini_classify` Gemini, `extract` Extract, `lookup` Investigate, `decide` Route, `draft` Draft.
- Step names stay English. Arabic letters in `ticket.text` (`\u0600`–`\u06FF` or `\u0750`–`\u077F`) switch received lines, produced lines, lookup lines, check lines, and skip reasons to Arabic in Tajawal. An empty message stays English.
- English skip reasons, verbatim: "The message had text." "This run asked Gemini directly." "Jev was already sure." "The empty message ended the path." "The run stopped."
- A step is `used`, `unused` (with a reason), or `unrecorded` (no invented reason).
- Empty message, or escalation reason `empty_ticket`, opens Prepare and wins over `classifier_path` and the trace.
- `gemini_fallback` and `disagreement` open Jev. `classifier_path` `jev` opens Draft and marks Gemini unused even if a Gemini stage event exists.
- `classifier_path` `gemini` with no stage events marks Jev `unrecorded` and opens Draft. `classifier_path` `gemini` with any stage events opens Prepare and marks Jev unused because this run asked Gemini directly.
- `status === "failed"` with stage events opens the last of those events, marks every later step unused because the run stopped, and sets that step's produced line to "The run stopped." With no stage events, keep the open step and replace only its produced line. Never copy `result.error` into the chart.
- Prepare states the channel and that the message was cleaned. It does not paste `ticket.text` into a node.
- Card numbers stay masked. Never show a password, PIN, or other secret. A credential check says only that it passed, failed, or was unavailable, or that none was recorded.
- Tool details may include only `query`, `txn_ref`, `phone`, `service`, and `reason`.
- Mermaid uses `securityLevel: "strict"` and `htmlLabels: false`. If rendering throws, show the English sentence "The chart could not be drawn." The written list still renders.
- The employee switches steps with English-name buttons. Do not depend on clicking inside the Mermaid picture.
- Work from `employee-frontend`. Tests: `npm test -- src/features/review/ticket-flow.test.ts`.

---

### Task 1: Sentence catalog

**Files:**
- Create: `employee-frontend/src/features/review/ticket-flow-copy.ts`
- Test: `employee-frontend/src/features/review/ticket-flow.test.ts`

**Interfaces:**
- Consumes: nothing
- Produces: `isArabicMessage(text: string): boolean`, `sentence(id: SentenceId, arabic: boolean, vars?: Record<string, string | number>): string`, `channelName(channel: string, arabic: boolean): string`, `fieldLabel(key: string, arabic: boolean): string`, `lookupSentence(status: string | null, arabic: boolean): string`, `toolLine(event: { tool?: string; status?: string; arguments?: unknown }, arabic: boolean): string`, `checkLines(events: { kind?: string; status?: string; findings?: unknown; credential_check_degraded?: unknown; reasons?: unknown }[], arabic: boolean): string[]`, and `SentenceId` covering every id used below.

- [ ] **Step 1: Write the failing test**

Create `employee-frontend/src/features/review/ticket-flow.test.ts`:

```typescript
import { expect, it } from "vitest"
import { channelName, checkLines, fieldLabel, isArabicMessage, lookupSentence, sentence, toolLine } from "./ticket-flow-copy"

it("treats Arabic letters as an Arabic message and a blank message as English", () => {
  expect(isArabicMessage("التحويل لم يصل")).toBe(true)
  expect(isArabicMessage("The transfer failed")).toBe(false)
  expect(isArabicMessage("   ")).toBe(false)
})

it("returns the English skip reasons verbatim and the Arabic reasons for the same ids", () => {
  expect(sentence("messageHadText", false)).toBe("The message had text.")
  expect(sentence("askedGeminiDirectly", false)).toBe("This run asked Gemini directly.")
  expect(sentence("jevWasSure", false)).toBe("Jev was already sure.")
  expect(sentence("emptyEnded", false)).toBe("The empty message ended the path.")
  expect(sentence("runStopped", false)).toBe("The run stopped.")
  expect(sentence("chartFailed", false)).toBe("The chart could not be drawn.")
  expect(sentence("messageHadText", true)).toBe("الرسالة تحتوي على نص.")
  expect(sentence("runStopped", true)).toBe("توقف التشغيل.")
})

it("names channels and fields in the selected language", () => {
  expect(channelName("whatsapp", false)).toBe("WhatsApp")
  expect(channelName("whatsapp", true)).toBe("واتساب")
  expect(fieldLabel("txn_ref", false)).toBe("Transaction reference")
  expect(fieldLabel("txn_ref", true)).toBe("الرقم المرجعي")
})

it("fills a sentence template and describes a lookup", () => {
  expect(sentence("prepareReceived", false, { channel: "WhatsApp", length: "180" })).toBe(
    "Read the WhatsApp message (180 characters).",
  )
  expect(lookupSentence("matched", false)).toBe("One transaction matched.")
  expect(lookupSentence("matched", true)).toBe("تطابق تحويل واحد.")
  expect(lookupSentence(null, false)).toBe("Lookup was not recorded.")
})

it("keeps only safe tool details and states credential checks without secrets", () => {
  expect(toolLine({ tool: "lookup_transaction", status: "ok", arguments: { txn_ref: "ZC-1044", pin: "1234" } }, false)).toBe(
    "Looked up a transaction reference: ZC-1044. Completed.",
  )
  expect(toolLine({ tool: "lookup_transaction", status: "ok", arguments: { txn_ref: "ZC-1044", pin: "1234" } }, false)).not.toContain("1234")
  expect(checkLines([{ kind: "guardrail", status: "passed", findings: [], credential_check_degraded: true }], false)).toEqual([
    "The credential check was unavailable.",
  ])
  expect(checkLines([{ kind: "guardrail", status: "passed", findings: [] }], false)).toEqual([
    "The credential check passed.",
    "No safety-check findings were recorded.",
  ])
})
```

- [ ] **Step 2: Run the test to verify it fails**

Run from `employee-frontend`: `npm test -- src/features/review/ticket-flow.test.ts`

Expected: FAIL because `./ticket-flow-copy` does not exist.

- [ ] **Step 3: Write the sentence catalog**

Create `employee-frontend/src/features/review/ticket-flow-copy.ts`:

```typescript
import { humanize } from "../../lib/format"

const ARABIC = /[\u0600-\u06FF\u0750-\u077F]/

export function isArabicMessage(text: string): boolean {
  return ARABIC.test(text)
}

const EN = {
  messageHadText: "The message had text.",
  askedGeminiDirectly: "This run asked Gemini directly.",
  jevWasSure: "Jev was already sure.",
  emptyEnded: "The empty message ended the path.",
  runStopped: "The run stopped.",
  chartFailed: "The chart could not be drawn.",
  notUsed: "not used",
  notRecorded: "not recorded",
  notAsked: "This step was not asked.",
  notRecordedStep: "This step was not recorded.",
  recorded: "Recorded.",
  prepareReceived: "Read the {channel} message ({length} characters).",
  prepareEmpty: "No customer message was recorded for this step.",
  prepareProduced: "Arabic digits were converted to 0–9, and card numbers were hidden.",
  cleaned: "Received the cleaned message.",
  jevSure: "Jev classified this ticket. Gemini was not asked. {category}, {confidence} confidence, priority {priority}.",
  jevUnsure: "Jev was unsure, so Gemini was asked.",
  geminiAfterJev: "Received Jev's uncertain classification.",
  classified: "{category}, {confidence} confidence, priority {priority}.",
  extractReceived: "Received the classification {category}.",
  fieldLine: "{label}: {value}.",
  fieldFrom: "{label}: {value} from “{span}”.",
  fieldMissing: "{label}: This field was not recorded.",
  notStated: "Not stated",
  lookupReceived: "Received the extracted details.",
  lookupMissing: "Lookup was not recorded.",
  decideReceived: "Received the investigation result.",
  assigned: "Assigned to {team}.",
  held: "Held for a person: {reasons}.",
  noEscalation: "No escalation. Ready for review.",
  draftReceived: "Received {category} for {team}.",
  draftSaved: "A reply was saved for a person to review.",
  draftMissing: "No reply was saved.",
  citations: "{count} policy passages were cited.",
  citationOne: "1 policy passage was cited.",
  credentialPassed: "The credential check passed.",
  credentialFailed: "The credential check failed.",
  credentialUnavailable: "The credential check was unavailable.",
  credentialUnrecorded: "No credential check was recorded.",
  safetyFlagged: "Safety checks flagged {findings}.",
  safetyClear: "No safety-check findings were recorded.",
  noPriority: "no priority",
  noTeam: "no team",
  noCategory: "Unclassified",
  toolOk: "{action}. Completed.",
  toolCancelled: "{action}. Cancelled.",
  toolIncomplete: "{action}. Did not complete.",
  toolPlain: "{action}.",
  lookupMatched: "One transaction matched.",
  lookupAmount: "A transaction was found, but the amount in the message does not match the record.",
  lookupDate: "A transaction was found, but the date does not match the record.",
  lookupMissingStatus: "No transaction matched the details in the message.",
  lookupAmbiguous: "Several transactions matched, so none was selected.",
  lookupSkipped: "This issue does not need a transaction lookup.",
} as const

const AR: Record<keyof typeof EN, string> = {
  messageHadText: "الرسالة تحتوي على نص.",
  askedGeminiDirectly: "هذا التشغيل طلب جيميناي مباشرة.",
  jevWasSure: "جيف كان متأكدًا.",
  emptyEnded: "الرسالة الفارغة أنهت المسار.",
  runStopped: "توقف التشغيل.",
  chartFailed: "The chart could not be drawn.",
  notUsed: "لم تُستخدم",
  notRecorded: "غير مسجّلة",
  notAsked: "لم يُطلب تنفيذ هذه الخطوة.",
  notRecordedStep: "هذه الخطوة غير مسجّلة.",
  recorded: "مُسجّلة.",
  prepareReceived: "قُرئت رسالة {channel} ({length} حرفًا).",
  prepareEmpty: "لم تُسجَّل رسالة للعميل في هذه الخطوة.",
  prepareProduced: "حُوّلت الأرقام العربية إلى 0–9، وأُخفيت أرقام البطاقات.",
  cleaned: "استلم الرسالة بعد تنظيفها.",
  jevSure: "صنّف جيف هذه التذكرة. لم يُسأل جيميناي. {category}، ثقة {confidence}، أولوية {priority}.",
  jevUnsure: "جيف لم يكن متأكدًا، لذلك سُئل جيميناي.",
  geminiAfterJev: "استلم تصنيف جيف غير المؤكد.",
  classified: "{category}، ثقة {confidence}، أولوية {priority}.",
  extractReceived: "استلم التصنيف {category}.",
  fieldLine: "{label}: {value}.",
  fieldFrom: "{label}: {value} من «{span}».",
  fieldMissing: "{label}: هذا الحقل غير مسجّل.",
  notStated: "غير مذكور",
  lookupReceived: "استلم التفاصيل المستخرجة.",
  lookupMissing: "لم يُسجَّل البحث.",
  decideReceived: "استلم نتيجة التحقق.",
  assigned: "أُسندت إلى {team}.",
  held: "أُبقيت لموظف: {reasons}.",
  noEscalation: "لا يوجد تصعيد. جاهزة للمراجعة.",
  draftReceived: "استلم {category} لفريق {team}.",
  draftSaved: "حُفظ رد ليراجعه موظف.",
  draftMissing: "لم يُحفظ رد.",
  citations: "استُشهد بـ {count} مقاطع من السياسة.",
  citationOne: "استُشهد بمقطع واحد من السياسة.",
  credentialPassed: "نجح فحص بيانات الدخول.",
  credentialFailed: "فشل فحص بيانات الدخول.",
  credentialUnavailable: "فحص بيانات الدخول غير متاح.",
  credentialUnrecorded: "لم يُسجَّل فحص بيانات الدخول.",
  safetyFlagged: "فحوصات السلامة أشارت إلى {findings}.",
  safetyClear: "لم تُسجَّل ملاحظات من فحوصات السلامة.",
  noPriority: "بدون أولوية",
  noTeam: "بدون فريق",
  noCategory: "بدون تصنيف",
  toolOk: "{action}. اكتمل.",
  toolCancelled: "{action}. أُلغي.",
  toolIncomplete: "{action}. لم يكتمل.",
  toolPlain: "{action}.",
  lookupMatched: "تطابق تحويل واحد.",
  lookupAmount: "وُجد تحويل، لكن المبلغ في الرسالة لا يطابق السجل.",
  lookupDate: "وُجد تحويل، لكن التاريخ لا يطابق السجل.",
  lookupMissingStatus: "لا يوجد تحويل يطابق التفاصيل في الرسالة.",
  lookupAmbiguous: "تطابق أكثر من تحويل، لذلك لم يُختَر أي منها.",
  lookupSkipped: "هذه المشكلة لا تحتاج إلى البحث عن تحويل.",
}

export type SentenceId = keyof typeof EN

export function sentence(id: SentenceId, arabic: boolean, vars: Record<string, string | number> = {}): string {
  return (arabic ? AR : EN)[id].replace(/\{(\w+)\}/g, (_, key: string) => String(vars[key] ?? ""))
}

export function channelName(channel: string, arabic: boolean): string {
  if (channel === "app") return arabic ? "تطبيق زين كاش" : "ZainCash app"
  if (channel === "whatsapp") return arabic ? "واتساب" : "WhatsApp"
  if (channel === "call_note") return arabic ? "ملاحظة مكالمة" : "call note"
  return humanize(channel)
}

const FIELDS: Record<string, [string, string]> = {
  txn_ref: ["Transaction reference", "الرقم المرجعي"],
  amount: ["Amount", "المبلغ"],
  date: ["Date", "التاريخ"],
  phone: ["Phone number", "رقم الهاتف"],
}

export function fieldLabel(key: string, arabic: boolean): string {
  const pair = FIELDS[key]
  if (!pair) return humanize(key)
  return arabic ? pair[1] : pair[0]
}

const LOOKUP: Record<string, SentenceId> = {
  matched: "lookupMatched",
  amount_mismatch: "lookupAmount",
  date_mismatch: "lookupDate",
  not_found: "lookupMissingStatus",
  ambiguous: "lookupAmbiguous",
  not_applicable: "lookupSkipped",
}

export function lookupSentence(status: string | null, arabic: boolean): string {
  if (!status) return sentence("lookupMissing", arabic)
  const id = LOOKUP[status]
  return id ? sentence(id, arabic) : humanize(status)
}

const TOOLS: Record<string, string> = {
  lookup_transaction: "Looked up a transaction reference",
  search_transactions: "Searched transactions",
  get_customer_recent_transactions: "Listed recent transactions",
  get_customer_ticket_history: "Checked earlier tickets for this customer",
  check_service_status: "Checked whether a service was disrupted",
  search_knowledge_base: "Searched the knowledge base",
  flag_for_human: "Flagged the ticket for a person",
  submit_draft: "Submitted a draft reply",
}

const SAFE_ARGS = ["query", "txn_ref", "phone", "service", "reason"] as const

export function toolLine(event: { tool?: string; status?: string; arguments?: unknown }, arabic: boolean): string {
  const name = event.tool || "a lookup"
  const args = event.arguments
  const record = args !== null && typeof args === "object" && !Array.isArray(args) ? (args as Record<string, unknown>) : {}
  const key = SAFE_ARGS.find((item) => typeof record[item] === "string" && String(record[item]).trim())
  const raw = key ? String(record[key]).trim() : ""
  const detail = key === "reason" && raw ? humanize(raw) : raw
  const action = `${TOOLS[name] || humanize(name)}${detail ? `: ${detail}` : ""}`
  if (event.status === "ok") return sentence("toolOk", arabic, { action })
  if (event.status === "cancelled") return sentence("toolCancelled", arabic, { action })
  if (event.status) return sentence("toolIncomplete", arabic, { action })
  return sentence("toolPlain", arabic, { action })
}

function texts(value: unknown): string[] {
  return Array.isArray(value) ? value.filter((item): item is string => typeof item === "string" && item.trim() !== "") : []
}

export function checkLines(
  events: { kind?: string; status?: string; findings?: unknown; credential_check_degraded?: unknown; reasons?: unknown }[],
  arabic: boolean,
): string[] {
  return events.flatMap((event) => {
    if (event.kind === "guardrail") {
      const findings = texts(event.findings)
      if (event.credential_check_degraded === true) return [sentence("credentialUnavailable", arabic)]
      const credential = event.status === "passed" && findings.length === 0
        ? sentence("credentialPassed", arabic)
        : findings.length
          ? sentence("credentialFailed", arabic)
          : sentence("credentialUnrecorded", arabic)
      const safety = findings.length
        ? sentence("safetyFlagged", arabic, { findings: findings.map(humanize).join(", ") })
        : sentence("safetyClear", arabic)
      return [credential, safety]
    }
    if (event.kind === "draft") {
      const reasons = texts(event.reasons).map(humanize).join(", ")
      const status = humanize(event.status || "status unknown").toLowerCase()
      return [reasons ? `Draft ${status}: ${reasons}.` : `Draft ${status}.`]
    }
    return []
  })
}
```

- [ ] **Step 4: Run the test to verify it passes**

Run from `employee-frontend`: `npm test -- src/features/review/ticket-flow.test.ts`

Expected: PASS, 5 tests.

- [ ] **Step 5: Commit**

```bash
git add employee-frontend/src/features/review/ticket-flow-copy.ts employee-frontend/src/features/review/ticket-flow.test.ts
git commit -m "$(cat <<'EOF'
feat: add English and Arabic sentences for the ticket flow

EOF
)"
```

---

### Task 2: Which step is open

**Files:**
- Create: `employee-frontend/src/features/review/ticket-flow.ts`
- Modify: `employee-frontend/src/features/review/ticket-flow.test.ts`

**Interfaces:**
- Consumes: `sentence`, `isArabicMessage` from `./ticket-flow-copy`
- Produces:
  - `export const STEP_ORDER = ["prepare", "escalate_empty", "jev_classify", "gemini_classify", "extract", "lookup", "decide", "draft"] as const`
  - `export type FlowStepId = (typeof STEP_ORDER)[number]`
  - `export type FlowStep = { id: FlowStepId; name: string; state: "used" | "unused" | "unrecorded"; reason: string | null; received: string; produced: string; events: string[] }`
  - `export type TicketFlow = { arabic: boolean; selectedId: FlowStepId; steps: FlowStep[] }`
  - `export function buildTicketFlow(result: Result): TicketFlow`

- [ ] **Step 1: Write the failing tests**

Append to `ticket-flow.test.ts`. Add `import type { Result } from "../../lib/types"` and `import { buildTicketFlow } from "./ticket-flow"`. Add this helper and these tests:

```typescript
function result(patch: Partial<Result> = {}, ticket: Partial<Result["ticket"]> = {}): Result {
  return {
    id: 10,
    ticket_id: 1,
    run_id: 3,
    ticket: {
      id: 1,
      external_id: "T-1",
      text: "The transfer failed",
      received_at: "2026-10-12T10:00:00Z",
      channel: "whatsapp",
      customer_phone: null,
      ...ticket,
    },
    category: "failed_transfer",
    category_confidence: 0.82,
    category_probs: {},
    priority: "high",
    priority_confidence: null,
    flags: {},
    classifier_path: "jev",
    extracted: {},
    lookup_status: "matched",
    matched_txn_ref: "ZC-1044",
    team: "Payments Ops",
    escalated: false,
    escalation_reasons: [],
    escalation_note: null,
    draft_text: "reply",
    final_text: null,
    citations: [],
    agent_trace: [],
    status: "pending_review",
    error: "PIN 1234 should stay hidden",
    latency_ms: 1,
    cost_usd: 0,
    updated_at: "2026-10-12T10:00:00Z",
    ...patch,
  }
}

function step(flow: ReturnType<typeof buildTicketFlow>, id: string) {
  const found = flow.steps.find((item) => item.id === id)
  if (!found) throw new Error(`missing ${id}`)
  return found
}

it("opens Draft on a straight Jev path and explains the skipped steps", () => {
  const flow = buildTicketFlow(result())
  expect(flow.selectedId).toBe("draft")
  expect(step(flow, "gemini_classify")).toMatchObject({ state: "unused", reason: "Jev was already sure." })
  expect(step(flow, "escalate_empty")).toMatchObject({ state: "unused", reason: "The message had text." })
  expect(step(flow, "jev_classify").state).toBe("used")
})

it("opens Jev when Gemini gave the second opinion", () => {
  expect(buildTicketFlow(result({ classifier_path: "gemini_fallback" })).selectedId).toBe("jev_classify")
  expect(buildTicketFlow(result({ classifier_path: "disagreement" })).selectedId).toBe("jev_classify")
})

it("opens Prepare for an empty message and stops the later steps", () => {
  const flow = buildTicketFlow(result({ classifier_path: "jev", escalation_reasons: [] }, { text: "  " }))
  expect(flow.selectedId).toBe("prepare")
  expect(flow.arabic).toBe(false)
  for (const id of ["jev_classify", "gemini_classify", "extract", "lookup", "decide", "draft"]) {
    expect(step(flow, id)).toMatchObject({ state: "unused", reason: "The empty message ended the path." })
  }
})

it("opens Prepare when Gemini was asked directly", () => {
  const flow = buildTicketFlow(result({
    classifier_path: "gemini",
    agent_trace: [{ kind: "stage", node: "gemini_classify" }],
  }))
  expect(flow.selectedId).toBe("prepare")
  expect(step(flow, "jev_classify")).toMatchObject({ state: "unused", reason: "This run asked Gemini directly." })
})

it("does not invent a Jev skip reason when a Gemini path has no trace", () => {
  const flow = buildTicketFlow(result({ classifier_path: "gemini", agent_trace: [] }))
  expect(flow.selectedId).toBe("draft")
  expect(step(flow, "jev_classify")).toMatchObject({ state: "unrecorded", reason: null })
})

it("lets a Jev path ignore a stray Gemini stage event", () => {
  const flow = buildTicketFlow(result({
    classifier_path: "jev",
    agent_trace: [{ kind: "stage", node: "gemini_classify" }],
  }))
  expect(flow.selectedId).toBe("draft")
  expect(step(flow, "gemini_classify").reason).toBe("Jev was already sure.")
})

it("stops a failed run at its last stage event and hides the raw error", () => {
  const flow = buildTicketFlow(result({
    status: "failed",
    classifier_path: "jev",
    agent_trace: [{ kind: "stage", node: "extract" }],
  }))
  expect(flow.selectedId).toBe("extract")
  expect(step(flow, "extract").produced).toBe("The run stopped.")
  expect(step(flow, "lookup")).toMatchObject({ state: "unused", reason: "The run stopped." })
  expect(step(flow, "draft").state).toBe("unused")
  expect(JSON.stringify(flow)).not.toContain("PIN 1234")
})

it("uses the run-stopped sentence on Draft when a failed Jev path has no stage events", () => {
  const flow = buildTicketFlow(result({ status: "failed", classifier_path: "jev", agent_trace: [] }))
  expect(flow.selectedId).toBe("draft")
  expect(step(flow, "draft").produced).toBe("The run stopped.")
  expect(JSON.stringify(flow)).not.toContain("PIN 1234")
})
```

- [ ] **Step 2: Run the test to verify it fails**

Run from `employee-frontend`: `npm test -- src/features/review/ticket-flow.test.ts`

Expected: FAIL because `buildTicketFlow` is not defined.

- [ ] **Step 3: Implement path selection**

Create `employee-frontend/src/features/review/ticket-flow.ts`:

```typescript
import type { Result } from "../../lib/types"
import { isArabicMessage, sentence } from "./ticket-flow-copy"
import { reviewEvidence } from "./review-evidence"

export const STEP_ORDER = [
  "prepare",
  "escalate_empty",
  "jev_classify",
  "gemini_classify",
  "extract",
  "lookup",
  "decide",
  "draft",
] as const

export type FlowStepId = (typeof STEP_ORDER)[number]
export type FlowStepState = "used" | "unused" | "unrecorded"

export type FlowStep = {
  id: FlowStepId
  name: string
  state: FlowStepState
  reason: string | null
  received: string
  produced: string
  events: string[]
}

export type TicketFlow = {
  arabic: boolean
  selectedId: FlowStepId
  steps: FlowStep[]
}

const NAMES: Record<FlowStepId, string> = {
  prepare: "Prepare",
  escalate_empty: "Empty ticket",
  jev_classify: "Jev",
  gemini_classify: "Gemini",
  extract: "Extract",
  lookup: "Investigate",
  decide: "Route",
  draft: "Draft",
}

type Route = "empty" | "straight" | "cascade" | "gemini_direct" | "gemini_unknown" | "unknown"

function isStep(value: string | undefined): value is FlowStepId {
  return STEP_ORDER.includes(value as FlowStepId)
}

function stageNodes(result: Result): FlowStepId[] {
  return reviewEvidence(result).stages.map((event) => event.node).filter(isStep)
}

function routeOf(result: Result): Route {
  const blank = !result.ticket.text.trim()
  if (blank || result.escalation_reasons.includes("empty_ticket")) return "empty"
  if (result.classifier_path === "jev") return "straight"
  if (result.classifier_path === "gemini_fallback" || result.classifier_path === "disagreement") return "cascade"
  if (result.classifier_path === "gemini") {
    return stageNodes(result).length === 0 ? "gemini_unknown" : "gemini_direct"
  }
  const stages = stageNodes(result)
  if (stages.includes("jev_classify") && stages.includes("gemini_classify")) return "cascade"
  return "unknown"
}

function usedIds(route: Route, stages: FlowStepId[]): FlowStepId[] {
  if (route === "empty") return ["prepare", "escalate_empty"]
  if (route === "cascade") return ["prepare", "jev_classify", "gemini_classify", "extract", "lookup", "decide", "draft"]
  if (route === "gemini_direct" || route === "gemini_unknown") {
    return ["prepare", "gemini_classify", "extract", "lookup", "decide", "draft"]
  }
  if (route === "unknown") return stages
  return ["prepare", "jev_classify", "extract", "lookup", "decide", "draft"]
}

function unusedReason(id: FlowStepId, route: Route, arabic: boolean): string {
  if (route === "empty") return sentence("emptyEnded", arabic)
  if (id === "escalate_empty") return sentence("messageHadText", arabic)
  if (id === "jev_classify") return sentence("askedGeminiDirectly", arabic)
  return sentence("jevWasSure", arabic)
}

function defaultSelected(route: Route): FlowStepId {
  if (route === "empty" || route === "gemini_direct") return "prepare"
  if (route === "cascade") return "jev_classify"
  return "draft"
}

export function buildTicketFlow(result: Result): TicketFlow {
  const arabic = isArabicMessage(result.ticket.text)
  const route = routeOf(result)
  const used = new Set(usedIds(route, stageNodes(result)))
  let selectedId = defaultSelected(route)
  const steps: FlowStep[] = STEP_ORDER.map((id) => {
    const state: FlowStepState = route === "unknown"
      ? (used.has(id) ? "used" : "unrecorded")
      : route === "gemini_unknown" && id === "jev_classify"
        ? "unrecorded"
        : used.has(id) ? "used" : "unused"
    const reason = state === "unused" ? unusedReason(id, route, arabic) : null
    const received = state === "used" ? sentence("recorded", arabic) : sentence(state === "unused" ? "notAsked" : "notRecordedStep", arabic)
    const produced = reason ?? (state === "used" ? sentence("recorded", arabic) : sentence("notRecordedStep", arabic))
    return { id, name: NAMES[id], state, reason, received, produced, events: [] }
  })
  if (result.status === "failed") {
    const stages = stageNodes(result)
    if (stages.length === 0) {
      const open = steps.find((item) => item.id === selectedId)
      if (open) open.produced = sentence("runStopped", arabic)
    } else {
      const last = stages[stages.length - 1]
      const index = STEP_ORDER.indexOf(last)
      selectedId = last
      for (const item of steps) {
        const itemIndex = STEP_ORDER.indexOf(item.id)
        if (item.id === last) {
          item.state = "used"
          item.reason = null
          item.produced = sentence("runStopped", arabic)
        } else if (itemIndex > index) {
          item.state = "unused"
          item.reason = sentence("runStopped", arabic)
          item.produced = sentence("runStopped", arabic)
        }
      }
    }
  }
  return { arabic, selectedId, steps }
}
```

- [ ] **Step 4: Run the tests to verify they pass**

Run from `employee-frontend`: `npm test -- src/features/review/ticket-flow.test.ts`

Expected: PASS. The Task 1 tests still pass.

- [ ] **Step 5: Commit**

```bash
git add employee-frontend/src/features/review/ticket-flow.ts employee-frontend/src/features/review/ticket-flow.test.ts
git commit -m "$(cat <<'EOF'
feat: choose the open step for one ticket's pipeline

EOF
)"
```

---

### Task 3: Received, produced, and drafting events

**Files:**
- Modify: `employee-frontend/src/features/review/ticket-flow.ts`
- Modify: `employee-frontend/src/features/review/ticket-flow.test.ts`

**Interfaces:**
- Consumes: `buildTicketFlow`, `FlowStep`, and from `ticket-flow-copy`: `sentence`, `channelName`, `fieldLabel`, `lookupSentence`, `toolLine`, `checkLines`
- Produces: the same `buildTicketFlow`. Used steps now carry real `received`, `produced`, and `events`. `events` for Draft are tool lines from `reviewEvidence(result).tools` followed by `checkLines(reviewEvidence(result).otherEvents, arabic)`.

- [ ] **Step 1: Write the failing tests**

Append:

```typescript
it("describes Prepare without pasting the customer message", () => {
  const flow = buildTicketFlow(result({}, { text: "The transfer failed", channel: "whatsapp" }))
  expect(step(flow, "prepare").received).toBe("Read the WhatsApp message (19 characters).")
  expect(step(flow, "prepare").produced).toBe("Arabic digits were converted to 0–9, and card numbers were hidden.")
  expect(step(flow, "prepare").received).not.toContain("The transfer failed")
})

it("says a missing extracted field was not recorded", () => {
  const flow = buildTicketFlow(result({ extracted: {} }))
  expect(step(flow, "extract").events).toContain("Transaction reference: This field was not recorded.")
})

it("uses Arabic received and produced lines when the message is Arabic", () => {
  const flow = buildTicketFlow(result({}, { text: "التحويل لم يصل", channel: "whatsapp" }))
  expect(flow.arabic).toBe(true)
  expect(step(flow, "prepare").received).toContain("واتساب")
  expect(step(flow, "prepare").produced).toBe("حُوّلت الأرقام العربية إلى 0–9، وأُخفيت أرقام البطاقات.")
})

it("omits unsafe tool arguments from the Draft events", () => {
  const flow = buildTicketFlow(result({
    agent_trace: [{ kind: "tool", tool: "search_knowledge_base", status: "ok", arguments: { query: "refund", password: "secret" } }],
  }))
  expect(step(flow, "draft").events.join("\n")).toContain("Searched the knowledge base: refund. Completed.")
  expect(step(flow, "draft").events.join("\n")).not.toContain("secret")
})
```

The character count for `"The transfer failed"` is 19. Keep that expectation.

- [ ] **Step 2: Run the test to verify it fails**

Run from `employee-frontend`: `npm test -- src/features/review/ticket-flow.test.ts`

Expected: FAIL because Prepare's received line is still "Recorded."

- [ ] **Step 3: Replace the placeholder story**

In `ticket-flow.ts`, import `categoryLabel`, `humanize`, and `percentage` from `../../lib/format`, and import `channelName`, `checkLines`, `fieldLabel`, `lookupSentence`, `toolLine` from `./ticket-flow-copy`.

Add this function and call it from the `STEP_ORDER.map` callback instead of the placeholder `received` / `produced` lines. Keep the failure block after the map so it still overwrites the stopped step's `produced`.

```typescript
import type { ExtractedField, Result } from "../../lib/types"
import { categoryLabel, humanize, percentage } from "../../lib/format"
import { channelName, checkLines, fieldLabel, isArabicMessage, lookupSentence, sentence, toolLine } from "./ticket-flow-copy"

const FIELD_KEYS = ["txn_ref", "amount", "date", "phone"] as const

function fieldValue(field: ExtractedField | undefined, arabic: boolean): string | null {
  if (!field) return null
  if (field.value == null || field.value === "") return sentence("notStated", arabic)
  if (typeof field.value === "number" || field.currency) {
    const amount = Number(field.value)
    const shown = Number.isFinite(amount) ? amount.toLocaleString("en-US") : String(field.value)
    return `${shown} ${field.currency || "IQD"}`
  }
  return String(field.value)
}

function story(id: FlowStepId, result: Result, arabic: boolean, route: Route): { received: string; produced: string; events: string[] } {
  const category = result.category ? categoryLabel(result.category) : sentence("noCategory", arabic)
  const confidence = percentage(result.category_confidence)
  const priority = result.priority || sentence("noPriority", arabic)
  const team = result.team || sentence("noTeam", arabic)
  if (id === "prepare") {
    const length = result.ticket.text.trim().length
    const received = length
      ? sentence("prepareReceived", arabic, { channel: channelName(result.ticket.channel, arabic), length: length.toLocaleString("en-US") })
      : sentence("prepareEmpty", arabic)
    return { received, produced: sentence("prepareProduced", arabic), events: [] }
  }
  if (id === "jev_classify") {
    const produced = route === "straight"
      ? sentence("jevSure", arabic, { category, confidence, priority })
      : sentence("jevUnsure", arabic)
    return { received: sentence("cleaned", arabic), produced, events: [] }
  }
  if (id === "gemini_classify") {
    const received = route === "gemini_direct" || route === "gemini_unknown"
      ? sentence("cleaned", arabic)
      : sentence("geminiAfterJev", arabic)
    return { received, produced: sentence("classified", arabic, { category, confidence, priority }), events: [] }
  }
  if (id === "extract") {
    const events = FIELD_KEYS.map((key) => {
      const label = fieldLabel(key, arabic)
      const field = result.extracted[key]
      const value = fieldValue(field, arabic)
      if (value == null) return sentence("fieldMissing", arabic, { label })
      return field?.span
        ? sentence("fieldFrom", arabic, { label, value, span: field.span })
        : sentence("fieldLine", arabic, { label, value })
    })
    return { received: sentence("extractReceived", arabic, { category }), produced: events[events.length - 1], events: events.slice(0, -1) }
  }
  if (id === "lookup") {
    return { received: sentence("lookupReceived", arabic), produced: lookupSentence(result.lookup_status, arabic), events: [] }
  }
  if (id === "decide") {
    const reasons = result.escalation_reasons.map(humanize).join(", ")
    const produced = result.escalated
      ? sentence("held", arabic, { reasons: reasons || sentence("notRecorded", arabic) })
      : `${sentence("assigned", arabic, { team })} ${sentence("noEscalation", arabic)}`
    return { received: sentence("decideReceived", arabic), produced, events: [] }
  }
  const evidence = reviewEvidence(result)
  const events = [
    ...evidence.tools.map((event) => toolLine(event, arabic)),
    ...checkLines(evidence.otherEvents, arabic),
  ]
  const citations = result.citations?.length ?? 0
  const produced = [
    result.draft_text ? sentence("draftSaved", arabic) : sentence("draftMissing", arabic),
    citations === 1 ? sentence("citationOne", arabic) : sentence("citations", arabic, { count: citations }),
  ].join(" ")
  return { received: sentence("draftReceived", arabic, { category, team }), produced, events }
}
```

Replace the three placeholder assignments inside the `STEP_ORDER.map` callback with:

```typescript
    const told = state === "used" ? story(id, result, arabic, route) : null
    const received = told?.received ?? sentence(state === "unused" ? "notAsked" : "notRecordedStep", arabic)
    const produced = reason ?? told?.produced ?? sentence("notRecordedStep", arabic)
    const events = told?.events ?? []
    return { id, name: NAMES[id], state, reason, received, produced, events }
```

`Route` stays in this file. The failure block remains after the map and still overwrites the stopped step.

- [ ] **Step 4: Run the tests to verify they pass**

Run from `employee-frontend`: `npm test -- src/features/review/ticket-flow.test.ts`

Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add employee-frontend/src/features/review/ticket-flow.ts employee-frontend/src/features/review/ticket-flow.test.ts
git commit -m "$(cat <<'EOF'
feat: describe what each pipeline step received and produced

EOF
)"
```

---

### Task 4: Mermaid source

**Files:**
- Modify: `employee-frontend/src/features/review/ticket-flow.ts`
- Modify: `employee-frontend/src/features/review/ticket-flow.test.ts`

**Interfaces:**
- Consumes: `TicketFlow`, `FlowStepId`, `buildTicketFlow`
- Produces:
  - `export function mermaidText(value: string): string`
  - `export function pipelineChart(flow: TicketFlow, selectedId: FlowStepId): string`
  - `export function detailChart(flow: TicketFlow, selectedId: FlowStepId): string`

- [ ] **Step 1: Write the failing tests**

Append:

```typescript
import { detailChart, mermaidText, pipelineChart } from "./ticket-flow"

it("escapes text that could break a Mermaid node", () => {
  expect(mermaidText('Say "hi" <script>')).toBe("Say 'hi' script")
  expect(mermaidText("a[b]")).toBe("a(b)")
})

it("draws the full pipeline with the taken step, the skip reason, and the selection", () => {
  const flow = buildTicketFlow(result())
  const chart = pipelineChart(flow, flow.selectedId)
  expect(chart.startsWith("flowchart TD")).toBe(true)
  expect(chart).toContain("class gemini_classify unused")
  expect(chart).toContain("Jev was already sure.")
  expect(chart).toContain("class draft used,selected")
  expect(chart).toContain("jev_classify --> extract")
})

it("draws the open step from received through events to produced", () => {
  const flow = buildTicketFlow(result({
    agent_trace: [{ kind: "tool", tool: "lookup_transaction", status: "ok", arguments: { txn_ref: "ZC-1044" } }],
  }))
  const chart = detailChart(flow, "draft")
  expect(chart).toContain("flowchart TD")
  expect(chart).toContain("ZC-1044")
  expect(chart).toContain("n0 --> n1")
})
```

Merge the new import with the existing `buildTicketFlow` import from `./ticket-flow`. Do not leave two import lines from the same module.

- [ ] **Step 2: Run the test to verify it fails**

Run from `employee-frontend`: `npm test -- src/features/review/ticket-flow.test.ts`

Expected: FAIL because `pipelineChart` is not defined.

- [ ] **Step 3: Write the chart builders**

Add to `ticket-flow.ts`:

```typescript
export function mermaidText(value: string): string {
  return value
    .replace(/[<>]/g, "")
    .replaceAll('"', "'")
    .replaceAll("[", "(")
    .replaceAll("]", ")")
    .replaceAll("`", "'")
    .replaceAll("\n", " ")
}

function nodeLabel(step: FlowStep, arabic: boolean): string {
  if (step.state === "used") return step.name
  if (step.state === "unrecorded") return `${step.name} — ${sentence("notRecorded", arabic)}`
  return `${step.name} — ${sentence("notUsed", arabic)} — ${step.reason ?? sentence("notRecorded", arabic)}`
}

export function pipelineChart(flow: TicketFlow, selectedId: FlowStepId): string {
  const byId = new Map(flow.steps.map((step) => [step.id, step]))
  const lines = [
    "flowchart TD",
    "  classDef used fill:#eef7f0,stroke:#3d7a4a,color:#173222",
    "  classDef unused fill:#f7f7f8,stroke:#999999,color:#666666,stroke-dasharray:4 3",
    "  classDef unrecorded fill:#ffffff,stroke:#bbbbbb,color:#666666",
    "  classDef selected stroke-width:3px,stroke:#1d4e89",
  ]
  for (const step of flow.steps) {
    lines.push(`  ${step.id}["${mermaidText(nodeLabel(step, flow.arabic))}"]`)
  }
  const used = flow.steps.filter((step) => step.state === "used").map((step) => step.id)
  for (let index = 0; index < used.length - 1; index += 1) {
    lines.push(`  ${used[index]} --> ${used[index + 1]}`)
  }
  const unused = (id: FlowStepId) => byId.get(id)?.state === "unused"
  if (unused("escalate_empty")) lines.push("  prepare -.-> escalate_empty")
  if (unused("jev_classify")) lines.push("  prepare -.-> jev_classify")
  if (unused("gemini_classify")) {
    lines.push(`  ${byId.get("jev_classify")?.state === "used" ? "jev_classify" : "prepare"} -.-> gemini_classify`)
  }
  for (const step of flow.steps) {
    const selected = step.id === selectedId ? ",selected" : ""
    lines.push(`  class ${step.id} ${step.state}${selected}`)
  }
  return lines.join("\n")
}

export function detailChart(flow: TicketFlow, selectedId: FlowStepId): string {
  const step = flow.steps.find((item) => item.id === selectedId) ?? flow.steps[0]
  const parts = [step.received, ...step.events, step.produced]
  const lines = ["flowchart TD"]
  parts.forEach((part, index) => lines.push(`  n${index}["${mermaidText(part)}"]`))
  for (let index = 0; index < parts.length - 1; index += 1) lines.push(`  n${index} --> n${index + 1}`)
  return lines.join("\n")
}
```

- [ ] **Step 4: Run the tests to verify they pass**

Run from `employee-frontend`: `npm test -- src/features/review/ticket-flow.test.ts`

Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add employee-frontend/src/features/review/ticket-flow.ts employee-frontend/src/features/review/ticket-flow.test.ts
git commit -m "$(cat <<'EOF'
feat: build Mermaid source for one ticket's pipeline and open step

EOF
)"
```

---

### Task 5: Draw the charts on the ticket page

**Files:**
- Create: `employee-frontend/src/features/review/TicketFlow.tsx`
- Modify: `employee-frontend/src/features/review/TicketReviewPage.tsx`
- Modify: `employee-frontend/package.json`
- Modify: `employee-frontend/package-lock.json`

**Interfaces:**
- Consumes: `buildTicketFlow`, `pipelineChart`, `detailChart`, `FlowStepId`, and `sentence("chartFailed", false)`
- Produces: `export function TicketFlow({ result }: { result: Result })`

- [ ] **Step 1: Install the chart packages**

Run from `employee-frontend`:

```bash
npm install mermaid @fontsource/tajawal
```

Expected: both packages appear in `dependencies` in `package.json`.

- [ ] **Step 2: Write the component**

Create `employee-frontend/src/features/review/TicketFlow.tsx`:

```tsx
import { useEffect, useRef, useState } from "react"
import "@fontsource/tajawal/arabic-400.css"
import "@fontsource/tajawal/arabic-500.css"
import { Workflow } from "lucide-react"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import type { Result } from "@/lib/types"
import { buildTicketFlow, detailChart, pipelineChart, type FlowStepId } from "./ticket-flow"
import { sentence } from "./ticket-flow-copy"

export function TicketFlow({ result }: { result: Result }) {
  const flow = buildTicketFlow(result)
  const [selectedId, setSelectedId] = useState<FlowStepId>(flow.selectedId)
  const [seenId, setSeenId] = useState(result.id)
  const [pipelineSvg, setPipelineSvg] = useState("")
  const [detailSvg, setDetailSvg] = useState("")
  const [chartError, setChartError] = useState(false)
  const renderCount = useRef(0)
  if (result.id !== seenId) {
    setSeenId(result.id)
    setSelectedId(flow.selectedId)
  }
  useEffect(() => {
    let cancelled = false
    const current = buildTicketFlow(result)
    renderCount.current += 1
    const suffix = `${result.id}-${renderCount.current}`
    ;(async () => {
      try {
        const mermaid = (await import("mermaid")).default
        mermaid.initialize({
          startOnLoad: false,
          securityLevel: "strict",
          htmlLabels: false,
          fontFamily: current.arabic ? "Tajawal, sans-serif" : "Geist Variable, sans-serif",
        })
        const pipeline = await mermaid.render(`ticket-flow-pipeline-${suffix}`, pipelineChart(current, selectedId))
        const detail = await mermaid.render(`ticket-flow-detail-${suffix}`, detailChart(current, selectedId))
        if (!cancelled) {
          setPipelineSvg(pipeline.svg)
          setDetailSvg(detail.svg)
          setChartError(false)
        }
      } catch {
        if (!cancelled) setChartError(true)
      }
    })()
    return () => {
      cancelled = true
    }
  }, [result, selectedId])
  const font = flow.arabic ? "Tajawal, sans-serif" : undefined
  return (
    <Card>
      <CardHeader>
        <CardTitle className="section-title">
          <Workflow size={17} />
          Pipeline flow
        </CardTitle>
      </CardHeader>
      <CardContent>
        <div className="flex flex-wrap gap-2">
          {flow.steps.map((step) => (
            <Button
              key={step.id}
              type="button"
              size="sm"
              variant={step.id === selectedId ? "default" : "outline"}
              aria-pressed={step.id === selectedId}
              onClick={() => setSelectedId(step.id)}
            >
              {step.name}
            </Button>
          ))}
        </div>
        {chartError ? (
          <p className="muted small">{sentence("chartFailed", false)}</p>
        ) : (
          <div style={{ fontFamily: font }}>
            <div dangerouslySetInnerHTML={{ __html: pipelineSvg }} />
            <div dangerouslySetInnerHTML={{ __html: detailSvg }} />
          </div>
        )}
      </CardContent>
    </Card>
  )
}
```

- [ ] **Step 3: Mount it above the written list**

In `TicketReviewPage.tsx`, import `TicketFlow` from `./TicketFlow`. Immediately above `<PipelineTrace result={result} />`, add `<TicketFlow result={result} />`. Do not change `PipelineTrace`.

- [ ] **Step 4: Verify**

Run from `employee-frontend`:

```bash
npm test -- src/features/review/ticket-flow.test.ts
npm run typecheck
```

Expected: tests PASS and `tsc --noEmit` exits 0.

Then run `npm run dev` and open one existing ticket at `http://localhost:5173`. Confirm the pipeline chart and the detail chart are above the written list, the highlighted step matches the open detail, choosing another English step name redraws the detail chart, and an Arabic customer message uses Tajawal for the Arabic lines. The written list is still the English trace.

- [ ] **Step 5: Commit**

```bash
git add employee-frontend/package.json employee-frontend/package-lock.json employee-frontend/src/features/review/TicketFlow.tsx employee-frontend/src/features/review/TicketReviewPage.tsx
git commit -m "$(cat <<'EOF'
feat: show the open ticket's pipeline as two Mermaid charts

EOF
)"
```
