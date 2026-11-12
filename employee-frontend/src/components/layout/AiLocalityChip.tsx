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
      <TooltipContent>
        <strong className="ai-chip-line">{copy.ai.tooltip}</strong>
        {MODEL_STEPS.map((step) => {
          const item = ai.steps[step]
          return item ? (
            <span key={step} className="ai-chip-line">
              {copy.models.steps[step]}: <span dir="ltr">{item.model}</span> ({copy.models.locality[item.locality]})
            </span>
          ) : null
        })}
      </TooltipContent>
    </Tooltip>
  )
}
