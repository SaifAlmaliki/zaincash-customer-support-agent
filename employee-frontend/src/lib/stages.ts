import {
  ScanText,
  Tags,
  TextSearch,
  SearchCheck,
  GitBranch,
  SquarePen,
} from "lucide-react"

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
