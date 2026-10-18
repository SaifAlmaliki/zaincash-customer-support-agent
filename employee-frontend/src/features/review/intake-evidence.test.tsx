import { renderToStaticMarkup } from "react-dom/server"
import { expect, it } from "vitest"
import type { IntakeEvidenceData } from "@/lib/types"
import { IntakeEvidence } from "./IntakeEvidence"

const intakeFixture: IntakeEvidenceData = {
  summary_ar: "فشل تحويل بمبلغ غير معروف.",
  quality: "partial_context",
  facts: {
    amount: { key: "amount", status: "unknown", value: null, normalized: null },
    txn_ref: { key: "txn_ref", status: "known", value: "ZC-123 مرحبا DEMO-2410000123", normalized: "DEMO-2410000123" },
  },
  additional_issues: [],
  unknown_keys: ["amount"],
  messages: [
    { id: "m1", role: "user", text: "The transfer failed yesterday", language: "en" },
    { id: "m2", role: "user", text: "<script>alert(1)</script>", language: "en" },
  ],
  attachments: [
    {
      id: "a1",
      filename: "receipt.png",
      download_url: "/api/results/1/intake/attachments/a1",
    },
  ],
  submitted_at: "2026-10-18T09:00:00Z",
}

it("shows unknowns and original transcript alongside Arabic summary", () => {
  const html = renderToStaticMarkup(<IntakeEvidence intake={intakeFixture} />)
  expect(html).toContain("ملخص المشكلة")
  expect(html).toContain("Unknown")
  expect(html).toContain("The transfer failed yesterday")
  expect(html).toContain("/api/results/1/intake/attachments/")
  expect(html).not.toContain("Bearer")
  expect(html).toContain("DEMO-2410000123")
  expect(html).not.toContain("<script>")
  expect(html).toContain("&lt;script&gt;")
})

it("has no intake panel for historical tickets", () => {
  expect(renderToStaticMarkup(<IntakeEvidence intake={null} />)).toBe("")
})
