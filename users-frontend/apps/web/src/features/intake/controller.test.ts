import { describe, expect, it, vi } from "vitest"
import { IntakeRequestError, type IntakeApi } from "./api"
import { IntakeController } from "./controller"
import { memoryStorage, type SessionStorage } from "./session"
import type { SessionView } from "./types"

function emptySession(overrides: Partial<SessionView> = {}): SessionView {
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

function fakeApi(overrides: Partial<SessionView> = {}): IntakeApi {
  const session = emptySession(overrides)
  return {
    create: vi.fn(async () => ({ credentials: { session_id: "session-1", token: "token" }, session })),
    get: vi.fn(async () => session),
    message: vi.fn(async () => session),
    review: vi.fn(async () => session),
    retry: vi.fn(async () => session),
    submit: vi.fn(async () => ({
      ticket_reference: "INTAKE-demo",
      submitted_at: "2026-10-18T09:00:00Z",
      processing_status: "processing" as const,
    })),
    upload: vi.fn(async () => ({
      attachment: {
        id: "att-1",
        filename: "error.png",
        mime_type: "image/png",
        size: 2,
        width: 1,
        height: 1,
        message_id: null,
        removed: false,
      },
      session,
    })),
    remove: vi.fn(async () => session),
    image: vi.fn(async () => new Blob(["png"])),
  }
}

const review = {
  id: "review-1",
  revision: 2,
  language: "en" as const,
  quality: "partial_context" as const,
  text: "The transfer failed.",
  facts: {},
  additional_issues: [],
  unknown_keys: ["amount"],
  attachment_ids: [],
}

describe("intake controller", () => {
  it("creates one session when initialized twice", async () => {
    const api = fakeApi()
    const storage = memoryStorage()
    const controller = new IntakeController(api, storage)
    await Promise.all([controller.initialize("ar"), controller.initialize("ar")])
    expect(api.create).toHaveBeenCalledTimes(1)
    expect(storage.load()?.credentials.session_id).toBe("session-1")
  })

  it("retries a lost submission response with the original request ID", async () => {
    const api = fakeApi({ phase: "review_ready", revision: 2, review })
    const controller = new IntakeController(api, memoryStorage())
    await controller.initialize("en")
    vi.mocked(api.submit).mockRejectedValueOnce(new TypeError("connection lost"))
    await controller.submit()
    const original = vi.mocked(api.submit).mock.calls[0]?.[1].request_id
    await controller.retry()
    expect(vi.mocked(api.submit).mock.calls[1]?.[1].request_id).toBe(original)
  })

  it("replays a saved submission after reload", async () => {
    const storage = memoryStorage({
      credentials: { session_id: "session-1", token: "token" },
      pending: {
        kind: "submit",
        request_id: "saved-request",
        payload: { request_id: "saved-request", expected_revision: 2, review_id: "review-1", confirmed: true },
      },
    })
    const api = fakeApi({ phase: "review_ready", revision: 2, review })
    const controller = new IntakeController(api, storage)
    await controller.initialize("en")
    expect(api.create).not.toHaveBeenCalled()
    await controller.retry()
    expect(vi.mocked(api.submit).mock.calls[0]?.[1].request_id).toBe("saved-request")
  })

  it("keeps the server session when another tab changed the review", async () => {
    const current = emptySession({ phase: "review_ready", revision: 4, review: { ...review, text: "Updated on the other tab." } })
    const api = fakeApi({ phase: "review_ready", revision: 2, review })
    vi.mocked(api.review).mockRejectedValueOnce(new IntakeRequestError("Reload the current conversation.", 409, "revision_conflict"))
    vi.mocked(api.get).mockResolvedValue(current)
    const controller = new IntakeController(api, memoryStorage())
    await controller.initialize("en")
    await controller.requestReview(true, "en")
    expect(controller.getSnapshot().session?.review?.text).toBe("Updated on the other tab.")
    expect(controller.getSnapshot().error).toMatch(/Reload/)
  })

  it("retries a message with the original body", async () => {
    const payload = {
      request_id: "message-1",
      expected_revision: 1,
      text: "first",
      language: "en" as const,
      attachment_ids: [] as string[],
    }
    const storage = memoryStorage({
      credentials: { session_id: "session-1", token: "token" },
      pending: { kind: "message", request_id: "message-1", payload },
    })
    const api = fakeApi()
    const controller = new IntakeController(api, storage)
    await controller.initialize("en")
    await controller.retry()
    expect(vi.mocked(api.message).mock.calls[0]?.[1]).toEqual(payload)
  })

  it("sends a message only after the upload revision is current", async () => {
    const api = fakeApi()
    let release: (value: Awaited<ReturnType<IntakeApi["upload"]>>) => void = () => undefined
    vi.mocked(api.upload).mockImplementation(
      () =>
        new Promise((resolve) => {
          release = resolve
        }),
    )
    const controller = new IntakeController(api, memoryStorage())
    await controller.initialize("en")
    const file = new File([new Uint8Array([1, 2])], "error.png", { type: "image/png" })
    const uploaded = controller.upload(file)
    const sent = controller.send("hello", "en", ["att-1"])
    release({
      attachment: {
        id: "att-1",
        filename: "error.png",
        mime_type: "image/png",
        size: 2,
        width: 1,
        height: 1,
        message_id: null,
        removed: false,
      },
      session: emptySession({ revision: 4 }),
    })
    await uploaded
    await sent
    expect(vi.mocked(api.message).mock.calls[0]?.[1].expected_revision).toBe(4)
  })

  it("keeps the in-memory session when storage cannot save", async () => {
    const storage: SessionStorage = {
      load: () => null,
      save: () => {
        throw new Error("quota")
      },
      clear: () => undefined,
    }
    const api = fakeApi()
    const controller = new IntakeController(api, storage)
    await controller.initialize("en")
    expect(controller.getSnapshot().session?.id).toBe("session-1")
    expect(controller.getSnapshot().resumeUnavailable).toBe(true)
    expect(controller.getSnapshot().error).not.toMatch(/token/i)
  })

  it("ignores a late reply from the previous report", async () => {
    const api = fakeApi()
    let release: (value: SessionView) => void = () => undefined
    vi.mocked(api.message).mockImplementation(
      () =>
        new Promise((resolve) => {
          release = resolve
        }),
    )
    const controller = new IntakeController(api, memoryStorage())
    await controller.initialize("en")
    const sent = controller.send("old report", "en", [])
    const started = controller.startNew("en")
    release(emptySession({ messages: [{ id: "old", role: "user", text: "old report", language: "en", created_at: "2026-10-18T09:00:00Z", attachment_ids: [] }] }))
    await sent
    await started
    expect(controller.getSnapshot().session?.messages ?? []).toEqual([])
  })

  it("stops polling an in-flight turn after the deadline", async () => {
    vi.useFakeTimers()
    const session = emptySession({ turn_status: "processing" })
    const api = fakeApi(session)
    vi.mocked(api.create).mockResolvedValue({ credentials: { session_id: "session-1", token: "token" }, session })
    vi.mocked(api.get).mockResolvedValue(session)
    const controller = new IntakeController(api, memoryStorage())
    await controller.initialize("en")
    await vi.advanceTimersByTimeAsync(2000)
    expect(api.get).toHaveBeenCalled()
    await vi.advanceTimersByTimeAsync(70_000)
    expect(controller.getSnapshot().pollingExhausted).toBe(true)
    controller.dispose()
    vi.useRealTimers()
  })
})
