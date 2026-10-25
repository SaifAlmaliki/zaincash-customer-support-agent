# Graph Report - zaincash-support  (2026-10-25)

## Corpus Check
- 300 files · ~248,184 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 30 file(s) not represented in the graph (top: (none) 18, .jsonl 4, .css 4)

## Summary
- 3012 nodes · 9305 edges · 165 communities (117 shown, 48 thin omitted)
- Extraction: 89% EXTRACTED · 11% INFERRED · 0% AMBIGUOUS · INFERRED: 1046 edges (avg confidence: 0.93)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `7185740d`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- agent.py
- intake/types.ts
- pytest
- TurnStore
- make_ticket
- build_tools
- QueuePage.tsx
- Customer conversation intake for ZainCash support
- workspace-ui.tsx
- IntakeController
- test_credential_check.py
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
- asyncio
- ui/components.json
- test_submission.py
- fact
- Vite Config
- Human Review Gate
- compilerOptions
- DraftContext
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
- test_llm.py
- tasks
- TicketReviewPage.tsx
- IntakePage.tsx
- test_handoff.py
- PipelineState
- UploadedDocument
- PipelineState
- attachments.py
- load_taxonomy
- Credentials
- lib/types.ts
- test-kb/README.md
- Plan 3 — Knowledge retrieval and grounded reply drafting
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
- json
- ticket-flow.ts
- useCopy
- compilerOptions
- قواعد المعرفة العربية للعرض أمام لجنة التحكيم
- pydantic
- dependencies
- InvalidEvidence
- dependencies
- compilerOptions
- agent.py
- controller.test.ts
- test_final_fix_handoff.py
- ZainCash Support Workspace
- negative/README.md
- scripts
- scripts
- compilerOptions
- Settings
- dependencies
- web/tsconfig.json
- employee-frontend/tsconfig.json
- exports
- jev.py
- scripts
- users-frontend/README.md
- context
- TurnContext
- attachments.py
- test_cli.py
- intake/contracts.py
- InvalidEvidence
- Ticket flow charts
- intake/model.py
- RunRow
- intake.py
- KnowledgeService
- _DatabaseCall
- test_recovery_regressions.py
- _bounded
- intake/conftest.py
- _finite_nonnegative
- intake/api.ts
- ar/other.md
- test_dbapi_commit_handoff_arbitrates_cancellation
- fixture
- task8-history-policy.md
- @testing-library/react
- FakeJevRunnable
- intake/README.md
- ar/account_kyc.md
- ar/agent_dispute.md
- ar/failed_transfer.md
- ar/app_bug.md
- IntakePage.test.tsx
- employee-frontend/src/components/theme-provider.tsx
- ar/bill_payment.md
- rules.py
- trace-facts.ts
- ar/fraud_report.md
- Customer intake chat layout
- ar/general_inquiry.md
- ar/login_access.md
- ar/wrong_recipient.md

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

## Communities (165 total, 48 thin omitted)

### Community 0 - "agent.py"
Cohesion: 0.06
Nodes (8): get_settings(), SearchResult, _error_cost(), _number(), DraftToolLimit, CredentialChecker, DraftChatOpenRouter, DraftProviderResponseError

### Community 1 - "intake/types.ts"
Cohesion: 0.11
Nodes (23): IntakeApi, ControllerState, emptyState(), fileIdentity(), factText(), Attachment, Credentials, CustomerReview (+15 more)

### Community 2 - "pytest"
Cohesion: 0.19
Nodes (37): answer(), call(), Checker, draft_state(), Knowledge, script(), submit(), pipeline() (+29 more)

### Community 3 - "TurnStore"
Cohesion: 0.16
Nodes (11): OperationClaim, TurnResult, RevisionConflict, sanitize_intake_text(), _jsonable(), TurnStore, repo(), test_recovered_attempt_cannot_publish_stale_output() (+3 more)

### Community 4 - "make_ticket"
Cohesion: 0.14
Nodes (29): requests_credentials(), make_ticket(), check(), state(), test_aggregation_is_deduplicated_and_has_no_state_side_effects(), test_amount_occurrences_keep_their_own_currency_and_sign(), test_avoid_sharing_warning_does_not_excuse_a_later_request(), test_candidate_prompt_limit_does_not_hide_later_ungrounded_references() (+21 more)

### Community 5 - "build_tools"
Cohesion: 0.12
Nodes (6): DraftSubmission, build_tools(), flag(), retrieve(), status(), _error_cost()

### Community 6 - "QueuePage.tsx"
Cohesion: 0.14
Nodes (46): EmptyState(), ErrorState(), LoadingState(), Metric(), PageHeader(), PriorityBadge(), StatusBadge(), Button() (+38 more)

### Community 7 - "Customer conversation intake for ZainCash support"
Cohesion: 0.06
Nodes (32): 10. Verification and acceptance criteria, 11. Delivery and review, 1. Outcome and agreed requirements, 2. Current implementation and integration points, 3. Approach and boundaries, 4. Conversation state and turn flow, 5. Facts, evidence, and readiness, 6. Language and screenshot behavior (+24 more)

### Community 8 - "workspace-ui.tsx"
Cohesion: 0.11
Nodes (16): ConfirmDialog(), FilterSelect(), Dialog(), DialogContent(), DialogDescription(), DialogFooter(), DialogHeader(), DialogOverlay() (+8 more)

### Community 9 - "IntakeController"
Cohesion: 0.20
Nodes (5): IntakeController, isConflict(), isOffline(), safeMessage(), Language

### Community 10 - "test_credential_check.py"
Cohesion: 0.15
Nodes (16): CredentialCheck, DegradedCredentialChecker, JevCredentialChecker, ResponseRunnable, test_bad_usage_cannot_poison_cost(), test_cancellation_propagates_with_cost_for_outer_timeout_owner(), test_invalid_price_is_a_configuration_error(), test_malformed_noul_degrades_without_losing_measured_cost() (+8 more)

### Community 11 - "test_rag_api.py"
Cohesion: 0.14
Nodes (18): client(), evidence_client(), test_actual_guardrail_failure_is_separate_from_reply(), test_concurrent_index_requests_share_active_work(), test_disabled_or_missing_provider_stores_without_indexing(), test_explicit_retry_tags_search_and_chunk_pagination(), test_health_distinguishes_failed_from_empty(), test_health_requires_compatible_nonempty_index() (+10 more)

### Community 12 - "employee-frontend/package.json"
Cohesion: 0.06
Nodes (31): @base-ui/react, class-variance-authority, cn, eslint, @eslint/js, eslint-plugin-react-hooks, eslint-plugin-react-refresh, @fontsource/tajawal (+23 more)

### Community 14 - "make_output"
Cohesion: 0.14
Nodes (30): build_graph(), PipelineDeps, FakeClassifier, make_output(), pipeline(), test_run_batch_no_db_writes_summary_and_out(), fake_build(), response_payload() (+22 more)

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
Cohesion: 0.09
Nodes (20): get_session(), get_result(), list_results(), read_intake_attachment(), review_result(), ReviewInput, health(), insights() (+12 more)

### Community 20 - "knowledge.py"
Cohesion: 0.11
Nodes (16): delete_document(), download_document(), index_document(), list_chunks(), list_documents(), _require_provider(), search_knowledge(), upload_document() (+8 more)

### Community 21 - "web/package.json"
Cohesion: 0.08
Nodes (25): jsdom, @testing-library/user-event, @workspace/ui, eslint, @eslint/js, eslint-plugin-react-hooks, eslint-plugin-react-refresh, globals (+17 more)

### Community 22 - "main.py"
Cohesion: 0.10
Nodes (13): upgrade_workspace_schema(), create_app(), recover(), fail_intake_placeholders(), reconcile_intake_run(), recover_intake_processing(), dispatch_intake(), IndexJobs (+5 more)

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
Cohesion: 0.08
Nodes (41): EmbeddingBatch, EmbeddingError, _nonnegative_number(), OpenRouterEmbedder, _ordered_vectors(), _response_cost(), Embeddings, embed() (+33 more)

### Community 29 - "Classify and Extract Prompts"
Cohesion: 0.31
Nodes (9): extract, gemini_classify, Pipeline Graph Orchestration, jev_classify, prepare, Gemini Classify Prompt v1, Gemini Extract Prompt v1, GeminiClassifier (+1 more)

### Community 30 - "test_draft_tools.py"
Cohesion: 0.14
Nodes (29): TicketRow, TransactionRow, test_contracts_reject_extra_keys(), test_datetimes_must_be_timezone_aware(), test_repeated_init_db_keeps_existing_tickets(), ErrorEmbedder, test_all_eight_tools_and_seven_parallel_calls_execute_only_six(), test_context_copies_input_and_rejects_raising_hard_call_limit() (+21 more)

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
Cohesion: 0.09
Nodes (34): KnowledgeChunk, IndexAttemptLostError, FakeEmbedder, GatedEmbedder, LateEmbedder, PaidEmbedder, count_chunks(), settings() (+26 more)

### Community 36 - "web/components.json"
Cohesion: 0.10
Nodes (19): aliases, components, hooks, lib, ui, utils, iconLibrary, menuAccent (+11 more)

### Community 38 - "asyncio"
Cohesion: 0.07
Nodes (39): _command_settings(), ingest_kb_cmd(), init_db_cmd(), Mode, run_batch_cmd(), _run_in_memory(), _run_with_db(), seed_db_cmd() (+31 more)

### Community 39 - "ui/components.json"
Cohesion: 0.10
Nodes (19): aliases, components, hooks, lib, ui, utils, iconLibrary, menuAccent (+11 more)

### Community 40 - "test_submission.py"
Cohesion: 0.19
Nodes (8): IncidentRow, _payload(), test_concurrent_submit_dispatches_once(), test_second_request_id_reuses_the_approved_review(), test_submission_replay_creates_one_ticket(), test_incident_windows_are_inclusive_bounded_and_read_only(), observe(), test_search_and_incidents_limit_ten_and_all_database_calls_run_off_loop()

### Community 41 - "fact"
Cohesion: 0.17
Nodes (44): Analysis, EvidenceRef, Fact, merge_analysis(), context(), fact(), image_evidence(), message() (+36 more)

### Community 43 - "Human Review Gate"
Cohesion: 0.25
Nodes (4): support CLI, Support Workspace UI Plan, Review API, Workspace UI Verification

### Community 44 - "compilerOptions"
Cohesion: 0.12
Nodes (16): compilerOptions, allowImportingTsExtensions, erasableSyntaxOnly, lib, module, moduleDetection, noEmit, noFallthroughCasesInSwitch (+8 more)

### Community 46 - "DraftContext"
Cohesion: 0.09
Nodes (14): _Execution, _ModelUsage, DraftContext, Completion and review record — 2026-10-17, Execution handoff, File map and shared interfaces, Global Constraints, Plan 3 RAG Drafting Implementation Plan (+6 more)

### Community 47 - "compilerOptions"
Cohesion: 0.12
Nodes (16): compilerOptions, allowImportingTsExtensions, erasableSyntaxOnly, lib, module, moduleDetection, noEmit, noFallthroughCasesInSwitch (+8 more)

### Community 48 - "support_test"
Cohesion: 0.08
Nodes (26): index_deadlines(), support_test(), Evidence by layer, Known limitations and remaining work, Repeatable local walkthrough, Synthetic demo readiness, Completion audit — 2026-10-18, Customer Conversation Intake Implementation Plan (+18 more)

### Community 57 - "parse_document"
Cohesion: 0.10
Nodes (30): TextChunk, _append_chunks(), _check_extracted_size(), DocumentParseError, parse_document(), _parse_pdf(), make_pdf(), test_arabic_text_and_bom_are_preserved() (+22 more)

### Community 58 - "investigation.py"
Cohesion: 0.19
Nodes (13): parse_dt(), DraftToolInputError, _datetime(), _days(), _field(), _involves(), _phone(), _phones() (+5 more)

### Community 59 - "intake/repository.py"
Cohesion: 0.16
Nodes (21): Base, CustomerReview, Receipt, ReviewSnapshot, IntakeAttachmentRow, IntakeMessageRow, IntakeOperationRow, IntakeSessionRow (+13 more)

### Community 60 - "guardrails.py"
Cohesion: 0.06
Nodes (57): Candidate, _add(), find_candidates(), normalize_phone(), _overlaps(), parse_amount(), resolve_date(), _safe_date() (+49 more)

### Community 61 - "NewBatchPage.tsx"
Cohesion: 0.24
Nodes (12): Tabs(), TabsContent(), TabsList(), tabsListVariants, TabsTrigger(), Textarea(), exampleTickets, NewBatchPage() (+4 more)

### Community 62 - "lookup.py"
Cohesion: 0.16
Nodes (15): TxnRecord, _as_date(), InMemoryTransactionRepo, _iqd_amount(), match_transaction(), TransactionRepo, _ex(), _match() (+7 more)

### Community 63 - "test_llm.py"
Cohesion: 0.10
Nodes (13): GeminiStructuredLLM, Sample, make_draft_model(), make_gemini_llm(), _llm(), _S, test_draft_model_uses_millisecond_timeout_and_disables_sdk_retries(), test_openrouter_reported_cost_takes_precedence_over_token_estimate() (+5 more)

### Community 64 - "tasks"
Cohesion: 0.12
Nodes (16): dependsOn, inputs, outputs, cache, persistent, dependsOn, dependsOn, $schema (+8 more)

### Community 65 - "TicketReviewPage.tsx"
Cohesion: 0.13
Nodes (33): Task 8: Employee evidence panel and processing state, Confidence(), Badge(), badgeVariants, Card(), CardContent(), CardHeader(), CardTitle() (+25 more)

### Community 66 - "IntakePage.tsx"
Cohesion: 0.14
Nodes (19): Global Constraints, Intake Chat UI Implementation Plan, Task 1: Put the summary and receipt in the thread, Task 2: Put screenshots inside the composer, Task 3: Apply the workspace chat styles, Task 4: Check the page in the browser, 4. Components, ChatTranscript() (+11 more)

### Community 67 - "test_handoff.py"
Cohesion: 0.31
Nodes (7): complete_conversation(), _dated(), _message(), _opening(), _png(), _review(), _user()

### Community 68 - "PipelineState"
Cohesion: 0.11
Nodes (15): DraftResult, RagDrafter, Drafter, DraftExecutionError, NullDrafter, UnavailableDrafter, draft(), test_real_search_fault_carries_safe_draft_execution_error() (+7 more)

### Community 69 - "UploadedDocument"
Cohesion: 0.15
Nodes (12): UploadedDocument, DocumentValidationError, store_document(), KnowledgeDocumentIndex, ingest_one(), ingest_paths(), ingest_status(), retry_ids() (+4 more)

### Community 70 - "PipelineState"
Cohesion: 0.20
Nodes (8): _Nodes, PipelineState, Global Constraints, Task 1: Sentence catalog, Ticket Flow Charts Implementation Plan, 3. What the employee sees, 4. Which step is open, SentenceId

### Community 71 - "attachments.py"
Cohesion: 0.13
Nodes (14): _display_name(), IntakeError, OperationConflict, StaleReview, TurnBusy, assert_same_operation(), new_access_token(), operation_fingerprint() (+6 more)

### Community 72 - "load_taxonomy"
Cohesion: 0.22
Nodes (4): load_taxonomy(), tax(), taxonomy(), taxonomy()

### Community 73 - "Credentials"
Cohesion: 0.34
Nodes (3): Credentials, SessionView, IntakeService

### Community 74 - "lib/types.ts"
Cohesion: 0.11
Nodes (27): acceptIndexRequest(), canRequestIndex(), PendingIndexes, persistPendingIndexes(), pollKnowledge(), refresh(), stop(), PollOptions (+19 more)

### Community 75 - "test-kb/README.md"
Cohesion: 0.27
Nodes (3): Fictional RAG walkthrough inputs, مشاكل البطاقة — سياسة خيالية للعرض التجريبي, استرجاع مبلغ شراء — سياسة خيالية للعرض التجريبي

### Community 76 - "Plan 3 — Knowledge retrieval and grounded reply drafting"
Cohesion: 0.12
Nodes (15): 10. Remaining demo roadmap, 1. Intent and acceptance criteria, 3. Provider and configuration, 4. Knowledge ingestion and persistence, 5. Retrieval and evidence, 7. Draft guardrails and failure outcomes, 8. Pipeline, API, CLI and UI integration, 9. Demo policies and verification (+7 more)

### Community 77 - "build_pipeline"
Cohesion: 0.14
Nodes (17): build_pipeline(), ConfigError, make_jev_client(), GeminiAnalysis, FakeStructuredLLM, ScriptedChat, _settings(), test_all_modes_use_credential_checker_independently_of_classifier() (+9 more)

### Community 79 - "devDependencies"
Cohesion: 0.12
Nodes (16): devDependencies, eslint, @eslint/js, eslint-plugin-react-hooks, eslint-plugin-react-refresh, globals, prettier, prettier-plugin-tailwindcss (+8 more)

### Community 80 - "judge-demo.ar.md"
Cohesion: 0.14
Nodes (13): أعطال التطبيق — سياسة خيالية للعرض التجريبي, استرجاع مبلغ شراء — سياسة خيالية للعرض التجريبي, استعادة الدخول — سياسة خيالية للعرض التجريبي, الاستفسار الآمن من الدعم — سياسة خيالية للعرض التجريبي, الاستفسار المؤقت للدعم في المهمة ٨ — سياسة خيالية للعرض التجريبي, التحويل المعلّق — سياسة خيالية للعرض التجريبي, التحويل لمستلم بالخطأ — سياسة خيالية للعرض التجريبي, الطلبات غير الواضحة وخارج النطاق — سياسة خيالية للعرض التجريبي (+5 more)

### Community 93 - "pipeline/contracts.py"
Cohesion: 0.09
Nodes (35): LLMUnavailable, StructuredLLM, Candidates, ClassificationResult, ClassifierOutput, FieldPick, NormalizedTicket, Classifier (+27 more)

### Community 94 - "devDependencies"
Cohesion: 0.11
Nodes (19): devDependencies, eslint, @eslint/js, eslint-plugin-react-hooks, eslint-plugin-react-refresh, globals, jsdom, @tailwindcss/vite (+11 more)

### Community 95 - "devDependencies"
Cohesion: 0.14
Nodes (14): devDependencies, eslint, @eslint/js, eslint-plugin-react-hooks, eslint-plugin-react-refresh, globals, tailwindcss, @tailwindcss/vite (+6 more)

### Community 96 - "json"
Cohesion: 0.17
Nodes (12): load_jsonl(), load_tickets(), _rows(), outcome_to_dict(), outcome_to_row(), test_csv_with_bom_and_missing_columns(), test_duplicate_external_ids_keep_first(), test_json_object_without_ids() (+4 more)

### Community 97 - "ticket-flow.ts"
Cohesion: 0.10
Nodes (41): Task 2: Which step is open, Task 3: Received, produced, and drafting events, Task 4: Mermaid source, Task 5: Draw the charts on the ticket page, buttonVariants, buildTicketFlow(), AR, channelName() (+33 more)

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

### Community 106 - "agent.py"
Cohesion: 0.24
Nodes (8): _Flag, _History, _Input, _Knowledge, _Lookup, _Recent, _Search, _Service

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

### Community 114 - "Settings"
Cohesion: 0.12
Nodes (10): Settings, test_blank_intake_model_is_rejected(), test_non_positive_image_limit_is_rejected(), test_relative_upload_directory_is_rooted_in_the_repository(), test_defaults(), test_drafting_configuration_cannot_bypass_hard_limits(), test_drafting_limits_load_from_environment(), test_env_overrides() (+2 more)

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

### Community 119 - "jev.py"
Cohesion: 0.25
Nodes (9): build_order_check(), build_questions(), build_state(), category_criteria(), _input_tokens(), JevClassifier, _picks(), _priority() (+1 more)

### Community 120 - "scripts"
Cohesion: 0.50
Nodes (4): scripts, format, lint, typecheck

### Community 122 - "context"
Cohesion: 0.22
Nodes (16): Question, Readiness, _asked_already(), asks_for_secret(), assess_readiness(), _can_ask(), canonical_category(), choose_question() (+8 more)

### Community 123 - "TurnContext"
Cohesion: 0.22
Nodes (5): QuestionRecord, TurnContext, IntakeGraph, _invitation(), Shared contracts (implement in Task 1; extend only through explicit edits here)

### Community 124 - "attachments.py"
Cohesion: 0.12
Nodes (22): AttachmentStore, ImageRejected, NotOwned, initial_state(), IntakeRepository, make_intake_service(), builder(), png_bytes() (+14 more)

### Community 125 - "test_cli.py"
Cohesion: 0.18
Nodes (9): test_config_error_exits_2(), boom(), test_ingest_directory_is_deterministic_and_duplicate_is_free(), test_ingest_disabled_configuration_never_calls_provider(), test_ingest_failure_exit_and_retry_stored(), test_ingest_invalid_source_does_not_stop_other_files(), test_ingest_limits_batch_without_partial_side_effects(), test_retry_stored_indexes_old_uploads_without_recovering_other_process_jobs() (+1 more)

### Community 126 - "intake/contracts.py"
Cohesion: 0.15
Nodes (8): Attachment, _aware(), IntakeModel, IntakeState, Message, grounded_analysis(), grounded_review(), ScriptedIntakeModel

### Community 127 - "InvalidEvidence"
Cohesion: 0.19
Nodes (14): ReviewText, build_review(), _compact(), _render_value(), _ticket_text(), _tokens(), validate_review_numbers(), review() (+6 more)

### Community 128 - "Ticket flow charts"
Cohesion: 0.22
Nodes (8): 1. Outcome, 2. Scope, 5. Language, 6. How a result becomes the charts, 7. Sentences, 8. Tests, 9. Files, Ticket flow charts

### Community 129 - "intake/model.py"
Cohesion: 0.11
Nodes (27): ImageInput, ModelCall, ModelUnavailable, _analysis_prompt(), _bounded_context(), _guard_size(), ModelBudget, OpenRouterIntakeModel (+19 more)

### Community 130 - "RunRow"
Cohesion: 0.31
Nodes (8): get_run(), list_runs(), start_run(), RunRow, model_ids(), run_job(), run_view(), Task 5: Exactly-once submission and durable employee visibility

### Community 131 - "intake.py"
Cohesion: 0.16
Nodes (20): create_session(), _credentials(), _dump(), get_session(), post_message(), read_attachment(), remove_attachment(), request_review() (+12 more)

### Community 132 - "KnowledgeService"
Cohesion: 0.09
Nodes (11): Embedder, _abandoned(), _Claim, _error_cost(), KnowledgeError, KnowledgeExecutionError, KnowledgeService, test_failed_reindex_keeps_previous_chunks_atomically_and_is_retryable() (+3 more)

### Community 133 - "_DatabaseCall"
Cohesion: 0.17
Nodes (3): _check_deadline(), _consume(), _DatabaseCall

### Community 134 - "test_recovery_regressions.py"
Cohesion: 0.30
Nodes (10): command(), create(), test_actual_app_restart_reconciles_failed_placeholder(), test_failed_review_retry_cannot_reopen_submitted_session(), test_original_payload_identity_survives_sanitization(), test_publication_failure_is_retryable_without_restart(), fail_once(), test_receipt_reference_is_preserved() (+2 more)

### Community 135 - "_bounded"
Cohesion: 0.22
Nodes (6): DraftAlreadySubmitted, _bounded(), visit(), guarded(), invoke(), _json()

### Community 136 - "intake/conftest.py"
Cohesion: 0.12
Nodes (14): init_db(), make_engine(), make_sessionmaker(), reset_db(), lifespan(), intake_client(), intake_db(), reviewed() (+6 more)

### Community 138 - "intake/api.ts"
Cohesion: 0.15
Nodes (13): createIntakeApi(), IntakeRequestError, isRecord(), parseJson(), parseReceipt(), parseSession(), readError(), stringList() (+5 more)

### Community 140 - "test_dbapi_commit_handoff_arbitrates_cancellation"
Cohesion: 0.47
Nodes (4): test_dbapi_commit_handoff_arbitrates_cancellation(), gate(), gate_before_dbapi(), gate_inside_dbapi()

### Community 144 - "FakeJevRunnable"
Cohesion: 0.32
Nodes (10): FakeJevRunnable, _criteria(), _run(), test_low_top_probability_is_uncertain(), test_one_main_call_with_all_questions(), test_order_check_uses_reversed_options(), test_order_disagreement_is_uncertain(), test_priority_level_maps_to_p_label() (+2 more)

### Community 155 - "IntakePage.test.tsx"
Cohesion: 0.26
Nodes (10): Task 6: Customer API client and resumable UI state, Task 7: Bilingual customer chat, screenshots and reviewed submission, copy(), attachment, collectingController(), emptySession(), fakeApi(), readyController() (+2 more)

### Community 156 - "employee-frontend/src/components/theme-provider.tsx"
Cohesion: 0.21
Nodes (11): disableTransitionsTemporarily(), getSystemTheme(), isEditableTarget(), isTheme(), ResolvedTheme, Theme, THEME_VALUES, ThemeProvider() (+3 more)

### Community 158 - "rules.py"
Cohesion: 0.12
Nodes (24): Decision, ExtractedField, LookupResult, decide(), empty_ticket_decision(), merge_reasons(), note_for(), _unique() (+16 more)

### Community 159 - "trace-facts.ts"
Cohesion: 0.21
Nodes (13): save(), classifySentence(), FIELD_LABELS, fieldValue(), LOOKUP, quoted(), record(), stageFacts() (+5 more)

### Community 161 - "Customer intake chat layout"
Cohesion: 0.33
Nodes (5): 1. Outcome, 2. Scope, 3. Layout, 5. Checks, Customer intake chat layout

## Ambiguous Edges - Review These
- `Fraud Report` → `Plan 1 Live Smoke`  [AMBIGUOUS]
  README.md · relation: conceptually_related_to

## Knowledge Gaps
- **90 isolated node(s):** `zaincash-support`, `@base-ui/react`, `@fontsource-variable/plus-jakarta-sans`, `@fontsource/tajawal`, `@tailwindcss/vite` (+85 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 998 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **48 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `HTTP contract (implemented in Tasks 4–5)` connect `attachments.py` to `intake/model.py`, `RunRow`, `TurnStore`, `TicketReviewPage.tsx`, `intake/conftest.py`, `support_test`, `IntakePage.test.tsx`, `guardrails.py`?**
  _High betweenness centrality (0.102) - this node is a cross-community bridge._
- **Are the 33 inferred relationships involving `Settings` (e.g. with `_command_settings()` and `_run_in_memory()`) actually correct?**
  _`Settings` has 33 INFERRED edges - model-reasoned connections that need verification._
- **What connects `zaincash-support`, `@base-ui/react`, `@fontsource-variable/plus-jakarta-sans` to the rest of the system?**
  _90 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `agent.py` be split into smaller, more focused modules?**
  _Cohesion score 0.061683599419448475 - nodes in this community are weakly interconnected._
- **Why does `Settings` connect `Settings` to `agent.py`, `intake/model.py`, `RunRow`, `pytest`, `KnowledgeService`, `intake/conftest.py`, `test_rag_api.py`, `fixture`, `make_output`, `.__init__`, `main.py`, `test_workspace_api.py`, `test_embeddings.py`, `test_draft_tools.py`, `test_kb_service.py`, `asyncio`, `fact`, `DraftContext`, `support_test`, `intake/repository.py`, `test_llm.py`, `PipelineState`, `attachments.py`, `load_taxonomy`, `build_pipeline`, `test_final_fix_handoff.py`, `attachments.py`, `test_cli.py`?**
  _High betweenness centrality (0.080) - this node is a cross-community bridge._
- **Are the 24 inferred relationships involving `KnowledgeService` (e.g. with `Settings` and `UploadedDocument`) actually correct?**
  _`KnowledgeService` has 24 INFERRED edges - model-reasoned connections that need verification._

### Low-confidence Hints
_AMBIGUOUS edges — the extractor was unsure. Verify before acting on these._

- **What is the exact relationship between `Fraud Report` and `Plan 1 Live Smoke`?**
  _Edge tagged AMBIGUOUS (relation: conceptually_related_to) - confidence is low._