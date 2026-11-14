import { Cpu } from "lucide-react"
import { Tooltip, TooltipContent, TooltipTrigger } from "@/components/ui/tooltip"
import { useCopy } from "@/lib/locale"
import { MODEL_STEPS } from "@/lib/model-steps"
import { useWorkspace } from "@/lib/workspace"

export function AiLocalityChip() {
  const { health } = useWorkspace()
  const copy = useCopy()
  const ai = health?.ai
  if (!ai) return null
  return (
    <Tooltip>
      <TooltipTrigger render={<span className={`ai-chip ai-${ai.locality}`} tabIndex={0} />}>
        <Cpu size={12} />
        {copy.ai[ai.locality]}
      </TooltipTrigger>
      <TooltipContent className="ai-locality-tooltip" side="bottom" align="end" sideOffset={8}>
        <p className="ai-locality-title">{copy.ai.tooltip}</p>
        <ul className="ai-locality-steps">
          {MODEL_STEPS.map((step) => {
            const item = ai.steps[step]
            return item ? (
              <li key={step}>
                <span className="ai-locality-step">{copy.models.steps[step]}</span>
                <span className={`ai-locality-where${item.locality === "local" ? " is-local" : ""}`}>
                  {copy.models.locality[item.locality]}
                </span>
                <span className="ai-locality-model">
                  <bdi dir="ltr">{item.model}</bdi>
                </span>
              </li>
            ) : null
          })}
        </ul>
      </TooltipContent>
    </Tooltip>
  )
}
