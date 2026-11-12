import { renderToStaticMarkup } from "react-dom/server"
import { afterEach, expect, it } from "vitest"
import { TooltipProvider } from "@/components/ui/tooltip"
import { getLocale, setLocale } from "@/lib/locale"
import type { Health } from "@/lib/types"
import { WorkspaceContext } from "@/lib/workspace"
import { AiLocalityChip } from "./AiLocalityChip"

const originalLocale = getLocale()
afterEach(() => setLocale(originalLocale))

const base: Health = {
  database: "connected",
  configured_modes: ["jev"],
  capabilities: { drafting: true, rag_indexing: true, evaluation: false },
}

function chip(health: Health) {
  return renderToStaticMarkup(
    <TooltipProvider>
      <WorkspaceContext.Provider
        value={{ revision: 0, refresh: () => {}, health, connectionError: null, notify: () => {} }}
      >
        <AiLocalityChip />
      </WorkspaceContext.Provider>
    </TooltipProvider>,
  )
}

const mixed: Health = {
  ...base,
  ai: {
    locality: "mixed",
    steps: { draft: { provider: "ollama", model: "qwen3:4b", locality: "local", status: "ready" } },
  },
}

it("shows where AI runs", () => {
  setLocale("en")
  expect(chip(mixed)).toContain("AI: Mixed")
  setLocale("ar")
  expect(chip(mixed)).toContain("الذكاء الاصطناعي: مختلط")
})

it("renders nothing before health reports AI steps", () => {
  expect(chip(base)).toBe("")
})
