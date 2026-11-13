import { describe, expect, it } from "vitest"
import { parseTicketFile, validateEvaluation } from "./imports"

describe("ticket uploads", () => {
  it("reads quoted CSV fields, BOM, escaped quotes and Arabic without splitting messages", () => {
    const text =
      '\uFEFFexternal_id,text,customer_phone\r\nT-1,"حولت 50,000 دينار، وكتبت ""مستعجل""",07701234567\r\n'
    expect(parseTicketFile(text, "tickets.csv")[0]).toMatchObject({
      external_id: "T-1",
      text: 'حولت 50,000 دينار، وكتبت "مستعجل"',
    })
  })
  it("supports JSONL and message aliases", () => {
    expect(
      parseTicketFile(
        '{"message":"مرحبا","customer_phone":"07701234567"}\n{"text":"سؤال","customer_phone":"07701234567"}\n',
        "tickets.jsonl"
      )
    ).toHaveLength(2)
  })
  it("requires and normalizes the customer phone", () => {
    expect(() => parseTicketFile('[{"text":"one"}]', "t.json")).toThrow(/Row 1 needs a valid customer phone/)
    expect(() => parseTicketFile('[{"text":"one","customer_phone":"0770"}]', "t.json")).toThrow(/Row 1/)
    expect(parseTicketFile('[{"text":"one","customer_phone":"+964 770 123 4567"}]', "t.json")[0].customer_phone).toBe("07701234567")
  })
  it("lists every row without a valid phone", () => {
    expect(() =>
      parseTicketFile('[{"text":"one"},{"text":"two","customer_phone":"0770"},{"text":"three","customer_phone":"07701234567"}]', "t.json")
    ).toThrow("Rows 1, 2 need a valid customer phone (07XXXXXXXXX).")
    expect(() =>
      parseTicketFile('[{"text":"one","customer_phone":"07701234567"},{"text":"two"}]', "t.json")
    ).toThrow("Row 2 needs a valid customer phone (07XXXXXXXXX).")
  })
  it("rejects conflicting IDs, empty messages and malformed containers", () => {
    expect(() =>
      parseTicketFile(
        '[{"id":"a","text":"one","customer_phone":"07701234567"},{"id":"a","text":"two","customer_phone":"07701234567"}]',
        "t.json"
      )
    ).toThrow(/unique/i)
    expect(() => parseTicketFile('[{"text":"  "}]', "t.json")).toThrow(
      /message/i
    )
    expect(() => parseTicketFile('{"hello":true}', "t.json")).toThrow(/array/i)
  })
})

describe("evaluation evidence", () => {
  it("requires a held-out split and finite fraction metrics", () => {
    const report = {
      model: "test-model",
      split: "test",
      sample_size: 100,
      generated_at: "2026-10-07",
      classification_accuracy: 0.87,
      extraction_accuracy: 0.91,
      confusion_cases: [],
    }
    expect(validateEvaluation(report).sample_size).toBe(100)
    expect(() =>
      validateEvaluation({ ...report, classification_accuracy: 91 })
    ).toThrow()
    expect(() => validateEvaluation({ ...report, split: "dev" })).toThrow()
  })
})
