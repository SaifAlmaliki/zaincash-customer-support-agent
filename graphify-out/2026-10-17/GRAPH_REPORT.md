# Graph Report - zaincash-support  (2026-10-17)

## Corpus Check
- 131 files · ~58,026 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 12 file(s) not represented in the graph (top: (none) 5, .jsonl 3, .css 2)

## Summary
- 1020 nodes · 3013 edges · 57 communities (42 shown, 15 thin omitted)
- Extraction: 93% EXTRACTED · 7% INFERRED · 0% AMBIGUOUS · INFERRED: 221 edges (avg confidence: 0.93)
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- Classification and Extraction
- Ticket Ingest
- Pipeline Wiring and Fixtures
- Settings and Gemini Client
- Form Controls and Preview
- Shared UI States
- Results and Review API
- Workspace Cards and Badges
- SQL Persistence
- Drafting and Graph Factory
- Transaction Lookup
- App and Database Bootstrap
- Dialogs and Pipeline Strip
- UI Package Metadata
- Routing and Escalation
- Support Taxonomy Categories
- shadcn Component Config
- Workspace Routes
- App TypeScript Config
- Support CLI
- Knowledge Documents API
- Node TypeScript Config
- Pipeline Graph Nodes
- UI Dev Dependencies
- Pipeline Contracts
- Taxonomy Helpers
- UI Runtime Dependencies
- Theme Provider
- Batch Runner
- Classify and Extract Prompts
- Select Component
- Pipeline Design Spec
- Workspace Plan Concepts
- Drafting Plan Concepts
- Runs API
- Null Drafter Boundaries
- UI npm Scripts
- Pipeline Spec Rules
- Health and Insights Routes
- Vite Logo
- ZainCash Mark
- Root TypeScript Config
- Vite Config
- Human Review Gate
- React Logo
- Human Flag Tool
- Recent Transactions Tool
- Ticket History Tool
- Lookup Transaction Tool
- Search Transactions Tool
- Submit Draft Tool
- Project Root

## God Nodes (most connected - your core abstractions)
1. `make_output()` - 33 edges
2. `Settings` - 30 edges
3. `PipelineState` - 30 edges
4. `QueuePage()` - 30 edges
5. `Button()` - 28 edges
6. `make_ticket()` - 26 edges
7. `FieldPick` - 24 edges
8. `NormalizedTicket` - 23 edges
9. `build_pipeline()` - 23 edges
10. `react` - 22 edges

## Surprising Connections (you probably didn't know these)
- `Red-Flag Escalation` --semantically_similar_to--> `Routing and Escalation Rules`  [INFERRED] [semantically similar]
  README.md → docs/superpowers/plans/2026-10-07-plan1-core-pipeline-part2.md
- `OpenRouter Provider Migration` --semantically_similar_to--> `OpenRouter`  [INFERRED] [semantically similar]
  docs/superpowers/specs/2026-10-07-support-pipeline-design.md → README.md
- `Cascade Mode` --semantically_similar_to--> `Cascade Classifier`  [INFERRED] [semantically similar]
  README.md → docs/superpowers/specs/2026-10-07-support-pipeline-design.md
- `No Send Path` --semantically_similar_to--> `Human Approval Gate`  [INFERRED] [semantically similar]
  docs/superpowers/specs/2026-10-07-support-pipeline-design.md → README.md
- `NullDrafter` --semantically_similar_to--> `NullDrafter`  [INFERRED] [semantically similar]
  docs/superpowers/plans/2026-10-07-plan1-core-pipeline-part3.md → README.md

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **Ticket Processing Stage Flow** — backend_app_pipeline_runner_prepare, backend_app_pipeline_runner_jev_classify, backend_app_pipeline_runner_gemini_classify, backend_app_pipeline_runner_extract, backend_app_pipeline_runner_lookup, backend_app_pipeline_runner_decide, backend_app_pipeline_runner_draft [EXTRACTED 1.00]
- **Cascade Classification Path** — docs_superpowers_specs_2026_10_07_support_pipeline_design_cascade, docs_superpowers_plans_2026_10_07_plan1_core_pipeline_part2_jev_classifier, docs_superpowers_plans_2026_10_07_plan1_core_pipeline_part2_gemini_classifier, docs_superpowers_plans_2026_10_07_plan1_core_pipeline_part2_cascade_combine, readme_human_approval [EXTRACTED 1.00]
- **Drafting Agent Toolset** — backend_app_pipeline_runner_lookup_transaction, backend_app_pipeline_runner_search_transactions, backend_app_pipeline_runner_get_customer_recent_transactions, backend_app_pipeline_runner_get_customer_ticket_history, backend_app_pipeline_runner_check_service_status, backend_app_pipeline_runner_search_knowledge_base, backend_app_pipeline_runner_flag_for_human, backend_app_pipeline_runner_submit_draft [EXTRACTED 1.00]
- **Vite Logo Mark** — customer_support_ui_public_vite_vite_logo, customer_support_ui_public_vite_v_mark, customer_support_ui_public_vite_lightning_bolt [INFERRED 0.95]
- **ZainCash Mark Composition** — customer_support_ui_public_zaincash_mark_logo, customer_support_ui_public_zaincash_mark_crimson_square, customer_support_ui_public_zaincash_mark_stacked_bars [EXTRACTED 1.00]
- **React Brand Mark** — customer_support_ui_src_assets_react_logo, customer_support_ui_src_assets_react_atom, customer_support_ui_src_assets_react_brand [INFERRED 0.95]

## Communities (57 total, 15 thin omitted)

### Community 0 - "Classification and Extraction"
Cohesion: 0.06
Nodes (57): LLMUnavailable, StructuredLLM, Candidates, ClassificationResult, ClassifierOutput, FieldPick, NormalizedTicket, Classifier (+49 more)

### Community 1 - "Ticket Ingest"
Cohesion: 0.06
Nodes (47): TicketInput, load_jsonl(), load_tickets(), _rows(), Candidate, _add(), find_candidates(), normalize_phone() (+39 more)

### Community 2 - "Pipeline Wiring and Fixtures"
Cohesion: 0.07
Nodes (41): build_graph(), PipelineDeps, InMemoryTransactionRepo, load_taxonomy(), tax(), FakeClassifier, FakeJevRunnable, make_output() (+33 more)

### Community 3 - "Settings and Gemini Client"
Cohesion: 0.06
Nodes (27): Settings, GeminiStructuredLLM, Sample, build_pipeline(), ConfigError, make_gemini_llm(), make_jev_client(), model_ids() (+19 more)

### Community 4 - "Form Controls and Preview"
Cohesion: 0.08
Nodes (39): Input(), Tabs(), TabsContent(), TabsList(), tabsListVariants, TabsTrigger(), Textarea(), examples (+31 more)

### Community 5 - "Shared UI States"
Cohesion: 0.19
Nodes (33): EmptyState(), ErrorState(), LoadingState(), PageHeader(), PriorityBadge(), StatusBadge(), Table(), TableBody() (+25 more)

### Community 6 - "Results and Review API"
Cohesion: 0.14
Nodes (14): get_session(), get_result(), list_results(), review_result(), BatchInput, ReviewInput, ReviewRow, TicketResultRow (+6 more)

### Community 7 - "Workspace Cards and Badges"
Cohesion: 0.18
Nodes (20): Confidence(), Metric(), statusLabels, Badge(), badgeVariants, Card(), CardContent(), CardHeader() (+12 more)

### Community 8 - "SQL Persistence"
Cohesion: 0.16
Nodes (18): IncidentRow, RunRow, TransactionRow, create_run(), finish_run(), load_incidents(), load_transactions(), SqlTransactionRepo (+10 more)

### Community 9 - "Drafting and Graph Factory"
Cohesion: 0.12
Nodes (7): DraftResult, _default_retry(), _percentile(), _retryable(), Drafter, NullDrafter, draft()

### Community 10 - "Transaction Lookup"
Cohesion: 0.16
Nodes (17): TxnRecord, _as_date(), _iqd_amount(), match_transaction(), parse_dt(), TransactionRepo, txn_from_dict(), _ex() (+9 more)

### Community 11 - "App and Database Bootstrap"
Cohesion: 0.16
Nodes (9): Base, init_db(), make_engine(), make_sessionmaker(), reset_db(), upgrade_workspace_schema(), create_app(), lifespan() (+1 more)

### Community 12 - "Dialogs and Pipeline Strip"
Cohesion: 0.17
Nodes (14): PipelineStrip(), ConfirmDialog(), Button(), buttonVariants, Dialog(), DialogContent(), DialogDescription(), DialogFooter() (+6 more)

### Community 13 - "UI Package Metadata"
Cohesion: 0.11
Nodes (21): name, private, type, version, eslint, @eslint/js, eslint-plugin-react-hooks, eslint-plugin-react-refresh (+13 more)

### Community 14 - "Routing and Escalation"
Cohesion: 0.22
Nodes (17): Decision, LookupResult, decide(), empty_ticket_decision(), merge_reasons(), note_for(), _unique(), Category (+9 more)

### Community 15 - "Support Taxonomy Categories"
Cohesion: 0.22
Nodes (21): lookup, Account KYC, Account & Security, Agent Dispute, Agent Network, App Bug, Bill Payment, Card Issue (+13 more)

### Community 16 - "shadcn Component Config"
Cohesion: 0.09
Nodes (21): aliases, components, hooks, lib, ui, utils, iconLibrary, menuAccent (+13 more)

### Community 17 - "Workspace Routes"
Cohesion: 0.18
Nodes (16): App(), EvaluationPage, InsightsPage, KnowledgePage, NewBatchPage, QueuePage, RunDetailPage, RunsPage (+8 more)

### Community 18 - "App TypeScript Config"
Cohesion: 0.09
Nodes (21): compilerOptions, allowArbitraryExtensions, allowImportingTsExtensions, erasableSyntaxOnly, jsx, lib, module, moduleDetection (+13 more)

### Community 19 - "Support CLI"
Cohesion: 0.21
Nodes (9): init_db_cmd(), Mode, run_batch_cmd(), _run_in_memory(), _run_with_db(), seed_db_cmd(), _sessionmaker(), get_settings() (+1 more)

### Community 20 - "Knowledge Documents API"
Cohesion: 0.20
Nodes (6): delete_document(), document_view(), download_document(), list_documents(), upload_document(), UploadedDocument

### Community 21 - "Node TypeScript Config"
Cohesion: 0.12
Nodes (16): compilerOptions, allowImportingTsExtensions, erasableSyntaxOnly, lib, module, moduleDetection, noEmit, noFallthroughCasesInSwitch (+8 more)

### Community 23 - "UI Dev Dependencies"
Cohesion: 0.12
Nodes (16): devDependencies, eslint, @eslint/js, eslint-plugin-react-hooks, eslint-plugin-react-refresh, globals, prettier, prettier-plugin-tailwindcss (+8 more)

### Community 24 - "Pipeline Contracts"
Cohesion: 0.31
Nodes (5): ExtractedField, outcome_to_dict(), outcome_to_row(), test_failed_outcome_and_dict_form(), test_full_outcome_is_json_safe()

### Community 25 - "Taxonomy Helpers"
Cohesion: 0.24
Nodes (5): most_urgent(), priority_rank(), TaxonomyError, test_priority_helpers(), test_rejects_unknown_team()

### Community 26 - "UI Runtime Dependencies"
Cohesion: 0.15
Nodes (13): dependencies, @base-ui/react, class-variance-authority, cn, @fontsource-variable/geist, lucide-react, react, react-dom (+5 more)

### Community 27 - "Theme Provider"
Cohesion: 0.21
Nodes (11): disableTransitionsTemporarily(), getSystemTheme(), isEditableTarget(), isTheme(), ResolvedTheme, Theme, THEME_VALUES, ThemeProvider() (+3 more)

### Community 28 - "Batch Runner"
Cohesion: 0.42
Nodes (9): save_outcomes(), TicketOutcome, outcome_from_state(), run_batch(), RunSummary, summarize(), process_batch(), process() (+1 more)

### Community 29 - "Classify and Extract Prompts"
Cohesion: 0.31
Nodes (8): extract, gemini_classify, jev_classify, prepare, Gemini Classify Prompt v1, Gemini Extract Prompt v1, GeminiClassifier, JevClassifier

### Community 30 - "Select Component"
Cohesion: 0.27
Nodes (7): FilterSelect(), SelectContent(), SelectItem(), SelectScrollDownButton(), SelectScrollUpButton(), SelectTrigger(), SelectValue()

### Community 31 - "Pipeline Design Spec"
Cohesion: 0.25
Nodes (7): pgvector Postgres Service, pgdata Volume, Support Pipeline Design, Gemini 3.8 Flash, Jev, OpenRouter, ZainCash Support Pipeline

### Community 32 - "Workspace Plan Concepts"
Cohesion: 0.24
Nodes (8): Pipeline Graph Orchestration, Support Workspace HTML Shell, Support Workspace, Batch Runner, support CLI, Live Batch API, Support Workspace UI Plan, Plan 1 Live Smoke

### Community 33 - "Drafting Plan Concepts"
Cohesion: 0.25
Nodes (7): check_service_status, decide, draft, Plan 1 Part 2, Plan 1 Core Pipeline, Five-Plan Roadmap, Weekly Pattern Report

### Community 34 - "Runs API"
Cohesion: 0.29
Nodes (3): get_run(), list_runs(), start_run()

### Community 35 - "Null Drafter Boundaries"
Cohesion: 0.25
Nodes (4): search_knowledge_base, Workspace NullDrafter Boundary, NullDrafter, NullDrafter

### Community 36 - "UI npm Scripts"
Cohesion: 0.25
Nodes (8): scripts, build, dev, format, lint, preview, test, typecheck

### Community 38 - "Health and Insights Routes"
Cohesion: 0.53
Nodes (3): health(), insights(), workspace()

### Community 39 - "Vite Logo"
Cohesion: 0.40
Nodes (5): Iconify Logos, Yellow-to-Orange Lightning Bolt, Cyan-to-Purple V Mark, Vite, Vite Logo

### Community 40 - "ZainCash Mark"
Cohesion: 0.50
Nodes (5): Stacked Cash or Cards Motif, Crimson Rounded Square (#da3345), ZainCash Mark, Three Tilted White Rounded Bars, ZainCash

### Community 41 - "Root TypeScript Config"
Cohesion: 0.40
Nodes (4): compilerOptions, paths, files, references

### Community 42 - "Vite Config"
Cohesion: 0.40
Nodes (3): @tailwindcss/vite, vite, @vitejs/plugin-react

### Community 44 - "React Logo"
Cohesion: 0.67
Nodes (4): React Atom Mark, React, Iconify Logos, React Logo

## Ambiguous Edges - Review These
- `Plan 1 Live Smoke` → `Fraud Report`  [AMBIGUOUS]
  README.md · relation: conceptually_related_to
- `Three Tilted White Rounded Bars` → `Stacked Cash or Cards Motif`  [AMBIGUOUS]
  customer-support-ui/public/zaincash-mark.svg · relation: conceptually_related_to

## Knowledge Gaps
- **31 isolated node(s):** `zaincash-support`, `@fontsource-variable/geist`, `shadcn`, `tailwindcss`, `tw-animate-css` (+26 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 293 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **15 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `react` connect `Form Controls and Preview` to `Shared UI States`, `Workspace Cards and Badges`, `Dialogs and Pipeline Strip`, `UI Package Metadata`, `Workspace Routes`, `Theme Provider`, `Select Component`?**
  _High betweenness centrality (0.018) - this node is a cross-community bridge._
- **Are the 11 inferred relationships involving `Settings` (e.g. with `_run_in_memory()` and `_run_with_db()`) actually correct?**
  _`Settings` has 11 INFERRED edges - model-reasoned connections that need verification._
- **What connects `zaincash-support`, `@fontsource-variable/geist`, `shadcn` to the rest of the system?**
  _31 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Classification and Extraction` be split into smaller, more focused modules?**
  _Cohesion score 0.061009817671809255 - nodes in this community are weakly interconnected._
- **Why does `Settings` connect `Settings and Gemini Client` to `Pipeline Wiring and Fixtures`, `SQL Persistence`, `Drafting and Graph Factory`, `App and Database Bootstrap`, `Support CLI`?**
  _High betweenness centrality (0.018) - this node is a cross-community bridge._

### Low-confidence Hints
_AMBIGUOUS edges — the extractor was unsure. Verify before acting on these._

- **What is the exact relationship between `Plan 1 Live Smoke` and `Fraud Report`?**
  _Edge tagged AMBIGUOUS (relation: conceptually_related_to) - confidence is low._
- **What is the exact relationship between `Three Tilted White Rounded Bars` and `Stacked Cash or Cards Motif`?**
  _Edge tagged AMBIGUOUS (relation: conceptually_related_to) - confidence is low._