import { Button, buttonVariants } from "@workspace/ui/components/button"
import { quietButton } from "./buttons"
import { choiceLabel } from "./composer"
import type { IntakeCopy } from "./copy"
import type { AnswerTo, PendingQuestion } from "./types"

export function QuestionExtras({
  question,
  copy,
  interactive,
  attachInputId,
  attachDisabled,
  onAnswer,
}: {
  question: PendingQuestion
  copy: IntakeCopy
  interactive: boolean
  attachInputId: string
  attachDisabled: boolean
  onAnswer: (text: string, answer: AnswerTo) => void
}) {
  return (
    <div className="intake-question-extras">
      {question.reason ? (
        <p className="intake-why" dir="auto">
          {copy.whyPrefix} {question.reason}
        </p>
      ) : null}
      {interactive && question.choices.length ? (
        <div className="intake-choices" role="group" aria-label={copy.quickReplies}>
          {question.choices.map((choice) => {
            const label = choiceLabel(choice, question.answer_kind, copy)
            if (choice === "attach") {
              return (
                <label
                  key={choice}
                  htmlFor={attachInputId}
                  aria-disabled={attachDisabled}
                  className={`${buttonVariants({ variant: "outline", size: "sm" })} ${quietButton} intake-choice${attachDisabled ? " is-disabled" : ""}`}
                >
                  {label}
                </label>
              )
            }
            return (
              <Button
                key={choice}
                type="button"
                variant="outline"
                size="sm"
                className={`${quietButton} intake-choice`}
                onClick={() => onAnswer(label, { message_id: question.message_id, key: question.key, choice })}
              >
                {label}
              </Button>
            )
          })}
        </div>
      ) : null}
    </div>
  )
}
