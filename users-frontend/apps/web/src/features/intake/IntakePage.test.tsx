import { act, render, screen, waitFor, within } from "@testing-library/react"
import userEvent from "@testing-library/user-event"
import { fireEvent } from "@testing-library/react"
import { beforeEach, expect, it, vi } from "vitest"
import { IntakeRequestError, type IntakeApi } from "./api"
import { IntakeController } from "./controller"
import { IntakePage } from "./IntakePage"
import { memoryStorage } from "./session"
import { CUSTOMER_PHONE, attachment, emptySession as sharedEmptySession, fakeApi as sharedFakeApi, review } from "./test/fixtures"
import type { SessionView } from "./types"
import { ThemeProvider } from "@/components/theme-provider"

function pageReadiness(): SessionView["readiness"] {
  return { quality: "collecting", missing: [], conflicts: [], reason: "Collecting", next_key: null }
}

function emptySession(overrides: Partial<SessionView> = {}): SessionView {
  return sharedEmptySession({ revision: 2, readiness: pageReadiness(), ...overrides })
}

function fakeApi(overrides: Partial<SessionView> = {}): IntakeApi {
  const session = emptySession(overrides)
  return {
    ...sharedFakeApi(session),
    upload: vi.fn(async () => ({ attachment, session: emptySession({ ...session, revision: 3, attachments: [attachment] }) })),
    remove: vi.fn(async () => emptySession({ attachments: [{ ...attachment, removed: true }] })),
  }
}

async function readyController(language: "ar" | "en") {
  const api = fakeApi({ phase: "review_ready", language, review })
  const controller = new IntakeController(api, memoryStorage())
  await controller.initialize(language, CUSTOMER_PHONE)
  return { controller, api }
}

async function collectingController(language: "ar" | "en", overrides: Partial<SessionView> = {}) {
  const api = fakeApi({ phase: "collecting", language, ...overrides })
  const controller = new IntakeController(api, memoryStorage())
  await controller.initialize(language, CUSTOMER_PHONE)
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
  expect(within(screen.getByRole("region", { name: "Ticket received" })).getByText(CUSTOMER_PHONE)).toBeVisible()
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
  expect(document.documentElement).toHaveAttribute("lang", "ar")
  expect(document.documentElement).toHaveAttribute("dir", "rtl")
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

it("asks for the phone number in Iraqi Arabic before the chat", async () => {
  const user = userEvent.setup()
  const api = fakeApi({ language: "ar" })
  const controller = new IntakeController(api, memoryStorage())
  render(<IntakePage controller={controller} />)
  const phone = await screen.findByRole("textbox", { name: "رقم هاتفك بزين كاش" })
  expect(document.documentElement).toHaveAttribute("lang", "ar")
  expect(document.documentElement).toHaveAttribute("dir", "rtl")
  expect(phone).toHaveFocus()
  await user.type(phone, "0770")
  await user.click(screen.getByRole("button", { name: "استمرار" }))
  expect(screen.getByRole("alert")).toHaveTextContent("اكتب رقم زين كاش صحيح، مثل 07701234567.")
  expect(api.create).not.toHaveBeenCalled()
  await user.clear(phone)
  await user.type(phone, "+964 770 123 4567")
  await user.click(screen.getByRole("button", { name: "استمرار" }))
  expect(api.create).toHaveBeenCalledWith("ar", CUSTOMER_PHONE, expect.any(AbortSignal))
  expect(await screen.findByLabelText("رسالتك")).toBeVisible()
})

it("shows the server's invalid-number answer on the phone screen", async () => {
  const user = userEvent.setup()
  const api = fakeApi({ language: "en" })
  vi.mocked(api.create).mockRejectedValueOnce(new IntakeRequestError("Enter a valid ZainCash phone number, for example 07701234567.", 422, "invalid_phone"))
  const controller = new IntakeController(api, memoryStorage())
  render(<IntakePage controller={controller} />)
  await user.click(await screen.findByRole("button", { name: "English" }))
  await user.type(screen.getByRole("textbox", { name: "Your ZainCash phone number" }), "07701234567")
  await user.click(screen.getByRole("button", { name: "Continue" }))
  expect(await screen.findByRole("alert")).toHaveTextContent("Enter a valid ZainCash phone number")
  expect(screen.getByRole("textbox", { name: "Your ZainCash phone number" })).toBeVisible()
})

it("shows the signed-in phone and changes number after confirmation", async () => {
  const user = userEvent.setup()
  const { controller } = await collectingController("en", {
    messages: [{ id: "m1", role: "user", text: "old report", language: "en", created_at: "2026-10-18T09:00:00Z", attachment_ids: [] }],
  })
  render(<IntakePage controller={controller} />)
  expect(screen.getByRole("group", { name: "Signed in as" })).toHaveTextContent(CUSTOMER_PHONE)
  await user.click(screen.getByRole("button", { name: "Change number" }))
  await user.click(screen.getByRole("button", { name: "Use another number" }))
  expect(await screen.findByRole("textbox", { name: "Your ZainCash phone number" })).toBeVisible()
  expect(document.documentElement).toHaveAttribute("lang", "en")
  expect(screen.queryByText("old report")).not.toBeInTheDocument()
})

it("retains text typed while the previous message is in flight", async () => {
  const { controller, api } = await collectingController("en")
  let release!: (view: SessionView) => void
  vi.mocked(api.message).mockImplementation(() => new Promise((resolve) => { release = resolve }))
  render(<IntakePage controller={controller} />)
  const input = screen.getByRole("textbox", { name: "Your message" })
  fireEvent.change(input, { target: { value: "first" } })
  fireEvent.click(screen.getByRole("button", { name: "Send" }))
  await waitFor(() => expect(api.message).toHaveBeenCalled())
  fireEvent.change(input, { target: { value: "a new correction" } })
  await act(async () => { release(emptySession({ revision: 4 })) })
  expect(input).toHaveValue("a new correction")
})

it("copies selected files before the input file list is cleared", async () => {
  const { controller, api } = await collectingController("en")
  render(<IntakePage controller={controller} />)
  const files = [new File(["a"], "one.png", { type: "image/png" }), new File(["b"], "two.png", { type: "image/png" })]
  // Real FileList is live: clearing the native input mutates that same list.
  const input = screen.getByLabelText("Attach screenshots") as HTMLInputElement
  Object.defineProperty(input, "files", { configurable: true, get: () => files })
  Object.defineProperty(input, "value", { configurable: true, set: () => { files.length = 0 } })
  fireEvent.change(input)
  await waitFor(() => expect(api.upload).toHaveBeenCalledTimes(2))
})

it("labels conflicting and inapplicable facts on the confirmation surface", async () => {
  const api = fakeApi({ phase: "review_ready", review: { ...review, facts: {
    amount: { key: "amount", status: "conflicting", value: "50000", normalized: null, evidence: [] },
    date: { key: "date", status: "not_applicable", value: null, normalized: null, evidence: [] },
  } } })
  const controller = new IntakeController(api, memoryStorage())
  await controller.initialize("en", CUSTOMER_PHONE)
  render(<IntakePage controller={controller} />)
  expect(screen.getByText("Conflicting: 50000", { exact: true })).toBeVisible()
  expect(screen.getByText("Not applicable")).toBeVisible()
})

it("renders the complete themed page when browser storage is denied", async () => {
  const { controller } = await collectingController("en")
  const denied = vi.spyOn(window, "localStorage", "get").mockImplementation(() => { throw new DOMException("Denied", "SecurityError") })
  try {
    render(<ThemeProvider defaultTheme="dark"><IntakePage controller={controller} /></ThemeProvider>)
    expect(screen.getByRole("textbox", { name: "Your message" })).toBeVisible()
    fireEvent.keyDown(window, { key: "d" })
    expect(document.documentElement).toHaveClass("light")
  } finally { denied.mockRestore() }
})
