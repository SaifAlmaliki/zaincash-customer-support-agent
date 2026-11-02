import { afterEach, expect, it, vi } from "vitest"
import { loadRunResults, RUN_RESULT_CONCURRENCY } from "./run-results"

function json(value: unknown, status = 200) {
  return new Response(JSON.stringify(value), {
    status,
    headers: { "Content-Type": "application/json" },
  })
}

function deferred<T>() {
  let resolve!: (value: T | PromiseLike<T>) => void
  let reject!: (reason?: unknown) => void
  const promise = new Promise<T>((res, rej) => {
    resolve = res
    reject = rej
  })
  return { promise, resolve, reject }
}

afterEach(() => {
  vi.unstubAllGlobals()
  vi.restoreAllMocks()
})

it("loads every detail once, preserves order, and respects the in-flight limit", async () => {
  const ids = Array.from({ length: 12 }, (_, index) => index + 1)
  const gate = deferred<void>()
  const detailUrls: string[] = []
  let active = 0
  let maximumActive = 0
  const fetchMock = vi.fn(async (input: RequestInfo | URL) => {
    const url = String(input)
    if (url.includes("run_id=")) return json({ items: ids.map((id) => ({ id })) })
    detailUrls.push(url)
    active += 1
    maximumActive = Math.max(maximumActive, active)
    await gate.promise
    active -= 1
    const id = Number(url.split("/").at(-1))
    return json({ id, ticket: { external_id: `T-${id}` } })
  })
  vi.stubGlobal("fetch", fetchMock)

  const pending = loadRunResults("/results?run_id=3&limit=500", {})
  await vi.waitFor(() => expect(active).toBe(RUN_RESULT_CONCURRENCY))
  gate.resolve()
  const results = await pending

  expect(maximumActive).toBe(RUN_RESULT_CONCURRENCY)
  expect(results.map((item) => item.id)).toEqual(ids)
  expect(detailUrls).toHaveLength(ids.length)
  expect(new Set(detailUrls).size).toBe(ids.length)
})

it("returns an empty result without requesting details", async () => {
  const fetchMock = vi.fn(async () => json({ items: [] }))
  vi.stubGlobal("fetch", fetchMock)
  await expect(loadRunResults("/results?run_id=3&limit=500", {})).resolves.toEqual([])
  expect(fetchMock).toHaveBeenCalledTimes(1)
})

it("preserves a detail failure through the existing request error path", async () => {
  vi.stubGlobal("fetch", vi.fn(async (input: RequestInfo | URL) => {
    const url = String(input)
    if (url.includes("run_id=")) return json({ items: [{ id: 1 }, { id: 2 }] })
    if (url.endsWith("/2")) return json({ detail: "detail failed" }, 500)
    return json({ id: 1 })
  }))
  await expect(loadRunResults("/results?run_id=3&limit=500", {})).rejects.toThrow("detail failed")
})

it("preserves a list failure without requesting details", async () => {
  const fetchMock = vi.fn(async () => json({ detail: "list failed" }, 503))
  vi.stubGlobal("fetch", fetchMock)
  await expect(loadRunResults("/results?run_id=3&limit=500", {})).rejects.toThrow("list failed")
  expect(fetchMock).toHaveBeenCalledTimes(1)
})

it("propagates the caller signal to detail requests and rejects on abort", async () => {
  const controller = new AbortController()
  let detailSignal: AbortSignal | null | undefined
  vi.stubGlobal("fetch", vi.fn(async (input: RequestInfo | URL, init?: RequestInit) => {
    if (String(input).includes("run_id=")) return json({ items: [{ id: 1 }] })
    detailSignal = init?.signal
    return new Promise<Response>((_resolve, reject) => {
      init?.signal?.addEventListener("abort", () => reject(new DOMException("Aborted", "AbortError")), { once: true })
    })
  }))

  const pending = loadRunResults("/results?run_id=3&limit=500", { signal: controller.signal })
  const rejection = expect(pending).rejects.toMatchObject({ name: "AbortError" })
  await vi.waitFor(() => expect(detailSignal).toBe(controller.signal))
  controller.abort()
  await rejection
})

it("rejects a pre-aborted request before loading detail items", async () => {
  const controller = new AbortController()
  controller.abort()
  const fetchMock = vi.fn(async (_input: RequestInfo | URL, init?: RequestInit) => {
    if (init?.signal?.aborted) throw new DOMException("Aborted", "AbortError")
    return json({ items: [{ id: 1 }] })
  })
  vi.stubGlobal("fetch", fetchMock)

  await expect(loadRunResults("/results?run_id=3&limit=500", {
    signal: controller.signal,
  })).rejects.toMatchObject({ name: "AbortError" })
  expect(fetchMock).toHaveBeenCalledTimes(1)
  expect(fetchMock.mock.calls[0][1]?.signal).toBe(controller.signal)
})
