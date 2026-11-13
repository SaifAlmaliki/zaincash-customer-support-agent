import { Link } from "react-router-dom"
import { Smartphone } from "lucide-react"
import { dateLabel, timeLabel } from "@/lib/format"
import { customerPath } from "@/lib/phone"
import type { Ticket } from "@/lib/types"

export function TicketIdentity({
  ticket,
  index,
  ticketPath,
}: {
  ticket: Ticket
  index: number
  ticketPath: string
}) {
  return (
    <div className="ticket-identity">
      <span className={`ticket-avatar avatar-${index % 4}`}>
        <Smartphone size={17} />
      </span>
      <div>
        <Link to={customerPath(ticket.customer_phone)} className="ticket-id">
          <bdi dir="ltr">{ticket.customer_phone}</bdi>
        </Link>
        <small>
          <Link to={ticketPath}>
            <bdi dir="ltr">{ticket.external_id}</bdi>
          </Link>{" "}
          · {dateLabel(ticket.received_at)}, {timeLabel(ticket.received_at)}
        </small>
      </div>
    </div>
  )
}
