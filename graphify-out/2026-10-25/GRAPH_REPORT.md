# Graph Report - zaincash-support  (2026-10-25)

## Corpus Check
- 305 files · ~252,669 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 30 file(s) not represented in the graph (top: (none) 18, .jsonl 4, .css 4)

## Summary
- 3059 nodes · 9447 edges · 170 communities (129 shown, 41 thin omitted)
- Extraction: 89% EXTRACTED · 11% INFERRED · 0% AMBIGUOUS · INFERRED: 1046 edges (avg confidence: 0.93)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `244e23ff`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- stage6_draft/model.py
- intake/types.ts
- pytest
- TurnStore
- test_draft_guardrails.py
- tools.py
- QueuePage.tsx
- Customer conversation intake for ZainCash support
- ref_vitest
- IntakeController
- FakeJevRunnable
- test_rag_api.py
- employee-frontend/package.json
- intake/contracts.py
- Support Taxonomy Categories
- ui/package.json
- employee-frontend/src/App.tsx
- users-frontend/package.json
- make_output
- UploadedDocument
- web/package.json
- test_recovery_regressions.py
- compilerOptions
- employee-frontend/components.json
- EmbeddingError
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
- fakes.py
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
- IntakeRepository
- intake/repository.py
- main.py
- NewBatchPage.tsx
- investigation.py
- test_llm.py
- tasks
- useCopy
- IntakePage.tsx
- test_handoff.py
- PipelineState
- datetime
- normalize.py
- intake/conftest.py
- lookup.py
- Credentials
- lib/types.ts
- test-kb/README.md
- db/repository.py
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
- FakeJevRunnable
- devDependencies
- devDependencies
- guardrails.py
- ticket-flow.ts
- review.py
- compilerOptions
- قواعد المعرفة العربية للعرض أمام لجنة التحكيم
- pydantic
- dependencies
- InvalidEvidence
- dependencies
- compilerOptions
- pipeline/graph.py
- controller.test.ts
- test_final_fix_handoff.py
- ZainCash Support Workspace
- negative/README.md
- scripts
- scripts
- compilerOptions
- _DatabaseCall
- dependencies
- web/tsconfig.json
- employee-frontend/tsconfig.json
- exports
- response_payload
- scripts
- users-frontend/README.md
- context
- TurnContext
- AttachmentStore
- ar/failed_transfer.md
- workspace-ui.tsx
- test_gemini.py
- health
- intake/model.py
- RagDrafter
- intake.py
- IntakePage.test.tsx
- KnowledgeService
- cli.py
- Customer Conversation Intake Implementation Plan
- main.py
- ingest.py
- intake/api.ts
- DraftContext
- kb/service.py
- test_cli.py
- KnowledgeDocumentIndex
- @testing-library/react
- LLMUnavailable
- components-ai-thought-chain.tsx
- submission.py
- intake/README.md
- errors.py
- Customer intake verification — 2026-10-18
- knowledge.py
- test_workspace_api.py
- ErrorEmbedder
- employee-frontend/src/components/theme-provider.tsx
- index_deadlines
- load_taxonomy
- runs.py
- TicketOutcome
- Customer intake chat layout
- bill-payment-biller-notice.md
- ar/other.md
- test_draft_model.py
- Ticket flow charts
- KnowledgePage
- call
- task8-history-policy.md
- collapsible.tsx

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
- `7. Draft guardrails and failure outcomes` --references--> `requests_credentials()`  [INFERRED]
  docs/superpowers/specs/2026-10-17-plan3-rag-drafting-design.md → backend/app/pipeline/stage6_draft/guardrails.py
- `Task 8: Demo corpus, full verification and readiness record` --references--> `support_test()`  [INFERRED]
  docs/superpowers/plans/2026-10-17-plan3-rag-drafting.md → backend/tests/test_kb_service.py

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **Cascade Classification Path** — docs_superpowers_specs_2026_10_07_support_pipeline_design_cascade, docs_superpowers_plans_2026_10_07_plan1_core_pipeline_part2_jev_classifier, docs_superpowers_plans_2026_10_07_plan1_core_pipeline_part2_gemini_classifier, docs_superpowers_plans_2026_10_07_plan1_core_pipeline_part2_cascade_combine, readme_human_approval [EXTRACTED 1.00]
- **Drafting Agent Toolset** — backend_app_pipeline_runner_lookup_transaction, backend_app_pipeline_runner_search_transactions, backend_app_pipeline_runner_get_customer_recent_transactions, backend_app_pipeline_runner_get_customer_ticket_history, backend_app_pipeline_runner_check_service_status, backend_app_pipeline_runner_search_knowledge_base, backend_app_pipeline_runner_flag_for_human, backend_app_pipeline_runner_submit_draft [EXTRACTED 1.00]
- **Ticket Processing Stage Flow** — backend_app_pipeline_runner_prepare, backend_app_pipeline_runner_jev_classify, backend_app_pipeline_runner_gemini_classify, backend_app_pipeline_runner_extract, backend_app_pipeline_runner_lookup, backend_app_pipeline_runner_decide, backend_app_pipeline_runner_draft [EXTRACTED 1.00]

## Communities (170 total, 41 thin omitted)

### Community 1 - "intake/types.ts"
Cohesion: 0.12
Nodes (20): IntakeApi, ControllerState, emptyState(), fileIdentity(), Credentials, EvidenceRef, Fact, IntakeMessage (+12 more)

### Community 2 - "pytest"
Cohesion: 0.21
Nodes (33): test_contracts_reject_extra_keys(), test_datetimes_must_be_timezone_aware(), answer(), draft_state(), script(), drafter(), events(), test_callback_partial_response_and_error_cost_are_alternatives() (+25 more)

### Community 3 - "TurnStore"
Cohesion: 0.17
Nodes (12): OperationClaim, TurnResult, RevisionConflict, sanitize_intake_text(), _jsonable(), TurnStore, test_stale_attempt_audit_is_retained_once_with_attempt_identity(), repo() (+4 more)

### Community 4 - "test_draft_guardrails.py"
Cohesion: 0.13
Nodes (28): check_draft(), _citation_findings(), requests_credentials(), check(), state(), test_aggregation_is_deduplicated_and_has_no_state_side_effects(), test_amount_occurrences_keep_their_own_currency_and_sign(), test_avoid_sharing_warning_does_not_excuse_a_later_request() (+20 more)

### Community 5 - "tools.py"
Cohesion: 0.07
Nodes (19): DraftAlreadySubmitted, DraftSubmission, DraftToolLimit, build_tools(), flag(), guarded(), invoke(), retrieve() (+11 more)

### Community 6 - "QueuePage.tsx"
Cohesion: 0.18
Nodes (35): Confidence(), EmptyState(), ErrorState(), LoadingState(), PageHeader(), PriorityBadge(), StatusBadge(), Table() (+27 more)

### Community 7 - "Customer conversation intake for ZainCash support"
Cohesion: 0.07
Nodes (28): 10. Verification and acceptance criteria, 11. Delivery and review, 1. Outcome and agreed requirements, 2. Current implementation and integration points, 3. Approach and boundaries, 4. Conversation state and turn flow, 5. Facts, evidence, and readiness, 6. Language and screenshot behavior (+20 more)

### Community 8 - "ref_vitest"
Cohesion: 0.22
Nodes (7): intakeFixture, factValue(), IntakeEvidence(), Screenshot(), canReview(), REVIEWABLE, IntakeEvidenceData

### Community 9 - "IntakeController"
Cohesion: 0.19
Nodes (5): IntakeController, isConflict(), isOffline(), safeMessage(), Language

### Community 10 - "FakeJevRunnable"
Cohesion: 0.13
Nodes (18): CredentialCheck, DegradedCredentialChecker, _finite_nonnegative(), _get(), JevCredentialChecker, ResponseRunnable, test_bad_usage_cannot_poison_cost(), test_cancellation_propagates_with_cost_for_outer_timeout_owner() (+10 more)

### Community 11 - "test_rag_api.py"
Cohesion: 0.15
Nodes (18): client(), evidence_client(), kb_env(), test_actual_guardrail_failure_is_separate_from_reply(), test_concurrent_index_requests_share_active_work(), test_disabled_or_missing_provider_stores_without_indexing(), test_explicit_retry_tags_search_and_chunk_pagination(), test_health_distinguishes_failed_from_empty() (+10 more)

### Community 12 - "employee-frontend/package.json"
Cohesion: 0.06
Nodes (31): @base-ui/react, class-variance-authority, cn, eslint, @eslint/js, eslint-plugin-react-hooks, eslint-plugin-react-refresh, @fontsource/tajawal (+23 more)

### Community 14 - "intake/contracts.py"
Cohesion: 0.15
Nodes (9): _aware(), IntakeModel, IntakeState, Message, Readiness, grounded_analysis(), grounded_review(), image_evidence() (+1 more)

### Community 15 - "Support Taxonomy Categories"
Cohesion: 0.21
Nodes (22): lookup, Account KYC, Account & Security, Agent Dispute, Agent Network, App Bug, Bill Payment, Card Issue (+14 more)

### Community 16 - "ui/package.json"
Cohesion: 0.07
Nodes (29): @turbo/gen, zod, @base-ui/react, class-variance-authority, cn, eslint, @eslint/js, eslint-plugin-react-hooks (+21 more)

### Community 17 - "employee-frontend/src/App.tsx"
Cohesion: 0.10
Nodes (25): App(), EvaluationPage, InsightsPage, KnowledgePage, NewBatchPage, QueuePage, RunDetailPage, RunsPage (+17 more)

### Community 18 - "users-frontend/package.json"
Cohesion: 0.09
Nodes (22): turbo, devDependencies, prettier, prettier-plugin-tailwindcss, turbo, typescript, engines, node (+14 more)

### Community 19 - "make_output"
Cohesion: 0.26
Nodes (20): FakeClassifier, make_output(), make_ticket(), _deps(), _run(), test_cascade_confident_jev_skips_gemini(), test_cascade_degrades_when_jev_fails(), test_cascade_uncertain_jev_goes_to_gemini() (+12 more)

### Community 20 - "UploadedDocument"
Cohesion: 0.19
Nodes (12): UploadedDocument, document_filename(), document_view(), DocumentValidationError, store_document(), KnowledgeDocumentIndex, ingest_one(), ingest_status() (+4 more)

### Community 21 - "web/package.json"
Cohesion: 0.08
Nodes (25): jsdom, @testing-library/user-event, @workspace/ui, eslint, @eslint/js, eslint-plugin-react-hooks, eslint-plugin-react-refresh, globals (+17 more)

### Community 22 - "test_recovery_regressions.py"
Cohesion: 0.44
Nodes (8): command(), create(), test_failed_review_retry_cannot_reopen_submitted_session(), test_original_payload_identity_survives_sanitization(), test_publication_failure_is_retryable_without_restart(), fail_once(), test_receipt_reference_is_preserved(), test_superseded_failed_operation_cannot_be_retried()

### Community 23 - "compilerOptions"
Cohesion: 0.08
Nodes (23): compilerOptions, allowArbitraryExtensions, allowImportingTsExtensions, erasableSyntaxOnly, jsx, lib, module, moduleDetection (+15 more)

### Community 24 - "employee-frontend/components.json"
Cohesion: 0.09
Nodes (21): aliases, components, hooks, lib, ui, utils, iconLibrary, menuAccent (+13 more)

### Community 25 - "EmbeddingError"
Cohesion: 0.12
Nodes (11): Embedder, EmbeddingBatch, SearchResult, EmbeddingError, _nonnegative_number(), _ordered_vectors(), _response_cost(), Embeddings (+3 more)

### Community 26 - "compilerOptions"
Cohesion: 0.09
Nodes (22): compilerOptions, allowArbitraryExtensions, allowImportingTsExtensions, erasableSyntaxOnly, jsx, lib, module, moduleDetection (+14 more)

### Community 27 - "web/src/components/theme-provider.tsx"
Cohesion: 0.17
Nodes (12): App(), disableTransitionsTemporarily(), getSystemTheme(), isEditableTarget(), isTheme(), ResolvedTheme, Theme, THEME_VALUES (+4 more)

### Community 28 - "test_embeddings.py"
Cohesion: 0.17
Nodes (18): OpenRouterEmbedder, settings(), test_33_inputs_are_batched_and_each_batch_maps_its_own_indexes(), test_billed_batch_cost_survives_cancellation_without_cross_call_leakage(), test_cancellation_propagates_to_the_callers_deadline(), test_empty_input_returns_empty_batch_without_a_request(), unexpected_request(), test_invalid_rag_settings_are_rejected() (+10 more)

### Community 29 - "Classify and Extract Prompts"
Cohesion: 0.31
Nodes (9): extract, gemini_classify, Pipeline Graph Orchestration, jev_classify, prepare, Gemini Classify Prompt v1, Gemini Extract Prompt v1, GeminiClassifier (+1 more)

### Community 30 - "test_draft_tools.py"
Cohesion: 0.13
Nodes (28): IncidentRow, TransactionRow, api(), settings(), test_all_eight_tools_and_seven_parallel_calls_execute_only_six(), test_context_copies_input_and_rejects_raising_hard_call_limit(), test_database_faults_remain_distinct_and_record_paid_search_cost(), test_discovered_ref_can_be_inspected_but_not_promoted_to_match() (+20 more)

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
Nodes (22): IndexAttemptLostError, GatedEmbedder, LateEmbedder, PaidEmbedder, count_chunks(), test_competing_callers_refuse_active_attempt_and_release_transactions(), test_db_deadline_cancelled_publication_cannot_commit_late(), test_db_deadline_is_cumulative_across_publication_statements() (+14 more)

### Community 36 - "web/components.json"
Cohesion: 0.10
Nodes (19): aliases, components, hooks, lib, ui, utils, iconLibrary, menuAccent (+11 more)

### Community 38 - "fakes.py"
Cohesion: 0.13
Nodes (24): StructuredLLM, Candidates, ClassificationResult, ClassifierOutput, FieldPick, NormalizedTicket, Classifier, FieldExtractor (+16 more)

### Community 39 - "ui/components.json"
Cohesion: 0.10
Nodes (19): aliases, components, hooks, lib, ui, utils, iconLibrary, menuAccent (+11 more)

### Community 40 - "Settings"
Cohesion: 0.11
Nodes (10): Settings, test_blank_intake_model_is_rejected(), test_non_positive_image_limit_is_rejected(), test_relative_upload_directory_is_rooted_in_the_repository(), test_defaults(), test_drafting_configuration_cannot_bypass_hard_limits(), test_drafting_limits_load_from_environment(), test_env_overrides() (+2 more)

### Community 41 - "fact"
Cohesion: 0.26
Nodes (28): Attachment, EvidenceRef, InvalidEvidence, merge_analysis(), checked_update(), remove_attachment_evidence(), context(), fact() (+20 more)

### Community 43 - "Human Review Gate"
Cohesion: 0.25
Nodes (4): support CLI, Support Workspace UI Plan, Review API, Workspace UI Verification

### Community 44 - "compilerOptions"
Cohesion: 0.12
Nodes (16): compilerOptions, allowImportingTsExtensions, erasableSyntaxOnly, lib, module, moduleDetection, noEmit, noFallthroughCasesInSwitch (+8 more)

### Community 46 - "agent.py"
Cohesion: 0.19
Nodes (8): _Nodes, PipelineState, Global Constraints, Task 1: Sentence catalog, Ticket Flow Charts Implementation Plan, 3. What the employee sees, 4. Which step is open, SentenceId

### Community 47 - "compilerOptions"
Cohesion: 0.12
Nodes (16): compilerOptions, allowImportingTsExtensions, erasableSyntaxOnly, lib, module, moduleDetection, noEmit, noFallthroughCasesInSwitch (+8 more)

### Community 48 - "support_test"
Cohesion: 0.12
Nodes (18): ingest(), support_test(), Evidence by layer, Known limitations and remaining work, Repeatable local walkthrough, Synthetic demo readiness, Execution conventions and repository baseline, Artifacts, servers and remaining concerns (+10 more)

### Community 57 - "parse_document"
Cohesion: 0.11
Nodes (29): TextChunk, _append_chunks(), _check_extracted_size(), DocumentParseError, parse_document(), _parse_pdf(), make_pdf(), test_arabic_text_and_bom_are_preserved() (+21 more)

### Community 58 - "IntakeRepository"
Cohesion: 0.14
Nodes (4): IntakeRepository, make_intake_service(), builder(), repo()

### Community 59 - "intake/repository.py"
Cohesion: 0.15
Nodes (20): _display_name(), CustomerReview, IntakeAttachmentRow, IntakeMessageRow, IntakeSessionRow, assert_same_operation(), _attachment(), customer_review() (+12 more)

### Community 60 - "main.py"
Cohesion: 0.12
Nodes (13): RunRow, recover(), run_job(), fail_intake_placeholders(), reconcile_intake_run(), recover_intake_processing(), dispatch_intake(), test_review_to_employee_handoff() (+5 more)

### Community 61 - "NewBatchPage.tsx"
Cohesion: 0.12
Nodes (17): badgeVariants, Input(), Tabs(), TabsContent(), TabsList(), tabsListVariants, TabsTrigger(), Textarea() (+9 more)

### Community 62 - "investigation.py"
Cohesion: 0.18
Nodes (14): TxnRecord, parse_dt(), DraftToolInputError, _datetime(), _days(), _field(), _involves(), _phone() (+6 more)

### Community 63 - "test_llm.py"
Cohesion: 0.11
Nodes (12): GeminiStructuredLLM, Sample, make_gemini_llm(), _llm(), _S, test_draft_model_uses_millisecond_timeout_and_disables_sdk_retries(), test_openrouter_reported_cost_takes_precedence_over_token_estimate(), test_openrouter_retry_budget_is_bounded() (+4 more)

### Community 64 - "tasks"
Cohesion: 0.12
Nodes (16): dependsOn, inputs, outputs, cache, persistent, dependsOn, dependsOn, $schema (+8 more)

### Community 65 - "useCopy"
Cohesion: 0.16
Nodes (28): 6. How a result becomes the charts, Metric(), Badge(), Card(), CardContent(), CardHeader(), CardTitle(), EvaluationPage() (+20 more)

### Community 66 - "IntakePage.tsx"
Cohesion: 0.13
Nodes (22): Global Constraints, Intake Chat UI Implementation Plan, Task 1: Put the summary and receipt in the thread, Task 2: Put screenshots inside the composer, Task 3: Apply the workspace chat styles, Task 4: Check the page in the browser, 4. Components, ChatTranscript() (+14 more)

### Community 67 - "test_handoff.py"
Cohesion: 0.19
Nodes (20): Analysis, test_reinspection_keeps_current_images_and_new_observations(), again(), initial(), test_validation_failure_retains_usage_audit(), ainvoke(), _amount(), analyze() (+12 more)

### Community 68 - "PipelineState"
Cohesion: 0.08
Nodes (23): DraftResult, Drafter, NullDrafter, UnavailableDrafter, 10. Remaining demo roadmap, 1. Intent and acceptance criteria, 2. Current implementation and integration points, 3. Provider and configuration (+15 more)

### Community 69 - "datetime"
Cohesion: 0.18
Nodes (15): get_result(), list_results(), read_intake_attachment(), review_result(), ReviewInput, ReviewRow, TicketResultRow, IntakeSubmissionRow (+7 more)

### Community 70 - "normalize.py"
Cohesion: 0.22
Nodes (16): detect_arabizi(), fold_arabic(), has_latin_mix(), _latin_words(), mask_cards(), normalize(), sanitize_for_storage(), test_arabizi_detection() (+8 more)

### Community 71 - "intake/conftest.py"
Cohesion: 0.13
Nodes (13): build_graph(), PipelineDeps, InMemoryTransactionRepo, load_taxonomy(), tax(), intake_client(), pipeline(), taxonomy() (+5 more)

### Community 72 - "lookup.py"
Cohesion: 0.16
Nodes (15): _as_date(), _iqd_amount(), match_transaction(), TransactionRepo, txn_from_dict(), _ex(), _match(), test_ambiguous_then_disambiguated_by_counterpart() (+7 more)

### Community 73 - "Credentials"
Cohesion: 0.17
Nodes (7): Credentials, SessionView, IntakeService, _payload(), test_concurrent_submit_dispatches_once(), test_second_request_id_reuses_the_approved_review(), test_submission_replay_creates_one_ticket()

### Community 74 - "lib/types.ts"
Cohesion: 0.10
Nodes (33): acceptIndexRequest(), canRequestIndex(), PendingIndexes, persistPendingIndexes(), pollKnowledge(), refresh(), stop(), PollOptions (+25 more)

### Community 75 - "test-kb/README.md"
Cohesion: 0.09
Nodes (11): Fictional RAG walkthrough inputs, توثيق الحساب — سياسة خيالية للعرض التجريبي, نزاع مع وكيل — سياسة خيالية للعرض التجريبي, أعطال التطبيق — سياسة خيالية للعرض التجريبي, دفع الفواتير — سياسة خيالية للعرض التجريبي, مشاكل البطاقة — سياسة خيالية للعرض التجريبي, تصعيد شبهة الاحتيال — سياسة خيالية للعرض التجريبي, الاستفسار الآمن من الدعم — سياسة خيالية للعرض التجريبي (+3 more)

### Community 76 - "db/repository.py"
Cohesion: 0.19
Nodes (16): TicketRow, create_run(), finish_run(), load_incidents(), load_transactions(), _to_record(), _upsert(), upsert_tickets() (+8 more)

### Community 77 - "build_pipeline"
Cohesion: 0.14
Nodes (21): _run_with_db(), SqlTransactionRepo, build_pipeline(), ConfigError, make_jev_client(), model_ids(), run_batch(), GeminiAnalysis (+13 more)

### Community 79 - "devDependencies"
Cohesion: 0.12
Nodes (16): devDependencies, eslint, @eslint/js, eslint-plugin-react-hooks, eslint-plugin-react-refresh, globals, prettier, prettier-plugin-tailwindcss (+8 more)

### Community 80 - "judge-demo.ar.md"
Cohesion: 0.14
Nodes (13): أعطال التطبيق — سياسة خيالية للعرض التجريبي, استرجاع مبلغ شراء — سياسة خيالية للعرض التجريبي, استعادة الدخول — سياسة خيالية للعرض التجريبي, الاستفسار الآمن من الدعم — سياسة خيالية للعرض التجريبي, الاستفسار المؤقت للدعم في المهمة ٨ — سياسة خيالية للعرض التجريبي, التحويل المعلّق — سياسة خيالية للعرض التجريبي, التحويل لمستلم بالخطأ — سياسة خيالية للعرض التجريبي, الطلبات غير الواضحة وخارج النطاق — سياسة خيالية للعرض التجريبي (+5 more)

### Community 93 - "FakeJevRunnable"
Cohesion: 0.14
Nodes (19): build_order_check(), build_questions(), build_state(), category_criteria(), _input_tokens(), JevClassifier, _picks(), _priority() (+11 more)

### Community 94 - "devDependencies"
Cohesion: 0.11
Nodes (19): devDependencies, eslint, @eslint/js, eslint-plugin-react-hooks, eslint-plugin-react-refresh, globals, jsdom, @tailwindcss/vite (+11 more)

### Community 95 - "devDependencies"
Cohesion: 0.14
Nodes (14): devDependencies, eslint, @eslint/js, eslint-plugin-react-hooks, eslint-plugin-react-refresh, globals, tailwindcss, @tailwindcss/vite (+6 more)

### Community 96 - "guardrails.py"
Cohesion: 0.10
Nodes (27): Candidate, _add(), find_candidates(), normalize_phone(), _overlaps(), parse_amount(), resolve_date(), _safe_date() (+19 more)

### Community 97 - "ticket-flow.ts"
Cohesion: 0.07
Nodes (71): Task 2: Which step is open, Task 3: Received, produced, and drafting events, Task 4: Mermaid source, Task 5: Draw the charts on the ticket page, buildTicketFlow(), AR, channelName(), checkLines() (+63 more)

### Community 98 - "review.py"
Cohesion: 0.19
Nodes (14): ReviewText, build_review(), _compact(), _render_value(), _ticket_text(), _tokens(), validate_review_numbers(), review() (+6 more)

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
Nodes (17): dependencies, @base-ui/react, class-variance-authority, cn, @fontsource/tajawal, @fontsource-variable/plus-jakarta-sans, lucide-react, mermaid (+9 more)

### Community 103 - "InvalidEvidence"
Cohesion: 0.20
Nodes (13): canonical_digits(), normalize_reported_date(), _apply(), _check_reference(), _compact(), _newer_correction(), _normalize_precise(), _own_phone_quote() (+5 more)

### Community 104 - "dependencies"
Cohesion: 0.15
Nodes (13): dependencies, @base-ui/react, class-variance-authority, cn, @fontsource/tajawal, @fontsource-variable/plus-jakarta-sans, @hugeicons/core-free-icons, @hugeicons/react (+5 more)

### Community 105 - "compilerOptions"
Cohesion: 0.17
Nodes (11): compilerOptions, jsx, lib, module, moduleResolution, outDir, skipLibCheck, strict (+3 more)

### Community 106 - "pipeline/graph.py"
Cohesion: 0.11
Nodes (3): _default_retry(), _percentile(), _retryable()

### Community 107 - "controller.test.ts"
Cohesion: 0.21
Nodes (7): controller, emptySession(), fakeApi(), review, browserSessionStorage(), SessionStorage, SavedSession

### Community 108 - "test_final_fix_handoff.py"
Cohesion: 0.09
Nodes (25): Passage, process_batch(), Checker, Knowledge, ScriptedChat, assert_completed_evidence(), faulty_knowledge(), read() (+17 more)

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

### Community 114 - "_DatabaseCall"
Cohesion: 0.17
Nodes (3): _check_deadline(), _consume(), _DatabaseCall

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

### Community 119 - "response_payload"
Cohesion: 0.22
Nodes (16): embedder_for(), item(), response_payload(), respond(), respond(), test_billed_cost_survives_cancellation_during_client_close(), test_billed_response_cost_is_retained_when_its_vectors_are_invalid(), test_cost_uses_one_reported_value_or_configured_token_estimate() (+8 more)

### Community 120 - "scripts"
Cohesion: 0.50
Nodes (4): scripts, format, lint, typecheck

### Community 122 - "context"
Cohesion: 0.20
Nodes (20): Fact, Question, _asked_already(), asks_for_secret(), assess_readiness(), _can_ask(), canonical_category(), choose_question() (+12 more)

### Community 123 - "TurnContext"
Cohesion: 0.24
Nodes (5): QuestionRecord, TurnContext, IntakeGraph, _invitation(), Shared contracts (implement in Task 1; extend only through explicit edits here)

### Community 124 - "AttachmentStore"
Cohesion: 0.16
Nodes (18): AttachmentStore, ImageRejected, NotOwned, png_bytes(), repo(), store(), test_active_turn_rejects_upload(), test_changed_invalid_bytes_conflict_before_decoding_replay() (+10 more)

### Community 126 - "workspace-ui.tsx"
Cohesion: 0.15
Nodes (18): ConfirmDialog(), FilterSelect(), Button(), buttonVariants, Dialog(), DialogContent(), DialogDescription(), DialogFooter() (+10 more)

### Community 127 - "test_gemini.py"
Cohesion: 0.31
Nodes (12): ExtractedSpan, _Fields, GeminiFields, _a(), _classify(), test_all_samples_failing_raises(), test_extractor_requests_only_named_fields(), test_failed_samples_count_against_confidence() (+4 more)

### Community 128 - "health"
Cohesion: 0.53
Nodes (3): health(), insights(), workspace()

### Community 129 - "intake/model.py"
Cohesion: 0.11
Nodes (28): ImageInput, ModelCall, ModelUnavailable, _analysis_prompt(), _bounded_context(), _guard_size(), ModelBudget, OpenRouterIntakeModel (+20 more)

### Community 130 - "RagDrafter"
Cohesion: 0.08
Nodes (15): KnowledgeExecutionError, RagDrafter, CredentialChecker, DraftExecutionError, Completion and review record — 2026-10-17, Execution handoff, File map and shared interfaces, Global Constraints (+7 more)

### Community 131 - "intake.py"
Cohesion: 0.17
Nodes (20): create_session(), _credentials(), _dump(), get_session(), post_message(), read_attachment(), remove_attachment(), request_review() (+12 more)

### Community 132 - "IntakePage.test.tsx"
Cohesion: 0.20
Nodes (13): HTTP contract (implemented in Tasks 4–5), Task 6: Customer API client and resumable UI state, Task 7: Bilingual customer chat, screenshots and reviewed submission, Task 8: Employee evidence panel and processing state, Task 9: End-to-end handoff, live vision evidence and runbook, copy(), attachment, collectingController() (+5 more)

### Community 133 - "KnowledgeService"
Cohesion: 0.11
Nodes (16): _abandoned(), _Claim, _error_cost(), KnowledgeError, KnowledgeService, FakeEmbedder, test_category_filters_include_general_policies_and_validate_tags(), test_claim_locks_source_even_before_index_row_exists() (+8 more)

### Community 134 - "cli.py"
Cohesion: 0.17
Nodes (12): _command_settings(), ingest_kb_cmd(), init_db_cmd(), Mode, run_batch_cmd(), _run_in_memory(), seed_db_cmd(), _sessionmaker() (+4 more)

### Community 135 - "Customer Conversation Intake Implementation Plan"
Cohesion: 0.29
Nodes (7): Completion audit — 2026-10-18, Customer Conversation Intake Implementation Plan, File map and dependency order, Global Constraints, Plan review and execution handoff, Review Focus, Spec coverage and acceptance map

### Community 136 - "main.py"
Cohesion: 0.12
Nodes (15): init_db(), make_engine(), make_sessionmaker(), reset_db(), upgrade_workspace_schema(), create_app(), lifespan(), IndexJobs (+7 more)

### Community 137 - "ingest.py"
Cohesion: 0.26
Nodes (8): load_jsonl(), load_tickets(), _rows(), test_csv_with_bom_and_missing_columns(), test_duplicate_external_ids_keep_first(), test_json_object_without_ids(), test_jsonl_fixture_loads(), test_unsupported_format()

### Community 138 - "intake/api.ts"
Cohesion: 0.15
Nodes (13): createIntakeApi(), IntakeRequestError, isRecord(), parseJson(), parseReceipt(), parseSession(), readError(), stringList() (+5 more)

### Community 139 - "DraftContext"
Cohesion: 0.11
Nodes (8): _error_cost(), _Execution, _ModelUsage, _number(), DraftContext, _bounded(), visit(), Task 3: Ticket-scoped investigation and all eight tools

### Community 141 - "test_cli.py"
Cohesion: 0.18
Nodes (9): test_config_error_exits_2(), boom(), test_ingest_directory_is_deterministic_and_duplicate_is_free(), test_ingest_disabled_configuration_never_calls_provider(), test_ingest_failure_exit_and_retry_stored(), test_ingest_invalid_source_does_not_stop_other_files(), test_ingest_limits_batch_without_partial_side_effects(), test_retry_stored_indexes_old_uploads_without_recovering_other_process_jobs() (+1 more)

### Community 142 - "KnowledgeDocumentIndex"
Cohesion: 0.19
Nodes (7): test_db_deadline_includes_pool_and_checkout_without_late_claim(), checked_in(), test_db_deadline_search_cancellation_is_nonblocking_and_retains_cost(), test_dbapi_commit_handoff_arbitrates_cancellation(), gate(), gate_before_dbapi(), gate_inside_dbapi()

### Community 144 - "LLMUnavailable"
Cohesion: 0.24
Nodes (11): LLMUnavailable, combine(), merge_picks(), test_both_missing_raises(), test_cost_is_summed(), test_degraded_when_jev_missing(), test_disagreement_when_jev_was_partly_confident(), test_gemini_low_confidence() (+3 more)

### Community 148 - "components-ai-thought-chain.tsx"
Cohesion: 0.14
Nodes (15): Status, StatusIcon(), statusStyles, StepContext, StepContextType, ThoughtChain(), ThoughtChainContent(), ThoughtChainItem() (+7 more)

### Community 149 - "submission.py"
Cohesion: 0.34
Nodes (8): Receipt, ReviewSnapshot, IntakeOperationRow, processing_status(), current_session_view(), SubmissionResult, SubmissionService, Ticket

### Community 151 - "errors.py"
Cohesion: 0.39
Nodes (5): IntakeError, OperationConflict, StaleReview, TurnBusy, Task 1: Durable intake sessions and ownership

### Community 152 - "Customer intake verification — 2026-10-18"
Cohesion: 0.25
Nodes (6): Browser handoff, Customer intake verification — 2026-10-18, Final automated checks, Live vision and paired review, Repaired gaps and regression evidence, Review decisions and remaining limits

### Community 153 - "knowledge.py"
Cohesion: 0.10
Nodes (15): delete_document(), download_document(), index_document(), list_chunks(), list_documents(), _require_provider(), search_knowledge(), upload_document() (+7 more)

### Community 154 - "test_workspace_api.py"
Cohesion: 0.19
Nodes (7): start_run(), test_batch_and_queue_expose_real_results(), test_batch_failure_is_isolated_and_conflicting_ids_rejected(), test_openrouter_credentials_enable_api_modes_without_exposing_keys(), test_progress_counts_only_durable_results_after_save_failure(), fail_one_save(), test_review_requires_text_and_rejects_stale_updates()

### Community 156 - "employee-frontend/src/components/theme-provider.tsx"
Cohesion: 0.21
Nodes (11): disableTransitionsTemporarily(), getSystemTheme(), isEditableTarget(), isTheme(), ResolvedTheme, Theme, THEME_VALUES, ThemeProvider() (+3 more)

### Community 157 - "index_deadlines"
Cohesion: 0.40
Nodes (3): index_deadlines(), settings(), expire_during_embedding()

### Community 158 - "load_taxonomy"
Cohesion: 0.12
Nodes (24): Decision, ExtractedField, LookupResult, decide(), empty_ticket_decision(), merge_reasons(), note_for(), _unique() (+16 more)

### Community 159 - "runs.py"
Cohesion: 0.21
Nodes (4): get_session(), get_run(), list_runs(), start_run()

### Community 160 - "TicketOutcome"
Cohesion: 0.20
Nodes (13): save_outcomes(), TicketOutcome, TicketExecution, outcome_from_state(), outcome_to_dict(), outcome_to_row(), process(), test_failed_outcome_and_dict_form() (+5 more)

### Community 161 - "Customer intake chat layout"
Cohesion: 0.33
Nodes (5): 1. Outcome, 2. Scope, 3. Layout, 5. Checks, Customer intake chat layout

### Community 164 - "test_draft_model.py"
Cohesion: 0.27
Nodes (8): make_draft_model(), response_payload(), run_provider_pipeline(), send(), search_response(), test_empty_choices_escalates_and_keeps_paid_response_usage(), test_failed_response_id_is_deduplicated_against_earlier_success(), test_other_conversion_value_errors_remain_unexpected()

### Community 165 - "Ticket flow charts"
Cohesion: 0.25
Nodes (7): 1. Outcome, 2. Scope, 5. Language, 7. Sentences, 8. Tests, 9. Files, Ticket flow charts

### Community 166 - "KnowledgePage"
Cohesion: 0.46
Nodes (8): BadgeLabel(), KnowledgePage(), beginMutation(), deleteDocument(), finishMutation(), indexDocument(), upload(), sizeLabel()

### Community 167 - "call"
Cohesion: 0.67
Nodes (4): call(), submit(), pipeline(), submit()

## Ambiguous Edges - Review These
- `Fraud Report` → `Plan 1 Live Smoke`  [AMBIGUOUS]
  README.md · relation: conceptually_related_to

## Knowledge Gaps
- **91 isolated node(s):** `zaincash-support`, `@base-ui/react`, `@fontsource-variable/plus-jakarta-sans`, `@fontsource/tajawal`, `@tailwindcss/vite` (+86 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 1013 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **41 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `HTTP contract (implemented in Tasks 4–5)` connect `IntakePage.test.tsx` to `guardrails.py`, `intake/model.py`, `TurnStore`, `Customer Conversation Intake Implementation Plan`, `errors.py`, `main.py`?**
  _High betweenness centrality (0.099) - this node is a cross-community bridge._
- **Are the 33 inferred relationships involving `Settings` (e.g. with `_command_settings()` and `_run_in_memory()`) actually correct?**
  _`Settings` has 33 INFERRED edges - model-reasoned connections that need verification._
- **What connects `zaincash-support`, `@base-ui/react`, `@fontsource-variable/plus-jakarta-sans` to the rest of the system?**
  _91 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `intake/types.ts` be split into smaller, more focused modules?**
  _Cohesion score 0.12043010752688173 - nodes in this community are weakly interconnected._
- **Why does `Task 3: Received, produced, and drafting events` connect `ticket-flow.ts` to `pytest`, `agent.py`?**
  _High betweenness centrality (0.078) - this node is a cross-community bridge._
- **Are the 24 inferred relationships involving `KnowledgeService` (e.g. with `Settings` and `UploadedDocument`) actually correct?**
  _`KnowledgeService` has 24 INFERRED edges - model-reasoned connections that need verification._

### Low-confidence Hints
_AMBIGUOUS edges — the extractor was unsure. Verify before acting on these._

- **What is the exact relationship between `Fraud Report` and `Plan 1 Live Smoke`?**
  _Edge tagged AMBIGUOUS (relation: conceptually_related_to) - confidence is low._