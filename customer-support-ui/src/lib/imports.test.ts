import { describe, expect, it } from "vitest"
import { parseTicketFile, validateEvaluation } from "./imports"

describe("ticket uploads", () => {
  it("reads quoted CSV fields, BOM, escaped quotes and Arabic without splitting messages", () => {
    const text =
      '\uFEFFexternal_id,text\r\nT-1,"حولت 50,000 دينار، وكتبت ""مستعجل"""\r\n'
    expect(parseTicketFile(text, "tickets.csv")[0]).toMatchObject({
      external_id: "T-1",
      text: 'حولت 50,000 دينار، وكتبت "مستعجل"',
      channel: "app",
    })
  })
  it("supports JSONL and message aliases", () => {
    expect(
      parseTicketFile('{"message":"مرحبا"}\n{"text":"سؤال"}\n', "tickets.jsonl")
    ).toHaveLength(2)
  })
  it("rejects conflicting IDs, empty messages and malformed containers", () => {
    expect(() =>
      parseTicketFile(
        '[{"id":"a","text":"one"},{"id":"a","text":"two"}]',
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
