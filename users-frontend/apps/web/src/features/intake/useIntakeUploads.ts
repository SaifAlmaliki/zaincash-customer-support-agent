import { useCallback, useEffect, useRef, useState } from "react"
import type { IntakeController } from "./controller"

export type UploadPreview = {
  id: string
  name: string
  url: string
}

export function useIntakeUploads(
  controller: IntakeController,
  createId: () => string = () => crypto.randomUUID(),
) {
  const [previews, setPreviews] = useState<UploadPreview[]>([])
  const previewUrls = useRef(new Map<string, string>())
  const mounted = useRef(true)

  const clearPreviews = useCallback((ids?: ReadonlySet<string>) => {
    if (mounted.current) {
      setPreviews((current) =>
        ids ? current.filter((item) => !ids.has(item.id)) : [],
      )
    }
    for (const [id, url] of previewUrls.current) {
      if (ids && !ids.has(id)) continue
      URL.revokeObjectURL(url)
      previewUrls.current.delete(id)
    }
  }, [])

  useEffect(() => {
    mounted.current = true
    return () => {
      mounted.current = false
      clearPreviews()
    }
  }, [clearPreviews])

  const selectFiles = useCallback(async (files: File[]) => {
    const local = files.map((file) => ({
      file,
      preview: {
        id: createId(),
        name: file.name,
        url: URL.createObjectURL(file),
      },
    }))
    for (const item of local) {
      previewUrls.current.set(item.preview.id, item.preview.url)
    }
    if (mounted.current) {
      setPreviews((current) => [
        ...current,
        ...local.map((item) => item.preview),
      ])
    }

    for (let index = 0; index < local.length; index += 1) {
      const item = local[index]!
      try {
        await controller.upload(item.file, item.preview.id)
      } catch {
        clearPreviews(new Set(local.slice(index).map((entry) => entry.preview.id)))
        return
      }
      if (!mounted.current) return
      clearPreviews(new Set([item.preview.id]))
    }
  }, [clearPreviews, controller, createId])

  return { previews, selectFiles, clearPreviews }
}
