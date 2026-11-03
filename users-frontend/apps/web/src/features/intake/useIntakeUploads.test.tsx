import { act, renderHook, waitFor } from "@testing-library/react"
import { afterEach, describe, expect, it, vi } from "vitest"
import type { IntakeApi, UploadResult } from "./api"
import { IntakeController } from "./controller"
import { memoryStorage } from "./session"
import { attachment, emptySession, fakeApi } from "./test/fixtures"
import { useIntakeUploads } from "./useIntakeUploads"

function uploadResult(): UploadResult {
  return { attachment, session: emptySession({ attachments: [attachment] }) }
}

type Pending = {
  onProgress?: (fraction: number) => void
  resolve: (value: UploadResult) => void
}

function deferredUploads(api: IntakeApi): Pending[] {
  const pending: Pending[] = []
  vi.mocked(api.upload).mockImplementation(
    (_credentials, _file, _requestId, _revision, onProgress) =>
      new Promise<UploadResult>((resolve) => {
        pending.push({ onProgress, resolve })
      }),
  )
  return pending
}

function mockUrls() {
  const create = vi.spyOn(URL, "createObjectURL")
    .mockReturnValueOnce("blob:one")
    .mockReturnValueOnce("blob:two")
  const revoke = vi.spyOn(URL, "revokeObjectURL").mockImplementation(() => undefined)
  return { create, revoke }
}

afterEach(() => {
  vi.restoreAllMocks()
})

describe("useIntakeUploads", () => {
  it("keeps identical filenames and bytes on independent client IDs and progress keys", async () => {
    const { revoke } = mockUrls()
    const api = fakeApi()
    const pending = deferredUploads(api)
    const controller = new IntakeController(api, memoryStorage())
    await controller.initialize("en")
    const ids = ["client-one", "client-two"]
    const { result } = renderHook(() =>
      useIntakeUploads(controller, () => ids.shift()!),
    )
    const files = [
      new File(["same"], "error.png", { type: "image/png" }),
      new File(["same"], "error.png", { type: "image/png" }),
    ]

    let selection!: Promise<void>
    act(() => {
      selection = result.current.selectFiles(files)
    })
    await waitFor(() => expect(pending).toHaveLength(1))
    expect(result.current.previews.map((item) => item.id)).toEqual([
      "client-one",
      "client-two",
    ])

    act(() => pending[0]!.onProgress?.(0.25))
    expect(controller.getSnapshot().uploads).toEqual({ "client-one": 0.25 })

    await act(async () => {
      pending[0]!.resolve(uploadResult())
      await Promise.resolve()
    })
    await waitFor(() => expect(pending).toHaveLength(2))
    act(() => pending[1]!.onProgress?.(0.5))
    expect(controller.getSnapshot().uploads).toEqual({ "client-two": 0.5 })
    expect(result.current.previews.map((item) => item.id)).toEqual(["client-two"])

    await act(async () => {
      pending[1]!.resolve(uploadResult())
      await selection
    })
    expect(result.current.previews).toEqual([])
    expect(revoke).toHaveBeenCalledWith("blob:one")
    expect(revoke).toHaveBeenCalledWith("blob:two")
  })

  it("stops on the first failure and removes current plus unattempted previews", async () => {
    const { revoke } = mockUrls()
    const api = fakeApi()
    vi.mocked(api.upload).mockRejectedValueOnce(new TypeError("offline"))
    const controller = new IntakeController(api, memoryStorage())
    await controller.initialize("en")
    const ids = ["client-one", "client-two"]
    const { result } = renderHook(() =>
      useIntakeUploads(controller, () => ids.shift()!),
    )
    const files = [
      new File(["one"], "one.png", { type: "image/png" }),
      new File(["two"], "two.png", { type: "image/png" }),
    ]

    await act(async () => {
      await result.current.selectFiles(files)
    })

    expect(api.upload).toHaveBeenCalledTimes(1)
    expect(result.current.previews).toEqual([])
    expect(revoke).toHaveBeenCalledWith("blob:one")
    expect(revoke).toHaveBeenCalledWith("blob:two")
  })

  it("revokes outstanding URLs on unmount and does not start a later upload", async () => {
    const { revoke } = mockUrls()
    const api = fakeApi()
    const pending = deferredUploads(api)
    const controller = new IntakeController(api, memoryStorage())
    await controller.initialize("en")
    const ids = ["client-one", "client-two"]
    const { result, unmount } = renderHook(() =>
      useIntakeUploads(controller, () => ids.shift()!),
    )

    let selection!: Promise<void>
    act(() => {
      selection = result.current.selectFiles([
        new File(["one"], "one.png", { type: "image/png" }),
        new File(["two"], "two.png", { type: "image/png" }),
      ])
    })
    await waitFor(() => expect(pending).toHaveLength(1))
    unmount()
    expect(revoke).toHaveBeenCalledWith("blob:one")
    expect(revoke).toHaveBeenCalledWith("blob:two")

    await act(async () => {
      pending[0]!.resolve(uploadResult())
      await selection
    })
    expect(api.upload).toHaveBeenCalledTimes(1)
  })
})
