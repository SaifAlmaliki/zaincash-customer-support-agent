# Graph Report - zaincash-support  (2026-11-13)

## Corpus Check
- 425 files · ~420,098 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 27 file(s) not represented in the graph (top: (none) 17, .jsonl 4, .css 4)

## Summary
- 3935 nodes · 12854 edges · 180 communities (139 shown, 41 thin omitted)
- Extraction: 85% EXTRACTED · 15% INFERRED · 0% AMBIGUOUS · INFERRED: 1868 edges (avg confidence: 0.93)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `295b9e08`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- NewBatchPage.tsx
- Step
- pytest
- TurnStore
- investigation.py
- pipeline/graph.py
- Card
- Customer conversation intake for ZainCash support
- lib/types.ts
- IntakeController
- FakeJevRunnable
- test_rag_api.py
- employee-frontend/package.json
- QueuePage.tsx
- Support Taxonomy Categories
- ui/package.json
- locale.tsx
- users-frontend/package.json
- make_ticket
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
- ChangeModelDialog.tsx
- ui/components.json
- Settings
- fact
- Vite Config
- Human Review Gate
- compilerOptions
- PipelineState
- compilerOptions
- Plan 3 RAG Drafting Implementation Plan
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
- taxonomy.py
- pipeline/contracts.py
- DocumentList.tsx
- intake/types.ts
- tasks
- knowledge.py
- intake/contracts.py
- test_handoff.py
- PipelineState
- results.py
- make_ticket
- intake/repository.py
- Credentials
- ConfiguredEmbedder
- FakeJevRunnable
- test-kb/README.md
- test_workspace_api.py
- KnowledgeService
- devDependencies
- judge-demo.ar.md
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
- test_recovery_regressions.py
- devDependencies
- devDependencies
- FieldPick
- ticket-flow.ts
- review.py
- compilerOptions
- قواعد المعرفة العربية للعرض أمام لجنة التحكيم
- pydantic
- dependencies
- InvalidEvidence
- dependencies
- compilerOptions
- ref_vitest
- IntakePage.test.tsx
- test_final_fix_handoff.py
- ZainCash Support Workspace
- negative/README.md
- scripts
- scripts
- compilerOptions
- Maintainability and stale-code refactor — design specification
- httpx
- web/tsconfig.json
- employee-frontend/tsconfig.json
- exports
- Review Focus
- scripts
- users-frontend/README.md
- intake/contracts.py
- TurnContext
- ingest.py
- admin.py
- guardrails.py
- test_cli.py
- SessionStorage
- intake/model.py
- test_llm.py
- intake.py
- Review Focus
- _DatabaseCall
- test_db_deadline_includes_pool_and_checkout_without_late_claim
- Customer Conversation Intake Implementation Plan
- KnowledgeError
- submission.py
- FakeXHR
- pipeline/contracts.py
- agent.py
- db/repository.py
- tests/test_repository.py
- test_embedding_switch.py
- ModelChoice
- components-ai-thought-chain.tsx
- kb/service.py
- intake/README.md
- InvalidPhone
- create_app
- batch_jobs.py
- ZainCash support: architecture and ticket flow {#support-overview}
- support_test
- employee-frontend/src/components/theme-provider.tsx
- intake/test_repository.py
- lookup.py
- schemas.py
- catalog.py
- Customer phone identity design
- bill-payment-biller-notice.md
- api-entrypoint.sh
- config.py
- test_workspace_schema.py
- 6.5 Text and direction
- build_pipeline
- RAG drafting verification — 2026-10-17
- workspace.py
- test_admin_api.py
- Deviations from the spec (intentional, small)
- 4. Backend design
- 5. Backend design
- index_deadlines
- collapsible.tsx

## God Nodes (most connected - your core abstractions)
1. `Settings` - 186 edges
2. `Step` - 108 edges
3. `ModelChoice` - 91 edges
4. `KnowledgeService` - 85 edges
5. `ActiveModels` - 74 edges
6. `useCopy()` - 65 edges
7. `IntakeController` - 55 edges
8. `fact()` - 53 edges
9. `context()` - 53 edges
10. `draft_state()` - 49 edges

## Surprising Connections (you probably didn't know these)
- `Repeatable local walkthrough` --references--> `Settings`  [INFERRED]
  docs/demo-readiness.md → backend/app/config.py
- `Ticket write paths` --references--> `upsert_tickets()`  [INFERRED]
  docs/superpowers/specs/2026-11-13-customer-phone-identity-design.md → backend/app/db/repository.py
- `Existing data` --references--> `upgrade_workspace_schema()`  [INFERRED]
  docs/superpowers/specs/2026-11-13-customer-phone-identity-design.md → backend/app/db/workspace_schema.py
- `Task 9: Repair the Five-Record JSONL Baseline Fixture` --references--> `load_jsonl()`  [INFERRED]
  docs/superpowers/plans/2026-11-02-backend-maintainability.md → backend/app/ingest.py
- `5.3 Knowledge-service boundary` --references--> `_DatabaseCall`  [INFERRED]
  docs/superpowers/specs/2026-11-02-maintainability-refactor-design.md → backend/app/kb/database.py

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **Cascade Classification Path** — docs_superpowers_specs_2026_10_07_support_pipeline_design_cascade, docs_superpowers_plans_2026_10_07_plan1_core_pipeline_part2_jev_classifier, docs_superpowers_plans_2026_10_07_plan1_core_pipeline_part2_gemini_classifier, docs_superpowers_plans_2026_10_07_plan1_core_pipeline_part2_cascade_combine, readme_human_approval [EXTRACTED 1.00]
- **Drafting Agent Toolset** — backend_app_pipeline_runner_lookup_transaction, backend_app_pipeline_runner_search_transactions, backend_app_pipeline_runner_get_customer_recent_transactions, backend_app_pipeline_runner_get_customer_ticket_history, backend_app_pipeline_runner_check_service_status, backend_app_pipeline_runner_search_knowledge_base, backend_app_pipeline_runner_flag_for_human, backend_app_pipeline_runner_submit_draft [EXTRACTED 1.00]
- **Ticket Processing Stage Flow** — backend_app_pipeline_runner_prepare, backend_app_pipeline_runner_jev_classify, backend_app_pipeline_runner_gemini_classify, backend_app_pipeline_runner_extract, backend_app_pipeline_runner_lookup, backend_app_pipeline_runner_decide, backend_app_pipeline_runner_draft [EXTRACTED 1.00]

## Communities (180 total, 41 thin omitted)

### Community 0 - "NewBatchPage.tsx"
Cohesion: 0.10
Nodes (27): Global Constraints, Per-model Evaluation Implementation Plan — Part 3 of 3 (frontend, translations, verification), Task 14: Evaluation view helpers, Task 15: Provenance, headline metrics, comparison table and empty state, Task 16: Model detail, confusion matrix and predictions drawer, Task 17: Run dialog, progress, page assembly, route and styles, Task 18: Documentation, full verification and manual check, Tabs() (+19 more)

### Community 1 - "Step"
Cohesion: 0.10
Nodes (30): ActiveModels, Step, make_draft_model(), make_gemini_llm(), batch_concurrency(), _local_pipeline(), ticket_timeout_s(), fake_registry() (+22 more)

### Community 2 - "pytest"
Cohesion: 0.18
Nodes (40): _tool_chat(), answer(), call(), Checker, draft_state(), Knowledge, script(), submit() (+32 more)

### Community 3 - "TurnStore"
Cohesion: 0.23
Nodes (9): OperationClaim, TurnResult, RevisionConflict, sanitize_intake_text(), _jsonable(), TurnStore, test_recovered_attempt_cannot_publish_stale_output(), test_review_publication_revision_matches_the_session() (+1 more)

### Community 4 - "investigation.py"
Cohesion: 0.07
Nodes (26): parse_dt(), DraftToolInputError, _datetime(), _days(), _field(), _involves(), _phone(), _phones() (+18 more)

### Community 5 - "pipeline/graph.py"
Cohesion: 0.08
Nodes (16): _default_retry(), _percentile(), _retryable(), FieldExtractor, RagDrafter, CredentialChecker, response_payload(), send() (+8 more)

### Community 6 - "Card"
Cohesion: 0.12
Nodes (40): Backend API contract used here, 5.2 Page structure, Metric(), Card(), CardContent(), CardHeader(), CardTitle(), adminErrorMessage() (+32 more)

### Community 7 - "Customer conversation intake for ZainCash support"
Cohesion: 0.06
Nodes (31): 10. Verification and acceptance criteria, 11. Delivery and review, 1. Outcome and agreed requirements, 2. Current implementation and integration points, 3. Approach and boundaries, 4. Conversation state and turn flow, 5. Facts, evidence, and readiness, 6. Language and screenshot behavior (+23 more)

### Community 8 - "lib/types.ts"
Cohesion: 0.06
Nodes (49): Admin model configuration — employee frontend implementation plan, File structure, Global Constraints, Review Focus, Task 1: API types, admin session and admin requests, Task 2: Strings, the AI locality chip, run models and the batch switch message, Task 3: Model choice logic and the change dialog, Task 13: Evaluation types, API client, formatters, copy and report import (+41 more)

### Community 9 - "IntakeController"
Cohesion: 0.16
Nodes (10): Task 6: Customer API client and resumable UI state, Task 1: Cleanup-first removal of reference-verified dead code and dependencies, Task 7: Preserve resume-unavailable state across `startNew`, Task 7: Intake app data layer — phone helper, contracts, API, controller, emptyState(), IntakeController, isConflict(), isOffline() (+2 more)

### Community 10 - "FakeJevRunnable"
Cohesion: 0.12
Nodes (18): CredentialCheck, DegradedCredentialChecker, _finite_nonnegative(), _get(), JevCredentialChecker, ResponseRunnable, test_bad_usage_cannot_poison_cost(), test_cancellation_propagates_with_cost_for_outer_timeout_owner() (+10 more)

### Community 11 - "test_rag_api.py"
Cohesion: 0.12
Nodes (23): client(), evidence_client(), pipeline(), submit(), test_actual_guardrail_failure_is_separate_from_reply(), test_concurrent_index_requests_share_active_work(), test_disabled_or_missing_provider_stores_without_indexing(), test_explicit_retry_tags_search_and_chunk_pagination() (+15 more)

### Community 12 - "employee-frontend/package.json"
Cohesion: 0.06
Nodes (30): @base-ui/react, class-variance-authority, cn, eslint, @eslint/js, eslint-plugin-react-hooks, eslint-plugin-react-refresh, @fontsource/tajawal (+22 more)

### Community 14 - "QueuePage.tsx"
Cohesion: 0.14
Nodes (52): Task 12: Locale parity test and translated Runs pages, Task 10: Employee app — customer page and ticket header link, Task 9: Employee app — required phone, queue identity and search, batch entry, 5.1 Data access, 7. Testing, Confidence(), EmptyState(), ErrorState() (+44 more)

### Community 15 - "Support Taxonomy Categories"
Cohesion: 0.21
Nodes (22): lookup, Account KYC, Account & Security, Agent Dispute, Agent Network, App Bug, Bill Payment, Card Issue (+14 more)

### Community 16 - "ui/package.json"
Cohesion: 0.08
Nodes (24): @base-ui/react, class-variance-authority, cn, eslint, @eslint/js, eslint-plugin-react-hooks, eslint-plugin-react-refresh, @fontsource/tajawal (+16 more)

### Community 17 - "locale.tsx"
Cohesion: 0.08
Nodes (37): App(), CustomerPage, EvaluationPage, InsightsPage, KnowledgePage, ModelsPage, NewBatchPage, QueuePage (+29 more)

### Community 18 - "users-frontend/package.json"
Cohesion: 0.08
Nodes (23): turbo, devDependencies, prettier, prettier-plugin-tailwindcss, turbo, typescript, engines, node (+15 more)

### Community 19 - "make_ticket"
Cohesion: 0.19
Nodes (16): build_graph(), PipelineDeps, InMemoryTransactionRepo, load_taxonomy(), tax(), pipeline(), taxonomy(), test_run_batch_defaults_to_jev() (+8 more)

### Community 20 - "test_draft_guardrails.py"
Cohesion: 0.13
Nodes (30): Passage, check_draft(), _citation_findings(), requests_credentials(), make_ticket(), check(), state(), test_aggregation_is_deduplicated_and_has_no_state_side_effects() (+22 more)

### Community 21 - "web/package.json"
Cohesion: 0.05
Nodes (52): clsx, jsdom, tailwind-merge, @testing-library/jest-dom, @testing-library/user-event, @workspace/ui, dependencies, clsx (+44 more)

### Community 22 - "test_recovery_regressions.py"
Cohesion: 0.14
Nodes (16): _command_settings(), ingest_kb_cmd(), init_db_cmd(), Mode, run_batch_cmd(), _run_in_memory(), _run_with_db(), seed_db_cmd() (+8 more)

### Community 23 - "compilerOptions"
Cohesion: 0.08
Nodes (23): compilerOptions, allowArbitraryExtensions, allowImportingTsExtensions, erasableSyntaxOnly, jsx, lib, module, moduleDetection (+15 more)

### Community 24 - "employee-frontend/components.json"
Cohesion: 0.09
Nodes (21): aliases, components, hooks, lib, ui, utils, iconLibrary, menuAccent (+13 more)

### Community 25 - "ModelSettingsStore"
Cohesion: 0.12
Nodes (12): ModelSettingAuditRow, ModelSettingRow, _iso(), ModelSettingsStore, make_knowledge_service(), _store(), test_describe_reports_a_saved_model_that_is_no_longer_installed(), test_empty_store_uses_env_defaults() (+4 more)

### Community 26 - "compilerOptions"
Cohesion: 0.09
Nodes (22): compilerOptions, allowArbitraryExtensions, allowImportingTsExtensions, erasableSyntaxOnly, jsx, lib, module, moduleDetection (+14 more)

### Community 27 - "web/src/components/theme-provider.tsx"
Cohesion: 0.16
Nodes (13): App(), controller, disableTransitionsTemporarily(), getSystemTheme(), isEditableTarget(), isTheme(), ResolvedTheme, Theme (+5 more)

### Community 28 - "EmbeddingError"
Cohesion: 0.07
Nodes (44): EmbeddingBatch, EmbeddingError, _nonnegative_number(), OpenAICompatibleEmbedder, OpenRouterEmbedder, _ordered_vectors(), _response_cost(), Embeddings (+36 more)

### Community 29 - "Classify and Extract Prompts"
Cohesion: 0.33
Nodes (7): extract, gemini_classify, Pipeline Graph Orchestration, jev_classify, prepare, GeminiClassifier, JevClassifier

### Community 30 - "test_draft_tools.py"
Cohesion: 0.12
Nodes (29): ErrorEmbedder, test_all_eight_tools_and_seven_parallel_calls_execute_only_six(), test_context_copies_input_and_rejects_raising_hard_call_limit(), test_database_faults_remain_distinct_and_record_paid_search_cost(), test_discovered_ref_can_be_inspected_but_not_promoted_to_match(), test_exact_and_fuzzy_queries_are_scoped_and_never_confirm_candidates(), test_exact_reference_still_requires_customer_and_excludes_future(), test_failure_trace_bounds_invalid_numeric_arguments() (+21 more)

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
Cohesion: 0.12
Nodes (26): FakeEmbedder, GatedEmbedder, LateEmbedder, PaidEmbedder, count_chunks(), test_category_filters_include_general_policies_and_validate_tags(), test_claim_locks_source_even_before_index_row_exists(), test_competing_callers_refuse_active_attempt_and_release_transactions() (+18 more)

### Community 36 - "web/components.json"
Cohesion: 0.10
Nodes (19): aliases, components, hooks, lib, ui, utils, iconLibrary, menuAccent (+11 more)

### Community 38 - "ChangeModelDialog.tsx"
Cohesion: 0.10
Nodes (39): Task 1: Remove reference-verified dead exports, components, and the Mermaid dependency, ConfirmDialog(), FilterSelect(), Badge(), badgeVariants, Button(), buttonVariants, Dialog() (+31 more)

### Community 39 - "ui/components.json"
Cohesion: 0.10
Nodes (19): aliases, components, hooks, lib, ui, utils, iconLibrary, menuAccent (+11 more)

### Community 40 - "Settings"
Cohesion: 0.07
Nodes (22): Settings, draft_timeout_s(), env_defaults(), intake_timeout_s(), _settings(), test_eligibility(), test_env_defaults_match_todays_settings(), test_env_overrides_for_draft_and_intake() (+14 more)

### Community 41 - "fact"
Cohesion: 0.23
Nodes (30): Attachment, merge_analysis(), context(), fact(), message(), proposal(), test_additional_issue_is_resolved_in_place_instead_of_appended(), test_amount_uses_supported_value_not_first_number_in_quote() (+22 more)

### Community 43 - "Human Review Gate"
Cohesion: 0.25
Nodes (4): support CLI, Support Workspace UI Plan, Review API, Workspace UI Verification

### Community 44 - "compilerOptions"
Cohesion: 0.12
Nodes (16): compilerOptions, allowImportingTsExtensions, erasableSyntaxOnly, lib, module, moduleDetection, noEmit, noFallthroughCasesInSwitch (+8 more)

### Community 46 - "PipelineState"
Cohesion: 0.12
Nodes (10): DraftResult, _Nodes, Drafter, DraftExecutionError, NullDrafter, UnavailableDrafter, PipelineState, 2. Current implementation and integration points (+2 more)

### Community 47 - "compilerOptions"
Cohesion: 0.12
Nodes (16): compilerOptions, allowImportingTsExtensions, erasableSyntaxOnly, lib, module, moduleDetection, noEmit, noFallthroughCasesInSwitch (+8 more)

### Community 48 - "Plan 3 RAG Drafting Implementation Plan"
Cohesion: 0.22
Nodes (9): Completion and review record — 2026-10-17, Execution handoff, File map and shared interfaces, Global Constraints, Plan 3 RAG Drafting Implementation Plan, Plan self-review, Review Focus, Task 6: API/CLI indexing and persisted citation projection (+1 more)

### Community 57 - "parse_document"
Cohesion: 0.10
Nodes (30): TextChunk, _append_chunks(), _check_extracted_size(), DocumentParseError, parse_document(), _parse_pdf(), make_pdf(), test_arabic_text_and_bom_are_preserved() (+22 more)

### Community 58 - "AttachmentStore"
Cohesion: 0.16
Nodes (19): AttachmentStore, ImageRejected, NotOwned, png_bytes(), repo(), store(), test_active_turn_rejects_upload(), test_changed_invalid_bytes_conflict_before_decoding_replay() (+11 more)

### Community 59 - "contracts.ts"
Cohesion: 0.10
Nodes (46): Task 4: Make pending operations discriminated and use one request identity, Task 5: Add complete dependency-free API and persisted-session guards, createIntakeApi(), parseJson(), readError(), UploadResult, finiteNonnegative(), INTAKE_FALLBACK_MESSAGE (+38 more)

### Community 60 - "taxonomy.py"
Cohesion: 0.20
Nodes (3): TaxonomyError, taxonomy(), test_rejects_unknown_team()

### Community 61 - "pipeline/contracts.py"
Cohesion: 0.14
Nodes (17): ClassificationResult, detect_arabizi(), fold_arabic(), has_latin_mix(), _latin_words(), normalize(), sanitize_for_storage(), mask_cards() (+9 more)

### Community 62 - "DocumentList.tsx"
Cohesion: 0.16
Nodes (20): Task 5: Extract presentational DocumentList and KnowledgeReadiness components, 6.1 Verification and cleanup, 6.2 Retire the legacy trace/chart cluster, 6.3 Runs and request loading, 6.4 Focused view extraction, 6. Employee frontend design, Input(), DocumentList() (+12 more)

### Community 63 - "intake/types.ts"
Cohesion: 0.07
Nodes (34): HTTP contract (implemented in Tasks 4–5), Task 7: Bilingual customer chat, screenshots and reviewed submission, Task 8: Employee evidence panel and processing state, Task 9: End-to-end handoff, live vision evidence and runbook, Global Constraints, Intake Chat UI Implementation Plan, Task 1: Put the summary and receipt in the thread, Task 2: Put screenshots inside the composer (+26 more)

### Community 64 - "tasks"
Cohesion: 0.11
Nodes (18): dependsOn, inputs, outputs, cache, persistent, dependsOn, dependsOn, $schema (+10 more)

### Community 65 - "knowledge.py"
Cohesion: 0.10
Nodes (24): session(), _configured(), delete_document(), download_document(), index_document(), list_chunks(), list_documents(), _require_provider() (+16 more)

### Community 66 - "intake/contracts.py"
Cohesion: 0.14
Nodes (9): _aware(), IntakeModel, IntakeState, Message, initial_state(), grounded_analysis(), grounded_review(), image_evidence() (+1 more)

### Community 67 - "test_handoff.py"
Cohesion: 0.22
Nodes (16): Analysis, _amount(), analyze(), complete_conversation(), _dated(), _message(), _opening(), _png() (+8 more)

### Community 68 - "PipelineState"
Cohesion: 0.12
Nodes (15): 10. Remaining demo roadmap, 1. Intent and acceptance criteria, 3. Provider and configuration, 4. Knowledge ingestion and persistence, 5. Retrieval and evidence, 7. Draft guardrails and failure outcomes, 8. Pipeline, API, CLI and UI integration, 9. Demo policies and verification (+7 more)

### Community 69 - "results.py"
Cohesion: 0.15
Nodes (18): get_result(), list_results(), read_intake_attachment(), review_result(), ReviewRow, TicketResultRow, IntakeSubmissionRow, employee_attachment() (+10 more)

### Community 70 - "make_ticket"
Cohesion: 0.21
Nodes (19): FakeClassifier, make_output(), _deps(), _run(), test_concurrency_is_limited(), test_draft_node_never_retries_or_restarts_paid_work(), test_drafter_reasons_escalate(), draft() (+11 more)

### Community 71 - "intake/repository.py"
Cohesion: 0.22
Nodes (14): _display_name(), CustomerReview, IntakeAttachmentRow, IntakeMessageRow, attachment_from_row(), customer_review(), load_attachments(), load_messages() (+6 more)

### Community 72 - "Credentials"
Cohesion: 0.15
Nodes (9): Credentials, SessionView, IntakeService, make_intake_service(), _payload(), test_concurrent_submit_dispatches_once(), test_second_request_id_reuses_the_approved_review(), test_submission_replay_creates_one_ticket() (+1 more)

### Community 73 - "ConfiguredEmbedder"
Cohesion: 0.16
Nodes (5): ConfiguredEmbedder, _Store, choice_for(), _Store, test_configured_embedder_follows_the_current_setting()

### Community 74 - "FakeJevRunnable"
Cohesion: 0.29
Nodes (10): FakeJevRunnable, _criteria(), _run(), test_low_top_probability_is_uncertain(), test_one_main_call_with_all_questions(), test_order_check_uses_reversed_options(), test_order_disagreement_is_uncertain(), test_priority_level_maps_to_p_label() (+2 more)

### Community 75 - "test-kb/README.md"
Cohesion: 0.07
Nodes (14): Fictional RAG walkthrough inputs, توثيق الحساب — سياسة خيالية للعرض التجريبي, نزاع مع وكيل — سياسة خيالية للعرض التجريبي, أعطال التطبيق — سياسة خيالية للعرض التجريبي, دفع الفواتير — سياسة خيالية للعرض التجريبي, مشاكل البطاقة — سياسة خيالية للعرض التجريبي, التحويل المعلّق — سياسة خيالية للعرض التجريبي, تصعيد شبهة الاحتيال — سياسة خيالية للعرض التجريبي (+6 more)

### Community 76 - "test_workspace_api.py"
Cohesion: 0.14
Nodes (15): review_payload(), start_run(), test_batch_and_queue_expose_real_results(), test_batch_failure_is_isolated_and_conflicting_ids_rejected(), test_customer_profile_lists_the_latest_result_of_each_ticket(), test_only_jev_mode_is_configured_and_retired_modes_are_rejected(), test_progress_counts_only_durable_results_after_save_failure(), fail_one_save() (+7 more)

### Community 77 - "KnowledgeService"
Cohesion: 0.12
Nodes (12): Embedder, KnowledgeChunk, _Claim, _error_cost(), KnowledgeService, test_incompatible_or_unowned_chunks_cannot_be_searched(), test_model_changes_require_reindex_and_keep_chunk_ids(), test_pdf_page_metadata_and_repeated_text_chunk_identity() (+4 more)

### Community 79 - "devDependencies"
Cohesion: 0.12
Nodes (16): devDependencies, eslint, @eslint/js, eslint-plugin-react-hooks, eslint-plugin-react-refresh, globals, prettier, prettier-plugin-tailwindcss (+8 more)

### Community 80 - "judge-demo.ar.md"
Cohesion: 0.14
Nodes (13): أعطال التطبيق — سياسة خيالية للعرض التجريبي, استرجاع مبلغ شراء — سياسة خيالية للعرض التجريبي, استعادة الدخول — سياسة خيالية للعرض التجريبي, الاستفسار الآمن من الدعم — سياسة خيالية للعرض التجريبي, الاستفسار المؤقت للدعم في المهمة ٨ — سياسة خيالية للعرض التجريبي, التحويل المعلّق — سياسة خيالية للعرض التجريبي, التحويل لمستلم بالخطأ — سياسة خيالية للعرض التجريبي, الطلبات غير الواضحة وخارج النطاق — سياسة خيالية للعرض التجريبي (+5 more)

### Community 93 - "test_recovery_regressions.py"
Cohesion: 0.24
Nodes (12): command(), create(), test_actual_app_restart_reconciles_failed_placeholder(), test_failed_review_retry_cannot_reopen_submitted_session(), test_original_payload_identity_survives_sanitization(), test_publication_failure_is_retryable_without_restart(), fail_once(), test_receipt_reference_is_preserved() (+4 more)

### Community 94 - "devDependencies"
Cohesion: 0.11
Nodes (19): devDependencies, eslint, @eslint/js, eslint-plugin-react-hooks, eslint-plugin-react-refresh, globals, jsdom, @tailwindcss/vite (+11 more)

### Community 95 - "devDependencies"
Cohesion: 0.17
Nodes (12): devDependencies, eslint, @eslint/js, eslint-plugin-react-hooks, eslint-plugin-react-refresh, globals, tailwindcss, @types/node (+4 more)

### Community 96 - "FieldPick"
Cohesion: 0.09
Nodes (23): LLMUnavailable, StructuredLLM, FieldPick, _field(), fill_gaps(), finalize(), _is_weak(), ExtractedSpan (+15 more)

### Community 97 - "ticket-flow.ts"
Cohesion: 0.06
Nodes (65): Global Constraints, Task 1: Sentence catalog, Task 2: Which step is open, Task 3: Received, produced, and drafting events, Task 4: Mermaid source, Task 5: Draw the charts on the ticket page, Ticket Flow Charts Implementation Plan, 1. Outcome (+57 more)

### Community 98 - "review.py"
Cohesion: 0.19
Nodes (15): ReviewText, InvalidEvidence, validate(), build_review(), _compact(), _render_value(), _ticket_text(), _tokens() (+7 more)

### Community 99 - "compilerOptions"
Cohesion: 0.14
Nodes (13): compilerOptions, jsx, lib, module, moduleResolution, noEmit, paths, skipLibCheck (+5 more)

### Community 100 - "قواعد المعرفة العربية للعرض أمام لجنة التحكيم"
Cohesion: 0.33
Nodes (6): الأصل ونتيجة التحقق, توليد مسودة ومراجعتها, خريطة الملفات وأسئلة العرض, خطوات الرفع والفهرسة والبحث أمام اللجنة, قواعد المعرفة العربية للعرض أمام لجنة التحكيم, ماذا أرفع؟

### Community 101 - "pydantic"
Cohesion: 0.23
Nodes (6): CitationSource, _Draft, draft_evidence(), _Guardrail, _TraceModel, _validated()

### Community 102 - "dependencies"
Cohesion: 0.12
Nodes (16): dependencies, @base-ui/react, class-variance-authority, cn, @fontsource/tajawal, @fontsource-variable/plus-jakarta-sans, lucide-react, motion (+8 more)

### Community 103 - "InvalidEvidence"
Cohesion: 0.12
Nodes (25): EvidenceRef, Fact, canonical_digits(), normalize_reported_date(), _apply(), _check_reference(), _compact(), checked_update() (+17 more)

### Community 104 - "dependencies"
Cohesion: 0.20
Nodes (10): dependencies, @base-ui/react, class-variance-authority, cn, @fontsource/tajawal, @fontsource-variable/plus-jakarta-sans, react, react-dom (+2 more)

### Community 105 - "compilerOptions"
Cohesion: 0.17
Nodes (11): compilerOptions, jsx, lib, module, moduleResolution, outDir, skipLibCheck, strict (+3 more)

### Community 106 - "ref_vitest"
Cohesion: 0.07
Nodes (27): Employee Frontend Maintainability Implementation Plan, Global Constraints, Review Focus, Task 2: Migrate active TicketFlow coverage, then retire the legacy trace/chart cluster, Task 4: Extract and test the pure queue projection, Task 6: Repair ExtractedField fixtures and make standalone typecheck real, Task 7: Repair employee README paths/test-count guidance and run final acceptance, originalLocale (+19 more)

### Community 107 - "IntakePage.test.tsx"
Cohesion: 0.10
Nodes (26): @testing-library/react, IntakeApi, session, IntakeRequestError, malformed, populated, ControllerState, fileIdentity() (+18 more)

### Community 108 - "test_final_fix_handoff.py"
Cohesion: 0.12
Nodes (19): assert_completed_evidence(), faulty_knowledge(), read(), outer_deadlines(), PaidEmbeddings, runner_env(), build(), sessions() (+11 more)

### Community 109 - "ZainCash Support Workspace"
Cohesion: 0.25
Nodes (8): Current capability boundaries, Data source, Modular file map, Open the right project, Run locally, shadcn conventions, Workflow, ZainCash Support Workspace

### Community 111 - "scripts"
Cohesion: 0.25
Nodes (8): scripts, build, dev, format, lint, preview, test, typecheck

### Community 112 - "scripts"
Cohesion: 0.25
Nodes (8): scripts, build, dev, format, lint, preview, test, typecheck

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

### Community 119 - "Review Focus"
Cohesion: 0.12
Nodes (15): Customer Frontend Maintainability Implementation Plan, Global Constraints, Review Focus, Task 2: Make standalone typechecking and root test execution real, Task 3: Centralize test cleanup and shared intake fixtures mechanically, Task 6: Extract stable-ID sequential upload lifecycle with TDD, Task 8: Disable streaming Stop when no handler exists, Task 9: Run the complete customer acceptance matrix and final diff review (+7 more)

### Community 120 - "scripts"
Cohesion: 0.50
Nodes (4): scripts, format, lint, typecheck

### Community 122 - "intake/contracts.py"
Cohesion: 0.21
Nodes (16): Question, Readiness, _asked_already(), asks_for_secret(), assess_readiness(), _can_ask(), canonical_category(), choose_question() (+8 more)

### Community 123 - "TurnContext"
Cohesion: 0.21
Nodes (5): QuestionRecord, TurnContext, IntakeGraph, _invitation(), Shared contracts (implement in Task 1; extend only through explicit edits here)

### Community 124 - "ingest.py"
Cohesion: 0.16
Nodes (14): load_jsonl(), load_tickets(), _rows(), test_csv_with_bom_and_missing_columns(), test_duplicate_external_ids_keep_first(), test_invalid_phone_names_the_row(), test_json_object_without_ids(), test_jsonl_fixture_loads() (+6 more)

### Community 125 - "admin.py"
Cohesion: 0.14
Nodes (17): audit(), catalog(), _check_provider(), ChoiceInput, embedding_switch(), ModelOptions, models(), ProbeInput (+9 more)

### Community 126 - "guardrails.py"
Cohesion: 0.09
Nodes (28): Candidate, _add(), find_candidates(), normalize_phone(), _overlaps(), parse_amount(), resolve_date(), _safe_date() (+20 more)

### Community 127 - "test_cli.py"
Cohesion: 0.15
Nodes (9): test_config_error_exits_2(), boom(), test_ingest_directory_is_deterministic_and_duplicate_is_free(), test_ingest_disabled_configuration_never_calls_provider(), test_ingest_failure_exit_and_retry_stored(), test_ingest_invalid_source_does_not_stop_other_files(), test_ingest_limits_batch_without_partial_side_effects(), test_retry_stored_indexes_old_uploads_without_recovering_other_process_jobs() (+1 more)

### Community 128 - "SessionStorage"
Cohesion: 0.22
Nodes (5): SessionStorage, credentials, invalidValues, messagePayload, SavedSession

### Community 129 - "intake/model.py"
Cohesion: 0.12
Nodes (27): ImageInput, ModelCall, ModelUnavailable, _analysis_prompt(), _bounded_context(), _guard_size(), IntakeModel, ModelBudget (+19 more)

### Community 130 - "test_llm.py"
Cohesion: 0.13
Nodes (11): StructuredChatLLM, _llm(), _S, test_draft_model_uses_millisecond_timeout_and_disables_sdk_retries(), test_openrouter_reported_cost_takes_precedence_over_token_estimate(), test_openrouter_retry_budget_is_bounded(), test_openrouter_structured_samples_use_configured_key_and_validate_output(), send() (+3 more)

### Community 131 - "intake.py"
Cohesion: 0.17
Nodes (19): create_session(), _credentials(), _dump(), get_session(), post_message(), read_attachment(), remove_attachment(), request_review() (+11 more)

### Community 132 - "Review Focus"
Cohesion: 0.11
Nodes (17): api(), settings(), Review Focus, Task 1: Establish the safety baseline and remove tracked Graphify cache contents, Task 2: Delete the superseded architecture HTML after a fresh reference check, Task 3: Remove confirmed stale local runtime state and the duplicate screenshot, Task 4: Repair only current setup and processing documentation, Task 5: Restrict Docker build context without deleting installed dependencies (+9 more)

### Community 134 - "test_db_deadline_includes_pool_and_checkout_without_late_claim"
Cohesion: 0.15
Nodes (8): test_db_deadline_includes_pool_and_checkout_without_late_claim(), checked_in(), test_db_deadline_search_cancellation_is_nonblocking_and_retains_cost(), test_dbapi_commit_handoff_arbitrates_cancellation(), gate(), gate_before_dbapi(), gate_inside_dbapi(), test_index_deadline_or_cancellation_preserves_real_adapter_partial_cost()

### Community 135 - "Customer Conversation Intake Implementation Plan"
Cohesion: 0.20
Nodes (8): Completion audit — 2026-10-18, Customer Conversation Intake Implementation Plan, Execution conventions and repository baseline, File map and dependency order, Global Constraints, Plan review and execution handoff, Review Focus, Spec coverage and acceptance map

### Community 136 - "KnowledgeError"
Cohesion: 0.29
Nodes (4): DocumentNotFoundError, IndexAttemptLostError, KnowledgeError, Task 14: Preserve Safe Knowledge 503s and Log Only Unexpected Diagnostic Types

### Community 137 - "submission.py"
Cohesion: 0.18
Nodes (15): Receipt, ReviewSnapshot, IntakeOperationRow, IntakeError, OperationConflict, StaleReview, TurnBusy, assert_same_operation() (+7 more)

### Community 139 - "pipeline/contracts.py"
Cohesion: 0.07
Nodes (41): Candidates, ClassifierOutput, NormalizedTicket, Classifier, build_order_check(), build_questions(), build_state(), category_criteria() (+33 more)

### Community 140 - "agent.py"
Cohesion: 0.04
Nodes (34): SearchResult, _abandoned(), _check_deadline(), _consume(), KnowledgeExecutionError, _error_cost(), _Execution, _has_response_usage() (+26 more)

### Community 141 - "db/repository.py"
Cohesion: 0.17
Nodes (3): Base, IncidentRow, TransactionRow

### Community 142 - "tests/test_repository.py"
Cohesion: 0.13
Nodes (16): load_incidents(), load_transactions(), SqlTransactionRepo, _to_record(), _upsert(), upsert_tickets(), _count(), sf() (+8 more)

### Community 143 - "test_embedding_switch.py"
Cohesion: 0.10
Nodes (14): EmbeddingSwitchRow, EmbeddingSwitches, SwitchConflict, _view(), _client(), _documents(), test_failed_documents_are_listed(), test_run_start_locks_the_switch_table_before_its_first_write() (+6 more)

### Community 144 - "ModelChoice"
Cohesion: 0.09
Nodes (25): _chat(), _describe(), _draft(), _embed(), _extract(), _intake(), probe(), _ProbeAnswer (+17 more)

### Community 148 - "components-ai-thought-chain.tsx"
Cohesion: 0.15
Nodes (15): Status, StatusIcon(), statusStyles, StepContext, StepContextType, ThoughtChain(), ThoughtChainContent(), ThoughtChainItem() (+7 more)

### Community 149 - "kb/service.py"
Cohesion: 0.09
Nodes (23): _safe_dispatch(), get_run(), list_runs(), start_run(), RunRow, create_run(), _accepts(), lifespan() (+15 more)

### Community 151 - "InvalidPhone"
Cohesion: 0.12
Nodes (22): get_customer(), customer_phone_or_none(), InvalidPhone, normalize_customer_phone(), ensure_customers(), CustomerRow, TicketRow, _ticket_phone() (+14 more)

### Community 152 - "create_app"
Cohesion: 0.12
Nodes (19): init_db(), initialize_database(), make_engine(), make_sessionmaker(), reset_db(), create_app(), intake_client(), intake_db() (+11 more)

### Community 153 - "batch_jobs.py"
Cohesion: 0.22
Nodes (14): save_outcomes(), TicketOutcome, TicketExecution, outcome_from_state(), summarize(), outcome_to_dict(), outcome_to_row(), _current_models() (+6 more)

### Community 154 - "ZainCash support: architecture and ticket flow {#support-overview}"
Cohesion: 0.50
Nodes (3): 1 · System architecture {#system-architecture}, 2 · Ticket flow {#ticket-flow}, ZainCash support: architecture and ticket flow {#support-overview}

### Community 155 - "support_test"
Cohesion: 0.15
Nodes (14): support_test(), Evidence by layer, Known limitations and remaining work, Repeatable local walkthrough, Synthetic demo readiness, Task 8: Demo corpus, full verification and readiness record, Global Constraints, Browser handoff (+6 more)

### Community 156 - "employee-frontend/src/components/theme-provider.tsx"
Cohesion: 0.23
Nodes (11): disableTransitionsTemporarily(), getSystemTheme(), isEditableTarget(), isTheme(), ResolvedTheme, Theme, THEME_VALUES, ThemeProvider() (+3 more)

### Community 157 - "intake/test_repository.py"
Cohesion: 0.11
Nodes (14): IntakeSessionRow, InvalidCustomerPhone, IntakeRepository, builder(), repo(), test_blank_intake_model_is_rejected(), test_contracts_reject_extra_keys(), test_datetimes_must_be_timezone_aware() (+6 more)

### Community 158 - "lookup.py"
Cohesion: 0.10
Nodes (37): Decision, ExtractedField, LookupResult, TxnRecord, _as_date(), _iqd_amount(), match_transaction(), TransactionRepo (+29 more)

### Community 159 - "schemas.py"
Cohesion: 0.20
Nodes (5): BatchInput, KnowledgeIndexInput, KnowledgeSearchInput, ReviewInput, TicketInput

### Community 160 - "catalog.py"
Cohesion: 0.22
Nodes (9): CatalogCache, step_catalog(), BrokenStatusProvider, test_a_provider_whose_status_check_raises_is_listed_as_unreachable(), test_catalog_errors_stay_per_provider_and_cache_respects_ttl(), test_classify_catalog_only_offers_typesafe(), test_step_catalog_filters_and_marks_unknown(), Task 8: Live model tests and the model catalog (+1 more)

### Community 161 - "Customer phone identity design"
Cohesion: 0.12
Nodes (15): Backend, Canonical phone format, Customer phone identity design, Data model, Decisions, Employee API, employee-frontend, Error handling (+7 more)

### Community 164 - "config.py"
Cohesion: 0.05
Nodes (31): Provider, UnsupportedOperation, _capabilities(), DraftProviderResponseError, OpenRouterChat, OpenRouterProvider, _per_million(), provider_errors() (+23 more)

### Community 165 - "test_workspace_schema.py"
Cohesion: 0.29
Nodes (8): assert_customer_schema(), LegacySchemaError, _nullable(), _table_exists(), upgrade_workspace_schema(), test_fresh_schema_passes_the_customer_check(), test_intake_sessions_without_a_customer_phone_stop_startup(), test_nullable_ticket_phone_stops_startup_with_a_reset_instruction()

### Community 166 - "6.5 Text and direction"
Cohesion: 0.15
Nodes (11): Task 3: Split RunDetailPage and introduce bounded run-result loading, 6.1 Route and access, 6.2 Page, 6.3 Change dialog, 6.4 Visible to all employees, 6.5 Text and direction, 6. Employee-frontend design, loadRunResults() (+3 more)

### Community 167 - "build_pipeline"
Cohesion: 0.12
Nodes (21): Sample, build_pipeline(), ConfigError, model_ids(), run_batch(), FakeStructuredLLM, ScriptedChat, _settings() (+13 more)

### Community 168 - "RAG drafting verification — 2026-10-17"
Cohesion: 0.20
Nodes (10): ingest(), Artifacts, servers and remaining concerns, Citation IDs and provider evidence, Commands and automated verification — historical Task 8, Corpus and actual retrieval, Current final verification and review closure, Environment and isolation, Live browser and persistence evidence (+2 more)

### Community 169 - "workspace.py"
Cohesion: 0.24
Nodes (6): get_session(), health(), insights(), workspace(), knowledge_configured(), latest_results_query()

### Community 170 - "test_admin_api.py"
Cohesion: 0.43
Nodes (6): make_client(), test_admin_is_disabled_without_a_token(), test_models_and_catalog(), test_non_ascii_and_blank_tokens_are_rejected(), test_save_rejections_change_nothing(), test_test_save_and_audit()

### Community 171 - "Deviations from the spec (intentional, small)"
Cohesion: 0.29
Nodes (6): Deviations from the spec (intentional, small), Global Constraints, Per-model Evaluation Implementation Plan — Part 2 of 3 (evaluation engine), Task 11: `support eval` CLI and v2 export, Task 7: Metrics, Task 9: Runner, request validation and cost estimate

### Community 172 - "4. Backend design"
Cohesion: 0.17
Nodes (8): _classify(), 4.2 Provider protocol, 4.4 Snapshot semantics, 4.5 Step requirements and live tests, 4.6 Options, 4.7 Timeouts, 4.8 Embedding switch (short pause), 4. Backend design

### Community 173 - "5. Backend design"
Cohesion: 0.25
Nodes (6): 5.1 Dead-code cleanup, 5.2 Extraction ownership, 5.3 Knowledge-service boundary, 5.4 Shared backend boundaries, 5.5 Confirmed backend defect fixes, 5. Backend design

### Community 174 - "index_deadlines"
Cohesion: 0.40
Nodes (3): index_deadlines(), settings(), expire_during_embedding()

## Ambiguous Edges - Review These
- `Fraud Report` → `Plan 1 Live Smoke`  [AMBIGUOUS]
  README.md · relation: conceptually_related_to

## Knowledge Gaps
- **83 isolated node(s):** `zaincash-support`, `@base-ui/react`, `@fontsource-variable/plus-jakarta-sans`, `@fontsource/tajawal`, `@tailwindcss/vite` (+78 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 1220 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **41 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `2. Current state` connect `pipeline/contracts.py` to `NewBatchPage.tsx`, `build_pipeline`, `QueuePage.tsx`, `make_ticket`, `lookup.py`?**
  _High betweenness centrality (0.101) - this node is a cross-community bridge._
- **Are the 53 inferred relationships involving `Settings` (e.g. with `_command_settings()` and `_run_in_memory()`) actually correct?**
  _`Settings` has 53 INFERRED edges - model-reasoned connections that need verification._
- **What connects `zaincash-support`, `@base-ui/react`, `@fontsource-variable/plus-jakarta-sans` to the rest of the system?**
  _83 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `NewBatchPage.tsx` be split into smaller, more focused modules?**
  _Cohesion score 0.09986504723346828 - nodes in this community are weakly interconnected._
- **Why does `Settings` connect `Settings` to `intake/model.py`, `Step`, `pytest`, `Review Focus`, `pipeline/graph.py`, `test_llm.py`, `submission.py`, `test_rag_api.py`, `agent.py`, `pipeline/contracts.py`, `tests/test_repository.py`, `test_embedding_switch.py`, `ModelChoice`, `make_ticket`, `kb/service.py`, `test_recovery_regressions.py`, `create_app`, `ModelSettingsStore`, `support_test`, `EmbeddingError`, `intake/test_repository.py`, `test_draft_tools.py`, `catalog.py`, `test_kb_service.py`, `config.py`, `test_workspace_schema.py`, `build_pipeline`, `RAG drafting verification — 2026-10-17`, `fact`, `test_admin_api.py`, `index_deadlines`, `AttachmentStore`, `intake/repository.py`, `Credentials`, `ConfiguredEmbedder`, `test_workspace_api.py`, `KnowledgeService`, `test_final_fix_handoff.py`, `httpx`, `test_cli.py`?**
  _High betweenness centrality (0.092) - this node is a cross-community bridge._
- **Are the 68 inferred relationships involving `Step` (e.g. with `catalog()` and `_check_provider()`) actually correct?**
  _`Step` has 68 INFERRED edges - model-reasoned connections that need verification._

### Low-confidence Hints
_AMBIGUOUS edges — the extractor was unsure. Verify before acting on these._

- **What is the exact relationship between `Fraud Report` and `Plan 1 Live Smoke`?**
  _Edge tagged AMBIGUOUS (relation: conceptually_related_to) - confidence is low._