import { afterEach, expect, it } from "vitest"
import { getLocale, setLocale } from "./locale"
import { countLabel, msLabel, percent1, usd } from "./format"

const originalLocale = getLocale()
afterEach(() => setLocale(originalLocale))

it("formats usage numbers and keeps null as a dash", () => {
  setLocale("en")
  expect(usd(null)).toBe("—")
  expect(usd(0)).toBe("$0")
  expect(usd(0.000412)).toBe("$0.00041")
  expect(usd(0.0144)).toBe("$0.0144")
  expect(usd(12.3456)).toBe("$12.35")
  expect(msLabel(undefined)).toBe("—")
  expect(msLabel(850)).toBe("850 ms")
  expect(msLabel(2500)).toBe("2.5 s")
  expect(percent1(0.8765)).toBe("87.7%")
  expect(percent1(null)).toBe("—")
  expect(countLabel(1534.4)).toBe("1,534")
})

it("localises duration units and keeps Latin digits", () => {
  setLocale("ar")
  expect(msLabel(850)).toBe("850 مللي ث")
  expect(msLabel(2500)).toBe("2.5 ث")
})
