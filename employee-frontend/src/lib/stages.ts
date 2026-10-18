import {
  ScanText,
  Tags,
  TextSearch,
  SearchCheck,
  GitBranch,
  SquarePen,
} from "lucide-react"
import type { Result } from "@/lib/types"

export const stages = [
  {
    id: "prepare",
    label: "Prepare",
    subtitle: "Clean the message",
    icon: ScanText,
    files: ["stage1_normalize/normalize.py", "stage1_normalize/candidates.py"],
    description:
      "Normalize Arabic digits, mask card numbers and find candidate details in the original message.",
  },
  {
    id: "classify",
    label: "Classify",
    subtitle: "Understand the issue",
    icon: Tags,
    files: [
      "stage2_classify/jev.py",
      "stage2_classify/gemini.py",
      "stage2_classify/cascade.py",
    ],
    description:
      "Jev categorizes the issue and estimates priority. Uncertain classifications get a Gemini second opinion, or a human escalation.",
  },
  {
    id: "extract",
    label: "Extract",
    subtitle: "Capture key details",
    icon: TextSearch,
    files: ["stage3_extract/extract.py", "stage1_normalize/dates.py"],
    description:
      "Verify transaction references, amounts, dates and phone numbers against source text. Unstated details remain empty.",
  },
  {
    id: "lookup",
    label: "Investigate",
    subtitle: "Check the transaction",
    icon: SearchCheck,
    files: ["stage4_lookup/lookup.py"],
    description:
      "Match extracted details to the mock transaction store. Missing, ambiguous and inconsistent matches need a person to investigate.",
  },
  {
    id: "decide",
    label: "Route",
    subtitle: "Find the right team",
    icon: GitBranch,
    files: ["stage5_decide/rules.py"],
    description:
      "Apply the category-to-team mapping and priority rules. Preserve every reason for escalation.",
  },
  {
    id: "draft",
    label: "Draft & review",
    subtitle: "Keep people in control",
    icon: SquarePen,
    files: ["stage6_draft/agent.py", "stage6_draft/tools.py", "stage6_draft/guardrails.py"],
    description:
      "When configured with indexed policies, the RAG agent investigates and prepares an Iraqi-Arabic draft with retained citations. Guardrails and credential checks flag issues for human review; disabled or unavailable drafting is recorded explicitly. Staff review and approve the final reply.",
  },
]

export const stageOutcomes: Record<
  string,
  { summary: string; statuses: { label: string; test: (row: Result) => boolean }[] }
> = {
  prepare: {
    summary:
      "The message is cleaned and card numbers are hidden before anyone decides the issue.",
    statuses: [{ label: "Message cleaned", test: () => true }],
  },
  classify: {
    summary:
      "The issue is named and given a priority. Uncertain tickets are marked for a person.",
    statuses: [
      {
        label: "Category decided",
        test: (row) => Boolean(row.category) && !usesSecondOpinion(row),
      },
      {
        label: "Second opinion used",
        test: (row) => Boolean(row.category) && usesSecondOpinion(row),
      },
      { label: "Not categorized", test: (row) => !row.category },
    ],
  },
  extract: {
    summary: "Only details the customer actually wrote are kept.",
    statuses: [
      { label: "Details captured", test: hasStatedDetail },
      { label: "Nothing stated in the message", test: (row) => !hasStatedDetail(row) },
    ],
  },
  lookup: {
    summary:
      "The transaction is checked against what the customer wrote.",
    statuses: [
      { label: "Transaction matched", test: (row) => row.lookup_status === "matched" },
      { label: "No matching transaction", test: (row) => row.lookup_status === "not_found" },
      {
        label: "More than one possible match",
        test: (row) => row.lookup_status === "ambiguous",
      },
      {
        label: "No transaction to check",
        test: (row) => row.lookup_status === "not_applicable",
      },
      {
        label: "Not checked yet",
        test: (row) =>
          !["matched", "not_found", "ambiguous", "not_applicable"].includes(
            row.lookup_status || ""
          ),
      },
    ],
  },
  decide: {
    summary:
      "The ticket is sent to a team, and every reason for a person to step in is kept.",
    statuses: [
      { label: "Held for a person", test: (row) => row.escalated },
      {
        label: "Assigned to a team",
        test: (row) => !row.escalated && Boolean(row.team),
      },
      { label: "Not routed yet", test: (row) => !row.escalated && !row.team },
    ],
  },
  draft: {
    summary:
      "A reply is prepared for a person to approve. Nothing is sent on its own.",
    statuses: [
      { label: "Waiting for review", test: (row) => row.status === "pending_review" },
      {
        label: "Approved by a person",
        test: (row) => row.status === "approved" || row.status === "edited",
      },
      { label: "Needs a closer look", test: (row) => row.status === "escalated" },
      { label: "Rejected", test: (row) => row.status === "rejected" },
    ],
  },
}

function usesSecondOpinion(row: Result) {
  return (row.classifier_path || "").includes("gemini")
}

function hasStatedDetail(row: Result) {
  return Object.values(row.extracted || {}).some(
    (field) => field?.value != null && field.value !== ""
  )
}

export function queueStepStatus(stageId: string, results: Result[]) {
  const outcome = stageOutcomes[stageId]
  if (!outcome) return []
  const counted = new Set<number>()
  const rows = outcome.statuses.map((status) => {
    const matches = results.filter((row) => status.test(row))
    matches.forEach((row) => counted.add(row.id))
    return { label: status.label, count: matches.length }
  })
  const other = results.filter((row) => !counted.has(row.id)).length
  if (other) rows.push({ label: "Still in progress", count: other })
  return rows
}
export const agentTools = [
  "lookup_transaction",
  "search_transactions",
  "get_customer_recent_transactions",
  "get_customer_ticket_history",
  "check_service_status",
  "search_knowledge_base",
  "flag_for_human",
  "submit_draft",
]
