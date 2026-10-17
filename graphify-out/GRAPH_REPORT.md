# Graph Report - zaincash-support  (2026-10-17)

## Corpus Check
- 149 files · ~86,399 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 12 file(s) not represented in the graph (top: (none) 5, .jsonl 3, .css 2)

## Summary
- 1620 nodes · 5143 edges · 79 communities (62 shown, 17 thin omitted)
- Extraction: 89% EXTRACTED · 11% INFERRED · 0% AMBIGUOUS · INFERRED: 543 edges (avg confidence: 0.92)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `276aaa72`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- jev.py
- Ticket Ingest
- taxonomy.py
- Settings and Gemini Client
- Form Controls and Preview
- Shared UI States
- Results and Review API
- Workspace Cards and Badges
- SQL Persistence
- DraftResult
- Transaction Lookup
- App and Database Bootstrap
- Dialogs and Pipeline Strip
- UI Package Metadata
- make_ticket
- Support Taxonomy Categories
- shadcn Component Config
- Workspace Routes
- App TypeScript Config
- Support CLI
- UploadedDocument
- Node TypeScript Config
- Pipeline Graph Nodes
- UI Dev Dependencies
- pipeline/contracts.py
- test_rag_drafter.py
- UI Runtime Dependencies
- Theme Provider
- test_embeddings.py
- Classify and Extract Prompts
- FakeJevRunnable
- Pipeline Design Spec
- Workspace Plan Concepts
- Drafting Plan Concepts
- test_kb_service.py
- Null Drafter Boundaries
- UI npm Scripts
- Pipeline Spec Rules
- test_draft_tools.py
- Vite Logo
- ZainCash Mark
- Root TypeScript Config
- Vite Config
- Human Review Gate
- React Logo
- KnowledgeService
- service.py
- Human Flag Tool
- Recent Transactions Tool
- Ticket History Tool
- Lookup Transaction Tool
- Search Transactions Tool
- Submit Draft Tool
- Project Root
- parse_document
- tools.py
- agent.py
- SqlInvestigationRepo
- NewBatchPage.tsx
- gemini.py
- extract.py
- _DatabaseCall
- LLMUnavailable
- factory.py
- Plan 3 — Knowledge retrieval and grounded reply drafting
- ingest.py
- KnowledgeDocumentIndex
- Plan 3 RAG Drafting Implementation Plan
- SqlTransactionRepo
- KnowledgePage.tsx
- graph.py
- test_db_deadline_cancelled_publication_cannot_commit_late
- test_dbapi_commit_handoff_arbitrates_cancellation
- CredentialChecker
- DraftSubmission

## God Nodes (most connected - your core abstractions)
1. `KnowledgeService` - 71 edges
2. `Settings` - 58 edges
3. `PipelineState` - 48 edges
4. `make_ticket()` - 42 edges
5. `build_pipeline()` - 41 edges
6. `draft_state()` - 40 edges
7. `make_output()` - 38 edges
8. `drafter()` - 33 edges
9. `EmbeddingError` - 32 edges
10. `parse_document()` - 30 edges

## Surprising Connections (you probably didn't know these)
- `Task 6: API/CLI indexing and persisted citation projection` --references--> `KnowledgeService`  [INFERRED]
  docs/superpowers/plans/2026-10-17-plan3-rag-drafting.md → backend/app/kb/service.py
- `Pipeline and CLI` --references--> `NullDrafter`  [INFERRED]
  docs/superpowers/specs/2026-10-17-plan3-rag-drafting-design.md → backend/app/pipeline/stage6_draft/drafting.py
- `7. Draft guardrails and failure outcomes` --references--> `requests_credentials()`  [INFERRED]
  docs/superpowers/specs/2026-10-17-plan3-rag-drafting-design.md → backend/app/pipeline/stage6_draft/guardrails.py
- `Task 8: Demo corpus, full verification and readiness record` --references--> `support_test()`  [INFERRED]
  docs/superpowers/plans/2026-10-17-plan3-rag-drafting.md → backend/tests/test_kb_service.py
- `2. Current implementation and integration points` --references--> `UploadedDocument`  [INFERRED]
  docs/superpowers/specs/2026-10-17-plan3-rag-drafting-design.md → backend/app/db/document_models.py

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **Cascade Classification Path** — docs_superpowers_specs_2026_10_07_support_pipeline_design_cascade, docs_superpowers_plans_2026_10_07_plan1_core_pipeline_part2_jev_classifier, docs_superpowers_plans_2026_10_07_plan1_core_pipeline_part2_gemini_classifier, docs_superpowers_plans_2026_10_07_plan1_core_pipeline_part2_cascade_combine, readme_human_approval [EXTRACTED 1.00]
- **ZainCash Mark Composition** — customer_support_ui_public_zaincash_mark_logo, customer_support_ui_public_zaincash_mark_crimson_square, customer_support_ui_public_zaincash_mark_stacked_bars [EXTRACTED 1.00]
- **Drafting Agent Toolset** — backend_app_pipeline_runner_lookup_transaction, backend_app_pipeline_runner_search_transactions, backend_app_pipeline_runner_get_customer_recent_transactions, backend_app_pipeline_runner_get_customer_ticket_history, backend_app_pipeline_runner_check_service_status, backend_app_pipeline_runner_search_knowledge_base, backend_app_pipeline_runner_flag_for_human, backend_app_pipeline_runner_submit_draft [EXTRACTED 1.00]
- **Ticket Processing Stage Flow** — backend_app_pipeline_runner_prepare, backend_app_pipeline_runner_jev_classify, backend_app_pipeline_runner_gemini_classify, backend_app_pipeline_runner_extract, backend_app_pipeline_runner_lookup, backend_app_pipeline_runner_decide, backend_app_pipeline_runner_draft [EXTRACTED 1.00]
- **Vite Logo Mark** — customer_support_ui_public_vite_vite_logo, customer_support_ui_public_vite_v_mark, customer_support_ui_public_vite_lightning_bolt [INFERRED 0.95]
- **React Brand Mark** — customer_support_ui_src_assets_react_logo, customer_support_ui_src_assets_react_atom, customer_support_ui_src_assets_react_brand [INFERRED 0.95]

## Communities (79 total, 17 thin omitted)

### Community 0 - "jev.py"
Cohesion: 0.22
Nodes (10): ClassificationResult, build_order_check(), build_questions(), build_state(), category_criteria(), _input_tokens(), JevClassifier, _picks() (+2 more)

### Community 1 - "Ticket Ingest"
Cohesion: 0.05
Nodes (60): TicketInput, Passage, Candidate, _add(), find_candidates(), normalize_phone(), _overlaps(), parse_amount() (+52 more)

### Community 2 - "taxonomy.py"
Cohesion: 0.10
Nodes (14): build_graph(), PipelineDeps, InMemoryTransactionRepo, load_taxonomy(), most_urgent(), priority_rank(), TaxonomyError, tax() (+6 more)

### Community 3 - "Settings and Gemini Client"
Cohesion: 0.07
Nodes (17): Settings, GeminiStructuredLLM, test_defaults(), test_drafting_configuration_cannot_bypass_hard_limits(), test_drafting_limits_load_from_environment(), test_env_overrides(), test_legacy_gemini_model_names_are_qualified_for_openrouter(), test_openrouter_key_is_loaded_from_environment() (+9 more)

### Community 4 - "Form Controls and Preview"
Cohesion: 0.11
Nodes (23): examples, previewResults, previewRuns, Resource, request(), EvaluationReport, ExtractedField, Health (+15 more)

### Community 5 - "Shared UI States"
Cohesion: 0.23
Nodes (26): EmptyState(), ErrorState(), LoadingState(), Metric(), PageHeader(), PriorityBadge(), StatusBadge(), Table() (+18 more)

### Community 6 - "Results and Review API"
Cohesion: 0.10
Nodes (20): get_session(), get_result(), list_results(), review_result(), get_run(), list_runs(), start_run(), BatchInput (+12 more)

### Community 7 - "Workspace Cards and Badges"
Cohesion: 0.19
Nodes (22): Confidence(), Badge(), Card(), CardContent(), CardHeader(), CardTitle(), EvaluationPage(), readReport() (+14 more)

### Community 8 - "SQL Persistence"
Cohesion: 0.22
Nodes (13): RunRow, create_run(), finish_run(), load_incidents(), load_transactions(), _upsert(), upsert_tickets(), RunSummary (+5 more)

### Community 9 - "DraftResult"
Cohesion: 0.12
Nodes (13): DraftResult, RagDrafter, Drafter, DraftExecutionError, UnavailableDrafter, draft(), draft(), draft() (+5 more)

### Community 10 - "Transaction Lookup"
Cohesion: 0.13
Nodes (16): TxnRecord, _as_date(), _iqd_amount(), match_transaction(), TransactionRepo, Category, _ex(), _match() (+8 more)

### Community 11 - "App and Database Bootstrap"
Cohesion: 0.09
Nodes (18): init_db(), make_engine(), make_sessionmaker(), reset_db(), upgrade_workspace_schema(), create_app(), lifespan(), sf() (+10 more)

### Community 12 - "Dialogs and Pipeline Strip"
Cohesion: 0.16
Nodes (19): PipelineStrip(), ConfirmDialog(), FilterSelect(), statusLabels, Button(), Dialog(), DialogContent(), DialogDescription() (+11 more)

### Community 13 - "UI Package Metadata"
Cohesion: 0.11
Nodes (20): name, private, type, version, eslint, @eslint/js, eslint-plugin-react-hooks, eslint-plugin-react-refresh (+12 more)

### Community 14 - "make_ticket"
Cohesion: 0.08
Nodes (57): LookupResult, decide(), empty_ticket_decision(), merge_reasons(), note_for(), _unique(), requests_credentials(), FakeClassifier (+49 more)

### Community 15 - "Support Taxonomy Categories"
Cohesion: 0.22
Nodes (21): lookup, Account KYC, Account & Security, Agent Dispute, Agent Network, App Bug, Bill Payment, Card Issue (+13 more)

### Community 16 - "shadcn Component Config"
Cohesion: 0.09
Nodes (21): aliases, components, hooks, lib, ui, utils, iconLibrary, menuAccent (+13 more)

### Community 17 - "Workspace Routes"
Cohesion: 0.20
Nodes (17): App(), EvaluationPage, InsightsPage, KnowledgePage, NewBatchPage, QueuePage, RunDetailPage, RunsPage (+9 more)

### Community 18 - "App TypeScript Config"
Cohesion: 0.09
Nodes (21): compilerOptions, allowArbitraryExtensions, allowImportingTsExtensions, erasableSyntaxOnly, jsx, lib, module, moduleDetection (+13 more)

### Community 19 - "Support CLI"
Cohesion: 0.20
Nodes (11): init_db_cmd(), Mode, run_batch_cmd(), _run_in_memory(), _run_with_db(), seed_db_cmd(), _sessionmaker(), get_settings() (+3 more)

### Community 20 - "UploadedDocument"
Cohesion: 0.16
Nodes (12): delete_document(), download_document(), list_documents(), upload_document(), UploadedDocument, document_filename(), document_view(), DocumentValidationError (+4 more)

### Community 21 - "Node TypeScript Config"
Cohesion: 0.12
Nodes (16): compilerOptions, allowImportingTsExtensions, erasableSyntaxOnly, lib, module, moduleDetection, noEmit, noFallthroughCasesInSwitch (+8 more)

### Community 23 - "UI Dev Dependencies"
Cohesion: 0.12
Nodes (16): devDependencies, eslint, @eslint/js, eslint-plugin-react-hooks, eslint-plugin-react-refresh, globals, prettier, prettier-plugin-tailwindcss (+8 more)

### Community 24 - "pipeline/contracts.py"
Cohesion: 0.21
Nodes (13): save_outcomes(), Decision, TicketOutcome, outcome_from_state(), summarize(), outcome_to_dict(), outcome_to_row(), process_batch() (+5 more)

### Community 25 - "test_rag_drafter.py"
Cohesion: 0.08
Nodes (55): SearchResult, Sample, ConfigError, model_ids(), GeminiAnalysis, FakeStructuredLLM, answer(), call() (+47 more)

### Community 26 - "UI Runtime Dependencies"
Cohesion: 0.15
Nodes (13): dependencies, @base-ui/react, class-variance-authority, cn, @fontsource-variable/geist, lucide-react, react, react-dom (+5 more)

### Community 27 - "Theme Provider"
Cohesion: 0.17
Nodes (12): disableTransitionsTemporarily(), getSystemTheme(), isEditableTarget(), isTheme(), ResolvedTheme, Theme, THEME_VALUES, ThemeProvider() (+4 more)

### Community 28 - "test_embeddings.py"
Cohesion: 0.10
Nodes (40): EmbeddingBatch, EmbeddingError, _nonnegative_number(), OpenRouterEmbedder, _ordered_vectors(), _response_cost(), _percentile(), embedder_for() (+32 more)

### Community 29 - "Classify and Extract Prompts"
Cohesion: 0.31
Nodes (8): extract, gemini_classify, jev_classify, prepare, Gemini Classify Prompt v1, Gemini Extract Prompt v1, GeminiClassifier, JevClassifier

### Community 30 - "FakeJevRunnable"
Cohesion: 0.09
Nodes (28): CredentialCheck, DegradedCredentialChecker, _finite_nonnegative(), _get(), JevCredentialChecker, FakeJevRunnable, ResponseRunnable, test_bad_usage_cannot_poison_cost() (+20 more)

### Community 31 - "Pipeline Design Spec"
Cohesion: 0.25
Nodes (7): pgvector Postgres Service, pgdata Volume, Support Pipeline Design, Gemini 3.8 Flash, Jev, OpenRouter, ZainCash Support Pipeline

### Community 32 - "Workspace Plan Concepts"
Cohesion: 0.24
Nodes (8): Pipeline Graph Orchestration, Support Workspace HTML Shell, Support Workspace, Batch Runner, support CLI, Live Batch API, Support Workspace UI Plan, Plan 1 Live Smoke

### Community 33 - "Drafting Plan Concepts"
Cohesion: 0.25
Nodes (7): check_service_status, decide, draft, Plan 1 Part 2, Plan 1 Core Pipeline, Five-Plan Roadmap, Weekly Pattern Report

### Community 34 - "test_kb_service.py"
Cohesion: 0.11
Nodes (27): FakeEmbedder, GatedEmbedder, LateEmbedder, PaidEmbedder, count_chunks(), index_deadlines(), settings(), test_category_filters_include_general_policies_and_validate_tags() (+19 more)

### Community 35 - "Null Drafter Boundaries"
Cohesion: 0.25
Nodes (4): search_knowledge_base, Workspace NullDrafter Boundary, NullDrafter, NullDrafter

### Community 36 - "UI npm Scripts"
Cohesion: 0.25
Nodes (8): scripts, build, dev, format, lint, preview, test, typecheck

### Community 38 - "test_draft_tools.py"
Cohesion: 0.11
Nodes (30): api(), ErrorEmbedder, settings(), test_all_eight_tools_and_seven_parallel_calls_execute_only_six(), test_context_copies_input_and_rejects_raising_hard_call_limit(), test_database_faults_remain_distinct_and_record_paid_search_cost(), test_discovered_ref_can_be_inspected_but_not_promoted_to_match(), test_exact_and_fuzzy_queries_are_scoped_and_never_confirm_candidates() (+22 more)

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

### Community 46 - "KnowledgeService"
Cohesion: 0.10
Nodes (11): Embedder, KnowledgeChunk, _abandoned(), _Claim, DocumentNotFoundError, _error_cost(), IndexAttemptLostError, KnowledgeError (+3 more)

### Community 48 - "service.py"
Cohesion: 0.19
Nodes (3): Base, IncidentRow, TransactionRow

### Community 57 - "parse_document"
Cohesion: 0.12
Nodes (27): TextChunk, _append_chunks(), _check_extracted_size(), DocumentParseError, parse_document(), _parse_pdf(), make_pdf(), test_arabic_text_and_bom_are_preserved() (+19 more)

### Community 58 - "tools.py"
Cohesion: 0.09
Nodes (17): DraftAlreadySubmitted, DraftToolLimit, build_tools(), flag(), guarded(), invoke(), retrieve(), _error_cost() (+9 more)

### Community 59 - "agent.py"
Cohesion: 0.08
Nodes (6): _error_cost(), _Execution, _ModelUsage, _number(), _bounded(), visit()

### Community 60 - "SqlInvestigationRepo"
Cohesion: 0.16
Nodes (13): parse_dt(), DraftToolInputError, _datetime(), _days(), _field(), _involves(), _phone(), _phones() (+5 more)

### Community 61 - "NewBatchPage.tsx"
Cohesion: 0.13
Nodes (16): badgeVariants, buttonVariants, Tabs(), TabsContent(), TabsList(), tabsListVariants, TabsTrigger(), Textarea() (+8 more)

### Community 62 - "gemini.py"
Cohesion: 0.20
Nodes (8): Candidates, ClassifierOutput, NormalizedTicket, Classifier, FieldExtractor, GeminiClassifier, verified_pick(), render_prompt()

### Community 63 - "extract.py"
Cohesion: 0.24
Nodes (14): ExtractedField, FieldPick, _field(), fill_gaps(), finalize(), _is_weak(), FakeExtractor, _setup() (+6 more)

### Community 64 - "_DatabaseCall"
Cohesion: 0.17
Nodes (3): _check_deadline(), _consume(), _DatabaseCall

### Community 65 - "LLMUnavailable"
Cohesion: 0.22
Nodes (11): LLMUnavailable, combine(), merge_picks(), test_both_missing_raises(), test_cost_is_summed(), test_degraded_when_jev_missing(), test_disagreement_when_jev_was_partly_confident(), test_gemini_low_confidence() (+3 more)

### Community 66 - "factory.py"
Cohesion: 0.19
Nodes (7): StructuredLLM, build_pipeline(), make_draft_model(), make_gemini_llm(), make_jev_client(), GeminiExtractor, NullDrafter

### Community 67 - "Plan 3 — Knowledge retrieval and grounded reply drafting"
Cohesion: 0.12
Nodes (15): 10. Remaining demo roadmap, 1. Intent and acceptance criteria, 3. Provider and configuration, 4. Knowledge ingestion and persistence, 5. Retrieval and evidence, 7. Draft guardrails and failure outcomes, 8. Pipeline, API, CLI and UI integration, 9. Demo policies and verification (+7 more)

### Community 68 - "ingest.py"
Cohesion: 0.26
Nodes (8): load_jsonl(), load_tickets(), _rows(), test_csv_with_bom_and_missing_columns(), test_duplicate_external_ids_keep_first(), test_json_object_without_ids(), test_jsonl_fixture_loads(), test_unsupported_format()

### Community 69 - "KnowledgeDocumentIndex"
Cohesion: 0.27
Nodes (6): KnowledgeDocumentIndex, test_db_deadline_includes_pool_and_checkout_without_late_claim(), checked_in(), test_db_deadline_search_cancellation_is_nonblocking_and_retains_cost(), test_deletion_during_embedding_never_resurrects_source(), test_incompatible_or_unowned_chunks_cannot_be_searched()

### Community 70 - "Plan 3 RAG Drafting Implementation Plan"
Cohesion: 0.20
Nodes (9): Execution handoff, File map and shared interfaces, Global Constraints, Plan 3 RAG Drafting Implementation Plan, Plan self-review, Review Focus, Task 6: API/CLI indexing and persisted citation projection, Task 7: Knowledge and review workspace integration (+1 more)

### Community 71 - "SqlTransactionRepo"
Cohesion: 0.33
Nodes (3): SqlTransactionRepo, _to_record(), test_sql_transaction_repo()

### Community 72 - "KnowledgePage.tsx"
Cohesion: 0.33
Nodes (6): Input(), BadgeLabel(), KnowledgePage(), deleteDocument(), api, sizeLabel()

### Community 74 - "test_db_deadline_cancelled_publication_cannot_commit_late"
Cohesion: 0.29
Nodes (3): test_db_deadline_cancelled_publication_cannot_commit_late(), test_db_deadline_is_cumulative_across_publication_statements(), changed_index()

### Community 75 - "test_dbapi_commit_handoff_arbitrates_cancellation"
Cohesion: 0.47
Nodes (4): test_dbapi_commit_handoff_arbitrates_cancellation(), gate(), gate_before_dbapi(), gate_inside_dbapi()

## Ambiguous Edges - Review These
- `Fraud Report` → `Plan 1 Live Smoke`  [AMBIGUOUS]
  README.md · relation: conceptually_related_to
- `Stacked Cash or Cards Motif` → `Three Tilted White Rounded Bars`  [AMBIGUOUS]
  customer-support-ui/public/zaincash-mark.svg · relation: conceptually_related_to

## Knowledge Gaps
- **31 isolated node(s):** `zaincash-support`, `@fontsource-variable/geist`, `shadcn`, `tailwindcss`, `tw-animate-css` (+26 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 457 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **17 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `KnowledgeService` connect `KnowledgeService` to `Ticket Ingest`, `factory.py`, `Settings and Gemini Client`, `test_kb_service.py`, `KnowledgeDocumentIndex`, `test_draft_tools.py`, `Plan 3 RAG Drafting Implementation Plan`, `DraftResult`, `test_db_deadline_cancelled_publication_cannot_commit_late`, `test_dbapi_commit_handoff_arbitrates_cancellation`, `CredentialChecker`, `service.py`, `UploadedDocument`, `test_rag_drafter.py`, `tools.py`, `agent.py`, `test_embeddings.py`, `parse_document`?**
  _High betweenness centrality (0.041) - this node is a cross-community bridge._
- **Are the 22 inferred relationships involving `KnowledgeService` (e.g. with `Settings` and `UploadedDocument`) actually correct?**
  _`KnowledgeService` has 22 INFERRED edges - model-reasoned connections that need verification._
- **What connects `zaincash-support`, `@fontsource-variable/geist`, `shadcn` to the rest of the system?**
  _31 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Ticket Ingest` be split into smaller, more focused modules?**
  _Cohesion score 0.050331731869137496 - nodes in this community are weakly interconnected._
- **Why does `Settings` connect `Settings and Gemini Client` to `factory.py`, `test_kb_service.py`, `test_draft_tools.py`, `SQL Persistence`, `DraftResult`, `App and Database Bootstrap`, `CredentialChecker`, `KnowledgeService`, `service.py`, `Support CLI`, `test_rag_drafter.py`, `agent.py`, `test_embeddings.py`?**
  _High betweenness centrality (0.036) - this node is a cross-community bridge._

### Low-confidence Hints
_AMBIGUOUS edges — the extractor was unsure. Verify before acting on these._

- **What is the exact relationship between `Fraud Report` and `Plan 1 Live Smoke`?**
  _Edge tagged AMBIGUOUS (relation: conceptually_related_to) - confidence is low._
- **What is the exact relationship between `Stacked Cash or Cards Motif` and `Three Tilted White Rounded Bars`?**
  _Edge tagged AMBIGUOUS (relation: conceptually_related_to) - confidence is low._