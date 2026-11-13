import { render, screen } from "@testing-library/react"
import userEvent from "@testing-library/user-event"
import { describe, expect, it, vi } from "vitest"
import { AgentChat } from "./agent-chat"

describe("AgentChat stop control", () => {
  it.each(["streaming", "submitted"] as const)(
    "disables Stop without a handler in %s state",
    (status) => {
      render(<AgentChat messages={[]} status={status} />)
      expect(screen.getByRole("button", { name: "Stop" })).toBeDisabled()
    }
  )

  it("keeps Stop enabled and calls a supplied handler", async () => {
    const user = userEvent.setup()
    const onStop = vi.fn()
    render(<AgentChat messages={[]} status="streaming" onStop={onStop} />)

    const button = screen.getByRole("button", { name: "Stop" })
    expect(button).toBeEnabled()
    await user.click(button)
    expect(onStop).toHaveBeenCalledTimes(1)
  })
})

describe("AgentChat interview parts", () => {
  it("renders a typing indicator, a pending user bubble and the input mode", () => {
    render(
      <AgentChat
        inputMode="tel"
        messages={[
          { id: "u", role: "user", pending: true, parts: [{ type: "text", text: "hello" }] },
          { id: "t", role: "assistant", parts: [{ type: "typing", label: "Support is typing…" }] },
        ]}
      />
    )
    expect(screen.getByRole("img", { name: "Support is typing…" })).toBeVisible()
    expect(screen.getByText("hello")).toHaveClass("opacity-60")
    expect(screen.getByRole("textbox")).toHaveAttribute("inputmode", "tel")
  })
})
