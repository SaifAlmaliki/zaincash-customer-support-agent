import { request } from "@/lib/api"
import type { Result } from "@/lib/types"

export const RUN_RESULT_CONCURRENCY = 8

export async function loadRunResults(
  path: string,
  options: RequestInit,
): Promise<Result[]> {
  const page = await request<{ items: Result[] }>(path, options)
  const results = new Array<Result>(page.items.length)
  let nextIndex = 0

  async function worker() {
    while (nextIndex < page.items.length) {
      const index = nextIndex
      nextIndex += 1
      options.signal?.throwIfAborted()
      results[index] = await request<Result>(
        `/results/${page.items[index].id}`,
        options,
      )
    }
  }

  await Promise.all(
    Array.from(
      { length: Math.min(RUN_RESULT_CONCURRENCY, page.items.length) },
      () => worker(),
    ),
  )
  return results
}
