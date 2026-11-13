# Graph Report - zaincash-support  (2026-11-13)

## Corpus Check
- 400 files · ~444,730 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 25 file(s) not represented in the graph (top: (none) 15, .jsonl 4, .css 4)

## Summary
- 3983 nodes · 13266 edges · 168 communities (139 shown, 29 thin omitted)
- Extraction: 85% EXTRACTED · 15% INFERRED · 0% AMBIGUOUS · INFERRED: 2004 edges (avg confidence: 0.93)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `e3f85d78`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- Review Focus
- Step
- pytest
- TurnStore
- investigation.py
- ._metadata
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
- load_taxonomy
- test_draft_guardrails.py
- web/package.json
- test_recovery_regressions.py
- compilerOptions
- employee-frontend/components.json
- ModelSettingsStore
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
- locale.tsx
- Human Flag Tool
- Recent Transactions Tool
- Ticket History Tool
- Lookup Transaction Tool
- Search Transactions Tool
- Submit Draft Tool
- Project Root
- parse_document
- AttachmentStore
- contracts.ts
- fact
- LLMUnavailable
- knowledge-view.test.tsx
- IntakePage.tsx
- tasks
- knowledge.py
- ChangeModelDialog.tsx
- fact
- PipelineState
- results.py
- make_ticket
- intake/repository.py
- RunRow
- workspace.py
- FakeJevRunnable
- normalize.py
- test_workspace_api.py
- test_interview_api.py
- devDependencies
- turns.py
- build_tools
- factory.py
- tools.py
- 5. Backend design
- scripts
- TicketInput
- Backend
- dependencies
- DraftSubmission
- @testing-library/react
- HTTP contract (implemented in Tasks 4–5)
- uuid
- devDependencies
- devDependencies
- fakes.py
- ticket-flow.ts
- review.py
- compilerOptions
- collapsible.tsx
- pydantic
- dependencies
- InvalidEvidence
- dependencies
- compilerOptions
- lib/types.ts
- intake/api.ts
- test_final_fix_handoff.py
- scripts
- lookup.py
- compilerOptions
- Maintainability and stale-code refactor — design specification
- httpx
- web/tsconfig.json
- employee-frontend/tsconfig.json
- exports
- IntakePage.tsx
- scripts
- users-frontend/README.md
- policy.py
- TurnContext
- admin.py
- guardrails.py
- test_cli.py
- Credentials
- intake/model.py
- test_llm.py
- intake.py
- Review Focus
- _DatabaseCall
- test_dbapi_commit_handoff_arbitrates_cancellation
- config.py
- intake/test_repository.py
- jev.py
- submission.py
- db/repository.py
- db/repository.py
- knowledge_runtime.py
- probe.py
- components-ai-thought-chain.tsx
- intake/README.md
- pipeline/graph.py
- create_app
- main.py
- ZainCash support: architecture and ticket flow {#support-overview}
- IntakePage.test.tsx
- employee-frontend/src/components/theme-provider.tsx
- agent.py
- test_taxonomy.py
- TicketRow
- test_embedding_switch.py
- Customer phone identity design
- api-entrypoint.sh
- ProviderRegistry
- test_workspace_schema.py
- build_pipeline
- support_test
- intake/contracts.py
- Deviations from the spec (intentional, small)
- test_submission.py

## God Nodes (most connected - your core abstractions)
1. `Settings` - 188 edges
2. `Step` - 108 edges
3. `ModelChoice` - 91 edges
4. `KnowledgeService` - 85 edges
5. `ActiveModels` - 74 edges
6. `fact()` - 68 edges
7. `useCopy()` - 68 edges
8. `context()` - 64 edges
9. `message()` - 59 edges
10. `IntakeController` - 55 edges

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

## Communities (168 total, 29 thin omitted)

### Community 0 - "Review Focus"
Cohesion: 0.22
Nodes (8): Customer Frontend Maintainability Implementation Plan, Global Constraints, Review Focus, Task 2: Make standalone typechecking and root test execution real, Task 3: Centralize test cleanup and shared intake fixtures mechanically, Task 6: Extract stable-ID sequential upload lifecycle with TDD, Task 8: Disable streaming Stop when no handler exists, Task 9: Run the complete customer acceptance matrix and final diff review

### Community 1 - "Step"
Cohesion: 0.11
Nodes (27): _Store, ActiveModels, Step, make_gemini_llm(), batch_concurrency(), _current_models(), _local_pipeline(), ticket_timeout_s() (+19 more)

### Community 2 - "pytest"
Cohesion: 0.18
Nodes (40): _tool_chat(), answer(), call(), Checker, draft_state(), script(), submit(), pipeline() (+32 more)

### Community 3 - "TurnStore"
Cohesion: 0.28
Nodes (8): OperationClaim, ReviewSnapshot, TurnResult, RevisionConflict, TurnStore, test_recovered_attempt_cannot_publish_stale_output(), test_review_publication_revision_matches_the_session(), Task 4: Quick-reply answers without a model call

### Community 4 - "investigation.py"
Cohesion: 0.14
Nodes (15): parse_dt(), TxnRecord, DraftToolInputError, _datetime(), _days(), _field(), _involves(), _phone() (+7 more)

### Community 6 - "Card"
Cohesion: 0.11
Nodes (66): Task 5: Extract presentational DocumentList and KnowledgeReadiness components, Task 12: Locale parity test and translated Runs pages, 6.1 Verification and cleanup, 6.2 Retire the legacy trace/chart cluster, 6.3 Runs and request loading, 6.4 Focused view extraction, 6. Employee frontend design, Confidence() (+58 more)

### Community 7 - "Customer conversation intake for ZainCash support"
Cohesion: 0.06
Nodes (31): 10. Verification and acceptance criteria, 11. Delivery and review, 1. Outcome and agreed requirements, 2. Current implementation and integration points, 3. Approach and boundaries, 4. Conversation state and turn flow, 5. Facts, evidence, and readiness, 6. Language and screenshot behavior (+23 more)

### Community 8 - "lib/api.ts"
Cohesion: 0.10
Nodes (29): Admin model configuration — employee frontend implementation plan, File structure, Global Constraints, Review Focus, Task 2: Strings, the AI locality chip, run models and the batch switch message, Task 3: Model choice logic and the change dialog, Task 14: Evaluation view helpers, Input() (+21 more)

### Community 9 - "IntakeController"
Cohesion: 0.17
Nodes (11): Task 1: Cleanup-first removal of reference-verified dead code and dependencies, Task 7: Preserve resume-unavailable state across `startNew`, Task 7: Intake app data layer — phone helper, contracts, API, controller, Task 7: Customer frontend data layer, ControllerState, emptyState(), IntakeController, isConflict() (+3 more)

### Community 10 - "FakeJevRunnable"
Cohesion: 0.11
Nodes (19): CredentialCheck, CredentialChecker, DegradedCredentialChecker, _finite_nonnegative(), _get(), JevCredentialChecker, ResponseRunnable, test_bad_usage_cannot_poison_cost() (+11 more)

### Community 11 - "test_rag_api.py"
Cohesion: 0.10
Nodes (22): KnowledgeExecutionError, client(), evidence_client(), test_actual_guardrail_failure_is_separate_from_reply(), test_concurrent_index_requests_share_active_work(), test_disabled_or_missing_provider_stores_without_indexing(), test_explicit_retry_tags_search_and_chunk_pagination(), test_health_distinguishes_failed_from_empty() (+14 more)

### Community 12 - "employee-frontend/package.json"
Cohesion: 0.06
Nodes (30): @base-ui/react, class-variance-authority, cn, eslint, @eslint/js, eslint-plugin-react-hooks, eslint-plugin-react-refresh, @fontsource/tajawal (+22 more)

### Community 14 - "QueuePage.tsx"
Cohesion: 0.15
Nodes (30): Task 4: Extract and test the pure queue projection, Task 10: Employee app — customer page and ticket header link, 5.1 Data access, 7. Testing, PageHeader(), PriorityBadge(), StatusBadge(), Table() (+22 more)

### Community 15 - "Support Taxonomy Categories"
Cohesion: 0.21
Nodes (22): lookup, Account KYC, Account & Security, Agent Dispute, Agent Network, App Bug, Bill Payment, Card Issue (+14 more)

### Community 16 - "ui/package.json"
Cohesion: 0.08
Nodes (24): @base-ui/react, class-variance-authority, cn, eslint, @eslint/js, eslint-plugin-react-hooks, eslint-plugin-react-refresh, @fontsource/tajawal (+16 more)

### Community 17 - "ModelsPage.tsx"
Cohesion: 0.12
Nodes (30): App(), CustomerPage, EvaluationPage, InsightsPage, KnowledgePage, ModelsPage, NewBatchPage, QueuePage (+22 more)

### Community 18 - "users-frontend/package.json"
Cohesion: 0.08
Nodes (23): turbo, devDependencies, prettier, prettier-plugin-tailwindcss, turbo, typescript, engines, node (+15 more)

### Community 19 - "load_taxonomy"
Cohesion: 0.17
Nodes (17): build_graph(), PipelineDeps, InMemoryTransactionRepo, load_taxonomy(), tax(), FakeClassifier, pipeline(), taxonomy() (+9 more)

### Community 20 - "test_draft_guardrails.py"
Cohesion: 0.13
Nodes (28): check_draft(), _citation_findings(), requests_credentials(), check(), state(), test_aggregation_is_deduplicated_and_has_no_state_side_effects(), test_amount_occurrences_keep_their_own_currency_and_sign(), test_avoid_sharing_warning_does_not_excuse_a_later_request() (+20 more)

### Community 21 - "web/package.json"
Cohesion: 0.08
Nodes (24): clsx, jsdom, tailwind-merge, @workspace/ui, eslint, @eslint/js, eslint-plugin-react-hooks, eslint-plugin-react-refresh (+16 more)

### Community 22 - "test_recovery_regressions.py"
Cohesion: 0.19
Nodes (10): _command_settings(), ingest_kb_cmd(), init_db_cmd(), Mode, run_batch_cmd(), _run_in_memory(), seed_db_cmd(), _sessionmaker() (+2 more)

### Community 23 - "compilerOptions"
Cohesion: 0.08
Nodes (23): compilerOptions, allowArbitraryExtensions, allowImportingTsExtensions, erasableSyntaxOnly, jsx, lib, module, moduleDetection (+15 more)

### Community 24 - "employee-frontend/components.json"
Cohesion: 0.09
Nodes (21): aliases, components, hooks, lib, ui, utils, iconLibrary, menuAccent (+13 more)

### Community 25 - "ModelSettingsStore"
Cohesion: 0.07
Nodes (27): ModelSettingAuditRow, ModelSettingRow, probe(), _iso(), ModelSettingsStore, ModelChoice, ProbeResult, FakeProvider (+19 more)

### Community 26 - "compilerOptions"
Cohesion: 0.09
Nodes (22): compilerOptions, allowArbitraryExtensions, allowImportingTsExtensions, erasableSyntaxOnly, jsx, lib, module, moduleDetection (+14 more)

### Community 27 - "web/src/components/theme-provider.tsx"
Cohesion: 0.10
Nodes (19): App(), controller, disableTransitionsTemporarily(), getSystemTheme(), isEditableTarget(), isTheme(), ResolvedTheme, Theme (+11 more)

### Community 28 - "EmbeddingError"
Cohesion: 0.07
Nodes (44): EmbeddingBatch, EmbeddingError, _nonnegative_number(), OpenAICompatibleEmbedder, OpenRouterEmbedder, _ordered_vectors(), _response_cost(), Embeddings (+36 more)

### Community 29 - "Classify and Extract Prompts"
Cohesion: 0.33
Nodes (7): extract, gemini_classify, Pipeline Graph Orchestration, jev_classify, prepare, GeminiClassifier, JevClassifier

### Community 30 - "test_draft_tools.py"
Cohesion: 0.12
Nodes (30): test_contracts_reject_extra_keys(), test_datetimes_must_be_timezone_aware(), ErrorEmbedder, test_all_eight_tools_and_seven_parallel_calls_execute_only_six(), test_context_copies_input_and_rejects_raising_hard_call_limit(), test_database_faults_remain_distinct_and_record_paid_search_cost(), test_discovered_ref_can_be_inspected_but_not_promoted_to_match(), test_exact_and_fuzzy_queries_are_scoped_and_never_confirm_candidates() (+22 more)

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
Nodes (38): KnowledgeChunk, KnowledgeService, FakeEmbedder, GatedEmbedder, LateEmbedder, PaidEmbedder, test_real_knowledge_search_snapshots_are_isolated_and_json_ready(), count_chunks() (+30 more)

### Community 36 - "web/components.json"
Cohesion: 0.10
Nodes (19): aliases, components, hooks, lib, ui, utils, iconLibrary, menuAccent (+11 more)

### Community 38 - "NewBatchPage.tsx"
Cohesion: 0.08
Nodes (33): Global Constraints, Per-model Evaluation Implementation Plan — Part 3 of 3 (frontend, translations, verification), Task 13: Evaluation types, API client, formatters, copy and report import, Task 15: Provenance, headline metrics, comparison table and empty state, Task 16: Model detail, confusion matrix and predictions drawer, Task 17: Run dialog, progress, page assembly, route and styles, Task 18: Documentation, full verification and manual check, Task 9: Employee app — required phone, queue identity and search, batch entry (+25 more)

### Community 39 - "ui/components.json"
Cohesion: 0.10
Nodes (19): aliases, components, hooks, lib, ui, utils, iconLibrary, menuAccent (+11 more)

### Community 40 - "Settings"
Cohesion: 0.08
Nodes (24): Settings, draft_timeout_s(), env_defaults(), intake_timeout_s(), test_blank_intake_model_is_rejected(), test_non_positive_image_limit_is_rejected(), test_relative_upload_directory_is_rooted_in_the_repository(), _settings() (+16 more)

### Community 41 - "Guided intake interview — design"
Cohesion: 0.06
Nodes (38): QuestionRecord, 1. Question rules (backend), 2. API contract, 3. Chat screen, 4. Review card, Actions, Additional issues, Approach (+30 more)

### Community 43 - "Human Review Gate"
Cohesion: 0.25
Nodes (4): support CLI, Support Workspace UI Plan, Review API, Workspace UI Verification

### Community 44 - "compilerOptions"
Cohesion: 0.12
Nodes (16): compilerOptions, allowImportingTsExtensions, erasableSyntaxOnly, lib, module, moduleDetection, noEmit, noFallthroughCasesInSwitch (+8 more)

### Community 46 - "PipelineState"
Cohesion: 0.11
Nodes (13): DraftResult, _Nodes, Drafter, NullDrafter, UnavailableDrafter, PipelineState, draft(), draft() (+5 more)

### Community 47 - "compilerOptions"
Cohesion: 0.12
Nodes (16): compilerOptions, allowImportingTsExtensions, erasableSyntaxOnly, lib, module, moduleDetection, noEmit, noFallthroughCasesInSwitch (+8 more)

### Community 48 - "locale.tsx"
Cohesion: 0.10
Nodes (23): LanguageToggle(), ModelsPage(), embed, originalLocale, page(), originalLocale, DocumentListProps, knowledgeDocument() (+15 more)

### Community 57 - "parse_document"
Cohesion: 0.13
Nodes (26): TextChunk, _append_chunks(), _check_extracted_size(), DocumentParseError, parse_document(), _parse_pdf(), make_pdf(), test_arabic_text_and_bom_are_preserved() (+18 more)

### Community 58 - "AttachmentStore"
Cohesion: 0.14
Nodes (19): AttachmentStore, ImageRejected, IntakeError, NotOwned, OperationConflict, StaleReview, TurnBusy, png_bytes() (+11 more)

### Community 59 - "contracts.ts"
Cohesion: 0.19
Nodes (29): Task 5: Add complete dependency-free API and persisted-session guards, createIntakeApi(), finiteNonnegative(), INTAKE_FALLBACK_MESSAGE, invalid(), isRecord(), language(), nullableString() (+21 more)

### Community 60 - "fact"
Cohesion: 0.18
Nodes (40): Attachment, InvalidEvidence, merge_analysis(), checked_update(), build_review(), validate_review_numbers(), context(), fact() (+32 more)

### Community 61 - "LLMUnavailable"
Cohesion: 0.09
Nodes (11): LLMUnavailable, Sample, StructuredLLM, DraftProviderResponseError, ExtractedSpan, _Fields, GeminiExtractor, GeminiFields (+3 more)

### Community 62 - "knowledge-view.test.tsx"
Cohesion: 0.23
Nodes (14): acceptIndexRequest(), canRequestIndex(), PendingIndexes, persistPendingIndexes(), pollKnowledge(), refresh(), stop(), PollOptions (+6 more)

### Community 63 - "IntakePage.tsx"
Cohesion: 0.18
Nodes (23): Task 8: Chat screen — instant bubble, typing, reasons, quick replies, composer hints, AgentChat, AgentChatProps, AgentMessage, AssistantText(), AttachedFile, AttachedImage, ChatStatus (+15 more)

### Community 64 - "tasks"
Cohesion: 0.11
Nodes (18): dependsOn, inputs, outputs, cache, persistent, dependsOn, dependsOn, $schema (+10 more)

### Community 65 - "knowledge.py"
Cohesion: 0.08
Nodes (30): session(), _configured(), delete_document(), download_document(), index_document(), list_chunks(), list_documents(), _require_provider() (+22 more)

### Community 66 - "ChangeModelDialog.tsx"
Cohesion: 0.09
Nodes (40): 5.2 Page structure, 5.3 Text and direction, 5.4 Runs pages, 5.5 Import format, 5. Employee-frontend design, ConfirmDialog(), FilterSelect(), Button() (+32 more)

### Community 67 - "fact"
Cohesion: 0.23
Nodes (18): Analysis, ReviewText, _amount(), analyze(), complete_conversation(), _dated(), _message(), _opening() (+10 more)

### Community 68 - "PipelineState"
Cohesion: 0.11
Nodes (18): 10. Remaining demo roadmap, 1. Intent and acceptance criteria, 3. Provider and configuration, 4. Knowledge ingestion and persistence, 5. Retrieval and evidence, 6. Bounded investigation agent, 7. Draft guardrails and failure outcomes, 8. Pipeline, API, CLI and UI integration (+10 more)

### Community 69 - "results.py"
Cohesion: 0.15
Nodes (18): get_result(), list_results(), read_intake_attachment(), review_result(), ReviewInput, ReviewRow, TicketResultRow, TransactionRow (+10 more)

### Community 70 - "make_ticket"
Cohesion: 0.34
Nodes (17): make_output(), make_ticket(), _deps(), _run(), test_concurrency_is_limited(), test_draft_node_never_retries_or_restarts_paid_work(), test_drafter_reasons_escalate(), test_empty_batch() (+9 more)

### Community 71 - "intake/repository.py"
Cohesion: 0.17
Nodes (15): _display_name(), CustomerReview, IntakeAttachmentRow, IntakeMessageRow, attachment_from_row(), customer_review(), load_attachments(), load_messages() (+7 more)

### Community 72 - "RunRow"
Cohesion: 0.15
Nodes (7): get_session(), get_run(), list_runs(), start_run(), BatchInput, columns(), run_view()

### Community 73 - "workspace.py"
Cohesion: 0.38
Nodes (5): health(), insights(), workspace(), knowledge_configured(), latest_results_query()

### Community 74 - "FakeJevRunnable"
Cohesion: 0.29
Nodes (10): FakeJevRunnable, _criteria(), _run(), test_low_top_probability_is_uncertain(), test_one_main_call_with_all_questions(), test_order_check_uses_reversed_options(), test_order_disagreement_is_uncertain(), test_priority_level_maps_to_p_label() (+2 more)

### Community 75 - "normalize.py"
Cohesion: 0.14
Nodes (23): detect_arabizi(), fold_arabic(), has_latin_mix(), _latin_words(), normalize(), sanitize_for_storage(), mask_cards(), test_arabizi_detection() (+15 more)

### Community 76 - "test_workspace_api.py"
Cohesion: 0.14
Nodes (15): review_payload(), start_run(), test_batch_and_queue_expose_real_results(), test_batch_failure_is_isolated_and_conflicting_ids_rejected(), test_customer_profile_lists_the_latest_result_of_each_ticket(), test_only_jev_mode_is_configured_and_retired_modes_are_rejected(), test_progress_counts_only_durable_results_after_save_failure(), fail_one_save() (+7 more)

### Community 77 - "test_interview_api.py"
Cohesion: 0.22
Nodes (18): analyze_calls(), ask(), complete_without_reference(), opening(), opening_with_amount(), reference_answer(), send(), start() (+10 more)

### Community 79 - "devDependencies"
Cohesion: 0.12
Nodes (16): devDependencies, eslint, @eslint/js, eslint-plugin-react-hooks, eslint-plugin-react-refresh, globals, prettier, prettier-plugin-tailwindcss (+8 more)

### Community 80 - "turns.py"
Cohesion: 0.16
Nodes (9): IntakeOperationRow, assert_same_operation(), operation_fingerprint(), sanitize_intake_text(), SubmissionService, _jsonable(), test_changed_payload_cannot_reuse_operation_identity(), Task 1: Record the Baseline and Remove Reference-Verified Dead Code (+1 more)

### Community 81 - "build_tools"
Cohesion: 0.12
Nodes (8): DraftAlreadySubmitted, DraftToolLimit, build_tools(), guarded(), invoke(), _json(), Backend Maintainability Implementation Plan, Global Constraints

### Community 82 - "factory.py"
Cohesion: 0.23
Nodes (8): make_draft_model(), response_payload(), run_provider_pipeline(), send(), search_response(), test_empty_choices_escalates_and_keeps_paid_response_usage(), test_failed_response_id_is_deduplicated_against_earlier_success(), test_other_conversion_value_errors_remain_unexpected()

### Community 83 - "tools.py"
Cohesion: 0.20
Nodes (10): retrieve(), _error_cost(), _Flag, _History, _Input, _Knowledge, _Lookup, _Recent (+2 more)

### Community 84 - "5. Backend design"
Cohesion: 0.25
Nodes (6): 5.1 Dead-code cleanup, 5.2 Extraction ownership, 5.3 Knowledge-service boundary, 5.4 Shared backend boundaries, 5.5 Confirmed backend defect fixes, 5. Backend design

### Community 85 - "scripts"
Cohesion: 0.25
Nodes (8): scripts, build, dev, format, lint, preview, test, typecheck

### Community 87 - "Backend"
Cohesion: 0.33
Nodes (6): Backend, Data model, Employee API, Existing data, Intake, Ticket write paths

### Community 88 - "dependencies"
Cohesion: 0.33
Nodes (6): dependencies, clsx, react, react-dom, tailwind-merge, @workspace/ui

### Community 90 - "@testing-library/react"
Cohesion: 0.40
Nodes (3): @testing-library/jest-dom, @testing-library/react, @testing-library/user-event

### Community 91 - "HTTP contract (implemented in Tasks 4–5)"
Cohesion: 0.50
Nodes (4): HTTP contract (implemented in Tasks 4–5), Task 4: Resumable graph turns, review and customer API, Task 8: Employee evidence panel and processing state, Task 9: End-to-end handoff, live vision evidence and runbook

### Community 93 - "uuid"
Cohesion: 0.22
Nodes (12): command(), create(), test_actual_app_restart_reconciles_failed_placeholder(), test_failed_review_retry_cannot_reopen_submitted_session(), test_original_payload_identity_survives_sanitization(), test_publication_failure_is_retryable_without_restart(), fail_once(), test_receipt_reference_is_preserved() (+4 more)

### Community 94 - "devDependencies"
Cohesion: 0.11
Nodes (19): devDependencies, eslint, @eslint/js, eslint-plugin-react-hooks, eslint-plugin-react-refresh, globals, jsdom, @tailwindcss/vite (+11 more)

### Community 95 - "devDependencies"
Cohesion: 0.17
Nodes (12): devDependencies, eslint, @eslint/js, eslint-plugin-react-hooks, eslint-plugin-react-refresh, globals, tailwindcss, @types/node (+4 more)

### Community 96 - "fakes.py"
Cohesion: 0.21
Nodes (16): FieldPick, FieldExtractor, _field(), fill_gaps(), finalize(), _is_weak(), FakeExtractor, _setup() (+8 more)

### Community 97 - "ticket-flow.ts"
Cohesion: 0.06
Nodes (62): Task 1: Sentence catalog, Task 2: Which step is open, Task 3: Received, produced, and drafting events, Task 4: Mermaid source, Task 5: Draw the charts on the ticket page, 1. Outcome, 2. Scope, 4. Which step is open (+54 more)

### Community 98 - "review.py"
Cohesion: 0.20
Nodes (4): _compact(), _render_value(), _ticket_text(), _tokens()

### Community 99 - "compilerOptions"
Cohesion: 0.14
Nodes (13): compilerOptions, jsx, lib, module, moduleResolution, noEmit, paths, skipLibCheck (+5 more)

### Community 101 - "pydantic"
Cohesion: 0.23
Nodes (6): CitationSource, _Draft, draft_evidence(), _Guardrail, _TraceModel, _validated()

### Community 102 - "dependencies"
Cohesion: 0.12
Nodes (16): dependencies, @base-ui/react, class-variance-authority, cn, @fontsource/tajawal, @fontsource-variable/plus-jakarta-sans, lucide-react, motion (+8 more)

### Community 103 - "InvalidEvidence"
Cohesion: 0.17
Nodes (14): canonical_digits(), normalize_reported_date(), _apply(), _check_reference(), _compact(), _newer_correction(), _normalize_precise(), _validate_fact() (+6 more)

### Community 104 - "dependencies"
Cohesion: 0.20
Nodes (10): dependencies, @base-ui/react, class-variance-authority, cn, @fontsource/tajawal, @fontsource-variable/plus-jakarta-sans, react, react-dom (+2 more)

### Community 105 - "compilerOptions"
Cohesion: 0.17
Nodes (11): compilerOptions, jsx, lib, module, moduleResolution, outDir, skipLibCheck, strict (+3 more)

### Community 106 - "lib/types.ts"
Cohesion: 0.05
Nodes (45): Employee Frontend Maintainability Implementation Plan, Global Constraints, Review Focus, Task 1: Remove reference-verified dead exports, components, and the Mermaid dependency, Task 2: Migrate active TicketFlow coverage, then retire the legacy trace/chart cluster, Task 3: Split RunDetailPage and introduce bounded run-result loading, Task 6: Repair ExtractedField fixtures and make standalone typecheck real, Task 7: Repair employee README paths/test-count guidance and run final acceptance (+37 more)

### Community 107 - "intake/api.ts"
Cohesion: 0.14
Nodes (19): Task 4: Make pending operations discriminated and use one request identity, IntakeApi, fileIdentity(), Attachment, Credentials, CustomerReview, IntakeMessage, MessageCommand (+11 more)

### Community 108 - "test_final_fix_handoff.py"
Cohesion: 0.11
Nodes (22): Passage, process_batch(), Knowledge, assert_completed_evidence(), faulty_knowledge(), read(), outer_deadlines(), PaidEmbeddings (+14 more)

### Community 111 - "scripts"
Cohesion: 0.25
Nodes (8): scripts, build, dev, format, lint, preview, test, typecheck

### Community 112 - "lookup.py"
Cohesion: 0.14
Nodes (16): _as_date(), _iqd_amount(), match_transaction(), TransactionRepo, txn_from_dict(), _ex(), _match(), test_ambiguous_then_disambiguated_by_counterpart() (+8 more)

### Community 113 - "compilerOptions"
Cohesion: 0.29
Nodes (6): compilerOptions, module, moduleResolution, skipLibCheck, strict, target

### Community 114 - "Maintainability and stale-code refactor — design specification"
Cohesion: 0.12
Nodes (15): 10. Verification and acceptance, 1. Outcome and success criteria, 2. Audit baseline, 3. Selected approach and sequence, 4. Boundaries and non-goals, 8.1 Approved deletions, 8.2 Docker and documentation, 8.3 Graphify outputs (+7 more)

### Community 115 - "httpx"
Cohesion: 0.11
Nodes (14): OllamaProvider, _provider(), _tags_handler(), test_catalog_lists_installed_models_with_reported_capabilities(), handler(), test_chat_model_sets_the_configured_context_window(), test_chat_model_targets_the_configured_server(), test_embedder_uses_openai_compatible_endpoint_without_dimensions() (+6 more)

### Community 116 - "web/tsconfig.json"
Cohesion: 0.33
Nodes (5): compilerOptions, paths, files, @workspace/ui/*, references

### Community 117 - "employee-frontend/tsconfig.json"
Cohesion: 0.40
Nodes (4): compilerOptions, paths, files, references

### Community 118 - "exports"
Cohesion: 0.40
Nodes (5): exports, ./components/*, ./globals.css, ./hooks/*, ./lib/*

### Community 119 - "IntakePage.tsx"
Cohesion: 0.06
Nodes (36): Global Constraints, Intake Chat UI Implementation Plan, Task 1: Put the summary and receipt in the thread, Task 2: Put screenshots inside the composer, Task 3: Apply the workspace chat styles, Task 4: Check the page in the browser, Task 8: Intake app UI — phone screen, profile chip, change number, receipt, Task 10: Grouped review card with answer buttons (+28 more)

### Community 120 - "scripts"
Cohesion: 0.50
Nodes (4): scripts, format, lint, typecheck

### Community 122 - "policy.py"
Cohesion: 0.09
Nodes (58): AskedQuestion, IntakeState, PendingQuestion, ProgressItem, Question, Readiness, answer_choices(), answer_kind() (+50 more)

### Community 123 - "TurnContext"
Cohesion: 0.13
Nodes (8): TurnContext, IntakeGraph, _invitation(), grounded_analysis(), grounded_review(), ScriptedIntakeModel, choice_for(), Task 6: Intake uses the configured, per-session model

### Community 125 - "admin.py"
Cohesion: 0.06
Nodes (36): audit(), catalog(), _check_provider(), ChoiceInput, embedding_switch(), ModelOptions, models(), ProbeInput (+28 more)

### Community 126 - "guardrails.py"
Cohesion: 0.09
Nodes (28): Candidate, _add(), find_candidates(), normalize_phone(), _overlaps(), parse_amount(), resolve_date(), _safe_date() (+20 more)

### Community 127 - "test_cli.py"
Cohesion: 0.16
Nodes (8): test_config_error_exits_2(), boom(), test_ingest_directory_is_deterministic_and_duplicate_is_free(), test_ingest_disabled_configuration_never_calls_provider(), test_ingest_failure_exit_and_retry_stored(), test_ingest_invalid_source_does_not_stop_other_files(), test_ingest_limits_batch_without_partial_side_effects(), test_settings_validation_is_safe_field_diagnostic_exit_2()

### Community 128 - "Credentials"
Cohesion: 0.26
Nodes (4): Credentials, SessionView, IntakeService, make_intake_service()

### Community 129 - "intake/model.py"
Cohesion: 0.11
Nodes (28): ImageInput, ModelCall, ModelUnavailable, _analysis_prompt(), _bounded_context(), _guard_size(), IntakeModel, validate() (+20 more)

### Community 130 - "test_llm.py"
Cohesion: 0.11
Nodes (12): StructuredChatLLM, DraftModelInfo, _llm(), _S, test_draft_model_uses_millisecond_timeout_and_disables_sdk_retries(), test_openrouter_reported_cost_takes_precedence_over_token_estimate(), test_openrouter_retry_budget_is_bounded(), test_openrouter_structured_samples_use_configured_key_and_validate_output() (+4 more)

### Community 131 - "intake.py"
Cohesion: 0.17
Nodes (22): ask_question(), create_session(), _credentials(), _dump(), get_session(), post_message(), read_attachment(), remove_attachment() (+14 more)

### Community 132 - "Review Focus"
Cohesion: 0.14
Nodes (13): api(), settings(), Global Constraints, Repository Hygiene Maintainability Implementation Plan, Review Focus, Task 1: Establish the safety baseline and remove tracked Graphify cache contents, Task 2: Delete the superseded architecture HTML after a fresh reference check, Task 3: Remove confirmed stale local runtime state and the duplicate screenshot (+5 more)

### Community 133 - "_DatabaseCall"
Cohesion: 0.09
Nodes (9): _abandoned(), _check_deadline(), _consume(), _DatabaseCall, DocumentNotFoundError, IndexAttemptLostError, KnowledgeError, Task 14: Preserve Safe Knowledge 503s and Log Only Unexpected Diagnostic Types (+1 more)

### Community 134 - "test_dbapi_commit_handoff_arbitrates_cancellation"
Cohesion: 0.47
Nodes (4): test_dbapi_commit_handoff_arbitrates_cancellation(), gate(), gate_before_dbapi(), gate_inside_dbapi()

### Community 137 - "config.py"
Cohesion: 0.06
Nodes (20): Embedder, UnsupportedOperation, _capabilities(), OpenRouterProvider, _per_million(), TypeSafeProvider, eligibility(), Capability (+12 more)

### Community 138 - "intake/test_repository.py"
Cohesion: 0.15
Nodes (14): IntakeSessionRow, InvalidCustomerPhone, IntakeRepository, builder(), test_concurrent_uploads_stop_at_the_session_cap(), attempt(), test_image_bytes_are_decoded_not_trusted(), repo() (+6 more)

### Community 139 - "jev.py"
Cohesion: 0.08
Nodes (35): Candidates, ClassificationResult, ClassifierOutput, NormalizedTicket, Classifier, build_order_check(), build_questions(), build_state() (+27 more)

### Community 140 - "submission.py"
Cohesion: 0.54
Nodes (4): Receipt, IntakeSubmissionRow, SubmissionResult, Ticket

### Community 141 - "db/repository.py"
Cohesion: 0.14
Nodes (4): Base, CustomerRow, IncidentRow, EmbeddingSwitchRow

### Community 142 - "db/repository.py"
Cohesion: 0.15
Nodes (21): _run_with_db(), ensure_customers(), RunRow, create_run(), finish_run(), load_incidents(), load_transactions(), save_outcomes() (+13 more)

### Community 143 - "knowledge_runtime.py"
Cohesion: 0.21
Nodes (4): ConfiguredEmbedder, make_knowledge_service(), _Store, test_configured_embedder_follows_the_current_setting()

### Community 144 - "probe.py"
Cohesion: 0.11
Nodes (13): _chat(), _classify(), _describe(), _draft(), _embed(), _extract(), _intake(), _ProbeAnswer (+5 more)

### Community 148 - "components-ai-thought-chain.tsx"
Cohesion: 0.14
Nodes (16): Status, StatusIcon(), statusStyles, StepContext, StepContextType, ThoughtChain(), ThoughtChainContent(), ThoughtChainItem() (+8 more)

### Community 151 - "pipeline/graph.py"
Cohesion: 0.09
Nodes (33): Decision, ExtractedField, LookupResult, TicketOutcome, TicketExecution, _default_retry(), outcome_from_state(), _percentile() (+25 more)

### Community 152 - "create_app"
Cohesion: 0.10
Nodes (23): init_db(), initialize_database(), make_engine(), make_sessionmaker(), reset_db(), _accepts(), create_app(), intake_failed() (+15 more)

### Community 153 - "main.py"
Cohesion: 0.11
Nodes (15): _safe_dispatch(), recover(), run_job(), fail_intake_placeholders(), reconcile_intake_run(), recover_intake_processing(), dispatch_intake(), test_review_to_employee_handoff() (+7 more)

### Community 154 - "ZainCash support: architecture and ticket flow {#support-overview}"
Cohesion: 0.50
Nodes (3): 1 · System architecture {#system-architecture}, 2 · Ticket flow {#ticket-flow}, ZainCash support: architecture and ticket flow {#support-overview}

### Community 155 - "IntakePage.test.tsx"
Cohesion: 0.09
Nodes (26): Task 6: Customer API client and resumable UI state, Task 7: Bilingual customer chat, screenshots and reviewed submission, copy(), parseJson(), readError(), FakeXHR, session, UploadResult (+18 more)

### Community 156 - "employee-frontend/src/components/theme-provider.tsx"
Cohesion: 0.23
Nodes (11): disableTransitionsTemporarily(), getSystemTheme(), isEditableTarget(), isTheme(), ResolvedTheme, Theme, THEME_VALUES, ThemeProvider() (+3 more)

### Community 157 - "agent.py"
Cohesion: 0.08
Nodes (12): _error_cost(), _Execution, _has_response_usage(), _ModelUsage, _number(), RagDrafter, DraftContext, DraftExecutionError (+4 more)

### Community 158 - "test_taxonomy.py"
Cohesion: 0.14
Nodes (6): most_urgent(), priority_rank(), TaxonomyError, taxonomy(), test_priority_helpers(), test_rejects_unknown_team()

### Community 159 - "TicketRow"
Cohesion: 0.09
Nodes (31): get_customer(), customer_phone_or_none(), InvalidPhone, normalize_customer_phone(), TicketRow, _ticket_phone(), load_jsonl(), load_tickets() (+23 more)

### Community 160 - "test_embedding_switch.py"
Cohesion: 0.13
Nodes (18): make_client(), test_admin_is_disabled_without_a_token(), test_models_and_catalog(), test_non_ascii_and_blank_tokens_are_rejected(), test_save_rejections_change_nothing(), test_test_save_and_audit(), _client(), _documents() (+10 more)

### Community 161 - "Customer phone identity design"
Cohesion: 0.22
Nodes (8): Canonical phone format, Customer phone identity design, Decisions, employee-frontend, Error handling, Intent, Out of scope, Testing

### Community 164 - "ProviderRegistry"
Cohesion: 0.10
Nodes (18): CatalogCache, step_catalog(), OpenRouterChat, provider_errors(), ProviderRegistry, UnknownProvider, BrokenStatusProvider, test_a_provider_whose_status_check_raises_is_listed_as_unreachable() (+10 more)

### Community 165 - "test_workspace_schema.py"
Cohesion: 0.29
Nodes (8): assert_customer_schema(), LegacySchemaError, _nullable(), _table_exists(), upgrade_workspace_schema(), test_fresh_schema_passes_the_customer_check(), test_intake_sessions_without_a_customer_phone_stop_startup(), test_nullable_ticket_phone_stops_startup_with_a_reset_instruction()

### Community 167 - "build_pipeline"
Cohesion: 0.11
Nodes (23): SqlTransactionRepo, build_pipeline(), ConfigError, model_ids(), run_batch(), FakeStructuredLLM, ScriptedChat, _settings() (+15 more)

### Community 168 - "support_test"
Cohesion: 0.04
Nodes (54): ingest(), index_deadlines(), settings(), support_test(), expire_during_embedding(), Fictional RAG walkthrough inputs, Evidence by layer, Known limitations and remaining work (+46 more)

### Community 169 - "intake/contracts.py"
Cohesion: 0.15
Nodes (15): quick_answer(), _aware(), EvidenceRef, Fact, IntakeModel, Message, remove_attachment_evidence(), image_evidence() (+7 more)

### Community 171 - "Deviations from the spec (intentional, small)"
Cohesion: 0.29
Nodes (6): Deviations from the spec (intentional, small), Global Constraints, Per-model Evaluation Implementation Plan — Part 2 of 3 (evaluation engine), Task 11: `support eval` CLI and v2 export, Task 7: Metrics, Task 9: Runner, request validation and cost estimate

### Community 172 - "test_submission.py"
Cohesion: 0.32
Nodes (4): _payload(), test_concurrent_submit_dispatches_once(), test_second_request_id_reuses_the_approved_review(), test_submission_replay_creates_one_ticket()

## Ambiguous Edges - Review These
- `Fraud Report` → `Plan 1 Live Smoke`  [AMBIGUOUS]
  README.md · relation: conceptually_related_to

## Knowledge Gaps
- **83 isolated node(s):** `zaincash-support`, `@base-ui/react`, `@fontsource-variable/plus-jakarta-sans`, `@fontsource/tajawal`, `@tailwindcss/vite` (+78 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 1194 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **29 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Settings` connect `Settings` to `intake/model.py`, `Step`, `test_llm.py`, `Review Focus`, `._metadata`, `pytest`, `config.py`, `intake/test_repository.py`, `test_rag_api.py`, `submission.py`, `db/repository.py`, `db/repository.py`, `knowledge_runtime.py`, `jev.py`, `load_taxonomy`, `test_recovery_regressions.py`, `create_app`, `main.py`, `ModelSettingsStore`, `EmbeddingError`, `agent.py`, `test_draft_tools.py`, `test_embedding_switch.py`, `test_kb_service.py`, `ProviderRegistry`, `test_workspace_schema.py`, `build_pipeline`, `support_test`, `AttachmentStore`, `fact`, `knowledge.py`, `intake/repository.py`, `test_workspace_api.py`, `turns.py`, `factory.py`, `test_final_fix_handoff.py`, `httpx`, `policy.py`, `test_cli.py`?**
  _High betweenness centrality (0.087) - this node is a cross-community bridge._
- **Are the 54 inferred relationships involving `Settings` (e.g. with `_command_settings()` and `_run_in_memory()`) actually correct?**
  _`Settings` has 54 INFERRED edges - model-reasoned connections that need verification._
- **What connects `zaincash-support`, `@base-ui/react`, `@fontsource-variable/plus-jakarta-sans` to the rest of the system?**
  _83 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Step` be split into smaller, more focused modules?**
  _Cohesion score 0.10714285714285714 - nodes in this community are weakly interconnected._
- **Why does `2. Current state` connect `jev.py` to `Card`, `NewBatchPage.tsx`, `build_pipeline`, `load_taxonomy`, `pipeline/graph.py`?**
  _High betweenness centrality (0.086) - this node is a cross-community bridge._
- **Are the 68 inferred relationships involving `Step` (e.g. with `catalog()` and `_check_provider()`) actually correct?**
  _`Step` has 68 INFERRED edges - model-reasoned connections that need verification._

### Low-confidence Hints
_AMBIGUOUS edges — the extractor was unsure. Verify before acting on these._

- **What is the exact relationship between `Fraud Report` and `Plan 1 Live Smoke`?**
  _Edge tagged AMBIGUOUS (relation: conceptually_related_to) - confidence is low._