# Graph Report - zaincash-support  (2026-10-25)

## Corpus Check
- 304 files · ~251,738 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 30 file(s) not represented in the graph (top: (none) 18, .jsonl 4, .css 4)

## Summary
- 3047 nodes · 9408 edges · 155 communities (112 shown, 43 thin omitted)
- Extraction: 89% EXTRACTED · 11% INFERRED · 0% AMBIGUOUS · INFERRED: 1045 edges (avg confidence: 0.93)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `ad6dd61d`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- stage6_draft/model.py
- intake/types.ts
- pytest
- TurnStore
- make_output
- agent.py
- QueuePage.tsx
- Customer conversation intake for ZainCash support
- components-ai-thought-chain.tsx
- IntakeController
- FakeJevRunnable
- test_rag_api.py
- employee-frontend/package.json
- intake/contracts.py
- Support Taxonomy Categories
- ui/package.json
- employee-frontend/src/App.tsx
- users-frontend/package.json
- test_cli.py
- UploadedDocument
- web/package.json
- test_recovery_regressions.py
- compilerOptions
- employee-frontend/components.json
- FakeJevRunnable
- compilerOptions
- web/src/components/theme-provider.tsx
- test_embeddings.py
- Classify and Extract Prompts
- test_draft_tools.py
- Pipeline Design Spec
- Batch Runner
- Drafting Plan Concepts
- test_kb_service.py
- search_knowledge_base
- web/components.json
- Pipeline Spec Rules
- test_workspace_api.py
- ui/components.json
- Settings
- fact
- Vite Config
- Human Review Gate
- compilerOptions
- agent.py
- compilerOptions
- support_test
- Human Flag Tool
- Recent Transactions Tool
- Ticket History Tool
- Lookup Transaction Tool
- Search Transactions Tool
- Submit Draft Tool
- Project Root
- parse_document
- intake/test_repository.py
- intake/repository.py
- IndexJobs
- workspace-ui.tsx
- investigation.py
- test_llm.py
- tasks
- format.ts
- IntakePage.tsx
- test_handoff.py
- PipelineState
- main.py
- PipelineState
- knowledge.py
- load_taxonomy
- test_submission.py
- lib/types.ts
- test-kb/README.md
- pipeline/graph.py
- build_pipeline
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
- pipeline/contracts.py
- devDependencies
- devDependencies
- guardrails.py
- ticket-flow.ts
- SourceEvidence.tsx
- compilerOptions
- قواعد المعرفة العربية للعرض أمام لجنة التحكيم
- pydantic
- dependencies
- InvalidEvidence
- dependencies
- compilerOptions
- EmbeddingError
- IntakePage.test.tsx
- test_final_fix_handoff.py
- ZainCash Support Workspace
- negative/README.md
- scripts
- scripts
- compilerOptions
- ar/card_issue.md
- dependencies
- web/tsconfig.json
- employee-frontend/tsconfig.json
- exports
- PipelineDeps
- scripts
- users-frontend/README.md
- context
- intake/contracts.py
- AttachmentStore
- ar/failed_transfer.md
- ar/general_inquiry.md
- InvalidEvidence
- response_payload
- intake/model.py
- Plan 3 RAG Drafting Implementation Plan
- intake.py
- _DatabaseCall
- KnowledgeService
- ingest.py
- Customer Conversation Intake Implementation Plan
- intake/conftest.py
- KnowledgePage
- intake/api.ts
- ar/login_access.md
- test_dbapi_commit_handoff_arbitrates_cancellation
- ar/refund_request.md
- task8-history-policy.md
- @testing-library/react
- ar/wrong_recipient.md
- collapsible.tsx
- intake/README.md
- canReview
- TicketInput
- employee-frontend/src/components/theme-provider.tsx
- rules.py
- Customer intake chat layout

## God Nodes (most connected - your core abstractions)
1. `Settings` - 100 edges
2. `KnowledgeService` - 79 edges
3. `fact()` - 52 edges
4. `IntakeController` - 51 edges
5. `PipelineState` - 50 edges
6. `context()` - 47 edges
7. `make_output()` - 44 edges
8. `make_ticket()` - 44 edges
9. `draft_state()` - 44 edges
10. `build_pipeline()` - 43 edges

## Surprising Connections (you probably didn't know these)
- `Repeatable local walkthrough` --references--> `Settings`  [INFERRED]
  docs/demo-readiness.md → backend/app/config.py
- `الأصل ونتيجة التحقق` --references--> `parse_document()`  [INFERRED]
  data/test-kb/README.md → backend/app/kb/parse.py
- `Task 6: API/CLI indexing and persisted citation projection` --references--> `KnowledgeService`  [INFERRED]
  docs/superpowers/plans/2026-10-17-plan3-rag-drafting.md → backend/app/kb/service.py
- `Pipeline and CLI` --references--> `NullDrafter`  [INFERRED]
  docs/superpowers/specs/2026-10-17-plan3-rag-drafting-design.md → backend/app/pipeline/stage6_draft/drafting.py
- `7. Draft guardrails and failure outcomes` --references--> `requests_credentials()`  [INFERRED]
  docs/superpowers/specs/2026-10-17-plan3-rag-drafting-design.md → backend/app/pipeline/stage6_draft/guardrails.py

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **Cascade Classification Path** — docs_superpowers_specs_2026_10_07_support_pipeline_design_cascade, docs_superpowers_plans_2026_10_07_plan1_core_pipeline_part2_jev_classifier, docs_superpowers_plans_2026_10_07_plan1_core_pipeline_part2_gemini_classifier, docs_superpowers_plans_2026_10_07_plan1_core_pipeline_part2_cascade_combine, readme_human_approval [EXTRACTED 1.00]
- **Drafting Agent Toolset** — backend_app_pipeline_runner_lookup_transaction, backend_app_pipeline_runner_search_transactions, backend_app_pipeline_runner_get_customer_recent_transactions, backend_app_pipeline_runner_get_customer_ticket_history, backend_app_pipeline_runner_check_service_status, backend_app_pipeline_runner_search_knowledge_base, backend_app_pipeline_runner_flag_for_human, backend_app_pipeline_runner_submit_draft [EXTRACTED 1.00]
- **Ticket Processing Stage Flow** — backend_app_pipeline_runner_prepare, backend_app_pipeline_runner_jev_classify, backend_app_pipeline_runner_gemini_classify, backend_app_pipeline_runner_extract, backend_app_pipeline_runner_lookup, backend_app_pipeline_runner_decide, backend_app_pipeline_runner_draft [EXTRACTED 1.00]

## Communities (155 total, 43 thin omitted)

### Community 1 - "intake/types.ts"
Cohesion: 0.11
Nodes (21): IntakeApi, ControllerState, emptyState(), fileIdentity(), Credentials, CustomerReview, EvidenceRef, Fact (+13 more)

### Community 2 - "pytest"
Cohesion: 0.18
Nodes (37): answer(), call(), Checker, draft_state(), Knowledge, test_sql_defaults_retrieve_real_indexed_evidence(), submit(), pipeline() (+29 more)

### Community 3 - "TurnStore"
Cohesion: 0.16
Nodes (11): OperationClaim, TurnResult, RevisionConflict, sanitize_intake_text(), _jsonable(), TurnStore, repo(), test_recovered_attempt_cannot_publish_stale_output() (+3 more)

### Community 4 - "make_output"
Cohesion: 0.08
Nodes (58): combine(), merge_picks(), requests_credentials(), FakeClassifier, make_output(), make_ticket(), test_both_missing_raises(), test_cost_is_summed() (+50 more)

### Community 5 - "agent.py"
Cohesion: 0.07
Nodes (21): DraftAlreadySubmitted, DraftSubmission, DraftToolLimit, _bounded(), visit(), build_tools(), flag(), guarded() (+13 more)

### Community 6 - "QueuePage.tsx"
Cohesion: 0.18
Nodes (49): EmptyState(), ErrorState(), LoadingState(), Metric(), PageHeader(), PriorityBadge(), StatusBadge(), Button() (+41 more)

### Community 7 - "Customer conversation intake for ZainCash support"
Cohesion: 0.06
Nodes (32): 10. Verification and acceptance criteria, 11. Delivery and review, 1. Outcome and agreed requirements, 2. Current implementation and integration points, 3. Approach and boundaries, 4. Conversation state and turn flow, 5. Facts, evidence, and readiness, 6. Language and screenshot behavior (+24 more)

### Community 8 - "components-ai-thought-chain.tsx"
Cohesion: 0.14
Nodes (15): Status, StatusIcon(), statusStyles, StepContext, StepContextType, ThoughtChain(), ThoughtChainContent(), ThoughtChainItem() (+7 more)

### Community 9 - "IntakeController"
Cohesion: 0.19
Nodes (5): IntakeController, isConflict(), isOffline(), safeMessage(), Language

### Community 10 - "FakeJevRunnable"
Cohesion: 0.12
Nodes (18): CredentialCheck, DegradedCredentialChecker, _finite_nonnegative(), _get(), JevCredentialChecker, ResponseRunnable, test_bad_usage_cannot_poison_cost(), test_cancellation_propagates_with_cost_for_outer_timeout_owner() (+10 more)

### Community 11 - "test_rag_api.py"
Cohesion: 0.14
Nodes (18): create_app(), client(), evidence_client(), test_actual_guardrail_failure_is_separate_from_reply(), test_concurrent_index_requests_share_active_work(), test_disabled_or_missing_provider_stores_without_indexing(), test_explicit_retry_tags_search_and_chunk_pagination(), test_health_distinguishes_failed_from_empty() (+10 more)

### Community 12 - "employee-frontend/package.json"
Cohesion: 0.06
Nodes (31): @base-ui/react, class-variance-authority, cn, eslint, @eslint/js, eslint-plugin-react-hooks, eslint-plugin-react-refresh, @fontsource/tajawal (+23 more)

### Community 14 - "intake/contracts.py"
Cohesion: 0.14
Nodes (10): Attachment, _aware(), IntakeModel, Message, ModelCall, Readiness, initial_state(), grounded_analysis() (+2 more)

### Community 15 - "Support Taxonomy Categories"
Cohesion: 0.21
Nodes (22): lookup, Account KYC, Account & Security, Agent Dispute, Agent Network, App Bug, Bill Payment, Card Issue (+14 more)

### Community 16 - "ui/package.json"
Cohesion: 0.07
Nodes (29): @turbo/gen, zod, @base-ui/react, class-variance-authority, cn, eslint, @eslint/js, eslint-plugin-react-hooks (+21 more)

### Community 17 - "employee-frontend/src/App.tsx"
Cohesion: 0.10
Nodes (26): App(), EvaluationPage, InsightsPage, KnowledgePage, NewBatchPage, QueuePage, RunDetailPage, RunsPage (+18 more)

### Community 18 - "users-frontend/package.json"
Cohesion: 0.09
Nodes (22): turbo, devDependencies, prettier, prettier-plugin-tailwindcss, turbo, typescript, engines, node (+14 more)

### Community 19 - "test_cli.py"
Cohesion: 0.18
Nodes (9): test_config_error_exits_2(), boom(), test_ingest_directory_is_deterministic_and_duplicate_is_free(), test_ingest_disabled_configuration_never_calls_provider(), test_ingest_failure_exit_and_retry_stored(), test_ingest_invalid_source_does_not_stop_other_files(), test_ingest_limits_batch_without_partial_side_effects(), test_retry_stored_indexes_old_uploads_without_recovering_other_process_jobs() (+1 more)

### Community 20 - "UploadedDocument"
Cohesion: 0.17
Nodes (14): UploadedDocument, document_filename(), document_view(), DocumentValidationError, store_document(), KnowledgeDocumentIndex, ingest_one(), ingest_paths() (+6 more)

### Community 21 - "web/package.json"
Cohesion: 0.08
Nodes (25): jsdom, @testing-library/user-event, @workspace/ui, eslint, @eslint/js, eslint-plugin-react-hooks, eslint-plugin-react-refresh, globals (+17 more)

### Community 22 - "test_recovery_regressions.py"
Cohesion: 0.35
Nodes (10): command(), create(), test_actual_app_restart_reconciles_failed_placeholder(), test_failed_review_retry_cannot_reopen_submitted_session(), test_original_payload_identity_survives_sanitization(), test_publication_failure_is_retryable_without_restart(), fail_once(), test_receipt_reference_is_preserved() (+2 more)

### Community 23 - "compilerOptions"
Cohesion: 0.08
Nodes (23): compilerOptions, allowArbitraryExtensions, allowImportingTsExtensions, erasableSyntaxOnly, jsx, lib, module, moduleDetection (+15 more)

### Community 24 - "employee-frontend/components.json"
Cohesion: 0.09
Nodes (21): aliases, components, hooks, lib, ui, utils, iconLibrary, menuAccent (+13 more)

### Community 25 - "FakeJevRunnable"
Cohesion: 0.32
Nodes (10): FakeJevRunnable, _criteria(), _run(), test_low_top_probability_is_uncertain(), test_one_main_call_with_all_questions(), test_order_check_uses_reversed_options(), test_order_disagreement_is_uncertain(), test_priority_level_maps_to_p_label() (+2 more)

### Community 26 - "compilerOptions"
Cohesion: 0.09
Nodes (22): compilerOptions, allowArbitraryExtensions, allowImportingTsExtensions, erasableSyntaxOnly, jsx, lib, module, moduleDetection (+14 more)

### Community 27 - "web/src/components/theme-provider.tsx"
Cohesion: 0.15
Nodes (13): App(), controller, disableTransitionsTemporarily(), getSystemTheme(), isEditableTarget(), isTheme(), ResolvedTheme, Theme (+5 more)

### Community 28 - "test_embeddings.py"
Cohesion: 0.17
Nodes (18): OpenRouterEmbedder, settings(), test_33_inputs_are_batched_and_each_batch_maps_its_own_indexes(), test_billed_batch_cost_survives_cancellation_without_cross_call_leakage(), test_cancellation_propagates_to_the_callers_deadline(), test_empty_input_returns_empty_batch_without_a_request(), unexpected_request(), test_invalid_rag_settings_are_rejected() (+10 more)

### Community 29 - "Classify and Extract Prompts"
Cohesion: 0.31
Nodes (9): extract, gemini_classify, Pipeline Graph Orchestration, jev_classify, prepare, Gemini Classify Prompt v1, Gemini Extract Prompt v1, GeminiClassifier (+1 more)

### Community 30 - "test_draft_tools.py"
Cohesion: 0.12
Nodes (30): IncidentRow, TransactionRow, api(), ErrorEmbedder, settings(), test_all_eight_tools_and_seven_parallel_calls_execute_only_six(), test_context_copies_input_and_rejects_raising_hard_call_limit(), test_database_faults_remain_distinct_and_record_paid_search_cost() (+22 more)

### Community 31 - "Pipeline Design Spec"
Cohesion: 0.25
Nodes (7): pgvector Postgres Service, pgdata Volume, Support Pipeline Design, Gemini 3.8 Flash, Jev, OpenRouter, ZainCash Support Pipeline

### Community 32 - "Batch Runner"
Cohesion: 0.33
Nodes (6): Plan 1 Part 2, Batch Runner, NullDrafter, Plan 1 Core Pipeline, Live Batch API, NullDrafter

### Community 33 - "Drafting Plan Concepts"
Cohesion: 0.25
Nodes (5): check_service_status, decide, draft, Five-Plan Roadmap, Weekly Pattern Report

### Community 34 - "test_kb_service.py"
Cohesion: 0.11
Nodes (30): FakeEmbedder, GatedEmbedder, LateEmbedder, PaidEmbedder, count_chunks(), settings(), test_category_filters_include_general_policies_and_validate_tags(), test_claim_locks_source_even_before_index_row_exists() (+22 more)

### Community 36 - "web/components.json"
Cohesion: 0.10
Nodes (19): aliases, components, hooks, lib, ui, utils, iconLibrary, menuAccent (+11 more)

### Community 38 - "test_workspace_api.py"
Cohesion: 0.23
Nodes (7): start_run(), test_batch_and_queue_expose_real_results(), test_batch_failure_is_isolated_and_conflicting_ids_rejected(), test_openrouter_credentials_enable_api_modes_without_exposing_keys(), test_progress_counts_only_durable_results_after_save_failure(), fail_one_save(), test_review_requires_text_and_rejects_stale_updates()

### Community 39 - "ui/components.json"
Cohesion: 0.10
Nodes (19): aliases, components, hooks, lib, ui, utils, iconLibrary, menuAccent (+11 more)

### Community 40 - "Settings"
Cohesion: 0.15
Nodes (7): Settings, test_defaults(), test_drafting_configuration_cannot_bypass_hard_limits(), test_drafting_limits_load_from_environment(), test_env_overrides(), test_legacy_gemini_model_names_are_qualified_for_openrouter(), test_openrouter_key_is_loaded_from_environment()

### Community 41 - "fact"
Cohesion: 0.16
Nodes (40): Analysis, EvidenceRef, Fact, merge_analysis(), remove_attachment_evidence(), context(), fact(), image_evidence() (+32 more)

### Community 43 - "Human Review Gate"
Cohesion: 0.25
Nodes (4): support CLI, Support Workspace UI Plan, Review API, Workspace UI Verification

### Community 44 - "compilerOptions"
Cohesion: 0.12
Nodes (16): compilerOptions, allowImportingTsExtensions, erasableSyntaxOnly, lib, module, moduleDetection, noEmit, noFallthroughCasesInSwitch (+8 more)

### Community 46 - "agent.py"
Cohesion: 0.06
Nodes (20): KnowledgeExecutionError, DraftResult, build_pipeline(), make_gemini_llm(), make_jev_client(), _error_cost(), _Execution, _ModelUsage (+12 more)

### Community 47 - "compilerOptions"
Cohesion: 0.12
Nodes (16): compilerOptions, allowImportingTsExtensions, erasableSyntaxOnly, lib, module, moduleDetection, noEmit, noFallthroughCasesInSwitch (+8 more)

### Community 48 - "support_test"
Cohesion: 0.11
Nodes (19): index_deadlines(), support_test(), expire_during_embedding(), Evidence by layer, Known limitations and remaining work, Repeatable local walkthrough, Synthetic demo readiness, Commands and automated verification — historical Task 8 (+11 more)

### Community 57 - "parse_document"
Cohesion: 0.11
Nodes (29): TextChunk, _append_chunks(), _check_extracted_size(), DocumentParseError, parse_document(), _parse_pdf(), make_pdf(), test_arabic_text_and_bom_are_preserved() (+21 more)

### Community 58 - "intake/test_repository.py"
Cohesion: 0.18
Nodes (9): repo(), test_blank_intake_model_is_rejected(), test_contracts_reject_extra_keys(), test_datetimes_must_be_timezone_aware(), test_message_sequence_is_unique(), test_non_positive_image_limit_is_rejected(), test_relative_upload_directory_is_rooted_in_the_repository(), test_repeated_init_db_keeps_existing_tickets() (+1 more)

### Community 59 - "intake/repository.py"
Cohesion: 0.12
Nodes (29): CustomerReview, Receipt, ReviewSnapshot, IntakeAttachmentRow, IntakeMessageRow, IntakeOperationRow, IntakeSessionRow, IntakeSubmissionRow (+21 more)

### Community 61 - "workspace-ui.tsx"
Cohesion: 0.07
Nodes (37): ConfirmDialog(), FilterSelect(), Badge(), badgeVariants, buttonVariants, Dialog(), DialogContent(), DialogDescription() (+29 more)

### Community 62 - "investigation.py"
Cohesion: 0.09
Nodes (29): TxnRecord, _as_date(), _iqd_amount(), match_transaction(), parse_dt(), TransactionRepo, txn_from_dict(), DraftToolInputError (+21 more)

### Community 63 - "test_llm.py"
Cohesion: 0.13
Nodes (10): GeminiStructuredLLM, _llm(), _S, test_draft_model_uses_millisecond_timeout_and_disables_sdk_retries(), test_openrouter_reported_cost_takes_precedence_over_token_estimate(), test_openrouter_retry_budget_is_bounded(), test_openrouter_structured_samples_use_configured_key_and_validate_output(), send() (+2 more)

### Community 64 - "tasks"
Cohesion: 0.12
Nodes (16): dependsOn, inputs, outputs, cache, persistent, dependsOn, dependsOn, $schema (+8 more)

### Community 65 - "format.ts"
Cohesion: 0.08
Nodes (36): Ticket Flow Charts Implementation Plan, 1. Outcome, 2. Scope, 5. Language, 6. How a result becomes the charts, 7. Sentences, 8. Tests, 9. Files (+28 more)

### Community 66 - "IntakePage.tsx"
Cohesion: 0.13
Nodes (21): Global Constraints, Intake Chat UI Implementation Plan, Task 1: Put the summary and receipt in the thread, Task 2: Put screenshots inside the composer, Task 3: Apply the workspace chat styles, Task 4: Check the page in the browser, 4. Components, ChatTranscript() (+13 more)

### Community 67 - "test_handoff.py"
Cohesion: 0.12
Nodes (14): dispatch_intake(), complete_conversation(), _dated(), _message(), _opening(), _png(), _review(), test_review_to_employee_handoff() (+6 more)

### Community 68 - "PipelineState"
Cohesion: 0.11
Nodes (18): 10. Remaining demo roadmap, 1. Intent and acceptance criteria, 3. Provider and configuration, 4. Knowledge ingestion and persistence, 5. Retrieval and evidence, 6. Bounded investigation agent, 7. Draft guardrails and failure outcomes, 8. Pipeline, API, CLI and UI integration (+10 more)

### Community 69 - "main.py"
Cohesion: 0.06
Nodes (33): get_session(), _safe_dispatch(), get_result(), list_results(), read_intake_attachment(), review_result(), get_run(), list_runs() (+25 more)

### Community 70 - "PipelineState"
Cohesion: 0.23
Nodes (4): _Nodes, Global Constraints, 3. What the employee sees, 4. Which step is open

### Community 71 - "knowledge.py"
Cohesion: 0.17
Nodes (11): delete_document(), download_document(), index_document(), list_chunks(), list_documents(), _require_provider(), search_knowledge(), upload_document() (+3 more)

### Community 72 - "load_taxonomy"
Cohesion: 0.13
Nodes (9): load_taxonomy(), most_urgent(), priority_rank(), TaxonomyError, tax(), taxonomy(), taxonomy(), test_priority_helpers() (+1 more)

### Community 73 - "test_submission.py"
Cohesion: 0.32
Nodes (4): _payload(), test_concurrent_submit_dispatches_once(), test_second_request_id_reuses_the_approved_review(), test_submission_replay_creates_one_ticket()

### Community 74 - "lib/types.ts"
Cohesion: 0.10
Nodes (30): ingest(), Artifacts, servers and remaining concerns, acceptIndexRequest(), canRequestIndex(), PendingIndexes, persistPendingIndexes(), pollKnowledge(), refresh() (+22 more)

### Community 75 - "test-kb/README.md"
Cohesion: 0.13
Nodes (7): Fictional RAG walkthrough inputs, توثيق الحساب — سياسة خيالية للعرض التجريبي, نزاع مع وكيل — سياسة خيالية للعرض التجريبي, أعطال التطبيق — سياسة خيالية للعرض التجريبي, دفع الفواتير — سياسة خيالية للعرض التجريبي, تصعيد شبهة الاحتيال — سياسة خيالية للعرض التجريبي, الطلبات غير الواضحة وخارج النطاق — سياسة خيالية للعرض التجريبي

### Community 76 - "pipeline/graph.py"
Cohesion: 0.07
Nodes (41): _command_settings(), ingest_kb_cmd(), init_db_cmd(), Mode, run_batch_cmd(), _run_in_memory(), _run_with_db(), seed_db_cmd() (+33 more)

### Community 77 - "build_pipeline"
Cohesion: 0.11
Nodes (17): Sample, ConfigError, model_ids(), GeminiAnalysis, FakeStructuredLLM, ScriptedChat, _settings(), test_all_modes_use_credential_checker_independently_of_classifier() (+9 more)

### Community 79 - "devDependencies"
Cohesion: 0.12
Nodes (16): devDependencies, eslint, @eslint/js, eslint-plugin-react-hooks, eslint-plugin-react-refresh, globals, prettier, prettier-plugin-tailwindcss (+8 more)

### Community 80 - "judge-demo.ar.md"
Cohesion: 0.14
Nodes (13): أعطال التطبيق — سياسة خيالية للعرض التجريبي, استرجاع مبلغ شراء — سياسة خيالية للعرض التجريبي, استعادة الدخول — سياسة خيالية للعرض التجريبي, الاستفسار الآمن من الدعم — سياسة خيالية للعرض التجريبي, الاستفسار المؤقت للدعم في المهمة ٨ — سياسة خيالية للعرض التجريبي, التحويل المعلّق — سياسة خيالية للعرض التجريبي, التحويل لمستلم بالخطأ — سياسة خيالية للعرض التجريبي, الطلبات غير الواضحة وخارج النطاق — سياسة خيالية للعرض التجريبي (+5 more)

### Community 93 - "pipeline/contracts.py"
Cohesion: 0.08
Nodes (37): LLMUnavailable, StructuredLLM, Candidate, Candidates, ClassificationResult, ClassifierOutput, ExtractedField, FieldPick (+29 more)

### Community 94 - "devDependencies"
Cohesion: 0.11
Nodes (19): devDependencies, eslint, @eslint/js, eslint-plugin-react-hooks, eslint-plugin-react-refresh, globals, jsdom, @tailwindcss/vite (+11 more)

### Community 95 - "devDependencies"
Cohesion: 0.14
Nodes (14): devDependencies, eslint, @eslint/js, eslint-plugin-react-hooks, eslint-plugin-react-refresh, globals, tailwindcss, @tailwindcss/vite (+6 more)

### Community 96 - "guardrails.py"
Cohesion: 0.06
Nodes (55): find_candidates(), normalize_phone(), _overlaps(), parse_amount(), resolve_date(), _safe_date(), detect_arabizi(), fold_arabic() (+47 more)

### Community 97 - "ticket-flow.ts"
Cohesion: 0.09
Nodes (48): Task 1: Sentence catalog, Task 2: Which step is open, Task 3: Received, produced, and drafting events, Task 4: Mermaid source, Task 5: Draw the charts on the ticket page, buildTicketFlow(), AR, channelName() (+40 more)

### Community 98 - "SourceEvidence.tsx"
Cohesion: 0.25
Nodes (12): Confidence(), intakeFixture, factValue(), IntakeEvidence(), Screenshot(), highlightedText(), SourceEvidence(), channelLabel() (+4 more)

### Community 99 - "compilerOptions"
Cohesion: 0.14
Nodes (13): compilerOptions, jsx, lib, module, moduleResolution, noEmit, paths, skipLibCheck (+5 more)

### Community 100 - "قواعد المعرفة العربية للعرض أمام لجنة التحكيم"
Cohesion: 0.33
Nodes (6): الأصل ونتيجة التحقق, توليد مسودة ومراجعتها, خريطة الملفات وأسئلة العرض, خطوات الرفع والفهرسة والبحث أمام اللجنة, قواعد المعرفة العربية للعرض أمام لجنة التحكيم, ماذا أرفع؟

### Community 101 - "pydantic"
Cohesion: 0.27
Nodes (5): CitationSource, _Draft, _Guardrail, _TraceModel, _validated()

### Community 102 - "dependencies"
Cohesion: 0.12
Nodes (17): dependencies, @base-ui/react, class-variance-authority, cn, @fontsource/tajawal, @fontsource-variable/plus-jakarta-sans, lucide-react, mermaid (+9 more)

### Community 103 - "InvalidEvidence"
Cohesion: 0.17
Nodes (15): canonical_digits(), normalize_reported_date(), InvalidEvidence, _apply(), _check_reference(), _compact(), checked_update(), _newer_correction() (+7 more)

### Community 104 - "dependencies"
Cohesion: 0.15
Nodes (13): dependencies, @base-ui/react, class-variance-authority, cn, @fontsource/tajawal, @fontsource-variable/plus-jakarta-sans, @hugeicons/core-free-icons, @hugeicons/react (+5 more)

### Community 105 - "compilerOptions"
Cohesion: 0.17
Nodes (11): compilerOptions, jsx, lib, module, moduleResolution, outDir, skipLibCheck, strict (+3 more)

### Community 106 - "EmbeddingError"
Cohesion: 0.15
Nodes (9): EmbeddingBatch, EmbeddingError, _nonnegative_number(), _ordered_vectors(), _response_cost(), Embeddings, test_lock_serializes_operations_and_submit_waits_for_inflight_search(), embed() (+1 more)

### Community 107 - "IntakePage.test.tsx"
Cohesion: 0.13
Nodes (17): HTTP contract (implemented in Tasks 4–5), Task 6: Customer API client and resumable UI state, Task 7: Bilingual customer chat, screenshots and reviewed submission, copy(), emptySession(), fakeApi(), review, attachment (+9 more)

### Community 108 - "test_final_fix_handoff.py"
Cohesion: 0.12
Nodes (23): Passage, process_batch(), script(), assert_completed_evidence(), faulty_knowledge(), read(), outer_deadlines(), PaidEmbeddings (+15 more)

### Community 109 - "ZainCash Support Workspace"
Cohesion: 0.22
Nodes (9): Current capability boundaries, Data source, Modular file map, Open the right project, Run locally, shadcn conventions, Verification, Workflow (+1 more)

### Community 111 - "scripts"
Cohesion: 0.25
Nodes (8): scripts, build, dev, format, lint, preview, test, typecheck

### Community 112 - "scripts"
Cohesion: 0.25
Nodes (8): scripts, build, dev, format, lint, preview, test, typecheck

### Community 113 - "compilerOptions"
Cohesion: 0.29
Nodes (6): compilerOptions, module, moduleResolution, skipLibCheck, strict, target

### Community 115 - "dependencies"
Cohesion: 0.33
Nodes (6): dependencies, @hugeicons/core-free-icons, @hugeicons/react, react, react-dom, @workspace/ui

### Community 116 - "web/tsconfig.json"
Cohesion: 0.33
Nodes (5): compilerOptions, paths, files, @workspace/ui/*, references

### Community 117 - "employee-frontend/tsconfig.json"
Cohesion: 0.40
Nodes (4): compilerOptions, paths, files, references

### Community 118 - "exports"
Cohesion: 0.40
Nodes (5): exports, ./components/*, ./globals.css, ./hooks/*, ./lib/*

### Community 119 - "PipelineDeps"
Cohesion: 0.15
Nodes (16): make_draft_model(), build_graph(), PipelineDeps, InMemoryTransactionRepo, pipeline(), test_run_batch_no_db_writes_summary_and_out(), fake_build(), response_payload() (+8 more)

### Community 120 - "scripts"
Cohesion: 0.50
Nodes (4): scripts, format, lint, typecheck

### Community 122 - "context"
Cohesion: 0.20
Nodes (20): IntakeState, Question, _asked_already(), asks_for_secret(), assess_readiness(), _can_ask(), canonical_category(), choose_question() (+12 more)

### Community 123 - "intake/contracts.py"
Cohesion: 0.22
Nodes (5): QuestionRecord, TurnContext, IntakeGraph, _invitation(), Shared contracts (implement in Task 1; extend only through explicit edits here)

### Community 124 - "AttachmentStore"
Cohesion: 0.09
Nodes (25): AttachmentStore, _display_name(), Credentials, SessionView, ImageRejected, NotOwned, IntakeRepository, IntakeService (+17 more)

### Community 127 - "InvalidEvidence"
Cohesion: 0.29
Nodes (15): ReviewText, build_review(), _compact(), _render_value(), _ticket_text(), _tokens(), validate_review_numbers(), message() (+7 more)

### Community 128 - "response_payload"
Cohesion: 0.22
Nodes (16): embedder_for(), item(), response_payload(), respond(), respond(), test_billed_cost_survives_cancellation_during_client_close(), test_billed_response_cost_is_retained_when_its_vectors_are_invalid(), test_cost_uses_one_reported_value_or_configured_token_estimate() (+8 more)

### Community 129 - "intake/model.py"
Cohesion: 0.11
Nodes (26): ImageInput, ModelUnavailable, _analysis_prompt(), _bounded_context(), _guard_size(), ModelBudget, OpenRouterIntakeModel, validate() (+18 more)

### Community 130 - "Plan 3 RAG Drafting Implementation Plan"
Cohesion: 0.20
Nodes (10): Completion and review record — 2026-10-17, Execution handoff, File map and shared interfaces, Global Constraints, Plan 3 RAG Drafting Implementation Plan, Plan self-review, Review Focus, Task 6: API/CLI indexing and persisted citation projection (+2 more)

### Community 131 - "intake.py"
Cohesion: 0.17
Nodes (19): create_session(), _credentials(), _dump(), get_session(), post_message(), read_attachment(), remove_attachment(), request_review() (+11 more)

### Community 132 - "_DatabaseCall"
Cohesion: 0.13
Nodes (5): _abandoned(), _check_deadline(), _consume(), _DatabaseCall, _error_cost()

### Community 133 - "KnowledgeService"
Cohesion: 0.11
Nodes (9): Embedder, SearchResult, KnowledgeChunk, _Claim, IndexAttemptLostError, KnowledgeError, KnowledgeService, test_pdf_page_metadata_and_repeated_text_chunk_identity() (+1 more)

### Community 134 - "ingest.py"
Cohesion: 0.16
Nodes (8): load_jsonl(), load_tickets(), _rows(), test_csv_with_bom_and_missing_columns(), test_duplicate_external_ids_keep_first(), test_json_object_without_ids(), test_jsonl_fixture_loads(), test_unsupported_format()

### Community 135 - "Customer Conversation Intake Implementation Plan"
Cohesion: 0.20
Nodes (8): Completion audit — 2026-10-18, Customer Conversation Intake Implementation Plan, Execution conventions and repository baseline, File map and dependency order, Global Constraints, Plan review and execution handoff, Review Focus, Spec coverage and acceptance map

### Community 136 - "intake/conftest.py"
Cohesion: 0.16
Nodes (13): init_db(), make_engine(), make_sessionmaker(), reset_db(), upgrade_workspace_schema(), lifespan(), intake_client(), intake_db() (+5 more)

### Community 137 - "KnowledgePage"
Cohesion: 0.60
Nodes (5): beginMutation(), deleteDocument(), finishMutation(), indexDocument(), upload()

### Community 138 - "intake/api.ts"
Cohesion: 0.15
Nodes (13): createIntakeApi(), IntakeRequestError, isRecord(), parseJson(), parseReceipt(), parseSession(), readError(), stringList() (+5 more)

### Community 140 - "test_dbapi_commit_handoff_arbitrates_cancellation"
Cohesion: 0.15
Nodes (8): test_db_deadline_includes_pool_and_checkout_without_late_claim(), checked_in(), test_db_deadline_search_cancellation_is_nonblocking_and_retains_cost(), test_dbapi_commit_handoff_arbitrates_cancellation(), gate(), gate_before_dbapi(), gate_inside_dbapi(), test_index_deadline_or_cancellation_preserves_real_adapter_partial_cost()

### Community 151 - "canReview"
Cohesion: 0.50
Nodes (3): Task 8: Employee evidence panel and processing state, canReview(), REVIEWABLE

### Community 153 - "TicketInput"
Cohesion: 0.31
Nodes (3): KnowledgeIndexInput, KnowledgeSearchInput, TicketInput

### Community 156 - "employee-frontend/src/components/theme-provider.tsx"
Cohesion: 0.21
Nodes (11): disableTransitionsTemporarily(), getSystemTheme(), isEditableTarget(), isTheme(), ResolvedTheme, Theme, THEME_VALUES, ThemeProvider() (+3 more)

### Community 158 - "rules.py"
Cohesion: 0.19
Nodes (18): Decision, LookupResult, decide(), empty_ticket_decision(), merge_reasons(), note_for(), _unique(), Category (+10 more)

### Community 161 - "Customer intake chat layout"
Cohesion: 0.33
Nodes (5): 1. Outcome, 2. Scope, 3. Layout, 5. Checks, Customer intake chat layout

## Ambiguous Edges - Review These
- `Fraud Report` → `Plan 1 Live Smoke`  [AMBIGUOUS]
  README.md · relation: conceptually_related_to

## Knowledge Gaps
- **91 isolated node(s):** `zaincash-support`, `@base-ui/react`, `@fontsource-variable/plus-jakarta-sans`, `@fontsource/tajawal`, `@tailwindcss/vite` (+86 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 1010 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **43 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `HTTP contract (implemented in Tasks 4–5)` connect `IntakePage.test.tsx` to `guardrails.py`, `intake/model.py`, `TurnStore`, `test_handoff.py`, `main.py`, `Customer Conversation Intake Implementation Plan`, `canReview`, `intake/repository.py`?**
  _High betweenness centrality (0.103) - this node is a cross-community bridge._
- **Are the 33 inferred relationships involving `Settings` (e.g. with `_command_settings()` and `_run_in_memory()`) actually correct?**
  _`Settings` has 33 INFERRED edges - model-reasoned connections that need verification._
- **What connects `zaincash-support`, `@base-ui/react`, `@fontsource-variable/plus-jakarta-sans` to the rest of the system?**
  _91 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `intake/types.ts` be split into smaller, more focused modules?**
  _Cohesion score 0.11491935483870967 - nodes in this community are weakly interconnected._
- **Why does `Task 3: Received, produced, and drafting events` connect `ticket-flow.ts` to `pytest`, `SourceEvidence.tsx`, `PipelineState`, `QueuePage.tsx`?**
  _High betweenness centrality (0.083) - this node is a cross-community bridge._
- **Are the 24 inferred relationships involving `KnowledgeService` (e.g. with `Settings` and `UploadedDocument`) actually correct?**
  _`KnowledgeService` has 24 INFERRED edges - model-reasoned connections that need verification._

### Low-confidence Hints
_AMBIGUOUS edges — the extractor was unsure. Verify before acting on these._

- **What is the exact relationship between `Fraud Report` and `Plan 1 Live Smoke`?**
  _Edge tagged AMBIGUOUS (relation: conceptually_related_to) - confidence is low._