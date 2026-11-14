import { expect, it } from "vitest"
import ar from "./ar.json"
import en from "./en.json"

function entries(value: unknown, prefix = ""): [string, unknown][] {
  if (value && typeof value === "object" && !Array.isArray(value))
    return Object.entries(value).flatMap(([key, child]) =>
      entries(child, prefix ? `${prefix}.${key}` : key)
    )
  return [[prefix, value]]
}

it("Arabic and English define exactly the same keys", () => {
  expect(entries(ar).map(([k]) => k).sort()).toEqual(entries(en).map(([k]) => k).sort())
})

it("has no empty translations", () => {
  for (const [key, value] of [...entries(ar), ...entries(en)])
    expect(typeof value === "string" && value.trim().length > 0, key).toBe(true)
})
