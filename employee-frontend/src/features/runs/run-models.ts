import { MODEL_STEPS } from "@/lib/model-steps"
import type { ModelStep } from "@/lib/types"

const LEGACY: Record<string, ModelStep> = {
  jev: "classify",
  gemini: "extract",
  drafting: "draft",
  embedding: "embed",
}

export type RunModelRow = { step: ModelStep; provider: string | null; model: string }

export function runModelRows(modelIds: Record<string, string> | undefined): RunModelRow[] {
  if (!modelIds) return []
  const byStep = new Map<ModelStep, RunModelRow>()
  for (const [key, value] of Object.entries(modelIds)) {
    const step = (MODEL_STEPS as string[]).includes(key) ? (key as ModelStep) : LEGACY[key]
    if (!step || typeof value !== "string") continue
    const split = value.indexOf(":")
    const isRef = key === step && split > 0
    byStep.set(step, isRef
      ? { step, provider: value.slice(0, split), model: value.slice(split + 1) }
      : { step, provider: null, model: value })
  }
  return MODEL_STEPS.filter((step) => byStep.has(step)).map((step) => byStep.get(step)!)
}
