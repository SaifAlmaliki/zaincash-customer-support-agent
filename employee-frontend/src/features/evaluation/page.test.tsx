import { renderToStaticMarkup } from "react-dom/server"
import { MemoryRouter } from "react-router-dom"
import { afterEach, expect, it } from "vitest"
import { getLocale, setLocale } from "@/lib/locale"
import { WorkspaceContext } from "@/lib/workspace"
import { EvaluationPage } from "./EvaluationPage"

const originalLocale = getLocale()
afterEach(() => setLocale(originalLocale))

it("renders the page shell in Arabic without the old placeholder", () => {
  setLocale("ar")
  const html = renderToStaticMarkup(
    <MemoryRouter>
      <WorkspaceContext.Provider value={{
        revision: 0, refresh: () => {}, connectionError: null, notify: () => {},
        health: { database: "connected", configured_modes: ["jev"],
                  capabilities: { drafting: false, rag_indexing: false, evaluation: true } },
      }}>
        <EvaluationPage />
      </WorkspaceContext.Provider>
    </MemoryRouter>
  )
  expect(html).toContain("التقييم")
  expect(html).toContain("تكلفة وزمن استجابة كل عملية ذكاء اصطناعي.")
  expect(html).toContain("تحديث")
  for (const old of ["Import results", "Classification strategy", "Not run", "Expected report format"])
    expect(html, old).not.toContain(old)
})
