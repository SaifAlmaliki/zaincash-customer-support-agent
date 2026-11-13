import { expect, it } from "vitest"
import { normalizeCustomerPhone } from "./phone"

it.each([
  "07701234567", "0770 123 4567", "0770-123-4567", "(0770) 123-4567", "+9647701234567",
  "+964 770 123 4567", "9647701234567", "00964 770 123 4567", "7701234567",
  "٠٧٧٠١٢٣٤٥٦٧", "+۹۶۴\u00a0۷۷۰-۱۲۳ ۴۵۶۷", "  07701234567  ",
])("accepts %s", (raw) => {
  expect(normalizeCustomerPhone(raw)).toBe("07701234567")
})

it.each([
  "", "0770123456", "077012345678", "07201234567", "96407701234567", "07701234567x",
  "0770123456\uff11", "0770123456\u0967", "0770/123/4567",
])("rejects %s", (raw) => {
  expect(normalizeCustomerPhone(raw)).toBeNull()
})
