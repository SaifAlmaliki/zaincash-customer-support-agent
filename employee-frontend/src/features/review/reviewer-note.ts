import type { Result } from "@/lib/types"
import { teamName } from "./ticket-flow-copy"

const STATUS_AR: Record<string, string> = {
  pending: "معلّقة",
  completed: "مكتملة",
  failed: "فاشلة",
  declined: "مرفوضة",
}

function latinCount(text: string): number {
  return text.match(/[A-Za-z]/g)?.length ?? 0
}

function arabicCount(text: string): number {
  return text.match(/[\u0600-\u06FF]/g)?.length ?? 0
}

function englishProse(text: string): boolean {
  return latinCount(text) > arabicCount(text)
}

export function noteIsArabic(text: string): boolean {
  return arabicCount(text) > latinCount(text)
}

function ltr(value: string): string {
  return `\u2066${value}\u2069`
}

function day(value: string | number | null | undefined): string | null {
  if (value == null || value === "") return null
  return String(value).match(/\d{4}-\d{2}-\d{2}/)?.[0] ?? null
}

function factText(result: Result, key: string): string | null {
  const fact = result.intake?.facts?.[key]
  if (!fact || fact.status === "unknown") return null
  const value = fact.normalized ?? fact.value
  if (value == null || String(value).trim() === "") return null
  return String(value).trim()
}

function arabicInternalNote(result: Result): string | null {
  const txn = result.transaction
  const ref = String(txn?.txn_ref ?? result.matched_txn_ref ?? result.extracted?.txn_ref?.value ?? "").trim()
  const recordDate = day(txn?.created_at)
  const ticketDate = day(result.extracted?.date?.value) ?? day(factText(result, "date"))
  const recordName = txn?.receiver_name ? String(txn.receiver_name).trim() : ""
  const ticketName = factText(result, "recipient_name") ?? ""
  const status = txn?.status ? String(txn.status) : ""
  const parts: string[] = []

  if (result.lookup_status === "date_mismatch" && ref && recordDate && ticketDate) {
    parts.push(
      `وُجدت العملية ${ltr(ref)}، لكن التاريخ لا يطابق السجل (${ltr(recordDate)} في السجل، و${ltr(ticketDate)} في التذكرة).`,
    )
  } else if (result.lookup_status === "amount_mismatch" && ref) {
    parts.push(`وُجدت العملية ${ltr(ref)}، لكن المبلغ لا يطابق السجل.`)
  } else if (result.lookup_status === "not_found") {
    parts.push(ref ? `لم تُوجد العملية ${ltr(ref)} في السجل.` : "لا توجد عملية مطابقة في السجل.")
  } else if (result.lookup_status === "ambiguous") {
    parts.push("تطابق أكثر من عملية، لذلك لم تُعتمد أي منها.")
  } else if (result.lookup_status === "matched" && ref) {
    parts.push(`العملية ${ltr(ref)} مطابقة للسجل.`)
  }

  if (status) parts.push(`الحالة في السجل «${STATUS_AR[status] ?? status}».`)
  if (recordName && ticketName && recordName !== ticketName) {
    parts.push(`اسم المستلم في السجل «${recordName}»، بينما التذكرة تقول «${ticketName}».`)
  }
  if (result.escalated && result.team) {
    parts.push(`أُحيلت إلى ${teamName(result.team, true)} حسب السياسة.`)
  }
  return parts.length ? parts.join(" ") : null
}

function storedNote(result: Result): string {
  const own = result.internal_note?.trim()
  if (own) return own
  const parts = (result.escalation_note ?? "").split(/(?<=\.)\s+/).map((part) => part.trim()).filter(Boolean)
  const seen = new Set<string>()
  const unique = parts.filter((part) => (seen.has(part) ? false : seen.add(part)))
  const escalated = unique.filter((part) => part.startsWith("Escalated:"))
  const analysis = unique.filter((part) => !part.startsWith("Escalated:"))
  const summary = escalated.sort((a, b) => b.length - a.length)[0]
  return [summary, ...analysis].filter(Boolean).join(" ")
}

export function reviewerNote(result: Result, arabic: boolean): string {
  const stored = storedNote(result)
  if (arabic && englishProse(stored)) return arabicInternalNote(result) || stored
  return stored
}
