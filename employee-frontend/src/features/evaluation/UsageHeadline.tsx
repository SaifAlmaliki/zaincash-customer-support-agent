import { AlertTriangle, Clock3, Coins, Receipt, Ticket } from "lucide-react"
import { Metric } from "@/components/shared/workspace-ui"
import { msLabel, percent1, usd } from "@/lib/format"
import { fill, useCopy } from "@/lib/locale"
import type { UsageTotals } from "@/lib/types"

export function UsageHeadline({ totals }: { totals: UsageTotals }) {
  const h = useCopy().evaluation.headline
  return (
    <div className="metrics-grid usage-headline">
      <Metric label={h.cost} value={usd(totals.calls ? totals.cost_usd : null)}
              detail={fill(h.costDetail, { calls: totals.calls })} icon={<Coins size={19} />} />
      <Metric label={h.perTicket} value={usd(totals.cost_per_ticket_avg)}
              detail={fill(h.perTicketDetail, { value: usd(totals.cost_per_ticket_p95) })} icon={<Receipt size={19} />} />
      <Metric label={h.time} value={msLabel(totals.ai_time_p50_ms)}
              detail={fill(h.timeDetail, { value: msLabel(totals.ai_time_p95_ms) })} icon={<Clock3 size={19} />} />
      <Metric label={h.errors} value={percent1(totals.error_rate)}
              detail={fill(h.errorsDetail, { count: totals.errors })} icon={<AlertTriangle size={19} />} />
      <Metric label={h.tickets} value={totals.tickets}
              detail={fill(h.ticketsDetail, { count: totals.unknown_cost_calls })} icon={<Ticket size={19} />} />
    </div>
  )
}
