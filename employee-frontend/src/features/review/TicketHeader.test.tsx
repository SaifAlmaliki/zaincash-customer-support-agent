import { renderToStaticMarkup } from "react-dom/server"
import { MemoryRouter } from "react-router-dom"
import { afterEach, expect, it } from "vitest"
import { getLocale, setLocale } from "@/lib/locale"
import { resultFixture } from "@/lib/test-fixtures"
import { TicketHeader } from "./TicketHeader"

const originalLocale = getLocale()
afterEach(() => setLocale(originalLocale))

it("titles the ticket with the customer phone linked to the customer page", () => {
  const result = resultFixture(5, {}, { external_id: "INTAKE-abc", customer_phone: "07809876543" })
  const html = renderToStaticMarkup(<MemoryRouter><TicketHeader result={result} /></MemoryRouter>)
  expect(html).toMatch(/<h1>.*href="\/customers\/07809876543".*07809876543.*<\/h1>/)
  expect(html).toContain("INTAKE-abc")
})

it("offers reprocess and disables it while the ticket is processing", () => {
  setLocale("en")
  const ready = renderToStaticMarkup(
    <MemoryRouter><TicketHeader result={resultFixture(5)} onReprocess={() => {}} /></MemoryRouter>
  )
  expect(ready).toContain("Reprocess")
  const busy = renderToStaticMarkup(
    <MemoryRouter>
      <TicketHeader result={resultFixture(5, { status: "processing" })} onReprocess={() => {}} reprocessing />
    </MemoryRouter>
  )
  expect(busy).toContain("Reprocessing")
  expect(busy).toContain("disabled")
})
