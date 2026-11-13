import { Link, useParams } from "react-router-dom"
import { ArrowLeft } from "lucide-react"
import { Button } from "@/components/ui/button"
import { Card } from "@/components/ui/card"
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table"
import {
  EmptyState,
  ErrorState,
  LoadingState,
  PageHeader,
  PriorityBadge,
  StatusBadge,
} from "@/components/shared/workspace-ui"
import { useResource } from "@/hooks/use-resource"
import { ApiError, request } from "@/lib/api"
import { categoryLabel, dateLabel, timeLabel } from "@/lib/format"
import { fill, useCopy } from "@/lib/locale"
import { normalizeCustomerPhone } from "@/lib/phone"
import type { CustomerProfile } from "@/lib/types"
import { useWorkspace } from "@/lib/workspace"

async function loadCustomer(path: string, options: RequestInit) {
  try {
    return await request<CustomerProfile>(path, options)
  } catch (error) {
    if (error instanceof ApiError && error.status === 404) return null
    throw error
  }
}

function CustomerMissing({ title, description }: { title: string; description: string }) {
  const text = useCopy().customer
  return (
    <EmptyState title={title} description={description}>
      <Button nativeButton={false} render={<Link to="/" />}>
        {text.back}
      </Button>
    </EmptyState>
  )
}

export function CustomerProfileView({ customer }: { customer: CustomerProfile }) {
  const text = useCopy().customer
  const ticketCount =
    customer.ticket_count === 1
      ? text.ticketCountOne
      : fill(text.ticketCountMany, { count: customer.ticket_count })
  return (
    <>
      <Link to="/" className="back-link">
        <ArrowLeft size={15} />
        {text.back}
      </Link>
      <PageHeader
        title={<bdi dir="ltr">{customer.phone}</bdi>}
        description={`${fill(text.since, { date: dateLabel(customer.created_at) })} · ${ticketCount}`}
      />
      <Card className="queue-card">
        {customer.results.length ? (
          <Table className="ticket-table">
            <TableHeader>
              <TableRow>
                <TableHead>{text.colTicket}</TableHead>
                <TableHead>{text.colIssue}</TableHead>
                <TableHead>{text.colPriority}</TableHead>
                <TableHead>{text.colStatus}</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {customer.results.map((row) => (
                <TableRow key={row.id} className="ticket-row">
                  <TableCell>
                    <div className="ticket-identity">
                      <div>
                        <Link to={`/tickets/${row.id}`} className="ticket-id">
                          <bdi dir="ltr">{row.ticket.external_id}</bdi>
                        </Link>
                        <small>
                          {dateLabel(row.ticket.received_at)}, {timeLabel(row.ticket.received_at)}
                        </small>
                      </div>
                    </div>
                  </TableCell>
                  <TableCell>
                    <div className="ticket-subject">
                      <strong>{categoryLabel(row.category)}</strong>
                      <p dir="auto" lang="ar">{row.ticket.text}</p>
                    </div>
                  </TableCell>
                  <TableCell>
                    <PriorityBadge priority={row.priority} />
                  </TableCell>
                  <TableCell>
                    <StatusBadge status={row.status} />
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        ) : (
          <EmptyState title={text.noTickets} description={text.noTicketsDetail} />
        )}
      </Card>
    </>
  )
}

export function CustomerPage() {
  const { phone: raw = "" } = useParams()
  const workspace = useWorkspace()
  const text = useCopy().customer
  const phone = normalizeCustomerPhone(raw)
  const query = useResource<CustomerProfile | null>(
    phone ? `/customers/${phone}` : null,
    workspace.revision,
    0,
    loadCustomer,
  )
  if (!phone) return <CustomerMissing title={text.invalid} description={text.invalidDetail} />
  if (query.error) return <ErrorState message={query.error} retry={query.reload} />
  if (query.loading) return <LoadingState />
  if (!query.data) return <CustomerMissing title={text.notFound} description={text.notFoundDetail} />
  return <CustomerProfileView customer={query.data} />
}
