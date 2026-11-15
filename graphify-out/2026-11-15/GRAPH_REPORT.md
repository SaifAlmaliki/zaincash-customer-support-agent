# Graph Report - zaincash-support  (2026-11-14)

## Corpus Check
- 432 files · ~496,404 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 25 file(s) not represented in the graph (top: (none) 15, .jsonl 4, .css 4)

## Summary
- 4344 nodes · 14753 edges · 186 communities (151 shown, 35 thin omitted)
- Extraction: 85% EXTRACTED · 15% INFERRED · 0% AMBIGUOUS · INFERRED: 2279 edges (avg confidence: 0.93)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `5075511b`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- EmbeddingError
- ActiveModels
- pytest
- batch_jobs.py
- investigation.py
- load_tickets
- Card
- Customer conversation intake for ZainCash support
- lib/types.ts
- IntakeController
- FakeJevRunnable
- make_engine
- employee-frontend/package.json
- QueuePage.tsx
- Support Taxonomy Categories
- ui/package.json
- ModelsPage.tsx
- users-frontend/package.json
- load_taxonomy
- test_draft_guardrails.py
- web/package.json
- test_interview_scenarios.py
- compilerOptions
- employee-frontend/components.json
- EmbeddingError
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
- TurnStore
- ui/components.json
- intake/test_repository.py
- Guided intake interview — design
- Vite Config
- Human Review Gate
- compilerOptions
- workspace-ui.tsx
- compilerOptions
- Human Flag Tool
- Recent Transactions Tool
- Ticket History Tool
- Lookup Transaction Tool
- Search Transactions Tool
- Submit Draft Tool
- Project Root
- parse_document
- intake/repository.py
- contracts.ts
- test_llm.py
- results.py
- use-knowledge-library.ts
- db/models.py
- tasks
- knowledge.py
- ChangeModelDialog.tsx
- IntakePage.tsx
- RagDrafter
- agent-chat.tsx
- locale.tsx
- TicketResultRow
- cli.py
- fake_registry
- jev.py
- PipelineState
- test_workspace_api.py
- test_interview_api.py
- devDependencies
- agent.py
- Plan 3 RAG Drafting Implementation Plan
- ModelChoice
- main.py
- test_rag_api.py
- Guided intake interview verification — 2026-11-13
- context
- AI usage and performance dashboard (`/evaluation`) — design specification
- httpx
- TicketInput
- steps.py
- test_recovery_regressions.py
- EvaluationPage.tsx
- test_workspace_schema.py
- devDependencies
- devDependencies
- tools.py
- ticket-flow.ts
- intake/contracts.py
- compilerOptions
- pipeline/contracts.py
- Per-model evaluation (quality, system, cost) — design specification
- dependencies
- InvalidEvidence
- dependencies
- compilerOptions
- EmbeddingSwitches
- intake/api.ts
- test_final_fix_handoff.py
- normalize
- pydantic
- scripts
- make_ticket
- compilerOptions
- Maintainability and stale-code refactor — design specification
- test_extract_calls.py
- web/tsconfig.json
- employee-frontend/tsconfig.json
- exports
- Review Focus
- scripts
- users-frontend/README.md
- policy.py
- TurnContext
- RAG drafting verification — 2026-10-17
- admin.py
- guardrails.py
- build_tools
- Analysis
- intake/model.py
- openrouter_chat.py
- intake.py
- Admin-managed, model-agnostic pipeline configuration — design specification
- calls.py
- KnowledgeError
- ZainCash Support Workspace
- db/repository.py
- test_admin_api.py
- Customer intake verification — 2026-10-18
- Customer Conversation Intake Implementation Plan
- scripts
- test_cli.py
- lookup.py
- _DatabaseCall
- probe.py
- components-ai-thought-chain.tsx
- test_intake_calls.py
- intake/README.md
- pipeline/graph.py
- demo-readiness.md
- Review Focus
- ZainCash support: architecture and ticket flow {#support-overview}
- IntakePage.test.tsx
- employee-frontend/src/components/theme-provider.tsx
- _ModelUsage
- dependencies
- embedder.py
- taxonomy.py
- Customer phone identity design
- api-entrypoint.sh
- DraftContext
- Synthetic demo readiness
- Ticket flow charts
- build_pipeline
- passage-reading.ts
- 5. Backend design
- ScriptedIntakeModel
- Deviations from the spec (intentional, small)
- test_submission.py
- test_dbapi_commit_handoff_arbitrates_cancellation
- Backend
- index_deadlines
- 10. Verification and acceptance
- FakeXHR
- Global Constraints
- AI Usage and Performance Dashboard Implementation Plan — Part 1 of 2 (backend)
- collapsible.tsx
- setup.ts

## God Nodes (most connected - your core abstractions)
1. `Settings` - 207 edges
2. `Step` - 124 edges
3. `ModelChoice` - 106 edges
4. `KnowledgeService` - 87 edges
5. `fact()` - 81 edges
6. `context()` - 77 edges
7. `ActiveModels` - 76 edges
8. `message()` - 72 edges
9. `useCopy()` - 68 edges
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
- `Details, each shown once` --references--> `progress()`  [INFERRED]
  docs/superpowers/specs/2026-11-13-guided-intake-interview-design.md → backend/app/intake/policy.py

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **Cascade Classification Path** — docs_superpowers_specs_2026_10_07_support_pipeline_design_cascade, docs_superpowers_plans_2026_10_07_plan1_core_pipeline_part2_jev_classifier, docs_superpowers_plans_2026_10_07_plan1_core_pipeline_part2_gemini_classifier, docs_superpowers_plans_2026_10_07_plan1_core_pipeline_part2_cascade_combine, readme_human_approval [EXTRACTED 1.00]
- **Drafting Agent Toolset** — backend_app_pipeline_runner_lookup_transaction, backend_app_pipeline_runner_search_transactions, backend_app_pipeline_runner_get_customer_recent_transactions, backend_app_pipeline_runner_get_customer_ticket_history, backend_app_pipeline_runner_check_service_status, backend_app_pipeline_runner_search_knowledge_base, backend_app_pipeline_runner_flag_for_human, backend_app_pipeline_runner_submit_draft [EXTRACTED 1.00]
- **Ticket Processing Stage Flow** — backend_app_pipeline_runner_prepare, backend_app_pipeline_runner_jev_classify, backend_app_pipeline_runner_gemini_classify, backend_app_pipeline_runner_extract, backend_app_pipeline_runner_lookup, backend_app_pipeline_runner_decide, backend_app_pipeline_runner_draft [EXTRACTED 1.00]

## Communities (186 total, 35 thin omitted)

### Community 0 - "EmbeddingError"
Cohesion: 0.12
Nodes (36): OpenRouterEmbedder, embedder_for(), item(), response_payload(), settings(), test_33_inputs_are_batched_and_each_batch_maps_its_own_indexes(), respond(), test_billed_batch_cost_survives_cancellation_without_cross_call_leakage() (+28 more)

### Community 1 - "ActiveModels"
Cohesion: 0.10
Nodes (27): ActiveModels, batch_concurrency(), _local_pipeline(), ticket_timeout_s(), test_batch_concurrency_stays_within_bounds(), test_cloud_runs_keep_the_ticket_timeout(), test_local_drafts_get_room_for_their_longer_deadline(), test_local_extract_alone_extends_the_ticket_timeout() (+19 more)

### Community 2 - "pytest"
Cohesion: 0.15
Nodes (45): DraftModelInfo, test_contracts_reject_extra_keys(), test_datetimes_must_be_timezone_aware(), answer(), call(), Checker, draft_state(), Knowledge (+37 more)

### Community 3 - "batch_jobs.py"
Cohesion: 0.15
Nodes (18): save_outcomes(), TicketOutcome, TicketExecution, outcome_from_state(), one(), summarize(), outcome_to_dict(), outcome_to_row() (+10 more)

### Community 4 - "investigation.py"
Cohesion: 0.15
Nodes (15): parse_dt(), TxnRecord, DraftToolInputError, _datetime(), _days(), _field(), _involves(), _phone() (+7 more)

### Community 5 - "load_tickets"
Cohesion: 0.22
Nodes (11): load_jsonl(), load_tickets(), _rows(), test_csv_with_bom_and_missing_columns(), test_duplicate_external_ids_keep_first(), test_invalid_phone_names_the_row(), test_json_object_without_ids(), test_jsonl_fixture_loads() (+3 more)

### Community 6 - "Card"
Cohesion: 0.14
Nodes (49): Task 5: Extract presentational DocumentList and KnowledgeReadiness components, Task 12: Locale parity test and translated Runs pages, 6.4 Focused view extraction, Card(), CardContent(), CardHeader(), CardTitle(), AuditList() (+41 more)

### Community 7 - "Customer conversation intake for ZainCash support"
Cohesion: 0.06
Nodes (32): 10. Verification and acceptance criteria, 11. Delivery and review, 1. Outcome and agreed requirements, 2. Current implementation and integration points, 3. Approach and boundaries, 4. Conversation state and turn flow, 5. Facts, evidence, and readiness, 6. Language and screenshot behavior (+24 more)

### Community 8 - "lib/types.ts"
Cohesion: 0.05
Nodes (42): Employee Frontend Maintainability Implementation Plan, Global Constraints, Review Focus, Task 1: Remove reference-verified dead exports, components, and the Mermaid dependency, Task 2: Migrate active TicketFlow coverage, then retire the legacy trace/chart cluster, Task 4: Extract and test the pure queue projection, Task 6: Repair ExtractedField fixtures and make standalone typecheck real, Task 7: Repair employee README paths/test-count guidance and run final acceptance (+34 more)

### Community 9 - "IntakeController"
Cohesion: 0.14
Nodes (14): HTTP contract (implemented in Tasks 4–5), Task 6: Customer API client and resumable UI state, Task 1: Cleanup-first removal of reference-verified dead code and dependencies, Task 7: Preserve resume-unavailable state across `startNew`, Task 7: Intake app data layer — phone helper, contracts, API, controller, Task 7: Customer frontend data layer, ControllerState, emptyState() (+6 more)

### Community 10 - "FakeJevRunnable"
Cohesion: 0.08
Nodes (31): CredentialCheck, CredentialChecker, DegradedCredentialChecker, _finite_nonnegative(), _get(), JevCredentialChecker, FakeJevRunnable, _Runnable (+23 more)

### Community 11 - "make_engine"
Cohesion: 0.09
Nodes (24): initialize_database(), make_engine(), make_sessionmaker(), reset_db(), _accepts(), create_app(), intake_failed(), lifespan() (+16 more)

### Community 12 - "employee-frontend/package.json"
Cohesion: 0.06
Nodes (30): @base-ui/react, class-variance-authority, cn, eslint, @eslint/js, eslint-plugin-react-hooks, eslint-plugin-react-refresh, @fontsource/tajawal (+22 more)

### Community 14 - "QueuePage.tsx"
Cohesion: 0.15
Nodes (40): Task 3: Split RunDetailPage and introduce bounded run-result loading, Task 16: Model detail, confusion matrix and predictions drawer, Task 10: Employee app — customer page and ticket header link, Task 15: Ticket cost table and AI timeline, 6.4 Visible to all employees, 5.1 Data access, 7. Testing, Confidence() (+32 more)

### Community 15 - "Support Taxonomy Categories"
Cohesion: 0.21
Nodes (22): lookup, Account KYC, Account & Security, Agent Dispute, Agent Network, App Bug, Bill Payment, Card Issue (+14 more)

### Community 16 - "ui/package.json"
Cohesion: 0.08
Nodes (24): @base-ui/react, class-variance-authority, cn, eslint, @eslint/js, eslint-plugin-react-hooks, eslint-plugin-react-refresh, @fontsource/tajawal (+16 more)

### Community 17 - "ModelsPage.tsx"
Cohesion: 0.18
Nodes (20): App(), CustomerPage, EvaluationPage, InsightsPage, KnowledgePage, ModelsPage, NewBatchPage, QueuePage (+12 more)

### Community 18 - "users-frontend/package.json"
Cohesion: 0.08
Nodes (23): turbo, devDependencies, prettier, prettier-plugin-tailwindcss, turbo, typescript, engines, node (+15 more)

### Community 19 - "load_taxonomy"
Cohesion: 0.11
Nodes (24): build_graph(), PipelineDeps, InMemoryTransactionRepo, load_taxonomy(), tax(), FakeClassifier, intake_client(), pipeline() (+16 more)

### Community 20 - "test_draft_guardrails.py"
Cohesion: 0.14
Nodes (26): requests_credentials(), check(), state(), test_aggregation_is_deduplicated_and_has_no_state_side_effects(), test_amount_occurrences_keep_their_own_currency_and_sign(), test_avoid_sharing_warning_does_not_excuse_a_later_request(), test_candidate_prompt_limit_does_not_hide_later_ungrounded_references(), test_candidate_transactions_cannot_authorize_reply_evidence() (+18 more)

### Community 21 - "web/package.json"
Cohesion: 0.08
Nodes (25): clsx, jsdom, tailwind-merge, @testing-library/user-event, @workspace/ui, eslint, @eslint/js, eslint-plugin-react-hooks (+17 more)

### Community 22 - "test_interview_scenarios.py"
Cohesion: 0.26
Nodes (9): analyze_calls(), Chat, source_of(), summary(), test_complete_report_goes_straight_to_review(), test_no_reference_number_still_gives_a_complete_report(), test_vague_report_is_interviewed_into_a_complete_ticket(), updates() (+1 more)

### Community 23 - "compilerOptions"
Cohesion: 0.08
Nodes (23): compilerOptions, allowArbitraryExtensions, allowImportingTsExtensions, erasableSyntaxOnly, jsx, lib, module, moduleDetection (+15 more)

### Community 24 - "employee-frontend/components.json"
Cohesion: 0.09
Nodes (21): aliases, components, hooks, lib, ui, utils, iconLibrary, menuAccent (+13 more)

### Community 25 - "EmbeddingError"
Cohesion: 0.11
Nodes (9): EmbeddingBatch, EmbeddingError, _nonnegative_number(), _ordered_vectors(), _response_cost(), _percentile(), NamedEmbedder, test_lock_serializes_operations_and_submit_waits_for_inflight_search() (+1 more)

### Community 26 - "compilerOptions"
Cohesion: 0.09
Nodes (22): compilerOptions, allowArbitraryExtensions, allowImportingTsExtensions, erasableSyntaxOnly, jsx, lib, module, moduleDetection (+14 more)

### Community 27 - "web/src/components/theme-provider.tsx"
Cohesion: 0.16
Nodes (13): App(), controller, disableTransitionsTemporarily(), getSystemTheme(), isEditableTarget(), isTheme(), ResolvedTheme, Theme (+5 more)

### Community 28 - "Settings"
Cohesion: 0.08
Nodes (16): Settings, test_blank_intake_model_is_rejected(), test_non_positive_image_limit_is_rejected(), test_relative_upload_directory_is_rooted_in_the_repository(), test_anthropic_model_selects_the_draft_model_only(), test_defaults(), test_draft_token_prices_follow_the_selected_draft_model(), test_drafting_configuration_cannot_bypass_hard_limits() (+8 more)

### Community 29 - "Classify and Extract Prompts"
Cohesion: 0.33
Nodes (7): extract, gemini_classify, Pipeline Graph Orchestration, jev_classify, prepare, GeminiClassifier, JevClassifier

### Community 30 - "test_draft_tools.py"
Cohesion: 0.12
Nodes (28): IncidentRow, settings(), test_all_eight_tools_and_seven_parallel_calls_execute_only_six(), test_context_copies_input_and_rejects_raising_hard_call_limit(), test_database_faults_remain_distinct_and_record_paid_search_cost(), test_discovered_ref_can_be_inspected_but_not_promoted_to_match(), test_exact_and_fuzzy_queries_are_scoped_and_never_confirm_candidates(), test_exact_reference_still_requires_customer_and_excludes_future() (+20 more)

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

### Community 38 - "TurnStore"
Cohesion: 0.14
Nodes (18): OperationClaim, IntakeMessageRow, RevisionConflict, load_messages(), _message(), session_view(), turn_context(), _jsonable() (+10 more)

### Community 39 - "ui/components.json"
Cohesion: 0.10
Nodes (19): aliases, components, hooks, lib, ui, utils, iconLibrary, menuAccent (+11 more)

### Community 40 - "intake/test_repository.py"
Cohesion: 0.09
Nodes (27): AttachmentStore, _display_name(), Credentials, SessionView, ImageRejected, NotOwned, IntakeRepository, IntakeService (+19 more)

### Community 41 - "Guided intake interview — design"
Cohesion: 0.07
Nodes (28): 2. API contract, 3. Chat screen, 4. Review card, Actions, Additional issues, Approach, Composer hints, Copy (+20 more)

### Community 43 - "Human Review Gate"
Cohesion: 0.25
Nodes (4): support CLI, Support Workspace UI Plan, Review API, Workspace UI Verification

### Community 44 - "compilerOptions"
Cohesion: 0.12
Nodes (16): compilerOptions, allowImportingTsExtensions, erasableSyntaxOnly, lib, module, moduleDetection, noEmit, noFallthroughCasesInSwitch (+8 more)

### Community 46 - "workspace-ui.tsx"
Cohesion: 0.08
Nodes (54): 6.1 Route and access, 6.2 Page, 6.3 Change dialog, 6.5 Text and direction, 6. Employee-frontend design, 5.2 Page structure, WorkspaceProvider(), ConfirmDialog() (+46 more)

### Community 47 - "compilerOptions"
Cohesion: 0.12
Nodes (16): compilerOptions, allowImportingTsExtensions, erasableSyntaxOnly, lib, module, moduleDetection, noEmit, noFallthroughCasesInSwitch (+8 more)

### Community 57 - "parse_document"
Cohesion: 0.09
Nodes (33): _append_chunks(), _check_extracted_size(), _combining_only(), DocumentParseError, _is_ltr(), _is_rtl(), _line_text(), _logical_page_text() (+25 more)

### Community 58 - "intake/repository.py"
Cohesion: 0.12
Nodes (24): Receipt, ReviewSnapshot, IntakeAttachmentRow, IntakeOperationRow, IntakeSubmissionRow, IntakeError, InvalidCustomerPhone, OperationConflict (+16 more)

### Community 59 - "contracts.ts"
Cohesion: 0.17
Nodes (34): Task 5: Add complete dependency-free API and persisted-session guards, createIntakeApi(), ANSWER_KINDS, CHOICES, FACT_STATUSES, finiteNonnegative(), invalid(), isRecord() (+26 more)

### Community 60 - "test_llm.py"
Cohesion: 0.13
Nodes (17): make_draft_model(), make_gemini_llm(), response_payload(), run_provider_pipeline(), send(), search_response(), test_empty_choices_escalates_and_keeps_paid_response_usage(), test_failed_response_id_is_deduplicated_against_earlier_success() (+9 more)

### Community 61 - "results.py"
Cohesion: 0.09
Nodes (22): get_session(), get_result(), list_results(), read_intake_attachment(), review_result(), ReviewInput, health(), insights() (+14 more)

### Community 62 - "use-knowledge-library.ts"
Cohesion: 0.23
Nodes (14): acceptIndexRequest(), canRequestIndex(), PendingIndexes, persistPendingIndexes(), pollKnowledge(), refresh(), stop(), PollOptions (+6 more)

### Community 63 - "db/models.py"
Cohesion: 0.08
Nodes (28): Base, CustomerRow, ReviewRow, TransactionRow, init_db(), IntakeSessionRow, EmbeddingSwitchRow, ModelSettingAuditRow (+20 more)

### Community 64 - "tasks"
Cohesion: 0.11
Nodes (18): dependsOn, inputs, outputs, cache, persistent, dependsOn, dependsOn, $schema (+10 more)

### Community 65 - "knowledge.py"
Cohesion: 0.10
Nodes (26): session(), _configured(), delete_document(), download_document(), index_document(), list_chunks(), list_documents(), _require_provider() (+18 more)

### Community 66 - "ChangeModelDialog.tsx"
Cohesion: 0.09
Nodes (37): Admin model configuration — employee frontend implementation plan, Backend API contract used here, File structure, Global Constraints, Review Focus, Task 1: API types, admin session and admin requests, Task 2: Strings, the AI locality chip, run models and the batch switch message, Task 3: Model choice logic and the change dialog (+29 more)

### Community 67 - "IntakePage.tsx"
Cohesion: 0.07
Nodes (45): Global Constraints, Intake Chat UI Implementation Plan, Task 1: Put the summary and receipt in the thread, Task 2: Put screenshots inside the composer, Task 3: Apply the workspace chat styles, Task 4: Check the page in the browser, Task 8: Intake app UI — phone screen, profile chip, change number, receipt, 4. Components (+37 more)

### Community 68 - "RagDrafter"
Cohesion: 0.06
Nodes (30): DraftResult, RagDrafter, Drafter, DraftExecutionError, NullDrafter, UnavailableDrafter, draft(), test_real_search_fault_carries_safe_draft_execution_error() (+22 more)

### Community 69 - "agent-chat.tsx"
Cohesion: 0.17
Nodes (22): Task 8: Chat screen — instant bubble, typing, reasons, quick replies, composer hints, AgentChat, AgentChatProps, AgentMessage, AssistantText(), AttachedFile, AttachedImage, ChatStatus (+14 more)

### Community 70 - "locale.tsx"
Cohesion: 0.07
Nodes (39): Task 8: Employee evidence panel and processing state, Task 9: Employee app — required phone, queue identity and search, batch entry, base, mixed, originalLocale, LanguageToggle(), embed, originalLocale (+31 more)

### Community 71 - "TicketResultRow"
Cohesion: 0.11
Nodes (34): _filter(), usage_summary(), usage_ticket_calls(), usage_tickets(), TicketResultRow, AiCallRow, _by_model(), _by_process() (+26 more)

### Community 72 - "cli.py"
Cohesion: 0.11
Nodes (18): _command_settings(), ingest_kb_cmd(), init_db_cmd(), Mode, run_batch_cmd(), _run_in_memory(), _run_with_db(), seed_db_cmd() (+10 more)

### Community 73 - "fake_registry"
Cohesion: 0.13
Nodes (13): CatalogCache, step_catalog(), ProviderRegistry, UnknownProvider, fake_registry(), FakeProvider, BrokenStatusProvider, test_a_provider_whose_status_check_raises_is_listed_as_unreachable() (+5 more)

### Community 74 - "jev.py"
Cohesion: 0.07
Nodes (37): Candidates, ClassificationResult, ClassifierOutput, Classifier, build_order_check(), build_questions(), build_state(), category_criteria() (+29 more)

### Community 75 - "PipelineState"
Cohesion: 0.27
Nodes (4): _Nodes, PipelineState, Task 10: Disable Paid Whole-Node Retry for Jev Classification, 3. What the employee sees

### Community 76 - "test_workspace_api.py"
Cohesion: 0.11
Nodes (20): review_payload(), start_run(), test_batch_and_queue_expose_real_results(), test_batch_failure_is_isolated_and_conflicting_ids_rejected(), test_customer_profile_lists_the_latest_result_of_each_ticket(), test_progress_counts_only_durable_results_after_save_failure(), fail_one_save(), test_result_list_paginates_filters_and_run_id() (+12 more)

### Community 77 - "test_interview_api.py"
Cohesion: 0.21
Nodes (19): analyze_calls(), ask(), complete_without_reference(), opening(), opening_with_amount(), reference_answer(), send(), start() (+11 more)

### Community 79 - "devDependencies"
Cohesion: 0.12
Nodes (16): devDependencies, eslint, @eslint/js, eslint-plugin-react-hooks, eslint-plugin-react-refresh, globals, prettier, prettier-plugin-tailwindcss (+8 more)

### Community 81 - "Plan 3 RAG Drafting Implementation Plan"
Cohesion: 0.20
Nodes (10): Completion and review record — 2026-10-17, Execution handoff, File map and shared interfaces, Global Constraints, Plan 3 RAG Drafting Implementation Plan, Plan self-review, Review Focus, Task 6: API/CLI indexing and persisted citation projection (+2 more)

### Community 82 - "ModelChoice"
Cohesion: 0.09
Nodes (26): prices_for(), probe(), ModelChoice, ProbeResult, Step, probe_call(), test_start_updates_the_cache_without_reloading_from_the_database(), test_env_defaults_keep_their_prices() (+18 more)

### Community 83 - "main.py"
Cohesion: 0.11
Nodes (19): _safe_dispatch(), get_run(), list_runs(), start_run(), BatchInput, RunRow, recover(), run_job() (+11 more)

### Community 84 - "test_rag_api.py"
Cohesion: 0.13
Nodes (21): client(), evidence_client(), pipeline(), submit(), test_actual_guardrail_failure_is_separate_from_reply(), test_concurrent_index_requests_share_active_work(), test_disabled_or_missing_provider_stores_without_indexing(), test_explicit_retry_tags_search_and_chunk_pagination() (+13 more)

### Community 85 - "Guided intake interview verification — 2026-11-13"
Cohesion: 0.20
Nodes (9): Arabic at 390×844, starting from the vague message, English at 1280×900, with the complete message, Final automated checks, Guided intake interview verification — 2026-11-13, Live browser run, Live probe output (facts only), Live transfer probe, Observations (+1 more)

### Community 86 - "context"
Cohesion: 0.15
Nodes (55): Question, merge_analysis(), assess_readiness(), choose_question(), field_is_resolved(), field_needs_question(), context(), fact() (+47 more)

### Community 87 - "AI usage and performance dashboard (`/evaluation`) — design specification"
Cohesion: 0.14
Nodes (13): 10. Phase 2 (for reference, not designed here), 1. Outcome and success criteria, 2. Current state, 3. Decisions, 5.1 Page, 5.2 Components and data, 5.3 Text and direction, 5. Frontend design (+5 more)

### Community 88 - "httpx"
Cohesion: 0.11
Nodes (14): OllamaProvider, _provider(), _tags_handler(), test_catalog_lists_installed_models_with_reported_capabilities(), handler(), test_chat_model_sets_the_configured_context_window(), test_chat_model_targets_the_configured_server(), test_embedder_uses_openai_compatible_endpoint_without_dimensions() (+6 more)

### Community 90 - "steps.py"
Cohesion: 0.24
Nodes (10): draft_timeout_s(), eligibility(), env_defaults(), intake_timeout_s(), _settings(), test_eligibility(), test_env_defaults_match_todays_settings(), test_env_overrides_for_draft_and_intake() (+2 more)

### Community 91 - "test_recovery_regressions.py"
Cohesion: 0.40
Nodes (9): command(), create(), test_actual_app_restart_reconciles_failed_placeholder(), test_failed_review_retry_cannot_reopen_submitted_session(), test_original_payload_identity_survives_sanitization(), test_publication_failure_is_retryable_without_restart(), test_receipt_reference_is_preserved(), test_stale_attempt_audit_is_retained_once_with_attempt_identity() (+1 more)

### Community 92 - "EvaluationPage.tsx"
Cohesion: 0.11
Nodes (25): Global Constraints, Per-model Evaluation Implementation Plan — Part 3 of 3 (frontend, translations, verification), Task 13: Evaluation types, API client, formatters, copy and report import, Task 15: Provenance, headline metrics, comparison table and empty state, Task 17: Run dialog, progress, page assembly, route and styles, Task 18: Documentation, full verification and manual check, AI Usage and Performance Dashboard Implementation Plan — Part 2 of 2 (frontend, docs, verification), Deviation from the spec (+17 more)

### Community 93 - "test_workspace_schema.py"
Cohesion: 0.29
Nodes (8): assert_customer_schema(), LegacySchemaError, _nullable(), _table_exists(), upgrade_workspace_schema(), test_fresh_schema_passes_the_customer_check(), test_intake_sessions_without_a_customer_phone_stop_startup(), test_nullable_ticket_phone_stops_startup_with_a_reset_instruction()

### Community 94 - "devDependencies"
Cohesion: 0.11
Nodes (19): devDependencies, eslint, @eslint/js, eslint-plugin-react-hooks, eslint-plugin-react-refresh, globals, jsdom, @tailwindcss/vite (+11 more)

### Community 95 - "devDependencies"
Cohesion: 0.17
Nodes (12): devDependencies, eslint, @eslint/js, eslint-plugin-react-hooks, eslint-plugin-react-refresh, globals, tailwindcss, @types/node (+4 more)

### Community 96 - "tools.py"
Cohesion: 0.12
Nodes (15): DraftAlreadySubmitted, DraftToolLimit, _bounded(), visit(), guarded(), invoke(), _Flag, _History (+7 more)

### Community 97 - "ticket-flow.ts"
Cohesion: 0.07
Nodes (56): Global Constraints, Task 1: Sentence catalog, Task 2: Which step is open, Task 3: Received, produced, and drafting events, Task 4: Mermaid source, Task 5: Draw the charts on the ticket page, Ticket Flow Charts Implementation Plan, buildTicketFlow() (+48 more)

### Community 98 - "intake/contracts.py"
Cohesion: 0.14
Nodes (23): quick_answer(), Analysis, Attachment, _aware(), CustomerReview, EvidenceRef, Fact, IntakeModel (+15 more)

### Community 99 - "compilerOptions"
Cohesion: 0.14
Nodes (13): compilerOptions, jsx, lib, module, moduleResolution, noEmit, paths, skipLibCheck (+5 more)

### Community 100 - "pipeline/contracts.py"
Cohesion: 0.11
Nodes (28): LLMUnavailable, StructuredLLM, FieldPick, NormalizedTicket, FieldExtractor, _field(), fill_gaps(), finalize() (+20 more)

### Community 101 - "Per-model evaluation (quality, system, cost) — design specification"
Cohesion: 0.20
Nodes (9): 1. Outcome and success criteria, 3. Decisions, 5.3 Text and direction, 5.4 Runs pages, 5.5 Import format, 5. Employee-frontend design, 6. Error handling, 8. Out of scope (+1 more)

### Community 102 - "dependencies"
Cohesion: 0.12
Nodes (16): dependencies, @base-ui/react, class-variance-authority, cn, @fontsource/tajawal, @fontsource-variable/plus-jakarta-sans, lucide-react, motion (+8 more)

### Community 103 - "InvalidEvidence"
Cohesion: 0.09
Nodes (36): ReviewText, canonical_digits(), normalize_reported_date(), InvalidEvidence, _apply(), _check_reference(), _compact(), _complete_normalization() (+28 more)

### Community 104 - "dependencies"
Cohesion: 0.20
Nodes (10): dependencies, @base-ui/react, class-variance-authority, cn, @fontsource/tajawal, @fontsource-variable/plus-jakarta-sans, react, react-dom (+2 more)

### Community 105 - "compilerOptions"
Cohesion: 0.17
Nodes (11): compilerOptions, jsx, lib, module, moduleResolution, outDir, skipLibCheck, strict (+3 more)

### Community 106 - "EmbeddingSwitches"
Cohesion: 0.24
Nodes (3): EmbeddingSwitches, _view(), Task 4: The Models page, navigation and route

### Community 107 - "intake/api.ts"
Cohesion: 0.13
Nodes (17): Task 4: Make pending operations discriminated and use one request identity, IntakeApi, parseJson(), readError(), UploadResult, INTAKE_FALLBACK_MESSAGE, IntakeRequestError, Activity (+9 more)

### Community 108 - "test_final_fix_handoff.py"
Cohesion: 0.12
Nodes (20): process_batch(), assert_completed_evidence(), faulty_knowledge(), read(), outer_deadlines(), PaidEmbeddings, runner_env(), build() (+12 more)

### Community 109 - "normalize"
Cohesion: 0.17
Nodes (18): sanitize_intake_text(), detect_arabizi(), fold_arabic(), has_latin_mix(), _latin_words(), normalize(), sanitize_for_storage(), mask_cards() (+10 more)

### Community 110 - "pydantic"
Cohesion: 0.23
Nodes (6): CitationSource, _Draft, draft_evidence(), _Guardrail, _TraceModel, _validated()

### Community 111 - "scripts"
Cohesion: 0.25
Nodes (8): scripts, build, dev, format, lint, preview, test, typecheck

### Community 112 - "make_ticket"
Cohesion: 0.29
Nodes (17): make_output(), make_ticket(), _deps(), _run(), test_concurrency_is_limited(), test_draft_node_never_retries_or_restarts_paid_work(), test_drafter_reasons_escalate(), test_empty_batch() (+9 more)

### Community 113 - "compilerOptions"
Cohesion: 0.29
Nodes (6): compilerOptions, module, moduleResolution, skipLibCheck, strict, target

### Community 114 - "Maintainability and stale-code refactor — design specification"
Cohesion: 0.18
Nodes (10): 1. Outcome and success criteria, 2. Audit baseline, 3. Selected approach and sequence, 4. Boundaries and non-goals, 8.1 Approved deletions, 8.2 Docker and documentation, 8.3 Graphify outputs, 8. Repository hygiene and current documentation (+2 more)

### Community 115 - "test_extract_calls.py"
Cohesion: 0.20
Nodes (8): raw(), _Chat, _FailingExtractor, llm(), _S, test_each_attempt_is_recorded(), test_failed_parse_cost_reaches_the_ticket(), test_unknown_price_and_local_sources()

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
Cohesion: 0.12
Nodes (15): Customer Frontend Maintainability Implementation Plan, Global Constraints, Review Focus, Task 2: Make standalone typechecking and root test execution real, Task 3: Centralize test cleanup and shared intake fixtures mechanically, Task 6: Extract stable-ID sequential upload lifecycle with TDD, Task 8: Disable streaming Stop when no handler exists, Task 9: Run the complete customer acceptance matrix and final diff review (+7 more)

### Community 120 - "scripts"
Cohesion: 0.50
Nodes (4): scripts, format, lint, typecheck

### Community 122 - "policy.py"
Cohesion: 0.11
Nodes (39): AskedQuestion, IntakeState, PendingQuestion, ProgressItem, answer_choices(), answer_kind(), ask_for(), ask_once_keys() (+31 more)

### Community 123 - "TurnContext"
Cohesion: 0.11
Nodes (18): QuestionRecord, TurnContext, TurnResult, IntakeGraph, _invitation(), test_graph_budget_uses_the_pinned_choice_and_timeout(), choice_for(), test_pin_failure_is_reported_as_model_unavailable() (+10 more)

### Community 124 - "RAG drafting verification — 2026-10-17"
Cohesion: 0.20
Nodes (12): ingest(), support_test(), Artifacts, servers and remaining concerns, Citation IDs and provider evidence, Commands and automated verification — historical Task 8, Corpus and actual retrieval, Current final verification and review closure, Environment and isolation (+4 more)

### Community 125 - "admin.py"
Cohesion: 0.12
Nodes (23): audit(), catalog(), _check_provider(), ChoiceInput, embedding_switch(), ModelOptions, models(), _priced() (+15 more)

### Community 126 - "guardrails.py"
Cohesion: 0.08
Nodes (33): Candidate, _add(), find_candidates(), normalize_phone(), _overlaps(), parse_amount(), resolve_date(), _safe_date() (+25 more)

### Community 127 - "build_tools"
Cohesion: 0.11
Nodes (6): DraftSubmission, build_tools(), retrieve(), _error_cost(), Global Constraints, Repository Hygiene Maintainability Implementation Plan

### Community 128 - "Analysis"
Cohesion: 0.19
Nodes (16): _amount(), analyze(), complete_conversation(), _dated(), _message(), _opening(), _png(), _review() (+8 more)

### Community 129 - "intake/model.py"
Cohesion: 0.09
Nodes (34): ImageInput, ModelCall, ModelUnavailable, _analysis_prompt(), _bounded_context(), _guard_size(), IntakeModel, validate() (+26 more)

### Community 130 - "openrouter_chat.py"
Cohesion: 0.16
Nodes (3): DraftProviderResponseError, OpenRouterChat, Task 2: OpenRouter and TypeSafe providers, registry, generic embedder

### Community 131 - "intake.py"
Cohesion: 0.15
Nodes (22): ask_question(), create_session(), _credentials(), _dump(), get_session(), post_message(), read_attachment(), remove_attachment() (+14 more)

### Community 132 - "Admin-managed, model-agnostic pipeline configuration — design specification"
Cohesion: 0.12
Nodes (16): api(), Review Focus, Task 1: Establish the safety baseline and remove tracked Graphify cache contents, Task 2: Delete the superseded architecture HTML after a fresh reference check, Task 3: Remove confirmed stale local runtime state and the duplicate screenshot, Task 4: Repair only current setup and processing documentation, Task 5: Restrict Docker build context without deleting installed dependencies, Task 6: Regenerate current Graphify outputs as the final mutating task (+8 more)

### Community 133 - "calls.py"
Cohesion: 0.07
Nodes (38): OpenAICompatibleEmbedder, StructuredChatLLM, AiCall, call_context(), CallContext, cost_for(), count(), embed_process() (+30 more)

### Community 134 - "KnowledgeError"
Cohesion: 0.16
Nodes (7): DocumentNotFoundError, KnowledgeError, KnowledgeExecutionError, ErrorEmbedder, test_search_unexpected_fault_logs_only_safe_type(), fail_search(), Task 14: Preserve Safe Knowledge 503s and Log Only Unexpected Diagnostic Types

### Community 135 - "ZainCash Support Workspace"
Cohesion: 0.25
Nodes (8): Current capability boundaries, Data source, Modular file map, Open the right project, Run locally, shadcn conventions, Workflow, ZainCash Support Workspace

### Community 136 - "db/repository.py"
Cohesion: 0.08
Nodes (32): get_customer(), customer_phone_or_none(), InvalidPhone, normalize_customer_phone(), TicketRow, create_run(), finish_run(), load_incidents() (+24 more)

### Community 137 - "test_admin_api.py"
Cohesion: 0.05
Nodes (37): with_catalog_prices(), UnsupportedOperation, _capabilities(), OpenRouterProvider, _per_million(), provider_errors(), TypeSafeProvider, Capability (+29 more)

### Community 138 - "Customer intake verification — 2026-10-18"
Cohesion: 0.25
Nodes (6): Browser handoff, Customer intake verification — 2026-10-18, Final automated checks, Live vision and paired review, Repaired gaps and regression evidence, Review decisions and remaining limits

### Community 139 - "Customer Conversation Intake Implementation Plan"
Cohesion: 0.25
Nodes (8): Completion audit — 2026-10-18, Customer Conversation Intake Implementation Plan, Execution conventions and repository baseline, File map and dependency order, Global Constraints, Plan review and execution handoff, Review Focus, Spec coverage and acceptance map

### Community 140 - "scripts"
Cohesion: 0.25
Nodes (8): scripts, build, dev, format, lint, preview, test, typecheck

### Community 141 - "test_cli.py"
Cohesion: 0.16
Nodes (8): test_config_error_exits_2(), boom(), test_ingest_directory_is_deterministic_and_duplicate_is_free(), test_ingest_disabled_configuration_never_calls_provider(), test_ingest_failure_exit_and_retry_stored(), test_ingest_invalid_source_does_not_stop_other_files(), test_ingest_limits_batch_without_partial_side_effects(), test_settings_validation_is_safe_field_diagnostic_exit_2()

### Community 142 - "lookup.py"
Cohesion: 0.26
Nodes (14): _ex(), _match(), test_ambiguous_then_disambiguated_by_counterpart(), test_amount_and_date_mismatch(), test_fraud_reference_missing_from_the_ledger_is_not_found(), test_fraud_search_by_phone_amount_and_date(), test_fraud_with_a_real_reference_is_matched(), test_fraud_without_a_cited_payment_stays_not_applicable() (+6 more)

### Community 143 - "_DatabaseCall"
Cohesion: 0.07
Nodes (16): Embedder, Passage, SearchResult, TextChunk, _abandoned(), _check_deadline(), _consume(), _DatabaseCall (+8 more)

### Community 144 - "probe.py"
Cohesion: 0.13
Nodes (13): _chat(), _classify(), _describe(), _draft(), _embed(), _extract(), _intake(), _ProbeAnswer (+5 more)

### Community 148 - "components-ai-thought-chain.tsx"
Cohesion: 0.15
Nodes (15): Status, StatusIcon(), statusStyles, StepContext, StepContextType, ThoughtChain(), ThoughtChainContent(), ThoughtChainItem() (+7 more)

### Community 149 - "test_intake_calls.py"
Cohesion: 0.23
Nodes (9): ensure_customers(), add_intake_calls(), intake_calls(), link_intake_calls(), entry(), test_errors_rejections_and_legacy_entries(), test_intake_call_without_cost_uses_estimate_or_unknown(), test_provider_cost_entry() (+1 more)

### Community 151 - "pipeline/graph.py"
Cohesion: 0.11
Nodes (26): Decision, ExtractedField, LookupResult, _default_retry(), _retryable(), _as_date(), _iqd_amount(), match_transaction() (+18 more)

### Community 153 - "Review Focus"
Cohesion: 0.17
Nodes (10): Review Focus, Task 10: Grouped review card with answer buttons, Task 11: Employee label, full gates, live probe and verification record, Task 2: Prompt rules and the `recipient_name` vocabulary, Task 9: Progress strip, 1. Outcome, 2. Scope, 3. Layout (+2 more)

### Community 154 - "ZainCash support: architecture and ticket flow {#support-overview}"
Cohesion: 0.50
Nodes (3): 1 · System architecture {#system-architecture}, 2 · Ticket flow {#ticket-flow}, ZainCash support: architecture and ticket flow {#support-overview}

### Community 155 - "IntakePage.test.tsx"
Cohesion: 0.07
Nodes (35): Task 7: Bilingual customer chat, screenshots and reviewed submission, copy(), @testing-library/react, session, malformed, populated, fakeApi(), review (+27 more)

### Community 156 - "employee-frontend/src/components/theme-provider.tsx"
Cohesion: 0.23
Nodes (11): disableTransitionsTemporarily(), getSystemTheme(), isEditableTarget(), isTheme(), ResolvedTheme, Theme, THEME_VALUES, ThemeProvider() (+3 more)

### Community 157 - "_ModelUsage"
Cohesion: 0.21
Nodes (7): _error_cost(), _has_response_usage(), _ModelUsage, _number(), Task 11: Use Draft-Model-Specific Fallback Token Prices, Task 6: Record drafting model calls with latency, 4.4 Call-site changes

### Community 158 - "dependencies"
Cohesion: 0.33
Nodes (6): dependencies, clsx, react, react-dom, tailwind-merge, @workspace/ui

### Community 159 - "embedder.py"
Cohesion: 0.19
Nodes (4): ConfiguredEmbedder, _Store, _Store, test_configured_embedder_follows_the_current_setting()

### Community 160 - "taxonomy.py"
Cohesion: 0.22
Nodes (5): most_urgent(), priority_rank(), TaxonomyError, test_priority_helpers(), test_rejects_unknown_team()

### Community 161 - "Customer phone identity design"
Cohesion: 0.22
Nodes (8): Canonical phone format, Customer phone identity design, Decisions, employee-frontend, Error handling, Intent, Out of scope, Testing

### Community 164 - "DraftContext"
Cohesion: 0.22
Nodes (3): _Execution, DraftContext, Task 3: Ticket-scoped investigation and all eight tools

### Community 165 - "Synthetic demo readiness"
Cohesion: 0.50
Nodes (4): Evidence by layer, Known limitations and remaining work, Repeatable local walkthrough, Synthetic demo readiness

### Community 166 - "Ticket flow charts"
Cohesion: 0.20
Nodes (9): 1. Outcome, 2. Scope, 4. Which step is open, 5. Language, 6. How a result becomes the charts, 7. Sentences, 8. Tests, 9. Files (+1 more)

### Community 167 - "build_pipeline"
Cohesion: 0.10
Nodes (25): SqlTransactionRepo, Sample, build_pipeline(), ConfigError, model_ids(), run_batch(), FakeStructuredLLM, ScriptedChat (+17 more)

### Community 168 - "passage-reading.ts"
Cohesion: 0.39
Nodes (6): concisePassage(), directionOf(), keepLine(), PassageReading, sentences(), refund

### Community 169 - "5. Backend design"
Cohesion: 0.29
Nodes (5): 5.1 Dead-code cleanup, 5.3 Knowledge-service boundary, 5.4 Shared backend boundaries, 5.5 Confirmed backend defect fixes, 5. Backend design

### Community 171 - "Deviations from the spec (intentional, small)"
Cohesion: 0.29
Nodes (6): Deviations from the spec (intentional, small), Global Constraints, Per-model Evaluation Implementation Plan — Part 2 of 3 (evaluation engine), Task 11: `support eval` CLI and v2 export, Task 7: Metrics, Task 9: Runner, request validation and cost estimate

### Community 172 - "test_submission.py"
Cohesion: 0.32
Nodes (4): _payload(), test_concurrent_submit_dispatches_once(), test_second_request_id_reuses_the_approved_review(), test_submission_replay_creates_one_ticket()

### Community 173 - "test_dbapi_commit_handoff_arbitrates_cancellation"
Cohesion: 0.47
Nodes (4): test_dbapi_commit_handoff_arbitrates_cancellation(), gate(), gate_before_dbapi(), gate_inside_dbapi()

### Community 174 - "Backend"
Cohesion: 0.33
Nodes (6): Backend, Data model, Employee API, Existing data, Intake, Ticket write paths

### Community 179 - "index_deadlines"
Cohesion: 0.40
Nodes (3): index_deadlines(), settings(), expire_during_embedding()

### Community 180 - "10. Verification and acceptance"
Cohesion: 0.40
Nodes (5): 10. Verification and acceptance, Backend, Customer frontend, Employee frontend, Repository and Docker

## Ambiguous Edges - Review These
- `Fraud Report` → `Plan 1 Live Smoke`  [AMBIGUOUS]
  README.md · relation: conceptually_related_to

## Knowledge Gaps
- **83 isolated node(s):** `zaincash-support`, `@base-ui/react`, `@fontsource-variable/plus-jakarta-sans`, `@fontsource/tajawal`, `@tailwindcss/vite` (+78 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 1265 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **35 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Settings` connect `Settings` to `EmbeddingError`, `intake/model.py`, `ActiveModels`, `pytest`, `calls.py`, `db/repository.py`, `test_admin_api.py`, `make_engine`, `test_cli.py`, `_DatabaseCall`, `load_taxonomy`, `test_intake_calls.py`, `EmbeddingError`, `test_draft_tools.py`, `embedder.py`, `test_kb_service.py`, `Synthetic demo readiness`, `build_pipeline`, `intake/test_repository.py`, `index_deadlines`, `intake/repository.py`, `test_llm.py`, `db/models.py`, `RagDrafter`, `TicketResultRow`, `cli.py`, `fake_registry`, `jev.py`, `test_workspace_api.py`, `agent.py`, `ModelChoice`, `main.py`, `test_rag_api.py`, `context`, `httpx`, `steps.py`, `test_workspace_schema.py`, `test_final_fix_handoff.py`, `TurnContext`, `RAG drafting verification — 2026-10-17`, `admin.py`?**
  _High betweenness centrality (0.116) - this node is a cross-community bridge._
- **Are the 60 inferred relationships involving `Settings` (e.g. with `_command_settings()` and `_run_in_memory()`) actually correct?**
  _`Settings` has 60 INFERRED edges - model-reasoned connections that need verification._
- **What connects `zaincash-support`, `@base-ui/react`, `@fontsource-variable/plus-jakarta-sans` to the rest of the system?**
  _83 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `EmbeddingError` be split into smaller, more focused modules?**
  _Cohesion score 0.12323232323232323 - nodes in this community are weakly interconnected._
- **Why does `2. Current state` connect `jev.py` to `Per-model evaluation (quality, system, cost) — design specification`, `Card`, `build_pipeline`, `load_taxonomy`, `pipeline/graph.py`, `EvaluationPage.tsx`?**
  _High betweenness centrality (0.072) - this node is a cross-community bridge._
- **Are the 79 inferred relationships involving `Step` (e.g. with `catalog()` and `_check_provider()`) actually correct?**
  _`Step` has 79 INFERRED edges - model-reasoned connections that need verification._

### Low-confidence Hints
_AMBIGUOUS edges — the extractor was unsure. Verify before acting on these._

- **What is the exact relationship between `Fraud Report` and `Plan 1 Live Smoke`?**
  _Edge tagged AMBIGUOUS (relation: conceptually_related_to) - confidence is low._