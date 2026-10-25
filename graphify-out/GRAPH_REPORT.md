# Graph Report - zaincash-support  (2026-10-25)

## Corpus Check
- 300 files · ~249,722 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 30 file(s) not represented in the graph (top: (none) 18, .jsonl 4, .css 4)

## Summary
- 3024 nodes · 9344 edges · 159 communities (122 shown, 37 thin omitted)
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
- fakes.py
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
- db/repository.py
- ui/components.json
- Settings
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
- attachments.py
- intake/repository.py
- normalize.py
- NewBatchPage.tsx
- lookup.py
- test_llm.py
- tasks
- format.ts
- IntakePage.tsx
- test_handoff.py
- PipelineState
- datetime
- PipelineState
- cli.py
- factory.py
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
- guardrails.py
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
- IntakePage.test.tsx
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
- intake/contracts.py
- test_attachments.py
- AttachmentStore
- find_candidates
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
- index_deadlines
- test_dbapi_commit_handoff_arbitrates_cancellation
- test_gemini.py
- workspace.py
- @testing-library/react
- resolve_date
- KnowledgeError
- rag_fakes.py
- intake/README.md
- TicketReviewPage.tsx
- Ticket flow charts
- TicketInput
- ErrorEmbedder
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

## Communities (159 total, 37 thin omitted)

### Community 0 - "LLMUnavailable"
Cohesion: 0.11
Nodes (13): LLMUnavailable, combine(), merge_picks(), DraftChatOpenRouter, DraftProviderResponseError, test_both_missing_raises(), test_cost_is_summed(), test_degraded_when_jev_missing() (+5 more)

### Community 1 - "intake/types.ts"
Cohesion: 0.11
Nodes (21): IntakeApi, ControllerState, emptyState(), fileIdentity(), Credentials, CustomerReview, EvidenceRef, Fact (+13 more)

### Community 2 - "pytest"
Cohesion: 0.19
Nodes (38): test_contracts_reject_extra_keys(), test_datetimes_must_be_timezone_aware(), answer(), call(), Checker, draft_state(), script(), submit() (+30 more)

### Community 3 - "TurnStore"
Cohesion: 0.18
Nodes (13): OperationClaim, TurnResult, RevisionConflict, sanitize_intake_text(), _jsonable(), TurnStore, fail_once(), test_stale_attempt_audit_is_retained_once_with_attempt_identity() (+5 more)

### Community 4 - "make_ticket"
Cohesion: 0.14
Nodes (27): LookupResult, requests_credentials(), check(), state(), test_aggregation_is_deduplicated_and_has_no_state_side_effects(), test_amount_occurrences_keep_their_own_currency_and_sign(), test_avoid_sharing_warning_does_not_excuse_a_later_request(), test_candidate_prompt_limit_does_not_hide_later_ungrounded_references() (+19 more)

### Community 5 - "agent.py"
Cohesion: 0.06
Nodes (34): TxnRecord, parse_dt(), DraftAlreadySubmitted, DraftSubmission, DraftToolInputError, _datetime(), _days(), _field() (+26 more)

### Community 6 - "QueuePage.tsx"
Cohesion: 0.21
Nodes (30): EmptyState(), ErrorState(), LoadingState(), PageHeader(), PriorityBadge(), StatusBadge(), Table(), TableBody() (+22 more)

### Community 7 - "Customer conversation intake for ZainCash support"
Cohesion: 0.06
Nodes (31): 10. Verification and acceptance criteria, 11. Delivery and review, 1. Outcome and agreed requirements, 2. Current implementation and integration points, 3. Approach and boundaries, 4. Conversation state and turn flow, 5. Facts, evidence, and readiness, 6. Language and screenshot behavior (+23 more)

### Community 8 - "workspace-ui.tsx"
Cohesion: 0.15
Nodes (18): ConfirmDialog(), FilterSelect(), Button(), buttonVariants, Dialog(), DialogContent(), DialogDescription(), DialogFooter() (+10 more)

### Community 9 - "IntakeController"
Cohesion: 0.19
Nodes (5): IntakeController, isConflict(), isOffline(), safeMessage(), Language

### Community 10 - "FakeJevRunnable"
Cohesion: 0.09
Nodes (28): CredentialCheck, DegradedCredentialChecker, _finite_nonnegative(), _get(), JevCredentialChecker, FakeJevRunnable, ResponseRunnable, test_bad_usage_cannot_poison_cost() (+20 more)

### Community 11 - "test_rag_api.py"
Cohesion: 0.16
Nodes (18): TicketResultRow, client(), evidence_client(), kb_env(), test_actual_guardrail_failure_is_separate_from_reply(), test_concurrent_index_requests_share_active_work(), test_disabled_or_missing_provider_stores_without_indexing(), test_explicit_retry_tags_search_and_chunk_pagination() (+10 more)

### Community 12 - "employee-frontend/package.json"
Cohesion: 0.06
Nodes (31): @base-ui/react, class-variance-authority, cn, eslint, @eslint/js, eslint-plugin-react-hooks, eslint-plugin-react-refresh, @fontsource/tajawal (+23 more)

### Community 14 - "make_output"
Cohesion: 0.18
Nodes (24): DraftResult, NullDrafter, FakeClassifier, make_output(), make_ticket(), draft(), _deps(), _run() (+16 more)

### Community 15 - "Support Taxonomy Categories"
Cohesion: 0.21
Nodes (22): lookup, Account KYC, Account & Security, Agent Dispute, Agent Network, App Bug, Bill Payment, Card Issue (+14 more)

### Community 16 - "ui/package.json"
Cohesion: 0.07
Nodes (29): @turbo/gen, zod, @base-ui/react, class-variance-authority, cn, eslint, @eslint/js, eslint-plugin-react-hooks (+21 more)

### Community 17 - "employee-frontend/src/App.tsx"
Cohesion: 0.18
Nodes (16): App(), EvaluationPage, InsightsPage, KnowledgePage, NewBatchPage, QueuePage, RunDetailPage, RunsPage (+8 more)

### Community 18 - "users-frontend/package.json"
Cohesion: 0.09
Nodes (22): turbo, devDependencies, prettier, prettier-plugin-tailwindcss, turbo, typescript, engines, node (+14 more)

### Community 19 - "db/models.py"
Cohesion: 0.15
Nodes (11): get_session(), get_result(), list_results(), read_intake_attachment(), review_result(), ReviewInput, ReviewRow, TransactionRow (+3 more)

### Community 20 - "knowledge.py"
Cohesion: 0.10
Nodes (24): delete_document(), download_document(), index_document(), list_chunks(), list_documents(), _require_provider(), search_knowledge(), upload_document() (+16 more)

### Community 21 - "web/package.json"
Cohesion: 0.08
Nodes (25): jsdom, @testing-library/user-event, @workspace/ui, eslint, @eslint/js, eslint-plugin-react-hooks, eslint-plugin-react-refresh, globals (+17 more)

### Community 22 - "main.py"
Cohesion: 0.08
Nodes (23): _safe_dispatch(), upgrade_workspace_schema(), create_app(), lifespan(), recover(), fail_intake_placeholders(), reconcile_intake_run(), recover_intake_processing() (+15 more)

### Community 23 - "compilerOptions"
Cohesion: 0.08
Nodes (23): compilerOptions, allowArbitraryExtensions, allowImportingTsExtensions, erasableSyntaxOnly, jsx, lib, module, moduleDetection (+15 more)

### Community 24 - "employee-frontend/components.json"
Cohesion: 0.09
Nodes (21): aliases, components, hooks, lib, ui, utils, iconLibrary, menuAccent (+13 more)

### Community 25 - "fakes.py"
Cohesion: 0.19
Nodes (16): ExtractedField, FieldPick, FieldExtractor, _field(), fill_gaps(), finalize(), _is_weak(), FakeExtractor (+8 more)

### Community 26 - "compilerOptions"
Cohesion: 0.09
Nodes (22): compilerOptions, allowArbitraryExtensions, allowImportingTsExtensions, erasableSyntaxOnly, jsx, lib, module, moduleDetection (+14 more)

### Community 27 - "web/src/components/theme-provider.tsx"
Cohesion: 0.15
Nodes (13): App(), controller, disableTransitionsTemporarily(), getSystemTheme(), isEditableTarget(), isTheme(), ResolvedTheme, Theme (+5 more)

### Community 28 - "test_embeddings.py"
Cohesion: 0.16
Nodes (19): OpenRouterEmbedder, settings(), test_33_inputs_are_batched_and_each_batch_maps_its_own_indexes(), test_billed_batch_cost_survives_cancellation_without_cross_call_leakage(), test_billed_cost_survives_cancellation_during_client_close(), test_cancellation_propagates_to_the_callers_deadline(), test_empty_input_returns_empty_batch_without_a_request(), unexpected_request() (+11 more)

### Community 29 - "Classify and Extract Prompts"
Cohesion: 0.31
Nodes (9): extract, gemini_classify, Pipeline Graph Orchestration, jev_classify, prepare, Gemini Classify Prompt v1, Gemini Extract Prompt v1, GeminiClassifier (+1 more)

### Community 30 - "test_draft_tools.py"
Cohesion: 0.14
Nodes (26): api(), settings(), test_all_eight_tools_and_seven_parallel_calls_execute_only_six(), test_context_copies_input_and_rejects_raising_hard_call_limit(), test_database_faults_remain_distinct_and_record_paid_search_cost(), test_discovered_ref_can_be_inspected_but_not_promoted_to_match(), test_exact_and_fuzzy_queries_are_scoped_and_never_confirm_candidates(), test_exact_reference_still_requires_customer_and_excludes_future() (+18 more)

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
Cohesion: 0.10
Nodes (25): IndexAttemptLostError, GatedEmbedder, LateEmbedder, PaidEmbedder, count_chunks(), test_competing_callers_refuse_active_attempt_and_release_transactions(), test_db_deadline_cancelled_publication_cannot_commit_late(), test_db_deadline_includes_pool_and_checkout_without_late_claim() (+17 more)

### Community 36 - "web/components.json"
Cohesion: 0.10
Nodes (19): aliases, components, hooks, lib, ui, utils, iconLibrary, menuAccent (+11 more)

### Community 38 - "db/repository.py"
Cohesion: 0.13
Nodes (25): get_run(), list_runs(), start_run(), BatchInput, RunRow, TicketRow, create_run(), finish_run() (+17 more)

### Community 39 - "ui/components.json"
Cohesion: 0.10
Nodes (19): aliases, components, hooks, lib, ui, utils, iconLibrary, menuAccent (+11 more)

### Community 40 - "Settings"
Cohesion: 0.12
Nodes (10): Settings, test_blank_intake_model_is_rejected(), test_non_positive_image_limit_is_rejected(), test_relative_upload_directory_is_rooted_in_the_repository(), test_defaults(), test_drafting_configuration_cannot_bypass_hard_limits(), test_drafting_limits_load_from_environment(), test_env_overrides() (+2 more)

### Community 41 - "fact"
Cohesion: 0.17
Nodes (44): Analysis, EvidenceRef, Fact, merge_analysis(), context(), fact(), image_evidence(), message() (+36 more)

### Community 43 - "Human Review Gate"
Cohesion: 0.25
Nodes (4): support CLI, Support Workspace UI Plan, Review API, Workspace UI Verification

### Community 44 - "compilerOptions"
Cohesion: 0.12
Nodes (16): compilerOptions, allowImportingTsExtensions, erasableSyntaxOnly, lib, module, moduleDetection, noEmit, noFallthroughCasesInSwitch (+8 more)

### Community 46 - "RagDrafter"
Cohesion: 0.11
Nodes (6): _Execution, _ModelUsage, RagDrafter, DraftContext, DraftExecutionError, test_real_search_fault_carries_safe_draft_execution_error()

### Community 47 - "compilerOptions"
Cohesion: 0.12
Nodes (16): compilerOptions, allowImportingTsExtensions, erasableSyntaxOnly, lib, module, moduleDetection, noEmit, noFallthroughCasesInSwitch (+8 more)

### Community 48 - "support_test"
Cohesion: 0.18
Nodes (13): support_test(), Evidence by layer, Known limitations and remaining work, Repeatable local walkthrough, Synthetic demo readiness, Citation IDs and provider evidence, Commands and automated verification — historical Task 8, Corpus and actual retrieval (+5 more)

### Community 57 - "parse_document"
Cohesion: 0.11
Nodes (29): TextChunk, _append_chunks(), _check_extracted_size(), DocumentParseError, parse_document(), _parse_pdf(), make_pdf(), test_arabic_text_and_bom_are_preserved() (+21 more)

### Community 58 - "attachments.py"
Cohesion: 0.18
Nodes (13): _display_name(), IntakeMessageRow, IntakeError, NotOwned, OperationConflict, StaleReview, TurnBusy, assert_same_operation() (+5 more)

### Community 59 - "intake/repository.py"
Cohesion: 0.16
Nodes (20): CustomerReview, Receipt, ReviewSnapshot, IntakeAttachmentRow, IntakeOperationRow, _attachment(), customer_review(), initial_state() (+12 more)

### Community 60 - "normalize.py"
Cohesion: 0.19
Nodes (17): detect_arabizi(), fold_arabic(), has_latin_mix(), _latin_words(), mask_cards(), normalize(), sanitize_for_storage(), to_ascii_digits() (+9 more)

### Community 61 - "NewBatchPage.tsx"
Cohesion: 0.12
Nodes (16): Input(), Tabs(), TabsContent(), TabsList(), tabsListVariants, TabsTrigger(), Textarea(), readReport() (+8 more)

### Community 62 - "lookup.py"
Cohesion: 0.19
Nodes (13): _as_date(), _iqd_amount(), match_transaction(), TransactionRepo, _ex(), _match(), test_ambiguous_then_disambiguated_by_counterpart(), test_amount_and_date_mismatch() (+5 more)

### Community 63 - "test_llm.py"
Cohesion: 0.13
Nodes (11): GeminiStructuredLLM, make_gemini_llm(), _llm(), _S, test_draft_model_uses_millisecond_timeout_and_disables_sdk_retries(), test_openrouter_reported_cost_takes_precedence_over_token_estimate(), test_openrouter_retry_budget_is_bounded(), test_openrouter_structured_samples_use_configured_key_and_validate_output() (+3 more)

### Community 64 - "tasks"
Cohesion: 0.12
Nodes (16): dependsOn, inputs, outputs, cache, persistent, dependsOn, dependsOn, $schema (+8 more)

### Community 65 - "format.ts"
Cohesion: 0.11
Nodes (26): source, STAGE_NODES, timing(), renderableTrace(), reviewEvidence(), source, save(), checkFact() (+18 more)

### Community 66 - "IntakePage.tsx"
Cohesion: 0.13
Nodes (21): Global Constraints, Intake Chat UI Implementation Plan, Task 1: Put the summary and receipt in the thread, Task 2: Put screenshots inside the composer, Task 3: Apply the workspace chat styles, Task 4: Check the page in the browser, 4. Components, ChatTranscript() (+13 more)

### Community 67 - "test_handoff.py"
Cohesion: 0.31
Nodes (7): complete_conversation(), _dated(), _message(), _opening(), _png(), _review(), _user()

### Community 68 - "PipelineState"
Cohesion: 0.11
Nodes (18): 10. Remaining demo roadmap, 1. Intent and acceptance criteria, 3. Provider and configuration, 4. Knowledge ingestion and persistence, 5. Retrieval and evidence, 6. Bounded investigation agent, 7. Draft guardrails and failure outcomes, 8. Pipeline, API, CLI and UI integration (+10 more)

### Community 69 - "datetime"
Cohesion: 0.16
Nodes (5): Base, IncidentRow, IntakeSubmissionRow, employee_attachment(), intake_result_view()

### Community 70 - "PipelineState"
Cohesion: 0.17
Nodes (9): _Nodes, UnavailableDrafter, PipelineState, Global Constraints, Task 1: Sentence catalog, Ticket Flow Charts Implementation Plan, 3. What the employee sees, 4. Which step is open (+1 more)

### Community 71 - "cli.py"
Cohesion: 0.13
Nodes (15): _command_settings(), ingest_kb_cmd(), init_db_cmd(), Mode, run_batch_cmd(), _run_in_memory(), seed_db_cmd(), _sessionmaker() (+7 more)

### Community 72 - "factory.py"
Cohesion: 0.06
Nodes (26): build_graph(), PipelineDeps, InMemoryTransactionRepo, Drafter, load_taxonomy(), most_urgent(), priority_rank(), TaxonomyError (+18 more)

### Community 73 - "IntakeRepository"
Cohesion: 0.18
Nodes (7): Credentials, SessionView, IntakeService, _payload(), test_concurrent_submit_dispatches_once(), test_second_request_id_reuses_the_approved_review(), test_submission_replay_creates_one_ticket()

### Community 74 - "lib/types.ts"
Cohesion: 0.10
Nodes (32): acceptIndexRequest(), canRequestIndex(), PendingIndexes, persistPendingIndexes(), pollKnowledge(), refresh(), stop(), PollOptions (+24 more)

### Community 75 - "test-kb/README.md"
Cohesion: 0.08
Nodes (13): Fictional RAG walkthrough inputs, توثيق الحساب — سياسة خيالية للعرض التجريبي, نزاع مع وكيل — سياسة خيالية للعرض التجريبي, أعطال التطبيق — سياسة خيالية للعرض التجريبي, دفع الفواتير — سياسة خيالية للعرض التجريبي, مشاكل البطاقة — سياسة خيالية للعرض التجريبي, التحويل المعلّق — سياسة خيالية للعرض التجريبي, الاستفسار الآمن من الدعم — سياسة خيالية للعرض التجريبي (+5 more)

### Community 76 - "agent.py"
Cohesion: 0.06
Nodes (17): TicketOutcome, TicketExecution, _default_retry(), outcome_from_state(), _percentile(), _retryable(), RunSummary, summarize() (+9 more)

### Community 77 - "build_pipeline"
Cohesion: 0.13
Nodes (21): _run_with_db(), SqlTransactionRepo, Sample, build_pipeline(), ConfigError, make_jev_client(), model_ids(), run_batch() (+13 more)

### Community 79 - "devDependencies"
Cohesion: 0.12
Nodes (16): devDependencies, eslint, @eslint/js, eslint-plugin-react-hooks, eslint-plugin-react-refresh, globals, prettier, prettier-plugin-tailwindcss (+8 more)

### Community 80 - "judge-demo.ar.md"
Cohesion: 0.14
Nodes (13): أعطال التطبيق — سياسة خيالية للعرض التجريبي, استرجاع مبلغ شراء — سياسة خيالية للعرض التجريبي, استعادة الدخول — سياسة خيالية للعرض التجريبي, الاستفسار الآمن من الدعم — سياسة خيالية للعرض التجريبي, الاستفسار المؤقت للدعم في المهمة ٨ — سياسة خيالية للعرض التجريبي, التحويل المعلّق — سياسة خيالية للعرض التجريبي, التحويل لمستلم بالخطأ — سياسة خيالية للعرض التجريبي, الطلبات غير الواضحة وخارج النطاق — سياسة خيالية للعرض التجريبي (+5 more)

### Community 93 - "pipeline/contracts.py"
Cohesion: 0.12
Nodes (19): StructuredLLM, Candidates, ClassificationResult, ClassifierOutput, NormalizedTicket, Classifier, GeminiClassifier, GeminiExtractor (+11 more)

### Community 94 - "devDependencies"
Cohesion: 0.11
Nodes (19): devDependencies, eslint, @eslint/js, eslint-plugin-react-hooks, eslint-plugin-react-refresh, globals, jsdom, @tailwindcss/vite (+11 more)

### Community 95 - "devDependencies"
Cohesion: 0.14
Nodes (14): devDependencies, eslint, @eslint/js, eslint-plugin-react-hooks, eslint-plugin-react-refresh, globals, tailwindcss, @tailwindcss/vite (+6 more)

### Community 96 - "guardrails.py"
Cohesion: 0.20
Nodes (12): normalize_phone(), parse_amount(), _iso(), normalize_value(), check_draft(), _citation_findings(), _exact_amount(), _grounding_findings() (+4 more)

### Community 97 - "ticket-flow.ts"
Cohesion: 0.09
Nodes (50): Task 2: Which step is open, Task 3: Received, produced, and drafting events, Task 4: Mermaid source, Task 5: Draw the charts on the ticket page, buildTicketFlow(), AR, channelName(), checkLines() (+42 more)

### Community 98 - "useCopy"
Cohesion: 0.14
Nodes (15): LanguageToggle(), intakeFixture, factValue(), IntakeEvidence(), Screenshot(), applyDocumentLocale(), copies, Copy (+7 more)

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
Cohesion: 0.13
Nodes (15): dependencies, @base-ui/react, class-variance-authority, cn, @fontsource/tajawal, @fontsource-variable/plus-jakarta-sans, lucide-react, mermaid (+7 more)

### Community 103 - "InvalidEvidence"
Cohesion: 0.16
Nodes (16): canonical_digits(), normalize_reported_date(), InvalidEvidence, _apply(), _check_reference(), _compact(), checked_update(), _newer_correction() (+8 more)

### Community 104 - "dependencies"
Cohesion: 0.15
Nodes (13): dependencies, @base-ui/react, class-variance-authority, cn, @fontsource/tajawal, @fontsource-variable/plus-jakarta-sans, @hugeicons/core-free-icons, @hugeicons/react (+5 more)

### Community 105 - "compilerOptions"
Cohesion: 0.17
Nodes (11): compilerOptions, jsx, lib, module, moduleResolution, outDir, skipLibCheck, strict (+3 more)

### Community 106 - "EmbeddingError"
Cohesion: 0.13
Nodes (9): EmbeddingBatch, EmbeddingError, _nonnegative_number(), _ordered_vectors(), _response_cost(), Embeddings, test_lock_serializes_operations_and_submit_waits_for_inflight_search(), embed() (+1 more)

### Community 107 - "IntakePage.test.tsx"
Cohesion: 0.13
Nodes (17): HTTP contract (implemented in Tasks 4–5), Task 6: Customer API client and resumable UI state, Task 7: Bilingual customer chat, screenshots and reviewed submission, copy(), emptySession(), fakeApi(), review, attachment (+9 more)

### Community 108 - "test_final_fix_handoff.py"
Cohesion: 0.12
Nodes (22): Passage, process_batch(), Knowledge, assert_completed_evidence(), faulty_knowledge(), read(), outer_deadlines(), PaidEmbeddings (+14 more)

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
Cohesion: 0.27
Nodes (8): make_draft_model(), response_payload(), run_provider_pipeline(), send(), search_response(), test_empty_choices_escalates_and_keeps_paid_response_usage(), test_failed_response_id_is_deduplicated_against_earlier_success(), test_other_conversion_value_errors_remain_unexpected()

### Community 120 - "scripts"
Cohesion: 0.50
Nodes (4): scripts, format, lint, typecheck

### Community 122 - "context"
Cohesion: 0.14
Nodes (20): IntakeState, Question, Readiness, _asked_already(), asks_for_secret(), assess_readiness(), _can_ask(), canonical_category() (+12 more)

### Community 123 - "intake/contracts.py"
Cohesion: 0.14
Nodes (9): Attachment, _aware(), IntakeModel, Message, QuestionRecord, TurnContext, IntakeGraph, _invitation() (+1 more)

### Community 124 - "test_attachments.py"
Cohesion: 0.18
Nodes (15): IntakeSessionRow, ImageRejected, png_bytes(), test_active_turn_rejects_upload(), test_changed_invalid_bytes_conflict_before_decoding_replay(), test_concurrent_uploads_stop_at_the_session_cap(), attempt(), test_cross_session_read_and_removal() (+7 more)

### Community 125 - "AttachmentStore"
Cohesion: 0.13
Nodes (7): AttachmentStore, IntakeRepository, make_intake_service(), builder(), repo(), store(), repo()

### Community 126 - "find_candidates"
Cohesion: 0.25
Nodes (12): Candidate, _add(), find_candidates(), _overlaps(), test_amount_forms(), test_arabic_indic_amount_not_confused_with_phone(), test_dates_absolute_and_weekday(), test_dedupes_repeated_values() (+4 more)

### Community 127 - "InvalidEvidence"
Cohesion: 0.19
Nodes (14): ReviewText, build_review(), _compact(), _render_value(), _ticket_text(), _tokens(), validate_review_numbers(), review() (+6 more)

### Community 128 - "response_payload"
Cohesion: 0.25
Nodes (15): embedder_for(), item(), response_payload(), respond(), respond(), test_billed_response_cost_is_retained_when_its_vectors_are_invalid(), test_cost_uses_one_reported_value_or_configured_token_estimate(), test_invalid_response_envelopes_are_bounded() (+7 more)

### Community 129 - "intake/model.py"
Cohesion: 0.11
Nodes (27): ImageInput, ModelCall, ModelUnavailable, _analysis_prompt(), _bounded_context(), _guard_size(), ModelBudget, OpenRouterIntakeModel (+19 more)

### Community 130 - "Plan 3 RAG Drafting Implementation Plan"
Cohesion: 0.18
Nodes (11): Completion and review record — 2026-10-17, Execution handoff, File map and shared interfaces, Global Constraints, Plan 3 RAG Drafting Implementation Plan, Plan self-review, Review Focus, Task 3: Ticket-scoped investigation and all eight tools (+3 more)

### Community 131 - "intake.py"
Cohesion: 0.16
Nodes (19): create_session(), _credentials(), _dump(), get_session(), post_message(), read_attachment(), remove_attachment(), request_review() (+11 more)

### Community 132 - "_DatabaseCall"
Cohesion: 0.10
Nodes (7): KnowledgeChunk, _abandoned(), _check_deadline(), _Claim, _consume(), _DatabaseCall, _error_cost()

### Community 133 - "KnowledgeService"
Cohesion: 0.17
Nodes (13): Embedder, SearchResult, KnowledgeService, FakeEmbedder, test_category_filters_include_general_policies_and_validate_tags(), test_claim_locks_source_even_before_index_row_exists(), test_cosine_ranking_cutoff_and_duplicate_stable_ids(), test_incompatible_or_unowned_chunks_cannot_be_searched() (+5 more)

### Community 134 - "ingest.py"
Cohesion: 0.26
Nodes (8): load_jsonl(), load_tickets(), _rows(), test_csv_with_bom_and_missing_columns(), test_duplicate_external_ids_keep_first(), test_json_object_without_ids(), test_jsonl_fixture_loads(), test_unsupported_format()

### Community 135 - "Customer Conversation Intake Implementation Plan"
Cohesion: 0.25
Nodes (8): Completion audit — 2026-10-18, Customer Conversation Intake Implementation Plan, Execution conventions and repository baseline, File map and dependency order, Global Constraints, Plan review and execution handoff, Review Focus, Spec coverage and acceptance map

### Community 136 - "intake/conftest.py"
Cohesion: 0.11
Nodes (19): init_db(), make_engine(), make_sessionmaker(), reset_db(), intake_client(), intake_db(), reviewed(), test_repeated_init_db_keeps_existing_tickets() (+11 more)

### Community 137 - "KnowledgePage"
Cohesion: 0.57
Nodes (7): BadgeLabel(), KnowledgePage(), beginMutation(), deleteDocument(), finishMutation(), indexDocument(), upload()

### Community 138 - "intake/api.ts"
Cohesion: 0.15
Nodes (13): createIntakeApi(), IntakeRequestError, isRecord(), parseJson(), parseReceipt(), parseSession(), readError(), stringList() (+5 more)

### Community 139 - "index_deadlines"
Cohesion: 0.29
Nodes (4): index_deadlines(), settings(), test_index_deadline_persists_failure_and_retry_releases_slot(), expire_during_embedding()

### Community 140 - "test_dbapi_commit_handoff_arbitrates_cancellation"
Cohesion: 0.47
Nodes (4): test_dbapi_commit_handoff_arbitrates_cancellation(), gate(), gate_before_dbapi(), gate_inside_dbapi()

### Community 141 - "test_gemini.py"
Cohesion: 0.31
Nodes (12): ExtractedSpan, _Fields, GeminiFields, _a(), _classify(), test_all_samples_failing_raises(), test_extractor_requests_only_named_fields(), test_failed_samples_count_against_confidence() (+4 more)

### Community 142 - "workspace.py"
Cohesion: 0.27
Nodes (7): health(), insights(), workspace(), ingest(), latest_results_query(), Artifacts, servers and remaining concerns, start()

### Community 144 - "resolve_date"
Cohesion: 0.36
Nodes (4): resolve_date(), _safe_date(), test_resolve(), test_unresolvable_is_none()

### Community 148 - "KnowledgeError"
Cohesion: 0.20
Nodes (3): KnowledgeError, KnowledgeExecutionError, test_search_database_failure_preserves_completed_query_cost()

### Community 151 - "TicketReviewPage.tsx"
Cohesion: 0.17
Nodes (26): Task 8: Employee evidence panel and processing state, Confidence(), Metric(), Badge(), badgeVariants, Card(), CardContent(), CardHeader() (+18 more)

### Community 152 - "Ticket flow charts"
Cohesion: 0.22
Nodes (8): 1. Outcome, 2. Scope, 5. Language, 6. How a result becomes the charts, 7. Sentences, 8. Tests, 9. Files, Ticket flow charts

### Community 156 - "employee-frontend/src/components/theme-provider.tsx"
Cohesion: 0.21
Nodes (11): disableTransitionsTemporarily(), getSystemTheme(), isEditableTarget(), isTheme(), ResolvedTheme, Theme, THEME_VALUES, ThemeProvider() (+3 more)

### Community 158 - "rules.py"
Cohesion: 0.22
Nodes (16): Decision, decide(), empty_ticket_decision(), merge_reasons(), note_for(), _unique(), Category, _decide() (+8 more)

### Community 161 - "Customer intake chat layout"
Cohesion: 0.33
Nodes (5): 1. Outcome, 2. Scope, 3. Layout, 5. Checks, Customer intake chat layout

## Ambiguous Edges - Review These
- `Fraud Report` → `Plan 1 Live Smoke`  [AMBIGUOUS]
  README.md · relation: conceptually_related_to

## Knowledge Gaps
- **91 isolated node(s):** `zaincash-support`, `@base-ui/react`, `@fontsource-variable/plus-jakarta-sans`, `@fontsource/tajawal`, `@tailwindcss/vite` (+86 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 1001 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **37 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `HTTP contract (implemented in Tasks 4–5)` connect `IntakePage.test.tsx` to `guardrails.py`, `intake/model.py`, `TurnStore`, `db/repository.py`, `Customer Conversation Intake Implementation Plan`, `intake/conftest.py`, `TicketReviewPage.tsx`, `attachments.py`?**
  _High betweenness centrality (0.101) - this node is a cross-community bridge._
- **Are the 33 inferred relationships involving `Settings` (e.g. with `_command_settings()` and `_run_in_memory()`) actually correct?**
  _`Settings` has 33 INFERRED edges - model-reasoned connections that need verification._
- **What connects `zaincash-support`, `@base-ui/react`, `@fontsource-variable/plus-jakarta-sans` to the rest of the system?**
  _91 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `LLMUnavailable` be split into smaller, more focused modules?**
  _Cohesion score 0.11083743842364532 - nodes in this community are weakly interconnected._
- **Why does `Settings` connect `Settings` to `intake/model.py`, `pytest`, `_DatabaseCall`, `KnowledgeService`, `intake/conftest.py`, `index_deadlines`, `test_rag_api.py`, `main.py`, `test_embeddings.py`, `test_draft_tools.py`, `test_kb_service.py`, `db/repository.py`, `fact`, `RagDrafter`, `support_test`, `attachments.py`, `intake/repository.py`, `test_llm.py`, `cli.py`, `factory.py`, `agent.py`, `build_pipeline`, `EmbeddingError`, `test_final_fix_handoff.py`, `test_draft_model.py`, `AttachmentStore`?**
  _High betweenness centrality (0.073) - this node is a cross-community bridge._
- **Are the 24 inferred relationships involving `KnowledgeService` (e.g. with `Settings` and `UploadedDocument`) actually correct?**
  _`KnowledgeService` has 24 INFERRED edges - model-reasoned connections that need verification._

### Low-confidence Hints
_AMBIGUOUS edges — the extractor was unsure. Verify before acting on these._

- **What is the exact relationship between `Fraud Report` and `Plan 1 Live Smoke`?**
  _Edge tagged AMBIGUOUS (relation: conceptually_related_to) - confidence is low._