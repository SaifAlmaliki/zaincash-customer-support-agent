import { renderToStaticMarkup } from "react-dom/server"
import { expect, it } from "vitest"
import { resultFixture } from "@/lib/test-fixtures"
import { CustomerMessage } from "./SourceEvidence"

it("shows the original customer message on the review page", () => {
  const result = resultFixture(5, {}, { text: "بعد التحديث التطبيق يطفي اول ما افتحه" })
  const html = renderToStaticMarkup(<CustomerMessage result={result} />)
  expect(html).toContain("رسالة الزبون الأصلية")
  expect(html).toContain("بعد التحديث التطبيق يطفي اول ما افتحه")
})

it("omits the card when the ticket text is blank", () => {
  const html = renderToStaticMarkup(<CustomerMessage result={resultFixture(5, {}, { text: "  " })} />)
  expect(html).toBe("")
})
