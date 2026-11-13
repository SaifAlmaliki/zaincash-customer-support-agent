import { renderToStaticMarkup } from "react-dom/server"
import { MemoryRouter } from "react-router-dom"
import { expect, it } from "vitest"
import { resultFixture } from "@/lib/test-fixtures"
import { TicketIdentity } from "./TicketIdentity"

it("leads with the customer phone and links to the customer page and the ticket", () => {
  const { ticket } = resultFixture(7, {}, { external_id: "S-001", customer_phone: "07809876543" })
  const html = renderToStaticMarkup(
    <MemoryRouter>
      <TicketIdentity ticket={ticket} index={0} ticketPath="/tickets/7" />
    </MemoryRouter>,
  )
  expect(html).toContain('href="/customers/07809876543"')
  expect(html).toContain('href="/tickets/7"')
  expect(html.indexOf("07809876543")).toBeLessThan(html.indexOf("S-001"))
})
