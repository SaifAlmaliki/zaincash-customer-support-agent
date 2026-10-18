import { expect, it } from "vitest"
import { canReview } from "./review-availability"

it.each(["processing", "failed"])("prevents review while %s", (status) => {
  expect(canReview(status)).toBe(false)
})

it("allows the existing saved review states", () => {
  for (const status of ["pending_review", "escalated", "approved", "edited", "rejected"]) {
    expect(canReview(status)).toBe(true)
  }
})
