import { renderToStaticMarkup } from "react-dom/server"
import { MemoryRouter, Route, Routes } from "react-router-dom"
import { afterEach, expect, it } from "vitest"
import { getLocale, setLocale } from "@/lib/locale"
import { resultFixture } from "@/lib/test-fixtures"
import { WorkspaceContext } from "@/lib/workspace"
import { CustomerPage, CustomerProfileView } from "./CustomerPage"

const originalLocale = getLocale()
afterEach(() => setLocale(originalLocale))

it("lists the customer's tickets with links to each review", () => {
  setLocale("en")
  const html = renderToStaticMarkup(
    <MemoryRouter>
      <CustomerProfileView customer={{
        phone: "07809876543",
        created_at: "2026-10-07T09:30:00+03:00",
        ticket_count: 2,
        results: [
          resultFixture(11, {}, { external_id: "S-001", customer_phone: "07809876543" }),
          resultFixture(12, {}, { external_id: "S-009", customer_phone: "07809876543" }),
        ],
      }} />
    </MemoryRouter>,
  )
  expect(html).toContain("07809876543")
  expect(html).toContain("2 tickets")
  expect(html).toContain('href="/tickets/11"')
  expect(html).toContain("S-009")
})

it("shows a localized state for a malformed phone without loading", () => {
  setLocale("ar")
  const html = renderToStaticMarkup(
    <MemoryRouter initialEntries={["/customers/abc"]}>
      <WorkspaceContext.Provider value={{
        revision: 0, refresh: () => {}, health: null, connectionError: null, notify: () => {},
      }}>
        <Routes>
          <Route path="/customers/:phone" element={<CustomerPage />} />
        </Routes>
      </WorkspaceContext.Provider>
    </MemoryRouter>,
  )
  expect(html).toContain("رقم الهاتف غير صحيح")
})
