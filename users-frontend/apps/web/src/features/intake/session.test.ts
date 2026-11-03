import { describe, expect, it } from "vitest"
import { browserSessionStorage } from "./session"
import type { SavedSession } from "./types"

function storageWith(raw: string | null): Storage {
  return {
    length: 0,
    clear: () => undefined,
    getItem: () => raw,
    key: () => null,
    removeItem: () => undefined,
    setItem: () => undefined,
  }
}

const credentials = { session_id: "session-1", token: "token" }
const messagePayload = {
  request_id: "message-1",
  expected_revision: 1,
  text: "Transfer failed",
  language: "en" as const,
  attachment_ids: [] as string[],
}

const invalidValues: Array<[string, unknown]> = [
  ["null", null],
  ["array", []],
  ["missing token", { credentials: { session_id: "session-1" }, pending: null }],
  ["mismatched kind and payload", { credentials, pending: { kind: "message", payload: { request_id: "submit-1", expected_revision: 1, review_id: "review-1", confirmed: true } } }],
  ["conflicting legacy request ID", { credentials, pending: { kind: "message", request_id: "other-id", payload: messagePayload } }],
  ["invalid revision", { credentials, pending: { kind: "message", payload: { ...messagePayload, expected_revision: -1 } } }],
]

describe("browser session storage", () => {
  it.each(invalidValues)("rejects %s", (_name, value) => {
    const storage = browserSessionStorage(storageWith(JSON.stringify(value)))
    expect(storage.load()).toBeNull()
  })

  it("returns null for malformed JSON", () => {
    expect(browserSessionStorage(storageWith("{")).load()).toBeNull()
  })

  it("accepts and replays a valid pending operation", () => {
    const saved: SavedSession = {
      credentials,
      pending: { kind: "message", payload: messagePayload },
    }
    const storage = browserSessionStorage(storageWith(JSON.stringify(saved)))
    expect(storage.load()).toEqual(saved)
  })

  it("accepts a legacy outer ID only when it equals the payload ID", () => {
    const storage = browserSessionStorage(storageWith(JSON.stringify({
      credentials,
      pending: { kind: "message", request_id: "message-1", payload: messagePayload },
    })))
    expect(storage.load()).toEqual({
      credentials,
      pending: { kind: "message", payload: messagePayload },
    })
  })
})
