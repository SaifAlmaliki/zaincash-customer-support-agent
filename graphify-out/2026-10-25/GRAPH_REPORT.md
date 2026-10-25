# Graph Report - zaincash-support  (2026-10-25)

## Corpus Check
- 300 files · ~249,667 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 30 file(s) not represented in the graph (top: (none) 18, .jsonl 4, .css 4)

## Summary
- 3022 nodes · 9347 edges · 154 communities (118 shown, 36 thin omitted)
- Extraction: 89% EXTRACTED · 11% INFERRED · 0% AMBIGUOUS · INFERRED: 1045 edges (avg confidence: 0.93)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `548cdd87`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- LLMUnavailable
- intake/types.ts
- pytest
- TurnStore
- make_ticket
- agent.py
- QueuePage.tsx
- Customer conversation intake for ZainCash support
- workspace-ui.tsx
- IntakeController
- FakeJevRunnable
- test_rag_api.py
- employee-frontend/package.json
- make_output
- Support Taxonomy Categories
- ui/package.json
- employee-frontend/src/App.tsx
- users-frontend/package.json
- db/models.py
- knowledge.py
- web/package.json
- main.py
- compilerOptions
- employee-frontend/components.json
- test_workspace_api.py
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
- pipeline/graph.py
- ui/components.json
- test_submission.py
- fact
- Vite Config
- Human Review Gate
- compilerOptions
- RagDrafter
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
- investigation.py
- intake/repository.py
- guardrails.py
- NewBatchPage.tsx
- lookup.py
- Settings
- tasks
- format.ts
- IntakePage.tsx
- Analysis
- PipelineState
- main.py
- PipelineState
- cli.py
- load_taxonomy
- IntakeRepository
- lib/types.ts
- test-kb/README.md
- agent.py
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
- UploadedDocument
- ticket-flow.ts
- useCopy
- compilerOptions
- قواعد المعرفة العربية للعرض أمام لجنة التحكيم
- pydantic
- dependencies
- InvalidEvidence
- dependencies
- compilerOptions
- EmbeddingError
- controller.test.ts
- test_final_fix_handoff.py
- ZainCash Support Workspace
- negative/README.md
- scripts
- scripts
- compilerOptions
- Customer intake verification — 2026-10-18
- dependencies
- web/tsconfig.json
- employee-frontend/tsconfig.json
- exports
- test_draft_model.py
- scripts
- users-frontend/README.md
- context
- intake/helpers.py
- attachments.py
- test_cli.py
- test_db_deadline_cancelled_publication_cannot_commit_late
- InvalidEvidence
- response_payload
- intake/model.py
- Plan 3 RAG Drafting Implementation Plan
- intake.py
- _DatabaseCall
- Embedder
- test_recovery_regressions.py
- Customer Conversation Intake Implementation Plan
- intake/conftest.py
- KnowledgePage
- intake/api.ts
- index_deadlines
- test_dbapi_commit_handoff_arbitrates_cancellation
- @testing-library/react
- kb/service.py
- intake/README.md
- canReview
- IntakePage.test.tsx
- employee-frontend/src/components/theme-provider.tsx
- rules.py
- ar/fraud_report.md
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

## Communities (154 total, 36 thin omitted)

### Community 0 - "LLMUnavailable"
Cohesion: 0.24
Nodes (11): LLMUnavailable, combine(), merge_picks(), test_both_missing_raises(), test_cost_is_summed(), test_degraded_when_jev_missing(), test_disagreement_when_jev_was_partly_confident(), test_gemini_low_confidence() (+3 more)

### Community 1 - "intake/types.ts"
Cohesion: 0.11
Nodes (23): IntakeApi, ControllerState, emptyState(), fileIdentity(), factText(), Attachment, Credentials, CustomerReview (+15 more)

### Community 2 - "pytest"
Cohesion: 0.19
Nodes (37): test_contracts_reject_extra_keys(), test_datetimes_must_be_timezone_aware(), answer(), call(), Checker, draft_state(), Knowledge, script() (+29 more)

### Community 3 - "TurnStore"
Cohesion: 0.18
Nodes (10): OperationClaim, TurnResult, RevisionConflict, sanitize_intake_text(), TurnStore, repo(), test_recovered_attempt_cannot_publish_stale_output(), test_review_publication_revision_matches_the_session() (+2 more)

### Community 4 - "make_ticket"
Cohesion: 0.14
Nodes (28): check_draft(), requests_credentials(), make_ticket(), check(), state(), test_aggregation_is_deduplicated_and_has_no_state_side_effects(), test_amount_occurrences_keep_their_own_currency_and_sign(), test_avoid_sharing_warning_does_not_excuse_a_later_request() (+20 more)

### Community 5 - "agent.py"
Cohesion: 0.07
Nodes (20): DraftAlreadySubmitted, DraftSubmission, _bounded(), visit(), build_tools(), flag(), guarded(), invoke() (+12 more)

### Community 6 - "QueuePage.tsx"
Cohesion: 0.16
Nodes (46): EmptyState(), ErrorState(), LoadingState(), Metric(), PageHeader(), PriorityBadge(), StatusBadge(), Button() (+38 more)

### Community 7 - "Customer conversation intake for ZainCash support"
Cohesion: 0.06
Nodes (32): 10. Verification and acceptance criteria, 11. Delivery and review, 1. Outcome and agreed requirements, 2. Current implementation and integration points, 3. Approach and boundaries, 4. Conversation state and turn flow, 5. Facts, evidence, and readiness, 6. Language and screenshot behavior (+24 more)

### Community 8 - "workspace-ui.tsx"
Cohesion: 0.11
Nodes (17): ConfirmDialog(), FilterSelect(), buttonVariants, Dialog(), DialogContent(), DialogDescription(), DialogFooter(), DialogHeader() (+9 more)

### Community 9 - "IntakeController"
Cohesion: 0.20
Nodes (5): IntakeController, isConflict(), isOffline(), safeMessage(), Language

### Community 10 - "FakeJevRunnable"
Cohesion: 0.09
Nodes (28): CredentialCheck, DegradedCredentialChecker, _finite_nonnegative(), _get(), JevCredentialChecker, FakeJevRunnable, ResponseRunnable, test_bad_usage_cannot_poison_cost() (+20 more)

### Community 11 - "test_rag_api.py"
Cohesion: 0.14
Nodes (19): client(), evidence_client(), pipeline(), submit(), test_actual_guardrail_failure_is_separate_from_reply(), test_concurrent_index_requests_share_active_work(), test_disabled_or_missing_provider_stores_without_indexing(), test_explicit_retry_tags_search_and_chunk_pagination() (+11 more)

### Community 12 - "employee-frontend/package.json"
Cohesion: 0.06
Nodes (31): @base-ui/react, class-variance-authority, cn, eslint, @eslint/js, eslint-plugin-react-hooks, eslint-plugin-react-refresh, @fontsource/tajawal (+23 more)

### Community 14 - "make_output"
Cohesion: 0.24
Nodes (19): FakeClassifier, make_output(), _deps(), _run(), test_cascade_confident_jev_skips_gemini(), test_cascade_degrades_when_jev_fails(), test_cascade_uncertain_jev_goes_to_gemini(), test_concurrency_is_limited() (+11 more)

### Community 15 - "Support Taxonomy Categories"
Cohesion: 0.21
Nodes (22): lookup, Account KYC, Account & Security, Agent Dispute, Agent Network, App Bug, Bill Payment, Card Issue (+14 more)

### Community 16 - "ui/package.json"
Cohesion: 0.07
Nodes (29): @turbo/gen, zod, @base-ui/react, class-variance-authority, cn, eslint, @eslint/js, eslint-plugin-react-hooks (+21 more)

### Community 17 - "employee-frontend/src/App.tsx"
Cohesion: 0.15
Nodes (19): App(), EvaluationPage, InsightsPage, KnowledgePage, NewBatchPage, QueuePage, RunDetailPage, RunsPage (+11 more)

### Community 18 - "users-frontend/package.json"
Cohesion: 0.09
Nodes (22): turbo, devDependencies, prettier, prettier-plugin-tailwindcss, turbo, typescript, engines, node (+14 more)

### Community 19 - "db/models.py"
Cohesion: 0.13
Nodes (16): get_result(), list_results(), read_intake_attachment(), review_result(), BatchInput, ReviewInput, ReviewRow, TicketResultRow (+8 more)

### Community 20 - "knowledge.py"
Cohesion: 0.11
Nodes (14): delete_document(), download_document(), index_document(), list_chunks(), list_documents(), _require_provider(), search_knowledge(), upload_document() (+6 more)

### Community 21 - "web/package.json"
Cohesion: 0.08
Nodes (25): jsdom, @testing-library/user-event, @workspace/ui, eslint, @eslint/js, eslint-plugin-react-hooks, eslint-plugin-react-refresh, globals (+17 more)

### Community 22 - "main.py"
Cohesion: 0.11
Nodes (19): _safe_dispatch(), get_run(), list_runs(), start_run(), RunRow, create_app(), lifespan(), recover() (+11 more)

### Community 23 - "compilerOptions"
Cohesion: 0.08
Nodes (23): compilerOptions, allowArbitraryExtensions, allowImportingTsExtensions, erasableSyntaxOnly, jsx, lib, module, moduleDetection (+15 more)

### Community 24 - "employee-frontend/components.json"
Cohesion: 0.09
Nodes (21): aliases, components, hooks, lib, ui, utils, iconLibrary, menuAccent (+13 more)

### Community 25 - "test_workspace_api.py"
Cohesion: 0.23
Nodes (7): start_run(), test_batch_and_queue_expose_real_results(), test_batch_failure_is_isolated_and_conflicting_ids_rejected(), test_openrouter_credentials_enable_api_modes_without_exposing_keys(), test_progress_counts_only_durable_results_after_save_failure(), fail_one_save(), test_review_requires_text_and_rejects_stale_updates()

### Community 26 - "compilerOptions"
Cohesion: 0.09
Nodes (22): compilerOptions, allowArbitraryExtensions, allowImportingTsExtensions, erasableSyntaxOnly, jsx, lib, module, moduleDetection (+14 more)

### Community 27 - "web/src/components/theme-provider.tsx"
Cohesion: 0.17
Nodes (12): App(), disableTransitionsTemporarily(), getSystemTheme(), isEditableTarget(), isTheme(), ResolvedTheme, Theme, THEME_VALUES (+4 more)

### Community 28 - "test_embeddings.py"
Cohesion: 0.13
Nodes (17): OpenRouterEmbedder, settings(), test_33_inputs_are_batched_and_each_batch_maps_its_own_indexes(), test_billed_batch_cost_survives_cancellation_without_cross_call_leakage(), test_cancellation_propagates_to_the_callers_deadline(), test_empty_input_returns_empty_batch_without_a_request(), unexpected_request(), test_later_batch_failure_retains_prior_successful_request_cost() (+9 more)

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
Nodes (34): KnowledgeChunk, KnowledgeService, FakeEmbedder, GatedEmbedder, LateEmbedder, PaidEmbedder, count_chunks(), test_category_filters_include_general_policies_and_validate_tags() (+26 more)

### Community 36 - "web/components.json"
Cohesion: 0.10
Nodes (19): aliases, components, hooks, lib, ui, utils, iconLibrary, menuAccent (+11 more)

### Community 38 - "pipeline/graph.py"
Cohesion: 0.09
Nodes (31): _run_with_db(), create_run(), finish_run(), load_incidents(), load_transactions(), save_outcomes(), SqlTransactionRepo, _to_record() (+23 more)

### Community 39 - "ui/components.json"
Cohesion: 0.10
Nodes (19): aliases, components, hooks, lib, ui, utils, iconLibrary, menuAccent (+11 more)

### Community 40 - "test_submission.py"
Cohesion: 0.32
Nodes (4): _payload(), test_concurrent_submit_dispatches_once(), test_second_request_id_reuses_the_approved_review(), test_submission_replay_creates_one_ticket()

### Community 41 - "fact"
Cohesion: 0.25
Nodes (29): Attachment, EvidenceRef, merge_analysis(), context(), fact(), message(), proposal(), test_additional_issue_is_resolved_in_place_instead_of_appended() (+21 more)

### Community 43 - "Human Review Gate"
Cohesion: 0.25
Nodes (4): support CLI, Support Workspace UI Plan, Review API, Workspace UI Verification

### Community 44 - "compilerOptions"
Cohesion: 0.12
Nodes (16): compilerOptions, allowImportingTsExtensions, erasableSyntaxOnly, lib, module, moduleDetection, noEmit, noFallthroughCasesInSwitch (+8 more)

### Community 46 - "RagDrafter"
Cohesion: 0.12
Nodes (6): _Execution, _ModelUsage, RagDrafter, DraftContext, test_real_search_fault_carries_safe_draft_execution_error(), Task 5: Agent, failure conversion and pipeline wiring

### Community 47 - "compilerOptions"
Cohesion: 0.12
Nodes (16): compilerOptions, allowImportingTsExtensions, erasableSyntaxOnly, lib, module, moduleDetection, noEmit, noFallthroughCasesInSwitch (+8 more)

### Community 48 - "support_test"
Cohesion: 0.18
Nodes (13): support_test(), Evidence by layer, Known limitations and remaining work, Repeatable local walkthrough, Synthetic demo readiness, Citation IDs and provider evidence, Commands and automated verification — historical Task 8, Corpus and actual retrieval (+5 more)

### Community 57 - "parse_document"
Cohesion: 0.10
Nodes (30): TextChunk, _append_chunks(), _check_extracted_size(), DocumentParseError, parse_document(), _parse_pdf(), make_pdf(), test_arabic_text_and_bom_are_preserved() (+22 more)

### Community 58 - "investigation.py"
Cohesion: 0.16
Nodes (14): TxnRecord, parse_dt(), DraftToolInputError, _datetime(), _days(), _field(), _involves(), _phone() (+6 more)

### Community 59 - "intake/repository.py"
Cohesion: 0.12
Nodes (26): CustomerReview, Receipt, ReviewSnapshot, IntakeAttachmentRow, IntakeMessageRow, IntakeOperationRow, IntakeSubmissionRow, assert_same_operation() (+18 more)

### Community 60 - "guardrails.py"
Cohesion: 0.06
Nodes (56): Candidate, _add(), find_candidates(), normalize_phone(), _overlaps(), parse_amount(), resolve_date(), _safe_date() (+48 more)

### Community 61 - "NewBatchPage.tsx"
Cohesion: 0.15
Nodes (17): ingest(), Artifacts, servers and remaining concerns, Tabs(), TabsContent(), TabsList(), tabsListVariants, TabsTrigger(), Textarea() (+9 more)

### Community 62 - "lookup.py"
Cohesion: 0.17
Nodes (14): _as_date(), _iqd_amount(), match_transaction(), TransactionRepo, _ex(), _match(), test_ambiguous_then_disambiguated_by_counterpart(), test_amount_and_date_mismatch() (+6 more)

### Community 63 - "Settings"
Cohesion: 0.07
Nodes (22): Settings, GeminiStructuredLLM, make_draft_model(), make_gemini_llm(), test_blank_intake_model_is_rejected(), test_non_positive_image_limit_is_rejected(), test_relative_upload_directory_is_rooted_in_the_repository(), test_defaults() (+14 more)

### Community 64 - "tasks"
Cohesion: 0.12
Nodes (16): dependsOn, inputs, outputs, cache, persistent, dependsOn, dependsOn, $schema (+8 more)

### Community 65 - "format.ts"
Cohesion: 0.07
Nodes (47): Ticket Flow Charts Implementation Plan, 1. Outcome, 2. Scope, 5. Language, 6. How a result becomes the charts, 7. Sentences, 8. Tests, 9. Files (+39 more)

### Community 66 - "IntakePage.tsx"
Cohesion: 0.14
Nodes (19): Global Constraints, Intake Chat UI Implementation Plan, Task 1: Put the summary and receipt in the thread, Task 2: Put screenshots inside the composer, Task 3: Apply the workspace chat styles, Task 4: Check the page in the browser, 4. Components, ChatTranscript() (+11 more)

### Community 67 - "Analysis"
Cohesion: 0.14
Nodes (24): Analysis, test_reinspection_keeps_current_images_and_new_observations(), again(), initial(), test_review_after_failed_analysis_still_interprets_the_saved_message(), test_validation_failure_retains_usage_audit(), ainvoke(), _amount() (+16 more)

### Community 68 - "PipelineState"
Cohesion: 0.11
Nodes (18): 10. Remaining demo roadmap, 1. Intent and acceptance criteria, 3. Provider and configuration, 4. Knowledge ingestion and persistence, 5. Retrieval and evidence, 6. Bounded investigation agent, 7. Draft guardrails and failure outcomes, 8. Pipeline, API, CLI and UI integration (+10 more)

### Community 69 - "main.py"
Cohesion: 0.09
Nodes (10): get_session(), health(), insights(), workspace(), Base, TicketRow, init_db(), upgrade_workspace_schema() (+2 more)

### Community 70 - "PipelineState"
Cohesion: 0.12
Nodes (11): DraftResult, _Nodes, Drafter, DraftExecutionError, NullDrafter, UnavailableDrafter, PipelineState, Global Constraints (+3 more)

### Community 71 - "cli.py"
Cohesion: 0.10
Nodes (19): _command_settings(), ingest_kb_cmd(), init_db_cmd(), Mode, run_batch_cmd(), _run_in_memory(), seed_db_cmd(), _sessionmaker() (+11 more)

### Community 72 - "load_taxonomy"
Cohesion: 0.14
Nodes (6): load_taxonomy(), TaxonomyError, tax(), taxonomy(), taxonomy(), test_rejects_unknown_team()

### Community 73 - "IntakeRepository"
Cohesion: 0.26
Nodes (4): Credentials, SessionView, IntakeService, make_intake_service()

### Community 74 - "lib/types.ts"
Cohesion: 0.11
Nodes (27): acceptIndexRequest(), canRequestIndex(), PendingIndexes, persistPendingIndexes(), pollKnowledge(), refresh(), stop(), PollOptions (+19 more)

### Community 75 - "test-kb/README.md"
Cohesion: 0.08
Nodes (13): Fictional RAG walkthrough inputs, توثيق الحساب — سياسة خيالية للعرض التجريبي, نزاع مع وكيل — سياسة خيالية للعرض التجريبي, أعطال التطبيق — سياسة خيالية للعرض التجريبي, دفع الفواتير — سياسة خيالية للعرض التجريبي, مشاكل البطاقة — سياسة خيالية للعرض التجريبي, التحويل المعلّق — سياسة خيالية للعرض التجريبي, الاستفسار الآمن من الدعم — سياسة خيالية للعرض التجريبي (+5 more)

### Community 76 - "agent.py"
Cohesion: 0.07
Nodes (6): _error_cost(), _number(), DraftToolLimit, CredentialChecker, DraftChatOpenRouter, DraftProviderResponseError

### Community 77 - "build_pipeline"
Cohesion: 0.11
Nodes (20): Sample, build_pipeline(), ConfigError, make_jev_client(), model_ids(), GeminiAnalysis, FakeStructuredLLM, ScriptedChat (+12 more)

### Community 79 - "devDependencies"
Cohesion: 0.12
Nodes (16): devDependencies, eslint, @eslint/js, eslint-plugin-react-hooks, eslint-plugin-react-refresh, globals, prettier, prettier-plugin-tailwindcss (+8 more)

### Community 80 - "judge-demo.ar.md"
Cohesion: 0.14
Nodes (13): أعطال التطبيق — سياسة خيالية للعرض التجريبي, استرجاع مبلغ شراء — سياسة خيالية للعرض التجريبي, استعادة الدخول — سياسة خيالية للعرض التجريبي, الاستفسار الآمن من الدعم — سياسة خيالية للعرض التجريبي, الاستفسار المؤقت للدعم في المهمة ٨ — سياسة خيالية للعرض التجريبي, التحويل المعلّق — سياسة خيالية للعرض التجريبي, التحويل لمستلم بالخطأ — سياسة خيالية للعرض التجريبي, الطلبات غير الواضحة وخارج النطاق — سياسة خيالية للعرض التجريبي (+5 more)

### Community 93 - "pipeline/contracts.py"
Cohesion: 0.10
Nodes (34): StructuredLLM, Candidates, ClassificationResult, ClassifierOutput, ExtractedField, FieldPick, NormalizedTicket, Classifier (+26 more)

### Community 94 - "devDependencies"
Cohesion: 0.11
Nodes (19): devDependencies, eslint, @eslint/js, eslint-plugin-react-hooks, eslint-plugin-react-refresh, globals, jsdom, @tailwindcss/vite (+11 more)

### Community 95 - "devDependencies"
Cohesion: 0.14
Nodes (14): devDependencies, eslint, @eslint/js, eslint-plugin-react-hooks, eslint-plugin-react-refresh, globals, tailwindcss, @tailwindcss/vite (+6 more)

### Community 96 - "UploadedDocument"
Cohesion: 0.16
Nodes (14): UploadedDocument, document_filename(), document_view(), DocumentValidationError, store_document(), KnowledgeDocumentIndex, ingest_one(), ingest_paths() (+6 more)

### Community 97 - "ticket-flow.ts"
Cohesion: 0.09
Nodes (51): Task 1: Sentence catalog, Task 2: Which step is open, Task 3: Received, produced, and drafting events, Task 4: Mermaid source, Task 5: Draw the charts on the ticket page, buildTicketFlow(), AR, channelName() (+43 more)

### Community 98 - "useCopy"
Cohesion: 0.16
Nodes (16): LanguageToggle(), intakeFixture, factValue(), IntakeEvidence(), Screenshot(), applyDocumentLocale(), copies, Copy (+8 more)

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
Cohesion: 0.13
Nodes (15): dependencies, @base-ui/react, class-variance-authority, cn, @fontsource/tajawal, @fontsource-variable/plus-jakarta-sans, lucide-react, mermaid (+7 more)

### Community 103 - "InvalidEvidence"
Cohesion: 0.17
Nodes (16): Fact, canonical_digits(), normalize_reported_date(), _apply(), _check_reference(), _compact(), checked_update(), _newer_correction() (+8 more)

### Community 104 - "dependencies"
Cohesion: 0.15
Nodes (13): dependencies, @base-ui/react, class-variance-authority, cn, @fontsource/tajawal, @fontsource-variable/plus-jakarta-sans, @hugeicons/core-free-icons, @hugeicons/react (+5 more)

### Community 105 - "compilerOptions"
Cohesion: 0.17
Nodes (11): compilerOptions, jsx, lib, module, moduleResolution, outDir, skipLibCheck, strict (+3 more)

### Community 106 - "EmbeddingError"
Cohesion: 0.17
Nodes (8): EmbeddingBatch, EmbeddingError, _nonnegative_number(), _ordered_vectors(), _response_cost(), Embeddings, test_lock_serializes_operations_and_submit_waits_for_inflight_search(), embed()

### Community 107 - "controller.test.ts"
Cohesion: 0.21
Nodes (7): controller, emptySession(), fakeApi(), review, browserSessionStorage(), SessionStorage, SavedSession

### Community 108 - "test_final_fix_handoff.py"
Cohesion: 0.11
Nodes (21): Passage, process_batch(), assert_completed_evidence(), faulty_knowledge(), read(), outer_deadlines(), PaidEmbeddings, runner_env() (+13 more)

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

### Community 114 - "Customer intake verification — 2026-10-18"
Cohesion: 0.25
Nodes (6): Browser handoff, Customer intake verification — 2026-10-18, Final automated checks, Live vision and paired review, Repaired gaps and regression evidence, Review decisions and remaining limits

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

### Community 119 - "test_draft_model.py"
Cohesion: 0.33
Nodes (7): response_payload(), run_provider_pipeline(), send(), search_response(), test_empty_choices_escalates_and_keeps_paid_response_usage(), test_failed_response_id_is_deduplicated_against_earlier_success(), test_other_conversion_value_errors_remain_unexpected()

### Community 120 - "scripts"
Cohesion: 0.50
Nodes (4): scripts, format, lint, typecheck

### Community 122 - "context"
Cohesion: 0.14
Nodes (22): _aware(), IntakeModel, IntakeState, Message, Question, QuestionRecord, Readiness, _asked_already() (+14 more)

### Community 123 - "intake/helpers.py"
Cohesion: 0.15
Nodes (7): TurnContext, IntakeGraph, _invitation(), grounded_analysis(), grounded_review(), image_evidence(), ScriptedIntakeModel

### Community 124 - "attachments.py"
Cohesion: 0.10
Nodes (29): AttachmentStore, _display_name(), IntakeSessionRow, ImageRejected, IntakeError, NotOwned, OperationConflict, StaleReview (+21 more)

### Community 125 - "test_cli.py"
Cohesion: 0.18
Nodes (9): test_config_error_exits_2(), boom(), test_ingest_directory_is_deterministic_and_duplicate_is_free(), test_ingest_disabled_configuration_never_calls_provider(), test_ingest_failure_exit_and_retry_stored(), test_ingest_invalid_source_does_not_stop_other_files(), test_ingest_limits_batch_without_partial_side_effects(), test_retry_stored_indexes_old_uploads_without_recovering_other_process_jobs() (+1 more)

### Community 126 - "test_db_deadline_cancelled_publication_cannot_commit_late"
Cohesion: 0.29
Nodes (3): test_db_deadline_cancelled_publication_cannot_commit_late(), test_db_deadline_is_cumulative_across_publication_statements(), changed_index()

### Community 127 - "InvalidEvidence"
Cohesion: 0.18
Nodes (15): ReviewText, InvalidEvidence, validate(), build_review(), _compact(), _render_value(), _ticket_text(), _tokens() (+7 more)

### Community 128 - "response_payload"
Cohesion: 0.22
Nodes (17): embedder_for(), item(), response_payload(), respond(), respond(), test_billed_cost_survives_cancellation_during_client_close(), test_billed_response_cost_is_retained_when_its_vectors_are_invalid(), test_cost_uses_one_reported_value_or_configured_token_estimate() (+9 more)

### Community 129 - "intake/model.py"
Cohesion: 0.11
Nodes (26): ImageInput, ModelCall, ModelUnavailable, _analysis_prompt(), _bounded_context(), _guard_size(), ModelBudget, OpenRouterIntakeModel (+18 more)

### Community 130 - "Plan 3 RAG Drafting Implementation Plan"
Cohesion: 0.18
Nodes (11): Completion and review record — 2026-10-17, Execution handoff, File map and shared interfaces, Global Constraints, Plan 3 RAG Drafting Implementation Plan, Plan self-review, Review Focus, Task 3: Ticket-scoped investigation and all eight tools (+3 more)

### Community 131 - "intake.py"
Cohesion: 0.16
Nodes (19): create_session(), _credentials(), _dump(), get_session(), post_message(), read_attachment(), remove_attachment(), request_review() (+11 more)

### Community 132 - "_DatabaseCall"
Cohesion: 0.12
Nodes (4): _Claim, _consume(), _DatabaseCall, IndexAttemptLostError

### Community 134 - "test_recovery_regressions.py"
Cohesion: 0.35
Nodes (10): command(), create(), test_actual_app_restart_reconciles_failed_placeholder(), test_failed_review_retry_cannot_reopen_submitted_session(), test_original_payload_identity_survives_sanitization(), test_publication_failure_is_retryable_without_restart(), fail_once(), test_receipt_reference_is_preserved() (+2 more)

### Community 135 - "Customer Conversation Intake Implementation Plan"
Cohesion: 0.25
Nodes (8): Completion audit — 2026-10-18, Customer Conversation Intake Implementation Plan, Execution conventions and repository baseline, File map and dependency order, Global Constraints, Plan review and execution handoff, Review Focus, Spec coverage and acceptance map

### Community 136 - "intake/conftest.py"
Cohesion: 0.13
Nodes (18): make_engine(), make_sessionmaker(), reset_db(), build_graph(), PipelineDeps, InMemoryTransactionRepo, intake_client(), pipeline() (+10 more)

### Community 137 - "KnowledgePage"
Cohesion: 0.60
Nodes (5): beginMutation(), deleteDocument(), finishMutation(), indexDocument(), upload()

### Community 138 - "intake/api.ts"
Cohesion: 0.15
Nodes (13): createIntakeApi(), IntakeRequestError, isRecord(), parseJson(), parseReceipt(), parseSession(), readError(), stringList() (+5 more)

### Community 139 - "index_deadlines"
Cohesion: 0.40
Nodes (3): index_deadlines(), settings(), expire_during_embedding()

### Community 140 - "test_dbapi_commit_handoff_arbitrates_cancellation"
Cohesion: 0.47
Nodes (4): test_dbapi_commit_handoff_arbitrates_cancellation(), gate(), gate_before_dbapi(), gate_inside_dbapi()

### Community 148 - "kb/service.py"
Cohesion: 0.14
Nodes (6): SearchResult, _abandoned(), _check_deadline(), _error_cost(), KnowledgeError, KnowledgeExecutionError

### Community 151 - "canReview"
Cohesion: 0.50
Nodes (3): Task 8: Employee evidence panel and processing state, canReview(), REVIEWABLE

### Community 155 - "IntakePage.test.tsx"
Cohesion: 0.26
Nodes (10): Task 6: Customer API client and resumable UI state, Task 7: Bilingual customer chat, screenshots and reviewed submission, copy(), attachment, collectingController(), emptySession(), fakeApi(), readyController() (+2 more)

### Community 156 - "employee-frontend/src/components/theme-provider.tsx"
Cohesion: 0.21
Nodes (11): disableTransitionsTemporarily(), getSystemTheme(), isEditableTarget(), isTheme(), ResolvedTheme, Theme, THEME_VALUES, ThemeProvider() (+3 more)

### Community 158 - "rules.py"
Cohesion: 0.16
Nodes (21): Decision, LookupResult, decide(), empty_ticket_decision(), merge_reasons(), note_for(), _unique(), Category (+13 more)

### Community 161 - "Customer intake chat layout"
Cohesion: 0.33
Nodes (5): 1. Outcome, 2. Scope, 3. Layout, 5. Checks, Customer intake chat layout

## Ambiguous Edges - Review These
- `Fraud Report` → `Plan 1 Live Smoke`  [AMBIGUOUS]
  README.md · relation: conceptually_related_to

## Knowledge Gaps
- **91 isolated node(s):** `zaincash-support`, `@base-ui/react`, `@fontsource-variable/plus-jakarta-sans`, `@fontsource/tajawal`, `@tailwindcss/vite` (+86 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 1000 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **36 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `HTTP contract (implemented in Tasks 4–5)` connect `attachments.py` to `intake/model.py`, `TurnStore`, `Analysis`, `Customer Conversation Intake Implementation Plan`, `main.py`, `canReview`, `IntakePage.test.tsx`, `guardrails.py`?**
  _High betweenness centrality (0.102) - this node is a cross-community bridge._
- **Are the 33 inferred relationships involving `Settings` (e.g. with `_command_settings()` and `_run_in_memory()`) actually correct?**
  _`Settings` has 33 INFERRED edges - model-reasoned connections that need verification._
- **What connects `zaincash-support`, `@base-ui/react`, `@fontsource-variable/plus-jakarta-sans` to the rest of the system?**
  _91 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `intake/types.ts` be split into smaller, more focused modules?**
  _Cohesion score 0.10952380952380952 - nodes in this community are weakly interconnected._
- **Why does `Settings` connect `Settings` to `response_payload`, `intake/model.py`, `pytest`, `Embedder`, `intake/conftest.py`, `index_deadlines`, `test_rag_api.py`, `kb/service.py`, `main.py`, `test_workspace_api.py`, `test_embeddings.py`, `test_draft_tools.py`, `test_kb_service.py`, `pipeline/graph.py`, `fact`, `RagDrafter`, `support_test`, `intake/repository.py`, `main.py`, `cli.py`, `load_taxonomy`, `agent.py`, `build_pipeline`, `EmbeddingError`, `test_final_fix_handoff.py`, `test_draft_model.py`, `attachments.py`, `test_cli.py`?**
  _High betweenness centrality (0.075) - this node is a cross-community bridge._
- **Are the 24 inferred relationships involving `KnowledgeService` (e.g. with `Settings` and `UploadedDocument`) actually correct?**
  _`KnowledgeService` has 24 INFERRED edges - model-reasoned connections that need verification._

### Low-confidence Hints
_AMBIGUOUS edges — the extractor was unsure. Verify before acting on these._

- **What is the exact relationship between `Fraud Report` and `Plan 1 Live Smoke`?**
  _Edge tagged AMBIGUOUS (relation: conceptually_related_to) - confidence is low._