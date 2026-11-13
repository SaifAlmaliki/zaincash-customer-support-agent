import { renderToStaticMarkup } from "react-dom/server"
import { MemoryRouter } from "react-router-dom"
import { expect, it } from "vitest"
import { resultFixture } from "@/lib/test-fixtures"
import { TicketHeader } from "./TicketHeader"

it("titles the ticket with the customer phone linked to the customer page", () => {
  const result = resultFixture(5, {}, { external_id: "INTAKE-abc", customer_phone: "07809876543" })
  const html = renderToStaticMarkup(<MemoryRouter><TicketHeader result={result} /></MemoryRouter>)
  expect(html).toMatch(/<h1>.*href="\/customers\/07809876543".*07809876543.*<\/h1>/)
  expect(html).toContain("INTAKE-abc")
})
