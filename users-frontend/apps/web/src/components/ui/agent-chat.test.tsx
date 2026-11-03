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
