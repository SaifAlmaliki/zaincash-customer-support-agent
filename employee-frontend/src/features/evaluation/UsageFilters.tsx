import { RefreshCw } from "lucide-react"
import { Button } from "@/components/ui/button"
import { FilterSelect } from "@/components/shared/workspace-ui"
import { fill, useCopy } from "@/lib/locale"
import type { AiProcess, UsageFilters as Filters, UsagePeriod } from "@/lib/types"
import { PROCESS_ORDER, processLabel } from "./usage-view"

export function UsageFilters({ filters, onChange, models, runs, onRefresh }: {
  filters: Filters
  onChange: (filters: Filters) => void
  models: string[]
  runs: number[]
  onRefresh: () => void
}) {
  const copy = useCopy().evaluation
  const f = copy.filters
  return (
    <div className="usage-filters">
      <FilterSelect label={f.period} value={filters.period}
        options={[{ value: "24h", label: f.day }, { value: "7d", label: f.week }, { value: "30d", label: f.month }]}
        onChange={(value) => onChange({ ...filters, period: value as UsagePeriod })} />
      <FilterSelect label={f.process} value={filters.process}
        options={[{ value: "all", label: f.allProcesses },
                  ...PROCESS_ORDER.map((p) => ({ value: p, label: processLabel(p, copy) }))]}
        onChange={(value) => onChange({ ...filters, process: value as AiProcess | "all" })} />
      <FilterSelect label={f.model} value={filters.model || "all"}
        options={[{ value: "all", label: f.allModels }, ...models.map((m) => ({ value: m, label: m }))]}
        onChange={(value) => onChange({ ...filters, model: value === "all" ? "" : value })} />
      <FilterSelect label={f.run} value={filters.runId || "all"}
        options={[{ value: "all", label: f.allRuns },
                  ...runs.map((id) => ({ value: String(id), label: fill(f.runOption, { id: String(id).padStart(3, "0") }) }))]}
        onChange={(value) => onChange({ ...filters, runId: value === "all" ? "" : value })} />
      <Button variant="outline" onClick={onRefresh}>
        <RefreshCw size={15} />
        {copy.refresh}
      </Button>
    </div>
  )
}
