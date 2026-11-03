import type {
  Attachment,
  Credentials,
  EvidenceRef,
  Fact,
  Language,
  MessageCommand,
  PendingOperation,
  Receipt,
  ReviewCommand,
  SavedSession,
  SessionView,
  SubmitCommand,
} from "./types"

export const INTAKE_FALLBACK_MESSAGE =
  "The conversation could not be updated. Try again."

export class IntakeRequestError extends Error {
  readonly status: number
  readonly code: string

  constructor(message: string, status: number, code: string) {
    super(message)
    this.name = "IntakeRequestError"
    this.status = status
    this.code = code
  }
}

function invalid(): never {
  throw new IntakeRequestError(INTAKE_FALLBACK_MESSAGE, 200, "invalid_response")
}

function isRecord(value: unknown): value is Record<string, unknown> {
  return Boolean(value) && typeof value === "object" && !Array.isArray(value)
}

function stringList(value: unknown): value is string[] {
  return Array.isArray(value) && value.every((item) => typeof item === "string")
}

function nullableString(value: unknown): boolean {
  return value === null || typeof value === "string"
}

function finiteNonnegative(value: unknown): value is number {
  return typeof value === "number" && Number.isFinite(value) && value >= 0
}

function revision(value: unknown): value is number {
  return typeof value === "number" && Number.isInteger(value) && value >= 0
}

function language(value: unknown): value is Language {
  return value === "ar" || value === "en"
}

function validEvidence(value: unknown): value is EvidenceRef {
  return isRecord(value) &&
    (value.kind === "message" || value.kind === "image") &&
    typeof value.source_id === "string" &&
    typeof value.quote === "string"
}

function validEvidenceList(value: unknown): value is EvidenceRef[] {
  return Array.isArray(value) && value.every(validEvidence)
}

function validFact(value: unknown): value is Fact {
  return isRecord(value) &&
    typeof value.key === "string" &&
    ["known", "missing", "unknown", "conflicting", "not_applicable"].includes(String(value.status)) &&
    nullableString(value.value) &&
    (value.normalized === undefined || nullableString(value.normalized)) &&
    validEvidenceList(value.evidence) &&
    (value.supersedes === undefined || validEvidenceList(value.supersedes))
}

function validAttachment(value: unknown): value is Attachment {
  return isRecord(value) &&
    typeof value.id === "string" &&
    typeof value.filename === "string" &&
    ["image/png", "image/jpeg", "image/webp"].includes(String(value.mime_type)) &&
    finiteNonnegative(value.size) &&
    finiteNonnegative(value.width) &&
    finiteNonnegative(value.height) &&
    typeof value.removed === "boolean" &&
    nullableString(value.message_id)
}

function validMessage(value: unknown): boolean {
  return isRecord(value) &&
    typeof value.id === "string" &&
    typeof value.text === "string" &&
    (value.role === "user" || value.role === "assistant") &&
    language(value.language) &&
    typeof value.created_at === "string" &&
    stringList(value.attachment_ids)
}

function validReadiness(value: unknown): boolean {
  return isRecord(value) &&
    ["collecting", "sufficient_context", "partial_context"].includes(String(value.quality)) &&
    stringList(value.missing) &&
    stringList(value.conflicts) &&
    typeof value.reason === "string" &&
    nullableString(value.next_key)
}

function validReview(value: unknown): boolean {
  return isRecord(value) &&
    typeof value.id === "string" &&
    revision(value.revision) &&
    language(value.language) &&
    (value.quality === "sufficient_context" || value.quality === "partial_context") &&
    typeof value.text === "string" &&
    isRecord(value.facts) &&
    Object.values(value.facts).every(validFact) &&
    Array.isArray(value.additional_issues) &&
    value.additional_issues.every(validFact) &&
    stringList(value.unknown_keys) &&
    stringList(value.attachment_ids)
}

export function parseCredentials(value: unknown): Credentials {
  if (!isRecord(value) || typeof value.session_id !== "string" || !value.session_id ||
      typeof value.token !== "string" || !value.token) invalid()
  return { session_id: value.session_id, token: value.token }
}

export function parseAttachment(value: unknown): Attachment {
  if (!validAttachment(value)) invalid()
  return value
}

export function parseReceipt(value: unknown): Receipt {
  if (!isRecord(value) || typeof value.ticket_reference !== "string" || !value.ticket_reference ||
      typeof value.submitted_at !== "string" || !Number.isFinite(Date.parse(value.submitted_at)) ||
      !["processing", "ready_for_employee", "needs_attention"].includes(String(value.processing_status))) {
    invalid()
  }
  return value as unknown as Receipt
}

export function parseSession(value: unknown): SessionView {
  if (!isRecord(value) || typeof value.id !== "string" || !revision(value.revision) ||
      !["collecting", "review_ready", "submitted"].includes(String(value.phase)) ||
      !language(value.language) ||
      !["idle", "processing", "retryable_failure"].includes(String(value.turn_status)) ||
      !nullableString(value.active_request_id) ||
      !Array.isArray(value.messages) || !value.messages.every(validMessage) ||
      !Array.isArray(value.attachments) || !value.attachments.every(validAttachment) ||
      !validReadiness(value.readiness) ||
      (value.review !== null && !validReview(value.review)) ||
      !nullableString(value.error_code)) {
    invalid()
  }
  if (value.receipt !== null) parseReceipt(value.receipt)
  return value as unknown as SessionView
}

function requestIdentity(value: unknown): value is Record<string, unknown> & {
  request_id: string
  expected_revision: number
} {
  return isRecord(value) && typeof value.request_id === "string" && !!value.request_id &&
    revision(value.expected_revision)
}

function validMessageCommand(value: unknown): value is MessageCommand {
  return requestIdentity(value) && typeof value.text === "string" &&
    language(value.language) && stringList(value.attachment_ids)
}

function validReviewCommand(value: unknown): value is ReviewCommand {
  return requestIdentity(value) && typeof value.allow_partial === "boolean" &&
    language(value.language)
}

function validSubmitCommand(value: unknown): value is SubmitCommand {
  return requestIdentity(value) && typeof value.review_id === "string" &&
    value.confirmed === true
}

function parsePendingOperation(value: unknown): PendingOperation | null {
  if (!isRecord(value)) return null
  if (value.kind === "message" && validMessageCommand(value.payload)) {
    return { kind: "message", payload: value.payload }
  }
  if (value.kind === "review" && validReviewCommand(value.payload)) {
    return { kind: "review", payload: value.payload }
  }
  if (value.kind === "submit" && validSubmitCommand(value.payload)) {
    return { kind: "submit", payload: value.payload }
  }
  return null
}

export function parseSavedSession(value: unknown): SavedSession | null {
  try {
    if (!isRecord(value)) return null
    const credentials = parseCredentials(value.credentials)
    if (value.pending === null) return { credentials, pending: null }
    if (!isRecord(value.pending) || !isRecord(value.pending.payload)) return null
    if ("request_id" in value.pending &&
        value.pending.request_id !== value.pending.payload.request_id) return null
    const pending = parsePendingOperation(value.pending)
    return pending ? { credentials, pending } : null
  } catch {
    return null
  }
}
