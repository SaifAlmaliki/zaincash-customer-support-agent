import type { Activity } from "./controller"
import type { IntakeCopy } from "./copy"
import type { AnswerKind, Choice } from "./types"

export type ComposerHint = { placeholder: string; inputMode: "text" | "tel" | "numeric" }

export function composerHint(kind: AnswerKind | null, copy: IntakeCopy): ComposerHint {
  switch (kind) {
    case "phone":
      return { placeholder: copy.hintPhone, inputMode: "tel" }
    case "amount":
      return { placeholder: copy.hintAmount, inputMode: "numeric" }
    case "reference":
      return { placeholder: copy.hintReference, inputMode: "text" }
    case "date":
      return { placeholder: copy.hintDate, inputMode: "text" }
    default:
      return { placeholder: copy.placeholder, inputMode: "text" }
  }
}

export function choiceLabel(choice: Choice, kind: AnswerKind, copy: IntakeCopy): string {
  if (choice === "yes") return copy.choiceYes
  if (choice === "no") return copy.choiceNo
  if (choice === "attach") return copy.choiceAttach
  return kind === "reference" ? copy.choiceNoReference : copy.choiceUnknown
}

export function activityText(activity: Activity | null, busy: boolean, processing: boolean, copy: IntakeCopy) {
  if (busy) {
    const text: Record<Activity, string> = {
      message: copy.sending,
      ask: copy.sending,
      review: copy.processing,
      upload: copy.uploading,
      remove: copy.removing,
      submit: copy.submitting,
    }
    return text[activity ?? "message"]
  }
  return processing ? copy.processing : null
}
