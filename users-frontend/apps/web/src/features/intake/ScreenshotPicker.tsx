import { Button } from "@workspace/ui/components/button"
import type { IntakeCopy } from "./copy"
import type { Attachment } from "./types"

export function ScreenshotPicker({
  copy,
  attachments,
  previews,
  progress,
  disabled,
  onSelect,
  onRemove,
}: {
  copy: IntakeCopy
  attachments: Attachment[]
  previews: { name: string; url: string }[]
  progress: Record<string, number>
  disabled: boolean
  onSelect: (files: FileList) => void
  onRemove: (attachmentId: string) => void
}) {
  const visible = attachments.filter((item) => !item.removed)
  return (
    <div className="intake-shots">
      <label className="intake-label" htmlFor="intake-shots">
        {copy.attach}
      </label>
      <input
        id="intake-shots"
        type="file"
        accept="image/png,image/jpeg,image/webp"
        multiple
        disabled={disabled}
        onChange={(event) => {
          if (event.target.files?.length) onSelect(event.target.files)
          event.target.value = ""
        }}
      />
      <ul className="intake-shot-list">
        {previews.map((preview) => (
          <li key={preview.url}>
            <img src={preview.url} alt={preview.name} />
            <progress value={progress[preview.name] ?? 0} max={1} aria-label={`${copy.uploadProgress} ${preview.name}`} />
          </li>
        ))}
        {visible.map((attachment) => (
          <li key={attachment.id}>
            <span dir="auto">{attachment.filename}</span>
            <Button type="button" variant="outline" disabled={disabled} onClick={() => onRemove(attachment.id)}>
              {copy.remove}
            </Button>
          </li>
        ))}
      </ul>
    </div>
  )
}
