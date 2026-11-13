import { describe, expect, it } from "vitest"
import {
  IntakeRequestError,
  parseCredentials,
  parseSavedSession,
  parseSession,
} from "./contracts"
import { attachment, emptySession, review } from "./test/fixtures"

const populated = emptySession({
  phase: "review_ready",
  active_request_id: null,
  messages: [
    {
      id: "m1",
      role: "user",
      text: "Transfer failed",
      language: "en",
      created_at: "2026-10-18T09:00:00Z",
      attachment_ids: ["att-1"],
    },
  ],
  attachments: [attachment],
  review: {
    ...review,
    facts: {
      amount: {
        key: "amount",
        status: "known",
        value: "50000",
        normalized: "50000",
        evidence: [{ kind: "message", source_id: "m1", quote: "50000" }],
        supersedes: [],
      },
    },
  },
})

const malformed: Array<[string, unknown]> = [
  ["customer phone", { ...populated, customer_phone: 4 }],
  ["missing customer phone", { ...populated, customer_phone: "" }],
  ["active request ID", { ...populated, active_request_id: 4 }],
  ["error code", { ...populated, error_code: 4 }],
  ["message language", { ...populated, messages: [{ ...populated.messages[0]!, language: "fr" }] }],
  ["message timestamp", { ...populated, messages: [{ ...populated.messages[0]!, created_at: 4 }] }],
  ["message attachments", { ...populated, messages: [{ ...populated.messages[0]!, attachment_ids: [4] }] }],
  ["readiness quality", { ...populated, readiness: { ...populated.readiness, quality: "ready" } }],
  ["readiness reason", { ...populated, readiness: { ...populated.readiness, reason: 4 } }],
  ["readiness next key", { ...populated, readiness: { ...populated.readiness, next_key: 4 } }],
  ["review revision", { ...populated, review: { ...populated.review!, revision: "2" } }],
  ["review language", { ...populated, review: { ...populated.review!, language: "fr" } }],
  ["review quality", { ...populated, review: { ...populated.review!, quality: "collecting" } }],
  ["required fact value", { ...populated, review: { ...populated.review!, facts: { amount: { ...populated.review!.facts.amount!, value: undefined } } } }],
  ["required fact evidence", { ...populated, review: { ...populated.review!, facts: { amount: { ...populated.review!.facts.amount!, evidence: undefined } } } }],
  ["fact evidence entry", { ...populated, review: { ...populated.review!, facts: { amount: { ...populated.review!.facts.amount!, evidence: [{}] } } } }],
  ["fact supersedes entry", { ...populated, review: { ...populated.review!, facts: { amount: { ...populated.review!.facts.amount!, supersedes: [{}] } } } }],
  ["additional issue", { ...populated, review: { ...populated.review!, additional_issues: [{}] } }],
  ["pending question kind", { ...populated, pending_question: { key: "amount", message_id: "m1", text: "?", reason: "", answer_kind: "money", choices: [], attempt: 1 } }],
  ["pending question choice", { ...populated, pending_question: { key: "amount", message_id: "m1", text: "?", reason: "", answer_kind: "amount", choices: ["maybe"], attempt: 1 } }],
  ["progress tier", { ...populated, progress: [{ key: "amount", tier: "later", status: "known", display: null }] }],
  ["progress status", { ...populated, progress: [{ key: "amount", tier: "required", status: "done", display: null }] }],
]

describe("intake runtime contracts", () => {
  it.each(malformed)("rejects malformed %s", (_name, value) => {
    expect(() => parseSession(value)).toThrow(IntakeRequestError)
    expect(() => parseSession(value)).toThrow(/could not be updated/i)
  })

  it.each([Number.NaN, Number.POSITIVE_INFINITY, Number.NEGATIVE_INFINITY])(
    "rejects non-finite nested attachment number %s",
    (number) => {
      for (const key of ["size", "width", "height"] as const) {
        const parse = () =>
          parseSession({
            ...populated,
            attachments: [{ ...attachment, [key]: number }],
          })
        expect(parse).toThrow(IntakeRequestError)
        expect(parse).toThrow(expect.objectContaining({ code: "invalid_response" }))
      }
    },
  )

  it.each([
    { session_id: 1, token: "token" },
    { session_id: "session-1", token: {} },
    { session_id: "", token: "token" },
    { session_id: "session-1", token: "" },
  ])("rejects invalid credentials %#", (value) => {
    expect(() => parseCredentials(value)).toThrow(IntakeRequestError)
  })

  it("accepts the fully populated valid session", () => {
    expect(parseSession(populated)).toEqual(populated)
  })

  it("fills the interview fields for an older server", () => {
    const older: Record<string, unknown> = { ...populated }
    delete older.pending_question
    delete older.progress
    expect(parseSession(older)).toMatchObject({ pending_question: null, progress: [] })
  })

  it("restores a saved quick reply and a saved ask", () => {
    const credentials = { session_id: "session-1", token: "token" }
    const answer = { request_id: "r1", expected_revision: 2, text: "اي", language: "ar", attachment_ids: [], answer_to: { message_id: "q1", key: "debited", choice: "yes" } }
    expect(parseSavedSession({ credentials, pending: { kind: "message", payload: answer } })?.pending).toEqual({ kind: "message", payload: answer })
    const ask = { request_id: "r2", expected_revision: 2, key: "txn_ref" }
    expect(parseSavedSession({ credentials, pending: { kind: "ask", payload: ask } })?.pending).toEqual({ kind: "ask", payload: ask })
    expect(parseSavedSession({ credentials, pending: { kind: "message", payload: { ...answer, answer_to: { key: "debited" } } } })).toBeNull()
  })
})
