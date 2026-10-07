# Pipeline stage map

Use this to jump from a step in the flow (README diagram / UI / a LangGraph node name) to the file that implements it, and to the tool involved.

## Flow → files

| Flow step (README) | LangGraph node | File(s) | Tool(s) / model |
|---|---|---|---|
| Clean the text (digits → 0-9, hide cards) | `prepare` | `stage1_normalize/normalize.py` | `normalize()`, `mask_cards()`, `fold_arabic()` |
| Find refs/phones/amounts/dates (regex) | `prepare` | `stage1_normalize/candidates.py` | `find_candidates()` — recall-tuned regex |
| Resolve relative dates | (used in extract) | `stage1_normalize/dates.py` | `resolve_date()` |
| Jev reads the ticket | `jev_classify` | `stage2_classify/jev.py` | Jev via langchain-typesafe: category, priority, flags, candidate picks (+ reversed-option check) |
| Gemini second opinion | `gemini_classify` | `stage2_classify/gemini.py` | Gemini structured output, 3 samples |
| Jev → Gemini → human decision | `gemini_classify` (cascade mode) | `stage2_classify/cascade.py` | `combine()` |
| Classify/Extract prompts | — | `stage2_classify/prompts/gemini_classify_v1.md`, `gemini_extract_v1.md` | prompt files (versioned) |
| Extract ref/amount/date/phone | `extract` | `stage3_extract/extract.py` | `finalize()`, `fill_gaps()`, span verification |
| Look up the transaction | `lookup` | `stage4_lookup/lookup.py` (+ `app/db/repository.py`) | `match_transaction()`, `lookup_transaction` tool |
| Route to team + red-flag check | `decide` | `stage5_decide/rules.py` | `decide()`, `merge_reasons()` |
| Draft the reply (Plan 3) | `draft` | `stage6_draft/agent.py`, `stage6_draft/drafting.py` | LangChain `create_agent` |
| Safety checks on the draft (Plan 3) | `draft` | `stage6_draft/guardrails.py` | Jev `requests_credentials` noul + regex |
| KB search (Plan 3) | `draft` (tool) | `stage6_draft/tools/search_knowledge_base.py` | `search_knowledge_base` |

## The 8 drafting tools (Plan 3) → `stage6_draft/tools/`

| Tool | File | What it does |
|---|---|---|
| `lookup_transaction` | `tools/lookup_transaction.py` | exact ref lookup |
| `search_transactions` | `tools/search_transactions.py` | fuzzy search when no ref |
| `get_customer_recent_transactions` | `tools/customer_transactions.py` | recent activity |
| `get_customer_ticket_history` | `tools/ticket_history.py` | repeat contacts |
| `check_service_status` | `tools/service_status.py` | known outages |
| `search_knowledge_base` | `tools/search_knowledge_base.py` | pgvector policy chunks |
| `flag_for_human` | `tools/flag_for_human.py` | record an escalation reason |
| `submit_draft` | `tools/submit_draft.py` | record the draft (terminal) |

## Orchestration and wiring (not a stage)

| What | File |
|---|---|
| Build the graph, run a batch, summarize | `pipeline/graph.py` |
| LangGraph state | `pipeline/state.py` |
| Shared dataclasses | `pipeline/contracts.py` |
| Wire real clients (Jev/Gemini) | `pipeline/factory.py` |
| Outcome → dict/DB row | `pipeline/io/serialize.py` |
