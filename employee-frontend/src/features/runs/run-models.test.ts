import { expect, it } from "vitest"
import { runModelRows } from "./run-models"

it("orders provider refs by step and keeps colons in model ids", () => {
  expect(runModelRows({ draft: "ollama:qwen3:4b", classify: "typesafe:jev-1.13.0" })).toEqual([
    { step: "classify", provider: "typesafe", model: "jev-1.13.0" },
    { step: "draft", provider: "ollama", model: "qwen3:4b" },
  ])
})

it("maps legacy run model ids to steps", () => {
  expect(runModelRows({ jev: "jev-1.13.0", drafting: "google/gemini-3.8-flash" })).toEqual([
    { step: "classify", provider: null, model: "jev-1.13.0" },
    { step: "draft", provider: null, model: "google/gemini-3.8-flash" },
  ])
  expect(runModelRows(undefined)).toEqual([])
})
