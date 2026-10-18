import type { IntakeCopy } from "./copy"
import type { Receipt } from "./types"

export function ReceiptPanel({ receipt, copy }: { receipt: Receipt; copy: IntakeCopy }) {
  const detail =
    receipt.processing_status === "needs_attention"
      ? copy.receiptAttention
      : receipt.processing_status === "ready_for_employee"
        ? copy.receiptReady
        : copy.receiptProcessing
  return (
    <section className="intake-receipt" aria-labelledby="intake-receipt-heading">
      <h2 id="intake-receipt-heading">{copy.receiptTitle}</h2>
      <p>
        <bdi dir="ltr">{receipt.ticket_reference}</bdi>
      </p>
      <p>{detail}</p>
    </section>
  )
}
