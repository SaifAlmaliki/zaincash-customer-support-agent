# Graph Report - zaincash-support  (2026-11-14)

## Corpus Check
- 408 files · ~478,891 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 25 file(s) not represented in the graph (top: (none) 15, .jsonl 4, .css 4)

## Summary
- 4102 nodes · 13657 edges · 160 communities (132 shown, 28 thin omitted)
- Extraction: 84% EXTRACTED · 16% INFERRED · 0% AMBIGUOUS · INFERRED: 2117 edges (avg confidence: 0.93)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `b698403e`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- EmbeddingError
- ActiveModels
- pytest
- Button
- investigation.py
- test_admin_api.py
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
- main.py
- compilerOptions
- web/src/components/theme-provider.tsx
- Step
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
- fact
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
- .create
- contracts.ts
- intake/contracts.py
- TicketRow
- knowledge-view.test.tsx
- TicketInput
- tasks
- knowledge.py
- ChangeModelDialog.tsx
- IntakePage.tsx
- PipelineState
- Review Focus
- httpx
- collapsible.tsx
- create_app
- FakeJevRunnable
- pipeline/graph.py
- test_workspace_api.py
- test_interview_api.py
- devDependencies
- cli.py
- build_tools
- FakeProvider
- normalizeCustomerPhone
- ScriptedIntakeModel
- Guided intake interview verification — 2026-11-13
- test_handoff.py
- test_recovery_regressions.py
- Global Constraints
- Customer intake chat layout
- Per-model evaluation (quality, system, cost) — design specification
- devDependencies
- devDependencies
- pipeline/contracts.py
- ticket-flow.ts
- compilerOptions
- StructuredLLM
- dependencies
- review.py
- dependencies
- compilerOptions
- KnowledgeError
- intake/api.ts
- test_final_fix_handoff.py
- pydantic
- scripts
- lookup.py
- compilerOptions
- Maintainability and stale-code refactor — design specification
- 5. Backend design
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
- Settings
- intake.py
- Review Focus
- kb/service.py
- useCopy
- types.py
- pipeline/contracts.py
- intake/repository.py
- scripts
- db/repository.py
- test_steps.py
- probe.py
- components-ai-thought-chain.tsx
- intake/README.md
- taxonomy.py
- make_engine
- ZainCash support: architecture and ticket flow {#support-overview}
- IntakePage.test.tsx
- employee-frontend/src/components/theme-provider.tsx
- tools.py
- test_dbapi_commit_handoff_arbitrates_cancellation
- load_tickets
- EmbeddingSwitches
- Customer phone identity design
- api-entrypoint.sh
- test_workspace_schema.py
- build_pipeline
- support_test
- dependencies
- Deviations from the spec (intentional, small)
- test_submission.py
- setup.ts

## God Nodes (most connected - your core abstractions)
1. `Settings` - 190 edges
2. `Step` - 109 edges
3. `ModelChoice` - 92 edges
4. `KnowledgeService` - 86 edges
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

## Communities (160 total, 28 thin omitted)

### Community 0 - "EmbeddingError"
Cohesion: 0.07
Nodes (43): EmbeddingError, _nonnegative_number(), OpenAICompatibleEmbedder, OpenRouterEmbedder, _ordered_vectors(), _response_cost(), Embeddings, embedder_for() (+35 more)

### Community 1 - "ActiveModels"
Cohesion: 0.12
Nodes (16): ActiveModels, batch_concurrency(), _local_pipeline(), ticket_timeout_s(), test_batch_concurrency_stays_within_bounds(), test_cloud_runs_keep_the_ticket_timeout(), test_local_drafts_get_room_for_their_longer_deadline(), test_local_extract_alone_extends_the_ticket_timeout() (+8 more)

### Community 2 - "pytest"
Cohesion: 0.20
Nodes (36): test_blank_intake_model_is_rejected(), test_non_positive_image_limit_is_rejected(), answer(), draft_state(), script(), drafter(), events(), test_anthropic_fallback_prices_and_provider_cost_precedence() (+28 more)

### Community 3 - "Button"
Cohesion: 0.18
Nodes (18): Backend API contract used here, Button(), buttonVariants, ModelsPage(), embed, originalLocale, page(), UnlockedModels() (+10 more)

### Community 4 - "investigation.py"
Cohesion: 0.14
Nodes (15): DraftToolInputError, _datetime(), _days(), _field(), _involves(), _phone(), _phones(), _record() (+7 more)

### Community 5 - "test_admin_api.py"
Cohesion: 0.43
Nodes (6): make_client(), test_admin_is_disabled_without_a_token(), test_models_and_catalog(), test_non_ascii_and_blank_tokens_are_rejected(), test_save_rejections_change_nothing(), test_test_save_and_audit()

### Community 6 - "Card"
Cohesion: 0.16
Nodes (32): Task 5: Extract presentational DocumentList and KnowledgeReadiness components, 6.4 Focused view extraction, Card(), CardContent(), CardHeader(), CardTitle(), Input(), AdminUnlock() (+24 more)

### Community 7 - "Customer conversation intake for ZainCash support"
Cohesion: 0.06
Nodes (31): 10. Verification and acceptance criteria, 11. Delivery and review, 1. Outcome and agreed requirements, 2. Current implementation and integration points, 3. Approach and boundaries, 4. Conversation state and turn flow, 5. Facts, evidence, and readiness, 6. Language and screenshot behavior (+23 more)

### Community 8 - "lib/api.ts"
Cohesion: 0.05
Nodes (51): Task 2: Migrate active TicketFlow coverage, then retire the legacy trace/chart cluster, Admin model configuration — employee frontend implementation plan, File structure, Global Constraints, Review Focus, Task 1: API types, admin session and admin requests, Task 2: Strings, the AI locality chip, run models and the batch switch message, Task 3: Model choice logic and the change dialog (+43 more)

### Community 9 - "IntakeController"
Cohesion: 0.12
Nodes (20): Task 6: Customer API client and resumable UI state, Task 7: Bilingual customer chat, screenshots and reviewed submission, Task 1: Cleanup-first removal of reference-verified dead code and dependencies, Task 4: Make pending operations discriminated and use one request identity, Task 7: Preserve resume-unavailable state across `startNew`, Task 7: Intake app data layer — phone helper, contracts, API, controller, Task 7: Customer frontend data layer, copy() (+12 more)

### Community 10 - "FakeJevRunnable"
Cohesion: 0.13
Nodes (18): CredentialCheck, DegradedCredentialChecker, _finite_nonnegative(), _get(), JevCredentialChecker, ResponseRunnable, test_bad_usage_cannot_poison_cost(), test_cancellation_propagates_with_cost_for_outer_timeout_owner() (+10 more)

### Community 11 - "test_rag_api.py"
Cohesion: 0.12
Nodes (22): client(), evidence_client(), kb_env(), test_actual_guardrail_failure_is_separate_from_reply(), test_concurrent_index_requests_share_active_work(), test_disabled_or_missing_provider_stores_without_indexing(), test_explicit_retry_tags_search_and_chunk_pagination(), test_health_distinguishes_failed_from_empty() (+14 more)

### Community 12 - "employee-frontend/package.json"
Cohesion: 0.06
Nodes (30): @base-ui/react, class-variance-authority, cn, eslint, @eslint/js, eslint-plugin-react-hooks, eslint-plugin-react-refresh, @fontsource/tajawal (+22 more)

### Community 14 - "QueuePage.tsx"
Cohesion: 0.13
Nodes (44): Task 3: Split RunDetailPage and introduce bounded run-result loading, Task 16: Model detail, confusion matrix and predictions drawer, Task 10: Employee app — customer page and ticket header link, Task 9: Employee app — required phone, queue identity and search, batch entry, 6.4 Visible to all employees, 5.1 Data access, EmptyState(), ErrorState() (+36 more)

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
Cohesion: 0.08
Nodes (45): build_graph(), PipelineDeps, InMemoryTransactionRepo, load_taxonomy(), FakeClassifier, make_output(), make_ticket(), pipeline() (+37 more)

### Community 20 - "test_draft_guardrails.py"
Cohesion: 0.13
Nodes (28): LookupResult, check_draft(), requests_credentials(), check(), state(), test_aggregation_is_deduplicated_and_has_no_state_side_effects(), test_amount_occurrences_keep_their_own_currency_and_sign(), test_avoid_sharing_warning_does_not_excuse_a_later_request() (+20 more)

### Community 21 - "web/package.json"
Cohesion: 0.08
Nodes (25): clsx, jsdom, tailwind-merge, @testing-library/user-event, @workspace/ui, eslint, @eslint/js, eslint-plugin-react-hooks (+17 more)

### Community 22 - "test_interview_scenarios.py"
Cohesion: 0.31
Nodes (9): analyze_calls(), Chat, source_of(), summary(), test_complete_report_goes_straight_to_review(), test_no_reference_number_still_gives_a_complete_report(), test_vague_report_is_interviewed_into_a_complete_ticket(), updates() (+1 more)

### Community 23 - "compilerOptions"
Cohesion: 0.08
Nodes (23): compilerOptions, allowArbitraryExtensions, allowImportingTsExtensions, erasableSyntaxOnly, jsx, lib, module, moduleDetection (+15 more)

### Community 24 - "employee-frontend/components.json"
Cohesion: 0.09
Nodes (21): aliases, components, hooks, lib, ui, utils, iconLibrary, menuAccent (+13 more)

### Community 25 - "main.py"
Cohesion: 0.09
Nodes (11): get_session(), Base, IncidentRow, TransactionRow, EmbeddingSwitchRow, ModelSettingAuditRow, ModelSettingRow, _store() (+3 more)

### Community 26 - "compilerOptions"
Cohesion: 0.09
Nodes (22): compilerOptions, allowArbitraryExtensions, allowImportingTsExtensions, erasableSyntaxOnly, jsx, lib, module, moduleDetection (+14 more)

### Community 27 - "web/src/components/theme-provider.tsx"
Cohesion: 0.10
Nodes (19): App(), controller, disableTransitionsTemporarily(), getSystemTheme(), isEditableTarget(), isTheme(), ResolvedTheme, Theme (+11 more)

### Community 28 - "Step"
Cohesion: 0.09
Nodes (24): CatalogCache, step_catalog(), ConfiguredEmbedder, _Store, eligibility(), ProviderStatus, Step, fake_registry() (+16 more)

### Community 29 - "Classify and Extract Prompts"
Cohesion: 0.33
Nodes (7): extract, gemini_classify, Pipeline Graph Orchestration, jev_classify, prepare, GeminiClassifier, JevClassifier

### Community 30 - "test_draft_tools.py"
Cohesion: 0.12
Nodes (28): ErrorEmbedder, settings(), test_all_eight_tools_and_seven_parallel_calls_execute_only_six(), test_context_copies_input_and_rejects_raising_hard_call_limit(), test_database_faults_remain_distinct_and_record_paid_search_cost(), test_discovered_ref_can_be_inspected_but_not_promoted_to_match(), test_exact_and_fuzzy_queries_are_scoped_and_never_confirm_candidates(), test_exact_reference_still_requires_customer_and_excludes_future() (+20 more)

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
Nodes (37): KnowledgeChunk, KnowledgeService, FakeEmbedder, GatedEmbedder, LateEmbedder, PaidEmbedder, count_chunks(), test_category_filters_include_general_policies_and_validate_tags() (+29 more)

### Community 36 - "web/components.json"
Cohesion: 0.10
Nodes (19): aliases, components, hooks, lib, ui, utils, iconLibrary, menuAccent (+11 more)

### Community 38 - "NewBatchPage.tsx"
Cohesion: 0.06
Nodes (41): Global Constraints, Per-model Evaluation Implementation Plan — Part 3 of 3 (frontend, translations, verification), Task 14: Evaluation view helpers, Task 15: Provenance, headline metrics, comparison table and empty state, Task 17: Run dialog, progress, page assembly, route and styles, Task 18: Documentation, full verification and manual check, 6.1 Route and access, 6.2 Page (+33 more)

### Community 39 - "ui/components.json"
Cohesion: 0.10
Nodes (19): aliases, components, hooks, lib, ui, utils, iconLibrary, menuAccent (+11 more)

### Community 40 - "fact"
Cohesion: 0.14
Nodes (48): Question, ReviewText, choose_question(), build_review(), validate_review_numbers(), context(), fact(), message() (+40 more)

### Community 41 - "Guided intake interview — design"
Cohesion: 0.07
Nodes (28): 2. API contract, 3. Chat screen, 4. Review card, Actions, Additional issues, Approach, Composer hints, Copy (+20 more)

### Community 43 - "Human Review Gate"
Cohesion: 0.25
Nodes (4): support CLI, Support Workspace UI Plan, Review API, Workspace UI Verification

### Community 44 - "compilerOptions"
Cohesion: 0.12
Nodes (16): compilerOptions, allowImportingTsExtensions, erasableSyntaxOnly, lib, module, moduleDetection, noEmit, noFallthroughCasesInSwitch (+8 more)

### Community 46 - "PipelineState"
Cohesion: 0.24
Nodes (5): _Nodes, PipelineState, Global Constraints, Ticket Flow Charts Implementation Plan, 3. What the employee sees

### Community 47 - "compilerOptions"
Cohesion: 0.12
Nodes (16): compilerOptions, allowImportingTsExtensions, erasableSyntaxOnly, lib, module, moduleDetection, noEmit, noFallthroughCasesInSwitch (+8 more)

### Community 48 - "AI usage and performance dashboard (`/evaluation`) — design specification"
Cohesion: 0.11
Nodes (18): recent(), 10. Phase 2 (for reference, not designed here), 1. Outcome and success criteria, 2. Current state, 3. Decisions, 4.2 Processes, 4.5 Prices for estimates, 4.6 Reporting API (+10 more)

### Community 57 - "parse_document"
Cohesion: 0.12
Nodes (27): TextChunk, _append_chunks(), _check_extracted_size(), DocumentParseError, parse_document(), _parse_pdf(), make_pdf(), test_arabic_text_and_bom_are_preserved() (+19 more)

### Community 58 - ".create"
Cohesion: 0.08
Nodes (31): AttachmentStore, Credentials, SessionView, IntakeSessionRow, ImageRejected, InvalidCustomerPhone, NotOwned, IntakeRepository (+23 more)

### Community 59 - "contracts.ts"
Cohesion: 0.17
Nodes (34): Task 5: Add complete dependency-free API and persisted-session guards, createIntakeApi(), ANSWER_KINDS, CHOICES, FACT_STATUSES, finiteNonnegative(), invalid(), isRecord() (+26 more)

### Community 60 - "intake/contracts.py"
Cohesion: 0.09
Nodes (44): quick_answer(), Analysis, Attachment, _aware(), CustomerReview, EvidenceRef, Fact, IntakeModel (+36 more)

### Community 61 - "TicketRow"
Cohesion: 0.07
Nodes (43): get_customer(), get_result(), list_results(), read_intake_attachment(), review_result(), ReviewInput, health(), insights() (+35 more)

### Community 62 - "knowledge-view.test.tsx"
Cohesion: 0.25
Nodes (13): acceptIndexRequest(), canRequestIndex(), PendingIndexes, persistPendingIndexes(), pollKnowledge(), refresh(), stop(), PollOptions (+5 more)

### Community 64 - "tasks"
Cohesion: 0.11
Nodes (18): dependsOn, inputs, outputs, cache, persistent, dependsOn, dependsOn, $schema (+10 more)

### Community 65 - "knowledge.py"
Cohesion: 0.10
Nodes (27): session(), _configured(), delete_document(), download_document(), index_document(), list_chunks(), list_documents(), _require_provider() (+19 more)

### Community 66 - "ChangeModelDialog.tsx"
Cohesion: 0.15
Nodes (28): ConfirmDialog(), Dialog(), DialogContent(), DialogDescription(), DialogFooter(), DialogHeader(), DialogOverlay(), DialogPortal() (+20 more)

### Community 67 - "IntakePage.tsx"
Cohesion: 0.06
Nodes (65): Task 1: Put the summary and receipt in the thread, Task 8: Chat screen — instant bubble, typing, reasons, quick replies, composer hints, Task 9: Progress strip, 4. Components, 7.1 Verification and cleanup, 7.2 Runtime contracts and persisted operations, 7.3 Upload lifecycle, 7.4 Controller, chat, and tests (+57 more)

### Community 68 - "PipelineState"
Cohesion: 0.11
Nodes (18): 10. Remaining demo roadmap, 1. Intent and acceptance criteria, 3. Provider and configuration, 4. Knowledge ingestion and persistence, 5. Retrieval and evidence, 6. Bounded investigation agent, 7. Draft guardrails and failure outcomes, 8. Pipeline, API, CLI and UI integration (+10 more)

### Community 69 - "Review Focus"
Cohesion: 0.29
Nodes (5): test_entry_points_upgrade_legacy_run_status(), test_result_list_paginates_filters_and_run_id(), Review Focus, Task 13: Finish Physical Unlink on Completed Attachment-Removal Replay, Task 15: Run Complete Backend Verification and Review the Final Diff

### Community 70 - "httpx"
Cohesion: 0.10
Nodes (14): OllamaProvider, _provider(), _tags_handler(), test_catalog_lists_installed_models_with_reported_capabilities(), handler(), test_chat_model_sets_the_configured_context_window(), test_chat_model_targets_the_configured_server(), test_embedder_uses_openai_compatible_endpoint_without_dimensions() (+6 more)

### Community 73 - "create_app"
Cohesion: 0.21
Nodes (12): create_app(), intake_failed(), build(), _client(), _documents(), test_failed_documents_are_listed(), test_run_start_locks_the_switch_table_before_its_first_write(), test_runs_are_blocked_while_a_switch_runs_and_restart_recovers() (+4 more)

### Community 74 - "FakeJevRunnable"
Cohesion: 0.29
Nodes (10): FakeJevRunnable, _criteria(), _run(), test_low_top_probability_is_uncertain(), test_one_main_call_with_all_questions(), test_order_check_uses_reversed_options(), test_order_disagreement_is_uncertain(), test_priority_level_maps_to_p_label() (+2 more)

### Community 75 - "pipeline/graph.py"
Cohesion: 0.06
Nodes (16): DraftResult, _default_retry(), _percentile(), _retryable(), _number(), DraftToolLimit, CredentialChecker, Drafter (+8 more)

### Community 76 - "test_workspace_api.py"
Cohesion: 0.12
Nodes (18): reset_db(), client(), review_payload(), start_run(), test_batch_and_queue_expose_real_results(), test_batch_failure_is_isolated_and_conflicting_ids_rejected(), test_customer_profile_lists_the_latest_result_of_each_ticket(), test_health_reports_ai_locality_and_runs_record_provider_refs() (+10 more)

### Community 77 - "test_interview_api.py"
Cohesion: 0.21
Nodes (19): analyze_calls(), ask(), complete_without_reference(), opening(), opening_with_amount(), reference_answer(), send(), start() (+11 more)

### Community 79 - "devDependencies"
Cohesion: 0.12
Nodes (16): devDependencies, eslint, @eslint/js, eslint-plugin-react-hooks, eslint-plugin-react-refresh, globals, prettier, prettier-plugin-tailwindcss (+8 more)

### Community 80 - "cli.py"
Cohesion: 0.10
Nodes (21): _command_settings(), ingest_kb_cmd(), init_db_cmd(), Mode, run_batch_cmd(), _run_in_memory(), _run_with_db(), seed_db_cmd() (+13 more)

### Community 81 - "build_tools"
Cohesion: 0.12
Nodes (7): build_tools(), retrieve(), _error_cost(), Backend Maintainability Implementation Plan, Global Constraints, Global Constraints, Repository Hygiene Maintainability Implementation Plan

### Community 82 - "FakeProvider"
Cohesion: 0.09
Nodes (18): probe(), ModelChoice, ProbeResult, _registry(), StructuredChat, test_draft_probe_requires_a_correct_tool_call(), test_embed_and_classify_probes(), test_every_step_has_a_probe() (+10 more)

### Community 83 - "normalizeCustomerPhone"
Cohesion: 0.13
Nodes (15): Employee Frontend Maintainability Implementation Plan, Global Constraints, Review Focus, Task 1: Remove reference-verified dead exports, components, and the Mermaid dependency, Task 4: Extract and test the pure queue projection, Task 6: Repair ExtractedField fixtures and make standalone typecheck real, Task 7: Repair employee README paths/test-count guidance and run final acceptance, SelectSeparator() (+7 more)

### Community 84 - "ScriptedIntakeModel"
Cohesion: 0.22
Nodes (6): grounded_analysis(), grounded_review(), ScriptedIntakeModel, HTTP contract (implemented in Tasks 4–5), Task 4: Resumable graph turns, review and customer API, Task 9: End-to-end handoff, live vision evidence and runbook

### Community 85 - "Guided intake interview verification — 2026-11-13"
Cohesion: 0.20
Nodes (9): Arabic at 390×844, starting from the vague message, English at 1280×900, with the complete message, Final automated checks, Guided intake interview verification — 2026-11-13, Live browser run, Live probe output (facts only), Live transfer probe, Observations (+1 more)

### Community 86 - "test_handoff.py"
Cohesion: 0.19
Nodes (15): _amount(), analyze(), complete_conversation(), _dated(), _message(), _opening(), _png(), _review() (+7 more)

### Community 87 - "test_recovery_regressions.py"
Cohesion: 0.24
Nodes (12): command(), create(), test_actual_app_restart_reconciles_failed_placeholder(), test_failed_review_retry_cannot_reopen_submitted_session(), test_original_payload_identity_survives_sanitization(), test_publication_failure_is_retryable_without_restart(), fail_once(), test_receipt_reference_is_preserved() (+4 more)

### Community 89 - "Global Constraints"
Cohesion: 0.33
Nodes (5): Global Constraints, Intake Chat UI Implementation Plan, Task 2: Put screenshots inside the composer, Task 3: Apply the workspace chat styles, Task 4: Check the page in the browser

### Community 90 - "Customer intake chat layout"
Cohesion: 0.25
Nodes (6): Task 10: Grouped review card with answer buttons, 1. Outcome, 2. Scope, 3. Layout, 5. Checks, Customer intake chat layout

### Community 92 - "Per-model evaluation (quality, system, cost) — design specification"
Cohesion: 0.20
Nodes (9): 1. Outcome and success criteria, 3. Decisions, 5.3 Text and direction, 5.4 Runs pages, 5.5 Import format, 5. Employee-frontend design, 6. Error handling, 8. Out of scope (+1 more)

### Community 94 - "devDependencies"
Cohesion: 0.11
Nodes (19): devDependencies, eslint, @eslint/js, eslint-plugin-react-hooks, eslint-plugin-react-refresh, globals, jsdom, @tailwindcss/vite (+11 more)

### Community 95 - "devDependencies"
Cohesion: 0.17
Nodes (12): devDependencies, eslint, @eslint/js, eslint-plugin-react-hooks, eslint-plugin-react-refresh, globals, tailwindcss, @types/node (+4 more)

### Community 96 - "pipeline/contracts.py"
Cohesion: 0.12
Nodes (27): LLMUnavailable, FieldPick, NormalizedTicket, FieldExtractor, _field(), fill_gaps(), finalize(), _is_weak() (+19 more)

### Community 97 - "ticket-flow.ts"
Cohesion: 0.06
Nodes (63): Task 1: Sentence catalog, Task 2: Which step is open, Task 3: Received, produced, and drafting events, Task 4: Mermaid source, Task 5: Draw the charts on the ticket page, 1. Outcome, 2. Scope, 4. Which step is open (+55 more)

### Community 99 - "compilerOptions"
Cohesion: 0.14
Nodes (13): compilerOptions, jsx, lib, module, moduleResolution, noEmit, paths, skipLibCheck (+5 more)

### Community 100 - "StructuredLLM"
Cohesion: 0.29
Nodes (3): Sample, StructuredLLM, Task 6: Ticket text generation, verification, `support eval-generate` and data card

### Community 102 - "dependencies"
Cohesion: 0.12
Nodes (16): dependencies, @base-ui/react, class-variance-authority, cn, @fontsource/tajawal, @fontsource-variable/plus-jakarta-sans, lucide-react, motion (+8 more)

### Community 103 - "review.py"
Cohesion: 0.17
Nodes (11): canonical_digits(), normalize_reported_date(), _compact(), _render_value(), _ticket_text(), _tokens(), test_ambiguous_slash_date_is_not_fabricated(), test_named_weekday_resolves_to_the_latest_matching_day() (+3 more)

### Community 104 - "dependencies"
Cohesion: 0.20
Nodes (10): dependencies, @base-ui/react, class-variance-authority, cn, @fontsource/tajawal, @fontsource-variable/plus-jakarta-sans, react, react-dom (+2 more)

### Community 105 - "compilerOptions"
Cohesion: 0.17
Nodes (11): compilerOptions, jsx, lib, module, moduleResolution, outDir, skipLibCheck, strict (+3 more)

### Community 106 - "KnowledgeError"
Cohesion: 0.09
Nodes (7): _DatabaseCall, _Claim, DocumentNotFoundError, IndexAttemptLostError, KnowledgeError, KnowledgeExecutionError, Task 14: Preserve Safe Knowledge 503s and Log Only Unexpected Diagnostic Types

### Community 107 - "intake/api.ts"
Cohesion: 0.10
Nodes (22): IntakeApi, ANSWER_KINDS, INTAKE_FALLBACK_MESSAGE, Activity, ControllerState, fileIdentity(), AnswerKind, AskCommand (+14 more)

### Community 108 - "test_final_fix_handoff.py"
Cohesion: 0.08
Nodes (28): RagDrafter, _tool_chat(), call(), Checker, ScriptedChat, submit(), assert_completed_evidence(), faulty_knowledge() (+20 more)

### Community 110 - "pydantic"
Cohesion: 0.23
Nodes (6): CitationSource, _Draft, draft_evidence(), _Guardrail, _TraceModel, _validated()

### Community 111 - "scripts"
Cohesion: 0.25
Nodes (8): scripts, build, dev, format, lint, preview, test, typecheck

### Community 112 - "lookup.py"
Cohesion: 0.17
Nodes (16): ExtractedField, _as_date(), _iqd_amount(), match_transaction(), TransactionRepo, state(), _ex(), _match() (+8 more)

### Community 113 - "compilerOptions"
Cohesion: 0.29
Nodes (6): compilerOptions, module, moduleResolution, skipLibCheck, strict, target

### Community 114 - "Maintainability and stale-code refactor — design specification"
Cohesion: 0.12
Nodes (15): 10. Verification and acceptance, 1. Outcome and success criteria, 2. Audit baseline, 3. Selected approach and sequence, 4. Boundaries and non-goals, 8.1 Approved deletions, 8.2 Docker and documentation, 8.3 Graphify outputs (+7 more)

### Community 115 - "5. Backend design"
Cohesion: 0.29
Nodes (5): 5.1 Dead-code cleanup, 5.3 Knowledge-service boundary, 5.4 Shared backend boundaries, 5.5 Confirmed backend defect fixes, 5. Backend design

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
Cohesion: 0.11
Nodes (38): AskedQuestion, IntakeState, answer_choices(), answer_kind(), ask_for(), ask_once_keys(), asked_count(), asks_for_secret() (+30 more)

### Community 123 - "TurnContext"
Cohesion: 0.12
Nodes (16): QuestionRecord, TurnContext, TurnResult, IntakeGraph, _invitation(), test_graph_budget_uses_the_pinned_choice_and_timeout(), test_pin_failure_is_reported_as_model_unavailable(), test_without_pinning_the_budget_uses_settings() (+8 more)

### Community 125 - "admin.py"
Cohesion: 0.12
Nodes (20): audit(), catalog(), _check_provider(), ChoiceInput, embedding_switch(), ModelOptions, models(), ProbeInput (+12 more)

### Community 126 - "guardrails.py"
Cohesion: 0.07
Nodes (45): Candidate, _add(), find_candidates(), normalize_phone(), _overlaps(), parse_amount(), resolve_date(), _safe_date() (+37 more)

### Community 129 - "intake/model.py"
Cohesion: 0.11
Nodes (30): ImageInput, ModelCall, ModelUnavailable, _analysis_prompt(), _bounded_context(), _guard_size(), IntakeModel, validate() (+22 more)

### Community 130 - "Settings"
Cohesion: 0.05
Nodes (30): get_settings(), Settings, StructuredChatLLM, make_draft_model(), make_gemini_llm(), model_ids(), DraftModelInfo, _current_models() (+22 more)

### Community 131 - "intake.py"
Cohesion: 0.15
Nodes (22): ask_question(), create_session(), _credentials(), _dump(), get_session(), post_message(), read_attachment(), remove_attachment() (+14 more)

### Community 132 - "Review Focus"
Cohesion: 0.12
Nodes (16): api(), Review Focus, Task 1: Establish the safety baseline and remove tracked Graphify cache contents, Task 2: Delete the superseded architecture HTML after a fresh reference check, Task 3: Remove confirmed stale local runtime state and the duplicate screenshot, Task 4: Repair only current setup and processing documentation, Task 5: Restrict Docker build context without deleting installed dependencies, Task 6: Regenerate current Graphify outputs as the final mutating task (+8 more)

### Community 133 - "kb/service.py"
Cohesion: 0.09
Nodes (13): Embedder, EmbeddingBatch, Passage, SearchResult, _abandoned(), _check_deadline(), _consume(), _error_cost() (+5 more)

### Community 135 - "useCopy"
Cohesion: 0.16
Nodes (26): Task 8: Employee evidence panel and processing state, Task 12: Locale parity test and translated Runs pages, Confidence(), intakeFixture, factValue(), IntakeEvidence(), ReportedDetails(), Screenshot() (+18 more)

### Community 137 - "types.py"
Cohesion: 0.05
Nodes (26): UnsupportedOperation, _capabilities(), DraftProviderResponseError, OpenRouterChat, OpenRouterProvider, _per_million(), provider_errors(), ProviderRegistry (+18 more)

### Community 139 - "pipeline/contracts.py"
Cohesion: 0.10
Nodes (26): Candidates, ClassificationResult, ClassifierOutput, Classifier, build_order_check(), build_questions(), build_state(), category_criteria() (+18 more)

### Community 140 - "intake/repository.py"
Cohesion: 0.09
Nodes (40): _display_name(), OperationClaim, Receipt, ReviewSnapshot, IntakeAttachmentRow, IntakeMessageRow, IntakeOperationRow, IntakeSubmissionRow (+32 more)

### Community 141 - "scripts"
Cohesion: 0.25
Nodes (8): scripts, build, dev, format, lint, preview, test, typecheck

### Community 142 - "db/repository.py"
Cohesion: 0.06
Nodes (54): _safe_dispatch(), get_run(), list_runs(), start_run(), BatchInput, ensure_customers(), parse_dt(), RunRow (+46 more)

### Community 143 - "test_steps.py"
Cohesion: 0.16
Nodes (12): draft_timeout_s(), env_defaults(), intake_timeout_s(), choice_for(), _Store, _settings(), test_eligibility(), test_env_defaults_match_todays_settings() (+4 more)

### Community 144 - "probe.py"
Cohesion: 0.08
Nodes (19): _chat(), _classify(), _describe(), _draft(), _embed(), _extract(), _intake(), _ProbeAnswer (+11 more)

### Community 148 - "components-ai-thought-chain.tsx"
Cohesion: 0.15
Nodes (15): Status, StatusIcon(), statusStyles, StepContext, StepContextType, ThoughtChain(), ThoughtChainContent(), ThoughtChainItem() (+7 more)

### Community 151 - "taxonomy.py"
Cohesion: 0.10
Nodes (24): Decision, decide(), empty_ticket_decision(), merge_reasons(), note_for(), _unique(), Category, most_urgent() (+16 more)

### Community 152 - "make_engine"
Cohesion: 0.12
Nodes (10): make_engine(), make_sessionmaker(), intake_client(), intake_db(), reviewed(), env(), env(), ingest_env() (+2 more)

### Community 154 - "ZainCash support: architecture and ticket flow {#support-overview}"
Cohesion: 0.50
Nodes (3): 1 · System architecture {#system-architecture}, 2 · Ticket flow {#ticket-flow}, ZainCash support: architecture and ticket flow {#support-overview}

### Community 155 - "IntakePage.test.tsx"
Cohesion: 0.07
Nodes (31): Task 8: Intake app UI — phone screen, profile chip, change number, receipt, @testing-library/react, parseJson(), readError(), FakeXHR, session, UploadResult, IntakeRequestError (+23 more)

### Community 156 - "employee-frontend/src/components/theme-provider.tsx"
Cohesion: 0.23
Nodes (11): disableTransitionsTemporarily(), getSystemTheme(), isEditableTarget(), isTheme(), ResolvedTheme, Theme, THEME_VALUES, ThemeProvider() (+3 more)

### Community 157 - "tools.py"
Cohesion: 0.06
Nodes (23): _error_cost(), _Execution, _has_response_usage(), _ModelUsage, DraftAlreadySubmitted, DraftContext, DraftSubmission, _bounded() (+15 more)

### Community 158 - "test_dbapi_commit_handoff_arbitrates_cancellation"
Cohesion: 0.47
Nodes (4): test_dbapi_commit_handoff_arbitrates_cancellation(), gate(), gate_before_dbapi(), gate_inside_dbapi()

### Community 159 - "load_tickets"
Cohesion: 0.12
Nodes (14): load_jsonl(), load_tickets(), _rows(), test_csv_with_bom_and_missing_columns(), test_duplicate_external_ids_keep_first(), test_invalid_phone_names_the_row(), test_json_object_without_ids(), test_jsonl_fixture_loads() (+6 more)

### Community 160 - "EmbeddingSwitches"
Cohesion: 0.08
Nodes (18): EmbeddingSwitches, _view(), Task 8: Live model tests and the model catalog, Task 4: The Models page, navigation and route, 4.3 Storage, 4.8 Embedding switch (short pause), 4.10 API, 4.11 CLI (+10 more)

### Community 161 - "Customer phone identity design"
Cohesion: 0.14
Nodes (13): Backend, Customer phone identity design, Data model, Decisions, Employee API, employee-frontend, Error handling, Existing data (+5 more)

### Community 165 - "test_workspace_schema.py"
Cohesion: 0.22
Nodes (10): assert_customer_schema(), LegacySchemaError, _nullable(), _table_exists(), upgrade_workspace_schema(), engine(), test_fresh_schema_passes_the_customer_check(), test_intake_sessions_without_a_customer_phone_stop_startup() (+2 more)

### Community 167 - "build_pipeline"
Cohesion: 0.15
Nodes (21): build_pipeline(), ConfigError, run_batch(), FakeStructuredLLM, Knowledge, test_config_error_exits_2(), boom(), _settings() (+13 more)

### Community 168 - "support_test"
Cohesion: 0.04
Nodes (55): ingest(), index_deadlines(), settings(), support_test(), expire_during_embedding(), Fictional RAG walkthrough inputs, Evidence by layer, Known limitations and remaining work (+47 more)

### Community 169 - "dependencies"
Cohesion: 0.33
Nodes (6): dependencies, clsx, react, react-dom, tailwind-merge, @workspace/ui

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
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 1226 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **28 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Settings` connect `Settings` to `EmbeddingError`, `intake/model.py`, `ActiveModels`, `pytest`, `kb/service.py`, `test_admin_api.py`, `types.py`, `test_rag_api.py`, `intake/repository.py`, `pipeline/contracts.py`, `db/repository.py`, `test_steps.py`, `probe.py`, `make_output`, `make_engine`, `main.py`, `Step`, `test_draft_tools.py`, `test_kb_service.py`, `test_workspace_schema.py`, `build_pipeline`, `fact`, `support_test`, `.create`, `Review Focus`, `httpx`, `create_app`, `pipeline/graph.py`, `test_workspace_api.py`, `cli.py`, `FakeProvider`, `test_final_fix_handoff.py`, `TurnContext`, `admin.py`?**
  _High betweenness centrality (0.093) - this node is a cross-community bridge._
- **Are the 55 inferred relationships involving `Settings` (e.g. with `_command_settings()` and `_run_in_memory()`) actually correct?**
  _`Settings` has 55 INFERRED edges - model-reasoned connections that need verification._
- **What connects `zaincash-support`, `@base-ui/react`, `@fontsource-variable/plus-jakarta-sans` to the rest of the system?**
  _83 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `EmbeddingError` be split into smaller, more focused modules?**
  _Cohesion score 0.07283702213279677 - nodes in this community are weakly interconnected._
- **Why does `Choice` connect `IntakePage.test.tsx` to `probe.py`, `IntakeController`, `policy.py`, `intake/api.ts`?**
  _High betweenness centrality (0.062) - this node is a cross-community bridge._
- **Are the 69 inferred relationships involving `Step` (e.g. with `catalog()` and `_check_provider()`) actually correct?**
  _`Step` has 69 INFERRED edges - model-reasoned connections that need verification._

### Low-confidence Hints
_AMBIGUOUS edges — the extractor was unsure. Verify before acting on these._

- **What is the exact relationship between `Fraud Report` and `Plan 1 Live Smoke`?**
  _Edge tagged AMBIGUOUS (relation: conceptually_related_to) - confidence is low._