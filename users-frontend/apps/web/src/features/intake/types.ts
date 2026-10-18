export type Language = "ar" | "en"
export type Phase = "collecting" | "review_ready" | "submitted"
export type TurnStatus = "idle" | "processing" | "retryable_failure"
export type Quality = "collecting" | "sufficient_context" | "partial_context"
export type ProcessingStatus = "processing" | "ready_for_employee" | "needs_attention"

export type EvidenceRef = {
  kind: "message" | "image"
  source_id: string
  quote: string
}

export type Fact = {
  key: string
  status: "known" | "missing" | "unknown" | "conflicting" | "not_applicable"
  value?: string | null
  normalized?: string | null
  evidence?: EvidenceRef[]
  supersedes?: EvidenceRef[]
}

export type Readiness = {
  quality: Quality
  missing: string[]
  conflicts: string[]
  reason: string
  next_key: string | null
}

export type IntakeMessage = {
  id: string
  role: "user" | "assistant"
  text: string
  language: Language
  created_at: string
  attachment_ids: string[]
}

export type Attachment = {
  id: string
  filename: string
  mime_type: string
  size: number
  width: number
  height: number
  message_id: string | null
  removed: boolean
}

export type CustomerReview = {
  id: string
  revision: number
  language: Language
  quality: "sufficient_context" | "partial_context"
  text: string
  facts: Record<string, Fact>
  additional_issues: Fact[]
  unknown_keys: string[]
  attachment_ids: string[]
}

export type Receipt = {
  ticket_reference: string
  submitted_at: string
  processing_status: ProcessingStatus
}

export type SessionView = {
  id: string
  revision: number
  phase: Phase
  language: Language
  turn_status: TurnStatus
  active_request_id: string | null
  messages: IntakeMessage[]
  attachments: Attachment[]
  readiness: Readiness
  review: CustomerReview | null
  receipt: Receipt | null
  error_code: string | null
}

export type Credentials = {
  session_id: string
  token: string
}

export type MessageCommand = {
  request_id: string
  expected_revision: number
  text: string
  language: Language
  attachment_ids: string[]
}

export type ReviewCommand = {
  request_id: string
  expected_revision: number
  allow_partial: boolean
  language: Language
}

export type SubmitCommand = {
  request_id: string
  expected_revision: number
  review_id: string
  confirmed: true
}

export type RemoveCommand = {
  request_id: string
  expected_revision: number
}

export type PendingOperation = {
  kind: "message" | "review" | "submit"
  request_id: string
  payload: MessageCommand | ReviewCommand | SubmitCommand
}

export type SavedSession = {
  credentials: Credentials
  pending: PendingOperation | null
}
