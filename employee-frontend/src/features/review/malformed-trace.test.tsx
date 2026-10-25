import { renderToStaticMarkup } from "react-dom/server"
import { expect, it } from "vitest"
import type { Result } from "@/lib/types"
import { CitationEvidence } from "./CitationEvidence"
import { PipelineTrace } from "./PipelineTrace"
import { reviewEvidence } from "./review-evidence"

const source = { id: "p1", document_id: 1, chunk_index: 0, filename: "saved.md", text: "دليل محفوظ", score: 0.9, page_start: null, page_end: null }

it.each([null, {}, [null], [null, 42, "bad", [], { kind: "tool", tool: "search_knowledge_base" }, { kind: "stage", node: "decide", elapsed_ms: 5 }]].map((raw) => ({ raw })))(
  "renders historical malformed traces without losing citations or raw audit data: $raw", ({ raw }) => {
    const result = { citations: ["p1"], citation_sources: [source], agent_trace: raw } as Result
    const before = JSON.stringify(raw)
    const evidence = reviewEvidence(result)
    expect(evidence.sources).toEqual([source])
    expect(evidence.tools.length).toBe(Array.isArray(raw) && raw.length > 1 ? 1 : 0)
    expect(renderToStaticMarkup(<CitationEvidence result={result} />)).toContain("دليل محفوظ")
    const trace = renderToStaticMarkup(<PipelineTrace result={result} />)
    expect(trace).toContain("أثر المعالجة والأدوات")
    if (Array.isArray(raw) && raw.length > 1) {
      expect(trace).toContain("بحث في قاعدة المعرفة")
      expect(trace).toContain("اكتمل")
      expect(trace).not.toContain(".py")
    }
    expect(result.agent_trace).toBe(raw)
    expect(JSON.stringify(raw)).toBe(before)
  }
)
