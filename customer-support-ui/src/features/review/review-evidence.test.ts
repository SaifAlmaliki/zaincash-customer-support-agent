import { expect, it } from "vitest"
import { reviewEvidence } from "./review-evidence"

const source = { id: "7:0", document_id: 7, chunk_index: 0, filename: "deleted-policy.md", text: "دليل محفوظ", score: 0.72, page_start: null, page_end: null }

it("uses cited result snapshots in citation order, independently of raw trace or deleted documents", () => {
  const evidence = reviewEvidence({ citations: ["missing", "7:0", "7:0"], citation_sources: [source, { ...source, id: "uncited" }], agent_trace: [{ kind: "draft", citation_sources: [{ ...source, text: "wrong raw text" }] }] })
  expect(evidence.sources).toEqual([source])
  expect(evidence.missingIds).toEqual(["missing"])
})

it("counts only tool events and preserves the other trace kinds separately", () => {
  const evidence = reviewEvidence({ citations: [], agent_trace: [{ kind: "stage" }, { kind: "tool", tool: "search_knowledge_base" }, { kind: "guardrail" }, { kind: "model" }, { kind: "skipped" }, { kind: "draft" }, { tool: "legacy_unknown" }] })
  expect(evidence.tools).toEqual([{ kind: "tool", tool: "search_knowledge_base" }])
  expect(evidence.otherEvents).toHaveLength(5)
})

it("keeps legacy citations explicitly unresolved instead of reconstructing evidence from trace", () => {
  const evidence = reviewEvidence({ citations: ["7:0"], agent_trace: [{ kind: "tool", retrieved_passages: [source] }] })
  expect(evidence.sources).toEqual([])
  expect(evidence.missingIds).toEqual(["7:0"])
})
