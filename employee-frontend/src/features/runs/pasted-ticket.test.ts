import { expect, it } from "vitest"
import { pastedTickets } from "./pasted-ticket"

it("builds one ticket only with a message and a valid phone", () => {
  expect(pastedTickets("حولت فلوس", "app", "+964 780 987 6543")).toEqual([
    { text: "حولت فلوس", channel: "app", customer_phone: "07809876543" },
  ])
  expect(pastedTickets("حولت فلوس", "app", "")).toEqual([])
  expect(pastedTickets("حولت فلوس", "app", "0780")).toEqual([])
  expect(pastedTickets("   ", "app", "07809876543")).toEqual([])
})
