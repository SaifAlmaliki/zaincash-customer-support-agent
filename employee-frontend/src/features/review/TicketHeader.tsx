import { Link } from "react-router-dom"
import { PageHeader, PriorityBadge, StatusBadge } from "@/components/shared/workspace-ui"
import { dateLabel, timeLabel } from "@/lib/format"
import { useCopy } from "@/lib/locale"
import { customerPath } from "@/lib/phone"
import type { Result } from "@/lib/types"

export function TicketHeader({ result }: { result: Result }) {
  const text = useCopy().review
  const { customer_phone: phone, external_id, received_at } = result.ticket
  return (
    <PageHeader
      title={
        <Link to={customerPath(phone)} className="customer-title-link" title={text.customerProfile}>
          <bdi dir="ltr">{phone}</bdi>
        </Link>
      }
      description={`${external_id} · ${dateLabel(received_at)}, ${timeLabel(received_at)} ${text.baghdad}`}
    >
      <PriorityBadge priority={result.priority} />
      <StatusBadge status={result.status} />
    </PageHeader>
  )
}
