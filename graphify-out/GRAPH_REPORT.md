# Graph Report - zaincash-support  (2026-10-17)

## Corpus Check
- 151 files · ~87,083 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 12 file(s) not represented in the graph (top: (none) 5, .jsonl 3, .css 2)

## Summary
- 1645 nodes · 5222 edges · 80 communities (61 shown, 19 thin omitted)
- Extraction: 90% EXTRACTED · 10% INFERRED · 0% AMBIGUOUS · INFERRED: 546 edges (avg confidence: 0.92)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `983b7731`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- jev.py
- Ticket Ingest
- PipelineDeps
- test_llm.py
- Form Controls and Preview
- Shared UI States
- Results and Review API
- Workspace Cards and Badges
- SQL Persistence
- DraftResult
- lookup.py
- App and Database Bootstrap
- Dialogs and Pipeline Strip
- UI Package Metadata
- test_draft_guardrails.py
- Support Taxonomy Categories
- shadcn Component Config
- Workspace Routes
- App TypeScript Config
- Support CLI
- UploadedDocument
- Node TypeScript Config
- Pipeline Graph Nodes
- UI Dev Dependencies
- graph.py
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
- DraftContext
- SqlInvestigationRepo
- NewBatchPage.tsx
- NormalizedTicket
- extract.py
- _DatabaseCall
- LLMUnavailable
- gemini.py
- Plan 3 — Knowledge retrieval and grounded reply drafting
- make_ticket
- KnowledgeDocumentIndex
- tools.py
- model.py
- KnowledgePage.tsx
- json
- KnowledgeError
- settings
- agent.py
- DraftSubmission

## God Nodes (most connected - your core abstractions)
1. `KnowledgeService` - 71 edges
2. `Settings` - 60 edges
3. `PipelineState` - 48 edges
4. `make_ticket()` - 42 edges
5. `draft_state()` - 42 edges
6. `build_pipeline()` - 41 edges
7. `make_output()` - 40 edges
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

## Communities (80 total, 19 thin omitted)

### Community 0 - "jev.py"
Cohesion: 0.26
Nodes (10): ClassificationResult, build_order_check(), build_questions(), build_state(), category_criteria(), _input_tokens(), JevClassifier, _picks() (+2 more)

### Community 1 - "Ticket Ingest"
Cohesion: 0.07
Nodes (43): TicketInput, Candidate, _add(), find_candidates(), normalize_phone(), _overlaps(), parse_amount(), resolve_date() (+35 more)

### Community 2 - "PipelineDeps"
Cohesion: 0.18
Nodes (8): build_graph(), PipelineDeps, InMemoryTransactionRepo, test_config_error_exits_2(), boom(), test_run_batch_no_db_writes_summary_and_out(), fake_build(), pipeline()

### Community 3 - "test_llm.py"
Cohesion: 0.14
Nodes (11): GeminiStructuredLLM, make_gemini_llm(), _llm(), _S, test_draft_model_uses_millisecond_timeout_and_disables_sdk_retries(), test_openrouter_reported_cost_takes_precedence_over_token_estimate(), test_openrouter_retry_budget_is_bounded(), test_openrouter_structured_samples_use_configured_key_and_validate_output() (+3 more)

### Community 4 - "Form Controls and Preview"
Cohesion: 0.11
Nodes (23): examples, previewResults, previewRuns, Resource, request(), EvaluationReport, ExtractedField, Health (+15 more)

### Community 5 - "Shared UI States"
Cohesion: 0.23
Nodes (26): EmptyState(), ErrorState(), LoadingState(), Metric(), PageHeader(), PriorityBadge(), StatusBadge(), Table() (+18 more)

### Community 6 - "Results and Review API"
Cohesion: 0.10
Nodes (21): get_session(), get_result(), list_results(), review_result(), get_run(), list_runs(), start_run(), BatchInput (+13 more)

### Community 7 - "Workspace Cards and Badges"
Cohesion: 0.19
Nodes (22): Confidence(), Badge(), Card(), CardContent(), CardHeader(), CardTitle(), EvaluationPage(), readReport() (+14 more)

### Community 8 - "SQL Persistence"
Cohesion: 0.15
Nodes (16): create_run(), finish_run(), load_incidents(), load_transactions(), SqlTransactionRepo, _to_record(), _upsert(), upsert_tickets() (+8 more)

### Community 9 - "DraftResult"
Cohesion: 0.13
Nodes (9): DraftResult, Drafter, DraftExecutionError, NullDrafter, UnavailableDrafter, draft(), draft(), draft() (+1 more)

### Community 10 - "lookup.py"
Cohesion: 0.06
Nodes (39): Decision, ExtractedField, _as_date(), _iqd_amount(), match_transaction(), TransactionRepo, decide(), empty_ticket_decision() (+31 more)

### Community 11 - "App and Database Bootstrap"
Cohesion: 0.10
Nodes (16): _sessionmaker(), init_db(), make_engine(), make_sessionmaker(), reset_db(), upgrade_workspace_schema(), create_app(), lifespan() (+8 more)

### Community 12 - "Dialogs and Pipeline Strip"
Cohesion: 0.16
Nodes (19): PipelineStrip(), ConfirmDialog(), FilterSelect(), statusLabels, Button(), Dialog(), DialogContent(), DialogDescription() (+11 more)

### Community 13 - "UI Package Metadata"
Cohesion: 0.11
Nodes (20): name, private, type, version, eslint, @eslint/js, eslint-plugin-react-hooks, eslint-plugin-react-refresh (+12 more)

### Community 14 - "test_draft_guardrails.py"
Cohesion: 0.13
Nodes (27): LookupResult, check_draft(), _citation_findings(), requests_credentials(), check(), state(), test_aggregation_is_deduplicated_and_has_no_state_side_effects(), test_amount_occurrences_keep_their_own_currency_and_sign() (+19 more)

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
Cohesion: 0.13
Nodes (16): init_db_cmd(), Mode, run_batch_cmd(), _run_in_memory(), seed_db_cmd(), get_settings(), load_jsonl(), load_tickets() (+8 more)

### Community 20 - "UploadedDocument"
Cohesion: 0.15
Nodes (13): delete_document(), download_document(), list_documents(), upload_document(), UploadedDocument, document_filename(), document_view(), DocumentValidationError (+5 more)

### Community 21 - "Node TypeScript Config"
Cohesion: 0.12
Nodes (16): compilerOptions, allowImportingTsExtensions, erasableSyntaxOnly, lib, module, moduleDetection, noEmit, noFallthroughCasesInSwitch (+8 more)

### Community 23 - "UI Dev Dependencies"
Cohesion: 0.12
Nodes (16): devDependencies, eslint, @eslint/js, eslint-plugin-react-hooks, eslint-plugin-react-refresh, globals, prettier, prettier-plugin-tailwindcss (+8 more)

### Community 24 - "graph.py"
Cohesion: 0.19
Nodes (12): _run_with_db(), save_outcomes(), TicketOutcome, _default_retry(), outcome_from_state(), _percentile(), _retryable(), run_batch() (+4 more)

### Community 25 - "test_rag_drafter.py"
Cohesion: 0.06
Nodes (71): Settings, build_pipeline(), ConfigError, make_draft_model(), make_jev_client(), model_ids(), GeminiAnalysis, RagDrafter (+63 more)

### Community 26 - "UI Runtime Dependencies"
Cohesion: 0.15
Nodes (13): dependencies, @base-ui/react, class-variance-authority, cn, @fontsource-variable/geist, lucide-react, react, react-dom (+5 more)

### Community 27 - "Theme Provider"
Cohesion: 0.17
Nodes (12): disableTransitionsTemporarily(), getSystemTheme(), isEditableTarget(), isTheme(), ResolvedTheme, Theme, THEME_VALUES, ThemeProvider() (+4 more)

### Community 28 - "test_embeddings.py"
Cohesion: 0.10
Nodes (40): EmbeddingBatch, EmbeddingError, _nonnegative_number(), OpenRouterEmbedder, _ordered_vectors(), _response_cost(), embedder_for(), item() (+32 more)

### Community 29 - "Classify and Extract Prompts"
Cohesion: 0.31
Nodes (8): extract, gemini_classify, jev_classify, prepare, Gemini Classify Prompt v1, Gemini Extract Prompt v1, GeminiClassifier, JevClassifier

### Community 30 - "FakeJevRunnable"
Cohesion: 0.07
Nodes (37): CredentialCheck, DegradedCredentialChecker, _finite_nonnegative(), _get(), JevCredentialChecker, FakeJevRunnable, ResponseRunnable, test_bad_usage_cannot_poison_cost() (+29 more)

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
Nodes (21): GatedEmbedder, LateEmbedder, PaidEmbedder, count_chunks(), test_competing_callers_refuse_active_attempt_and_release_transactions(), test_db_deadline_cancelled_publication_cannot_commit_late(), test_db_deadline_is_cumulative_across_publication_statements(), changed_index() (+13 more)

### Community 35 - "Null Drafter Boundaries"
Cohesion: 0.25
Nodes (4): search_knowledge_base, Workspace NullDrafter Boundary, NullDrafter, NullDrafter

### Community 36 - "UI npm Scripts"
Cohesion: 0.25
Nodes (8): scripts, build, dev, format, lint, preview, test, typecheck

### Community 38 - "test_draft_tools.py"
Cohesion: 0.10
Nodes (32): IncidentRow, TransactionRow, api(), ErrorEmbedder, settings(), sf(), state(), test_all_eight_tools_and_seven_parallel_calls_execute_only_six() (+24 more)

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
Cohesion: 0.15
Nodes (14): Embedder, SearchResult, KnowledgeService, FakeEmbedder, test_real_knowledge_search_snapshots_are_isolated_and_json_ready(), test_category_filters_include_general_policies_and_validate_tags(), test_claim_locks_source_even_before_index_row_exists(), test_cosine_ranking_cutoff_and_duplicate_stable_ids() (+6 more)

### Community 48 - "service.py"
Cohesion: 0.12
Nodes (6): Base, KnowledgeChunk, KnowledgeDocumentIndex, _abandoned(), _consume(), _error_cost()

### Community 57 - "parse_document"
Cohesion: 0.12
Nodes (26): TextChunk, _append_chunks(), _check_extracted_size(), DocumentParseError, parse_document(), _parse_pdf(), make_pdf(), test_arabic_text_and_bom_are_preserved() (+18 more)

### Community 58 - "tools.py"
Cohesion: 0.14
Nodes (6): DraftAlreadySubmitted, DraftToolLimit, build_tools(), flag(), guarded(), invoke()

### Community 59 - "DraftContext"
Cohesion: 0.13
Nodes (9): Passage, _error_cost(), _ModelUsage, _number(), DraftContext, _bounded(), visit(), _json() (+1 more)

### Community 60 - "SqlInvestigationRepo"
Cohesion: 0.19
Nodes (14): TxnRecord, parse_dt(), DraftToolInputError, _datetime(), _days(), _field(), _involves(), _phone() (+6 more)

### Community 61 - "NewBatchPage.tsx"
Cohesion: 0.13
Nodes (16): badgeVariants, buttonVariants, Tabs(), TabsContent(), TabsList(), tabsListVariants, TabsTrigger(), Textarea() (+8 more)

### Community 62 - "NormalizedTicket"
Cohesion: 0.32
Nodes (9): Candidates, ClassifierOutput, NormalizedTicket, Classifier, FieldExtractor, GeminiClassifier, _field(), fill_gaps() (+1 more)

### Community 63 - "extract.py"
Cohesion: 0.23
Nodes (11): Sample, FieldPick, finalize(), FakeExtractor, _setup(), test_fill_gaps_noop_and_failure_tolerant(), test_fill_gaps_only_asks_for_weak_required_fields(), test_gemini_span_not_in_text_is_null() (+3 more)

### Community 64 - "_DatabaseCall"
Cohesion: 0.13
Nodes (4): _check_deadline(), _Claim, _DatabaseCall, IndexAttemptLostError

### Community 65 - "LLMUnavailable"
Cohesion: 0.16
Nodes (12): LLMUnavailable, combine(), merge_picks(), _Execution, test_both_missing_raises(), test_cost_is_summed(), test_degraded_when_jev_missing(), test_disagreement_when_jev_was_partly_confident() (+4 more)

### Community 66 - "gemini.py"
Cohesion: 0.16
Nodes (16): StructuredLLM, ExtractedSpan, _Fields, GeminiExtractor, GeminiFields, verified_pick(), render_prompt(), _a() (+8 more)

### Community 67 - "Plan 3 — Knowledge retrieval and grounded reply drafting"
Cohesion: 0.11
Nodes (18): 10. Remaining demo roadmap, 1. Intent and acceptance criteria, 3. Provider and configuration, 4. Knowledge ingestion and persistence, 5. Retrieval and evidence, 6. Bounded investigation agent, 7. Draft guardrails and failure outcomes, 8. Pipeline, API, CLI and UI integration (+10 more)

### Community 68 - "make_ticket"
Cohesion: 0.28
Nodes (18): FakeClassifier, make_output(), make_ticket(), _deps(), _run(), test_cascade_confident_jev_skips_gemini(), test_cascade_degrades_when_jev_fails(), test_cascade_uncertain_jev_goes_to_gemini() (+10 more)

### Community 69 - "KnowledgeDocumentIndex"
Cohesion: 0.19
Nodes (7): test_db_deadline_includes_pool_and_checkout_without_late_claim(), checked_in(), test_db_deadline_search_cancellation_is_nonblocking_and_retains_cost(), test_dbapi_commit_handoff_arbitrates_cancellation(), gate(), gate_before_dbapi(), gate_inside_dbapi()

### Community 70 - "tools.py"
Cohesion: 0.20
Nodes (10): retrieve(), _error_cost(), _Flag, _History, _Input, _Knowledge, _Lookup, _Recent (+2 more)

### Community 72 - "KnowledgePage.tsx"
Cohesion: 0.33
Nodes (6): Input(), BadgeLabel(), KnowledgePage(), deleteDocument(), api, sizeLabel()

### Community 73 - "json"
Cohesion: 0.44
Nodes (4): outcome_to_dict(), outcome_to_row(), test_failed_outcome_and_dict_form(), test_full_outcome_is_json_safe()

### Community 74 - "KnowledgeError"
Cohesion: 0.25
Nodes (3): DocumentNotFoundError, KnowledgeError, test_search_database_failure_preserves_completed_query_cost()

## Ambiguous Edges - Review These
- `Fraud Report` → `Plan 1 Live Smoke`  [AMBIGUOUS]
  README.md · relation: conceptually_related_to
- `Stacked Cash or Cards Motif` → `Three Tilted White Rounded Bars`  [AMBIGUOUS]
  customer-support-ui/public/zaincash-mark.svg · relation: conceptually_related_to

## Knowledge Gaps
- **31 isolated node(s):** `zaincash-support`, `@fontsource-variable/geist`, `shadcn`, `tailwindcss`, `tw-animate-css` (+26 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 466 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **19 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Settings` connect `test_rag_drafter.py` to `test_kb_service.py`, `test_llm.py`, `test_draft_tools.py`, `SQL Persistence`, `lookup.py`, `App and Database Bootstrap`, `agent.py`, `settings`, `KnowledgeService`, `service.py`, `Support CLI`, `graph.py`, `DraftContext`, `test_embeddings.py`?**
  _High betweenness centrality (0.041) - this node is a cross-community bridge._
- **Are the 22 inferred relationships involving `KnowledgeService` (e.g. with `Settings` and `UploadedDocument`) actually correct?**
  _`KnowledgeService` has 22 INFERRED edges - model-reasoned connections that need verification._
- **What connects `zaincash-support`, `@fontsource-variable/geist`, `shadcn` to the rest of the system?**
  _31 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Ticket Ingest` be split into smaller, more focused modules?**
  _Cohesion score 0.06924882629107981 - nodes in this community are weakly interconnected._
- **Why does `KnowledgeService` connect `KnowledgeService` to `_DatabaseCall`, `test_kb_service.py`, `KnowledgeDocumentIndex`, `tools.py`, `test_draft_tools.py`, `KnowledgeError`, `agent.py`, `service.py`, `UploadedDocument`, `test_rag_drafter.py`, `tools.py`, `DraftContext`, `test_embeddings.py`, `FakeJevRunnable`, `parse_document`?**
  _High betweenness centrality (0.040) - this node is a cross-community bridge._

### Low-confidence Hints
_AMBIGUOUS edges — the extractor was unsure. Verify before acting on these._

- **What is the exact relationship between `Fraud Report` and `Plan 1 Live Smoke`?**
  _Edge tagged AMBIGUOUS (relation: conceptually_related_to) - confidence is low._
- **What is the exact relationship between `Stacked Cash or Cards Motif` and `Three Tilted White Rounded Bars`?**
  _Edge tagged AMBIGUOUS (relation: conceptually_related_to) - confidence is low._