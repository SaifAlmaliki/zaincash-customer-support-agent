# Graph Report - zaincash-support  (2026-10-17)

## Corpus Check
- 178 files · ~177,105 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 13 file(s) not represented in the graph (top: (none) 5, .jsonl 4, .css 2)

## Summary
- 1689 nodes · 5265 edges · 96 communities (65 shown, 31 thin omitted)
- Extraction: 90% EXTRACTED · 10% INFERRED · 0% AMBIGUOUS · INFERRED: 549 edges (avg confidence: 0.92)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `a337e3b7`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- jev.py
- guardrails.py
- PipelineDeps
- test_llm.py
- Form Controls and Preview
- Shared UI States
- runs.py
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
- Plan 3 RAG Drafting Implementation Plan
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
- rules.py
- extract.py
- _DatabaseCall
- LLMUnavailable
- gemini.py
- Plan 3 — Knowledge retrieval and grounded reply drafting
- make_ticket
- test_dbapi_commit_handoff_arbitrates_cancellation
- tools.py
- model.py
- taxonomy.py
- json
- normalize.py
- settings
- factory.py
- test_workspace_api.py
- ingest.py
- resolve_date
- account_kyc.md
- agent_dispute.md
- app_bug.md
- bill_payment.md
- card_issue.md
- failed_transfer.md
- fraud_report.md
- general_inquiry.md
- login_access.md
- other.md
- refund_request.md
- wrong_recipient.md

## God Nodes (most connected - your core abstractions)
1. `KnowledgeService` - 71 edges
2. `Settings` - 62 edges
3. `PipelineState` - 48 edges
4. `draft_state()` - 42 edges
5. `make_ticket()` - 42 edges
6. `build_pipeline()` - 41 edges
7. `make_output()` - 40 edges
8. `drafter()` - 33 edges
9. `EmbeddingError` - 32 edges
10. `FakeJevRunnable` - 30 edges

## Surprising Connections (you probably didn't know these)
- `7. Draft guardrails and failure outcomes` --references--> `requests_credentials()`  [INFERRED]
  docs/superpowers/specs/2026-10-17-plan3-rag-drafting-design.md → backend/app/pipeline/stage6_draft/guardrails.py
- `Evidence by layer` --references--> `support_test()`  [INFERRED]
  docs/demo-readiness.md → backend/tests/test_kb_service.py
- `Repeatable local walkthrough` --references--> `Settings`  [INFERRED]
  docs/demo-readiness.md → backend/app/config.py
- `Known limitations and remaining work` --references--> `get_settings()`  [INFERRED]
  docs/demo-readiness.md → backend/app/config.py
- `Commands and automated verification` --references--> `support_test()`  [INFERRED]
  docs/verification/2026-10-17-rag-drafting.md → backend/tests/test_kb_service.py

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **Cascade Classification Path** — docs_superpowers_specs_2026_10_07_support_pipeline_design_cascade, docs_superpowers_plans_2026_10_07_plan1_core_pipeline_part2_jev_classifier, docs_superpowers_plans_2026_10_07_plan1_core_pipeline_part2_gemini_classifier, docs_superpowers_plans_2026_10_07_plan1_core_pipeline_part2_cascade_combine, readme_human_approval [EXTRACTED 1.00]
- **ZainCash Mark Composition** — customer_support_ui_public_zaincash_mark_logo, customer_support_ui_public_zaincash_mark_crimson_square, customer_support_ui_public_zaincash_mark_stacked_bars [EXTRACTED 1.00]
- **Drafting Agent Toolset** — backend_app_pipeline_runner_lookup_transaction, backend_app_pipeline_runner_search_transactions, backend_app_pipeline_runner_get_customer_recent_transactions, backend_app_pipeline_runner_get_customer_ticket_history, backend_app_pipeline_runner_check_service_status, backend_app_pipeline_runner_search_knowledge_base, backend_app_pipeline_runner_flag_for_human, backend_app_pipeline_runner_submit_draft [EXTRACTED 1.00]
- **Ticket Processing Stage Flow** — backend_app_pipeline_runner_prepare, backend_app_pipeline_runner_jev_classify, backend_app_pipeline_runner_gemini_classify, backend_app_pipeline_runner_extract, backend_app_pipeline_runner_lookup, backend_app_pipeline_runner_decide, backend_app_pipeline_runner_draft [EXTRACTED 1.00]
- **Vite Logo Mark** — customer_support_ui_public_vite_vite_logo, customer_support_ui_public_vite_v_mark, customer_support_ui_public_vite_lightning_bolt [INFERRED 0.95]
- **React Brand Mark** — customer_support_ui_src_assets_react_logo, customer_support_ui_src_assets_react_atom, customer_support_ui_src_assets_react_brand [INFERRED 0.95]

## Communities (96 total, 31 thin omitted)

### Community 0 - "jev.py"
Cohesion: 0.18
Nodes (15): Candidates, ClassificationResult, ClassifierOutput, NormalizedTicket, Classifier, GeminiClassifier, build_order_check(), build_questions() (+7 more)

### Community 1 - "guardrails.py"
Cohesion: 0.12
Nodes (25): Passage, Candidate, _add(), find_candidates(), normalize_phone(), _overlaps(), parse_amount(), to_ascii_digits() (+17 more)

### Community 2 - "PipelineDeps"
Cohesion: 0.21
Nodes (8): build_graph(), PipelineDeps, InMemoryTransactionRepo, test_config_error_exits_2(), boom(), test_run_batch_no_db_writes_summary_and_out(), fake_build(), pipeline()

### Community 3 - "test_llm.py"
Cohesion: 0.14
Nodes (11): GeminiStructuredLLM, make_gemini_llm(), _llm(), _S, test_draft_model_uses_millisecond_timeout_and_disables_sdk_retries(), test_openrouter_reported_cost_takes_precedence_over_token_estimate(), test_openrouter_retry_budget_is_bounded(), test_openrouter_structured_samples_use_configured_key_and_validate_output() (+3 more)

### Community 4 - "Form Controls and Preview"
Cohesion: 0.12
Nodes (23): examples, previewResults, previewRuns, Resource, api, request(), EvaluationReport, ExtractedField (+15 more)

### Community 5 - "Shared UI States"
Cohesion: 0.18
Nodes (33): EmptyState(), ErrorState(), LoadingState(), PageHeader(), PriorityBadge(), StatusBadge(), Table(), TableBody() (+25 more)

### Community 6 - "runs.py"
Cohesion: 0.29
Nodes (9): get_run(), list_runs(), start_run(), BatchInput, RunRow, create_run(), model_ids(), run_job() (+1 more)

### Community 7 - "Workspace Cards and Badges"
Cohesion: 0.23
Nodes (17): Confidence(), Metric(), Badge(), Card(), CardContent(), CardHeader(), CardTitle(), EvaluationPage() (+9 more)

### Community 8 - "SQL Persistence"
Cohesion: 0.19
Nodes (8): finish_run(), load_incidents(), load_transactions(), SqlTransactionRepo, _to_record(), _upsert(), RunSummary, test_sql_transaction_repo()

### Community 9 - "DraftResult"
Cohesion: 0.14
Nodes (9): DraftResult, Drafter, DraftExecutionError, NullDrafter, UnavailableDrafter, draft(), draft(), draft() (+1 more)

### Community 10 - "lookup.py"
Cohesion: 0.18
Nodes (15): ExtractedField, _as_date(), _iqd_amount(), match_transaction(), TransactionRepo, _ex(), _match(), test_ambiguous_then_disambiguated_by_counterpart() (+7 more)

### Community 11 - "App and Database Bootstrap"
Cohesion: 0.15
Nodes (9): init_db(), make_engine(), make_sessionmaker(), reset_db(), upgrade_workspace_schema(), create_app(), lifespan(), sf() (+1 more)

### Community 12 - "Dialogs and Pipeline Strip"
Cohesion: 0.14
Nodes (23): PipelineStrip(), ConfirmDialog(), FilterSelect(), statusLabels, Button(), buttonVariants, Dialog(), DialogContent() (+15 more)

### Community 13 - "UI Package Metadata"
Cohesion: 0.11
Nodes (20): name, private, type, version, eslint, @eslint/js, eslint-plugin-react-hooks, eslint-plugin-react-refresh (+12 more)

### Community 14 - "test_draft_guardrails.py"
Cohesion: 0.14
Nodes (27): LookupResult, requests_credentials(), check(), state(), test_aggregation_is_deduplicated_and_has_no_state_side_effects(), test_amount_occurrences_keep_their_own_currency_and_sign(), test_avoid_sharing_warning_does_not_excuse_a_later_request(), test_candidate_prompt_limit_does_not_hide_later_ungrounded_references() (+19 more)

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
Cohesion: 0.15
Nodes (10): init_db_cmd(), Mode, run_batch_cmd(), _run_in_memory(), _run_with_db(), seed_db_cmd(), _sessionmaker(), get_settings() (+2 more)

### Community 20 - "UploadedDocument"
Cohesion: 0.10
Nodes (15): delete_document(), download_document(), list_documents(), upload_document(), UploadedDocument, Base, document_filename(), document_view() (+7 more)

### Community 21 - "Node TypeScript Config"
Cohesion: 0.12
Nodes (16): compilerOptions, allowImportingTsExtensions, erasableSyntaxOnly, lib, module, moduleDetection, noEmit, noFallthroughCasesInSwitch (+8 more)

### Community 23 - "UI Dev Dependencies"
Cohesion: 0.12
Nodes (16): devDependencies, eslint, @eslint/js, eslint-plugin-react-hooks, eslint-plugin-react-refresh, globals, prettier, prettier-plugin-tailwindcss (+8 more)

### Community 24 - "graph.py"
Cohesion: 0.18
Nodes (13): save_outcomes(), TicketOutcome, _default_retry(), outcome_from_state(), _percentile(), _retryable(), summarize(), process_batch() (+5 more)

### Community 25 - "test_rag_drafter.py"
Cohesion: 0.06
Nodes (71): Settings, build_pipeline(), ConfigError, make_draft_model(), make_jev_client(), run_batch(), GeminiAnalysis, RagDrafter (+63 more)

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
Cohesion: 0.08
Nodes (29): CredentialCheck, CredentialChecker, DegradedCredentialChecker, _finite_nonnegative(), _get(), JevCredentialChecker, FakeJevRunnable, ResponseRunnable (+21 more)

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
Cohesion: 0.08
Nodes (30): FakeEmbedder, GatedEmbedder, LateEmbedder, PaidEmbedder, test_real_knowledge_search_snapshots_are_isolated_and_json_ready(), count_chunks(), test_category_filters_include_general_policies_and_validate_tags(), test_claim_locks_source_even_before_index_row_exists() (+22 more)

### Community 35 - "Null Drafter Boundaries"
Cohesion: 0.25
Nodes (4): search_knowledge_base, Workspace NullDrafter Boundary, NullDrafter, NullDrafter

### Community 36 - "UI npm Scripts"
Cohesion: 0.25
Nodes (8): scripts, build, dev, format, lint, preview, test, typecheck

### Community 38 - "test_draft_tools.py"
Cohesion: 0.05
Nodes (47): get_session(), get_result(), list_results(), review_result(), ReviewInput, TicketInput, health(), insights() (+39 more)

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
Cohesion: 0.09
Nodes (15): Embedder, SearchResult, _abandoned(), _check_deadline(), _Claim, DocumentNotFoundError, _error_cost(), IndexAttemptLostError (+7 more)

### Community 48 - "Plan 3 RAG Drafting Implementation Plan"
Cohesion: 0.08
Nodes (23): start(), Fictional RAG walkthrough inputs, Evidence by layer, Known limitations and remaining work, Repeatable local walkthrough, Synthetic demo readiness, Execution handoff, File map and shared interfaces (+15 more)

### Community 57 - "parse_document"
Cohesion: 0.12
Nodes (26): TextChunk, _append_chunks(), _check_extracted_size(), DocumentParseError, parse_document(), _parse_pdf(), make_pdf(), test_arabic_text_and_bom_are_preserved() (+18 more)

### Community 58 - "tools.py"
Cohesion: 0.13
Nodes (7): DraftAlreadySubmitted, DraftToolLimit, build_tools(), flag(), guarded(), invoke(), _json()

### Community 59 - "DraftContext"
Cohesion: 0.09
Nodes (7): _error_cost(), _Execution, _ModelUsage, _number(), DraftContext, _bounded(), visit()

### Community 60 - "SqlInvestigationRepo"
Cohesion: 0.18
Nodes (14): TxnRecord, parse_dt(), DraftToolInputError, _datetime(), _days(), _field(), _involves(), _phone() (+6 more)

### Community 61 - "NewBatchPage.tsx"
Cohesion: 0.15
Nodes (16): badgeVariants, Input(), Tabs(), TabsContent(), TabsList(), tabsListVariants, TabsTrigger(), Textarea() (+8 more)

### Community 62 - "rules.py"
Cohesion: 0.22
Nodes (16): Decision, decide(), empty_ticket_decision(), merge_reasons(), note_for(), _unique(), Category, _decide() (+8 more)

### Community 63 - "extract.py"
Cohesion: 0.23
Nodes (14): FieldPick, FieldExtractor, _field(), fill_gaps(), finalize(), _is_weak(), FakeExtractor, _setup() (+6 more)

### Community 65 - "LLMUnavailable"
Cohesion: 0.24
Nodes (11): LLMUnavailable, combine(), merge_picks(), test_both_missing_raises(), test_cost_is_summed(), test_degraded_when_jev_missing(), test_disagreement_when_jev_was_partly_confident(), test_gemini_low_confidence() (+3 more)

### Community 66 - "gemini.py"
Cohesion: 0.31
Nodes (12): ExtractedSpan, _Fields, GeminiFields, _a(), _classify(), test_all_samples_failing_raises(), test_extractor_requests_only_named_fields(), test_failed_samples_count_against_confidence() (+4 more)

### Community 67 - "Plan 3 — Knowledge retrieval and grounded reply drafting"
Cohesion: 0.11
Nodes (18): 10. Remaining demo roadmap, 1. Intent and acceptance criteria, 3. Provider and configuration, 4. Knowledge ingestion and persistence, 5. Retrieval and evidence, 6. Bounded investigation agent, 7. Draft guardrails and failure outcomes, 8. Pipeline, API, CLI and UI integration (+10 more)

### Community 68 - "make_ticket"
Cohesion: 0.28
Nodes (18): FakeClassifier, make_output(), make_ticket(), _deps(), _run(), test_cascade_confident_jev_skips_gemini(), test_cascade_degrades_when_jev_fails(), test_cascade_uncertain_jev_goes_to_gemini() (+10 more)

### Community 69 - "test_dbapi_commit_handoff_arbitrates_cancellation"
Cohesion: 0.47
Nodes (4): test_dbapi_commit_handoff_arbitrates_cancellation(), gate(), gate_before_dbapi(), gate_inside_dbapi()

### Community 70 - "tools.py"
Cohesion: 0.14
Nodes (11): DraftSubmission, retrieve(), _error_cost(), _Flag, _History, _Input, _Knowledge, _Lookup (+3 more)

### Community 72 - "taxonomy.py"
Cohesion: 0.16
Nodes (8): load_taxonomy(), most_urgent(), priority_rank(), TaxonomyError, tax(), taxonomy(), test_priority_helpers(), test_rejects_unknown_team()

### Community 73 - "json"
Cohesion: 0.38
Nodes (4): outcome_to_dict(), outcome_to_row(), test_failed_outcome_and_dict_form(), test_full_outcome_is_json_safe()

### Community 74 - "normalize.py"
Cohesion: 0.22
Nodes (16): detect_arabizi(), fold_arabic(), has_latin_mix(), _latin_words(), mask_cards(), normalize(), sanitize_for_storage(), test_arabizi_detection() (+8 more)

### Community 75 - "settings"
Cohesion: 0.29
Nodes (5): index_deadlines(), settings(), support_test(), test_job_deadline_bounds_source_lock_wait_before_claim(), Task 3: Ticket-scoped investigation and all eight tools

### Community 76 - "factory.py"
Cohesion: 0.13
Nodes (5): Sample, StructuredLLM, GeminiExtractor, verified_pick(), render_prompt()

### Community 77 - "test_workspace_api.py"
Cohesion: 0.16
Nodes (10): upsert_tickets(), start_run(), test_batch_and_queue_expose_real_results(), test_batch_failure_is_isolated_and_conflicting_ids_rejected(), test_concurrent_conflicting_insert_is_rechecked_after_upsert(), racing_upsert(), test_openrouter_credentials_enable_api_modes_without_exposing_keys(), test_progress_counts_only_durable_results_after_save_failure() (+2 more)

### Community 79 - "ingest.py"
Cohesion: 0.26
Nodes (8): load_jsonl(), load_tickets(), _rows(), test_csv_with_bom_and_missing_columns(), test_duplicate_external_ids_keep_first(), test_json_object_without_ids(), test_jsonl_fixture_loads(), test_unsupported_format()

### Community 80 - "resolve_date"
Cohesion: 0.36
Nodes (4): resolve_date(), _safe_date(), test_resolve(), test_unresolvable_is_none()

## Ambiguous Edges - Review These
- `Fraud Report` → `Plan 1 Live Smoke`  [AMBIGUOUS]
  README.md · relation: conceptually_related_to
- `Stacked Cash or Cards Motif` → `Three Tilted White Rounded Bars`  [AMBIGUOUS]
  customer-support-ui/public/zaincash-mark.svg · relation: conceptually_related_to

## Knowledge Gaps
- **31 isolated node(s):** `@fontsource-variable/geist`, `prettier`, `prettier-plugin-tailwindcss`, `shadcn`, `tailwindcss` (+26 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 495 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **31 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Artifacts, servers and remaining concerns` connect `Plan 3 RAG Drafting Implementation Plan` to `test_draft_tools.py`?**
  _High betweenness centrality (0.221) - this node is a cross-community bridge._
- **Are the 22 inferred relationships involving `KnowledgeService` (e.g. with `Settings` and `UploadedDocument`) actually correct?**
  _`KnowledgeService` has 22 INFERRED edges - model-reasoned connections that need verification._
- **What connects `@fontsource-variable/geist`, `prettier`, `prettier-plugin-tailwindcss` to the rest of the system?**
  _31 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `guardrails.py` be split into smaller, more focused modules?**
  _Cohesion score 0.12307692307692308 - nodes in this community are weakly interconnected._
- **Why does `start()` connect `Plan 3 RAG Drafting Implementation Plan` to `NewBatchPage.tsx`?**
  _High betweenness centrality (0.220) - this node is a cross-community bridge._

### Low-confidence Hints
_AMBIGUOUS edges — the extractor was unsure. Verify before acting on these._

- **What is the exact relationship between `Fraud Report` and `Plan 1 Live Smoke`?**
  _Edge tagged AMBIGUOUS (relation: conceptually_related_to) - confidence is low._
- **What is the exact relationship between `Stacked Cash or Cards Motif` and `Three Tilted White Rounded Bars`?**
  _Edge tagged AMBIGUOUS (relation: conceptually_related_to) - confidence is low._