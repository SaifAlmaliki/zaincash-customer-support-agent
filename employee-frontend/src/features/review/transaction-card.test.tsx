import { renderToStaticMarkup } from "react-dom/server"
import { expect, it } from "vitest"
import { resultFixture } from "@/lib/test-fixtures"
import type { InvestigatedTransaction } from "@/lib/types"
import { TransactionCard } from "./SourceEvidence"

const REASON = "الدفع الإلكتروني غير مفعّل على البطاقة"
const FOUND = "عمليات وجدها البحث (غير مؤكدة)"
const SKIPPED = "هذه المشكلة لا تحتاج البحث عن عملية"

function declined(txn_ref: string, receiver_name: string, amount_iqd: number, created_at: string): InvestigatedTransaction {
  return {
    txn_ref, sender_phone: "07851110004", receiver_phone: null, receiver_name, amount_iqd,
    type: "card", status: "declined", created_at, biller: null, agent_id: null, failure_reason: REASON,
  }
}

it("shows found rows when there is no confirmed transaction", () => {
  const result = resultFixture(9, {
    transaction: null, lookup_status: "not_applicable", investigated_transactions: [
      declined("ZC2410001006", "متجر الرافدين", 12000, "2026-10-07T09:15:00+03:00"),
      declined("ZC2410001005", "سوق بغداد أونلاين", 45000, "2026-10-06T20:40:00+03:00"),
    ],
  })
  const html = renderToStaticMarkup(<TransactionCard result={result} />)
  for (const text of [FOUND, "متجر الرافدين", "12,000 IQD", "مرفوضة", "دفع بالبطاقة", REASON, "ZC2410001005"]) {
    expect(html).toContain(text)
  }
  expect(html).not.toContain(SKIPPED)
})

it("shows the confirmed transaction instead of found rows", () => {
  const result = resultFixture(9, {
    lookup_status: "matched", matched_txn_ref: "ZC2410001004",
    transaction: { txn_ref: "ZC2410001004", amount_iqd: 25000, status: "completed", type: "merchant" },
    investigated_transactions: [declined("ZC2410001006", "متجر الرافدين", 12000, "2026-10-07T09:15:00+03:00")],
  })
  const html = renderToStaticMarkup(<TransactionCard result={result} />)
  expect(html).toContain("ZC2410001004")
  expect(html).not.toContain(FOUND)
})

it("keeps the skipped message when nothing was found", () => {
  const html = renderToStaticMarkup(
    <TransactionCard result={resultFixture(9, { transaction: null, investigated_transactions: [] })} />,
  )
  expect(html).toContain(SKIPPED)
})
