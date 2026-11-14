import { expect, it } from "vitest"
import { concisePassage } from "./passage-reading"

const refund = [
  "Merchant refund — fictional demo policy",
  "Category: refund_request",
  "SYNTHETIC / FICTIONAL DEMO ONLY — مو سياسة حقيقية لزين كاش.",
  "إذا الزبون ألغى طلب من متجر أو خدمة ويريد فلوسه، راجع وصف الشراء ومرجع العملية والمبلغ بالسجل التجريبي إذا",
  "متوفر. إلغاء الطلب مو دليل إن الاسترجاع اكتمل. خليه يحتفظ بتأكيد الإلغاء غير السري للمراجعة الرسمية.",
  "وجّه الطلب لفريق Disputes. إذا العملية مو مطابقة أو تأكيد المتجر ناقص، وضّح شنو اللي يحتاج تدقيق بشري. لا",
  "تذكر مدة استرجاع أو مبلغ تعويض من عندك، ولا تدّعي إنك وافقت على الاسترجاع أو نفذته.",
].join("\n")

it("answers in two Arabic sentences and reads right to left", () => {
  const reading = concisePassage(refund)
  expect(reading.direction).toBe("rtl")
  expect(reading.lead).toBe(
    "إذا الزبون ألغى طلب من متجر أو خدمة ويريد فلوسه، راجع وصف الشراء ومرجع العملية والمبلغ بالسجل التجريبي إذا متوفر. إلغاء الطلب مو دليل إن الاسترجاع اكتمل.",
  )
  expect(reading.lead).not.toContain("SYNTHETIC")
  expect(reading.lead).not.toContain("Category")
  expect(reading.rest.startsWith("خليه يحتفظ")).toBe(true)
})
