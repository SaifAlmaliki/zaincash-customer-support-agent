import { normalizeCustomerPhone } from "./phone"
import type { TicketInput } from "./types"

function csvRows(text: string): string[][] {
  const rows: string[][] = []
  let row: string[] = [],
    field = "",
    quoted = false
  for (let i = 0; i < text.length; i++) {
    const char = text[i]
    if (char === '"') {
      if (quoted && text[i + 1] === '"') {
        field += '"'
        i++
      } else quoted = !quoted
    } else if (char === "," && !quoted) {
      row.push(field)
      field = ""
    } else if ((char === "\n" || char === "\r") && !quoted) {
      if (char === "\r" && text[i + 1] === "\n") i++
      row.push(field)
      if (row.some(Boolean)) rows.push(row)
      row = []
      field = ""
    } else field += char
  }
  if (quoted) throw new Error("A quoted CSV field is not closed.")
  row.push(field)
  if (row.some(Boolean)) rows.push(row)
  return rows
}

export function parseTicketFile(
  contents: string,
  filename: string
): TicketInput[] {
  const text = contents.replace(/^\uFEFF/, "")
  let rows: unknown
  if (filename.endsWith(".csv")) {
    const [header, ...body] = csvRows(text)
    if (!header) throw new Error("The file is empty.")
    rows = body.map((row) =>
      Object.fromEntries(header.map((key, i) => [key.trim(), row[i] || ""]))
    )
  } else if (filename.endsWith(".jsonl"))
    rows = text
      .split(/\r?\n/)
      .filter((line) => line.trim())
      .map((line) => JSON.parse(line))
  else if (filename.endsWith(".json")) {
    const data = JSON.parse(text)
    rows = Array.isArray(data) ? data : data.tickets
  } else throw new Error("Choose a .csv, .json or .jsonl ticket file.")
  if (!Array.isArray(rows) || rows.length === 0)
    throw new Error("Provide a nonempty array of tickets.")
  if (rows.length > 500)
    throw new Error("A batch can contain up to 500 tickets.")
  const ids = new Set<string>()
  const badPhoneRows: number[] = []
  const tickets = rows.map((row, index) => {
    if (!row || typeof row !== "object")
      throw new Error(`Row ${index + 1} must be a ticket object.`)
    const message = row.text ?? row.message
    if (typeof message !== "string" || !message.trim())
      throw new Error(`Row ${index + 1} needs a message.`)
    if (message.length > 6000)
      throw new Error(`Row ${index + 1} exceeds 6,000 characters.`)
    const id = String(
      row.external_id || row.id || `UI-${crypto.randomUUID().slice(0, 12)}`
    )
    if (ids.has(id)) throw new Error("Each ticket must have a unique ID.")
    ids.add(id)
    const channel = row.channel || "app"
    if (!["app", "whatsapp", "call_note"].includes(channel))
      throw new Error(`Row ${index + 1} has an unknown channel.`)
    const phone = normalizeCustomerPhone(String(row.customer_phone ?? ""))
    if (!phone) badPhoneRows.push(index + 1)
    return {
      external_id: id,
      text: message.trim(),
      channel,
      ...(row.received_at ? { received_at: String(row.received_at) } : {}),
      customer_phone: phone as string,
    }
  })
  if (badPhoneRows.length === 1)
    throw new Error(`Row ${badPhoneRows[0]} needs a valid customer phone (07XXXXXXXXX).`)
  if (badPhoneRows.length > 1)
    throw new Error(`Rows ${badPhoneRows.join(", ")} need a valid customer phone (07XXXXXXXXX).`)
  return tickets
}
