import type { EvaluationReport, TicketInput } from "./types"

function csvRows(text: string): string[][] {
  const rows: string[][] = []
  let row: string[] = [], field = "", quoted = false
  for (let i = 0; i < text.length; i++) {
    const char = text[i]
    if (char === '"') {
      if (quoted && text[i + 1] === '"') { field += '"'; i++ }
      else quoted = !quoted
    } else if (char === "," && !quoted) { row.push(field); field = "" }
    else if ((char === "\n" || char === "\r") && !quoted) {
      if (char === "\r" && text[i + 1] === "\n") i++
      row.push(field); if (row.some(Boolean)) rows.push(row)
      row = []; field = ""
    } else field += char
  }
  if (quoted) throw new Error("A quoted CSV field is not closed.")
  row.push(field); if (row.some(Boolean)) rows.push(row)
  return rows
}

export function parseTicketFile(contents: string, filename: string): TicketInput[] {
  const text = contents.replace(/^\uFEFF/, "")
  let rows: unknown
  if (filename.endsWith(".csv")) {
    const [header, ...body] = csvRows(text)
    if (!header) throw new Error("The file is empty.")
    rows = body.map((row) => Object.fromEntries(header.map((key, i) => [key.trim(), row[i] || ""])))
  } else if (filename.endsWith(".jsonl")) rows = text.split(/\r?\n/).filter((line) => line.trim()).map((line) => JSON.parse(line))
  else if (filename.endsWith(".json")) {
    const data = JSON.parse(text)
    rows = Array.isArray(data) ? data : data.tickets
  } else throw new Error("Choose a .csv, .json or .jsonl ticket file.")
  if (!Array.isArray(rows) || rows.length === 0) throw new Error("Provide a nonempty array of tickets.")
  if (rows.length > 500) throw new Error("A batch can contain up to 500 tickets.")
  const ids = new Set<string>()
  return rows.map((row, index) => {
    if (!row || typeof row !== "object") throw new Error(`Row ${index + 1} must be a ticket object.`)
    const message = row.text ?? row.message
    if (typeof message !== "string" || !message.trim()) throw new Error(`Row ${index + 1} needs a message.`)
    if (message.length > 6000) throw new Error(`Row ${index + 1} exceeds 6,000 characters.`)
    const id = String(row.external_id || row.id || `UI-${crypto.randomUUID().slice(0, 12)}`)
    if (ids.has(id)) throw new Error("Each ticket must have a unique ID.")
    ids.add(id)
    const channel = row.channel || "app"
    if (!["app", "whatsapp", "call_note"].includes(channel)) throw new Error(`Row ${index + 1} has an unknown channel.`)
    return { external_id: id, text: message.trim(), channel, ...(row.received_at ? { received_at: row.received_at } : {}), customer_phone: row.customer_phone || null }
  })
}

export function validateEvaluation(data: unknown): EvaluationReport {
  if (!data || typeof data !== "object") throw new Error("Choose a JSON evaluation report.")
  const report = data as Record<string, unknown>
  if (typeof report.model !== "string" || !report.model.trim() || report.split !== "test" ||
      !Number.isInteger(report.sample_size) || Number(report.sample_size) < 1 ||
      typeof report.generated_at !== "string" || Number.isNaN(Date.parse(report.generated_at))) {
    throw new Error("A report needs model, split: test, a positive sample_size, and generated_at.")
  }
  for (const key of ["classification_accuracy", "extraction_accuracy"]) {
    if (typeof report[key] !== "number" || !Number.isFinite(report[key]) || report[key] < 0 || report[key] > 1) {
      throw new Error("Accuracy must be a number between 0 and 1.")
    }
  }
  if (!Array.isArray(report.confusion_cases) || !report.confusion_cases.every((item) => typeof item === "string")) {
    throw new Error("confusion_cases must be an array of text descriptions.")
  }
  return report as EvaluationReport
}
