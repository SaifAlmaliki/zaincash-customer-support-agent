import { render, screen, waitFor } from "@testing-library/react"
import userEvent from "@testing-library/user-event"
import { fireEvent } from "@testing-library/react"
import { beforeEach, expect, it, vi } from "vitest"
import type { IntakeApi } from "./api"
import { IntakeController } from "./controller"
import { IntakePage } from "./IntakePage"
import { memoryStorage } from "./session"
import type { Attachment, CustomerReview, SessionView } from "./types"

function emptySession(overrides: Partial<SessionView> = {}): SessionView {
  return {
    id: "session-1",
    revision: 2,
    phase: "collecting",
    language: "en",
    turn_status: "idle",
    active_request_id: null,
    messages: [],
    attachments: [],
    readiness: { quality: "collecting", missing: [], conflicts: [], reason: "Collecting", next_key: null },
    review: null,
    receipt: null,
    error_code: null,
    ...overrides,
  }
}

const review: CustomerReview = {
  id: "review-1",
  revision: 2,
  language: "en",
  quality: "partial_context",
  text: "The transfer failed.",
  facts: { amount: { key: "amount", status: "unknown", value: null, normalized: null, evidence: [] } },
  additional_issues: [],
  unknown_keys: ["amount"],
  attachment_ids: [],
}

const attachment: Attachment = {
  id: "att-1",
  filename: "error.png",
  mime_type: "image/png",
  size: 2,
  width: 1,
  height: 1,
  message_id: null,
  removed: false,
}

function fakeApi(overrides: Partial<SessionView> = {}): IntakeApi {
  const session = emptySession(overrides)
  return {
    create: vi.fn(async () => ({ credentials: { session_id: "session-1", token: "secret-token" }, session })),
    get: vi.fn(async () => session),
    message: vi.fn(async () => session),
    review: vi.fn(async (_credentials, command): Promise<SessionView> => ({
      ...session,
      language: command.language,
      review: { ...review, language: command.language },
    })),
    retry: vi.fn(async () => session),
    submit: vi.fn(async () => ({
      ticket_reference: "INTAKE-demo",
      submitted_at: "2026-10-18T09:00:00Z",
      processing_status: "processing" as const,
    })),
    upload: vi.fn(async () => ({ attachment, session: emptySession({ ...session, revision: 3, attachments: [attachment] }) })),
    remove: vi.fn(async () => emptySession({ attachments: [{ ...attachment, removed: true }] })),
    image: vi.fn(async () => new Blob(["png"])),
  }
}

async function readyController(language: "ar" | "en") {
  const api = fakeApi({ phase: "review_ready", language, review })
  const controller = new IntakeController(api, memoryStorage())
  await controller.initialize(language)
  return { controller, api }
}

async function collectingController(language: "ar" | "en", overrides: Partial<SessionView> = {}) {
  const api = fakeApi({ phase: "collecting", language, ...overrides })
  const controller = new IntakeController(api, memoryStorage())
  await controller.initialize(language)
  return { controller, api }
}

beforeEach(() => {
  vi.restoreAllMocks()
})

it("requires explicit submission after summary review", async () => {
  const user = userEvent.setup()
  const { controller, api } = await readyController("en")
  render(<IntakePage controller={controller} />)
  expect(await screen.findByRole("heading", { name: "Review your report" })).toBeVisible()
  expect(api.submit).not.toHaveBeenCalled()
  await user.click(screen.getByRole("button", { name: "Submit ticket" }))
  expect(await screen.findByText("INTAKE-demo")).toBeVisible()
  expect(api.submit).toHaveBeenCalledTimes(1)
  expect(screen.getByText(/employee still needs to review it/i)).toBeVisible()
  expect(document.body.textContent).not.toMatch(/recovered|resolved/i)
})

it("keeps an unsent draft when a screenshot upload fails", async () => {
  const user = userEvent.setup()
  const { controller, api } = await collectingController("en")
  vi.mocked(api.upload).mockRejectedValueOnce(new Error("Upload failed"))
  render(<IntakePage controller={controller} />)
  const input = await screen.findByRole("textbox", { name: "Your message" })
  await user.type(input, "This error appeared yesterday")
  await user.upload(screen.getByLabelText("Attach screenshots"), new File([new Uint8Array([1, 2])], "error.png", { type: "image/png" }))
  expect(await screen.findByRole("alert")).toHaveTextContent("Upload failed")
  expect(input).toHaveValue("This error appeared yesterday")
})

it("submits once when the button is clicked twice", async () => {
  const user = userEvent.setup()
  const { controller, api } = await readyController("en")
  let release: (value: Awaited<ReturnType<IntakeApi["submit"]>>) => void = () => undefined
  vi.mocked(api.submit).mockImplementation(
    () =>
      new Promise((resolve) => {
        release = resolve
      }),
  )
  render(<IntakePage controller={controller} />)
  const button = await screen.findByRole("button", { name: "Submit ticket" })
  await user.click(button)
  await user.click(button)
  release({ ticket_reference: "INTAKE-demo", submitted_at: "2026-10-18T09:00:00Z", processing_status: "processing" })
  expect(await screen.findByText("INTAKE-demo")).toBeVisible()
  expect(api.submit).toHaveBeenCalledTimes(1)
})

it("requests a fresh review when the language changes", async () => {
  const user = userEvent.setup()
  const { controller, api } = await readyController("en")
  render(<IntakePage controller={controller} />)
  await user.click(await screen.findByRole("button", { name: "العربية" }))
  expect(await screen.findByRole("heading", { name: "راجع تفاصيل المشكلة" })).toBeVisible()
  expect(vi.mocked(api.review).mock.calls[0]?.[1].language).toBe("ar")
})

it("sends a correction as a normal message", async () => {
  const user = userEvent.setup()
  const { controller, api } = await readyController("en")
  vi.mocked(api.message).mockImplementation(async (_credentials, command) =>
    emptySession({
      revision: 3,
      messages: [{ id: "m-new", role: "user", text: command.text, language: "en", created_at: "2026-10-18T09:00:00Z", attachment_ids: [] }],
    }),
  )
  render(<IntakePage controller={controller} />)
  const input = await screen.findByRole("textbox", { name: "Your message" })
  await user.type(input, "I meant 50000 IQD")
  await user.click(screen.getByRole("button", { name: "Send" }))
  expect(vi.mocked(api.message).mock.calls[0]?.[1].text).toBe("I meant 50000 IQD")
  expect(api.submit).not.toHaveBeenCalled()
  expect(screen.queryByRole("heading", { name: "Review your report" })).not.toBeInTheDocument()
})

it("sends an image without requiring text", async () => {
  const user = userEvent.setup()
  const { controller, api } = await collectingController("en")
  render(<IntakePage controller={controller} />)
  await user.upload(await screen.findByLabelText("Attach screenshots"), new File([new Uint8Array([1, 2])], "error.png", { type: "image/png" }))
  await user.click(screen.getByRole("button", { name: "Send" }))
  expect(vi.mocked(api.message).mock.calls[0]?.[1]).toMatchObject({ text: "", attachment_ids: ["att-1"] })
})

it("removes an uploaded screenshot", async () => {
  const user = userEvent.setup()
  const { controller, api } = await collectingController("en", { attachments: [attachment] })
  render(<IntakePage controller={controller} />)
  await user.click(await screen.findByRole("button", { name: "Remove" }))
  expect(api.remove).toHaveBeenCalled()
  expect(screen.queryByText("error.png")).not.toBeInTheDocument()
})

it("shows unknown facts in a partial review", async () => {
  const { controller } = await readyController("en")
  render(<IntakePage controller={controller} />)
  expect(await screen.findByText("Some details are still unknown")).toBeVisible()
  expect(screen.getAllByText("Unknown").length).toBeGreaterThan(0)
  expect(screen.queryByText(/^0$/)).not.toBeInTheDocument()
})

it("does not send on IME enter and keeps shift-enter as a newline", async () => {
  const user = userEvent.setup()
  const { controller, api } = await collectingController("en")
  render(<IntakePage controller={controller} />)
  const input = await screen.findByRole("textbox", { name: "Your message" })
  input.focus()
  fireEvent.compositionStart(input)
  fireEvent.keyDown(input, { key: "Enter" })
  fireEvent.compositionEnd(input)
  expect(api.message).not.toHaveBeenCalled()
  await user.type(input, "hello")
  await user.keyboard("{Shift>}{Enter}{/Shift}")
  expect(input).toHaveValue("hello\n")
  expect(api.message).not.toHaveBeenCalled()
})

it("refreshes an in-flight turn", async () => {
  const user = userEvent.setup()
  const { controller, api } = await collectingController("en", { turn_status: "processing" })
  render(<IntakePage controller={controller} />)
  await user.click(await screen.findByRole("button", { name: "Refresh" }))
  expect(api.get).toHaveBeenCalled()
})

it("drops a late reply after starting a new report", async () => {
  const user = userEvent.setup()
  const { controller, api } = await collectingController("en", {
    messages: [{ id: "m1", role: "user", text: "old report", language: "en", created_at: "2026-10-18T09:00:00Z", attachment_ids: [] }],
  })
  let release: (value: SessionView) => void = () => undefined
  vi.mocked(api.message).mockImplementation(
    () =>
      new Promise((resolve) => {
        release = resolve
      }),
  )
  render(<IntakePage controller={controller} />)
  const input = await screen.findByRole("textbox", { name: "Your message" })
  await user.type(input, "more")
  await user.click(screen.getByRole("button", { name: "Send" }))
  await user.click(screen.getByRole("button", { name: "Start a new report" }))
  await user.click(screen.getByRole("button", { name: "Start new report" }))
  release(
    emptySession({
      messages: [{ id: "late", role: "user", text: "late secret", language: "en", created_at: "2026-10-18T09:00:00Z", attachment_ids: [] }],
    }),
  )
  await waitFor(() => expect(api.create).toHaveBeenCalledTimes(2))
  expect(screen.queryByText("late secret")).not.toBeInTheDocument()
})
