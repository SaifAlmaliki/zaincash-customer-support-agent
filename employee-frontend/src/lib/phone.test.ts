import { expect, it } from "vitest"
import { customerPath, normalizeCustomerPhone } from "./phone"

it.each(["07809876543", "+964 780 987 6543", "٠٧٨٠٩٨٧٦٥٤٣", "7809876543", "00964-780-987-6543"])("accepts %s", (raw) => {
  expect(normalizeCustomerPhone(raw)).toBe("07809876543")
})

it.each(["", "0780", "07809876543x", "07209876543", "needle"])("rejects %s", (raw) => {
  expect(normalizeCustomerPhone(raw)).toBeNull()
})

it("builds the customer page path", () => {
  expect(customerPath("07809876543")).toBe("/customers/07809876543")
})
