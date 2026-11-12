import { expect, it } from "vitest"
import type { CatalogModel, CatalogProvider, ModelChoiceInput } from "@/lib/types"
import {
  buildOptions,
  canSave,
  catalogView,
  choiceKey,
  filterModels,
  isValidTemperature,
  offersThinking,
  priceLabel,
} from "./model-choice"

const choice: ModelChoiceInput = { provider: "ollama", model: "qwen3:4b", options: { think: false } }
const model = (over: Partial<CatalogModel> = {}): CatalogModel => ({
  id: "qwen3:4b", name: "qwen3:4b", capabilities: ["tools"], price_in_per_m: 0, price_out_per_m: 0,
  context_length: null, eligibility: "eligible", ...over,
})
const provider = (over: Partial<CatalogProvider> = {}): CatalogProvider => ({
  provider: "ollama", locality: "local", status: "ready", status_detail: null, entries: [], error: null, ...over,
})

it("enables saving only after a passing test of the exact selection", () => {
  const tested = { key: choiceKey(choice), result: { ok: true, latency_ms: 900, error: null } }
  expect(canSave(choice, tested, "")).toBe(true)
  expect(canSave({ ...choice, options: { think: true } }, tested, "")).toBe(false)
  expect(canSave({ ...choice, options: { think: false, temperature: 0.2 } }, tested, "0.2")).toBe(false)
  expect(canSave({ ...choice, model: "qwen3:8b" }, tested, "")).toBe(false)
  expect(canSave(choice, { ...tested, result: { ok: false, latency_ms: 5, error: "x" } }, "")).toBe(false)
  expect(canSave(choice, null, "")).toBe(false)
  expect(canSave({ ...choice, model: "  " }, { ...tested, key: choiceKey({ ...choice, model: "  " }) }, "")).toBe(false)
})

it("blocks saving while the temperature field is invalid", () => {
  const tested = { key: choiceKey(choice), result: { ok: true, latency_ms: 900, error: null } }
  expect(canSave(choice, tested, "")).toBe(true)
  expect(canSave(choice, tested, "5")).toBe(false)
  expect(canSave(choice, tested, "abc")).toBe(false)
})

it("builds options from form values and validates temperature", () => {
  expect(buildOptions("", null)).toEqual({})
  expect(buildOptions("0.3", false)).toEqual({ temperature: 0.3, think: false })
  expect(isValidTemperature("")).toBe(true)
  expect(isValidTemperature("2")).toBe(true)
  expect(isValidTemperature("2.5")).toBe(false)
  expect(isValidTemperature("abc")).toBe(false)
})

it("filters by id or name and offers thinking only when possible", () => {
  const entries = [model(), model({ id: "gemma3:4b", name: "Gemma 3", capabilities: null })]
  expect(filterModels(entries, "gem").map((e) => e.id)).toEqual(["gemma3:4b"])
  expect(filterModels(entries, " ")).toHaveLength(2)
  expect(offersThinking(model())).toBe(false)
  expect(offersThinking(model({ capabilities: ["tools", "thinking"] }))).toBe(true)
  expect(offersThinking(model({ capabilities: null }))).toBe(true)
  expect(offersThinking(undefined)).toBe(true)
})

it("labels prices", () => {
  const template = "${in} / ${out} per 1M tokens"
  expect(priceLabel(model(), "Free", template)).toBe("Free")
  expect(priceLabel(model({ price_in_per_m: 3, price_out_per_m: 15 }), "Free", template)).toBe("$3.00 / $15.00 per 1M tokens")
  expect(priceLabel(model({ price_in_per_m: null, price_out_per_m: null }), "Free", template)).toBeNull()
})

it("catalogView reports provider problems without hiding the custom model field", () => {
  expect(catalogView(undefined).kind).toBe("loading")
  expect(catalogView(provider({ status: "unreachable", status_detail: "Ollama is not reachable at x." }))).toEqual({
    kind: "problem", message: "Ollama is not reachable at x.",
  })
  expect(catalogView(provider({ error: "Could not list models: ConnectError" }))).toEqual({
    kind: "problem", message: "Could not list models: ConnectError",
  })
  expect(catalogView(provider({ entries: [model()] }))).toEqual({ kind: "list", message: null })
})
