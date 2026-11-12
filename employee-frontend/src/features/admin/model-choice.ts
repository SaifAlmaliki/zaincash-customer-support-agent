import { fill } from "@/lib/locale"
import type { CatalogModel, CatalogProvider, ModelChoiceInput, ModelOptions, ProbeResult } from "@/lib/types"

export type TestedChoice = { key: string; result: ProbeResult }

export function choiceKey(choice: ModelChoiceInput) {
  return JSON.stringify([
    choice.provider,
    choice.model.trim(),
    choice.options.temperature ?? null,
    choice.options.think ?? null,
  ])
}

export function isValidTemperature(value: string) {
  if (value.trim() === "") return true
  const number = Number(value)
  return Number.isFinite(number) && number >= 0 && number <= 2
}

export function buildOptions(temperature: string, think: boolean | null): ModelOptions {
  const options: ModelOptions = {}
  if (temperature.trim() !== "" && isValidTemperature(temperature)) options.temperature = Number(temperature)
  if (think !== null) options.think = think
  return options
}

export function canSave(choice: ModelChoiceInput, tested: TestedChoice | null, temperature: string) {
  return (
    choice.model.trim() !== "" &&
    isValidTemperature(temperature) &&
    tested !== null &&
    tested.result.ok &&
    tested.key === choiceKey(choice)
  )
}

export function filterModels(entries: CatalogModel[], query: string) {
  const needle = query.trim().toLowerCase()
  if (!needle) return entries
  return entries.filter(
    (entry) => entry.id.toLowerCase().includes(needle) || entry.name.toLowerCase().includes(needle),
  )
}

export function offersThinking(entry: CatalogModel | undefined) {
  return entry === undefined || entry.capabilities === null || entry.capabilities.includes("thinking")
}

export function priceLabel(entry: CatalogModel, free: string, template: string): string | null {
  const input = entry.price_in_per_m
  const output = entry.price_out_per_m
  if (input === null && output === null) return null
  if ((input ?? 0) === 0 && (output ?? 0) === 0) return free
  return fill(template, { in: (input ?? 0).toFixed(2), out: (output ?? 0).toFixed(2) })
}

export function catalogView(provider: CatalogProvider | undefined): {
  kind: "loading" | "problem" | "list"
  message: string | null
} {
  if (!provider) return { kind: "loading", message: null }
  if (provider.status !== "ready") return { kind: "problem", message: provider.status_detail ?? provider.status }
  if (provider.error) return { kind: "problem", message: provider.error }
  return { kind: "list", message: null }
}
