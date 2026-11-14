# Graph Report - zaincash-support  (2026-11-14)

## Corpus Check
- 418 files · ~491,607 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 25 file(s) not represented in the graph (top: (none) 15, .jsonl 4, .css 4)

## Summary
- 4199 nodes · 13965 edges · 172 communities (141 shown, 31 thin omitted)
- Extraction: 84% EXTRACTED · 16% INFERRED · 0% AMBIGUOUS · INFERRED: 2172 edges (avg confidence: 0.93)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `f6c328ec`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- EmbeddingError
- ActiveModels
- pytest
- imports.ts
- investigation.py
- InvalidPhone
- Card
- Customer conversation intake for ZainCash support
- ref_vitest
- IntakeController
- FakeJevRunnable
- make_engine
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
- InvalidEvidence
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
- telemetry/test_store.py
- tasks
- main.py
- ChangeModelDialog.tsx
- IntakePage.tsx
- Plan 3 — Knowledge retrieval and grounded reply drafting
- agent-chat.tsx
- httpx
- UploadedDocument
- cli.py
- test_catalog.py
- ChangeModelDialog.tsx
- pipeline/graph.py
- test_workspace_api.py
- test_interview_api.py
- devDependencies
- EmbeddingSwitches
- support_test
- Step
- FakeJevRunnable
- test_rag_api.py
- Guided intake interview verification — 2026-11-13
- fact
- test_recovery_regressions.py
- errors.py
- IntakeRepository
- resolver.py
- intake/test_repository.py
- KnowledgeError
- build_tools
- devDependencies
- devDependencies
- tools.py
- ticket-flow.ts
- intake/helpers.py
- compilerOptions
- fakes.py
- Plan 3 RAG Drafting Implementation Plan
- dependencies
- InvalidEvidence
- dependencies
- compilerOptions
- _DatabaseCall
- intake/api.ts
- test_final_fix_handoff.py
- Review Focus
- pydantic
- scripts
- Deviations from the spec (intentional, small)
- compilerOptions
- Maintainability and stale-code refactor — design specification
- calls.py
- web/tsconfig.json
- employee-frontend/tsconfig.json
- exports
- Review Focus
- scripts
- users-frontend/README.md
- policy.py
- TurnContext
- DraftToolLimit
- admin.py
- guardrails.py
- embedder.py
- test_handoff.py
- intake/model.py
- ProviderRegistry
- intake.py
- Review Focus
- test_calls.py
- RagDrafter
- Admin-managed, model-agnostic pipeline configuration — design specification
- batch_jobs.py
- types.py
- 5. Backend design
- pipeline/contracts.py
- .session_factory
- passage-reading.ts
- lookup.py
- KnowledgeService
- probe.py
- components-ai-thought-chain.tsx
- DraftSubmission
- intake/README.md
- test_taxonomy.py
- test_dbapi_commit_handoff_arbitrates_cancellation
- FakeXHR
- ZainCash support: architecture and ticket flow {#support-overview}
- IntakePage.test.tsx
- employee-frontend/src/components/theme-provider.tsx
- _ModelUsage
- .describe
- intake/contracts.py
- Customer phone identity design
- api-entrypoint.sh
- 7. Customer frontend design
- AI Usage and Performance Dashboard Implementation Plan — Part 1 of 2 (backend)
- build_pipeline
- test_submission.py

## God Nodes (most connected - your core abstractions)
1. `Settings` - 192 edges
2. `Step` - 109 edges
3. `ModelChoice` - 92 edges
4. `KnowledgeService` - 86 edges
5. `fact()` - 78 edges
6. `ActiveModels` - 74 edges
7. `context()` - 72 edges
8. `useCopy()` - 68 edges
9. `message()` - 67 edges
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

## Communities (172 total, 31 thin omitted)

### Community 0 - "EmbeddingError"
Cohesion: 0.06
Nodes (45): EmbeddingBatch, EmbeddingError, _nonnegative_number(), OpenAICompatibleEmbedder, OpenRouterEmbedder, _ordered_vectors(), _response_cost(), Embeddings (+37 more)

### Community 1 - "ActiveModels"
Cohesion: 0.13
Nodes (25): ActiveModels, Step, model_ids(), batch_concurrency(), _local_pipeline(), ticket_timeout_s(), fake_registry(), test_batch_concurrency_stays_within_bounds() (+17 more)

### Community 2 - "pytest"
Cohesion: 0.21
Nodes (36): _tool_chat(), answer(), call(), draft_state(), script(), submit(), drafter(), events() (+28 more)

### Community 3 - "imports.ts"
Cohesion: 0.10
Nodes (21): Global Constraints, Per-model Evaluation Implementation Plan — Part 3 of 3 (frontend, translations, verification), Task 13: Evaluation types, API client, formatters, copy and report import, Task 15: Provenance, headline metrics, comparison table and empty state, Task 17: Run dialog, progress, page assembly, route and styles, Task 18: Documentation, full verification and manual check, AI Usage and Performance Dashboard Implementation Plan — Part 2 of 2 (frontend, docs, verification), Deviation from the spec (+13 more)

### Community 4 - "investigation.py"
Cohesion: 0.16
Nodes (13): parse_dt(), DraftToolInputError, _datetime(), _days(), _field(), _involves(), _phone(), _phones() (+5 more)

### Community 5 - "InvalidPhone"
Cohesion: 0.07
Nodes (29): BatchInput, KnowledgeIndexInput, KnowledgeSearchInput, ReviewInput, TicketInput, customer_phone_or_none(), InvalidPhone, normalize_customer_phone() (+21 more)

### Community 6 - "Card"
Cohesion: 0.15
Nodes (52): Task 12: Locale parity test and translated Runs pages, Confidence(), EmptyState(), ErrorState(), LoadingState(), Metric(), Button(), buttonVariants (+44 more)

### Community 7 - "Customer conversation intake for ZainCash support"
Cohesion: 0.06
Nodes (31): 10. Verification and acceptance criteria, 11. Delivery and review, 1. Outcome and agreed requirements, 2. Current implementation and integration points, 3. Approach and boundaries, 4. Conversation state and turn flow, 5. Facts, evidence, and readiness, 6. Language and screenshot behavior (+23 more)

### Community 8 - "ref_vitest"
Cohesion: 0.05
Nodes (38): Task 8: Employee evidence panel and processing state, Employee Frontend Maintainability Implementation Plan, Global Constraints, Review Focus, Task 2: Migrate active TicketFlow coverage, then retire the legacy trace/chart cluster, Task 3: Split RunDetailPage and introduce bounded run-result loading, Task 6: Repair ExtractedField fixtures and make standalone typecheck real, Task 7: Repair employee README paths/test-count guidance and run final acceptance (+30 more)

### Community 9 - "IntakeController"
Cohesion: 0.15
Nodes (13): Task 4: Make pending operations discriminated and use one request identity, Task 7: Preserve resume-unavailable state across `startNew`, Task 7: Intake app data layer — phone helper, contracts, API, controller, Task 7: Customer frontend data layer, ControllerState, emptyState(), IntakeController, isConflict() (+5 more)

### Community 10 - "FakeJevRunnable"
Cohesion: 0.11
Nodes (22): CredentialCheck, DegradedCredentialChecker, _finite_nonnegative(), _get(), JevCredentialChecker, test_blank_intake_model_is_rejected(), test_contracts_reject_extra_keys(), test_datetimes_must_be_timezone_aware() (+14 more)

### Community 11 - "make_engine"
Cohesion: 0.06
Nodes (32): init_db(), initialize_database(), make_engine(), make_sessionmaker(), reset_db(), assert_customer_schema(), LegacySchemaError, _nullable() (+24 more)

### Community 12 - "employee-frontend/package.json"
Cohesion: 0.06
Nodes (30): @base-ui/react, class-variance-authority, cn, eslint, @eslint/js, eslint-plugin-react-hooks, eslint-plugin-react-refresh, @fontsource/tajawal (+22 more)

### Community 14 - "QueuePage.tsx"
Cohesion: 0.12
Nodes (40): Task 4: Extract and test the pure queue projection, Task 10: Employee app — customer page and ticket header link, Task 9: Employee app — required phone, queue identity and search, batch entry, Task 15: Ticket cost table and AI timeline, 5.1 Data access, PageHeader(), PriorityBadge(), StatusBadge() (+32 more)

### Community 15 - "Support Taxonomy Categories"
Cohesion: 0.21
Nodes (22): lookup, Account KYC, Account & Security, Agent Dispute, Agent Network, App Bug, Bill Payment, Card Issue (+14 more)

### Community 16 - "ui/package.json"
Cohesion: 0.08
Nodes (24): @base-ui/react, class-variance-authority, cn, eslint, @eslint/js, eslint-plugin-react-hooks, eslint-plugin-react-refresh, @fontsource/tajawal (+16 more)

### Community 17 - "ModelsPage.tsx"
Cohesion: 0.08
Nodes (38): App(), CustomerPage, EvaluationPage, InsightsPage, KnowledgePage, ModelsPage, NewBatchPage, QueuePage (+30 more)

### Community 18 - "users-frontend/package.json"
Cohesion: 0.08
Nodes (23): turbo, devDependencies, prettier, prettier-plugin-tailwindcss, turbo, typescript, engines, node (+15 more)

### Community 19 - "make_output"
Cohesion: 0.10
Nodes (40): build_graph(), PipelineDeps, InMemoryTransactionRepo, FakeClassifier, make_output(), pipeline(), test_config_error_exits_2(), boom() (+32 more)

### Community 20 - "test_draft_guardrails.py"
Cohesion: 0.13
Nodes (31): check_draft(), _citation_findings(), requests_credentials(), make_ticket(), check(), state(), test_aggregation_is_deduplicated_and_has_no_state_side_effects(), test_amount_occurrences_keep_their_own_currency_and_sign() (+23 more)

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
Cohesion: 0.16
Nodes (15): session(), OperationClaim, TurnResult, RevisionConflict, sanitize_intake_text(), _jsonable(), TurnStore, repo() (+7 more)

### Community 26 - "compilerOptions"
Cohesion: 0.09
Nodes (22): compilerOptions, allowArbitraryExtensions, allowImportingTsExtensions, erasableSyntaxOnly, jsx, lib, module, moduleDetection (+14 more)

### Community 27 - "web/src/components/theme-provider.tsx"
Cohesion: 0.10
Nodes (19): App(), controller, disableTransitionsTemporarily(), getSystemTheme(), isEditableTarget(), isTheme(), ResolvedTheme, Theme (+11 more)

### Community 28 - "Settings"
Cohesion: 0.10
Nodes (14): Settings, DraftModelInfo, test_anthropic_model_selects_the_draft_model_only(), test_defaults(), test_draft_token_prices_follow_the_selected_draft_model(), test_drafting_configuration_cannot_bypass_hard_limits(), test_drafting_limits_load_from_environment(), test_env_overrides() (+6 more)

### Community 29 - "Classify and Extract Prompts"
Cohesion: 0.33
Nodes (7): extract, gemini_classify, Pipeline Graph Orchestration, jev_classify, prepare, GeminiClassifier, JevClassifier

### Community 30 - "test_draft_tools.py"
Cohesion: 0.10
Nodes (35): CustomerRow, IncidentRow, TicketRow, TransactionRow, test_repeated_init_db_keeps_existing_tickets(), ErrorEmbedder, test_all_eight_tools_and_seven_parallel_calls_execute_only_six(), test_context_copies_input_and_rejects_raising_hard_call_limit() (+27 more)

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
Cohesion: 0.13
Nodes (25): KnowledgeDocumentIndex, FakeEmbedder, GatedEmbedder, LateEmbedder, PaidEmbedder, count_chunks(), test_category_filters_include_general_policies_and_validate_tags(), test_claim_locks_source_even_before_index_row_exists() (+17 more)

### Community 36 - "web/components.json"
Cohesion: 0.10
Nodes (19): aliases, components, hooks, lib, ui, utils, iconLibrary, menuAccent (+11 more)

### Community 38 - "IntakeRepository"
Cohesion: 0.22
Nodes (5): Credentials, SessionView, IntakeService, make_intake_service(), Task 1: Record the Baseline and Remove Reference-Verified Dead Code

### Community 39 - "ui/components.json"
Cohesion: 0.10
Nodes (19): aliases, components, hooks, lib, ui, utils, iconLibrary, menuAccent (+11 more)

### Community 40 - "intake/repository.py"
Cohesion: 0.14
Nodes (22): _display_name(), CustomerReview, Receipt, ReviewSnapshot, IntakeAttachmentRow, IntakeOperationRow, assert_same_operation(), attachment_from_row() (+14 more)

### Community 41 - "Guided intake interview — design"
Cohesion: 0.06
Nodes (34): 1. Question rules (backend), 2. API contract, 3. Chat screen, 4. Review card, Actions, Additional issues, Approach, Composer hints (+26 more)

### Community 43 - "Human Review Gate"
Cohesion: 0.25
Nodes (4): support CLI, Support Workspace UI Plan, Review API, Workspace UI Verification

### Community 44 - "compilerOptions"
Cohesion: 0.12
Nodes (16): compilerOptions, allowImportingTsExtensions, erasableSyntaxOnly, lib, module, moduleDetection, noEmit, noFallthroughCasesInSwitch (+8 more)

### Community 46 - "NewBatchPage.tsx"
Cohesion: 0.07
Nodes (37): Task 1: Remove reference-verified dead exports, components, and the Mermaid dependency, Task 16: Model detail, confusion matrix and predictions drawer, Task 14: Filters, headline, breakdown tables, trend and unattributed card, 6.1 Route and access, 6.2 Page, 6.3 Change dialog, 6.4 Visible to all employees, 6.5 Text and direction (+29 more)

### Community 47 - "compilerOptions"
Cohesion: 0.12
Nodes (16): compilerOptions, allowImportingTsExtensions, erasableSyntaxOnly, lib, module, moduleDetection, noEmit, noFallthroughCasesInSwitch (+8 more)

### Community 48 - "InvalidEvidence"
Cohesion: 0.26
Nodes (17): ReviewText, InvalidEvidence, validate(), build_review(), _compact(), _render_value(), _ticket_text(), _tokens() (+9 more)

### Community 57 - "parse_document"
Cohesion: 0.08
Nodes (35): TextChunk, _append_chunks(), _check_extracted_size(), _combining_only(), DocumentParseError, _is_ltr(), _is_rtl(), _line_text() (+27 more)

### Community 58 - "attachments.py"
Cohesion: 0.16
Nodes (18): AttachmentStore, ImageRejected, NotOwned, png_bytes(), repo(), store(), test_active_turn_rejects_upload(), test_changed_invalid_bytes_conflict_before_decoding_replay() (+10 more)

### Community 59 - "contracts.ts"
Cohesion: 0.13
Nodes (38): Task 5: Add complete dependency-free API and persisted-session guards, Task 8: Intake app UI — phone screen, profile chip, change number, receipt, createIntakeApi(), parseJson(), readError(), session, ANSWER_KINDS, CHOICES (+30 more)

### Community 60 - "test_llm.py"
Cohesion: 0.13
Nodes (13): StructuredChatLLM, make_draft_model(), make_gemini_llm(), _llm(), _S, test_draft_model_uses_millisecond_timeout_and_disables_sdk_retries(), test_openrouter_reported_cost_takes_precedence_over_token_estimate(), test_openrouter_retry_budget_is_bounded() (+5 more)

### Community 61 - "TicketRow"
Cohesion: 0.11
Nodes (24): get_customer(), get_result(), list_results(), read_intake_attachment(), review_result(), health(), insights(), workspace() (+16 more)

### Community 62 - "use-knowledge-library.ts"
Cohesion: 0.18
Nodes (20): Task 5: Extract presentational DocumentList and KnowledgeReadiness components, acceptIndexRequest(), canRequestIndex(), PendingIndexes, persistPendingIndexes(), pollKnowledge(), refresh(), stop() (+12 more)

### Community 63 - "telemetry/test_store.py"
Cohesion: 0.26
Nodes (11): AiCall, AiCallRow, add_calls(), call_rows(), persist_calls(), sf(), test_add_calls_failure_keeps_the_owner_transaction(), test_add_calls_inside_owner_transaction() (+3 more)

### Community 64 - "tasks"
Cohesion: 0.11
Nodes (18): dependsOn, inputs, outputs, cache, persistent, dependsOn, dependsOn, $schema (+10 more)

### Community 65 - "main.py"
Cohesion: 0.06
Nodes (23): get_session(), _configured(), delete_document(), download_document(), index_document(), list_chunks(), list_documents(), _require_provider() (+15 more)

### Community 66 - "ChangeModelDialog.tsx"
Cohesion: 0.06
Nodes (48): Admin model configuration — employee frontend implementation plan, Backend API contract used here, File structure, Global Constraints, Review Focus, Task 1: API types, admin session and admin requests, Task 2: Strings, the AI locality chip, run models and the batch switch message, Task 3: Model choice logic and the change dialog (+40 more)

### Community 67 - "IntakePage.tsx"
Cohesion: 0.07
Nodes (52): Global Constraints, Intake Chat UI Implementation Plan, Task 1: Put the summary and receipt in the thread, Task 2: Put screenshots inside the composer, Task 3: Apply the workspace chat styles, Task 4: Check the page in the browser, 4. Components, users-frontend (+44 more)

### Community 68 - "Plan 3 — Knowledge retrieval and grounded reply drafting"
Cohesion: 0.11
Nodes (18): 10. Remaining demo roadmap, 1. Intent and acceptance criteria, 3. Provider and configuration, 4. Knowledge ingestion and persistence, 5. Retrieval and evidence, 6. Bounded investigation agent, 7. Draft guardrails and failure outcomes, 8. Pipeline, API, CLI and UI integration (+10 more)

### Community 69 - "agent-chat.tsx"
Cohesion: 0.15
Nodes (25): Task 8: Chat screen — instant bubble, typing, reasons, quick replies, composer hints, clsx, tailwind-merge, @testing-library/user-event, AgentChat, AgentChatProps, AgentMessage, AssistantText() (+17 more)

### Community 70 - "httpx"
Cohesion: 0.11
Nodes (14): OllamaProvider, _provider(), _tags_handler(), test_catalog_lists_installed_models_with_reported_capabilities(), handler(), test_chat_model_sets_the_configured_context_window(), test_chat_model_targets_the_configured_server(), test_embedder_uses_openai_compatible_endpoint_without_dimensions() (+6 more)

### Community 71 - "UploadedDocument"
Cohesion: 0.17
Nodes (9): UploadedDocument, document_view(), test_db_deadline_cancelled_publication_cannot_commit_late(), test_db_deadline_is_cumulative_across_publication_statements(), changed_index(), test_db_deadline_second_cancel_during_failure_bookkeeping_keeps_cost(), test_job_deadline_bounds_source_lock_wait_before_claim(), view() (+1 more)

### Community 72 - "cli.py"
Cohesion: 0.06
Nodes (40): get_run(), list_runs(), start_run(), _command_settings(), ingest_kb_cmd(), ingest(), init_db_cmd(), Mode (+32 more)

### Community 73 - "test_catalog.py"
Cohesion: 0.15
Nodes (16): CatalogCache, step_catalog(), eligibility(), recent(), BrokenStatusProvider, test_a_provider_whose_status_check_raises_is_listed_as_unreachable(), test_catalog_errors_stay_per_provider_and_cache_respects_ttl(), test_classify_catalog_only_offers_typesafe() (+8 more)

### Community 74 - "ChangeModelDialog.tsx"
Cohesion: 0.15
Nodes (27): ConfirmDialog(), Dialog(), DialogContent(), DialogDescription(), DialogFooter(), DialogHeader(), DialogOverlay(), DialogPortal() (+19 more)

### Community 75 - "pipeline/graph.py"
Cohesion: 0.06
Nodes (18): DraftResult, _default_retry(), _Nodes, _retryable(), _Execution, DraftContext, CredentialChecker, Drafter (+10 more)

### Community 76 - "test_workspace_api.py"
Cohesion: 0.12
Nodes (19): review_payload(), start_run(), test_batch_and_queue_expose_real_results(), test_batch_failure_is_isolated_and_conflicting_ids_rejected(), test_customer_profile_lists_the_latest_result_of_each_ticket(), test_progress_counts_only_durable_results_after_save_failure(), fail_one_save(), test_result_list_paginates_filters_and_run_id() (+11 more)

### Community 77 - "test_interview_api.py"
Cohesion: 0.21
Nodes (19): analyze_calls(), ask(), complete_without_reference(), opening(), opening_with_amount(), reference_answer(), send(), start() (+11 more)

### Community 79 - "devDependencies"
Cohesion: 0.12
Nodes (16): devDependencies, eslint, @eslint/js, eslint-plugin-react-hooks, eslint-plugin-react-refresh, globals, prettier, prettier-plugin-tailwindcss (+8 more)

### Community 80 - "EmbeddingSwitches"
Cohesion: 0.17
Nodes (6): EmbeddingSwitchRow, EmbeddingSwitches, SwitchConflict, _view(), test_runs_are_blocked_while_a_switch_runs_and_restart_recovers(), Task 4: The Models page, navigation and route

### Community 81 - "support_test"
Cohesion: 0.07
Nodes (30): index_deadlines(), settings(), support_test(), test_source_validation_sanitizes_name_preserves_bom_and_caller_transaction(), expire_during_embedding(), Evidence by layer, Known limitations and remaining work, Repeatable local walkthrough (+22 more)

### Community 82 - "Step"
Cohesion: 0.07
Nodes (29): ModelSettingAuditRow, ModelSettingRow, probe(), ModelSettingsStore, ModelChoice, FakeProvider, test_start_updates_the_cache_without_reloading_from_the_database(), _registry() (+21 more)

### Community 83 - "FakeJevRunnable"
Cohesion: 0.29
Nodes (10): FakeJevRunnable, _criteria(), _run(), test_low_top_probability_is_uncertain(), test_one_main_call_with_all_questions(), test_order_check_uses_reversed_options(), test_order_disagreement_is_uncertain(), test_priority_level_maps_to_p_label() (+2 more)

### Community 84 - "test_rag_api.py"
Cohesion: 0.13
Nodes (19): client(), test_actual_guardrail_failure_is_separate_from_reply(), test_concurrent_index_requests_share_active_work(), test_disabled_or_missing_provider_stores_without_indexing(), test_explicit_retry_tags_search_and_chunk_pagination(), test_health_distinguishes_failed_from_empty(), test_health_requires_compatible_nonempty_index(), test_index_background_admission_is_bounded_and_releases_capacity() (+11 more)

### Community 85 - "Guided intake interview verification — 2026-11-13"
Cohesion: 0.18
Nodes (10): Arabic at 390×844, starting from the vague message, English at 1280×900, with the complete message, Existing-test expectation changes from Task 1, Final automated checks, Guided intake interview verification — 2026-11-13, Live browser run, Live probe output (facts only), Live transfer probe (+2 more)

### Community 86 - "fact"
Cohesion: 0.13
Nodes (65): Analysis, EvidenceRef, Question, Readiness, merge_analysis(), assess_readiness(), choose_question(), context() (+57 more)

### Community 87 - "test_recovery_regressions.py"
Cohesion: 0.35
Nodes (10): command(), create(), test_actual_app_restart_reconciles_failed_placeholder(), test_failed_review_retry_cannot_reopen_submitted_session(), test_original_payload_identity_survives_sanitization(), test_publication_failure_is_retryable_without_restart(), fail_once(), test_receipt_reference_is_preserved() (+2 more)

### Community 88 - "errors.py"
Cohesion: 0.36
Nodes (6): IntakeError, InvalidCustomerPhone, OperationConflict, StaleReview, TurnBusy, Task 1: Durable intake sessions and ownership

### Community 89 - "IntakeRepository"
Cohesion: 0.15
Nodes (5): IntakeRepository, intake_client(), builder(), HTTP contract (implemented in Tasks 4–5), Task 9: End-to-end handoff, live vision evidence and runbook

### Community 90 - "resolver.py"
Cohesion: 0.16
Nodes (15): draft_timeout_s(), env_defaults(), intake_timeout_s(), _settings(), test_eligibility(), test_env_defaults_match_todays_settings(), test_env_overrides_for_draft_and_intake(), test_local_timeouts_and_limits() (+7 more)

### Community 91 - "intake/test_repository.py"
Cohesion: 0.19
Nodes (12): IntakeMessageRow, IntakeSessionRow, initial_state(), intake_failed(), repo(), test_invalid_phone_cannot_start_a_session(), test_message_sequence_is_unique(), test_messages_keep_sequence_and_unicode() (+4 more)

### Community 92 - "KnowledgeError"
Cohesion: 0.19
Nodes (6): DocumentNotFoundError, KnowledgeError, KnowledgeExecutionError, test_search_unexpected_fault_logs_only_safe_type(), fail_search(), Task 14: Preserve Safe Knowledge 503s and Log Only Unexpected Diagnostic Types

### Community 93 - "build_tools"
Cohesion: 0.13
Nodes (7): build_tools(), flag(), retrieve(), _error_cost(), Backend Maintainability Implementation Plan, Global Constraints, Task 2: Separate Historical Escalation Text from Current Tool Reasons

### Community 94 - "devDependencies"
Cohesion: 0.11
Nodes (19): devDependencies, eslint, @eslint/js, eslint-plugin-react-hooks, eslint-plugin-react-refresh, globals, jsdom, @tailwindcss/vite (+11 more)

### Community 95 - "devDependencies"
Cohesion: 0.17
Nodes (12): devDependencies, eslint, @eslint/js, eslint-plugin-react-hooks, eslint-plugin-react-refresh, globals, tailwindcss, @types/node (+4 more)

### Community 96 - "tools.py"
Cohesion: 0.24
Nodes (8): _Flag, _History, _Input, _Knowledge, _Lookup, _Recent, _Search, _Service

### Community 97 - "ticket-flow.ts"
Cohesion: 0.06
Nodes (63): Task 1: Sentence catalog, Task 2: Which step is open, Task 3: Received, produced, and drafting events, Task 4: Mermaid source, Task 5: Draw the charts on the ticket page, 1. Outcome, 2. Scope, 4. Which step is open (+55 more)

### Community 98 - "intake/helpers.py"
Cohesion: 0.24
Nodes (4): grounded_analysis(), grounded_review(), image_evidence(), ScriptedIntakeModel

### Community 99 - "compilerOptions"
Cohesion: 0.14
Nodes (13): compilerOptions, jsx, lib, module, moduleResolution, noEmit, paths, skipLibCheck (+5 more)

### Community 100 - "fakes.py"
Cohesion: 0.09
Nodes (29): LLMUnavailable, StructuredLLM, FieldPick, NormalizedTicket, FieldExtractor, _field(), fill_gaps(), finalize() (+21 more)

### Community 101 - "Plan 3 RAG Drafting Implementation Plan"
Cohesion: 0.09
Nodes (20): Fictional RAG walkthrough inputs, Completion and review record — 2026-10-17, Execution handoff, File map and shared interfaces, Global Constraints, Plan 3 RAG Drafting Implementation Plan, Plan self-review, Review Focus (+12 more)

### Community 102 - "dependencies"
Cohesion: 0.12
Nodes (16): dependencies, @base-ui/react, class-variance-authority, cn, @fontsource/tajawal, @fontsource-variable/plus-jakarta-sans, lucide-react, motion (+8 more)

### Community 103 - "InvalidEvidence"
Cohesion: 0.13
Nodes (20): Fact, canonical_digits(), normalize_reported_date(), _apply(), _check_reference(), _compact(), checked_update(), _newer_correction() (+12 more)

### Community 104 - "dependencies"
Cohesion: 0.20
Nodes (10): dependencies, @base-ui/react, class-variance-authority, cn, @fontsource/tajawal, @fontsource-variable/plus-jakarta-sans, react, react-dom (+2 more)

### Community 105 - "compilerOptions"
Cohesion: 0.17
Nodes (11): compilerOptions, jsx, lib, module, moduleResolution, outDir, skipLibCheck, strict (+3 more)

### Community 107 - "intake/api.ts"
Cohesion: 0.10
Nodes (24): IntakeApi, UploadResult, INTAKE_FALLBACK_MESSAGE, malformed, populated, fileIdentity(), fakeApi(), review (+16 more)

### Community 108 - "test_final_fix_handoff.py"
Cohesion: 0.10
Nodes (22): Passage, SearchResult, Knowledge, assert_completed_evidence(), faulty_knowledge(), read(), outer_deadlines(), PaidEmbeddings (+14 more)

### Community 109 - "Review Focus"
Cohesion: 0.17
Nodes (10): Review Focus, Task 10: Grouped review card with answer buttons, Task 11: Employee label, full gates, live probe and verification record, Task 2: Prompt rules and the `recipient_name` vocabulary, Task 9: Progress strip, 1. Outcome, 2. Scope, 3. Layout (+2 more)

### Community 110 - "pydantic"
Cohesion: 0.23
Nodes (6): CitationSource, _Draft, draft_evidence(), _Guardrail, _TraceModel, _validated()

### Community 111 - "scripts"
Cohesion: 0.25
Nodes (8): scripts, build, dev, format, lint, preview, test, typecheck

### Community 112 - "Deviations from the spec (intentional, small)"
Cohesion: 0.29
Nodes (6): Deviations from the spec (intentional, small), Global Constraints, Per-model Evaluation Implementation Plan — Part 2 of 3 (evaluation engine), Task 11: `support eval` CLI and v2 export, Task 7: Metrics, Task 9: Runner, request validation and cost estimate

### Community 113 - "compilerOptions"
Cohesion: 0.29
Nodes (6): compilerOptions, module, moduleResolution, skipLibCheck, strict, target

### Community 114 - "Maintainability and stale-code refactor — design specification"
Cohesion: 0.12
Nodes (15): 10. Verification and acceptance, 1. Outcome and success criteria, 2. Audit baseline, 3. Selected approach and sequence, 4. Boundaries and non-goals, 8.1 Approved deletions, 8.2 Docker and documentation, 8.3 Graphify outputs (+7 more)

### Community 115 - "calls.py"
Cohesion: 0.29
Nodes (6): _percentile(), CallContext, count(), money(), usage_of(), test_usage_of_reads_langchain_and_ollama_metadata()

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
Cohesion: 0.20
Nodes (9): Customer Frontend Maintainability Implementation Plan, Global Constraints, Review Focus, Task 1: Cleanup-first removal of reference-verified dead code and dependencies, Task 2: Make standalone typechecking and root test execution real, Task 3: Centralize test cleanup and shared intake fixtures mechanically, Task 6: Extract stable-ID sequential upload lifecycle with TDD, Task 8: Disable streaming Stop when no handler exists (+1 more)

### Community 120 - "scripts"
Cohesion: 0.50
Nodes (4): scripts, format, lint, typecheck

### Community 122 - "policy.py"
Cohesion: 0.11
Nodes (38): AskedQuestion, IntakeState, answer_choices(), answer_kind(), ask_for(), ask_once_keys(), asked_count(), asks_for_secret() (+30 more)

### Community 123 - "TurnContext"
Cohesion: 0.15
Nodes (10): quick_answer(), QuestionRecord, TurnContext, IntakeGraph, _invitation(), test_graph_budget_uses_the_pinned_choice_and_timeout(), test_pin_failure_is_reported_as_model_unavailable(), test_without_pinning_the_budget_uses_settings() (+2 more)

### Community 124 - "DraftToolLimit"
Cohesion: 0.20
Nodes (7): DraftAlreadySubmitted, DraftToolLimit, _bounded(), visit(), guarded(), invoke(), _json()

### Community 125 - "admin.py"
Cohesion: 0.14
Nodes (19): audit(), catalog(), _check_provider(), ChoiceInput, embedding_switch(), ModelOptions, models(), ProbeInput (+11 more)

### Community 126 - "guardrails.py"
Cohesion: 0.07
Nodes (45): Candidate, _add(), find_candidates(), normalize_phone(), _overlaps(), parse_amount(), resolve_date(), _safe_date() (+37 more)

### Community 127 - "embedder.py"
Cohesion: 0.15
Nodes (6): ConfiguredEmbedder, _Store, make_knowledge_service(), choice_for(), _Store, test_configured_embedder_follows_the_current_setting()

### Community 128 - "test_handoff.py"
Cohesion: 0.33
Nodes (8): _amount(), complete_conversation(), _dated(), _message(), _opening(), _png(), _review(), _user()

### Community 129 - "intake/model.py"
Cohesion: 0.10
Nodes (30): ImageInput, ModelCall, ModelUnavailable, _analysis_prompt(), _bounded_context(), _guard_size(), IntakeModel, ModelBudget (+22 more)

### Community 130 - "ProviderRegistry"
Cohesion: 0.10
Nodes (11): DraftProviderResponseError, OpenRouterChat, provider_errors(), ProviderRegistry, UnknownProvider, test_registry_includes_ollama_and_its_errors(), test_registry_rejects_unknown_providers_and_exposes_errors(), File structure (+3 more)

### Community 131 - "intake.py"
Cohesion: 0.15
Nodes (22): ask_question(), create_session(), _credentials(), _dump(), get_session(), post_message(), read_attachment(), remove_attachment() (+14 more)

### Community 132 - "Review Focus"
Cohesion: 0.14
Nodes (13): api(), settings(), Global Constraints, Repository Hygiene Maintainability Implementation Plan, Review Focus, Task 1: Establish the safety baseline and remove tracked Graphify cache contents, Task 2: Delete the superseded architecture HTML after a fresh reference check, Task 3: Remove confirmed stale local runtime state and the duplicate screenshot (+5 more)

### Community 133 - "test_calls.py"
Cohesion: 0.17
Nodes (16): call_context(), cost_for(), embed_process(), record(), short_error(), Timer, call(), test_contexts_buffer_and_nest() (+8 more)

### Community 134 - "RagDrafter"
Cohesion: 0.15
Nodes (12): RagDrafter, DraftExecutionError, Checker, response_payload(), run_provider_pipeline(), send(), search_response(), test_empty_choices_escalates_and_keeps_paid_response_usage() (+4 more)

### Community 135 - "Admin-managed, model-agnostic pipeline configuration — design specification"
Cohesion: 0.29
Nodes (6): 10. Out of scope, 1. Outcome and success criteria, 3. Decisions, 7. Error handling, 9. Testing, Admin-managed, model-agnostic pipeline configuration — design specification

### Community 136 - "batch_jobs.py"
Cohesion: 0.09
Nodes (33): _safe_dispatch(), save_outcomes(), _accepts(), lifespan(), recover(), TicketOutcome, TicketExecution, outcome_from_state() (+25 more)

### Community 137 - "types.py"
Cohesion: 0.06
Nodes (25): UnsupportedOperation, _capabilities(), OpenRouterProvider, _per_million(), TypeSafeProvider, Capability, CatalogEntry, ProviderStatus (+17 more)

### Community 138 - "5. Backend design"
Cohesion: 0.29
Nodes (5): 5.1 Dead-code cleanup, 5.3 Knowledge-service boundary, 5.4 Shared backend boundaries, 5.5 Confirmed backend defect fixes, 5. Backend design

### Community 139 - "pipeline/contracts.py"
Cohesion: 0.07
Nodes (38): Candidates, ClassificationResult, ClassifierOutput, Classifier, build_order_check(), build_questions(), build_state(), category_criteria() (+30 more)

### Community 141 - "passage-reading.ts"
Cohesion: 0.39
Nodes (6): concisePassage(), directionOf(), keepLine(), PassageReading, sentences(), refund

### Community 142 - "lookup.py"
Cohesion: 0.10
Nodes (35): Decision, ExtractedField, LookupResult, TxnRecord, _as_date(), _iqd_amount(), match_transaction(), TransactionRepo (+27 more)

### Community 143 - "KnowledgeService"
Cohesion: 0.12
Nodes (8): Embedder, _Claim, _error_cost(), IndexAttemptLostError, KnowledgeService, test_pdf_page_metadata_and_repeated_text_chunk_identity(), 2. Current state, 4.9 Runtime embedder

### Community 144 - "probe.py"
Cohesion: 0.10
Nodes (14): _chat(), _classify(), _describe(), _draft(), _embed(), _extract(), _intake(), _ProbeAnswer (+6 more)

### Community 148 - "components-ai-thought-chain.tsx"
Cohesion: 0.13
Nodes (17): Status, StatusIcon(), statusStyles, StepContext, StepContextType, ThoughtChain(), ThoughtChainContent(), ThoughtChainItem() (+9 more)

### Community 151 - "test_taxonomy.py"
Cohesion: 0.13
Nodes (10): load_taxonomy(), most_urgent(), priority_rank(), TaxonomyError, tax(), taxonomy(), taxonomy(), taxonomy() (+2 more)

### Community 152 - "test_dbapi_commit_handoff_arbitrates_cancellation"
Cohesion: 0.14
Nodes (9): test_db_deadline_includes_pool_and_checkout_without_late_claim(), checked_in(), test_db_deadline_search_cancellation_is_nonblocking_and_retains_cost(), test_dbapi_commit_handoff_arbitrates_cancellation(), gate(), gate_before_dbapi(), gate_inside_dbapi(), test_index_deadline_or_cancellation_preserves_real_adapter_partial_cost() (+1 more)

### Community 154 - "ZainCash support: architecture and ticket flow {#support-overview}"
Cohesion: 0.50
Nodes (3): 1 · System architecture {#system-architecture}, 2 · Ticket flow {#ticket-flow}, ZainCash support: architecture and ticket flow {#support-overview}

### Community 155 - "IntakePage.test.tsx"
Cohesion: 0.13
Nodes (19): Task 6: Customer API client and resumable UI state, Task 7: Bilingual customer chat, screenshots and reviewed submission, copy(), collectingController(), debited, emptySession(), fakeApi(), firstMessage (+11 more)

### Community 156 - "employee-frontend/src/components/theme-provider.tsx"
Cohesion: 0.23
Nodes (11): disableTransitionsTemporarily(), getSystemTheme(), isEditableTarget(), isTheme(), ResolvedTheme, Theme, THEME_VALUES, ThemeProvider() (+3 more)

### Community 157 - "_ModelUsage"
Cohesion: 0.10
Nodes (19): _error_cost(), _has_response_usage(), _ModelUsage, _number(), Task 11: Use Draft-Model-Specific Fallback Token Prices, Task 6: Record drafting model calls with latency, 10. Phase 2 (for reference, not designed here), 1. Outcome and success criteria (+11 more)

### Community 159 - "intake/contracts.py"
Cohesion: 0.27
Nodes (6): Attachment, _aware(), IntakeModel, Message, PendingQuestion, ProgressItem

### Community 161 - "Customer phone identity design"
Cohesion: 0.13
Nodes (14): Backend, Canonical phone format, Customer phone identity design, Data model, Decisions, Employee API, employee-frontend, Error handling (+6 more)

### Community 164 - "7. Customer frontend design"
Cohesion: 0.40
Nodes (5): 7.1 Verification and cleanup, 7.2 Runtime contracts and persisted operations, 7.3 Upload lifecycle, 7.4 Controller, chat, and tests, 7. Customer frontend design

### Community 165 - "AI Usage and Performance Dashboard Implementation Plan — Part 1 of 2 (backend)"
Cohesion: 0.40
Nodes (4): AI Usage and Performance Dashboard Implementation Plan — Part 1 of 2 (backend), Global Constraints, Review Focus, Task 3: Ticket outcomes carry their calls; batch and CLI write them with the result

### Community 167 - "build_pipeline"
Cohesion: 0.11
Nodes (25): SqlTransactionRepo, Sample, build_pipeline(), ConfigError, run_batch(), FakeStructuredLLM, ScriptedChat, _settings() (+17 more)

### Community 172 - "test_submission.py"
Cohesion: 0.32
Nodes (4): _payload(), test_concurrent_submit_dispatches_once(), test_second_request_id_reuses_the_approved_review(), test_submission_replay_creates_one_ticket()

## Ambiguous Edges - Review These
- `Fraud Report` → `Plan 1 Live Smoke`  [AMBIGUOUS]
  README.md · relation: conceptually_related_to

## Knowledge Gaps
- **83 isolated node(s):** `zaincash-support`, `@base-ui/react`, `@fontsource-variable/plus-jakarta-sans`, `@fontsource/tajawal`, `@tailwindcss/vite` (+78 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 1247 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **31 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Settings` connect `Settings` to `EmbeddingError`, `intake/model.py`, `ProviderRegistry`, `ActiveModels`, `Review Focus`, `pytest`, `RagDrafter`, `types.py`, `FakeJevRunnable`, `make_engine`, `pipeline/contracts.py`, `KnowledgeService`, `make_output`, `test_taxonomy.py`, `test_draft_tools.py`, `test_kb_service.py`, `IntakeRepository`, `build_pipeline`, `intake/repository.py`, `attachments.py`, `test_llm.py`, `telemetry/test_store.py`, `main.py`, `httpx`, `cli.py`, `test_catalog.py`, `pipeline/graph.py`, `test_workspace_api.py`, `support_test`, `Step`, `test_rag_api.py`, `fact`, `IntakeRepository`, `resolver.py`, `intake/test_repository.py`, `test_final_fix_handoff.py`, `TurnContext`, `admin.py`, `embedder.py`?**
  _High betweenness centrality (0.100) - this node is a cross-community bridge._
- **Are the 56 inferred relationships involving `Settings` (e.g. with `_command_settings()` and `_run_in_memory()`) actually correct?**
  _`Settings` has 56 INFERRED edges - model-reasoned connections that need verification._
- **What connects `zaincash-support`, `@base-ui/react`, `@fontsource-variable/plus-jakarta-sans` to the rest of the system?**
  _83 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `EmbeddingError` be split into smaller, more focused modules?**
  _Cohesion score 0.06392405063291139 - nodes in this community are weakly interconnected._
- **Why does `2. Current state` connect `pipeline/contracts.py` to `imports.ts`, `Card`, `build_pipeline`, `lookup.py`, `make_output`?**
  _High betweenness centrality (0.070) - this node is a cross-community bridge._
- **Are the 69 inferred relationships involving `Step` (e.g. with `catalog()` and `_check_provider()`) actually correct?**
  _`Step` has 69 INFERRED edges - model-reasoned connections that need verification._

### Low-confidence Hints
_AMBIGUOUS edges — the extractor was unsure. Verify before acting on these._

- **What is the exact relationship between `Fraud Report` and `Plan 1 Live Smoke`?**
  _Edge tagged AMBIGUOUS (relation: conceptually_related_to) - confidence is low._