import { renderToStaticMarkup } from "react-dom/server"
import { MemoryRouter } from "react-router-dom"
import { expect, it } from "vitest"
import { WorkspaceContext } from "@/lib/workspace"
import { NewBatchPage } from "./NewBatchPage"

it("offers only Jev classification for a new batch", () => {
  const html = renderToStaticMarkup(
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
  expect(html).toContain("Jev")
  expect(html).not.toContain("Gemini")
  expect(html).not.toContain("Classification strategy")
})
