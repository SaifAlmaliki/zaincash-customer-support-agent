// Same rules as backend/app/customers/phone.py. The server stays authoritative.
const ALLOWED = /^[0-9\s+\-().]*$/
const CANONICAL = /^07[3-9][0-9]{8}$/
const WITHOUT_ZERO = /^7[3-9][0-9]{8}$/

function asciiDigits(value: string) {
  // U+0660–U+0669 and U+06F0–U+06F9 end in the digit value.
  return value.replace(/[\u0660-\u0669\u06f0-\u06f9]/g, (digit) => String(digit.charCodeAt(0) & 0xf))
}

export function normalizeCustomerPhone(raw: string): string | null {
  const text = asciiDigits(raw).trim()
  if (!ALLOWED.test(text)) return null
  let digits = text.replace(/[^0-9]/g, "")
  if (digits.startsWith("00964")) digits = digits.slice(2)
  if (digits.startsWith("964")) digits = `0${digits.slice(3)}`
  else if (WITHOUT_ZERO.test(digits)) digits = `0${digits}`
  return CANONICAL.test(digits) ? digits : null
}

export function customerPath(phone: string) {
  return `/customers/${encodeURIComponent(phone)}`
}
