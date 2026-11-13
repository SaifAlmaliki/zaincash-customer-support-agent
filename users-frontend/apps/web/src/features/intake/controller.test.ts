import { describe, expect, it, vi } from "vitest"
import { IntakeRequestError, type IntakeApi } from "./api"
import { IntakeController } from "./controller"
import { browserSessionStorage, memoryStorage, type SessionStorage } from "./session"
import { CUSTOMER_PHONE, attachment, emptySession, fakeApi as sharedFakeApi, review as sharedReview } from "./test/fixtures"
import type { MessageCommand, SavedSession, SessionView } from "./types"

const review = { ...sharedReview, facts: {} }

function fakeApi(overrides: Partial<SessionView> = {}): IntakeApi {
  const session = emptySession(overrides)
  return {
    ...sharedFakeApi(overrides),
    create: vi.fn(async () => ({ credentials: { session_id: "session-1", token: "token" }, session })),
    review: vi.fn(async () => session),
    upload: vi.fn(async () => ({ attachment, session })),
    remove: vi.fn(async () => session),
  }
}

describe("intake controller", () => {
  it("asks for the phone before creating a session", async () => {
    const api = fakeApi()
    const controller = new IntakeController(api, memoryStorage())
    await controller.initialize("ar")
    expect(controller.getSnapshot().needsPhone).toBe(true)
    expect(api.create).not.toHaveBeenCalled()
    await controller.initialize("ar", CUSTOMER_PHONE)
    expect(api.create).toHaveBeenCalledWith("ar", CUSTOMER_PHONE, expect.any(AbortSignal))
    expect(controller.getSnapshot().needsPhone).toBe(false)
    expect(controller.getSnapshot().session?.customer_phone).toBe(CUSTOMER_PHONE)
  })

  it("keeps the phone screen open when the server rejects the number", async () => {
    const api = fakeApi()
    vi.mocked(api.create).mockRejectedValueOnce(new IntakeRequestError("Enter a valid ZainCash phone number, for example 07701234567.", 422, "invalid_phone"))
    const controller = new IntakeController(api, memoryStorage())
    await controller.initialize("ar")
    await controller.initialize("ar", CUSTOMER_PHONE)
    expect(controller.getSnapshot()).toMatchObject({ needsPhone: true, phoneError: "invalid", session: null })
  })

  it("starts a new report for the same customer", async () => {
    const api = fakeApi()
    const controller = new IntakeController(api, memoryStorage())
    await controller.initialize("en", CUSTOMER_PHONE)
    await controller.startNew("en")
    expect(vi.mocked(api.create).mock.calls[1]?.[1]).toBe(CUSTOMER_PHONE)
  })

  it("changing the number forgets the saved session and asks again", async () => {
    const api = fakeApi()
    const storage = memoryStorage()
    const controller = new IntakeController(api, storage)
    await controller.initialize("en", CUSTOMER_PHONE)
    await controller.changeNumber()
    expect(storage.load()).toBeNull()
    expect(controller.getSnapshot()).toMatchObject({ needsPhone: true, session: null })
    expect(controller.access()).toBeNull()
  })

  it("returns to the phone screen when the saved session no longer exists", async () => {
    const storage = memoryStorage({ credentials: { session_id: "gone", token: "token" }, pending: null })
    const api = fakeApi()
    vi.mocked(api.get).mockRejectedValueOnce(new IntakeRequestError("Conversation not found.", 404, "not_owned"))
    const controller = new IntakeController(api, storage)
    await controller.initialize("ar")
    expect(controller.getSnapshot()).toMatchObject({ needsPhone: true, session: null, error: null })
    expect(storage.load()).toBeNull()
  })

  it("initializes when the browser denies access to localStorage itself", async () => {
    const denied = vi.spyOn(window, "localStorage", "get").mockImplementation(() => { throw new DOMException("Denied", "SecurityError") })
    try {
      const controller = new IntakeController(fakeApi(), browserSessionStorage())
      await controller.initialize("en", CUSTOMER_PHONE)
      expect(controller.getSnapshot().session?.id).toBe("session-1")
      expect(controller.getSnapshot().resumeUnavailable).toBe(true)
    } finally { denied.mockRestore() }
  })

  it("coalesces a double send into one logical message", async () => {
    const api = fakeApi()
    const controller = new IntakeController(api, memoryStorage())
    await controller.initialize("en", CUSTOMER_PHONE)
    await Promise.all([controller.send("same", "en", []), controller.send("same", "en", [])])
    expect(api.message).toHaveBeenCalledTimes(1)
  })
  it("retains an in-memory session across remount when storage fails", async () => {
    const api = fakeApi()
    const storage: SessionStorage = { load: () => null, save: () => { throw new Error("quota") }, clear: () => undefined }
    const controller = new IntakeController(api, storage)
    await controller.initialize("ar", CUSTOMER_PHONE)
    await controller.initialize("ar", CUSTOMER_PHONE)
    expect(api.create).toHaveBeenCalledTimes(1)
  })

  it("retry recovers failed initialization", async () => {
    const api = fakeApi()
    vi.mocked(api.create).mockRejectedValueOnce(new TypeError("offline"))
    const controller = new IntakeController(api, memoryStorage())
    await controller.initialize("ar", CUSTOMER_PHONE)
    await controller.retry()
    expect(controller.getSnapshot().session?.id).toBe("session-1")
  })

  it("reconciles a lost response then retries the accepted failed attempt", async () => {
    const api = fakeApi()
    const storage = memoryStorage()
    const controller = new IntakeController(api, storage)
    await controller.initialize("en", CUSTOMER_PHONE)
    vi.mocked(api.message).mockImplementationOnce(async (_credentials, body) => {
      vi.mocked(api.get).mockResolvedValue(emptySession({ revision: 2, turn_status: "retryable_failure", active_request_id: body.request_id }))
      throw new TypeError("offline")
    })
    await controller.send("Transfer failed", "en", [])
    await controller.retry()
    expect(api.message).toHaveBeenCalledTimes(1)
    expect(api.retry).toHaveBeenCalledTimes(1)
    expect(storage.load()?.pending).toBeNull()
  })

  it("uses the payload request ID when retrying an accepted failed message", async () => {
    const payload = {
      request_id: "message-retry-1",
      expected_revision: 1,
      text: "Transfer failed",
      language: "en" as const,
      attachment_ids: [] as string[],
    }
    const storage = memoryStorage({
      credentials: { session_id: "session-1", token: "token" },
      pending: { kind: "message", payload },
    })
    const api = fakeApi()
    vi.mocked(api.get).mockResolvedValue(
      emptySession({
        revision: 2,
        turn_status: "retryable_failure",
        active_request_id: payload.request_id,
      }),
    )
    const controller = new IntakeController(api, storage)
    await controller.initialize("en", CUSTOMER_PHONE)

    await controller.retry()

    expect(api.retry).toHaveBeenCalledWith(
      { session_id: "session-1", token: "token" },
      "message-retry-1",
      2,
      expect.any(AbortSignal),
    )
    expect(api.message).not.toHaveBeenCalled()
  })

  it("does not replace a new draft with an uncertain prior message", async () => {
    const api = fakeApi()
    const controller = new IntakeController(api, memoryStorage())
    await controller.initialize("en", CUSTOMER_PHONE)
    vi.mocked(api.message).mockRejectedValueOnce(new TypeError("offline"))
    await controller.send("first", "en", [])
    await controller.send("new correction", "en", [])
    expect(api.message).toHaveBeenCalledTimes(1)
    expect(controller.getSnapshot().error).toMatch(/retry/i)
  })

  it("a reconciled conflict allows a deliberate new action with a new identity", async () => {
    const api = fakeApi()
    const storage = memoryStorage()
    const controller = new IntakeController(api, storage)
    await controller.initialize("en", CUSTOMER_PHONE)
    vi.mocked(api.message).mockRejectedValueOnce(new IntakeRequestError("Reload", 409, "revision_conflict"))
    vi.mocked(api.get).mockResolvedValue(emptySession({ revision: 7 }))
    await controller.send("old", "en", [])
    const oldId = vi.mocked(api.message).mock.calls[0]![1].request_id
    await controller.send("corrected", "en", [])
    const body = vi.mocked(api.message).mock.calls[1]![1]
    expect(body).toMatchObject({ text: "corrected", expected_revision: 7 })
    expect(body.request_id).not.toBe(oldId)
  })

  it("reattaching a removed file starts a fresh upload operation", async () => {
    const api = fakeApi()
    const controller = new IntakeController(api, memoryStorage())
    await controller.initialize("en", CUSTOMER_PHONE)
    const file = new File(["image"], "error.png")
    await controller.upload(file, "upload-reattach-1")
    await controller.remove("att-1")
    await controller.upload(file, "upload-reattach-2")
    expect(vi.mocked(api.upload).mock.calls[1]![2]).not.toBe(vi.mocked(api.upload).mock.calls[0]![2])
  })

  it("retry reuses an uncertain upload identity and file", async () => {
    const api = fakeApi()
    const controller = new IntakeController(api, memoryStorage())
    await controller.initialize("en", CUSTOMER_PHONE)
    vi.mocked(api.upload).mockRejectedValueOnce(new TypeError("offline"))
    const file = new File(["image"], "error.png")
    await expect(controller.upload(file, "upload-retry")).rejects.toThrow()
    await controller.retry()
    expect(api.upload).toHaveBeenCalledTimes(2)
    expect(vi.mocked(api.upload).mock.calls[1]![2]).toBe(vi.mocked(api.upload).mock.calls[0]![2])
  })

  it("a late poll cannot overwrite a manual refresh", async () => {
    vi.useFakeTimers()
    const api = fakeApi({ turn_status: "processing" })
    let release!: (view: SessionView) => void
    vi.mocked(api.get).mockImplementationOnce(() => new Promise((resolve) => { release = resolve }))
    const controller = new IntakeController(api, memoryStorage())
    await controller.initialize("en", CUSTOMER_PHONE)
    await vi.advanceTimersByTimeAsync(2000)
    vi.mocked(api.get).mockResolvedValue(emptySession({ revision: 5 }))
    await controller.refresh()
    release(emptySession({ revision: 1, turn_status: "processing" }))
    await vi.advanceTimersByTimeAsync(0)
    expect(controller.getSnapshot().session?.revision).toBe(5)
    controller.dispose()
  })

  it("does not mutate a submitted report", async () => {
    const api = fakeApi({ phase: "submitted" })
    const controller = new IntakeController(api, memoryStorage())
    await controller.initialize("en", CUSTOMER_PHONE)
    await controller.send("late", "en", [])
    await controller.requestReview(true, "en")
    await controller.upload(new File(["x"], "x.png"), "upload-submitted")
    await controller.remove("att-1")
    expect(api.message).not.toHaveBeenCalled()
    expect(api.review).not.toHaveBeenCalled()
    expect(api.upload).not.toHaveBeenCalled()
    expect(api.remove).not.toHaveBeenCalled()
  })

  it("creates one session when initialized twice", async () => {
    const api = fakeApi()
    const storage = memoryStorage()
    const controller = new IntakeController(api, storage)
    await Promise.all([controller.initialize("ar", CUSTOMER_PHONE), controller.initialize("ar", CUSTOMER_PHONE)])
    expect(api.create).toHaveBeenCalledTimes(1)
    expect(storage.load()?.credentials.session_id).toBe("session-1")
  })

  it("retries a lost submission response with the original request ID", async () => {
    const api = fakeApi({ phase: "review_ready", revision: 2, review })
    const controller = new IntakeController(api, memoryStorage())
    await controller.initialize("en", CUSTOMER_PHONE)
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
        payload: {
          request_id: "saved-request",
          expected_revision: 2,
          review_id: "review-1",
          confirmed: true,
        },
      },
    })
    const api = fakeApi({ phase: "review_ready", revision: 2, review })
    const controller = new IntakeController(api, storage)
    await controller.initialize("en", CUSTOMER_PHONE)
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
    await controller.initialize("en", CUSTOMER_PHONE)
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
      pending: { kind: "message", payload },
    })
    const api = fakeApi()
    const controller = new IntakeController(api, storage)
    await controller.initialize("en", CUSTOMER_PHONE)
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
    await controller.initialize("en", CUSTOMER_PHONE)
    const file = new File([new Uint8Array([1, 2])], "error.png", { type: "image/png" })
    const uploaded = controller.upload(file, "upload-revision")
    const sent = controller.send("hello", "en", ["att-1"])
    await vi.waitFor(() => expect(api.upload).toHaveBeenCalled())
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
    await controller.initialize("en", CUSTOMER_PHONE)
    expect(controller.getSnapshot().session?.id).toBe("session-1")
    expect(controller.getSnapshot().resumeUnavailable).toBe(true)
    expect(controller.getSnapshot().error).not.toMatch(/token/i)
  })

  it("preserves resume-unavailable state when startNew cannot clear storage", async () => {
    const storage: SessionStorage = {
      load: () => null,
      save: () => undefined,
      clear: () => {
        throw new Error("denied")
      },
    }
    const api = fakeApi()
    const controller = new IntakeController(api, storage)
    await controller.initialize("en", CUSTOMER_PHONE)

    await controller.startNew("en")

    expect(controller.getSnapshot().resumeUnavailable).toBe(true)
    expect(controller.getSnapshot().error).toBe(
      "This browser cannot save the conversation for later. It stays open on this screen.",
    )
  })

  it("preserves the resume error when reboot also fails after a clear failure", async () => {
    const storage: SessionStorage = {
      load: () => null,
      save: () => undefined,
      clear: () => {
        throw new Error("denied token must not leak")
      },
    }
    const api = fakeApi()
    const controller = new IntakeController(api, storage)
    await controller.initialize("en", CUSTOMER_PHONE)
    vi.mocked(api.create).mockRejectedValueOnce(new TypeError("offline"))

    await controller.startNew("en")

    expect(controller.getSnapshot().resumeUnavailable).toBe(true)
    expect(controller.getSnapshot().error).toBe(
      "This browser cannot save the conversation for later. It stays open on this screen.",
    )
    expect(controller.getSnapshot().error).not.toMatch(/token|denied/i)
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
    await controller.initialize("en", CUSTOMER_PHONE)
    const sent = controller.send("old report", "en", [])
    await vi.waitFor(() => expect(api.message).toHaveBeenCalled())
    const started = controller.startNew("en")
    release(emptySession({ messages: [{ id: "old", role: "user", text: "old report", language: "en", created_at: "2026-10-18T09:00:00Z", attachment_ids: [] }] }))
    await sent
    await started
    expect(controller.getSnapshot().session?.messages ?? []).toEqual([])
  })

  it("shows an error when a session cannot be created", async () => {
    const api = fakeApi()
    vi.mocked(api.create).mockRejectedValueOnce(new IntakeRequestError("The conversation could not be updated. Try again.", 404, "intake_error"))
    const controller = new IntakeController(api, memoryStorage())
    await controller.initialize("en", CUSTOMER_PHONE)
    expect(controller.getSnapshot().session).toBeNull()
    expect(controller.getSnapshot().error).toMatch(/could not be updated/i)
  })

  it("stops polling an in-flight turn after the deadline", async () => {
    vi.useFakeTimers()
    const session = emptySession({ turn_status: "processing" })
    const api = fakeApi(session)
    vi.mocked(api.create).mockResolvedValue({ credentials: { session_id: "session-1", token: "token" }, session })
    vi.mocked(api.get).mockResolvedValue(session)
    const controller = new IntakeController(api, memoryStorage())
    await controller.initialize("en", CUSTOMER_PHONE)
    await vi.advanceTimersByTimeAsync(2000)
    expect(api.get).toHaveBeenCalled()
    await vi.advanceTimersByTimeAsync(70_000)
    expect(controller.getSnapshot().pollingExhausted).toBe(true)
    controller.dispose()
  })

  it("sends a quick reply with the question it answers", async () => {
    const api = fakeApi()
    const controller = new IntakeController(api, memoryStorage())
    await controller.initialize("ar", CUSTOMER_PHONE)
    await controller.send("اي", "ar", [], { message_id: "q1", key: "debited", choice: "yes" })
    expect(vi.mocked(api.message).mock.calls[0]?.[1]).toMatchObject({
      text: "اي",
      attachment_ids: [],
      answer_to: { message_id: "q1", key: "debited", choice: "yes" },
    })
  })

  it("asks for a chosen detail through the ask operation", async () => {
    const api = fakeApi()
    const controller = new IntakeController(api, memoryStorage())
    await controller.initialize("ar", CUSTOMER_PHONE)
    await controller.ask("txn_ref")
    expect(vi.mocked(api.ask).mock.calls[0]?.[1]).toMatchObject({ key: "txn_ref", expected_revision: 1 })
  })

  it("exposes the outgoing message and the activity while it is in flight", async () => {
    const api = fakeApi()
    let release!: (view: SessionView) => void
    vi.mocked(api.message).mockImplementation(() => new Promise((resolve) => { release = resolve }))
    const controller = new IntakeController(api, memoryStorage())
    await controller.initialize("en", CUSTOMER_PHONE)
    const sent = controller.send("hello", "en", [])
    await vi.waitFor(() => expect(controller.getSnapshot().busy).toBe(true))
    expect(controller.getSnapshot()).toMatchObject({ activity: "message", outgoing: { text: "hello" } })
    release(emptySession({ revision: 2 }))
    await sent
    expect(controller.getSnapshot()).toMatchObject({ busy: false, outgoing: null })
  })

  it("keeps an unsent message after a lost connection and resends it", async () => {
    const api = fakeApi()
    vi.mocked(api.message).mockRejectedValueOnce(new TypeError("offline"))
    vi.mocked(api.get).mockRejectedValueOnce(new TypeError("offline"))
    const controller = new IntakeController(api, memoryStorage())
    await controller.initialize("en", CUSTOMER_PHONE)
    await controller.send("hello", "en", [])
    expect(controller.getSnapshot().outgoing?.text).toBe("hello")
    expect(controller.getSnapshot().error).toBeTruthy()
    await controller.retry()
    const calls = vi.mocked(api.message).mock.calls
    expect(calls[1]?.[1].text).toBe("hello")
    expect(calls[1]?.[1].request_id).toBe(calls[0]?.[1].request_id)
  })

  describe("a saved unsent operation", () => {
    const credentials = { session_id: "session-1", token: "token" }
    const saved = (pending: SavedSession["pending"]) => memoryStorage({ credentials, pending })
    const message = (extra: Partial<MessageCommand> = {}): MessageCommand => ({
      request_id: "req-saved", expected_revision: 1, text: "hello", language: "en", attachment_ids: [], ...extra,
    })

    it("is replayed once with its request ID after a reload", async () => {
      const api = fakeApi({ revision: 1 })
      const storage = saved({ kind: "message", payload: message() })
      const controller = new IntakeController(api, storage)
      await controller.initialize("en")
      await vi.waitFor(() => expect(storage.load()?.pending).toBeNull())
      expect(controller.getSnapshot()).toMatchObject({ busy: false, outgoing: null })
      expect(api.message).toHaveBeenCalledTimes(1)
      expect(vi.mocked(api.message).mock.calls[0]?.[1]).toMatchObject({ request_id: "req-saved", text: "hello", expected_revision: 1 })
      await controller.refresh()
      expect(api.message).toHaveBeenCalledTimes(1)
    })

    it("is resolved by the completed view when the server already moved on", async () => {
      const api = fakeApi({ revision: 3 })
      const controller = new IntakeController(api, saved({ kind: "message", payload: message() }))
      await controller.initialize("en")
      await vi.waitFor(() => expect(api.message).toHaveBeenCalledTimes(1))
      await vi.waitFor(() => expect(controller.getSnapshot()).toMatchObject({ busy: false, outgoing: null }))
      expect(controller.getSnapshot()).toMatchObject({ error: null, restored: null })
      await controller.send("next", "en", [])
      expect(vi.mocked(api.message).mock.calls[1]?.[1]).toMatchObject({ text: "next", expected_revision: 3 })
    })

    it("keeps the answer it was answering", async () => {
      const api = fakeApi({ revision: 1 })
      const answerTo = { message_id: "q1", key: "debited", choice: "yes" as const }
      const controller = new IntakeController(api, saved({ kind: "message", payload: message({ text: "yes", answer_to: answerTo }) }))
      await controller.initialize("en")
      await vi.waitFor(() => expect(api.message).toHaveBeenCalledTimes(1))
      expect(vi.mocked(api.message).mock.calls[0]?.[1]).toMatchObject({ request_id: "req-saved", answer_to: answerTo })
    })

    it("replays a saved ask with its request ID", async () => {
      const api = fakeApi({ revision: 1 })
      const controller = new IntakeController(api, saved({ kind: "ask", payload: { request_id: "req-ask", expected_revision: 1, key: "txn_ref" } }))
      await controller.initialize("en")
      await vi.waitFor(() => expect(api.ask).toHaveBeenCalledTimes(1))
      expect(vi.mocked(api.ask).mock.calls[0]?.[1]).toEqual({ request_id: "req-ask", expected_revision: 1, key: "txn_ref" })
      expect(api.message).not.toHaveBeenCalled()
    })

    it("waits while the server is still processing, then replays", async () => {
      vi.useFakeTimers()
      try {
        const api = fakeApi({ revision: 2, turn_status: "processing" })
        const controller = new IntakeController(api, saved({ kind: "message", payload: message() }))
        await controller.initialize("en")
        expect(api.message).not.toHaveBeenCalled()
        vi.mocked(api.get).mockResolvedValue(emptySession({ revision: 3, turn_status: "idle" }))
        await vi.advanceTimersByTimeAsync(2000)
        await vi.waitFor(() => expect(api.message).toHaveBeenCalledTimes(1))
        expect(vi.mocked(api.message).mock.calls[0]?.[1].request_id).toBe("req-saved")
        controller.dispose()
      } finally {
        vi.useRealTimers()
      }
    })

    it("returns the text to the draft when the server never received it", async () => {
      const api = fakeApi({ revision: 3 })
      vi.mocked(api.message).mockRejectedValueOnce(new IntakeRequestError("The conversation changed.", 409, "revision_conflict"))
      const controller = new IntakeController(api, saved({ kind: "message", payload: message() }))
      await controller.initialize("en")
      await vi.waitFor(() => expect(controller.getSnapshot().restored?.text).toBe("hello"))
      expect(controller.getSnapshot()).toMatchObject({ busy: false, outgoing: null })
      await controller.send("hello again", "en", [])
      expect(api.message).toHaveBeenCalledTimes(2)
      expect(controller.getSnapshot().restored).toBeNull()
    })

    it("is not replayed again after a failed replay", async () => {
      const api = fakeApi({ revision: 1 })
      vi.mocked(api.message).mockRejectedValue(new TypeError("offline"))
      const controller = new IntakeController(api, saved({ kind: "message", payload: message() }))
      await controller.initialize("en")
      await vi.waitFor(() => expect(controller.getSnapshot().error).toBeTruthy())
      await controller.refresh()
      expect(api.message).toHaveBeenCalledTimes(1)
      expect(controller.getSnapshot().outgoing?.request_id).toBe("req-saved")
    })
  })

  it("shows the review activity when a failed review is retried on the server", async () => {
    const credentials = { session_id: "session-1", token: "token" }
    const api = fakeApi({ revision: 2, turn_status: "retryable_failure", active_request_id: "req-review" })
    const pending = { kind: "review" as const, payload: { request_id: "req-review", expected_revision: 1, allow_partial: true, language: "en" as const } }
    const controller = new IntakeController(api, memoryStorage({ credentials, pending }))
    const activities: (string | null)[] = []
    vi.mocked(api.retry).mockImplementation(async () => {
      activities.push(controller.getSnapshot().activity)
      return emptySession({ revision: 3 })
    })
    await controller.initialize("en")
    await controller.retry()
    expect(api.retry).toHaveBeenCalledWith(credentials, "req-review", 2, expect.any(AbortSignal))
    expect(activities).toEqual(["review"])
  })
})
