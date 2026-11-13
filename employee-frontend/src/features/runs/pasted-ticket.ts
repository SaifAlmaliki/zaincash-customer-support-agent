import { normalizeCustomerPhone } from "@/lib/phone"
import type { TicketInput } from "@/lib/types"

export function pastedTickets(message: string, channel: TicketInput["channel"], phone: string): TicketInput[] {
  const customerPhone = normalizeCustomerPhone(phone)
  return message.trim() && customerPhone ? [{ text: message, channel, customer_phone: customerPhone }] : []
}
