import { renderToStaticMarkup } from "react-dom/server"
import { afterEach, expect, it } from "vitest"
import { getLocale, setLocale } from "@/lib/locale"
import { ticketCalls, ticketPage } from "./fixtures"
import { TicketCostTable } from "./TicketCostTable"
import { TimelineView } from "./TicketTimeline"

const originalLocale = getLocale()
afterEach(() => setLocale(originalLocale))

function table() {
  return renderToStaticMarkup(
    <TicketCostTable page={ticketPage} sort="cost" onSort={() => {}} offset={0} limit={25}
                     onPage={() => {}} onOpen={() => {}} />
  )
}

it("lists tickets with cost split, AI time and an open button", () => {
  setLocale("en")
  const html = table()
  expect(html).toContain("INTAKE-ab12")
  expect(html).toContain("$0.0160")
  expect(html).toContain("incl. intake $0.00400")
  expect(html).toContain("2.0 s")
  expect(html).toContain('aria-label="Open the AI timeline of INTAKE-ab12"')
  expect(html).toContain("1–2 of 2")
})

it("TicketCostTable marks rows without recorded detail", () => {
  setLocale("ar")
  const html = table()
  expect(html).toContain("التفاصيل غير مسجلة")
  expect(html).not.toContain("Detail not recorded")
})

it("renders the timeline in Arabic with localised units and a dash for unknown cost", () => {
  setLocale("ar")
  const unknownCall = { ...ticketCalls.calls[1], id: 4, cost_usd: 0, cost_source: "unknown" as const }
  const html = renderToStaticMarkup(
    <TimelineView data={{ ...ticketCalls, calls: [...ticketCalls.calls, unknownCall] }} />)
  expect(html).toContain("800 مللي ث")
  expect(html).toContain('title="السعر غير معروف">—<')
  expect(html).not.toMatch(/\d (ms|s)\b/)
  expect(html).not.toContain("Price unknown")
  expect(renderToStaticMarkup(<TicketCostTable page={ticketPage} sort="cost" onSort={() => {}} offset={0}
                              limit={25} onPage={() => {}} onOpen={() => {}} />)).not.toMatch(/\d (ms|s)\b/)
})

it("renders the timeline in order with errors and local cost", () => {
  setLocale("en")
  const html = renderToStaticMarkup(<TimelineView data={ticketCalls} />)
  const order = ["Customer intake", "Classification (Jev)", "Detail extraction"].map((label) => html.indexOf(label))
  expect(order).toEqual([...order].sort((a, b) => a - b))
  expect(html).toContain("TimeoutError")
  expect(html).toContain("attempt 2")
  expect(html).toContain("Local · $0")
  expect(html).toContain("usage-bar-error")
  expect(html).toContain("1,200 in / 300 out")
})
