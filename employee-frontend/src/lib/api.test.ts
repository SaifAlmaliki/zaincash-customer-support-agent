import { afterEach, expect, it, vi } from "vitest"
import { ApiError, adminApi, api, loadQueue } from "./api"
import { getAdminSession, setAdminSession } from "./admin-session"

afterEach(() => {
  vi.unstubAllGlobals()
  vi.restoreAllMocks()
})

it("loads subsequent API pages so ticket 501 remains searchable and exportable", async () => {
  const fetch = vi.fn(async (url: string) => {
    const offset = Number(
      new URL(url, "http://localhost").searchParams.get("offset") || 0
    )
    const items = Array.from({ length: offset === 0 ? 500 : 1 }, (_, i) => ({
      id: offset + i + 1,
    }))
    return new Response(JSON.stringify({ items, total: 501 }), { status: 200 })
  })
  vi.stubGlobal("fetch", fetch)
  const result = await loadQueue("/results?limit=500", {})
  expect(result.items).toHaveLength(501)
  expect(result.items.at(-1)?.id).toBe(501)
  expect(fetch).toHaveBeenCalledTimes(2)
})

it("reports an inconsistent queue snapshot instead of silently dropping rows", async () => {
  vi.stubGlobal(
    "fetch",
    vi.fn(async (url: string) => {
      const offset = Number(
        new URL(url, "http://localhost").searchParams.get("offset") || 0
      )
      return new Response(
        JSON.stringify({ items: offset ? [] : [{ id: 1 }], total: 2 }),
        { status: 200 }
      )
    })
  )
  await expect(loadQueue("/results?limit=500", {})).rejects.toThrow(
    /queue changed/i
  )
})

it("starts every new run with Jev classification", async () => {
  const fetchMock = vi.spyOn(globalThis, "fetch").mockResolvedValue(
    new Response("{}", { status: 200, headers: { "Content-Type": "application/json" } }),
  )
  await api.startRun([{ text: "شكد العمولة", channel: "app", customer_phone: "07701234567" }])
  const options = fetchMock.mock.calls[0][1]
  expect(JSON.parse(String(options?.body)).mode).toBe("jev")
})

it("names the ticket row in validation errors", async () => {
  vi.spyOn(globalThis, "fetch").mockResolvedValue(new Response(JSON.stringify({
    detail: [{ loc: ["body", "tickets", 1, "customer_phone"], msg: "Value error, Enter a valid ZainCash phone number, for example 07701234567." }],
  }), { status: 422 }))
  await expect(api.startRun([])).rejects.toThrow("Ticket 2: Value error, Enter a valid ZainCash phone number")
})

it("sends the admin token and locks the session when it is rejected", async () => {
  setAdminSession({ token: "secret", name: "Sara" })
  const fetchMock = vi.spyOn(globalThis, "fetch").mockResolvedValue(
    new Response(JSON.stringify({ detail: "invalid_admin_token" }), { status: 401 }),
  )
  await expect(adminApi.models()).rejects.toMatchObject({ status: 401, message: "invalid_admin_token" })
  const [url, options] = fetchMock.mock.calls[0]
  expect(url).toBe("/api/admin/models")
  expect((options?.headers as Record<string, string>)["X-Admin-Token"]).toBe("secret")
  expect(getAdminSession()).toBeNull()
})

it("keeps the admin session on other errors and reports the status", async () => {
  setAdminSession({ token: "secret", name: "Sara" })
  vi.spyOn(globalThis, "fetch").mockResolvedValue(
    new Response(JSON.stringify({ detail: "Model test failed: no tool call" }), { status: 422 }),
  )
  const error = await adminApi
    .save("draft", { provider: "ollama", model: "qwen3:4b", options: {} }, "Sara")
    .catch((e: unknown) => e)
  expect(error).toBeInstanceOf(ApiError)
  expect((error as ApiError).status).toBe(422)
  expect((error as ApiError).message).toBe("Model test failed: no tool call")
  expect(getAdminSession()).not.toBeNull()
  setAdminSession(null)
})

it("saves with the admin name and sends model options", async () => {
  setAdminSession({ token: "secret", name: "Sara" })
  const fetchMock = vi.spyOn(globalThis, "fetch").mockResolvedValue(
    new Response("{}", { status: 200, headers: { "Content-Type": "application/json" } }),
  )
  await adminApi.save("draft", { provider: "ollama", model: "qwen3:4b", options: { think: false } }, "Sara")
  const [url, options] = fetchMock.mock.calls[0]
  expect(url).toBe("/api/admin/models/draft")
  expect(options?.method).toBe("PUT")
  expect(JSON.parse(String(options?.body))).toEqual({
    provider: "ollama", model: "qwen3:4b", options: { think: false }, changed_by: "Sara",
  })
  setAdminSession(null)
})
