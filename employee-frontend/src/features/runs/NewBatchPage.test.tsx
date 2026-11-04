import { renderToStaticMarkup } from "react-dom/server"
import { MemoryRouter } from "react-router-dom"
import { afterEach, expect, it } from "vitest"
import { getLocale, setLocale } from "@/lib/locale"
import { WorkspaceContext } from "@/lib/workspace"
import { NewBatchPage } from "./NewBatchPage"

const originalLocale = getLocale()
afterEach(() => setLocale(originalLocale))

function page() {
  return renderToStaticMarkup(
    <MemoryRouter>
      <WorkspaceContext.Provider value={{
        revision: 0,
        refresh: () => {},
        health: {
          database: "connected",
          configured_modes: ["jev"],
          capabilities: { drafting: false, rag_indexing: false, evaluation: false },
        },
        connectionError: null,
        notify: () => {},
      }}>
        <NewBatchPage />
      </WorkspaceContext.Provider>
    </MemoryRouter>,
  )
}

it("asks for tickets without model or file-format instructions", () => {
  setLocale("en")
  const html = page()
  expect(html).toContain("Add your tickets")
  expect(html).toContain("Start processing")
  expect(html).not.toContain("Jev")
  expect(html).not.toContain("Processing setup")
  expect(html).not.toContain("Expected file format")
  expect(html).not.toContain("TYPESAFE_API_KEY")
})

it("uses Arabic labels without developer instructions", () => {
  setLocale("ar")
  const html = page()
  expect(html).toContain("أضف التذاكر")
  expect(html).toContain("لصق تذكرة")
  expect(html).toContain("ابدأ المعالجة")
  expect(html).not.toContain("إعداد المعالجة")
  expect(html).not.toContain("صيغة الملف")
  expect(html).not.toContain("التصنيف")
  expect(html).not.toContain("Start processing")
  expect(html).not.toContain("Add your tickets")
})
