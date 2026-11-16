import { expect, it } from "vitest"
import { resultFixture } from "@/lib/test-fixtures"
import type { IntakeEvidenceData } from "@/lib/types"
import { reviewerNote } from "./reviewer-note"

const english =
  "The transaction ZC2410000123 is found but with a date mismatch (2026-10-06 vs ticket's 2026-11-15). The status is 'pending'. Recipient name in record is 'علي حسين', while ticket says 'مصطفلى'. Escalated to Payments Ops as per policy."

function mismatchTicket() {
  return resultFixture(10, {
    lookup_status: "date_mismatch",
    matched_txn_ref: "ZC2410000123",
    team: "Payments Ops",
    escalated: true,
    internal_note: english,
    extracted: {
      date: { value: "2026-11-15", span: "2026-11-15", start: 0, end: 10, method: "jev_pick", confidence: 1 },
      txn_ref: { value: "ZC2410000123", span: "ZC2410000123", start: 0, end: 12, method: "jev_pick", confidence: 1 },
    },
    transaction: {
      txn_ref: "ZC2410000123",
      status: "pending",
      receiver_name: "علي حسين",
      created_at: "2026-10-06T15:10:00+00:00",
    },
    intake: {
      summary_ar: "",
      quality: null,
      facts: {
        recipient_name: { key: "recipient_name", status: "known", value: "مصطفلى", normalized: null },
        date: { key: "date", status: "known", value: "امس", normalized: "2026-11-15" },
      },
      additional_issues: [],
      unknown_keys: [],
      messages: [],
      attachments: [],
    } satisfies IntakeEvidenceData,
  })
}

it("rewrites an English internal note in Arabic on the Arabic profile", () => {
  const note = reviewerNote(mismatchTicket(), true)
  expect(note).toContain("وُجدت العملية")
  expect(note).toContain("ZC2410000123")
  expect(note).toContain("2026-10-06")
  expect(note).toContain("2026-11-15")
  expect(note).toContain("معلّقة")
  expect(note).toContain("علي حسين")
  expect(note).toContain("مصطفلى")
  expect(note).toContain("عمليات المدفوعات")
  expect(note).not.toContain("date mismatch")
})

it("keeps the English internal note on the English profile", () => {
  expect(reviewerNote(mismatchTicket(), false)).toBe(english)
})

it("keeps an internal note that is already Arabic", () => {
  const arabic = "وُجدت العملية والتاريخ مختلف. أُحيلت إلى عمليات المدفوعات."
  const result = mismatchTicket()
  result.internal_note = arabic
  expect(reviewerNote(result, true)).toBe(arabic)
})
