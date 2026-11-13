# Graph Report - zaincash-support  (2026-11-13)

## Corpus Check
- 425 files · ~421,524 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 27 file(s) not represented in the graph (top: (none) 17, .jsonl 4, .css 4)

## Summary
- 3938 nodes · 12890 edges · 188 communities (147 shown, 41 thin omitted)
- Extraction: 86% EXTRACTED · 14% INFERRED · 0% AMBIGUOUS · INFERRED: 1868 edges (avg confidence: 0.93)
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
- test_draft_model.py
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
- main.py
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
- attachments.py
- contracts.ts
- intake/api.ts
- pipeline/contracts.py
- knowledge-view.test.tsx
- IntakePage.tsx
- tasks
- UploadedDocument
- intake/contracts.py
- fact
- PipelineState
- results.py
- make_ticket
- intake/repository.py
- test_submission.py
- ConfiguredEmbedder
- FakeJevRunnable
- test-kb/README.md
- test_workspace_api.py
- TicketReviewPage.tsx
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
- LLMUnavailable
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
- lookup.py
- compilerOptions
- Maintainability and stale-code refactor — design specification
- httpx
- web/tsconfig.json
- employee-frontend/tsconfig.json
- exports
- IntakePage
- scripts
- users-frontend/README.md
- intake/contracts.py
- TurnContext
- InvalidPhone
- admin.py
- guardrails.py
- test_cli.py
- pipeline/contracts.py
- intake/model.py
- test_llm.py
- intake.py
- Review Focus
- _DatabaseCall
- test_dbapi_commit_handoff_arbitrates_cancellation
- Customer Conversation Intake Implementation Plan
- KnowledgeError
- File structure
- find_candidates
- jev.py
- agent.py
- db/repository.py
- db/repository.py
- test_steps.py
- FakeProvider
- components-ai-thought-chain.tsx
- test_processing.py
- intake/README.md
- DraftResult
- create_app
- batch_jobs.py
- ZainCash support: architecture and ticket flow {#support-overview}
- Customer intake verification — 2026-10-18
- employee-frontend/src/components/theme-provider.tsx
- build_tools
- pipeline/graph.py
- knowledge.py
- catalog.py
- Customer phone identity design
- bill-payment-biller-notice.md
- api-entrypoint.sh
- config.py
- test_workspace_schema.py
- FieldPick
- build_pipeline
- RAG drafting verification — 2026-10-17
- _ModelUsage
- test_admin_api.py
- Deviations from the spec (intentional, small)
- probe.py
- 5. Backend design
- tools.py
- DraftContext
- Per-model evaluation (quality, system, cost) — design specification
- 4. Backend design
- ScriptedIntakeModel
- test_db_deadline_cancelled_publication_cannot_commit_late
- Backend
- 10. Verification and acceptance
- 8. Repository hygiene and current documentation

## God Nodes (most connected - your core abstractions)
1. `Settings` - 186 edges
2. `Step` - 108 edges
3. `ModelChoice` - 91 edges
4. `KnowledgeService` - 85 edges
5. `ActiveModels` - 74 edges
6. `useCopy()` - 67 edges
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
- `5.3 Knowledge-service boundary` --references--> `_DatabaseCall`  [INFERRED]
  docs/superpowers/specs/2026-11-02-maintainability-refactor-design.md → backend/app/kb/database.py
- `الأصل ونتيجة التحقق` --references--> `parse_document()`  [INFERRED]
  data/test-kb/README.md → backend/app/kb/parse.py

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **Cascade Classification Path** — docs_superpowers_specs_2026_10_07_support_pipeline_design_cascade, docs_superpowers_plans_2026_10_07_plan1_core_pipeline_part2_jev_classifier, docs_superpowers_plans_2026_10_07_plan1_core_pipeline_part2_gemini_classifier, docs_superpowers_plans_2026_10_07_plan1_core_pipeline_part2_cascade_combine, readme_human_approval [EXTRACTED 1.00]
- **Drafting Agent Toolset** — backend_app_pipeline_runner_lookup_transaction, backend_app_pipeline_runner_search_transactions, backend_app_pipeline_runner_get_customer_recent_transactions, backend_app_pipeline_runner_get_customer_ticket_history, backend_app_pipeline_runner_check_service_status, backend_app_pipeline_runner_search_knowledge_base, backend_app_pipeline_runner_flag_for_human, backend_app_pipeline_runner_submit_draft [EXTRACTED 1.00]
- **Ticket Processing Stage Flow** — backend_app_pipeline_runner_prepare, backend_app_pipeline_runner_jev_classify, backend_app_pipeline_runner_gemini_classify, backend_app_pipeline_runner_extract, backend_app_pipeline_runner_lookup, backend_app_pipeline_runner_decide, backend_app_pipeline_runner_draft [EXTRACTED 1.00]

## Communities (188 total, 41 thin omitted)

### Community 0 - "NewBatchPage.tsx"
Cohesion: 0.07
Nodes (36): Global Constraints, Per-model Evaluation Implementation Plan — Part 3 of 3 (frontend, translations, verification), Task 14: Evaluation view helpers, Task 15: Provenance, headline metrics, comparison table and empty state, Task 17: Run dialog, progress, page assembly, route and styles, Task 18: Documentation, full verification and manual check, 6.1 Route and access, 6.2 Page (+28 more)

### Community 1 - "Step"
Cohesion: 0.11
Nodes (32): _Store, ActiveModels, ModelChoice, Step, batch_concurrency(), _local_pipeline(), ticket_timeout_s(), fake_registry() (+24 more)

### Community 2 - "pytest"
Cohesion: 0.17
Nodes (40): _tool_chat(), answer(), call(), Checker, draft_state(), script(), submit(), pipeline() (+32 more)

### Community 3 - "TurnStore"
Cohesion: 0.18
Nodes (12): OperationClaim, TurnResult, RevisionConflict, sanitize_intake_text(), _jsonable(), TurnStore, fail_once(), repo() (+4 more)

### Community 4 - "investigation.py"
Cohesion: 0.14
Nodes (14): parse_dt(), TxnRecord, DraftToolInputError, _datetime(), _days(), _field(), _involves(), _phone() (+6 more)

### Community 5 - "test_draft_model.py"
Cohesion: 0.27
Nodes (8): make_draft_model(), response_payload(), run_provider_pipeline(), send(), search_response(), test_empty_choices_escalates_and_keeps_paid_response_usage(), test_failed_response_id_is_deduplicated_against_earlier_success(), test_other_conversion_value_errors_remain_unexpected()

### Community 6 - "Card"
Cohesion: 0.18
Nodes (35): Task 5: Extract presentational DocumentList and KnowledgeReadiness components, 6.4 Focused view extraction, Card(), CardContent(), CardHeader(), CardTitle(), Input(), AdminUnlock() (+27 more)

### Community 7 - "Customer conversation intake for ZainCash support"
Cohesion: 0.06
Nodes (31): 10. Verification and acceptance criteria, 11. Delivery and review, 1. Outcome and agreed requirements, 2. Current implementation and integration points, 3. Approach and boundaries, 4. Conversation state and turn flow, 5. Facts, evidence, and readiness, 6. Language and screenshot behavior (+23 more)

### Community 8 - "lib/types.ts"
Cohesion: 0.07
Nodes (45): Admin model configuration — employee frontend implementation plan, Backend API contract used here, File structure, Global Constraints, Review Focus, Task 1: API types, admin session and admin requests, Task 2: Strings, the AI locality chip, run models and the batch switch message, Task 3: Model choice logic and the change dialog (+37 more)

### Community 9 - "IntakeController"
Cohesion: 0.16
Nodes (10): Task 6: Customer API client and resumable UI state, Task 1: Cleanup-first removal of reference-verified dead code and dependencies, Task 7: Preserve resume-unavailable state across `startNew`, Task 7: Intake app data layer — phone helper, contracts, API, controller, emptyState(), IntakeController, isConflict(), isOffline() (+2 more)

### Community 10 - "FakeJevRunnable"
Cohesion: 0.10
Nodes (22): CredentialCheck, CredentialChecker, DegradedCredentialChecker, _finite_nonnegative(), _get(), JevCredentialChecker, test_contracts_reject_extra_keys(), test_datetimes_must_be_timezone_aware() (+14 more)

### Community 11 - "test_rag_api.py"
Cohesion: 0.09
Nodes (26): KnowledgeDocumentIndex, KnowledgeExecutionError, index_deadlines(), client(), evidence_client(), test_actual_guardrail_failure_is_separate_from_reply(), test_concurrent_index_requests_share_active_work(), test_disabled_or_missing_provider_stores_without_indexing() (+18 more)

### Community 12 - "employee-frontend/package.json"
Cohesion: 0.06
Nodes (30): @base-ui/react, class-variance-authority, cn, eslint, @eslint/js, eslint-plugin-react-hooks, eslint-plugin-react-refresh, @fontsource/tajawal (+22 more)

### Community 14 - "QueuePage.tsx"
Cohesion: 0.16
Nodes (41): Task 3: Split RunDetailPage and introduce bounded run-result loading, Task 16: Model detail, confusion matrix and predictions drawer, Task 10: Employee app — customer page and ticket header link, Task 9: Employee app — required phone, queue identity and search, batch entry, 5.1 Data access, 7. Testing, EmptyState(), ErrorState() (+33 more)

### Community 15 - "Support Taxonomy Categories"
Cohesion: 0.21
Nodes (22): lookup, Account KYC, Account & Security, Agent Dispute, Agent Network, App Bug, Bill Payment, Card Issue (+14 more)

### Community 16 - "ui/package.json"
Cohesion: 0.08
Nodes (24): @base-ui/react, class-variance-authority, cn, eslint, @eslint/js, eslint-plugin-react-hooks, eslint-plugin-react-refresh, @fontsource/tajawal (+16 more)

### Community 17 - "locale.tsx"
Cohesion: 0.10
Nodes (31): App(), CustomerPage, EvaluationPage, InsightsPage, KnowledgePage, ModelsPage, NewBatchPage, QueuePage (+23 more)

### Community 18 - "users-frontend/package.json"
Cohesion: 0.08
Nodes (23): turbo, devDependencies, prettier, prettier-plugin-tailwindcss, turbo, typescript, engines, node (+15 more)

### Community 19 - "make_ticket"
Cohesion: 0.23
Nodes (15): build_graph(), PipelineDeps, InMemoryTransactionRepo, load_taxonomy(), tax(), pipeline(), taxonomy(), test_run_batch_defaults_to_jev() (+7 more)

### Community 20 - "test_draft_guardrails.py"
Cohesion: 0.14
Nodes (27): LookupResult, requests_credentials(), check(), state(), test_aggregation_is_deduplicated_and_has_no_state_side_effects(), test_amount_occurrences_keep_their_own_currency_and_sign(), test_avoid_sharing_warning_does_not_excuse_a_later_request(), test_candidate_prompt_limit_does_not_hide_later_ungrounded_references() (+19 more)

### Community 21 - "web/package.json"
Cohesion: 0.05
Nodes (41): clsx, jsdom, tailwind-merge, @testing-library/jest-dom, @testing-library/react, @testing-library/user-event, @workspace/ui, dependencies (+33 more)

### Community 22 - "test_recovery_regressions.py"
Cohesion: 0.15
Nodes (14): _command_settings(), ingest_kb_cmd(), init_db_cmd(), Mode, run_batch_cmd(), _run_in_memory(), _run_with_db(), seed_db_cmd() (+6 more)

### Community 23 - "compilerOptions"
Cohesion: 0.08
Nodes (23): compilerOptions, allowArbitraryExtensions, allowImportingTsExtensions, erasableSyntaxOnly, jsx, lib, module, moduleDetection (+15 more)

### Community 24 - "employee-frontend/components.json"
Cohesion: 0.09
Nodes (21): aliases, components, hooks, lib, ui, utils, iconLibrary, menuAccent (+13 more)

### Community 25 - "main.py"
Cohesion: 0.06
Nodes (21): _accepts(), lifespan(), recover(), ModelSettingAuditRow, ModelSettingRow, EmbeddingSwitches, _view(), _iso() (+13 more)

### Community 26 - "compilerOptions"
Cohesion: 0.09
Nodes (22): compilerOptions, allowArbitraryExtensions, allowImportingTsExtensions, erasableSyntaxOnly, jsx, lib, module, moduleDetection (+14 more)

### Community 27 - "web/src/components/theme-provider.tsx"
Cohesion: 0.10
Nodes (19): App(), controller, disableTransitionsTemporarily(), getSystemTheme(), isEditableTarget(), isTheme(), ResolvedTheme, Theme (+11 more)

### Community 28 - "EmbeddingError"
Cohesion: 0.07
Nodes (45): EmbeddingBatch, EmbeddingError, _nonnegative_number(), OpenAICompatibleEmbedder, OpenRouterEmbedder, _ordered_vectors(), _response_cost(), Embeddings (+37 more)

### Community 29 - "Classify and Extract Prompts"
Cohesion: 0.33
Nodes (7): extract, gemini_classify, Pipeline Graph Orchestration, jev_classify, prepare, GeminiClassifier, JevClassifier

### Community 30 - "test_draft_tools.py"
Cohesion: 0.10
Nodes (30): IncidentRow, ErrorEmbedder, settings(), state(), test_all_eight_tools_and_seven_parallel_calls_execute_only_six(), test_database_faults_remain_distinct_and_record_paid_search_cost(), test_discovered_ref_can_be_inspected_but_not_promoted_to_match(), test_exact_and_fuzzy_queries_are_scoped_and_never_confirm_candidates() (+22 more)

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
Nodes (39): Embedder, KnowledgeChunk, KnowledgeService, FakeEmbedder, GatedEmbedder, LateEmbedder, PaidEmbedder, test_real_knowledge_search_snapshots_are_isolated_and_json_ready() (+31 more)

### Community 36 - "web/components.json"
Cohesion: 0.10
Nodes (19): aliases, components, hooks, lib, ui, utils, iconLibrary, menuAccent (+11 more)

### Community 38 - "ChangeModelDialog.tsx"
Cohesion: 0.11
Nodes (37): ConfirmDialog(), FilterSelect(), Button(), buttonVariants, Dialog(), DialogContent(), DialogDescription(), DialogFooter() (+29 more)

### Community 39 - "ui/components.json"
Cohesion: 0.10
Nodes (19): aliases, components, hooks, lib, ui, utils, iconLibrary, menuAccent (+11 more)

### Community 40 - "Settings"
Cohesion: 0.10
Nodes (15): Settings, test_blank_intake_model_is_rejected(), test_non_positive_image_limit_is_rejected(), test_relative_upload_directory_is_rooted_in_the_repository(), test_anthropic_model_selects_the_draft_model_only(), test_defaults(), test_draft_token_prices_follow_the_selected_draft_model(), test_drafting_configuration_cannot_bypass_hard_limits() (+7 more)

### Community 41 - "fact"
Cohesion: 0.23
Nodes (25): Attachment, Readiness, merge_analysis(), remove_attachment_evidence(), context(), message(), proposal(), test_additional_issue_is_resolved_in_place_instead_of_appended() (+17 more)

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

### Community 48 - "Plan 3 RAG Drafting Implementation Plan"
Cohesion: 0.20
Nodes (10): Completion and review record — 2026-10-17, Execution handoff, File map and shared interfaces, Global Constraints, Plan 3 RAG Drafting Implementation Plan, Plan self-review, Review Focus, Task 6: API/CLI indexing and persisted citation projection (+2 more)

### Community 57 - "parse_document"
Cohesion: 0.11
Nodes (29): TextChunk, _append_chunks(), _check_extracted_size(), DocumentParseError, parse_document(), _parse_pdf(), make_pdf(), test_arabic_text_and_bom_are_preserved() (+21 more)

### Community 58 - "attachments.py"
Cohesion: 0.07
Nodes (36): AttachmentStore, _display_name(), Credentials, SessionView, IntakeSessionRow, ImageRejected, IntakeError, InvalidCustomerPhone (+28 more)

### Community 59 - "contracts.ts"
Cohesion: 0.22
Nodes (27): Task 5: Add complete dependency-free API and persisted-session guards, createIntakeApi(), finiteNonnegative(), invalid(), isRecord(), language(), nullableString(), parseAttachment() (+19 more)

### Community 60 - "intake/api.ts"
Cohesion: 0.11
Nodes (24): Task 4: Make pending operations discriminated and use one request identity, IntakeApi, INTAKE_FALLBACK_MESSAGE, ControllerState, fileIdentity(), OwnedImage(), factText(), ReviewPanel() (+16 more)

### Community 61 - "pipeline/contracts.py"
Cohesion: 0.17
Nodes (18): detect_arabizi(), fold_arabic(), has_latin_mix(), _latin_words(), normalize(), sanitize_for_storage(), mask_cards(), to_ascii_digits() (+10 more)

### Community 62 - "knowledge-view.test.tsx"
Cohesion: 0.16
Nodes (17): DocumentListProps, acceptIndexRequest(), canRequestIndex(), PendingIndexes, persistPendingIndexes(), pollKnowledge(), refresh(), stop() (+9 more)

### Community 63 - "IntakePage.tsx"
Cohesion: 0.10
Nodes (29): AgentChat, AgentChatProps, AgentMessage, AssistantText(), AttachedFile, AttachedImage, ChatStatus, cn() (+21 more)

### Community 64 - "tasks"
Cohesion: 0.11
Nodes (18): dependsOn, inputs, outputs, cache, persistent, dependsOn, dependsOn, $schema (+10 more)

### Community 65 - "UploadedDocument"
Cohesion: 0.17
Nodes (13): session(), UploadedDocument, document_filename(), document_view(), DocumentValidationError, store_document(), ingest_one(), ingest_status() (+5 more)

### Community 67 - "fact"
Cohesion: 0.15
Nodes (29): Analysis, EvidenceRef, Fact, IntakeModel, dispatch_intake(), fact(), grounded_analysis(), image_evidence() (+21 more)

### Community 68 - "PipelineState"
Cohesion: 0.11
Nodes (18): 10. Remaining demo roadmap, 1. Intent and acceptance criteria, 3. Provider and configuration, 4. Knowledge ingestion and persistence, 5. Retrieval and evidence, 6. Bounded investigation agent, 7. Draft guardrails and failure outcomes, 8. Pipeline, API, CLI and UI integration (+10 more)

### Community 69 - "results.py"
Cohesion: 0.10
Nodes (24): get_customer(), get_session(), get_result(), list_results(), read_intake_attachment(), review_result(), health(), insights() (+16 more)

### Community 70 - "make_ticket"
Cohesion: 0.23
Nodes (20): ClassificationResult, JevClassifier, FakeClassifier, make_output(), make_ticket(), _deps(), _run(), test_concurrency_is_limited() (+12 more)

### Community 71 - "intake/repository.py"
Cohesion: 0.12
Nodes (30): CustomerReview, Receipt, IntakeAttachmentRow, IntakeMessageRow, IntakeOperationRow, IntakeSubmissionRow, assert_same_operation(), attachment_from_row() (+22 more)

### Community 72 - "test_submission.py"
Cohesion: 0.32
Nodes (4): _payload(), test_concurrent_submit_dispatches_once(), test_second_request_id_reuses_the_approved_review(), test_submission_replay_creates_one_ticket()

### Community 73 - "ConfiguredEmbedder"
Cohesion: 0.28
Nodes (4): ConfiguredEmbedder, choice_for(), _Store, test_configured_embedder_follows_the_current_setting()

### Community 74 - "FakeJevRunnable"
Cohesion: 0.29
Nodes (10): FakeJevRunnable, _criteria(), _run(), test_low_top_probability_is_uncertain(), test_one_main_call_with_all_questions(), test_order_check_uses_reversed_options(), test_order_disagreement_is_uncertain(), test_priority_level_maps_to_p_label() (+2 more)

### Community 75 - "test-kb/README.md"
Cohesion: 0.07
Nodes (14): Fictional RAG walkthrough inputs, توثيق الحساب — سياسة خيالية للعرض التجريبي, نزاع مع وكيل — سياسة خيالية للعرض التجريبي, أعطال التطبيق — سياسة خيالية للعرض التجريبي, دفع الفواتير — سياسة خيالية للعرض التجريبي, مشاكل البطاقة — سياسة خيالية للعرض التجريبي, التحويل المعلّق — سياسة خيالية للعرض التجريبي, تصعيد شبهة الاحتيال — سياسة خيالية للعرض التجريبي (+6 more)

### Community 76 - "test_workspace_api.py"
Cohesion: 0.14
Nodes (15): review_payload(), start_run(), test_batch_and_queue_expose_real_results(), test_batch_failure_is_isolated_and_conflicting_ids_rejected(), test_customer_profile_lists_the_latest_result_of_each_ticket(), test_only_jev_mode_is_configured_and_retired_modes_are_rejected(), test_progress_counts_only_durable_results_after_save_failure(), fail_one_save() (+7 more)

### Community 77 - "TicketReviewPage.tsx"
Cohesion: 0.15
Nodes (26): Task 8: Employee evidence panel and processing state, Task 12: Locale parity test and translated Runs pages, Confidence(), intakeFixture, factValue(), IntakeEvidence(), ReportedDetails(), Screenshot() (+18 more)

### Community 79 - "devDependencies"
Cohesion: 0.12
Nodes (16): devDependencies, eslint, @eslint/js, eslint-plugin-react-hooks, eslint-plugin-react-refresh, globals, prettier, prettier-plugin-tailwindcss (+8 more)

### Community 80 - "judge-demo.ar.md"
Cohesion: 0.14
Nodes (13): أعطال التطبيق — سياسة خيالية للعرض التجريبي, استرجاع مبلغ شراء — سياسة خيالية للعرض التجريبي, استعادة الدخول — سياسة خيالية للعرض التجريبي, الاستفسار الآمن من الدعم — سياسة خيالية للعرض التجريبي, الاستفسار المؤقت للدعم في المهمة ٨ — سياسة خيالية للعرض التجريبي, التحويل المعلّق — سياسة خيالية للعرض التجريبي, التحويل لمستلم بالخطأ — سياسة خيالية للعرض التجريبي, الطلبات غير الواضحة وخارج النطاق — سياسة خيالية للعرض التجريبي (+5 more)

### Community 93 - "test_recovery_regressions.py"
Cohesion: 0.35
Nodes (9): command(), create(), test_actual_app_restart_reconciles_failed_placeholder(), test_failed_review_retry_cannot_reopen_submitted_session(), test_original_payload_identity_survives_sanitization(), test_publication_failure_is_retryable_without_restart(), test_receipt_reference_is_preserved(), test_stale_attempt_audit_is_retained_once_with_attempt_identity() (+1 more)

### Community 94 - "devDependencies"
Cohesion: 0.11
Nodes (19): devDependencies, eslint, @eslint/js, eslint-plugin-react-hooks, eslint-plugin-react-refresh, globals, jsdom, @tailwindcss/vite (+11 more)

### Community 95 - "devDependencies"
Cohesion: 0.17
Nodes (12): devDependencies, eslint, @eslint/js, eslint-plugin-react-hooks, eslint-plugin-react-refresh, globals, tailwindcss, @types/node (+4 more)

### Community 96 - "LLMUnavailable"
Cohesion: 0.09
Nodes (19): LLMUnavailable, StructuredLLM, ExtractedSpan, _Fields, GeminiExtractor, GeminiFields, verified_pick(), render_prompt() (+11 more)

### Community 97 - "ticket-flow.ts"
Cohesion: 0.05
Nodes (70): Task 1: Sentence catalog, Task 2: Which step is open, Task 3: Received, produced, and drafting events, Task 4: Mermaid source, Task 5: Draw the charts on the ticket page, Employee Frontend Maintainability Implementation Plan, Global Constraints, Task 2: Migrate active TicketFlow coverage, then retire the legacy trace/chart cluster (+62 more)

### Community 98 - "review.py"
Cohesion: 0.17
Nodes (15): ReviewSnapshot, ReviewText, build_review(), _compact(), _render_value(), _ticket_text(), _tokens(), validate_review_numbers() (+7 more)

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
Cohesion: 0.16
Nodes (15): canonical_digits(), normalize_reported_date(), InvalidEvidence, _apply(), _check_reference(), _compact(), checked_update(), _newer_correction() (+7 more)

### Community 104 - "dependencies"
Cohesion: 0.20
Nodes (10): dependencies, @base-ui/react, class-variance-authority, cn, @fontsource/tajawal, @fontsource-variable/plus-jakarta-sans, react, react-dom (+2 more)

### Community 105 - "compilerOptions"
Cohesion: 0.17
Nodes (11): compilerOptions, jsx, lib, module, moduleResolution, outDir, skipLibCheck, strict (+3 more)

### Community 106 - "ref_vitest"
Cohesion: 0.07
Nodes (27): Review Focus, Task 1: Remove reference-verified dead exports, components, and the Mermaid dependency, Task 4: Extract and test the pure queue projection, Task 6: Repair ExtractedField fixtures and make standalone typecheck real, Task 7: Repair employee README paths/test-count guidance and run final acceptance, SelectSeparator(), originalLocale, projectQueue() (+19 more)

### Community 107 - "IntakePage.test.tsx"
Cohesion: 0.10
Nodes (26): Task 7: Bilingual customer chat, screenshots and reviewed submission, copy(), parseJson(), readError(), FakeXHR, session, UploadResult, IntakeRequestError (+18 more)

### Community 108 - "test_final_fix_handoff.py"
Cohesion: 0.10
Nodes (24): Passage, RagDrafter, DraftExecutionError, Knowledge, assert_completed_evidence(), faulty_knowledge(), read(), outer_deadlines() (+16 more)

### Community 109 - "ZainCash Support Workspace"
Cohesion: 0.22
Nodes (9): Current capability boundaries, Data source, Modular file map, Open the right project, Run locally, shadcn conventions, Verification, Workflow (+1 more)

### Community 111 - "scripts"
Cohesion: 0.25
Nodes (8): scripts, build, dev, format, lint, preview, test, typecheck

### Community 112 - "lookup.py"
Cohesion: 0.14
Nodes (16): RunSummary, _as_date(), _iqd_amount(), match_transaction(), TransactionRepo, _ex(), _match(), test_ambiguous_then_disambiguated_by_counterpart() (+8 more)

### Community 113 - "compilerOptions"
Cohesion: 0.29
Nodes (6): compilerOptions, module, moduleResolution, skipLibCheck, strict, target

### Community 114 - "Maintainability and stale-code refactor — design specification"
Cohesion: 0.18
Nodes (10): 1. Outcome and success criteria, 2. Audit baseline, 3. Selected approach and sequence, 4. Boundaries and non-goals, 6.1 Verification and cleanup, 6.2 Retire the legacy trace/chart cluster, 6.3 Runs and request loading, 6. Employee frontend design (+2 more)

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

### Community 119 - "IntakePage"
Cohesion: 0.07
Nodes (31): Global Constraints, Intake Chat UI Implementation Plan, Task 1: Put the summary and receipt in the thread, Task 2: Put screenshots inside the composer, Task 3: Apply the workspace chat styles, Task 4: Check the page in the browser, Customer Frontend Maintainability Implementation Plan, Global Constraints (+23 more)

### Community 120 - "scripts"
Cohesion: 0.50
Nodes (4): scripts, format, lint, typecheck

### Community 122 - "intake/contracts.py"
Cohesion: 0.21
Nodes (20): IntakeState, Question, _asked_already(), asks_for_secret(), assess_readiness(), _can_ask(), choose_question(), _fallback() (+12 more)

### Community 123 - "TurnContext"
Cohesion: 0.19
Nodes (7): QuestionRecord, TurnContext, IntakeGraph, _invitation(), test_graph_budget_uses_the_pinned_choice_and_timeout(), test_pin_failure_is_reported_as_model_unavailable(), test_without_pinning_the_budget_uses_settings()

### Community 124 - "InvalidPhone"
Cohesion: 0.08
Nodes (31): customer_phone_or_none(), InvalidPhone, normalize_customer_phone(), _ticket_phone(), load_jsonl(), load_tickets(), _rows(), initial_state() (+23 more)

### Community 125 - "admin.py"
Cohesion: 0.12
Nodes (18): audit(), catalog(), _check_provider(), ChoiceInput, embedding_switch(), ModelOptions, models(), ProbeInput (+10 more)

### Community 126 - "guardrails.py"
Cohesion: 0.13
Nodes (13): resolve_date(), _safe_date(), _iso(), normalize_value(), check_draft(), _citation_findings(), _exact_amount(), _grounding_findings() (+5 more)

### Community 127 - "test_cli.py"
Cohesion: 0.15
Nodes (8): test_config_error_exits_2(), boom(), test_ingest_directory_is_deterministic_and_duplicate_is_free(), test_ingest_disabled_configuration_never_calls_provider(), test_ingest_failure_exit_and_retry_stored(), test_ingest_invalid_source_does_not_stop_other_files(), test_ingest_limits_batch_without_partial_side_effects(), test_settings_validation_is_safe_field_diagnostic_exit_2()

### Community 128 - "pipeline/contracts.py"
Cohesion: 0.21
Nodes (11): Candidates, ClassifierOutput, ExtractedField, NormalizedTicket, Classifier, FieldExtractor, _field(), fill_gaps() (+3 more)

### Community 129 - "intake/model.py"
Cohesion: 0.11
Nodes (30): ImageInput, ModelCall, ModelUnavailable, _analysis_prompt(), _bounded_context(), _guard_size(), IntakeModel, validate() (+22 more)

### Community 130 - "test_llm.py"
Cohesion: 0.10
Nodes (14): Sample, StructuredChatLLM, make_gemini_llm(), DraftModelInfo, _llm(), _S, test_draft_model_uses_millisecond_timeout_and_disables_sdk_retries(), test_openrouter_reported_cost_takes_precedence_over_token_estimate() (+6 more)

### Community 131 - "intake.py"
Cohesion: 0.16
Nodes (20): create_session(), _credentials(), _dump(), get_session(), post_message(), read_attachment(), remove_attachment(), request_review() (+12 more)

### Community 132 - "Review Focus"
Cohesion: 0.11
Nodes (17): api(), Global Constraints, Repository Hygiene Maintainability Implementation Plan, Review Focus, Task 1: Establish the safety baseline and remove tracked Graphify cache contents, Task 2: Delete the superseded architecture HTML after a fresh reference check, Task 3: Remove confirmed stale local runtime state and the duplicate screenshot, Task 4: Repair only current setup and processing documentation (+9 more)

### Community 133 - "_DatabaseCall"
Cohesion: 0.12
Nodes (7): SearchResult, _abandoned(), _check_deadline(), _consume(), _DatabaseCall, _error_cost(), Task 4: Extract KB Database Call Mechanics Without Changing Transactions

### Community 134 - "test_dbapi_commit_handoff_arbitrates_cancellation"
Cohesion: 0.47
Nodes (4): test_dbapi_commit_handoff_arbitrates_cancellation(), gate(), gate_before_dbapi(), gate_inside_dbapi()

### Community 135 - "Customer Conversation Intake Implementation Plan"
Cohesion: 0.25
Nodes (8): Completion audit — 2026-10-18, Customer Conversation Intake Implementation Plan, Execution conventions and repository baseline, File map and dependency order, Global Constraints, Plan review and execution handoff, Review Focus, Spec coverage and acceptance map

### Community 136 - "KnowledgeError"
Cohesion: 0.23
Nodes (5): _Claim, DocumentNotFoundError, IndexAttemptLostError, KnowledgeError, Task 14: Preserve Safe Knowledge 503s and Log Only Unexpected Diagnostic Types

### Community 137 - "File structure"
Cohesion: 0.11
Nodes (8): DraftProviderResponseError, OpenRouterChat, provider_errors(), test_registry_includes_ollama_and_its_errors(), File structure, Task 11: Configuration, Docker and documentation, Task 2: OpenRouter and TypeSafe providers, registry, generic embedder, Task 3: Ollama provider

### Community 138 - "find_candidates"
Cohesion: 0.23
Nodes (15): Candidate, _add(), find_candidates(), normalize_phone(), _overlaps(), parse_amount(), test_amount_forms(), test_arabic_indic_amount_not_confused_with_phone() (+7 more)

### Community 139 - "jev.py"
Cohesion: 0.28
Nodes (8): build_order_check(), build_questions(), build_state(), category_criteria(), _input_tokens(), _picks(), _priority(), Taxonomy

### Community 140 - "agent.py"
Cohesion: 0.13
Nodes (7): DraftAlreadySubmitted, DraftToolLimit, _bounded(), visit(), guarded(), invoke(), _json()

### Community 141 - "db/repository.py"
Cohesion: 0.13
Nodes (6): Base, CustomerRow, init_db(), repo(), test_repeated_init_db_keeps_existing_tickets(), test_session_belongs_to_the_signed_in_customer()

### Community 142 - "db/repository.py"
Cohesion: 0.11
Nodes (26): get_run(), list_runs(), start_run(), ensure_customers(), RunRow, TransactionRow, create_run(), finish_run() (+18 more)

### Community 143 - "test_steps.py"
Cohesion: 0.18
Nodes (11): draft_timeout_s(), env_defaults(), intake_timeout_s(), _settings(), test_eligibility(), test_env_defaults_match_todays_settings(), test_env_overrides_for_draft_and_intake(), test_local_timeouts_and_limits() (+3 more)

### Community 144 - "FakeProvider"
Cohesion: 0.15
Nodes (13): probe(), FakeProvider, _registry(), StructuredChat, test_draft_probe_requires_a_correct_tool_call(), test_embed_and_classify_probes(), test_every_step_has_a_probe(), test_intake_probe_sends_an_image_and_needs_parsed_output() (+5 more)

### Community 148 - "components-ai-thought-chain.tsx"
Cohesion: 0.13
Nodes (17): Status, StatusIcon(), statusStyles, StepContext, StepContextType, ThoughtChain(), ThoughtChainContent(), ThoughtChainItem() (+9 more)

### Community 149 - "test_processing.py"
Cohesion: 0.53
Nodes (4): _submit(), test_committed_but_unscheduled_ticket_survives_recovery(), test_failed_outcome_save_preserves_placeholder_and_reconciles_counts(), test_processing_ticket_rejects_review()

### Community 151 - "DraftResult"
Cohesion: 0.16
Nodes (8): DraftResult, Drafter, NullDrafter, UnavailableDrafter, draft(), draft(), draft(), 2. Current implementation and integration points

### Community 152 - "create_app"
Cohesion: 0.09
Nodes (27): make_engine(), make_sessionmaker(), reset_db(), create_app(), intake_failed(), intake_client(), intake_db(), reviewed() (+19 more)

### Community 153 - "batch_jobs.py"
Cohesion: 0.16
Nodes (18): save_outcomes(), TicketOutcome, TicketExecution, outcome_from_state(), _percentile(), summarize(), outcome_to_dict(), outcome_to_row() (+10 more)

### Community 154 - "ZainCash support: architecture and ticket flow {#support-overview}"
Cohesion: 0.50
Nodes (3): 1 · System architecture {#system-architecture}, 2 · Ticket flow {#ticket-flow}, ZainCash support: architecture and ticket flow {#support-overview}

### Community 155 - "Customer intake verification — 2026-10-18"
Cohesion: 0.25
Nodes (6): Browser handoff, Customer intake verification — 2026-10-18, Final automated checks, Live vision and paired review, Repaired gaps and regression evidence, Review decisions and remaining limits

### Community 156 - "employee-frontend/src/components/theme-provider.tsx"
Cohesion: 0.23
Nodes (11): disableTransitionsTemporarily(), getSystemTheme(), isEditableTarget(), isTheme(), ResolvedTheme, Theme, THEME_VALUES, ThemeProvider() (+3 more)

### Community 157 - "build_tools"
Cohesion: 0.12
Nodes (5): DraftSubmission, build_tools(), flag(), retrieve(), _error_cost()

### Community 158 - "pipeline/graph.py"
Cohesion: 0.09
Nodes (25): Decision, _default_retry(), _retryable(), decide(), empty_ticket_decision(), merge_reasons(), note_for(), _unique() (+17 more)

### Community 159 - "knowledge.py"
Cohesion: 0.11
Nodes (16): _configured(), delete_document(), download_document(), index_document(), list_chunks(), list_documents(), _require_provider(), search_knowledge() (+8 more)

### Community 160 - "catalog.py"
Cohesion: 0.16
Nodes (10): CatalogCache, step_catalog(), ProviderRegistry, UnknownProvider, BrokenStatusProvider, test_a_provider_whose_status_check_raises_is_listed_as_unreachable(), test_catalog_errors_stay_per_provider_and_cache_respects_ttl(), test_classify_catalog_only_offers_typesafe() (+2 more)

### Community 161 - "Customer phone identity design"
Cohesion: 0.20
Nodes (9): Canonical phone format, Customer phone identity design, Decisions, employee-frontend, Error handling, Intent, Out of scope, Testing (+1 more)

### Community 164 - "config.py"
Cohesion: 0.07
Nodes (19): UnsupportedOperation, _capabilities(), OpenRouterProvider, _per_million(), TypeSafeProvider, eligibility(), Capability, CatalogEntry (+11 more)

### Community 165 - "test_workspace_schema.py"
Cohesion: 0.29
Nodes (8): assert_customer_schema(), LegacySchemaError, _nullable(), _table_exists(), upgrade_workspace_schema(), test_fresh_schema_passes_the_customer_check(), test_intake_sessions_without_a_customer_phone_stop_startup(), test_nullable_ticket_phone_stops_startup_with_a_reset_instruction()

### Community 166 - "FieldPick"
Cohesion: 0.40
Nodes (11): FieldPick, finalize(), FakeExtractor, _setup(), test_fill_gaps_noop_and_failure_tolerant(), test_fill_gaps_only_asks_for_weak_required_fields(), test_gemini_span_not_in_text_is_null(), test_gemini_word_amount_uses_normalized_hint() (+3 more)

### Community 167 - "build_pipeline"
Cohesion: 0.12
Nodes (23): SqlTransactionRepo, build_pipeline(), ConfigError, model_ids(), run_batch(), FakeStructuredLLM, ScriptedChat, _settings() (+15 more)

### Community 168 - "RAG drafting verification — 2026-10-17"
Cohesion: 0.12
Nodes (17): ingest(), support_test(), Evidence by layer, Known limitations and remaining work, Repeatable local walkthrough, Synthetic demo readiness, Backend Maintainability Implementation Plan, Global Constraints (+9 more)

### Community 169 - "_ModelUsage"
Cohesion: 0.23
Nodes (5): _error_cost(), _has_response_usage(), _ModelUsage, _number(), Task 11: Use Draft-Model-Specific Fallback Token Prices

### Community 170 - "test_admin_api.py"
Cohesion: 0.12
Nodes (13): ProbeResult, make_client(), test_admin_is_disabled_without_a_token(), test_models_and_catalog(), test_non_ascii_and_blank_tokens_are_rejected(), test_save_rejections_change_nothing(), test_test_save_and_audit(), test_choice_round_trip_keeps_colons_and_rejects_blank_model() (+5 more)

### Community 171 - "Deviations from the spec (intentional, small)"
Cohesion: 0.29
Nodes (6): Deviations from the spec (intentional, small), Global Constraints, Per-model Evaluation Implementation Plan — Part 2 of 3 (evaluation engine), Task 11: `support eval` CLI and v2 export, Task 7: Metrics, Task 9: Runner, request validation and cost estimate

### Community 172 - "probe.py"
Cohesion: 0.11
Nodes (13): _chat(), _classify(), _describe(), _draft(), _embed(), _extract(), _intake(), _ProbeAnswer (+5 more)

### Community 173 - "5. Backend design"
Cohesion: 0.29
Nodes (5): 5.1 Dead-code cleanup, 5.3 Knowledge-service boundary, 5.4 Shared backend boundaries, 5.5 Confirmed backend defect fixes, 5. Backend design

### Community 174 - "tools.py"
Cohesion: 0.24
Nodes (8): _Flag, _History, _Input, _Knowledge, _Lookup, _Recent, _Search, _Service

### Community 179 - "DraftContext"
Cohesion: 0.20
Nodes (3): _Execution, DraftContext, Task 3: Ticket-scoped investigation and all eight tools

### Community 180 - "Per-model evaluation (quality, system, cost) — design specification"
Cohesion: 0.20
Nodes (9): 1. Outcome and success criteria, 3. Decisions, 5.3 Text and direction, 5.4 Runs pages, 5.5 Import format, 5. Employee-frontend design, 6. Error handling, 8. Out of scope (+1 more)

### Community 181 - "4. Backend design"
Cohesion: 0.20
Nodes (10): 4.10 API, 4.11 CLI, 4.2 Usage metering, 4.4 Evaluation model list, 4.5 Dataset (`data/eval/`), 4.6 Runner, 4.7 Metrics, 4.8 Cost estimate (+2 more)

### Community 183 - "test_db_deadline_cancelled_publication_cannot_commit_late"
Cohesion: 0.29
Nodes (3): test_db_deadline_cancelled_publication_cannot_commit_late(), test_db_deadline_is_cumulative_across_publication_statements(), changed_index()

### Community 184 - "Backend"
Cohesion: 0.33
Nodes (6): Backend, Data model, Employee API, Existing data, Intake, Ticket write paths

### Community 185 - "10. Verification and acceptance"
Cohesion: 0.40
Nodes (5): 10. Verification and acceptance, Backend, Customer frontend, Employee frontend, Repository and Docker

### Community 187 - "8. Repository hygiene and current documentation"
Cohesion: 0.50
Nodes (4): 8.1 Approved deletions, 8.2 Docker and documentation, 8.3 Graphify outputs, 8. Repository hygiene and current documentation

## Ambiguous Edges - Review These
- `Fraud Report` → `Plan 1 Live Smoke`  [AMBIGUOUS]
  README.md · relation: conceptually_related_to

## Knowledge Gaps
- **83 isolated node(s):** `zaincash-support`, `@base-ui/react`, `@fontsource-variable/plus-jakarta-sans`, `@fontsource/tajawal`, `@tailwindcss/vite` (+78 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 1220 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **41 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Settings` connect `Settings` to `intake/model.py`, `Step`, `test_llm.py`, `pytest`, `_DatabaseCall`, `test_draft_model.py`, `File structure`, `test_rag_api.py`, `agent.py`, `db/repository.py`, `db/repository.py`, `test_steps.py`, `FakeProvider`, `make_ticket`, `test_recovery_regressions.py`, `create_app`, `main.py`, `EmbeddingError`, `test_draft_tools.py`, `catalog.py`, `test_kb_service.py`, `config.py`, `test_workspace_schema.py`, `build_pipeline`, `RAG drafting verification — 2026-10-17`, `test_admin_api.py`, `attachments.py`, `intake/repository.py`, `ConfiguredEmbedder`, `test_workspace_api.py`, `LLMUnavailable`, `test_final_fix_handoff.py`, `httpx`, `intake/contracts.py`, `TurnContext`, `test_cli.py`?**
  _High betweenness centrality (0.092) - this node is a cross-community bridge._
- **Are the 53 inferred relationships involving `Settings` (e.g. with `_command_settings()` and `_run_in_memory()`) actually correct?**
  _`Settings` has 53 INFERRED edges - model-reasoned connections that need verification._
- **What connects `zaincash-support`, `@base-ui/react`, `@fontsource-variable/plus-jakarta-sans` to the rest of the system?**
  _83 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `NewBatchPage.tsx` be split into smaller, more focused modules?**
  _Cohesion score 0.07142857142857142 - nodes in this community are weakly interconnected._
- **Why does `2. Current state` connect `pipeline/contracts.py` to `NewBatchPage.tsx`, `make_ticket`, `build_pipeline`, `Card`, `make_ticket`, `Per-model evaluation (quality, system, cost) — design specification`, `pipeline/graph.py`?**
  _High betweenness centrality (0.091) - this node is a cross-community bridge._
- **Are the 68 inferred relationships involving `Step` (e.g. with `catalog()` and `_check_provider()`) actually correct?**
  _`Step` has 68 INFERRED edges - model-reasoned connections that need verification._

### Low-confidence Hints
_AMBIGUOUS edges — the extractor was unsure. Verify before acting on these._

- **What is the exact relationship between `Fraud Report` and `Plan 1 Live Smoke`?**
  _Edge tagged AMBIGUOUS (relation: conceptually_related_to) - confidence is low._