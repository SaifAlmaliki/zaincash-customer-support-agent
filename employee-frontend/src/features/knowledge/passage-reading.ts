const ARABIC = /[\u0590-\u08FF]/

export type PassageReading = {
  lead: string
  rest: string
  direction: "rtl" | "ltr"
}

function directionOf(text: string): "rtl" | "ltr" {
  const arabic = text.match(/[\u0590-\u08FF]/g)?.length ?? 0
  const latin = text.match(/[A-Za-z]/g)?.length ?? 0
  return arabic > latin ? "rtl" : "ltr"
}

function keepLine(line: string, hasArabic: boolean) {
  const trimmed = line.trim()
  if (!trimmed) return false
  if (/^category\s*:/i.test(trimmed)) return false
  if (trimmed.includes("SYNTHETIC / FICTIONAL DEMO ONLY")) return false
  if (hasArabic && !ARABIC.test(trimmed)) return false
  return true
}

function sentences(text: string) {
  return (text.match(/[^.!?؟]+[.!?؟]+|[^.!?؟]+$/g) ?? [])
    .map((sentence) => sentence.trim())
    .filter(Boolean)
}

/** A short answer in the script's own direction, with the leftover policy text separate. */
export function concisePassage(text: string): PassageReading {
  const lines = text.split(/\r?\n/)
  const hasArabic = lines.some((line) => ARABIC.test(line))
  const body = lines
    .filter((line) => keepLine(line, hasArabic))
    .map((line) => line.trim())
    .join(" ")
    .replace(/\s+/g, " ")
    .trim()
  const parts = sentences(body)
  const lead = parts.slice(0, 2).join(" ")
  const rest = parts.slice(2).join(" ")
  const shown = lead || body
  return {
    lead: shown,
    rest: lead ? rest : "",
    direction: directionOf(shown || body),
  }
}
