import { renderToStaticMarkup } from "react-dom/server"
import { MemoryRouter } from "react-router-dom"
import { afterEach, expect, it } from "vitest"
import { setAdminSession } from "@/lib/admin-session"
import { getLocale, setLocale } from "@/lib/locale"
import type { EmbeddingSwitch, StepModel } from "@/lib/types"
import { WorkspaceContext } from "@/lib/workspace"
import { EmbeddingSwitchStatus } from "./EmbeddingSwitchStatus"
import { ModelStepCard } from "./ModelStepCard"
import { ModelsPage } from "./ModelsPage"

const originalLocale = getLocale()
afterEach(() => {
  setLocale(originalLocale)
  setAdminSession(null)
})

function page() {
  return renderToStaticMarkup(
    <MemoryRouter>
      <WorkspaceContext.Provider
        value={{ revision: 0, refresh: () => {}, health: null, connectionError: null, notify: () => {} }}
      >
        <ModelsPage />
      </WorkspaceContext.Provider>
    </MemoryRouter>,
  )
}

const embed: StepModel = {
  step: "embed", provider: "ollama", model: "nomic-embed-text", options: {}, source: "admin",
  updated_at: "2026-11-12T10:00:00+03:00", updated_by: "Sara", locality: "local", status: "ready",
  status_detail: null, requirements: ["embedding"], providers: ["openrouter", "ollama"],
}

it("asks for the admin token before showing models", () => {
  setLocale("en")
  const html = page()
  expect(html).toContain("Unlock admin settings")
  expect(html).toContain("Admin token")
  expect(html).not.toContain("Lock admin settings")
})

it("asks only for the token and lets the admin reveal it", () => {
  setLocale("en")
  const html = page()
  expect(html).not.toContain("Your name")
  expect(html.match(/<input/g)).toHaveLength(1)
  expect(html).toContain('type="password"')
  expect(html).toContain('aria-label="Show token"')
  setLocale("ar")
  expect(page()).toContain('aria-label="إظهار الرمز"')
})

it("shows the lock button and loads models once unlocked", () => {
  setLocale("en")
  setAdminSession({ token: "secret", name: "Sara" })
  const html = page()
  expect(html).toContain("Lock admin settings")
  expect(html).not.toContain("Unlock admin settings")
})

it("disables the embed change button while a switch runs", () => {
  setLocale("en")
  const html = renderToStaticMarkup(<ModelStepCard value={embed} disabled onChange={() => {}} />)
  expect(html).toContain("nomic-embed-text")
  expect(html).toContain("Set by Sara")
  expect(html).toMatch(/<button[^>]*disabled/)
})

it("shows a saved model that was removed from Ollama as not installed", () => {
  const missing: StepModel = {
    ...embed, status: "model_missing", status_detail: "The model is not installed in Ollama.",
  }
  setLocale("en")
  const html = renderToStaticMarkup(<ModelStepCard value={missing} disabled={false} onChange={() => {}} />)
  expect(html).toContain("status-model_missing")
  expect(html).toContain("Model not installed")
  setLocale("ar")
  expect(renderToStaticMarkup(<ModelStepCard value={missing} disabled={false} onChange={() => {}} />)).toContain(
    "النموذج غير مثبّت",
  )
})

it("shows switch progress and failed documents", () => {
  setLocale("ar")
  const value: EmbeddingSwitch = {
    id: 1, status: "completed_with_errors", total: 3, done: 3, failed_document_ids: [7], error: null,
    target: { provider: "ollama", model: "nomic-embed-text", options: {} },
    previous: { provider: "openrouter", model: "openai/text-embedding-3-small", options: {} },
    started_by: "Sara", started_at: "2026-11-12T10:00:00+03:00", finished_at: "2026-11-12T10:01:00+03:00",
  }
  const html = renderToStaticMarkup(<EmbeddingSwitchStatus value={value} />)
  expect(html).toContain("تم تبديل نموذج التضمين مع فشل بعض المستندات")
  expect(html).toContain("أُعيدت فهرسة 3 من 3 مستند")
  expect(html).toContain("7")
})
