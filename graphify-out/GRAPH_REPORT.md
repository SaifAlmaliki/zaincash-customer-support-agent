# Graph Report - zaincash-support  (2026-11-14)

## Corpus Check
- 426 files · ~491,589 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 25 file(s) not represented in the graph (top: (none) 15, .jsonl 4, .css 4)

## Summary
- 4149 nodes · 13784 edges · 175 communities (142 shown, 33 thin omitted)
- Extraction: 84% EXTRACTED · 16% INFERRED · 0% AMBIGUOUS · INFERRED: 2146 edges (avg confidence: 0.93)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `5aa4dd63`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- EmbeddingError
- ActiveModels
- pytest
- db/models.py
- investigation.py
- cli.py
- Card
- Customer conversation intake for ZainCash support
- RunDetailPage.tsx
- IntakeController
- FakeJevRunnable
- main.py
- employee-frontend/package.json
- QueuePage.tsx
- Support Taxonomy Categories
- ui/package.json
- ModelsPage.tsx
- users-frontend/package.json
- make_ticket
- test_draft_guardrails.py
- web/package.json
- test_interview_scenarios.py
- compilerOptions
- employee-frontend/components.json
- TurnStore
- compilerOptions
- web/src/components/theme-provider.tsx
- Settings
- Classify and Extract Prompts
- test_draft_tools.py
- Pipeline Design Spec
- Batch Runner
- Drafting Plan Concepts
- test_kb_service.py
- search_knowledge_base
- web/components.json
- IntakeRepository
- ui/components.json
- intake/repository.py
- Guided intake interview — design
- Vite Config
- Human Review Gate
- compilerOptions
- NewBatchPage.tsx
- compilerOptions
- AI usage and performance dashboard (`/evaluation`) — design specification
- Human Flag Tool
- Recent Transactions Tool
- Ticket History Tool
- Lookup Transaction Tool
- Search Transactions Tool
- Submit Draft Tool
- Project Root
- parse_document
- attachments.py
- contracts.ts
- test_llm.py
- TicketRow
- use-knowledge-library.ts
- canReview
- tasks
- knowledge.py
- ChangeModelDialog.tsx
- IntakePage.tsx
- DraftResult
- agent-chat.tsx
- httpx
- normalize.py
- pipeline/graph.py
- test_catalog.py
- ChangeModelDialog.tsx
- PipelineState
- test_workspace_api.py
- test_interview_api.py
- devDependencies
- EmbeddingSwitches
- Customer intake verification — 2026-10-18
- Step
- make_output
- test_rag_api.py
- Guided intake interview verification — 2026-11-13
- fact
- test_recovery_regressions.py
- submission.py
- test_lookup.py
- resolver.py
- test_cli.py
- RAG drafting verification — 2026-10-17
- tools.py
- devDependencies
- devDependencies
- gemini.py
- ticket-flow.ts
- Per-model evaluation (quality, system, cost) — design specification
- compilerOptions
- fakes.py
- ZainCash Support Workspace
- dependencies
- InvalidEvidence
- dependencies
- compilerOptions
- KnowledgeError
- intake/api.ts
- test_final_fix_handoff.py
- TicketInput
- pydantic
- scripts
- Deviations from the spec (intentional, small)
- compilerOptions
- Maintainability and stale-code refactor — design specification
- demo-readiness.md
- web/tsconfig.json
- employee-frontend/tsconfig.json
- exports
- Review Focus
- scripts
- users-frontend/README.md
- policy.py
- TurnContext
- find_candidates
- admin.py
- guardrails.py
- embedder.py
- test_workspace_schema.py
- intake/model.py
- openrouter_chat.py
- intake.py
- Review Focus
- EmbeddingBatch
- test_draft_model.py
- Ticket flow charts
- recover_intake_processing
- types.py
- 5. Backend design
- pipeline/contracts.py
- Global Constraints
- passage-reading.ts
- ExtractedField
- Embedder
- probe.py
- components-ai-thought-chain.tsx
- 4. Backend design
- intake/README.md
- test_taxonomy.py
- test_dbapi_commit_handoff_arbitrates_cancellation
- Global Constraints
- ZainCash support: architecture and ticket flow {#support-overview}
- IntakePage.test.tsx
- employee-frontend/src/components/theme-provider.tsx
- _ModelUsage
- _Execution
- _aware
- Customer phone identity design
- index_deadlines
- api-entrypoint.sh
- 7. Customer frontend design
- AI Usage and Performance Dashboard Implementation Plan — Part 1 of 2 (backend)
- _error_cost
- build_pipeline
- Customer Conversation Intake Implementation Plan
- state
- test_submission.py

## God Nodes (most connected - your core abstractions)
1. `Settings` - 190 edges
2. `Step` - 109 edges
3. `ModelChoice` - 92 edges
4. `KnowledgeService` - 86 edges
5. `fact()` - 77 edges
6. `ActiveModels` - 74 edges
7. `context()` - 71 edges
8. `useCopy()` - 68 edges
9. `message()` - 66 edges
10. `IntakeController` - 59 edges

## Surprising Connections (you probably didn't know these)
- `Repeatable local walkthrough` --references--> `Settings`  [INFERRED]
  docs/demo-readiness.md → backend/app/config.py
- `Ticket write paths` --references--> `upsert_tickets()`  [INFERRED]
  docs/superpowers/specs/2026-11-13-customer-phone-identity-design.md → backend/app/db/repository.py
- `Existing data` --references--> `upgrade_workspace_schema()`  [INFERRED]
  docs/superpowers/specs/2026-11-13-customer-phone-identity-design.md → backend/app/db/workspace_schema.py
- `Task 9: Repair the Five-Record JSONL Baseline Fixture` --references--> `load_jsonl()`  [INFERRED]
  docs/superpowers/plans/2026-11-02-backend-maintainability.md → backend/app/ingest.py
- `Re-ask once` --references--> `QuestionRecord`  [INFERRED]
  docs/superpowers/specs/2026-11-13-guided-intake-interview-design.md → backend/app/intake/contracts.py

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **Cascade Classification Path** — docs_superpowers_specs_2026_10_07_support_pipeline_design_cascade, docs_superpowers_plans_2026_10_07_plan1_core_pipeline_part2_jev_classifier, docs_superpowers_plans_2026_10_07_plan1_core_pipeline_part2_gemini_classifier, docs_superpowers_plans_2026_10_07_plan1_core_pipeline_part2_cascade_combine, readme_human_approval [EXTRACTED 1.00]
- **Drafting Agent Toolset** — backend_app_pipeline_runner_lookup_transaction, backend_app_pipeline_runner_search_transactions, backend_app_pipeline_runner_get_customer_recent_transactions, backend_app_pipeline_runner_get_customer_ticket_history, backend_app_pipeline_runner_check_service_status, backend_app_pipeline_runner_search_knowledge_base, backend_app_pipeline_runner_flag_for_human, backend_app_pipeline_runner_submit_draft [EXTRACTED 1.00]
- **Ticket Processing Stage Flow** — backend_app_pipeline_runner_prepare, backend_app_pipeline_runner_jev_classify, backend_app_pipeline_runner_gemini_classify, backend_app_pipeline_runner_extract, backend_app_pipeline_runner_lookup, backend_app_pipeline_runner_decide, backend_app_pipeline_runner_draft [EXTRACTED 1.00]

## Communities (175 total, 33 thin omitted)

### Community 0 - "EmbeddingError"
Cohesion: 0.12
Nodes (37): EmbeddingError, OpenRouterEmbedder, embedder_for(), item(), response_payload(), settings(), test_33_inputs_are_batched_and_each_batch_maps_its_own_indexes(), respond() (+29 more)

### Community 1 - "ActiveModels"
Cohesion: 0.09
Nodes (30): ActiveModels, make_draft_model(), make_gemini_llm(), model_ids(), batch_concurrency(), _current_models(), _local_pipeline(), ticket_timeout_s() (+22 more)

### Community 2 - "pytest"
Cohesion: 0.16
Nodes (42): test_blank_intake_model_is_rejected(), test_contracts_reject_extra_keys(), test_non_positive_image_limit_is_rejected(), _tool_chat(), answer(), call(), Checker, draft_state() (+34 more)

### Community 3 - "db/models.py"
Cohesion: 0.10
Nodes (19): Base, IntakeSubmissionRow, KnowledgeChunk, EmbeddingSwitchRow, ModelSettingAuditRow, ModelSettingRow, _client(), _documents() (+11 more)

### Community 4 - "investigation.py"
Cohesion: 0.16
Nodes (13): parse_dt(), DraftToolInputError, _datetime(), _days(), _field(), _involves(), _phone(), _phones() (+5 more)

### Community 5 - "cli.py"
Cohesion: 0.07
Nodes (28): _command_settings(), ingest_kb_cmd(), ingest(), init_db_cmd(), Mode, run_batch_cmd(), _run_in_memory(), seed_db_cmd() (+20 more)

### Community 6 - "Card"
Cohesion: 0.12
Nodes (57): Task 5: Extract presentational DocumentList and KnowledgeReadiness components, Task 12: Locale parity test and translated Runs pages, 6.4 Focused view extraction, ErrorState(), Card(), CardContent(), CardHeader(), CardTitle() (+49 more)

### Community 7 - "Customer conversation intake for ZainCash support"
Cohesion: 0.06
Nodes (31): 10. Verification and acceptance criteria, 11. Delivery and review, 1. Outcome and agreed requirements, 2. Current implementation and integration points, 3. Approach and boundaries, 4. Conversation state and turn flow, 5. Facts, evidence, and readiness, 6. Language and screenshot behavior (+23 more)

### Community 8 - "RunDetailPage.tsx"
Cohesion: 0.06
Nodes (40): Employee Frontend Maintainability Implementation Plan, Global Constraints, Review Focus, Task 1: Remove reference-verified dead exports, components, and the Mermaid dependency, Task 2: Migrate active TicketFlow coverage, then retire the legacy trace/chart cluster, Task 3: Split RunDetailPage and introduce bounded run-result loading, Task 4: Extract and test the pure queue projection, Task 6: Repair ExtractedField fixtures and make standalone typecheck real (+32 more)

### Community 9 - "IntakeController"
Cohesion: 0.15
Nodes (13): Task 6: Customer API client and resumable UI state, Task 1: Cleanup-first removal of reference-verified dead code and dependencies, Task 7: Preserve resume-unavailable state across `startNew`, Task 7: Intake app data layer — phone helper, contracts, API, controller, Task 7: Customer frontend data layer, ControllerState, emptyState(), IntakeController (+5 more)

### Community 10 - "FakeJevRunnable"
Cohesion: 0.11
Nodes (19): CredentialCheck, CredentialChecker, DegradedCredentialChecker, _finite_nonnegative(), _get(), JevCredentialChecker, ResponseRunnable, test_bad_usage_cannot_poison_cost() (+11 more)

### Community 11 - "main.py"
Cohesion: 0.06
Nodes (31): init_db(), initialize_database(), make_engine(), make_sessionmaker(), reset_db(), _accepts(), create_app(), lifespan() (+23 more)

### Community 12 - "employee-frontend/package.json"
Cohesion: 0.06
Nodes (30): @base-ui/react, class-variance-authority, cn, eslint, @eslint/js, eslint-plugin-react-hooks, eslint-plugin-react-refresh, @fontsource/tajawal (+22 more)

### Community 14 - "QueuePage.tsx"
Cohesion: 0.14
Nodes (35): Task 16: Model detail, confusion matrix and predictions drawer, Task 10: Employee app — customer page and ticket header link, Task 15: Ticket cost table and AI timeline, 5.1 Data access, Confidence(), EmptyState(), LoadingState(), PageHeader() (+27 more)

### Community 15 - "Support Taxonomy Categories"
Cohesion: 0.21
Nodes (22): lookup, Account KYC, Account & Security, Agent Dispute, Agent Network, App Bug, Bill Payment, Card Issue (+14 more)

### Community 16 - "ui/package.json"
Cohesion: 0.08
Nodes (24): @base-ui/react, class-variance-authority, cn, eslint, @eslint/js, eslint-plugin-react-hooks, eslint-plugin-react-refresh, @fontsource/tajawal (+16 more)

### Community 17 - "ModelsPage.tsx"
Cohesion: 0.09
Nodes (38): App(), CustomerPage, EvaluationPage, InsightsPage, KnowledgePage, ModelsPage, NewBatchPage, QueuePage (+30 more)

### Community 18 - "users-frontend/package.json"
Cohesion: 0.08
Nodes (23): turbo, devDependencies, prettier, prettier-plugin-tailwindcss, turbo, typescript, engines, node (+15 more)

### Community 19 - "make_ticket"
Cohesion: 0.21
Nodes (19): FakeClassifier, make_ticket(), _deps(), _run(), test_concurrency_is_limited(), test_draft_node_never_retries_or_restarts_paid_work(), test_drafter_reasons_escalate(), draft() (+11 more)

### Community 20 - "test_draft_guardrails.py"
Cohesion: 0.16
Nodes (25): requests_credentials(), check(), test_aggregation_is_deduplicated_and_has_no_state_side_effects(), test_amount_occurrences_keep_their_own_currency_and_sign(), test_avoid_sharing_warning_does_not_excuse_a_later_request(), test_candidate_prompt_limit_does_not_hide_later_ungrounded_references(), test_candidate_transactions_cannot_authorize_reply_evidence(), test_citations_must_have_been_retrieved_for_this_ticket() (+17 more)

### Community 21 - "web/package.json"
Cohesion: 0.05
Nodes (38): jsdom, @testing-library/jest-dom, @testing-library/react, @workspace/ui, dependencies, clsx, react, react-dom (+30 more)

### Community 22 - "test_interview_scenarios.py"
Cohesion: 0.31
Nodes (9): analyze_calls(), Chat, source_of(), summary(), test_complete_report_goes_straight_to_review(), test_no_reference_number_still_gives_a_complete_report(), test_vague_report_is_interviewed_into_a_complete_ticket(), updates() (+1 more)

### Community 23 - "compilerOptions"
Cohesion: 0.08
Nodes (23): compilerOptions, allowArbitraryExtensions, allowImportingTsExtensions, erasableSyntaxOnly, jsx, lib, module, moduleDetection (+15 more)

### Community 24 - "employee-frontend/components.json"
Cohesion: 0.09
Nodes (21): aliases, components, hooks, lib, ui, utils, iconLibrary, menuAccent (+13 more)

### Community 25 - "TurnStore"
Cohesion: 0.12
Nodes (19): session(), OperationClaim, ProgressItem, ReviewSnapshot, TurnResult, progress(), sanitize_intake_text(), _jsonable() (+11 more)

### Community 26 - "compilerOptions"
Cohesion: 0.09
Nodes (22): compilerOptions, allowArbitraryExtensions, allowImportingTsExtensions, erasableSyntaxOnly, jsx, lib, module, moduleDetection (+14 more)

### Community 27 - "web/src/components/theme-provider.tsx"
Cohesion: 0.16
Nodes (13): App(), controller, disableTransitionsTemporarily(), getSystemTheme(), isEditableTarget(), isTheme(), ResolvedTheme, Theme (+5 more)

### Community 28 - "Settings"
Cohesion: 0.10
Nodes (13): Settings, test_relative_upload_directory_is_rooted_in_the_repository(), test_anthropic_model_selects_the_draft_model_only(), test_defaults(), test_draft_token_prices_follow_the_selected_draft_model(), test_drafting_configuration_cannot_bypass_hard_limits(), test_drafting_limits_load_from_environment(), test_env_overrides() (+5 more)

### Community 29 - "Classify and Extract Prompts"
Cohesion: 0.33
Nodes (7): extract, gemini_classify, Pipeline Graph Orchestration, jev_classify, prepare, GeminiClassifier, JevClassifier

### Community 30 - "test_draft_tools.py"
Cohesion: 0.13
Nodes (27): IncidentRow, test_all_eight_tools_and_seven_parallel_calls_execute_only_six(), test_context_copies_input_and_rejects_raising_hard_call_limit(), test_database_faults_remain_distinct_and_record_paid_search_cost(), test_discovered_ref_can_be_inspected_but_not_promoted_to_match(), test_exact_and_fuzzy_queries_are_scoped_and_never_confirm_candidates(), test_exact_reference_still_requires_customer_and_excludes_future(), test_failure_trace_bounds_invalid_numeric_arguments() (+19 more)

### Community 31 - "Pipeline Design Spec"
Cohesion: 0.25
Nodes (7): pgvector Postgres Service, pgdata Volume, Support Pipeline Design, Gemini 3.8 Flash, Jev, OpenRouter, ZainCash Support Pipeline

### Community 32 - "Batch Runner"
Cohesion: 0.29
Nodes (7): Plan 1 Part 2, Batch Runner, NullDrafter, Plan 1 Core Pipeline, Live Batch API, Plan 1 Live Smoke, NullDrafter

### Community 33 - "Drafting Plan Concepts"
Cohesion: 0.25
Nodes (5): check_service_status, decide, draft, Five-Plan Roadmap, Weekly Pattern Report

### Community 34 - "test_kb_service.py"
Cohesion: 0.10
Nodes (36): KnowledgeService, FakeEmbedder, GatedEmbedder, LateEmbedder, PaidEmbedder, count_chunks(), test_category_filters_include_general_policies_and_validate_tags(), test_claim_locks_source_even_before_index_row_exists() (+28 more)

### Community 36 - "web/components.json"
Cohesion: 0.10
Nodes (19): aliases, components, hooks, lib, ui, utils, iconLibrary, menuAccent (+11 more)

### Community 38 - "IntakeRepository"
Cohesion: 0.10
Nodes (13): Credentials, IntakeModel, PendingQuestion, SessionView, IntakeRepository, IntakeService, make_intake_service(), intake_client() (+5 more)

### Community 39 - "ui/components.json"
Cohesion: 0.10
Nodes (19): aliases, components, hooks, lib, ui, utils, iconLibrary, menuAccent (+11 more)

### Community 40 - "intake/repository.py"
Cohesion: 0.13
Nodes (25): CustomerReview, Message, IntakeMessageRow, IntakeSessionRow, InvalidCustomerPhone, pending_question(), customer_review(), initial_state() (+17 more)

### Community 41 - "Guided intake interview — design"
Cohesion: 0.06
Nodes (35): 1. Question rules (backend), 2. API contract, 3. Chat screen, 4. Review card, Actions, Additional issues, Approach, Backend (pytest, guarded `support_test`) (+27 more)

### Community 43 - "Human Review Gate"
Cohesion: 0.25
Nodes (4): support CLI, Support Workspace UI Plan, Review API, Workspace UI Verification

### Community 44 - "compilerOptions"
Cohesion: 0.12
Nodes (16): compilerOptions, allowImportingTsExtensions, erasableSyntaxOnly, lib, module, moduleDetection, noEmit, noFallthroughCasesInSwitch (+8 more)

### Community 46 - "NewBatchPage.tsx"
Cohesion: 0.06
Nodes (50): Global Constraints, Per-model Evaluation Implementation Plan — Part 3 of 3 (frontend, translations, verification), Task 14: Evaluation view helpers, Task 15: Provenance, headline metrics, comparison table and empty state, Task 17: Run dialog, progress, page assembly, route and styles, Task 18: Documentation, full verification and manual check, Task 9: Employee app — required phone, queue identity and search, batch entry, AI Usage and Performance Dashboard Implementation Plan — Part 2 of 2 (frontend, docs, verification) (+42 more)

### Community 47 - "compilerOptions"
Cohesion: 0.12
Nodes (16): compilerOptions, allowImportingTsExtensions, erasableSyntaxOnly, lib, module, moduleDetection, noEmit, noFallthroughCasesInSwitch (+8 more)

### Community 48 - "AI usage and performance dashboard (`/evaluation`) — design specification"
Cohesion: 0.14
Nodes (13): 10. Phase 2 (for reference, not designed here), 1. Outcome and success criteria, 2. Current state, 3. Decisions, 5.1 Page, 5.2 Components and data, 5.3 Text and direction, 5. Frontend design (+5 more)

### Community 57 - "parse_document"
Cohesion: 0.08
Nodes (35): TextChunk, _append_chunks(), _check_extracted_size(), _combining_only(), DocumentParseError, _is_ltr(), _is_rtl(), _line_text() (+27 more)

### Community 58 - "attachments.py"
Cohesion: 0.12
Nodes (24): AttachmentStore, _display_name(), Attachment, IntakeAttachmentRow, ImageRejected, NotOwned, attachment_from_row(), png_bytes() (+16 more)

### Community 59 - "contracts.ts"
Cohesion: 0.17
Nodes (34): Task 5: Add complete dependency-free API and persisted-session guards, createIntakeApi(), ANSWER_KINDS, CHOICES, FACT_STATUSES, finiteNonnegative(), invalid(), isRecord() (+26 more)

### Community 60 - "test_llm.py"
Cohesion: 0.12
Nodes (12): StructuredChatLLM, DraftModelInfo, _llm(), _S, test_draft_model_uses_millisecond_timeout_and_disables_sdk_retries(), test_openrouter_reported_cost_takes_precedence_over_token_estimate(), test_openrouter_retry_budget_is_bounded(), test_openrouter_structured_samples_use_configured_key_and_validate_output() (+4 more)

### Community 61 - "TicketRow"
Cohesion: 0.06
Nodes (44): get_customer(), get_session(), get_result(), list_results(), read_intake_attachment(), review_result(), BatchInput, ReviewInput (+36 more)

### Community 62 - "use-knowledge-library.ts"
Cohesion: 0.26
Nodes (12): acceptIndexRequest(), canRequestIndex(), PendingIndexes, persistPendingIndexes(), pollKnowledge(), refresh(), stop(), PollOptions (+4 more)

### Community 63 - "canReview"
Cohesion: 0.50
Nodes (3): Task 8: Employee evidence panel and processing state, canReview(), REVIEWABLE

### Community 64 - "tasks"
Cohesion: 0.11
Nodes (18): dependsOn, inputs, outputs, cache, persistent, dependsOn, dependsOn, $schema (+10 more)

### Community 65 - "knowledge.py"
Cohesion: 0.09
Nodes (29): _configured(), delete_document(), download_document(), index_document(), list_chunks(), list_documents(), _require_provider(), search_knowledge() (+21 more)

### Community 66 - "ChangeModelDialog.tsx"
Cohesion: 0.07
Nodes (50): Admin model configuration — employee frontend implementation plan, Backend API contract used here, File structure, Global Constraints, Review Focus, Task 1: API types, admin session and admin requests, Task 2: Strings, the AI locality chip, run models and the batch switch message, Task 3: Model choice logic and the change dialog (+42 more)

### Community 67 - "IntakePage.tsx"
Cohesion: 0.07
Nodes (46): Task 1: Put the summary and receipt in the thread, Task 10: Grouped review card with answer buttons, Task 9: Progress strip, 1. Outcome, 2. Scope, 3. Layout, 4. Components, 5. Checks (+38 more)

### Community 68 - "DraftResult"
Cohesion: 0.05
Nodes (35): DraftResult, Drafter, NullDrafter, UnavailableDrafter, draft(), Completion and review record — 2026-10-17, Execution handoff, File map and shared interfaces (+27 more)

### Community 69 - "agent-chat.tsx"
Cohesion: 0.15
Nodes (25): Task 8: Chat screen — instant bubble, typing, reasons, quick replies, composer hints, clsx, tailwind-merge, @testing-library/user-event, AgentChat, AgentChatProps, AgentMessage, AssistantText() (+17 more)

### Community 70 - "httpx"
Cohesion: 0.11
Nodes (14): OllamaProvider, _provider(), _tags_handler(), test_catalog_lists_installed_models_with_reported_capabilities(), handler(), test_chat_model_sets_the_configured_context_window(), test_chat_model_targets_the_configured_server(), test_embedder_uses_openai_compatible_endpoint_without_dimensions() (+6 more)

### Community 71 - "normalize.py"
Cohesion: 0.14
Nodes (23): detect_arabizi(), fold_arabic(), has_latin_mix(), _latin_words(), normalize(), sanitize_for_storage(), mask_cards(), test_arabizi_detection() (+15 more)

### Community 72 - "pipeline/graph.py"
Cohesion: 0.06
Nodes (50): _safe_dispatch(), get_run(), list_runs(), start_run(), _run_with_db(), ensure_customers(), RunRow, TransactionRow (+42 more)

### Community 73 - "test_catalog.py"
Cohesion: 0.26
Nodes (8): CatalogCache, step_catalog(), BrokenStatusProvider, test_a_provider_whose_status_check_raises_is_listed_as_unreachable(), test_catalog_errors_stay_per_provider_and_cache_respects_ttl(), test_classify_catalog_only_offers_typesafe(), test_step_catalog_filters_and_marks_unknown(), Task 8: Live model tests and the model catalog

### Community 74 - "ChangeModelDialog.tsx"
Cohesion: 0.13
Nodes (33): ConfirmDialog(), FilterSelect(), Button(), Dialog(), DialogContent(), DialogDescription(), DialogFooter(), DialogHeader() (+25 more)

### Community 75 - "PipelineState"
Cohesion: 0.30
Nodes (3): _Nodes, PipelineState, 3. What the employee sees

### Community 76 - "test_workspace_api.py"
Cohesion: 0.13
Nodes (17): review_payload(), start_run(), test_batch_and_queue_expose_real_results(), test_batch_failure_is_isolated_and_conflicting_ids_rejected(), test_concurrent_conflicting_insert_is_rechecked_after_upsert(), racing_upsert(), test_customer_profile_lists_the_latest_result_of_each_ticket(), test_progress_counts_only_durable_results_after_save_failure() (+9 more)

### Community 77 - "test_interview_api.py"
Cohesion: 0.21
Nodes (19): analyze_calls(), ask(), complete_without_reference(), opening(), opening_with_amount(), reference_answer(), send(), start() (+11 more)

### Community 79 - "devDependencies"
Cohesion: 0.12
Nodes (16): devDependencies, eslint, @eslint/js, eslint-plugin-react-hooks, eslint-plugin-react-refresh, globals, prettier, prettier-plugin-tailwindcss (+8 more)

### Community 80 - "EmbeddingSwitches"
Cohesion: 0.19
Nodes (3): EmbeddingSwitches, _view(), Task 4: The Models page, navigation and route

### Community 81 - "Customer intake verification — 2026-10-18"
Cohesion: 0.25
Nodes (6): Browser handoff, Customer intake verification — 2026-10-18, Final automated checks, Live vision and paired review, Repaired gaps and regression evidence, Review decisions and remaining limits

### Community 82 - "Step"
Cohesion: 0.08
Nodes (22): probe(), _iso(), ModelChoice, ProbeResult, Step, test_start_updates_the_cache_without_reloading_from_the_database(), _registry(), StructuredChat (+14 more)

### Community 83 - "make_output"
Cohesion: 0.26
Nodes (14): build_graph(), PipelineDeps, InMemoryTransactionRepo, load_taxonomy(), tax(), make_output(), pipeline(), test_run_batch_defaults_to_jev() (+6 more)

### Community 84 - "test_rag_api.py"
Cohesion: 0.14
Nodes (18): client(), test_actual_guardrail_failure_is_separate_from_reply(), test_concurrent_index_requests_share_active_work(), test_disabled_or_missing_provider_stores_without_indexing(), test_explicit_retry_tags_search_and_chunk_pagination(), test_health_distinguishes_failed_from_empty(), test_health_requires_compatible_nonempty_index(), test_index_background_admission_is_bounded_and_releases_capacity() (+10 more)

### Community 85 - "Guided intake interview verification — 2026-11-13"
Cohesion: 0.20
Nodes (9): Arabic at 390×844, starting from the vague message, English at 1280×900, with the complete message, Final automated checks, Guided intake interview verification — 2026-11-13, Live browser run, Live probe output (facts only), Live transfer probe, Observations (+1 more)

### Community 86 - "fact"
Cohesion: 0.11
Nodes (54): Analysis, EvidenceRef, Readiness, ReviewText, build_review(), validate_review_numbers(), context(), fact() (+46 more)

### Community 87 - "test_recovery_regressions.py"
Cohesion: 0.22
Nodes (12): command(), create(), test_actual_app_restart_reconciles_failed_placeholder(), test_failed_review_retry_cannot_reopen_submitted_session(), test_original_payload_identity_survives_sanitization(), test_publication_failure_is_retryable_without_restart(), fail_once(), test_receipt_reference_is_preserved() (+4 more)

### Community 88 - "submission.py"
Cohesion: 0.21
Nodes (13): Receipt, IntakeOperationRow, IntakeError, OperationConflict, RevisionConflict, StaleReview, TurnBusy, assert_same_operation() (+5 more)

### Community 89 - "test_lookup.py"
Cohesion: 0.20
Nodes (15): _as_date(), _iqd_amount(), match_transaction(), txn_from_dict(), _ex(), _match(), test_ambiguous_then_disambiguated_by_counterpart(), test_amount_and_date_mismatch() (+7 more)

### Community 90 - "resolver.py"
Cohesion: 0.20
Nodes (10): draft_timeout_s(), eligibility(), env_defaults(), intake_timeout_s(), _settings(), test_eligibility(), test_env_defaults_match_todays_settings(), test_env_overrides_for_draft_and_intake() (+2 more)

### Community 91 - "test_cli.py"
Cohesion: 0.14
Nodes (9): test_config_error_exits_2(), boom(), test_ingest_directory_is_deterministic_and_duplicate_is_free(), test_ingest_disabled_configuration_never_calls_provider(), test_ingest_failure_exit_and_retry_stored(), test_ingest_invalid_source_does_not_stop_other_files(), test_ingest_limits_batch_without_partial_side_effects(), test_retry_stored_indexes_old_uploads_without_recovering_other_process_jobs() (+1 more)

### Community 92 - "RAG drafting verification — 2026-10-17"
Cohesion: 0.22
Nodes (11): support_test(), Artifacts, servers and remaining concerns, Citation IDs and provider evidence, Commands and automated verification — historical Task 8, Corpus and actual retrieval, Current final verification and review closure, Environment and isolation, Live browser and persistence evidence (+3 more)

### Community 93 - "tools.py"
Cohesion: 0.05
Nodes (28): KnowledgeExecutionError, DraftAlreadySubmitted, DraftSubmission, DraftToolLimit, _bounded(), visit(), build_tools(), flag() (+20 more)

### Community 94 - "devDependencies"
Cohesion: 0.11
Nodes (19): devDependencies, eslint, @eslint/js, eslint-plugin-react-hooks, eslint-plugin-react-refresh, globals, jsdom, @tailwindcss/vite (+11 more)

### Community 95 - "devDependencies"
Cohesion: 0.17
Nodes (12): devDependencies, eslint, @eslint/js, eslint-plugin-react-hooks, eslint-plugin-react-refresh, globals, tailwindcss, @types/node (+4 more)

### Community 96 - "gemini.py"
Cohesion: 0.18
Nodes (9): StructuredLLM, ExtractedSpan, _Fields, GeminiExtractor, GeminiFields, verified_pick(), render_prompt(), test_extractor_requests_only_named_fields() (+1 more)

### Community 97 - "ticket-flow.ts"
Cohesion: 0.08
Nodes (48): Task 2: Which step is open, Task 3: Received, produced, and drafting events, buildTicketFlow(), AR, channelName(), checkLines(), EN, fieldLabel() (+40 more)

### Community 98 - "Per-model evaluation (quality, system, cost) — design specification"
Cohesion: 0.20
Nodes (9): 1. Outcome and success criteria, 3. Decisions, 5.3 Text and direction, 5.4 Runs pages, 5.5 Import format, 5. Employee-frontend design, 6. Error handling, 8. Out of scope (+1 more)

### Community 99 - "compilerOptions"
Cohesion: 0.14
Nodes (13): compilerOptions, jsx, lib, module, moduleResolution, noEmit, paths, skipLibCheck (+5 more)

### Community 100 - "fakes.py"
Cohesion: 0.15
Nodes (19): LLMUnavailable, Sample, FieldPick, NormalizedTicket, FieldExtractor, _field(), fill_gaps(), finalize() (+11 more)

### Community 101 - "ZainCash Support Workspace"
Cohesion: 0.25
Nodes (8): Current capability boundaries, Data source, Modular file map, Open the right project, Run locally, shadcn conventions, Workflow, ZainCash Support Workspace

### Community 102 - "dependencies"
Cohesion: 0.12
Nodes (16): dependencies, @base-ui/react, class-variance-authority, cn, @fontsource/tajawal, @fontsource-variable/plus-jakarta-sans, lucide-react, motion (+8 more)

### Community 103 - "InvalidEvidence"
Cohesion: 0.11
Nodes (35): Fact, canonical_digits(), normalize_reported_date(), InvalidEvidence, _apply(), _check_reference(), _compact(), merge_analysis() (+27 more)

### Community 104 - "dependencies"
Cohesion: 0.20
Nodes (10): dependencies, @base-ui/react, class-variance-authority, cn, @fontsource/tajawal, @fontsource-variable/plus-jakarta-sans, react, react-dom (+2 more)

### Community 105 - "compilerOptions"
Cohesion: 0.17
Nodes (11): compilerOptions, jsx, lib, module, moduleResolution, outDir, skipLibCheck, strict (+3 more)

### Community 106 - "KnowledgeError"
Cohesion: 0.09
Nodes (9): _DatabaseCall, _Claim, DocumentNotFoundError, IndexAttemptLostError, KnowledgeError, ErrorEmbedder, Task 14: Preserve Safe Knowledge 503s and Log Only Unexpected Diagnostic Types, 2. Current state (+1 more)

### Community 107 - "intake/api.ts"
Cohesion: 0.11
Nodes (22): Task 4: Make pending operations discriminated and use one request identity, IntakeApi, INTAKE_FALLBACK_MESSAGE, Activity, fileIdentity(), AnswerKind, AskCommand, Credentials (+14 more)

### Community 108 - "test_final_fix_handoff.py"
Cohesion: 0.09
Nodes (23): Passage, RagDrafter, DraftExecutionError, assert_completed_evidence(), faulty_knowledge(), read(), outer_deadlines(), PaidEmbeddings (+15 more)

### Community 110 - "pydantic"
Cohesion: 0.23
Nodes (6): CitationSource, _Draft, draft_evidence(), _Guardrail, _TraceModel, _validated()

### Community 111 - "scripts"
Cohesion: 0.25
Nodes (8): scripts, build, dev, format, lint, preview, test, typecheck

### Community 112 - "Deviations from the spec (intentional, small)"
Cohesion: 0.17
Nodes (7): Deviations from the spec (intentional, small), Global Constraints, Per-model Evaluation Implementation Plan — Part 2 of 3 (evaluation engine), Task 11: `support eval` CLI and v2 export, Task 7: Metrics, Task 8: Evaluation storage and views, Task 9: Runner, request validation and cost estimate

### Community 113 - "compilerOptions"
Cohesion: 0.29
Nodes (6): compilerOptions, module, moduleResolution, skipLibCheck, strict, target

### Community 114 - "Maintainability and stale-code refactor — design specification"
Cohesion: 0.12
Nodes (15): 10. Verification and acceptance, 1. Outcome and success criteria, 2. Audit baseline, 3. Selected approach and sequence, 4. Boundaries and non-goals, 8.1 Approved deletions, 8.2 Docker and documentation, 8.3 Graphify outputs (+7 more)

### Community 115 - "demo-readiness.md"
Cohesion: 0.24
Nodes (5): Fictional RAG walkthrough inputs, Evidence by layer, Known limitations and remaining work, Repeatable local walkthrough, Synthetic demo readiness

### Community 116 - "web/tsconfig.json"
Cohesion: 0.33
Nodes (5): compilerOptions, paths, files, @workspace/ui/*, references

### Community 117 - "employee-frontend/tsconfig.json"
Cohesion: 0.40
Nodes (4): compilerOptions, paths, files, references

### Community 118 - "exports"
Cohesion: 0.40
Nodes (5): exports, ./components/*, ./globals.css, ./hooks/*, ./lib/*

### Community 119 - "Review Focus"
Cohesion: 0.22
Nodes (8): Customer Frontend Maintainability Implementation Plan, Global Constraints, Review Focus, Task 2: Make standalone typechecking and root test execution real, Task 3: Centralize test cleanup and shared intake fixtures mechanically, Task 6: Extract stable-ID sequential upload lifecycle with TDD, Task 8: Disable streaming Stop when no handler exists, Task 9: Run the complete customer acceptance matrix and final diff review

### Community 120 - "scripts"
Cohesion: 0.50
Nodes (4): scripts, format, lint, typecheck

### Community 122 - "policy.py"
Cohesion: 0.09
Nodes (56): AskedQuestion, IntakeState, Question, QuestionRecord, _review_prompt(), answer_choices(), answer_kind(), ask_for() (+48 more)

### Community 123 - "TurnContext"
Cohesion: 0.10
Nodes (13): quick_answer(), TurnContext, IntakeGraph, _invitation(), grounded_analysis(), grounded_review(), ScriptedIntakeModel, test_graph_budget_uses_the_pinned_choice_and_timeout() (+5 more)

### Community 124 - "find_candidates"
Cohesion: 0.25
Nodes (12): Candidate, _add(), find_candidates(), _overlaps(), test_amount_forms(), test_arabic_indic_amount_not_confused_with_phone(), test_dates_absolute_and_weekday(), test_dedupes_repeated_values() (+4 more)

### Community 125 - "admin.py"
Cohesion: 0.07
Nodes (32): audit(), catalog(), _check_provider(), ChoiceInput, embedding_switch(), ModelOptions, models(), ProbeInput (+24 more)

### Community 126 - "guardrails.py"
Cohesion: 0.12
Nodes (17): normalize_phone(), parse_amount(), resolve_date(), _safe_date(), _iso(), normalize_value(), check_draft(), _citation_findings() (+9 more)

### Community 127 - "embedder.py"
Cohesion: 0.19
Nodes (4): ConfiguredEmbedder, _Store, _Store, test_configured_embedder_follows_the_current_setting()

### Community 128 - "test_workspace_schema.py"
Cohesion: 0.29
Nodes (8): assert_customer_schema(), LegacySchemaError, _nullable(), _table_exists(), upgrade_workspace_schema(), test_fresh_schema_passes_the_customer_check(), test_intake_sessions_without_a_customer_phone_stop_startup(), test_nullable_ticket_phone_stops_startup_with_a_reset_instruction()

### Community 129 - "intake/model.py"
Cohesion: 0.08
Nodes (33): ImageInput, ModelCall, ModelUnavailable, _analysis_prompt(), _bounded_context(), _guard_size(), IntakeModel, validate() (+25 more)

### Community 131 - "intake.py"
Cohesion: 0.15
Nodes (22): ask_question(), create_session(), _credentials(), _dump(), get_session(), post_message(), read_attachment(), remove_attachment() (+14 more)

### Community 132 - "Review Focus"
Cohesion: 0.18
Nodes (11): api(), settings(), Review Focus, Task 1: Establish the safety baseline and remove tracked Graphify cache contents, Task 2: Delete the superseded architecture HTML after a fresh reference check, Task 3: Remove confirmed stale local runtime state and the duplicate screenshot, Task 4: Repair only current setup and processing documentation, Task 5: Restrict Docker build context without deleting installed dependencies (+3 more)

### Community 133 - "EmbeddingBatch"
Cohesion: 0.09
Nodes (11): EmbeddingBatch, SearchResult, _nonnegative_number(), OpenAICompatibleEmbedder, _ordered_vectors(), _response_cost(), Embeddings, test_lock_serializes_operations_and_submit_waits_for_inflight_search() (+3 more)

### Community 134 - "test_draft_model.py"
Cohesion: 0.33
Nodes (7): response_payload(), run_provider_pipeline(), send(), search_response(), test_empty_choices_escalates_and_keeps_paid_response_usage(), test_failed_response_id_is_deduplicated_against_earlier_success(), test_other_conversion_value_errors_remain_unexpected()

### Community 135 - "Ticket flow charts"
Cohesion: 0.20
Nodes (9): 1. Outcome, 2. Scope, 4. Which step is open, 5. Language, 6. How a result becomes the charts, 7. Sentences, 8. Tests, 9. Files (+1 more)

### Community 136 - "recover_intake_processing"
Cohesion: 0.36
Nodes (7): recover_intake_processing(), dispatch_intake(), test_review_to_employee_handoff(), _submit(), test_committed_but_unscheduled_ticket_survives_recovery(), test_failed_outcome_save_preserves_placeholder_and_reconciles_counts(), test_processing_ticket_rejects_review()

### Community 137 - "types.py"
Cohesion: 0.05
Nodes (30): UnsupportedOperation, _capabilities(), OpenRouterChat, OpenRouterProvider, _per_million(), provider_errors(), ProviderRegistry, UnknownProvider (+22 more)

### Community 138 - "5. Backend design"
Cohesion: 0.25
Nodes (6): 5.1 Dead-code cleanup, 5.2 Extraction ownership, 5.3 Knowledge-service boundary, 5.4 Shared backend boundaries, 5.5 Confirmed backend defect fixes, 5. Backend design

### Community 139 - "pipeline/contracts.py"
Cohesion: 0.09
Nodes (32): Candidates, ClassificationResult, ClassifierOutput, Classifier, build_order_check(), build_questions(), build_state(), category_criteria() (+24 more)

### Community 140 - "Global Constraints"
Cohesion: 0.29
Nodes (7): Global Constraints, Task 1: Sentence catalog, Task 4: Mermaid source, Task 5: Draw the charts on the ticket page, Ticket Flow Charts Implementation Plan, SentenceId, FlowStepId

### Community 141 - "passage-reading.ts"
Cohesion: 0.39
Nodes (6): concisePassage(), directionOf(), keepLine(), PassageReading, sentences(), refund

### Community 142 - "ExtractedField"
Cohesion: 0.23
Nodes (20): Decision, ExtractedField, LookupResult, decide(), empty_ticket_decision(), merge_reasons(), note_for(), _unique() (+12 more)

### Community 144 - "probe.py"
Cohesion: 0.11
Nodes (13): _chat(), _classify(), _describe(), _draft(), _embed(), _extract(), _intake(), _ProbeAnswer (+5 more)

### Community 148 - "components-ai-thought-chain.tsx"
Cohesion: 0.11
Nodes (18): Status, StatusIcon(), statusStyles, StepContext, StepContextType, ThoughtChain(), ThoughtChainContent(), ThoughtChainItem() (+10 more)

### Community 149 - "4. Backend design"
Cohesion: 0.33
Nodes (6): recent(), 4.2 Processes, 4.4 Call-site changes, 4.5 Prices for estimates, 4.6 Reporting API, 4. Backend design

### Community 151 - "test_taxonomy.py"
Cohesion: 0.19
Nodes (6): most_urgent(), priority_rank(), TaxonomyError, taxonomy(), test_priority_helpers(), test_rejects_unknown_team()

### Community 152 - "test_dbapi_commit_handoff_arbitrates_cancellation"
Cohesion: 0.47
Nodes (4): test_dbapi_commit_handoff_arbitrates_cancellation(), gate(), gate_before_dbapi(), gate_inside_dbapi()

### Community 153 - "Global Constraints"
Cohesion: 0.33
Nodes (5): Global Constraints, Intake Chat UI Implementation Plan, Task 2: Put screenshots inside the composer, Task 3: Apply the workspace chat styles, Task 4: Check the page in the browser

### Community 154 - "ZainCash support: architecture and ticket flow {#support-overview}"
Cohesion: 0.50
Nodes (3): 1 · System architecture {#system-architecture}, 2 · Ticket flow {#ticket-flow}, ZainCash support: architecture and ticket flow {#support-overview}

### Community 155 - "IntakePage.test.tsx"
Cohesion: 0.06
Nodes (41): Task 7: Bilingual customer chat, screenshots and reviewed submission, copy(), parseJson(), readError(), FakeXHR, session, UploadResult, IntakeRequestError (+33 more)

### Community 156 - "employee-frontend/src/components/theme-provider.tsx"
Cohesion: 0.23
Nodes (11): disableTransitionsTemporarily(), getSystemTheme(), isEditableTarget(), isTheme(), ResolvedTheme, Theme, THEME_VALUES, ThemeProvider() (+3 more)

### Community 157 - "_ModelUsage"
Cohesion: 0.13
Nodes (8): _error_cost(), _has_response_usage(), _ModelUsage, _number(), DraftContext, Task 3: Ticket-scoped investigation and all eight tools, Task 11: Use Draft-Model-Specific Fallback Token Prices, Task 6: Record drafting model calls with latency

### Community 161 - "Customer phone identity design"
Cohesion: 0.13
Nodes (14): Backend, Canonical phone format, Customer phone identity design, Data model, Decisions, Employee API, employee-frontend, Error handling (+6 more)

### Community 162 - "index_deadlines"
Cohesion: 0.40
Nodes (3): index_deadlines(), settings(), expire_during_embedding()

### Community 164 - "7. Customer frontend design"
Cohesion: 0.50
Nodes (4): 7.1 Verification and cleanup, 7.2 Runtime contracts and persisted operations, 7.4 Controller, chat, and tests, 7. Customer frontend design

### Community 167 - "build_pipeline"
Cohesion: 0.10
Nodes (32): build_pipeline(), ConfigError, run_batch(), FakeJevRunnable, FakeStructuredLLM, ScriptedChat, _settings(), test_builds_jev_pipeline_with_injected_clients() (+24 more)

### Community 168 - "Customer Conversation Intake Implementation Plan"
Cohesion: 0.25
Nodes (8): Completion audit — 2026-10-18, Customer Conversation Intake Implementation Plan, Execution conventions and repository baseline, File map and dependency order, Global Constraints, Plan review and execution handoff, Review Focus, Spec coverage and acceptance map

### Community 172 - "test_submission.py"
Cohesion: 0.32
Nodes (4): _payload(), test_concurrent_submit_dispatches_once(), test_second_request_id_reuses_the_approved_review(), test_submission_replay_creates_one_ticket()

## Ambiguous Edges - Review These
- `Fraud Report` → `Plan 1 Live Smoke`  [AMBIGUOUS]
  README.md · relation: conceptually_related_to

## Knowledge Gaps
- **83 isolated node(s):** `zaincash-support`, `@base-ui/react`, `@fontsource-variable/plus-jakarta-sans`, `@fontsource/tajawal`, `@tailwindcss/vite` (+78 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 1239 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **33 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Settings` connect `Settings` to `EmbeddingError`, `intake/model.py`, `ActiveModels`, `db/models.py`, `pytest`, `cli.py`, `EmbeddingBatch`, `test_draft_model.py`, `Review Focus`, `types.py`, `test_workspace_schema.py`, `main.py`, `pipeline/contracts.py`, `Embedder`, `_ModelUsage`, `test_draft_tools.py`, `test_kb_service.py`, `index_deadlines`, `IntakeRepository`, `build_pipeline`, `intake/repository.py`, `attachments.py`, `test_llm.py`, `knowledge.py`, `httpx`, `pipeline/graph.py`, `test_catalog.py`, `test_workspace_api.py`, `Step`, `make_output`, `test_rag_api.py`, `fact`, `submission.py`, `resolver.py`, `test_cli.py`, `RAG drafting verification — 2026-10-17`, `KnowledgeError`, `test_final_fix_handoff.py`, `demo-readiness.md`, `policy.py`, `TurnContext`, `embedder.py`?**
  _High betweenness centrality (0.103) - this node is a cross-community bridge._
- **Are the 55 inferred relationships involving `Settings` (e.g. with `_command_settings()` and `_run_in_memory()`) actually correct?**
  _`Settings` has 55 INFERRED edges - model-reasoned connections that need verification._
- **What connects `zaincash-support`, `@base-ui/react`, `@fontsource-variable/plus-jakarta-sans` to the rest of the system?**
  _83 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `EmbeddingError` be split into smaller, more focused modules?**
  _Cohesion score 0.11564625850340136 - nodes in this community are weakly interconnected._
- **Why does `2. Current state` connect `pipeline/contracts.py` to `Per-model evaluation (quality, system, cost) — design specification`, `Card`, `build_pipeline`, `NewBatchPage.tsx`, `ExtractedField`, `make_output`?**
  _High betweenness centrality (0.073) - this node is a cross-community bridge._
- **Are the 69 inferred relationships involving `Step` (e.g. with `catalog()` and `_check_provider()`) actually correct?**
  _`Step` has 69 INFERRED edges - model-reasoned connections that need verification._

### Low-confidence Hints
_AMBIGUOUS edges — the extractor was unsure. Verify before acting on these._

- **What is the exact relationship between `Fraud Report` and `Plan 1 Live Smoke`?**
  _Edge tagged AMBIGUOUS (relation: conceptually_related_to) - confidence is low._