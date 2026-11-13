# Graph Report - zaincash-support  (2026-11-13)

## Corpus Check
- 428 files · ~451,053 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 27 file(s) not represented in the graph (top: (none) 17, .jsonl 4, .css 4)

## Summary
- 4022 nodes · 13168 edges · 183 communities (143 shown, 40 thin omitted)
- Extraction: 85% EXTRACTED · 15% INFERRED · 0% AMBIGUOUS · INFERRED: 1963 edges (avg confidence: 0.93)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `f4dd1dcf`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- Review Focus
- Step
- pytest
- TurnStore
- investigation.py
- KnowledgeService
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
- Guided intake interview — design
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
- context
- EmbeddingSwitches
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
- test-kb/README.md
- test_workspace_api.py
- ticket-flow-copy.ts
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
- uuid
- devDependencies
- devDependencies
- pipeline/contracts.py
- ticket-flow.ts
- InvalidEvidence
- compilerOptions
- قواعد المعرفة العربية للعرض أمام لجنة التحكيم
- pydantic
- dependencies
- InvalidEvidence
- dependencies
- compilerOptions
- Result
- intake/api.ts
- test_final_fix_handoff.py
- ZainCash Support Workspace
- negative/README.md
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
- IntakeState
- TurnContext
- load_tickets
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
- Customer Conversation Intake Implementation Plan
- KnowledgeError
- config.py
- intake/test_repository.py
- jev.py
- submission.py
- db/repository.py
- db/repository.py
- config.py
- ModelChoice
- components-ai-thought-chain.tsx
- reviewEvidence
- intake/README.md
- pipeline/graph.py
- create_app
- main.py
- ZainCash support: architecture and ticket flow {#support-overview}
- FakeXHR
- employee-frontend/src/components/theme-provider.tsx
- agent.py
- test_taxonomy.py
- TicketRow
- fake_registry
- Customer phone identity design
- bill-payment-biller-notice.md
- api-entrypoint.sh
- ProviderRegistry
- test_workspace_schema.py
- index_deadlines
- build_pipeline
- RAG drafting verification — 2026-10-17
- intake/contracts.py
- Global Constraints
- Deviations from the spec (intentional, small)
- test_submission.py
- Global Constraints
- parse.py
- verify_pack.py
- Per-model evaluation (quality, system, cost) — design specification
- 7. Customer frontend design

## God Nodes (most connected - your core abstractions)
1. `Settings` - 188 edges
2. `Step` - 108 edges
3. `ModelChoice` - 91 edges
4. `KnowledgeService` - 85 edges
5. `ActiveModels` - 74 edges
6. `useCopy()` - 67 edges
7. `context()` - 64 edges
8. `fact()` - 63 edges
9. `message()` - 59 edges
10. `IntakeController` - 55 edges

## Surprising Connections (you probably didn't know these)
- `Repeatable local walkthrough` --references--> `Settings`  [INFERRED]
  docs/demo-readiness.md → backend/app/config.py
- `Ticket write paths` --references--> `upsert_tickets()`  [INFERRED]
  docs/superpowers/specs/2026-11-13-customer-phone-identity-design.md → backend/app/db/repository.py
- `Existing data` --references--> `upgrade_workspace_schema()`  [INFERRED]
  docs/superpowers/specs/2026-11-13-customer-phone-identity-design.md → backend/app/db/workspace_schema.py
- `Re-ask once` --references--> `QuestionRecord`  [INFERRED]
  docs/superpowers/specs/2026-11-13-guided-intake-interview-design.md → backend/app/intake/contracts.py
- `5.3 Knowledge-service boundary` --references--> `_DatabaseCall`  [INFERRED]
  docs/superpowers/specs/2026-11-02-maintainability-refactor-design.md → backend/app/kb/database.py

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **Cascade Classification Path** — docs_superpowers_specs_2026_10_07_support_pipeline_design_cascade, docs_superpowers_plans_2026_10_07_plan1_core_pipeline_part2_jev_classifier, docs_superpowers_plans_2026_10_07_plan1_core_pipeline_part2_gemini_classifier, docs_superpowers_plans_2026_10_07_plan1_core_pipeline_part2_cascade_combine, readme_human_approval [EXTRACTED 1.00]
- **Drafting Agent Toolset** — backend_app_pipeline_runner_lookup_transaction, backend_app_pipeline_runner_search_transactions, backend_app_pipeline_runner_get_customer_recent_transactions, backend_app_pipeline_runner_get_customer_ticket_history, backend_app_pipeline_runner_check_service_status, backend_app_pipeline_runner_search_knowledge_base, backend_app_pipeline_runner_flag_for_human, backend_app_pipeline_runner_submit_draft [EXTRACTED 1.00]
- **Ticket Processing Stage Flow** — backend_app_pipeline_runner_prepare, backend_app_pipeline_runner_jev_classify, backend_app_pipeline_runner_gemini_classify, backend_app_pipeline_runner_extract, backend_app_pipeline_runner_lookup, backend_app_pipeline_runner_decide, backend_app_pipeline_runner_draft [EXTRACTED 1.00]

## Communities (183 total, 40 thin omitted)

### Community 0 - "Review Focus"
Cohesion: 0.25
Nodes (7): Customer Frontend Maintainability Implementation Plan, Review Focus, Task 2: Make standalone typechecking and root test execution real, Task 3: Centralize test cleanup and shared intake fixtures mechanically, Task 6: Extract stable-ID sequential upload lifecycle with TDD, Task 8: Disable streaming Stop when no handler exists, Task 9: Run the complete customer acceptance matrix and final diff review

### Community 1 - "Step"
Cohesion: 0.11
Nodes (22): _Store, ActiveModels, Step, DraftModelInfo, batch_concurrency(), _local_pipeline(), ticket_timeout_s(), test_batch_concurrency_stays_within_bounds() (+14 more)

### Community 2 - "pytest"
Cohesion: 0.17
Nodes (42): _tool_chat(), answer(), call(), Checker, draft_state(), Knowledge, script(), submit() (+34 more)

### Community 3 - "TurnStore"
Cohesion: 0.18
Nodes (12): session(), OperationClaim, TurnResult, IntakeMessageRow, RevisionConflict, sanitize_intake_text(), _jsonable(), TurnStore (+4 more)

### Community 4 - "investigation.py"
Cohesion: 0.13
Nodes (15): parse_dt(), TxnRecord, DraftToolInputError, _datetime(), _days(), _field(), _involves(), _phone() (+7 more)

### Community 5 - "KnowledgeService"
Cohesion: 0.12
Nodes (18): Embedder, KnowledgeChunk, _Claim, _error_cost(), KnowledgeService, FakeEmbedder, test_category_filters_include_general_policies_and_validate_tags(), test_claim_locks_source_even_before_index_row_exists() (+10 more)

### Community 6 - "Card"
Cohesion: 0.14
Nodes (46): Task 8: Employee evidence panel and processing state, Task 5: Extract presentational DocumentList and KnowledgeReadiness components, 6.4 Focused view extraction, 6.5 Text and direction, Confidence(), Badge(), Button(), Card() (+38 more)

### Community 7 - "Customer conversation intake for ZainCash support"
Cohesion: 0.07
Nodes (28): 10. Verification and acceptance criteria, 11. Delivery and review, 1. Outcome and agreed requirements, 2. Current implementation and integration points, 3. Approach and boundaries, 4. Conversation state and turn flow, 5. Facts, evidence, and readiness, 6. Language and screenshot behavior (+20 more)

### Community 8 - "lib/types.ts"
Cohesion: 0.07
Nodes (49): Admin model configuration — employee frontend implementation plan, Backend API contract used here, File structure, Global Constraints, Review Focus, Task 1: API types, admin session and admin requests, Task 2: Strings, the AI locality chip, run models and the batch switch message, Task 3: Model choice logic and the change dialog (+41 more)

### Community 9 - "IntakeController"
Cohesion: 0.15
Nodes (14): Task 6: Customer API client and resumable UI state, Task 1: Cleanup-first removal of reference-verified dead code and dependencies, Task 7: Preserve resume-unavailable state across `startNew`, Task 7: Intake app data layer — phone helper, contracts, API, controller, Task 7: Customer frontend data layer, ControllerState, emptyState(), fileIdentity() (+6 more)

### Community 10 - "FakeJevRunnable"
Cohesion: 0.12
Nodes (18): CredentialCheck, DegradedCredentialChecker, _finite_nonnegative(), _get(), JevCredentialChecker, ResponseRunnable, test_bad_usage_cannot_poison_cost(), test_cancellation_propagates_with_cost_for_outer_timeout_owner() (+10 more)

### Community 11 - "test_rag_api.py"
Cohesion: 0.13
Nodes (21): client(), evidence_client(), test_actual_guardrail_failure_is_separate_from_reply(), test_concurrent_index_requests_share_active_work(), test_disabled_or_missing_provider_stores_without_indexing(), test_explicit_retry_tags_search_and_chunk_pagination(), test_health_distinguishes_failed_from_empty(), test_health_requires_compatible_nonempty_index() (+13 more)

### Community 12 - "employee-frontend/package.json"
Cohesion: 0.06
Nodes (30): @base-ui/react, class-variance-authority, cn, eslint, @eslint/js, eslint-plugin-react-hooks, eslint-plugin-react-refresh, @fontsource/tajawal (+22 more)

### Community 14 - "QueuePage.tsx"
Cohesion: 0.12
Nodes (55): Task 3: Split RunDetailPage and introduce bounded run-result loading, Task 12: Locale parity test and translated Runs pages, Task 16: Model detail, confusion matrix and predictions drawer, Task 10: Employee app — customer page and ticket header link, Task 9: Employee app — required phone, queue identity and search, batch entry, 6.4 Visible to all employees, 5.1 Data access, 7. Testing (+47 more)

### Community 15 - "Support Taxonomy Categories"
Cohesion: 0.21
Nodes (22): lookup, Account KYC, Account & Security, Agent Dispute, Agent Network, App Bug, Bill Payment, Card Issue (+14 more)

### Community 16 - "ui/package.json"
Cohesion: 0.08
Nodes (24): @base-ui/react, class-variance-authority, cn, eslint, @eslint/js, eslint-plugin-react-hooks, eslint-plugin-react-refresh, @fontsource/tajawal (+16 more)

### Community 17 - "locale.tsx"
Cohesion: 0.07
Nodes (47): App(), CustomerPage, EvaluationPage, InsightsPage, KnowledgePage, ModelsPage, NewBatchPage, QueuePage (+39 more)

### Community 18 - "users-frontend/package.json"
Cohesion: 0.08
Nodes (23): turbo, devDependencies, prettier, prettier-plugin-tailwindcss, turbo, typescript, engines, node (+15 more)

### Community 19 - "make_ticket"
Cohesion: 0.15
Nodes (23): build_graph(), PipelineDeps, InMemoryTransactionRepo, FakeClassifier, make_output(), intake_client(), pipeline(), reviewed() (+15 more)

### Community 20 - "test_draft_guardrails.py"
Cohesion: 0.14
Nodes (29): LookupResult, check_draft(), requests_credentials(), make_ticket(), check(), state(), test_aggregation_is_deduplicated_and_has_no_state_side_effects(), test_amount_occurrences_keep_their_own_currency_and_sign() (+21 more)

### Community 21 - "web/package.json"
Cohesion: 0.05
Nodes (41): clsx, jsdom, tailwind-merge, @testing-library/jest-dom, @testing-library/react, @testing-library/user-event, @workspace/ui, dependencies (+33 more)

### Community 22 - "test_recovery_regressions.py"
Cohesion: 0.12
Nodes (21): _command_settings(), ingest_kb_cmd(), init_db_cmd(), Mode, run_batch_cmd(), _run_in_memory(), _run_with_db(), seed_db_cmd() (+13 more)

### Community 23 - "compilerOptions"
Cohesion: 0.08
Nodes (23): compilerOptions, allowArbitraryExtensions, allowImportingTsExtensions, erasableSyntaxOnly, jsx, lib, module, moduleDetection (+15 more)

### Community 24 - "employee-frontend/components.json"
Cohesion: 0.09
Nodes (21): aliases, components, hooks, lib, ui, utils, iconLibrary, menuAccent (+13 more)

### Community 25 - "ModelSettingsStore"
Cohesion: 0.08
Nodes (16): ModelSettingAuditRow, ModelSettingRow, _iso(), ModelSettingsStore, test_choice_round_trip_keeps_colons_and_rejects_blank_model(), _store(), test_describe_reports_a_saved_model_that_is_no_longer_installed(), test_empty_store_uses_env_defaults() (+8 more)

### Community 26 - "compilerOptions"
Cohesion: 0.09
Nodes (22): compilerOptions, allowArbitraryExtensions, allowImportingTsExtensions, erasableSyntaxOnly, jsx, lib, module, moduleDetection (+14 more)

### Community 27 - "web/src/components/theme-provider.tsx"
Cohesion: 0.11
Nodes (17): App(), controller, disableTransitionsTemporarily(), getSystemTheme(), isEditableTarget(), isTheme(), ResolvedTheme, Theme (+9 more)

### Community 28 - "EmbeddingError"
Cohesion: 0.07
Nodes (44): EmbeddingBatch, EmbeddingError, _nonnegative_number(), OpenAICompatibleEmbedder, OpenRouterEmbedder, _ordered_vectors(), _response_cost(), Embeddings (+36 more)

### Community 29 - "Classify and Extract Prompts"
Cohesion: 0.33
Nodes (7): extract, gemini_classify, Pipeline Graph Orchestration, jev_classify, prepare, GeminiClassifier, JevClassifier

### Community 30 - "test_draft_tools.py"
Cohesion: 0.10
Nodes (36): IncidentRow, test_blank_intake_model_is_rejected(), test_contracts_reject_extra_keys(), test_datetimes_must_be_timezone_aware(), test_non_positive_image_limit_is_rejected(), ErrorEmbedder, settings(), state() (+28 more)

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
Cohesion: 0.11
Nodes (22): IndexAttemptLostError, GatedEmbedder, LateEmbedder, PaidEmbedder, count_chunks(), test_competing_callers_refuse_active_attempt_and_release_transactions(), test_db_deadline_cancelled_publication_cannot_commit_late(), test_db_deadline_is_cumulative_across_publication_statements() (+14 more)

### Community 36 - "web/components.json"
Cohesion: 0.10
Nodes (19): aliases, components, hooks, lib, ui, utils, iconLibrary, menuAccent (+11 more)

### Community 38 - "ChangeModelDialog.tsx"
Cohesion: 0.10
Nodes (24): 6.1 Route and access, 6.2 Page, 6.3 Change dialog, 6. Employee-frontend design, 5.2 Page structure, FilterSelect(), badgeVariants, buttonVariants (+16 more)

### Community 39 - "ui/components.json"
Cohesion: 0.10
Nodes (19): aliases, components, hooks, lib, ui, utils, iconLibrary, menuAccent (+11 more)

### Community 40 - "Settings"
Cohesion: 0.10
Nodes (13): Settings, test_anthropic_model_selects_the_draft_model_only(), test_defaults(), test_draft_token_prices_follow_the_selected_draft_model(), test_drafting_configuration_cannot_bypass_hard_limits(), test_drafting_limits_load_from_environment(), test_env_overrides(), test_legacy_gemini_model_names_are_qualified_for_openrouter() (+5 more)

### Community 41 - "Guided intake interview — design"
Cohesion: 0.06
Nodes (35): 1. Question rules (backend), 2. API contract, 3. Chat screen, 4. Review card, Actions, Additional issues, Approach, Backend (pytest, guarded `support_test`) (+27 more)

### Community 43 - "Human Review Gate"
Cohesion: 0.25
Nodes (4): support CLI, Support Workspace UI Plan, Review API, Workspace UI Verification

### Community 44 - "compilerOptions"
Cohesion: 0.12
Nodes (16): compilerOptions, allowImportingTsExtensions, erasableSyntaxOnly, lib, module, moduleDetection, noEmit, noFallthroughCasesInSwitch (+8 more)

### Community 46 - "PipelineState"
Cohesion: 0.10
Nodes (17): _Nodes, PipelineState, 1. Outcome, 2. Scope, 3. What the employee sees, 4. Which step is open, 5. Language, 7. Sentences (+9 more)

### Community 47 - "compilerOptions"
Cohesion: 0.12
Nodes (16): compilerOptions, allowImportingTsExtensions, erasableSyntaxOnly, lib, module, moduleDetection, noEmit, noFallthroughCasesInSwitch (+8 more)

### Community 48 - "Plan 3 RAG Drafting Implementation Plan"
Cohesion: 0.18
Nodes (11): Completion and review record — 2026-10-17, Execution handoff, File map and shared interfaces, Global Constraints, Plan 3 RAG Drafting Implementation Plan, Plan self-review, Review Focus, Task 1: Testable parsing and embedding boundary (+3 more)

### Community 57 - "parse_document"
Cohesion: 0.15
Nodes (22): DocumentParseError, parse_document(), make_pdf(), test_arabic_text_and_bom_are_preserved(), test_blank_pdf_tells_operator_to_use_ocr(), test_chunk_limit_is_enforced(), test_chunking_is_deterministic_bounded_and_overlapping(), test_empty_text_has_an_actionable_error() (+14 more)

### Community 58 - "AttachmentStore"
Cohesion: 0.14
Nodes (23): AttachmentStore, ImageRejected, NotOwned, OperationConflict, assert_same_operation(), png_bytes(), repo(), store() (+15 more)

### Community 59 - "contracts.ts"
Cohesion: 0.19
Nodes (29): Task 5: Add complete dependency-free API and persisted-session guards, createIntakeApi(), finiteNonnegative(), INTAKE_FALLBACK_MESSAGE, invalid(), isRecord(), language(), nullableString() (+21 more)

### Community 60 - "context"
Cohesion: 0.16
Nodes (35): Question, QuestionRecord, Readiness, assess_readiness(), context(), message(), test_full_payment_card_question_uses_safe_fallback(), test_assistant_text_cannot_ground_a_customer_fact() (+27 more)

### Community 61 - "EmbeddingSwitches"
Cohesion: 0.09
Nodes (15): EmbeddingSwitches, _view(), Task 4: The Models page, navigation and route, 4.8 Embedding switch (short pause), 4.10 API, 4.11 CLI, 4.1 Prerequisite: shared provider adapters, 4.2 Usage metering (+7 more)

### Community 62 - "knowledge-view.test.tsx"
Cohesion: 0.25
Nodes (13): acceptIndexRequest(), canRequestIndex(), PendingIndexes, persistPendingIndexes(), pollKnowledge(), refresh(), stop(), PollOptions (+5 more)

### Community 63 - "IntakePage.tsx"
Cohesion: 0.17
Nodes (23): Task 8: Chat screen — instant bubble, typing, reasons, quick replies, composer hints, AgentChat, AgentChatProps, AgentMessage, AssistantText(), AttachedFile, AttachedImage, ChatStatus (+15 more)

### Community 64 - "tasks"
Cohesion: 0.11
Nodes (18): dependsOn, inputs, outputs, cache, persistent, dependsOn, dependsOn, $schema (+10 more)

### Community 65 - "knowledge.py"
Cohesion: 0.11
Nodes (22): _configured(), delete_document(), download_document(), index_document(), list_chunks(), list_documents(), _require_provider(), search_knowledge() (+14 more)

### Community 66 - "ChangeModelDialog.tsx"
Cohesion: 0.15
Nodes (28): ConfirmDialog(), Dialog(), DialogContent(), DialogDescription(), DialogFooter(), DialogHeader(), DialogOverlay(), DialogPortal() (+20 more)

### Community 67 - "fact"
Cohesion: 0.19
Nodes (23): Analysis, EvidenceRef, fact(), test_reinspection_keeps_current_images_and_new_observations(), again(), initial(), test_review_after_failed_analysis_still_interprets_the_saved_message(), test_validation_failure_retains_usage_audit() (+15 more)

### Community 68 - "PipelineState"
Cohesion: 0.12
Nodes (15): 10. Remaining demo roadmap, 1. Intent and acceptance criteria, 3. Provider and configuration, 4. Knowledge ingestion and persistence, 5. Retrieval and evidence, 7. Draft guardrails and failure outcomes, 8. Pipeline, API, CLI and UI integration, 9. Demo policies and verification (+7 more)

### Community 69 - "results.py"
Cohesion: 0.17
Nodes (17): get_result(), list_results(), read_intake_attachment(), review_result(), ReviewInput, ReviewRow, TicketResultRow, employee_attachment() (+9 more)

### Community 70 - "make_ticket"
Cohesion: 0.22
Nodes (16): _deps(), _run(), test_concurrency_is_limited(), test_draft_node_never_retries_or_restarts_paid_work(), test_drafter_reasons_escalate(), draft(), test_empty_batch(), test_empty_ticket_escalates_without_model_calls() (+8 more)

### Community 71 - "intake/repository.py"
Cohesion: 0.18
Nodes (15): _display_name(), CustomerReview, IntakeAttachmentRow, attachment_from_row(), customer_review(), load_attachments(), load_messages(), _message() (+7 more)

### Community 72 - "RunRow"
Cohesion: 0.15
Nodes (14): get_run(), list_runs(), start_run(), BatchInput, RunRow, create_run(), run_job(), columns() (+6 more)

### Community 73 - "workspace.py"
Cohesion: 0.21
Nodes (6): get_session(), health(), insights(), workspace(), knowledge_configured(), latest_results_query()

### Community 74 - "FakeJevRunnable"
Cohesion: 0.29
Nodes (10): FakeJevRunnable, _criteria(), _run(), test_low_top_probability_is_uncertain(), test_one_main_call_with_all_questions(), test_order_check_uses_reversed_options(), test_order_disagreement_is_uncertain(), test_priority_level_maps_to_p_label() (+2 more)

### Community 75 - "test-kb/README.md"
Cohesion: 0.07
Nodes (14): Fictional RAG walkthrough inputs, توثيق الحساب — سياسة خيالية للعرض التجريبي, نزاع مع وكيل — سياسة خيالية للعرض التجريبي, أعطال التطبيق — سياسة خيالية للعرض التجريبي, دفع الفواتير — سياسة خيالية للعرض التجريبي, مشاكل البطاقة — سياسة خيالية للعرض التجريبي, التحويل المعلّق — سياسة خيالية للعرض التجريبي, تصعيد شبهة الاحتيال — سياسة خيالية للعرض التجريبي (+6 more)

### Community 76 - "test_workspace_api.py"
Cohesion: 0.11
Nodes (20): review_payload(), start_run(), test_batch_and_queue_expose_real_results(), test_batch_failure_is_isolated_and_conflicting_ids_rejected(), test_customer_profile_lists_the_latest_result_of_each_ticket(), test_only_jev_mode_is_configured_and_retired_modes_are_rejected(), test_progress_counts_only_durable_results_after_save_failure(), fail_one_save() (+12 more)

### Community 77 - "ticket-flow-copy.ts"
Cohesion: 0.14
Nodes (21): Task 3: Received, produced, and drafting events, AR, channelName(), checkLines(), EN, fieldLabel(), FIELDS, LOOKUP (+13 more)

### Community 79 - "devDependencies"
Cohesion: 0.12
Nodes (16): devDependencies, eslint, @eslint/js, eslint-plugin-react-hooks, eslint-plugin-react-refresh, globals, prettier, prettier-plugin-tailwindcss (+8 more)

### Community 80 - "judge-demo.ar.md"
Cohesion: 0.14
Nodes (13): أعطال التطبيق — سياسة خيالية للعرض التجريبي, استرجاع مبلغ شراء — سياسة خيالية للعرض التجريبي, استعادة الدخول — سياسة خيالية للعرض التجريبي, الاستفسار الآمن من الدعم — سياسة خيالية للعرض التجريبي, الاستفسار المؤقت للدعم في المهمة ٨ — سياسة خيالية للعرض التجريبي, التحويل المعلّق — سياسة خيالية للعرض التجريبي, التحويل لمستلم بالخطأ — سياسة خيالية للعرض التجريبي, الطلبات غير الواضحة وخارج النطاق — سياسة خيالية للعرض التجريبي (+5 more)

### Community 93 - "uuid"
Cohesion: 0.24
Nodes (12): command(), create(), test_actual_app_restart_reconciles_failed_placeholder(), test_failed_review_retry_cannot_reopen_submitted_session(), test_original_payload_identity_survives_sanitization(), test_publication_failure_is_retryable_without_restart(), fail_once(), test_receipt_reference_is_preserved() (+4 more)

### Community 94 - "devDependencies"
Cohesion: 0.11
Nodes (19): devDependencies, eslint, @eslint/js, eslint-plugin-react-hooks, eslint-plugin-react-refresh, globals, jsdom, @tailwindcss/vite (+11 more)

### Community 95 - "devDependencies"
Cohesion: 0.17
Nodes (12): devDependencies, eslint, @eslint/js, eslint-plugin-react-hooks, eslint-plugin-react-refresh, globals, tailwindcss, @types/node (+4 more)

### Community 96 - "pipeline/contracts.py"
Cohesion: 0.11
Nodes (26): LLMUnavailable, StructuredLLM, FieldPick, NormalizedTicket, FieldExtractor, _field(), fill_gaps(), finalize() (+18 more)

### Community 97 - "ticket-flow.ts"
Cohesion: 0.14
Nodes (25): buildTicketFlow(), teamName(), customerMessage(), defaultSelected(), excerpt(), FIELD_KEYS, fieldValue(), FlowStepState (+17 more)

### Community 98 - "InvalidEvidence"
Cohesion: 0.18
Nodes (17): ReviewText, InvalidEvidence, validate(), build_review(), _compact(), _render_value(), _ticket_text(), _tokens() (+9 more)

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
Nodes (29): Fact, canonical_digits(), normalize_reported_date(), _apply(), _check_reference(), _compact(), merge_analysis(), checked_update() (+21 more)

### Community 104 - "dependencies"
Cohesion: 0.20
Nodes (10): dependencies, @base-ui/react, class-variance-authority, cn, @fontsource/tajawal, @fontsource-variable/plus-jakarta-sans, react, react-dom (+2 more)

### Community 105 - "compilerOptions"
Cohesion: 0.17
Nodes (11): compilerOptions, jsx, lib, module, moduleResolution, outDir, skipLibCheck, strict (+3 more)

### Community 106 - "Result"
Cohesion: 0.08
Nodes (25): Employee Frontend Maintainability Implementation Plan, Global Constraints, Review Focus, Task 1: Remove reference-verified dead exports, components, and the Mermaid dependency, Task 4: Extract and test the pure queue projection, Task 6: Repair ExtractedField fixtures and make standalone typecheck real, Task 7: Repair employee README paths/test-count guidance and run final acceptance, SelectSeparator() (+17 more)

### Community 107 - "intake/api.ts"
Cohesion: 0.07
Nodes (43): Task 7: Bilingual customer chat, screenshots and reviewed submission, Task 4: Make pending operations discriminated and use one request identity, copy(), IntakeApi, parseJson(), readError(), session, UploadResult (+35 more)

### Community 108 - "test_final_fix_handoff.py"
Cohesion: 0.14
Nodes (17): process_batch(), assert_completed_evidence(), outer_deadlines(), runner_env(), build(), sessions(), test_concurrent_timeout_and_success_do_not_share_handoff(), test_exhausted_draft_budget_does_not_start_paid_work() (+9 more)

### Community 109 - "ZainCash Support Workspace"
Cohesion: 0.22
Nodes (9): Current capability boundaries, Data source, Modular file map, Open the right project, Run locally, shadcn conventions, Verification, Workflow (+1 more)

### Community 111 - "scripts"
Cohesion: 0.25
Nodes (8): scripts, build, dev, format, lint, preview, test, typecheck

### Community 112 - "lookup.py"
Cohesion: 0.10
Nodes (31): ExtractedField, _as_date(), _iqd_amount(), match_transaction(), TransactionRepo, decide(), empty_ticket_decision(), merge_reasons() (+23 more)

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
Nodes (36): Global Constraints, Intake Chat UI Implementation Plan, Task 1: Put the summary and receipt in the thread, Task 2: Put screenshots inside the composer, Task 3: Apply the workspace chat styles, Task 4: Check the page in the browser, Task 8: Intake app UI — phone screen, profile chip, change number, receipt, Review Focus (+28 more)

### Community 120 - "scripts"
Cohesion: 0.50
Nodes (4): scripts, format, lint, typecheck

### Community 122 - "IntakeState"
Cohesion: 0.15
Nodes (26): AskedQuestion, IntakeState, answer_choices(), answer_kind(), ask_for(), ask_once_keys(), asked_count(), asks_for_secret() (+18 more)

### Community 123 - "TurnContext"
Cohesion: 0.11
Nodes (14): TurnContext, IntakeGraph, _invitation(), grounded_analysis(), grounded_review(), image_evidence(), ScriptedIntakeModel, test_graph_budget_uses_the_pinned_choice_and_timeout() (+6 more)

### Community 124 - "load_tickets"
Cohesion: 0.16
Nodes (12): load_tickets(), _rows(), test_csv_with_bom_and_missing_columns(), test_duplicate_external_ids_keep_first(), test_invalid_phone_names_the_row(), test_json_object_without_ids(), test_jsonl_fixture_loads(), test_phones_are_canonical_and_missing_phones_stay_empty() (+4 more)

### Community 125 - "admin.py"
Cohesion: 0.12
Nodes (18): audit(), catalog(), _check_provider(), ChoiceInput, embedding_switch(), ModelOptions, models(), ProbeInput (+10 more)

### Community 126 - "guardrails.py"
Cohesion: 0.07
Nodes (42): Candidate, _add(), find_candidates(), normalize_phone(), _overlaps(), parse_amount(), resolve_date(), _safe_date() (+34 more)

### Community 127 - "test_cli.py"
Cohesion: 0.17
Nodes (9): test_config_error_exits_2(), boom(), test_ingest_directory_is_deterministic_and_duplicate_is_free(), test_ingest_disabled_configuration_never_calls_provider(), test_ingest_failure_exit_and_retry_stored(), test_ingest_invalid_source_does_not_stop_other_files(), test_ingest_limits_batch_without_partial_side_effects(), test_retry_stored_indexes_old_uploads_without_recovering_other_process_jobs() (+1 more)

### Community 128 - "Credentials"
Cohesion: 0.19
Nodes (7): Credentials, SessionView, IntakeService, make_intake_service(), builder(), Task 1: Record the Baseline and Remove Reference-Verified Dead Code, Task 5: Let the customer choose a detail to answer (`/ask`)

### Community 129 - "intake/model.py"
Cohesion: 0.12
Nodes (28): Attachment, ImageInput, ModelCall, ModelUnavailable, _analysis_prompt(), _bounded_context(), _guard_size(), IntakeModel (+20 more)

### Community 130 - "test_llm.py"
Cohesion: 0.09
Nodes (16): Sample, StructuredChatLLM, make_draft_model(), make_gemini_llm(), model_ids(), _current_models(), _llm(), _S (+8 more)

### Community 131 - "intake.py"
Cohesion: 0.17
Nodes (19): create_session(), _credentials(), _dump(), get_session(), post_message(), read_attachment(), remove_attachment(), request_review() (+11 more)

### Community 132 - "Review Focus"
Cohesion: 0.12
Nodes (16): api(), Review Focus, Task 1: Establish the safety baseline and remove tracked Graphify cache contents, Task 2: Delete the superseded architecture HTML after a fresh reference check, Task 3: Remove confirmed stale local runtime state and the duplicate screenshot, Task 4: Repair only current setup and processing documentation, Task 5: Restrict Docker build context without deleting installed dependencies, Task 6: Regenerate current Graphify outputs as the final mutating task (+8 more)

### Community 133 - "_DatabaseCall"
Cohesion: 0.13
Nodes (6): _abandoned(), _check_deadline(), _consume(), _DatabaseCall, Task 4: Extract KB Database Call Mechanics Without Changing Transactions, Question metadata

### Community 134 - "test_dbapi_commit_handoff_arbitrates_cancellation"
Cohesion: 0.19
Nodes (7): test_db_deadline_includes_pool_and_checkout_without_late_claim(), checked_in(), test_db_deadline_search_cancellation_is_nonblocking_and_retains_cost(), test_dbapi_commit_handoff_arbitrates_cancellation(), gate(), gate_before_dbapi(), gate_inside_dbapi()

### Community 135 - "Customer Conversation Intake Implementation Plan"
Cohesion: 0.20
Nodes (8): Completion audit — 2026-10-18, Customer Conversation Intake Implementation Plan, Execution conventions and repository baseline, File map and dependency order, Global Constraints, Plan review and execution handoff, Review Focus, Spec coverage and acceptance map

### Community 136 - "KnowledgeError"
Cohesion: 0.33
Nodes (3): DocumentNotFoundError, KnowledgeError, Task 14: Preserve Safe Knowledge 503s and Log Only Unexpected Diagnostic Types

### Community 137 - "config.py"
Cohesion: 0.08
Nodes (3): UnsupportedOperation, TypeSafeProvider, test_typesafe_status_and_unsupported_chat()

### Community 138 - "intake/test_repository.py"
Cohesion: 0.14
Nodes (10): IntakeSessionRow, InvalidCustomerPhone, initial_state(), IntakeRepository, repo(), test_invalid_phone_cannot_start_a_session(), test_relative_upload_directory_is_rooted_in_the_repository(), test_session_belongs_to_the_signed_in_customer() (+2 more)

### Community 139 - "jev.py"
Cohesion: 0.12
Nodes (23): Candidates, ClassificationResult, ClassifierOutput, Classifier, build_order_check(), build_questions(), build_state(), category_criteria() (+15 more)

### Community 140 - "submission.py"
Cohesion: 0.25
Nodes (8): Receipt, ReviewSnapshot, IntakeOperationRow, IntakeError, StaleReview, TurnBusy, SubmissionResult, SubmissionService

### Community 141 - "db/repository.py"
Cohesion: 0.14
Nodes (4): Base, TransactionRow, IntakeSubmissionRow, EmbeddingSwitchRow

### Community 142 - "db/repository.py"
Cohesion: 0.11
Nodes (26): ensure_customers(), finish_run(), load_incidents(), load_transactions(), save_outcomes(), _to_record(), _upsert(), upsert_tickets() (+18 more)

### Community 143 - "config.py"
Cohesion: 0.11
Nodes (15): ConfiguredEmbedder, draft_timeout_s(), eligibility(), env_defaults(), intake_timeout_s(), choice_for(), _Store, test_configured_embedder_follows_the_current_setting() (+7 more)

### Community 144 - "ModelChoice"
Cohesion: 0.10
Nodes (24): _chat(), _describe(), _draft(), _embed(), _extract(), _intake(), probe(), _ProbeAnswer (+16 more)

### Community 148 - "components-ai-thought-chain.tsx"
Cohesion: 0.11
Nodes (18): Status, StatusIcon(), statusStyles, StepContext, StepContextType, ThoughtChain(), ThoughtChainContent(), ThoughtChainItem() (+10 more)

### Community 149 - "reviewEvidence"
Cohesion: 0.18
Nodes (11): Task 2: Migrate active TicketFlow coverage, then retire the legacy trace/chart cluster, 6. How a result becomes the charts, 6.1 Verification and cleanup, 6.2 Retire the legacy trace/chart cluster, 6.3 Runs and request loading, 6. Employee frontend design, renderableTrace(), reviewEvidence() (+3 more)

### Community 151 - "pipeline/graph.py"
Cohesion: 0.06
Nodes (21): Passage, SearchResult, TicketExecution, _default_retry(), outcome_from_state(), _percentile(), _retryable(), DraftAlreadySubmitted (+13 more)

### Community 152 - "create_app"
Cohesion: 0.14
Nodes (15): make_engine(), make_sessionmaker(), reset_db(), create_app(), intake_failed(), intake_db(), env(), env() (+7 more)

### Community 153 - "main.py"
Cohesion: 0.10
Nodes (16): _safe_dispatch(), _accepts(), lifespan(), recover(), fail_intake_placeholders(), reconcile_intake_run(), recover_intake_processing(), dispatch_intake() (+8 more)

### Community 154 - "ZainCash support: architecture and ticket flow {#support-overview}"
Cohesion: 0.50
Nodes (3): 1 · System architecture {#system-architecture}, 2 · Ticket flow {#ticket-flow}, ZainCash support: architecture and ticket flow {#support-overview}

### Community 156 - "employee-frontend/src/components/theme-provider.tsx"
Cohesion: 0.20
Nodes (11): disableTransitionsTemporarily(), getSystemTheme(), isEditableTarget(), isTheme(), ResolvedTheme, Theme, THEME_VALUES, ThemeProvider() (+3 more)

### Community 157 - "agent.py"
Cohesion: 0.04
Nodes (32): KnowledgeExecutionError, DraftResult, _error_cost(), _Execution, _has_response_usage(), _ModelUsage, _number(), RagDrafter (+24 more)

### Community 158 - "test_taxonomy.py"
Cohesion: 0.11
Nodes (10): load_taxonomy(), most_urgent(), priority_rank(), TaxonomyError, tax(), taxonomy(), taxonomy(), taxonomy() (+2 more)

### Community 159 - "TicketRow"
Cohesion: 0.10
Nodes (23): get_customer(), KnowledgeIndexInput, KnowledgeSearchInput, TicketInput, customer_phone_or_none(), InvalidPhone, normalize_customer_phone(), CustomerRow (+15 more)

### Community 160 - "fake_registry"
Cohesion: 0.11
Nodes (25): CatalogCache, step_catalog(), fake_registry(), FakeProvider, BrokenStatusProvider, test_a_provider_whose_status_check_raises_is_listed_as_unreachable(), test_catalog_errors_stay_per_provider_and_cache_respects_ttl(), test_classify_catalog_only_offers_typesafe() (+17 more)

### Community 161 - "Customer phone identity design"
Cohesion: 0.13
Nodes (14): Backend, Customer phone identity design, Data model, Decisions, Employee API, employee-frontend, Error handling, Existing data (+6 more)

### Community 164 - "ProviderRegistry"
Cohesion: 0.05
Nodes (35): _classify(), Provider, _capabilities(), DraftProviderResponseError, OpenRouterChat, OpenRouterProvider, _per_million(), provider_errors() (+27 more)

### Community 165 - "test_workspace_schema.py"
Cohesion: 0.29
Nodes (8): assert_customer_schema(), LegacySchemaError, _nullable(), _table_exists(), upgrade_workspace_schema(), test_fresh_schema_passes_the_customer_check(), test_intake_sessions_without_a_customer_phone_stop_startup(), test_nullable_ticket_phone_stops_startup_with_a_reset_instruction()

### Community 166 - "index_deadlines"
Cohesion: 0.40
Nodes (3): index_deadlines(), settings(), expire_during_embedding()

### Community 167 - "build_pipeline"
Cohesion: 0.11
Nodes (23): SqlTransactionRepo, build_pipeline(), ConfigError, run_batch(), FakeStructuredLLM, ScriptedChat, _settings(), test_builds_jev_pipeline_with_injected_clients() (+15 more)

### Community 168 - "RAG drafting verification — 2026-10-17"
Cohesion: 0.08
Nodes (26): ingest(), support_test(), Evidence by layer, Known limitations and remaining work, Repeatable local walkthrough, Synthetic demo readiness, Backend Maintainability Implementation Plan, Global Constraints (+18 more)

### Community 169 - "intake/contracts.py"
Cohesion: 0.29
Nodes (4): _aware(), IntakeModel, Message, Shared contracts (implement in Task 1; extend only through explicit edits here)

### Community 170 - "Global Constraints"
Cohesion: 0.22
Nodes (9): Global Constraints, Task 1: Sentence catalog, Task 2: Which step is open, Task 4: Mermaid source, Task 5: Draw the charts on the ticket page, Ticket Flow Charts Implementation Plan, isArabicMessage(), SentenceId (+1 more)

### Community 171 - "Deviations from the spec (intentional, small)"
Cohesion: 0.29
Nodes (6): Deviations from the spec (intentional, small), Global Constraints, Per-model Evaluation Implementation Plan — Part 2 of 3 (evaluation engine), Task 11: `support eval` CLI and v2 export, Task 7: Metrics, Task 9: Runner, request validation and cost estimate

### Community 172 - "test_submission.py"
Cohesion: 0.32
Nodes (4): _payload(), test_concurrent_submit_dispatches_once(), test_second_request_id_reuses_the_approved_review(), test_submission_replay_creates_one_ticket()

### Community 173 - "Global Constraints"
Cohesion: 0.25
Nodes (7): Global Constraints, Per-model Evaluation Implementation Plan — Part 3 of 3 (frontend, translations, verification), Task 14: Evaluation view helpers, Task 15: Provenance, headline metrics, comparison table and empty state, Task 17: Run dialog, progress, page assembly, route and styles, Task 18: Documentation, full verification and manual check, Copy

### Community 174 - "parse.py"
Cohesion: 0.48
Nodes (4): TextChunk, _append_chunks(), _check_extracted_size(), _parse_pdf()

### Community 179 - "verify_pack.py"
Cohesion: 0.48
Nodes (3): digest(), main(), pointer()

### Community 180 - "Per-model evaluation (quality, system, cost) — design specification"
Cohesion: 0.20
Nodes (9): 1. Outcome and success criteria, 3. Decisions, 5.3 Text and direction, 5.4 Runs pages, 5.5 Import format, 5. Employee-frontend design, 6. Error handling, 8. Out of scope (+1 more)

### Community 181 - "7. Customer frontend design"
Cohesion: 0.50
Nodes (4): 7.1 Verification and cleanup, 7.2 Runtime contracts and persisted operations, 7.4 Controller, chat, and tests, 7. Customer frontend design

## Ambiguous Edges - Review These
- `Fraud Report` → `Plan 1 Live Smoke`  [AMBIGUOUS]
  README.md · relation: conceptually_related_to

## Knowledge Gaps
- **83 isolated node(s):** `zaincash-support`, `@base-ui/react`, `@fontsource-variable/plus-jakarta-sans`, `@fontsource/tajawal`, `@tailwindcss/vite` (+78 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 1252 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **40 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Settings` connect `Settings` to `Credentials`, `intake/model.py`, `Step`, `test_llm.py`, `pytest`, `KnowledgeService`, `config.py`, `intake/test_repository.py`, `test_rag_api.py`, `submission.py`, `jev.py`, `db/repository.py`, `config.py`, `ModelChoice`, `make_ticket`, `test_recovery_regressions.py`, `pipeline/graph.py`, `create_app`, `main.py`, `ModelSettingsStore`, `EmbeddingError`, `agent.py`, `test_taxonomy.py`, `test_draft_tools.py`, `fake_registry`, `test_kb_service.py`, `ProviderRegistry`, `test_workspace_schema.py`, `index_deadlines`, `build_pipeline`, `RAG drafting verification — 2026-10-17`, `AttachmentStore`, `context`, `intake/repository.py`, `test_workspace_api.py`, `test_final_fix_handoff.py`, `httpx`, `TurnContext`, `test_cli.py`?**
  _High betweenness centrality (0.095) - this node is a cross-community bridge._
- **Are the 54 inferred relationships involving `Settings` (e.g. with `_command_settings()` and `_run_in_memory()`) actually correct?**
  _`Settings` has 54 INFERRED edges - model-reasoned connections that need verification._
- **What connects `zaincash-support`, `@base-ui/react`, `@fontsource-variable/plus-jakarta-sans` to the rest of the system?**
  _83 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Step` be split into smaller, more focused modules?**
  _Cohesion score 0.1101010101010101 - nodes in this community are weakly interconnected._
- **Why does `2. Current state` connect `jev.py` to `Card`, `build_pipeline`, `Result`, `lookup.py`, `make_ticket`, `Per-model evaluation (quality, system, cost) — design specification`?**
  _High betweenness centrality (0.084) - this node is a cross-community bridge._
- **Are the 68 inferred relationships involving `Step` (e.g. with `catalog()` and `_check_provider()`) actually correct?**
  _`Step` has 68 INFERRED edges - model-reasoned connections that need verification._

### Low-confidence Hints
_AMBIGUOUS edges — the extractor was unsure. Verify before acting on these._

- **What is the exact relationship between `Fraud Report` and `Plan 1 Live Smoke`?**
  _Edge tagged AMBIGUOUS (relation: conceptually_related_to) - confidence is low._