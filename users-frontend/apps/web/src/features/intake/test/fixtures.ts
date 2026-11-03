import { vi } from "vitest"
import type { IntakeApi } from "../api"
import type { Attachment, CustomerReview, SessionView } from "../types"

export function emptySession(overrides: Partial<SessionView> = {}): SessionView {
  return {
    id: "session-1",
    revision: 1,
    phase: "collecting",
    language: "en",
    turn_status: "idle",
    active_request_id: null,
    messages: [],
    attachments: [],
    readiness: { quality: "collecting", missing: ["issue"], conflicts: [], reason: "Waiting", next_key: "issue" },
    review: null,
    receipt: null,
    error_code: null,
    ...overrides,
  }
}

export const review: CustomerReview = {
  id: "review-1",
  revision: 2,
  language: "en",
  quality: "partial_context",
  text: "The transfer failed.",
  facts: {
    amount: {
      key: "amount",
      status: "unknown",
      value: null,
      normalized: null,
      evidence: [],
    },
  },
  additional_issues: [],
  unknown_keys: ["amount"],
  attachment_ids: [],
}

export const attachment: Attachment = {
  id: "att-1",
  filename: "error.png",
  mime_type: "image/png",
  size: 2,
  width: 1,
  height: 1,
  message_id: null,
  removed: false,
}

export function fakeApi(overrides: Partial<SessionView> = {}): IntakeApi {
  const session = emptySession(overrides)
  return {
    create: vi.fn(async () => ({
      credentials: { session_id: "session-1", token: "secret-token" },
      session,
    })),
    get: vi.fn(async () => session),
    message: vi.fn(async () => session),
    review: vi.fn(async (_credentials, command): Promise<SessionView> =>
      emptySession({
        ...session,
        language: command.language,
        review: { ...review, language: command.language },
      }),
    ),
    retry: vi.fn(async () => session),
    submit: vi.fn(async () => ({
      ticket_reference: "INTAKE-demo",
      submitted_at: "2026-10-18T09:00:00Z",
      processing_status: "processing" as const,
    })),
    upload: vi.fn(async () => ({
      attachment,
      session: emptySession({
        ...session,
        revision: session.revision + 1,
        attachments: [attachment],
      }),
    })),
    remove: vi.fn(async () =>
      emptySession({
        ...session,
        attachments: [{ ...attachment, removed: true }],
      }),
    ),
    image: vi.fn(async () => new Blob(["png"])),
  }
}
