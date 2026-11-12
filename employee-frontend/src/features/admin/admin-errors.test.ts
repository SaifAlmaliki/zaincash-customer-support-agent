import { expect, it } from "vitest"
import { ApiError } from "@/lib/api"
import en from "@/locales/en.json"
import { adminErrorMessage } from "./admin-errors"

it("maps admin API errors to readable messages", () => {
  expect(adminErrorMessage(new ApiError("admin_disabled", 403), en.models)).toBe(en.models.disabled)
  expect(adminErrorMessage(new ApiError("invalid_admin_token", 401), en.models)).toBe(en.models.wrongToken)
  expect(adminErrorMessage(new ApiError("run_in_progress", 409), en.models)).toBe(en.models.runInProgress)
  expect(adminErrorMessage(new ApiError("switch_in_progress", 409), en.models)).toBe(en.models.switchInProgress)
  expect(adminErrorMessage(new ApiError("Model test failed: x", 422), en.models)).toBe("Model test failed: x")
  expect(adminErrorMessage(42, en.models)).toBe(en.models.genericError)
})
