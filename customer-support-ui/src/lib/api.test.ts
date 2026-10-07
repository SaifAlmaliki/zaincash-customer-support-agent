import { afterEach, expect, it, vi } from "vitest"
import { loadQueue } from "./api"

afterEach(() => vi.unstubAllGlobals())

it("loads subsequent API pages so ticket 501 remains searchable and exportable", async () => {
  const fetch = vi.fn(async (url: string) => {
    const offset = Number(new URL(url, "http://localhost").searchParams.get("offset") || 0)
    const items = Array.from({ length: offset === 0 ? 500 : 1 }, (_, i) => ({ id: offset + i + 1 }))
    return new Response(JSON.stringify({ items, total: 501 }), { status: 200 })
  })
  vi.stubGlobal("fetch", fetch)
  const result = await loadQueue("/results?limit=500", {})
  expect(result.items).toHaveLength(501)
  expect(result.items.at(-1)?.id).toBe(501)
  expect(fetch).toHaveBeenCalledTimes(2)
})

it("reports an inconsistent queue snapshot instead of silently dropping rows", async () => {
  vi.stubGlobal("fetch", vi.fn(async (url: string) => {
    const offset = Number(new URL(url, "http://localhost").searchParams.get("offset") || 0)
    return new Response(JSON.stringify({ items: offset ? [] : [{ id: 1 }], total: 2 }), { status: 200 })
  }))
  await expect(loadQueue("/results?limit=500", {})).rejects.toThrow(/queue changed/i)
})
