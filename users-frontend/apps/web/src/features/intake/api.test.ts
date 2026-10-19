import { describe, expect, it, vi } from "vitest"
import { createIntakeApi, IntakeRequestError, parseReceipt, parseSession } from "./api"
import type { SessionView } from "./types"

const session: SessionView = {
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
}

function jsonResponse(body: unknown, status = 200) {
  return new Response(JSON.stringify(body), { status, headers: { "Content-Type": "application/json" } })
}

describe("intake api", () => {
  it("rejects incomplete or invalid session projections before rendering", () => {
    expect(() => parseSession({ id: "s", revision: 1, phase: "collecting" })).toThrow(IntakeRequestError)
    expect(() => parseSession({ ...session, phase: "oops" })).toThrow(IntakeRequestError)
    expect(() => parseSession({ ...session, attachments: [{}] })).toThrow(IntakeRequestError)
    expect(() => parseReceipt({ ticket_reference: "INTAKE-x", processing_status: "resolved" })).toThrow(IntakeRequestError)
  })
  it("sends the bearer token and rejects an incomplete session", async () => {
    const fetchMock = vi.fn(async (_url: string, init?: RequestInit) => {
      const headers = new Headers(init?.headers)
      expect(headers.get("Authorization")).toBe("Bearer secret-token")
      expect(String(init?.body)).not.toContain("secret-token")
      return jsonResponse({ id: "session-1" })
    })
    vi.stubGlobal("fetch", fetchMock)
    const api = createIntakeApi("http://intake.test/api/intake")
    await expect(api.get({ session_id: "session-1", token: "secret-token" })).rejects.toBeInstanceOf(IntakeRequestError)
    expect(String(fetchMock.mock.calls[0]?.[0])).not.toContain("secret-token")
    vi.unstubAllGlobals()
  })

  it("uploads with progress and without a manual multipart content type", async () => {
    const sent: { headers: Record<string, string>; body: FormData | null } = { headers: {}, body: null }
    class FakeXHR {
      upload = { onprogress: null as ((event: ProgressEvent) => void) | null }
      status = 201
      responseText = JSON.stringify({
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
      })
      onload: (() => void) | null = null
      onerror: (() => void) | null = null
      onabort: (() => void) | null = null
      open() {}
      setRequestHeader(name: string, value: string) {
        sent.headers[name] = value
      }
      send(body: FormData) {
        sent.body = body
        this.upload.onprogress?.({ lengthComputable: true, loaded: 2, total: 2 } as ProgressEvent)
        this.onload?.()
      }
      abort() {}
    }
    vi.stubGlobal("XMLHttpRequest", FakeXHR)
    const api = createIntakeApi("/api/intake")
    const progress: number[] = []
    const file = new File([new Uint8Array([1, 2])], "error.png", { type: "image/png" })
    const result = await api.upload({ session_id: "session-1", token: "secret-token" }, file, "req-1", 3, (fraction) => {
      progress.push(fraction)
    })
    expect(result.session.id).toBe("session-1")
    expect(sent.headers.Authorization).toBe("Bearer secret-token")
    expect(sent.headers["Content-Type"]).toBeUndefined()
    expect(sent.body?.get("request_id")).toBe("req-1")
    expect(progress).toEqual([1])
    expect(String(sent.body?.get("file"))).not.toContain("secret-token")
    vi.unstubAllGlobals()
  })
})
