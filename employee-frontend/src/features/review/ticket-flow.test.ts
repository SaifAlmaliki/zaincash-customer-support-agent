import { expect, it } from "vitest"
import { channelName, checkLines, fieldLabel, isArabicMessage, lookupSentence, sentence, toolLine } from "./ticket-flow-copy"

it("treats Arabic letters as an Arabic message and a blank message as English", () => {
  expect(isArabicMessage("التحويل لم يصل")).toBe(true)
  expect(isArabicMessage("The transfer failed")).toBe(false)
  expect(isArabicMessage("   ")).toBe(false)
})

it("returns the English skip reasons verbatim and the Arabic reasons for the same ids", () => {
  expect(sentence("messageHadText", false)).toBe("The message had text.")
  expect(sentence("askedGeminiDirectly", false)).toBe("This run asked Gemini directly.")
  expect(sentence("jevWasSure", false)).toBe("Jev was already sure.")
  expect(sentence("emptyEnded", false)).toBe("The empty message ended the path.")
  expect(sentence("runStopped", false)).toBe("The run stopped.")
  expect(sentence("chartFailed", false)).toBe("The chart could not be drawn.")
  expect(sentence("messageHadText", true)).toBe("الرسالة تحتوي على نص.")
  expect(sentence("runStopped", true)).toBe("توقف التشغيل.")
})

it("names channels and fields in the selected language", () => {
  expect(channelName("whatsapp", false)).toBe("WhatsApp")
  expect(channelName("whatsapp", true)).toBe("واتساب")
  expect(fieldLabel("txn_ref", false)).toBe("Transaction reference")
  expect(fieldLabel("txn_ref", true)).toBe("الرقم المرجعي")
})

it("fills a sentence template and describes a lookup", () => {
  expect(sentence("prepareReceived", false, { channel: "WhatsApp", length: "180" })).toBe(
    "Read the WhatsApp message (180 characters).",
  )
  expect(lookupSentence("matched", false)).toBe("One transaction matched.")
  expect(lookupSentence("matched", true)).toBe("تطابق تحويل واحد.")
  expect(lookupSentence(null, false)).toBe("Lookup was not recorded.")
})

it("keeps only safe tool details and states credential checks without secrets", () => {
  expect(toolLine({ tool: "lookup_transaction", status: "ok", arguments: { txn_ref: "ZC-1044", pin: "1234" } }, false)).toBe(
    "Looked up a transaction reference: ZC-1044. Completed.",
  )
  expect(toolLine({ tool: "lookup_transaction", status: "ok", arguments: { txn_ref: "ZC-1044", pin: "1234" } }, false)).not.toContain("1234")
  expect(checkLines([{ kind: "guardrail", status: "passed", findings: [], credential_check_degraded: true }], false)).toEqual([
    "The credential check was unavailable.",
  ])
  expect(checkLines([{ kind: "guardrail", status: "passed", findings: [] }], false)).toEqual([
    "The credential check passed.",
    "No safety-check findings were recorded.",
  ])
})
