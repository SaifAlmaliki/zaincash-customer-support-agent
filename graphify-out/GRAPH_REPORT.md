# Graph Report - zaincash-support  (2026-11-14)

## Corpus Check
- 407 files · ~467,635 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 25 file(s) not represented in the graph (top: (none) 15, .jsonl 4, .css 4)

## Summary
- 4080 nodes · 13558 edges · 159 communities (131 shown, 28 thin omitted)
- Extraction: 85% EXTRACTED · 15% INFERRED · 0% AMBIGUOUS · INFERRED: 2053 edges (avg confidence: 0.93)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `ec68b426`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- agent.py
- Step
- pytest
- TurnStore
- investigation.py
- test_catalog.py
- Card
- Customer conversation intake for ZainCash support
- lib/api.ts
- IntakeController
- FakeJevRunnable
- test_rag_api.py
- employee-frontend/package.json
- QueuePage.tsx
- Support Taxonomy Categories
- ui/package.json
- ModelsPage.tsx
- users-frontend/package.json
- make_output
- test_draft_guardrails.py
- web/package.json
- test_interview_scenarios.py
- compilerOptions
- employee-frontend/components.json
- Step
- compilerOptions
- web/src/components/theme-provider.tsx
- EmbeddingError
- Classify and Extract Prompts
- test_draft_tools.py
- Pipeline Design Spec
- Batch Runner
- Drafting Plan Concepts
- test_kb_service.py
- search_knowledge_base
- web/components.json
- NewBatchPage.tsx
- ui/components.json
- Settings
- Guided intake interview — design
- Vite Config
- Human Review Gate
- compilerOptions
- PipelineState
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
- pytest
- contracts.ts
- fact
- build_tools
- lib/types.ts
- IntakePage.tsx
- tasks
- knowledge.py
- ChangeModelDialog.tsx
- IntakePage.tsx
- PipelineState
- main.py
- httpx
- test_handoff.py
- config.py
- create_app
- normalize.py
- KnowledgePage
- test_workspace_api.py
- test_interview_api.py
- devDependencies
- test_admin_api.py
- tools.py
- factory.py
- Ticket flow charts
- Per-model evaluation (quality, system, cost) — design specification
- Guided intake interview verification — 2026-11-13
- Embedder
- TicketInput
- 5. Backend design
- Global Constraints
- Customer intake chat layout
- IndexJobs
- Credentials
- devDependencies
- devDependencies
- fakes.py
- ticket-flow.ts
- InvalidEvidence
- compilerOptions
- collapsible.tsx
- dependencies
- evidence.py
- dependencies
- compilerOptions
- canReview
- intake/api.ts
- test_final_fix_handoff.py
- scripts
- lookup.py
- compilerOptions
- Maintainability and stale-code refactor — design specification
- web/tsconfig.json
- employee-frontend/tsconfig.json
- exports
- Review Focus
- scripts
- users-frontend/README.md
- policy.py
- TurnContext
- admin.py
- guardrails.py
- intake/model.py
- test_llm.py
- intake.py
- Review Focus
- _DatabaseCall
- types.py
- jev.py
- intake/repository.py
- cli.py
- resolver.py
- probe.py
- components-ai-thought-chain.tsx
- intake/README.md
- taxonomy.py
- create_app
- create_app
- ZainCash support: architecture and ticket flow {#support-overview}
- IntakePage.test.tsx
- employee-frontend/src/components/theme-provider.tsx
- agent.py
- TicketRow
- EmbeddingSwitches
- Customer phone identity design
- api-entrypoint.sh
- openrouter_chat.py
- test_workspace_schema.py
- build_pipeline
- support_test
- intake/contracts.py
- Deviations from the spec (intentional, small)
- test_submission.py

## God Nodes (most connected - your core abstractions)
1. `Settings` - 189 edges
2. `Step` - 108 edges
3. `ModelChoice` - 91 edges
4. `KnowledgeService` - 85 edges
5. `ActiveModels` - 74 edges
6. `fact()` - 73 edges
7. `context()` - 68 edges
8. `useCopy()` - 68 edges
9. `message()` - 63 edges
10. `IntakeController` - 59 edges

## Surprising Connections (you probably didn't know these)
- `Repeatable local walkthrough` --references--> `Settings`  [INFERRED]
  docs/demo-readiness.md → backend/app/config.py
- `Ticket write paths` --references--> `upsert_tickets()`  [INFERRED]
  docs/superpowers/specs/2026-11-13-customer-phone-identity-design.md → backend/app/db/repository.py
- `Existing data` --references--> `upgrade_workspace_schema()`  [INFERRED]
  docs/superpowers/specs/2026-11-13-customer-phone-identity-design.md → backend/app/db/workspace_schema.py
- `Details, each shown once` --references--> `progress()`  [INFERRED]
  docs/superpowers/specs/2026-11-13-guided-intake-interview-design.md → backend/app/intake/policy.py
- `Progress strip` --references--> `progress()`  [INFERRED]
  docs/superpowers/specs/2026-11-13-guided-intake-interview-design.md → backend/app/intake/policy.py

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **Cascade Classification Path** — docs_superpowers_specs_2026_10_07_support_pipeline_design_cascade, docs_superpowers_plans_2026_10_07_plan1_core_pipeline_part2_jev_classifier, docs_superpowers_plans_2026_10_07_plan1_core_pipeline_part2_gemini_classifier, docs_superpowers_plans_2026_10_07_plan1_core_pipeline_part2_cascade_combine, readme_human_approval [EXTRACTED 1.00]
- **Drafting Agent Toolset** — backend_app_pipeline_runner_lookup_transaction, backend_app_pipeline_runner_search_transactions, backend_app_pipeline_runner_get_customer_recent_transactions, backend_app_pipeline_runner_get_customer_ticket_history, backend_app_pipeline_runner_check_service_status, backend_app_pipeline_runner_search_knowledge_base, backend_app_pipeline_runner_flag_for_human, backend_app_pipeline_runner_submit_draft [EXTRACTED 1.00]
- **Ticket Processing Stage Flow** — backend_app_pipeline_runner_prepare, backend_app_pipeline_runner_jev_classify, backend_app_pipeline_runner_gemini_classify, backend_app_pipeline_runner_extract, backend_app_pipeline_runner_lookup, backend_app_pipeline_runner_decide, backend_app_pipeline_runner_draft [EXTRACTED 1.00]

## Communities (159 total, 28 thin omitted)

### Community 0 - "agent.py"
Cohesion: 0.11
Nodes (7): DraftAlreadySubmitted, DraftToolLimit, _bounded(), visit(), guarded(), invoke(), _json()

### Community 1 - "Step"
Cohesion: 0.08
Nodes (26): StructuredChatLLM, ActiveModels, make_draft_model(), make_gemini_llm(), model_ids(), batch_concurrency(), _local_pipeline(), ticket_timeout_s() (+18 more)

### Community 2 - "pytest"
Cohesion: 0.20
Nodes (36): answer(), call(), draft_state(), script(), submit(), pipeline(), submit(), drafter() (+28 more)

### Community 3 - "TurnStore"
Cohesion: 0.14
Nodes (14): OperationClaim, RevisionConflict, progress(), sanitize_intake_text(), _jsonable(), TurnStore, fail_once(), repo() (+6 more)

### Community 4 - "investigation.py"
Cohesion: 0.13
Nodes (15): parse_dt(), TxnRecord, _datetime(), _days(), _field(), _involves(), _phone(), _phones() (+7 more)

### Community 5 - "test_catalog.py"
Cohesion: 0.18
Nodes (8): CatalogCache, step_catalog(), FakeProvider, BrokenStatusProvider, test_a_provider_whose_status_check_raises_is_listed_as_unreachable(), test_catalog_errors_stay_per_provider_and_cache_respects_ttl(), test_classify_catalog_only_offers_typesafe(), test_step_catalog_filters_and_marks_unknown()

### Community 6 - "Card"
Cohesion: 0.12
Nodes (47): Global Constraints, Per-model Evaluation Implementation Plan — Part 3 of 3 (frontend, translations, verification), Task 12: Locale parity test and translated Runs pages, Task 15: Provenance, headline metrics, comparison table and empty state, Task 17: Run dialog, progress, page assembly, route and styles, Task 18: Documentation, full verification and manual check, 5.2 Page structure, Confidence() (+39 more)

### Community 7 - "Customer conversation intake for ZainCash support"
Cohesion: 0.06
Nodes (31): 10. Verification and acceptance criteria, 11. Delivery and review, 1. Outcome and agreed requirements, 2. Current implementation and integration points, 3. Approach and boundaries, 4. Conversation state and turn flow, 5. Facts, evidence, and readiness, 6. Language and screenshot behavior (+23 more)

### Community 8 - "lib/api.ts"
Cohesion: 0.07
Nodes (41): Admin model configuration — employee frontend implementation plan, Backend API contract used here, File structure, Global Constraints, Review Focus, Task 1: API types, admin session and admin requests, Task 2: Strings, the AI locality chip, run models and the batch switch message, Task 3: Model choice logic and the change dialog (+33 more)

### Community 9 - "IntakeController"
Cohesion: 0.15
Nodes (13): Task 6: Customer API client and resumable UI state, Task 1: Cleanup-first removal of reference-verified dead code and dependencies, Task 7: Preserve resume-unavailable state across `startNew`, Task 7: Intake app data layer — phone helper, contracts, API, controller, Task 7: Customer frontend data layer, ControllerState, emptyState(), IntakeController (+5 more)

### Community 10 - "FakeJevRunnable"
Cohesion: 0.09
Nodes (25): CredentialCheck, DegradedCredentialChecker, _finite_nonnegative(), _get(), JevCredentialChecker, test_blank_intake_model_is_rejected(), test_contracts_reject_extra_keys(), test_datetimes_must_be_timezone_aware() (+17 more)

### Community 11 - "test_rag_api.py"
Cohesion: 0.11
Nodes (23): Embeddings, client(), evidence_client(), kb_env(), test_actual_guardrail_failure_is_separate_from_reply(), test_concurrent_index_requests_share_active_work(), test_disabled_or_missing_provider_stores_without_indexing(), test_explicit_retry_tags_search_and_chunk_pagination() (+15 more)

### Community 12 - "employee-frontend/package.json"
Cohesion: 0.06
Nodes (30): @base-ui/react, class-variance-authority, cn, eslint, @eslint/js, eslint-plugin-react-hooks, eslint-plugin-react-refresh, @fontsource/tajawal (+22 more)

### Community 14 - "QueuePage.tsx"
Cohesion: 0.13
Nodes (51): Task 3: Split RunDetailPage and introduce bounded run-result loading, Task 5: Extract presentational DocumentList and KnowledgeReadiness components, Task 16: Model detail, confusion matrix and predictions drawer, Task 10: Employee app — customer page and ticket header link, Task 9: Employee app — required phone, queue identity and search, batch entry, 6.4 Visible to all employees, 5.1 Data access, 7. Testing (+43 more)

### Community 15 - "Support Taxonomy Categories"
Cohesion: 0.21
Nodes (22): lookup, Account KYC, Account & Security, Agent Dispute, Agent Network, App Bug, Bill Payment, Card Issue (+14 more)

### Community 16 - "ui/package.json"
Cohesion: 0.08
Nodes (24): @base-ui/react, class-variance-authority, cn, eslint, @eslint/js, eslint-plugin-react-hooks, eslint-plugin-react-refresh, @fontsource/tajawal (+16 more)

### Community 17 - "ModelsPage.tsx"
Cohesion: 0.08
Nodes (42): App(), CustomerPage, EvaluationPage, InsightsPage, KnowledgePage, ModelsPage, NewBatchPage, QueuePage (+34 more)

### Community 18 - "users-frontend/package.json"
Cohesion: 0.08
Nodes (23): turbo, devDependencies, prettier, prettier-plugin-tailwindcss, turbo, typescript, engines, node (+15 more)

### Community 19 - "make_output"
Cohesion: 0.09
Nodes (42): build_graph(), PipelineDeps, InMemoryTransactionRepo, load_taxonomy(), tax(), FakeClassifier, make_output(), pipeline() (+34 more)

### Community 20 - "test_draft_guardrails.py"
Cohesion: 0.12
Nodes (32): LookupResult, outcome_to_dict(), outcome_to_row(), requests_credentials(), make_ticket(), check(), state(), test_aggregation_is_deduplicated_and_has_no_state_side_effects() (+24 more)

### Community 21 - "web/package.json"
Cohesion: 0.05
Nodes (41): clsx, jsdom, tailwind-merge, @testing-library/jest-dom, @testing-library/react, @testing-library/user-event, @workspace/ui, dependencies (+33 more)

### Community 22 - "test_interview_scenarios.py"
Cohesion: 0.31
Nodes (9): analyze_calls(), Chat, source_of(), summary(), test_complete_report_goes_straight_to_review(), test_no_reference_number_still_gives_a_complete_report(), test_vague_report_is_interviewed_into_a_complete_ticket(), updates() (+1 more)

### Community 23 - "compilerOptions"
Cohesion: 0.08
Nodes (23): compilerOptions, allowArbitraryExtensions, allowImportingTsExtensions, erasableSyntaxOnly, jsx, lib, module, moduleDetection (+15 more)

### Community 24 - "employee-frontend/components.json"
Cohesion: 0.09
Nodes (21): aliases, components, hooks, lib, ui, utils, iconLibrary, menuAccent (+13 more)

### Community 25 - "Step"
Cohesion: 0.07
Nodes (36): ModelSettingAuditRow, ModelSettingRow, probe(), _iso(), ModelSettingsStore, ModelChoice, ProbeResult, Step (+28 more)

### Community 26 - "compilerOptions"
Cohesion: 0.09
Nodes (22): compilerOptions, allowArbitraryExtensions, allowImportingTsExtensions, erasableSyntaxOnly, jsx, lib, module, moduleDetection (+14 more)

### Community 27 - "web/src/components/theme-provider.tsx"
Cohesion: 0.10
Nodes (19): App(), controller, disableTransitionsTemporarily(), getSystemTheme(), isEditableTarget(), isTheme(), ResolvedTheme, Theme (+11 more)

### Community 28 - "EmbeddingError"
Cohesion: 0.08
Nodes (42): EmbeddingError, _nonnegative_number(), OpenRouterEmbedder, _ordered_vectors(), _response_cost(), _percentile(), NamedEmbedder, embedder_for() (+34 more)

### Community 29 - "Classify and Extract Prompts"
Cohesion: 0.33
Nodes (7): extract, gemini_classify, Pipeline Graph Orchestration, jev_classify, prepare, GeminiClassifier, JevClassifier

### Community 30 - "test_draft_tools.py"
Cohesion: 0.08
Nodes (30): EmbeddingBatch, LateEmbedder, ErrorEmbedder, settings(), test_all_eight_tools_and_seven_parallel_calls_execute_only_six(), test_database_faults_remain_distinct_and_record_paid_search_cost(), test_discovered_ref_can_be_inspected_but_not_promoted_to_match(), test_exact_and_fuzzy_queries_are_scoped_and_never_confirm_candidates() (+22 more)

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
Cohesion: 0.09
Nodes (41): KnowledgeChunk, KnowledgeService, FakeEmbedder, GatedEmbedder, PaidEmbedder, embedder(), count_chunks(), test_category_filters_include_general_policies_and_validate_tags() (+33 more)

### Community 36 - "web/components.json"
Cohesion: 0.10
Nodes (19): aliases, components, hooks, lib, ui, utils, iconLibrary, menuAccent (+11 more)

### Community 38 - "NewBatchPage.tsx"
Cohesion: 0.12
Nodes (23): 6.1 Route and access, 6.2 Page, 6.3 Change dialog, 6. Employee-frontend design, readReport(), TicketIdentity(), exampleTickets, NewBatchPage() (+15 more)

### Community 39 - "ui/components.json"
Cohesion: 0.10
Nodes (19): aliases, components, hooks, lib, ui, utils, iconLibrary, menuAccent (+11 more)

### Community 40 - "Settings"
Cohesion: 0.08
Nodes (13): Settings, test_relative_upload_directory_is_rooted_in_the_repository(), test_anthropic_model_selects_the_draft_model_only(), test_defaults(), test_draft_token_prices_follow_the_selected_draft_model(), test_drafting_configuration_cannot_bypass_hard_limits(), test_drafting_limits_load_from_environment(), test_env_overrides() (+5 more)

### Community 41 - "Guided intake interview — design"
Cohesion: 0.07
Nodes (28): 2. API contract, 3. Chat screen, 4. Review card, Actions, Additional issues, Approach, Backend (pytest, guarded `support_test`), Composer hints (+20 more)

### Community 43 - "Human Review Gate"
Cohesion: 0.25
Nodes (4): support CLI, Support Workspace UI Plan, Review API, Workspace UI Verification

### Community 44 - "compilerOptions"
Cohesion: 0.12
Nodes (16): compilerOptions, allowImportingTsExtensions, erasableSyntaxOnly, lib, module, moduleDetection, noEmit, noFallthroughCasesInSwitch (+8 more)

### Community 46 - "PipelineState"
Cohesion: 0.23
Nodes (5): _Nodes, PipelineState, Task 10: Disable Paid Whole-Node Retry for Jev Classification, 3. What the employee sees, 5.5 Confirmed backend defect fixes

### Community 47 - "compilerOptions"
Cohesion: 0.12
Nodes (16): compilerOptions, allowImportingTsExtensions, erasableSyntaxOnly, lib, module, moduleDetection, noEmit, noFallthroughCasesInSwitch (+8 more)

### Community 48 - "AI usage and performance dashboard (`/evaluation`) — design specification"
Cohesion: 0.11
Nodes (18): recent(), 10. Phase 2 (for reference, not designed here), 1. Outcome and success criteria, 2. Current state, 3. Decisions, 4.2 Processes, 4.5 Prices for estimates, 4.6 Reporting API (+10 more)

### Community 57 - "parse_document"
Cohesion: 0.11
Nodes (27): TextChunk, _append_chunks(), _check_extracted_size(), DocumentParseError, parse_document(), _parse_pdf(), _error_cost(), make_pdf() (+19 more)

### Community 58 - "pytest"
Cohesion: 0.09
Nodes (35): AttachmentStore, ImageInput, IntakeSessionRow, ImageRejected, IntakeError, InvalidCustomerPhone, NotOwned, OperationConflict (+27 more)

### Community 59 - "contracts.ts"
Cohesion: 0.17
Nodes (34): Task 5: Add complete dependency-free API and persisted-session guards, createIntakeApi(), ANSWER_KINDS, CHOICES, FACT_STATUSES, finiteNonnegative(), invalid(), isRecord() (+26 more)

### Community 60 - "fact"
Cohesion: 0.15
Nodes (48): Analysis, EvidenceRef, Fact, merge_analysis(), remove_attachment_evidence(), context(), fact(), image_evidence() (+40 more)

### Community 61 - "build_tools"
Cohesion: 0.13
Nodes (8): DraftToolInputError, build_tools(), flag(), retrieve(), _error_cost(), Backend Maintainability Implementation Plan, Global Constraints, Task 2: Separate Historical Escalation Text from Current Tool Reasons

### Community 62 - "lib/types.ts"
Cohesion: 0.05
Nodes (50): Employee Frontend Maintainability Implementation Plan, Global Constraints, Review Focus, Task 1: Remove reference-verified dead exports, components, and the Mermaid dependency, Task 2: Migrate active TicketFlow coverage, then retire the legacy trace/chart cluster, Task 4: Extract and test the pure queue projection, Task 6: Repair ExtractedField fixtures and make standalone typecheck real, Task 7: Repair employee README paths/test-count guidance and run final acceptance (+42 more)

### Community 63 - "IntakePage.tsx"
Cohesion: 0.17
Nodes (22): Task 8: Chat screen — instant bubble, typing, reasons, quick replies, composer hints, AgentChat, AgentChatProps, AgentMessage, AssistantText(), AttachedFile, AttachedImage, ChatStatus (+14 more)

### Community 64 - "tasks"
Cohesion: 0.11
Nodes (18): dependsOn, inputs, outputs, cache, persistent, dependsOn, dependsOn, $schema (+10 more)

### Community 65 - "knowledge.py"
Cohesion: 0.10
Nodes (26): _configured(), delete_document(), download_document(), index_document(), list_chunks(), list_documents(), _require_provider(), search_knowledge() (+18 more)

### Community 66 - "ChangeModelDialog.tsx"
Cohesion: 0.10
Nodes (38): 6.5 Text and direction, ConfirmDialog(), FilterSelect(), Dialog(), DialogContent(), DialogDescription(), DialogFooter(), DialogHeader() (+30 more)

### Community 67 - "IntakePage.tsx"
Cohesion: 0.11
Nodes (32): Task 1: Put the summary and receipt in the thread, Task 10: Grouped review card with answer buttons, Task 9: Progress strip, 4. Components, users-frontend, quietButton, solidButton, activityText() (+24 more)

### Community 68 - "PipelineState"
Cohesion: 0.07
Nodes (26): DraftResult, Drafter, DraftExecutionError, NullDrafter, draft(), draft(), draft(), 10. Remaining demo roadmap (+18 more)

### Community 69 - "main.py"
Cohesion: 0.06
Nodes (32): get_session(), get_result(), list_results(), read_intake_attachment(), review_result(), get_run(), list_runs(), start_run() (+24 more)

### Community 70 - "httpx"
Cohesion: 0.24
Nodes (12): _provider(), _tags_handler(), test_catalog_lists_installed_models_with_reported_capabilities(), handler(), test_chat_model_sets_the_configured_context_window(), test_chat_model_targets_the_configured_server(), test_embedder_uses_openai_compatible_endpoint_without_dimensions(), test_has_model_is_unknown_when_ollama_is_unreachable_or_unusable() (+4 more)

### Community 71 - "test_handoff.py"
Cohesion: 0.21
Nodes (13): _amount(), analyze(), complete_conversation(), _dated(), _message(), _opening(), _png(), _review() (+5 more)

### Community 73 - "create_app"
Cohesion: 0.27
Nodes (10): create_app(), intake_failed(), _client(), _documents(), test_failed_documents_are_listed(), test_run_start_locks_the_switch_table_before_its_first_write(), test_runs_are_blocked_while_a_switch_runs_and_restart_recovers(), test_switch_is_refused_while_a_run_is_running() (+2 more)

### Community 74 - "normalize.py"
Cohesion: 0.14
Nodes (26): detect_arabizi(), fold_arabic(), has_latin_mix(), _latin_words(), normalize(), sanitize_for_storage(), mask_cards(), _criteria() (+18 more)

### Community 75 - "KnowledgePage"
Cohesion: 0.29
Nodes (11): 6.1 Verification and cleanup, 6.2 Retire the legacy trace/chart cluster, 6.3 Runs and request loading, 6.4 Focused view extraction, 6. Employee frontend design, KnowledgePage(), beginMutation(), deleteDocument() (+3 more)

### Community 76 - "test_workspace_api.py"
Cohesion: 0.13
Nodes (17): review_payload(), start_run(), test_batch_and_queue_expose_real_results(), test_batch_failure_is_isolated_and_conflicting_ids_rejected(), test_customer_profile_lists_the_latest_result_of_each_ticket(), test_progress_counts_only_durable_results_after_save_failure(), fail_one_save(), test_result_list_paginates_filters_and_run_id() (+9 more)

### Community 77 - "test_interview_api.py"
Cohesion: 0.21
Nodes (19): analyze_calls(), ask(), complete_without_reference(), opening(), opening_with_amount(), reference_answer(), send(), start() (+11 more)

### Community 79 - "devDependencies"
Cohesion: 0.12
Nodes (16): devDependencies, eslint, @eslint/js, eslint-plugin-react-hooks, eslint-plugin-react-refresh, globals, prettier, prettier-plugin-tailwindcss (+8 more)

### Community 80 - "test_admin_api.py"
Cohesion: 0.33
Nodes (8): make_client(), build(), test_admin_is_disabled_without_a_token(), test_models_and_catalog(), test_non_ascii_and_blank_tokens_are_rejected(), test_save_rejections_change_nothing(), test_test_save_and_audit(), _tool_chat()

### Community 81 - "tools.py"
Cohesion: 0.16
Nodes (9): DraftSubmission, _Flag, _History, _Input, _Knowledge, _Lookup, _Recent, _Search (+1 more)

### Community 82 - "factory.py"
Cohesion: 0.33
Nodes (7): response_payload(), run_provider_pipeline(), send(), search_response(), test_empty_choices_escalates_and_keeps_paid_response_usage(), test_failed_response_id_is_deduplicated_against_earlier_success(), test_other_conversion_value_errors_remain_unexpected()

### Community 83 - "Ticket flow charts"
Cohesion: 0.20
Nodes (9): 1. Outcome, 2. Scope, 4. Which step is open, 5. Language, 6. How a result becomes the charts, 7. Sentences, 8. Tests, 9. Files (+1 more)

### Community 84 - "Per-model evaluation (quality, system, cost) — design specification"
Cohesion: 0.20
Nodes (9): 1. Outcome and success criteria, 3. Decisions, 5.3 Text and direction, 5.4 Runs pages, 5.5 Import format, 5. Employee-frontend design, 6. Error handling, 8. Out of scope (+1 more)

### Community 85 - "Guided intake interview verification — 2026-11-13"
Cohesion: 0.20
Nodes (9): Arabic at 390×844, starting from the vague message, English at 1280×900, with the complete message, Final automated checks, Guided intake interview verification — 2026-11-13, Live browser run, Live probe output (facts only), Live transfer probe, Observations (+1 more)

### Community 86 - "Embedder"
Cohesion: 0.29
Nodes (3): Embedder, 2. Current state, 4.9 Runtime embedder

### Community 88 - "5. Backend design"
Cohesion: 0.29
Nodes (5): 5.1 Dead-code cleanup, 5.2 Extraction ownership, 5.3 Knowledge-service boundary, 5.4 Shared backend boundaries, 5. Backend design

### Community 89 - "Global Constraints"
Cohesion: 0.33
Nodes (5): Global Constraints, Intake Chat UI Implementation Plan, Task 2: Put screenshots inside the composer, Task 3: Apply the workspace chat styles, Task 4: Check the page in the browser

### Community 90 - "Customer intake chat layout"
Cohesion: 0.33
Nodes (5): 1. Outcome, 2. Scope, 3. Layout, 5. Checks, Customer intake chat layout

### Community 93 - "Credentials"
Cohesion: 0.17
Nodes (12): Credentials, SessionView, IntakeService, command(), create(), test_actual_app_restart_reconciles_failed_placeholder(), test_failed_review_retry_cannot_reopen_submitted_session(), test_original_payload_identity_survives_sanitization() (+4 more)

### Community 94 - "devDependencies"
Cohesion: 0.11
Nodes (19): devDependencies, eslint, @eslint/js, eslint-plugin-react-hooks, eslint-plugin-react-refresh, globals, jsdom, @tailwindcss/vite (+11 more)

### Community 95 - "devDependencies"
Cohesion: 0.17
Nodes (12): devDependencies, eslint, @eslint/js, eslint-plugin-react-hooks, eslint-plugin-react-refresh, globals, tailwindcss, @types/node (+4 more)

### Community 96 - "fakes.py"
Cohesion: 0.10
Nodes (24): LLMUnavailable, FieldPick, FieldExtractor, _field(), fill_gaps(), finalize(), _is_weak(), ExtractedSpan (+16 more)

### Community 97 - "ticket-flow.ts"
Cohesion: 0.07
Nodes (56): Global Constraints, Task 1: Sentence catalog, Task 2: Which step is open, Task 3: Received, produced, and drafting events, Task 4: Mermaid source, Task 5: Draw the charts on the ticket page, Ticket Flow Charts Implementation Plan, buildTicketFlow() (+48 more)

### Community 98 - "InvalidEvidence"
Cohesion: 0.19
Nodes (15): ReviewText, InvalidEvidence, validate(), build_review(), _compact(), _render_value(), _ticket_text(), _tokens() (+7 more)

### Community 99 - "compilerOptions"
Cohesion: 0.14
Nodes (13): compilerOptions, jsx, lib, module, moduleResolution, noEmit, paths, skipLibCheck (+5 more)

### Community 102 - "dependencies"
Cohesion: 0.12
Nodes (16): dependencies, @base-ui/react, class-variance-authority, cn, @fontsource/tajawal, @fontsource-variable/plus-jakarta-sans, lucide-react, motion (+8 more)

### Community 103 - "evidence.py"
Cohesion: 0.18
Nodes (14): canonical_digits(), normalize_reported_date(), _apply(), _check_reference(), _compact(), checked_update(), _newer_correction(), _normalize_precise() (+6 more)

### Community 104 - "dependencies"
Cohesion: 0.20
Nodes (10): dependencies, @base-ui/react, class-variance-authority, cn, @fontsource/tajawal, @fontsource-variable/plus-jakarta-sans, react, react-dom (+2 more)

### Community 105 - "compilerOptions"
Cohesion: 0.17
Nodes (11): compilerOptions, jsx, lib, module, moduleResolution, outDir, skipLibCheck, strict (+3 more)

### Community 106 - "canReview"
Cohesion: 0.50
Nodes (3): Task 8: Employee evidence panel and processing state, canReview(), REVIEWABLE

### Community 107 - "intake/api.ts"
Cohesion: 0.11
Nodes (22): Task 4: Make pending operations discriminated and use one request identity, IntakeApi, INTAKE_FALLBACK_MESSAGE, Activity, fileIdentity(), AnswerKind, AskCommand, Credentials (+14 more)

### Community 108 - "test_final_fix_handoff.py"
Cohesion: 0.10
Nodes (21): Passage, Knowledge, assert_completed_evidence(), faulty_knowledge(), read(), outer_deadlines(), PaidEmbeddings, runner_env() (+13 more)

### Community 111 - "scripts"
Cohesion: 0.25
Nodes (8): scripts, build, dev, format, lint, preview, test, typecheck

### Community 112 - "lookup.py"
Cohesion: 0.16
Nodes (16): ExtractedField, _as_date(), _iqd_amount(), match_transaction(), TransactionRepo, state(), _ex(), _match() (+8 more)

### Community 113 - "compilerOptions"
Cohesion: 0.29
Nodes (6): compilerOptions, module, moduleResolution, skipLibCheck, strict, target

### Community 114 - "Maintainability and stale-code refactor — design specification"
Cohesion: 0.12
Nodes (15): 10. Verification and acceptance, 1. Outcome and success criteria, 2. Audit baseline, 3. Selected approach and sequence, 4. Boundaries and non-goals, 8.1 Approved deletions, 8.2 Docker and documentation, 8.3 Graphify outputs (+7 more)

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
Cohesion: 0.10
Nodes (48): AskedQuestion, IntakeState, Question, answer_choices(), answer_kind(), ask_for(), ask_once_keys(), asked_count() (+40 more)

### Community 123 - "TurnContext"
Cohesion: 0.10
Nodes (15): quick_answer(), TurnContext, TurnResult, IntakeGraph, _invitation(), grounded_analysis(), grounded_review(), ScriptedIntakeModel (+7 more)

### Community 125 - "admin.py"
Cohesion: 0.07
Nodes (31): audit(), catalog(), _check_provider(), ChoiceInput, embedding_switch(), ModelOptions, models(), ProbeInput (+23 more)

### Community 126 - "guardrails.py"
Cohesion: 0.08
Nodes (30): Candidate, _add(), find_candidates(), normalize_phone(), _overlaps(), parse_amount(), resolve_date(), _safe_date() (+22 more)

### Community 129 - "intake/model.py"
Cohesion: 0.11
Nodes (28): ModelCall, ModelUnavailable, _analysis_prompt(), _bounded_context(), _guard_size(), IntakeModel, ModelBudget, _record() (+20 more)

### Community 130 - "test_llm.py"
Cohesion: 0.24
Nodes (9): _llm(), _S, test_draft_model_uses_millisecond_timeout_and_disables_sdk_retries(), test_openrouter_reported_cost_takes_precedence_over_token_estimate(), test_openrouter_retry_budget_is_bounded(), test_openrouter_structured_samples_use_configured_key_and_validate_output(), send(), test_to_sample_exception_and_parse_error() (+1 more)

### Community 131 - "intake.py"
Cohesion: 0.10
Nodes (28): ask_question(), create_session(), _credentials(), _dump(), get_session(), post_message(), read_attachment(), remove_attachment() (+20 more)

### Community 132 - "Review Focus"
Cohesion: 0.17
Nodes (12): api(), Global Constraints, Repository Hygiene Maintainability Implementation Plan, Review Focus, Task 1: Establish the safety baseline and remove tracked Graphify cache contents, Task 2: Delete the superseded architecture HTML after a fresh reference check, Task 3: Remove confirmed stale local runtime state and the duplicate screenshot, Task 4: Repair only current setup and processing documentation (+4 more)

### Community 133 - "_DatabaseCall"
Cohesion: 0.07
Nodes (11): _abandoned(), _check_deadline(), _consume(), _DatabaseCall, _Claim, DocumentNotFoundError, IndexAttemptLostError, KnowledgeError (+3 more)

### Community 137 - "types.py"
Cohesion: 0.05
Nodes (29): OpenAICompatibleEmbedder, UnsupportedOperation, OllamaProvider, _capabilities(), OpenRouterProvider, _per_million(), provider_errors(), ProviderRegistry (+21 more)

### Community 139 - "jev.py"
Cohesion: 0.08
Nodes (33): Candidates, ClassificationResult, ClassifierOutput, NormalizedTicket, _default_retry(), _retryable(), Classifier, build_order_check() (+25 more)

### Community 140 - "intake/repository.py"
Cohesion: 0.13
Nodes (25): _display_name(), Receipt, ReviewSnapshot, IntakeAttachmentRow, IntakeMessageRow, IntakeOperationRow, IntakeSubmissionRow, assert_same_operation() (+17 more)

### Community 142 - "cli.py"
Cohesion: 0.09
Nodes (36): _command_settings(), ingest_kb_cmd(), init_db_cmd(), Mode, run_batch_cmd(), _run_in_memory(), _run_with_db(), seed_db_cmd() (+28 more)

### Community 143 - "resolver.py"
Cohesion: 0.10
Nodes (16): ConfiguredEmbedder, _Store, draft_timeout_s(), eligibility(), env_defaults(), intake_timeout_s(), choice_for(), _Store (+8 more)

### Community 144 - "probe.py"
Cohesion: 0.11
Nodes (13): _chat(), _classify(), _describe(), _draft(), _embed(), _extract(), _intake(), _ProbeAnswer (+5 more)

### Community 148 - "components-ai-thought-chain.tsx"
Cohesion: 0.15
Nodes (15): Status, StatusIcon(), statusStyles, StepContext, StepContextType, ThoughtChain(), ThoughtChainContent(), ThoughtChainItem() (+7 more)

### Community 151 - "taxonomy.py"
Cohesion: 0.11
Nodes (23): Decision, decide(), empty_ticket_decision(), merge_reasons(), note_for(), _unique(), Category, most_urgent() (+15 more)

### Community 152 - "create_app"
Cohesion: 0.14
Nodes (18): init_db(), initialize_database(), make_engine(), make_sessionmaker(), reset_db(), _accepts(), lifespan(), intake_client() (+10 more)

### Community 153 - "create_app"
Cohesion: 0.14
Nodes (23): session(), _safe_dispatch(), RunRow, recover(), TicketExecution, outcome_from_state(), _current_models(), process_batch() (+15 more)

### Community 154 - "ZainCash support: architecture and ticket flow {#support-overview}"
Cohesion: 0.50
Nodes (3): 1 · System architecture {#system-architecture}, 2 · Ticket flow {#ticket-flow}, ZainCash support: architecture and ticket flow {#support-overview}

### Community 155 - "IntakePage.test.tsx"
Cohesion: 0.07
Nodes (37): Task 7: Bilingual customer chat, screenshots and reviewed submission, Task 8: Intake app UI — phone screen, profile chip, change number, receipt, copy(), parseJson(), readError(), FakeXHR, session, UploadResult (+29 more)

### Community 156 - "employee-frontend/src/components/theme-provider.tsx"
Cohesion: 0.20
Nodes (11): disableTransitionsTemporarily(), getSystemTheme(), isEditableTarget(), isTheme(), ResolvedTheme, Theme, THEME_VALUES, ThemeProvider() (+3 more)

### Community 157 - "agent.py"
Cohesion: 0.13
Nodes (12): _error_cost(), _has_response_usage(), _ModelUsage, _number(), RagDrafter, DraftContext, DraftModelInfo, test_real_search_fault_carries_safe_draft_execution_error() (+4 more)

### Community 159 - "TicketRow"
Cohesion: 0.07
Nodes (34): get_customer(), customer_phone_or_none(), InvalidPhone, normalize_customer_phone(), ensure_customers(), CustomerRow, TicketRow, _ticket_phone() (+26 more)

### Community 160 - "EmbeddingSwitches"
Cohesion: 0.19
Nodes (3): EmbeddingSwitches, _view(), Task 4: The Models page, navigation and route

### Community 161 - "Customer phone identity design"
Cohesion: 0.14
Nodes (13): Backend, Customer phone identity design, Data model, Decisions, Employee API, employee-frontend, Error handling, Existing data (+5 more)

### Community 164 - "openrouter_chat.py"
Cohesion: 0.16
Nodes (3): DraftProviderResponseError, OpenRouterChat, Task 2: OpenRouter and TypeSafe providers, registry, generic embedder

### Community 165 - "test_workspace_schema.py"
Cohesion: 0.15
Nodes (8): assert_customer_schema(), LegacySchemaError, _nullable(), _table_exists(), upgrade_workspace_schema(), test_fresh_schema_passes_the_customer_check(), test_intake_sessions_without_a_customer_phone_stop_startup(), test_nullable_ticket_phone_stops_startup_with_a_reset_instruction()

### Community 167 - "build_pipeline"
Cohesion: 0.10
Nodes (25): Sample, StructuredLLM, build_pipeline(), ConfigError, run_batch(), CredentialChecker, UnavailableDrafter, FakeJevRunnable (+17 more)

### Community 168 - "support_test"
Cohesion: 0.04
Nodes (55): ingest(), SearchResult, index_deadlines(), settings(), support_test(), expire_during_embedding(), Fictional RAG walkthrough inputs, Evidence by layer (+47 more)

### Community 169 - "intake/contracts.py"
Cohesion: 0.11
Nodes (19): Attachment, _aware(), CustomerReview, IntakeModel, Message, PendingQuestion, ProgressItem, QuestionRecord (+11 more)

### Community 171 - "Deviations from the spec (intentional, small)"
Cohesion: 0.17
Nodes (7): Deviations from the spec (intentional, small), Global Constraints, Per-model Evaluation Implementation Plan — Part 2 of 3 (evaluation engine), Task 11: `support eval` CLI and v2 export, Task 7: Metrics, Task 8: Evaluation storage and views, Task 9: Runner, request validation and cost estimate

### Community 172 - "test_submission.py"
Cohesion: 0.32
Nodes (4): _payload(), test_concurrent_submit_dispatches_once(), test_second_request_id_reuses_the_approved_review(), test_submission_replay_creates_one_ticket()

## Ambiguous Edges - Review These
- `Fraud Report` → `Plan 1 Live Smoke`  [AMBIGUOUS]
  README.md · relation: conceptually_related_to

## Knowledge Gaps
- **83 isolated node(s):** `zaincash-support`, `@base-ui/react`, `@fontsource-variable/plus-jakarta-sans`, `@fontsource/tajawal`, `@tailwindcss/vite` (+78 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 1223 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **28 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Settings` connect `Settings` to `agent.py`, `intake/model.py`, `Step`, `test_llm.py`, `pytest`, `test_catalog.py`, `types.py`, `FakeJevRunnable`, `test_rag_api.py`, `intake/repository.py`, `jev.py`, `cli.py`, `resolver.py`, `make_output`, `create_app`, `Step`, `EmbeddingError`, `agent.py`, `test_draft_tools.py`, `test_kb_service.py`, `test_workspace_schema.py`, `build_pipeline`, `support_test`, `parse_document`, `pytest`, `fact`, `main.py`, `httpx`, `config.py`, `create_app`, `test_workspace_api.py`, `test_admin_api.py`, `factory.py`, `Embedder`, `test_final_fix_handoff.py`, `policy.py`, `TurnContext`?**
  _High betweenness centrality (0.085) - this node is a cross-community bridge._
- **Are the 54 inferred relationships involving `Settings` (e.g. with `_command_settings()` and `_run_in_memory()`) actually correct?**
  _`Settings` has 54 INFERRED edges - model-reasoned connections that need verification._
- **What connects `zaincash-support`, `@base-ui/react`, `@fontsource-variable/plus-jakarta-sans` to the rest of the system?**
  _83 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `agent.py` be split into smaller, more focused modules?**
  _Cohesion score 0.1067193675889328 - nodes in this community are weakly interconnected._
- **Why does `2. Current state` connect `jev.py` to `Card`, `NewBatchPage.tsx`, `build_pipeline`, `make_output`, `Per-model evaluation (quality, system, cost) — design specification`, `taxonomy.py`?**
  _High betweenness centrality (0.070) - this node is a cross-community bridge._
- **Are the 68 inferred relationships involving `Step` (e.g. with `catalog()` and `_check_provider()`) actually correct?**
  _`Step` has 68 INFERRED edges - model-reasoned connections that need verification._

### Low-confidence Hints
_AMBIGUOUS edges — the extractor was unsure. Verify before acting on these._

- **What is the exact relationship between `Fraud Report` and `Plan 1 Live Smoke`?**
  _Edge tagged AMBIGUOUS (relation: conceptually_related_to) - confidence is low._