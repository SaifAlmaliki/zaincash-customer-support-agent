import { expect, it } from "vitest"
import { ApiError } from "@/lib/api"
import en from "@/locales/en.json"
import { runStartError } from "./run-start-error"

it("explains a batch blocked by an embedding switch", () => {
  expect(runStartError(new ApiError("knowledge_switch_in_progress", 409), en.batch)).toBe(en.batch.switchInProgress)
  expect(runStartError(new Error("Ticket x already exists"), en.batch)).toBe("Ticket x already exists")
  expect(runStartError("nope", en.batch)).toBe(en.batch.startFailed)
})
