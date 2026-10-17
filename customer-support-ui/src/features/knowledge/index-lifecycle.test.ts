import { afterEach, expect, it, vi } from "vitest"
import type { KnowledgeDocument } from "../../lib/types"
import { acceptIndexRequest, pollKnowledge, type PendingIndexes } from "./index-lifecycle"

const document = (overrides: Partial<KnowledgeDocument> = {}): KnowledgeDocument => ({
  id: 7, filename: "synthetic-policy.md", sha256: "synthetic", size: 40,
  content_type: "text/markdown", created_at: "2026-10-17T00:00:00Z",
  updated_at: "2026-10-17T00:00:00Z", status: "awaiting_indexing",
  category_tags: [], chunk_count: 0, embedding_model: null,
  embedding_dimensions: null, chunking_version: null, indexed_at: null,
  error: null, cost_usd: 0, ...overrides,
})

afterEach(() => vi.useRealTimers())

it("follows accepted-but-not-claimed requests through indexing to publication", async () => {
  vi.useFakeTimers()
  const pending: PendingIndexes = new Map()
  acceptIndexRequest(pending, { ...document(), index_requested: true })
  const snapshots = [document(), document(), document({ status: "indexing" }), document({ status: "indexed", chunk_count: 2 })]
  const states: string[] = []
  const load = vi.fn(async () => [snapshots.shift()!])
  const stop = pollKnowledge({ pending, load, onData: (rows) => states.push(rows[0].status), onError: () => {}, onPaused: () => {} })
  await vi.advanceTimersByTimeAsync(12000)
  expect(states).toEqual(["awaiting_indexing", "awaiting_indexing", "indexing", "indexed"])
  expect(pending.size).toBe(0)
  expect(load).toHaveBeenCalledTimes(4)
  expect(vi.getTimerCount()).toBe(0)
  stop()
})

it("does not mistake the old failed retry snapshot for a new explicit failure", async () => {
  vi.useFakeTimers()
  const pending: PendingIndexes = new Map()
  const old = document({ status: "failed", error: "Embedding unavailable" })
  acceptIndexRequest(pending, { ...old, index_requested: true })
  const snapshots = [old, old, { ...old, updated_at: "2026-10-17T00:01:00Z" }]
  const seen: number[] = []
  pollKnowledge({ pending, load: async () => [snapshots.shift()!], onData: () => seen.push(pending.size), onError: () => {}, onPaused: () => {} })
  await vi.advanceTimersByTimeAsync(8000)
  expect(seen).toEqual([1, 1, 0])
  expect(vi.getTimerCount()).toBe(0)
})

it("does not poll idle or saturated uploads that were not admitted", async () => {
  vi.useFakeTimers()
  const pending: PendingIndexes = new Map()
  acceptIndexRequest(pending, { ...document(), index_requested: false })
  const load = vi.fn(async () => [document()])
  pollKnowledge({ pending, load, onData: () => {}, onError: () => {}, onPaused: () => {} })
  await vi.advanceTimersByTimeAsync(10000)
  expect(load).toHaveBeenCalledTimes(1)
  expect(pending.size).toBe(0)
  expect(vi.getTimerCount()).toBe(0)
})

it("bounds polling without dropping unresolved accepted IDs", async () => {
  vi.useFakeTimers()
  const pending: PendingIndexes = new Map()
  acceptIndexRequest(pending, { ...document(), index_requested: true })
  const paused = vi.fn()
  const load = vi.fn(async () => [document()])
  pollKnowledge({ pending, load, onData: () => {}, onError: () => {}, onPaused: paused })
  await vi.advanceTimersByTimeAsync(600000)
  expect(paused).toHaveBeenCalledOnce()
  expect(pending.has(7)).toBe(true)
  expect(load.mock.calls.length).toBeLessThanOrEqual(91)
  expect(vi.getTimerCount()).toBe(0)
})

it("aborts in-flight work and ignores late responses on cleanup", async () => {
  vi.useFakeTimers()
  let resolve!: (rows: KnowledgeDocument[]) => void
  let signal!: AbortSignal
  const onData = vi.fn()
  const stop = pollKnowledge({ pending: new Map(), load: (s) => { signal = s; return new Promise((r) => { resolve = r }) }, onData, onError: () => {}, onPaused: () => {} })
  stop()
  resolve([document({ status: "indexing" })])
  await vi.advanceTimersByTimeAsync(10000)
  expect(signal.aborted).toBe(true)
  expect(onData).not.toHaveBeenCalled()
  expect(vi.getTimerCount()).toBe(0)
})

it("stops on load failure without clearing accepted IDs or scheduling more requests", async () => {
  vi.useFakeTimers()
  const pending: PendingIndexes = new Map()
  acceptIndexRequest(pending, { ...document(), index_requested: true })
  const error = vi.fn()
  const load = vi.fn(async () => { throw new Error("Offline") })
  pollKnowledge({ pending, load, onData: () => {}, onError: error, onPaused: () => {} })
  await vi.advanceTimersByTimeAsync(10000)
  expect(error).toHaveBeenCalledWith("Offline")
  expect(pending.has(7)).toBe(true)
  expect(load).toHaveBeenCalledOnce()
  expect(vi.getTimerCount()).toBe(0)
})
