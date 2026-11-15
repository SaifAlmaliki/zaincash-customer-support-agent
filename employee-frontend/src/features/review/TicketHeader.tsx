import { RefreshCw } from "lucide-react"
import { Link } from "react-router-dom"
import { Button } from "@/components/ui/button"
import { PageHeader, PriorityBadge, StatusBadge } from "@/components/shared/workspace-ui"
import { dateLabel, timeLabel } from "@/lib/format"
import { useCopy } from "@/lib/locale"
import { customerPath } from "@/lib/phone"
import type { Result } from "@/lib/types"

export function TicketHeader({
  result,
  onReprocess,
  reprocessing = false,
}: {
  result: Result
  onReprocess?: () => void
  reprocessing?: boolean
}) {
  const text = useCopy().review
  const { customer_phone: phone, external_id, received_at } = result.ticket
  const busy = reprocessing || result.status === "processing"
  return (
    <PageHeader
      title={
        <Link to={customerPath(phone)} className="customer-title-link" title={text.customerProfile}>
          <bdi dir="ltr">{phone}</bdi>
        </Link>
      }
      description={`${external_id} · ${dateLabel(received_at)}, ${timeLabel(received_at)} ${text.baghdad}`}
    >
      {onReprocess && (
        <Button variant="outline" disabled={busy} onClick={onReprocess}>
          <RefreshCw size={14} />
          {reprocessing ? text.reprocessing : text.reprocess}
        </Button>
      )}
      <PriorityBadge priority={result.priority} />
      <StatusBadge status={result.status} />
    </PageHeader>
  )
}
