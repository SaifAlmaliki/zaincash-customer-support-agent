import { getCopy, getLocale } from "@/lib/locale"

export const categories: Record<string, string> = {
  failed_transfer: "Failed transfer",
  wrong_recipient: "Wrong recipient",
  login_access: "Login & access",
  agent_dispute: "Agent dispute",
  card_issue: "Card issue",
  bill_payment: "Bill payment",
  account_kyc: "Account verification",
  refund_request: "Refund request",
  fraud_report: "Fraud report",
  app_bug: "App issue",
  general_inquiry: "General inquiry",
  other: "Other",
}
export const teams = [
  "Payments Ops",
  "Disputes",
  "Account & Security",
  "Agent Network",
  "Cards",
  "Tech Support",
  "General Care",
]
export const categoryLabel = (id: string | null) => {
  const labels = getCopy().categories as Record<string, string>
  return id ? labels[id] || categories[id] || id.replaceAll("_", " ") : getCopy().common.unclassified
}
export const teamLabel = (id: string | null | undefined) => {
  if (!id) return getCopy().common.unassigned
  const labels = getCopy().teams as Record<string, string>
  return labels[id] || id
}
export const humanize = (text: string) =>
  text.replaceAll("_", " ").replace(/^./, (c) => c.toUpperCase())
export const percentage = (value: number | null | undefined) =>
  value == null ? "—" : `${Math.round(value * 100)}%`
export const dateLabel = (value: string) =>
  new Intl.DateTimeFormat(getLocale() === "ar" ? "ar-IQ-u-nu-latn" : "en-GB", {
    day: "numeric",
    month: "short",
    timeZone: "Asia/Baghdad",
  }).format(new Date(value))
export const timeLabel = (value: string) =>
  new Intl.DateTimeFormat(getLocale() === "ar" ? "ar-IQ-u-nu-latn" : "en-GB", {
    hour: "2-digit",
    minute: "2-digit",
    timeZone: "Asia/Baghdad",
  }).format(new Date(value))
export const duration = (ms: number) =>
  ms < 1000 ? `${ms} ms` : `${(ms / 1000).toFixed(1)} s`
export const sizeLabel = (bytes: number) =>
  bytes < 1024 * 1024
    ? `${Math.max(1, Math.round(bytes / 1024))} KB`
    : `${(bytes / 1024 / 1024).toFixed(1)} MB`
export function downloadJson(value: unknown, filename: string) {
  const url = URL.createObjectURL(
    new Blob([JSON.stringify(value, null, 2)], { type: "application/json" })
  )
  const link = document.createElement("a")
  link.href = url
  link.download = filename
  link.click()
  setTimeout(() => URL.revokeObjectURL(url), 1000)
}
