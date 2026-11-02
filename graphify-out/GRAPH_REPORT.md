# Graph Report - zaincash-support  (2026-11-02)

## Corpus Check
- 322 files · ~284,423 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 32 file(s) not represented in the graph (top: (none) 20, .jsonl 4, .css 4)

## Summary
- 3060 nodes · 9361 edges · 169 communities (125 shown, 44 thin omitted)
- Extraction: 89% EXTRACTED · 11% INFERRED · 0% AMBIGUOUS · INFERRED: 1028 edges (avg confidence: 0.92)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `7c877bc0`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- NewBatchPage.tsx
- intake/types.ts
- pytest
- TurnStore
- investigation.py
- agent.py
- QueuePage.tsx
- Customer conversation intake for ZainCash support
- trace-facts.ts
- IntakeController
- FakeJevRunnable
- test_rag_api.py
- employee-frontend/package.json
- intake/helpers.py
- Support Taxonomy Categories
- ui/package.json
- employee-frontend/src/App.tsx
- users-frontend/package.json
- make_ticket
- TicketRow
- web/package.json
- test_recovery_regressions.py
- compilerOptions
- employee-frontend/components.json
- agent-chat.tsx
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
- jev.py
- ui/components.json
- Settings
- fact
- Vite Config
- Human Review Gate
- compilerOptions
- PipelineState
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
- test_attachments.py
- pipeline/graph.py
- rules.py
- workspace-ui.tsx
- tools.py
- intake/types.ts
- tasks
- kb/service.py
- IntakePage.tsx
- test_handoff.py
- PipelineState
- TicketResultRow
- Credentials
- taxonomy.py
- test_submission.py
- _DatabaseCall
- lib/types.ts
- test-kb/README.md
- Plan 3 RAG Drafting Implementation Plan
- EmbeddingError
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
- canReview
- devDependencies
- devDependencies
- normalize.py
- ticket-flow.ts
- review.py
- compilerOptions
- قواعد المعرفة العربية للعرض أمام لجنة التحكيم
- pydantic
- dependencies
- InvalidEvidence
- dependencies
- compilerOptions
- main.py
- controller.test.ts
- test_final_fix_handoff.py
- ZainCash Support Workspace
- negative/README.md
- scripts
- scripts
- compilerOptions
- extract.py
- dependencies
- web/tsconfig.json
- employee-frontend/tsconfig.json
- exports
- attachments.py
- scripts
- users-frontend/README.md
- intake/contracts.py
- intake/contracts.py
- AttachmentStore
- ar/failed_transfer.md
- guardrails.py
- gemini.py
- response_payload
- intake/model.py
- test_llm.py
- intake.py
- errors.py
- KnowledgeService
- db/models.py
- Customer Conversation Intake Implementation Plan
- find_candidates
- intake/repository.py
- intake/api.ts
- fakes.py
- stage6_draft/model.py
- FakeJevRunnable
- test_dbapi_commit_handoff_arbitrates_cancellation
- resolve_date
- indexDocument
- components-ai-thought-chain.tsx
- db/repository.py
- intake/README.md
- workspace.py
- test_workspace_api.py
- test_serialize.py
- ZainCash support: architecture and ticket flow {#support-overview}
- Synthetic demo readiness
- employee-frontend/src/components/theme-provider.tsx
- ar/app_bug.md
- lookup.py
- ar/bill_payment.md
- ar/card_issue.md
- ar/fraud_report.md
- bill-payment-biller-notice.md
- api-entrypoint.sh
- factory.py
- ar/general_inquiry.md
- ar/login_access.md
- build_pipeline
- ar/refund_request.md

## God Nodes (most connected - your core abstractions)
1. `Settings` - 103 edges
2. `KnowledgeService` - 79 edges
3. `fact()` - 53 edges
4. `IntakeController` - 51 edges
5. `PipelineState` - 48 edges
6. `context()` - 48 edges
7. `draft_state()` - 44 edges
8. `message()` - 43 edges
9. `build_pipeline()` - 42 edges
10. `make_ticket()` - 41 edges

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

## Communities (169 total, 44 thin omitted)

### Community 0 - "NewBatchPage.tsx"
Cohesion: 0.12
Nodes (16): Badge(), badgeVariants, Tabs(), TabsContent(), TabsList(), tabsListVariants, TabsTrigger(), Textarea() (+8 more)

### Community 1 - "intake/types.ts"
Cohesion: 0.19
Nodes (10): IntakeApi, ControllerState, emptyState(), fileIdentity(), Credentials, MessageCommand, PendingOperation, ReviewCommand (+2 more)

### Community 2 - "pytest"
Cohesion: 0.20
Nodes (37): answer(), call(), draft_state(), Knowledge, script(), submit(), test_real_search_fault_carries_safe_draft_execution_error(), pipeline() (+29 more)

### Community 3 - "TurnStore"
Cohesion: 0.25
Nodes (6): OperationClaim, RevisionConflict, TurnBusy, _jsonable(), TurnStore, test_recovered_attempt_cannot_publish_stale_output()

### Community 4 - "investigation.py"
Cohesion: 0.16
Nodes (14): TxnRecord, parse_dt(), DraftToolInputError, _datetime(), _days(), _field(), _involves(), _phone() (+6 more)

### Community 5 - "agent.py"
Cohesion: 0.13
Nodes (6): _error_cost(), _Execution, _ModelUsage, _number(), DraftContext, Task 3: Ticket-scoped investigation and all eight tools

### Community 6 - "QueuePage.tsx"
Cohesion: 0.15
Nodes (50): EmptyState(), ErrorState(), LoadingState(), Metric(), PageHeader(), PriorityBadge(), StatusBadge(), Button() (+42 more)

### Community 7 - "Customer conversation intake for ZainCash support"
Cohesion: 0.06
Nodes (31): 10. Verification and acceptance criteria, 11. Delivery and review, 1. Outcome and agreed requirements, 2. Current implementation and integration points, 3. Approach and boundaries, 4. Conversation state and turn flow, 5. Facts, evidence, and readiness, 6. Language and screenshot behavior (+23 more)

### Community 8 - "trace-facts.ts"
Cohesion: 0.10
Nodes (23): Ticket Flow Charts Implementation Plan, 1. Outcome, 2. Scope, 5. Language, 6. How a result becomes the charts, 7. Sentences, 8. Tests, 9. Files (+15 more)

### Community 9 - "IntakeController"
Cohesion: 0.20
Nodes (5): IntakeController, isConflict(), isOffline(), safeMessage(), Language

### Community 10 - "FakeJevRunnable"
Cohesion: 0.10
Nodes (19): CredentialCheck, DegradedCredentialChecker, _finite_nonnegative(), _get(), JevCredentialChecker, Checker, ResponseRunnable, test_bad_usage_cannot_poison_cost() (+11 more)

### Community 11 - "test_rag_api.py"
Cohesion: 0.15
Nodes (17): client(), evidence_client(), test_actual_guardrail_failure_is_separate_from_reply(), test_concurrent_index_requests_share_active_work(), test_disabled_or_missing_provider_stores_without_indexing(), test_explicit_retry_tags_search_and_chunk_pagination(), test_health_distinguishes_failed_from_empty(), test_health_requires_compatible_nonempty_index() (+9 more)

### Community 12 - "employee-frontend/package.json"
Cohesion: 0.06
Nodes (31): @base-ui/react, class-variance-authority, cn, eslint, @eslint/js, eslint-plugin-react-hooks, eslint-plugin-react-refresh, @fontsource/tajawal (+23 more)

### Community 14 - "intake/helpers.py"
Cohesion: 0.22
Nodes (6): grounded_analysis(), grounded_review(), ScriptedIntakeModel, HTTP contract (implemented in Tasks 4–5), Task 4: Resumable graph turns, review and customer API, Task 9: End-to-end handoff, live vision evidence and runbook

### Community 15 - "Support Taxonomy Categories"
Cohesion: 0.22
Nodes (21): lookup, Account KYC, Account & Security, Agent Dispute, Agent Network, App Bug, Bill Payment, Card Issue (+13 more)

### Community 16 - "ui/package.json"
Cohesion: 0.07
Nodes (29): @turbo/gen, zod, @base-ui/react, class-variance-authority, cn, eslint, @eslint/js, eslint-plugin-react-hooks (+21 more)

### Community 17 - "employee-frontend/src/App.tsx"
Cohesion: 0.15
Nodes (20): App(), EvaluationPage, InsightsPage, KnowledgePage, NewBatchPage, QueuePage, RunDetailPage, RunsPage (+12 more)

### Community 18 - "users-frontend/package.json"
Cohesion: 0.09
Nodes (22): turbo, devDependencies, prettier, prettier-plugin-tailwindcss, turbo, typescript, engines, node (+14 more)

### Community 19 - "make_ticket"
Cohesion: 0.05
Nodes (69): build_graph(), PipelineDeps, InMemoryTransactionRepo, requests_credentials(), load_taxonomy(), tax(), FakeClassifier, make_output() (+61 more)

### Community 20 - "TicketRow"
Cohesion: 0.19
Nodes (16): get_run(), list_runs(), start_run(), BatchInput, _run_with_db(), RunRow, TicketRow, create_run() (+8 more)

### Community 21 - "web/package.json"
Cohesion: 0.07
Nodes (27): jsdom, @testing-library/jest-dom, @testing-library/react, @testing-library/user-event, @workspace/ui, eslint, @eslint/js, eslint-plugin-react-hooks (+19 more)

### Community 22 - "test_recovery_regressions.py"
Cohesion: 0.10
Nodes (18): _command_settings(), ingest_kb_cmd(), init_db_cmd(), Mode, run_batch_cmd(), _run_in_memory(), seed_db_cmd(), get_settings() (+10 more)

### Community 23 - "compilerOptions"
Cohesion: 0.08
Nodes (23): compilerOptions, allowArbitraryExtensions, allowImportingTsExtensions, erasableSyntaxOnly, jsx, lib, module, moduleDetection (+15 more)

### Community 24 - "employee-frontend/components.json"
Cohesion: 0.09
Nodes (21): aliases, components, hooks, lib, ui, utils, iconLibrary, menuAccent (+13 more)

### Community 25 - "agent-chat.tsx"
Cohesion: 0.15
Nodes (24): clsx, tailwind-merge, AgentChat, AgentChatProps, AgentMessage, AssistantText(), AttachedFile, AttachedImage (+16 more)

### Community 26 - "compilerOptions"
Cohesion: 0.09
Nodes (22): compilerOptions, allowArbitraryExtensions, allowImportingTsExtensions, erasableSyntaxOnly, jsx, lib, module, moduleDetection (+14 more)

### Community 27 - "web/src/components/theme-provider.tsx"
Cohesion: 0.15
Nodes (13): App(), controller, disableTransitionsTemporarily(), getSystemTheme(), isEditableTarget(), isTheme(), ResolvedTheme, Theme (+5 more)

### Community 28 - "test_embeddings.py"
Cohesion: 0.19
Nodes (18): OpenRouterEmbedder, settings(), test_33_inputs_are_batched_and_each_batch_maps_its_own_indexes(), test_billed_batch_cost_survives_cancellation_without_cross_call_leakage(), test_cancellation_propagates_to_the_callers_deadline(), test_empty_input_returns_empty_batch_without_a_request(), unexpected_request(), test_invalid_rag_settings_are_rejected() (+10 more)

### Community 29 - "Classify and Extract Prompts"
Cohesion: 0.31
Nodes (8): extract, gemini_classify, Pipeline Graph Orchestration, jev_classify, prepare, Gemini Extract Prompt v1, GeminiClassifier, JevClassifier

### Community 30 - "test_draft_tools.py"
Cohesion: 0.13
Nodes (26): api(), settings(), test_all_eight_tools_and_seven_parallel_calls_execute_only_six(), test_context_copies_input_and_rejects_raising_hard_call_limit(), test_database_faults_remain_distinct_and_record_paid_search_cost(), test_discovered_ref_can_be_inspected_but_not_promoted_to_match(), test_exact_and_fuzzy_queries_are_scoped_and_never_confirm_candidates(), test_exact_reference_still_requires_customer_and_excludes_future() (+18 more)

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

### Community 38 - "jev.py"
Cohesion: 0.24
Nodes (10): ClassificationResult, build_order_check(), build_questions(), build_state(), category_criteria(), _input_tokens(), JevClassifier, _picks() (+2 more)

### Community 39 - "ui/components.json"
Cohesion: 0.10
Nodes (19): aliases, components, hooks, lib, ui, utils, iconLibrary, menuAccent (+11 more)

### Community 40 - "Settings"
Cohesion: 0.10
Nodes (12): Settings, test_blank_intake_model_is_rejected(), test_non_positive_image_limit_is_rejected(), test_relative_upload_directory_is_rooted_in_the_repository(), test_anthropic_model_selects_the_draft_model_only(), test_defaults(), test_drafting_configuration_cannot_bypass_hard_limits(), test_drafting_limits_load_from_environment() (+4 more)

### Community 41 - "fact"
Cohesion: 0.22
Nodes (30): merge_analysis(), remove_attachment_evidence(), context(), fact(), message(), proposal(), test_additional_issue_is_resolved_in_place_instead_of_appended(), test_ambiguous_or_modified_relative_date_is_not_guessed() (+22 more)

### Community 43 - "Human Review Gate"
Cohesion: 0.25
Nodes (4): support CLI, Support Workspace UI Plan, Review API, Workspace UI Verification

### Community 44 - "compilerOptions"
Cohesion: 0.12
Nodes (16): compilerOptions, allowImportingTsExtensions, erasableSyntaxOnly, lib, module, moduleDetection, noEmit, noFallthroughCasesInSwitch (+8 more)

### Community 46 - "PipelineState"
Cohesion: 0.09
Nodes (15): KnowledgeExecutionError, DraftResult, _Nodes, RagDrafter, Drafter, DraftExecutionError, NullDrafter, UnavailableDrafter (+7 more)

### Community 47 - "compilerOptions"
Cohesion: 0.12
Nodes (16): compilerOptions, allowImportingTsExtensions, erasableSyntaxOnly, lib, module, moduleDetection, noEmit, noFallthroughCasesInSwitch (+8 more)

### Community 48 - "support_test"
Cohesion: 0.11
Nodes (19): ingest(), index_deadlines(), settings(), support_test(), expire_during_embedding(), Artifacts, servers and remaining concerns, Commands and automated verification — historical Task 8, Corpus and actual retrieval (+11 more)

### Community 57 - "parse_document"
Cohesion: 0.10
Nodes (30): TextChunk, _append_chunks(), _check_extracted_size(), DocumentParseError, parse_document(), _parse_pdf(), make_pdf(), test_arabic_text_and_bom_are_preserved() (+22 more)

### Community 58 - "test_attachments.py"
Cohesion: 0.17
Nodes (17): ImageRejected, IntakeError, NotOwned, OperationConflict, png_bytes(), test_active_turn_rejects_upload(), test_changed_invalid_bytes_conflict_before_decoding_replay(), test_concurrent_uploads_stop_at_the_session_cap() (+9 more)

### Community 59 - "pipeline/graph.py"
Cohesion: 0.09
Nodes (6): ClassifierOutput, Ticket, _default_retry(), _percentile(), _retryable(), CredentialChecker

### Community 60 - "rules.py"
Cohesion: 0.21
Nodes (18): Decision, LookupResult, decide(), empty_ticket_decision(), merge_reasons(), note_for(), _unique(), Category (+10 more)

### Community 61 - "workspace-ui.tsx"
Cohesion: 0.16
Nodes (16): ConfirmDialog(), FilterSelect(), Dialog(), DialogContent(), DialogDescription(), DialogFooter(), DialogHeader(), DialogOverlay() (+8 more)

### Community 62 - "tools.py"
Cohesion: 0.07
Nodes (22): DraftAlreadySubmitted, DraftSubmission, DraftToolLimit, _bounded(), visit(), build_tools(), flag(), guarded() (+14 more)

### Community 63 - "intake/types.ts"
Cohesion: 0.12
Nodes (19): Task 7: Bilingual customer chat, screenshots and reviewed submission, copy(), copy, IntakeCopy, OwnedImage(), factText(), ReviewPanel(), Attachment (+11 more)

### Community 64 - "tasks"
Cohesion: 0.12
Nodes (16): dependsOn, inputs, outputs, cache, persistent, dependsOn, dependsOn, $schema (+8 more)

### Community 65 - "kb/service.py"
Cohesion: 0.10
Nodes (25): delete_document(), download_document(), index_document(), list_chunks(), list_documents(), _require_provider(), search_knowledge(), upload_document() (+17 more)

### Community 66 - "IntakePage.tsx"
Cohesion: 0.13
Nodes (15): Global Constraints, Intake Chat UI Implementation Plan, Task 1: Put the summary and receipt in the thread, Task 2: Put screenshots inside the composer, Task 3: Apply the workspace chat styles, Task 4: Check the page in the browser, 1. Outcome, 2. Scope (+7 more)

### Community 67 - "test_handoff.py"
Cohesion: 0.13
Nodes (26): Analysis, EvidenceRef, Fact, IntakeModel, image_evidence(), test_reinspection_keeps_current_images_and_new_observations(), again(), initial() (+18 more)

### Community 68 - "PipelineState"
Cohesion: 0.12
Nodes (15): 10. Remaining demo roadmap, 1. Intent and acceptance criteria, 3. Provider and configuration, 4. Knowledge ingestion and persistence, 5. Retrieval and evidence, 7. Draft guardrails and failure outcomes, 8. Pipeline, API, CLI and UI integration, 9. Demo policies and verification (+7 more)

### Community 69 - "TicketResultRow"
Cohesion: 0.10
Nodes (15): get_session(), get_result(), list_results(), read_intake_attachment(), review_result(), KnowledgeIndexInput, KnowledgeSearchInput, ReviewInput (+7 more)

### Community 70 - "Credentials"
Cohesion: 0.26
Nodes (3): Credentials, SessionView, IntakeService

### Community 71 - "taxonomy.py"
Cohesion: 0.23
Nodes (5): most_urgent(), priority_rank(), TaxonomyError, test_priority_helpers(), test_rejects_unknown_team()

### Community 72 - "test_submission.py"
Cohesion: 0.32
Nodes (4): _payload(), test_concurrent_submit_dispatches_once(), test_second_request_id_reuses_the_approved_review(), test_submission_replay_creates_one_ticket()

### Community 73 - "_DatabaseCall"
Cohesion: 0.17
Nodes (3): _check_deadline(), _consume(), _DatabaseCall

### Community 74 - "lib/types.ts"
Cohesion: 0.10
Nodes (31): acceptIndexRequest(), canRequestIndex(), PendingIndexes, persistPendingIndexes(), pollKnowledge(), refresh(), stop(), PollOptions (+23 more)

### Community 75 - "test-kb/README.md"
Cohesion: 0.15
Nodes (6): Fictional RAG walkthrough inputs, توثيق الحساب — سياسة خيالية للعرض التجريبي, نزاع مع وكيل — سياسة خيالية للعرض التجريبي, الطلبات غير الواضحة وخارج النطاق — سياسة خيالية للعرض التجريبي, الاستفسار المؤقت للدعم في المهمة ٨ — سياسة خيالية للعرض التجريبي, التحويل لمستلم بالخطأ — سياسة خيالية للعرض التجريبي

### Community 76 - "Plan 3 RAG Drafting Implementation Plan"
Cohesion: 0.20
Nodes (10): Completion and review record — 2026-10-17, Execution handoff, File map and shared interfaces, Global Constraints, Plan 3 RAG Drafting Implementation Plan, Plan self-review, Review Focus, Task 6: API/CLI indexing and persisted citation projection (+2 more)

### Community 77 - "EmbeddingError"
Cohesion: 0.12
Nodes (9): EmbeddingBatch, EmbeddingError, _nonnegative_number(), _ordered_vectors(), _response_cost(), Embeddings, ErrorEmbedder, test_lock_serializes_operations_and_submit_waits_for_inflight_search() (+1 more)

### Community 79 - "devDependencies"
Cohesion: 0.12
Nodes (16): devDependencies, eslint, @eslint/js, eslint-plugin-react-hooks, eslint-plugin-react-refresh, globals, prettier, prettier-plugin-tailwindcss (+8 more)

### Community 80 - "judge-demo.ar.md"
Cohesion: 0.14
Nodes (13): أعطال التطبيق — سياسة خيالية للعرض التجريبي, استرجاع مبلغ شراء — سياسة خيالية للعرض التجريبي, استعادة الدخول — سياسة خيالية للعرض التجريبي, الاستفسار الآمن من الدعم — سياسة خيالية للعرض التجريبي, الاستفسار المؤقت للدعم في المهمة ٨ — سياسة خيالية للعرض التجريبي, التحويل المعلّق — سياسة خيالية للعرض التجريبي, التحويل لمستلم بالخطأ — سياسة خيالية للعرض التجريبي, الطلبات غير الواضحة وخارج النطاق — سياسة خيالية للعرض التجريبي (+5 more)

### Community 93 - "canReview"
Cohesion: 0.50
Nodes (3): Task 8: Employee evidence panel and processing state, canReview(), REVIEWABLE

### Community 94 - "devDependencies"
Cohesion: 0.11
Nodes (19): devDependencies, eslint, @eslint/js, eslint-plugin-react-hooks, eslint-plugin-react-refresh, globals, jsdom, @tailwindcss/vite (+11 more)

### Community 95 - "devDependencies"
Cohesion: 0.14
Nodes (14): devDependencies, eslint, @eslint/js, eslint-plugin-react-hooks, eslint-plugin-react-refresh, globals, tailwindcss, @tailwindcss/vite (+6 more)

### Community 96 - "normalize.py"
Cohesion: 0.19
Nodes (17): sanitize_intake_text(), detect_arabizi(), fold_arabic(), has_latin_mix(), _latin_words(), mask_cards(), normalize(), sanitize_for_storage() (+9 more)

### Community 97 - "ticket-flow.ts"
Cohesion: 0.06
Nodes (81): Global Constraints, Task 1: Sentence catalog, Task 2: Which step is open, Task 3: Received, produced, and drafting events, Task 4: Mermaid source, Task 5: Draw the charts on the ticket page, Confidence(), highlightedText() (+73 more)

### Community 98 - "review.py"
Cohesion: 0.32
Nodes (14): ReviewText, InvalidEvidence, build_review(), _compact(), _render_value(), _ticket_text(), _tokens(), validate_review_numbers() (+6 more)

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
Cohesion: 0.18
Nodes (15): canonical_digits(), normalize_reported_date(), _apply(), _check_reference(), _compact(), checked_update(), _newer_correction(), _normalize_precise() (+7 more)

### Community 104 - "dependencies"
Cohesion: 0.15
Nodes (13): dependencies, @base-ui/react, class-variance-authority, cn, @fontsource/tajawal, @fontsource-variable/plus-jakarta-sans, @hugeicons/core-free-icons, @hugeicons/react (+5 more)

### Community 105 - "compilerOptions"
Cohesion: 0.17
Nodes (11): compilerOptions, jsx, lib, module, moduleResolution, outDir, skipLibCheck, strict (+3 more)

### Community 106 - "main.py"
Cohesion: 0.12
Nodes (11): _safe_dispatch(), upgrade_workspace_schema(), recover(), fail_intake_placeholders(), reconcile_intake_run(), recover_intake_processing(), dispatch_intake(), _submit() (+3 more)

### Community 107 - "controller.test.ts"
Cohesion: 0.15
Nodes (14): Task 6: Customer API client and resumable UI state, emptySession(), fakeApi(), review, attachment, collectingController(), emptySession(), fakeApi() (+6 more)

### Community 108 - "test_final_fix_handoff.py"
Cohesion: 0.11
Nodes (20): Passage, assert_completed_evidence(), faulty_knowledge(), read(), outer_deadlines(), PaidEmbeddings, runner_env(), build() (+12 more)

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

### Community 114 - "extract.py"
Cohesion: 0.18
Nodes (9): LLMUnavailable, Candidates, NormalizedTicket, Classifier, FieldExtractor, _field(), fill_gaps(), _is_weak() (+1 more)

### Community 115 - "dependencies"
Cohesion: 0.25
Nodes (8): dependencies, clsx, @hugeicons/core-free-icons, @hugeicons/react, react, react-dom, tailwind-merge, @workspace/ui

### Community 116 - "web/tsconfig.json"
Cohesion: 0.33
Nodes (5): compilerOptions, paths, files, @workspace/ui/*, references

### Community 117 - "employee-frontend/tsconfig.json"
Cohesion: 0.40
Nodes (4): compilerOptions, paths, files, references

### Community 118 - "exports"
Cohesion: 0.40
Nodes (5): exports, ./components/*, ./globals.css, ./hooks/*, ./lib/*

### Community 119 - "attachments.py"
Cohesion: 0.14
Nodes (13): _display_name(), IntakeMessageRow, IntakeSessionRow, assert_same_operation(), new_access_token(), operation_fingerprint(), repo(), test_changed_payload_cannot_reuse_operation_identity() (+5 more)

### Community 120 - "scripts"
Cohesion: 0.50
Nodes (4): scripts, format, lint, typecheck

### Community 122 - "intake/contracts.py"
Cohesion: 0.24
Nodes (17): IntakeState, Question, Readiness, _asked_already(), asks_for_secret(), assess_readiness(), _can_ask(), canonical_category() (+9 more)

### Community 123 - "intake/contracts.py"
Cohesion: 0.10
Nodes (13): _aware(), Message, QuestionRecord, ReviewSnapshot, TurnContext, TurnResult, IntakeGraph, _invitation() (+5 more)

### Community 124 - "AttachmentStore"
Cohesion: 0.13
Nodes (6): AttachmentStore, IntakeRepository, make_intake_service(), builder(), repo(), store()

### Community 126 - "guardrails.py"
Cohesion: 0.23
Nodes (12): normalize_phone(), parse_amount(), to_ascii_digits(), normalize_value(), check_draft(), _citation_findings(), _exact_amount(), _grounding_findings() (+4 more)

### Community 127 - "gemini.py"
Cohesion: 0.14
Nodes (10): Sample, StructuredLLM, ExtractedSpan, _Fields, GeminiExtractor, GeminiFields, verified_pick(), render_prompt() (+2 more)

### Community 128 - "response_payload"
Cohesion: 0.22
Nodes (16): embedder_for(), item(), response_payload(), respond(), respond(), test_billed_cost_survives_cancellation_during_client_close(), test_billed_response_cost_is_retained_when_its_vectors_are_invalid(), test_cost_uses_one_reported_value_or_configured_token_estimate() (+8 more)

### Community 129 - "intake/model.py"
Cohesion: 0.10
Nodes (27): Attachment, ImageInput, ModelCall, _analysis_prompt(), _bounded_context(), _guard_size(), ModelBudget, OpenRouterIntakeModel (+19 more)

### Community 130 - "test_llm.py"
Cohesion: 0.13
Nodes (11): GeminiStructuredLLM, make_gemini_llm(), _llm(), _S, test_draft_model_uses_millisecond_timeout_and_disables_sdk_retries(), test_openrouter_reported_cost_takes_precedence_over_token_estimate(), test_openrouter_retry_budget_is_bounded(), test_openrouter_structured_samples_use_configured_key_and_validate_output() (+3 more)

### Community 131 - "intake.py"
Cohesion: 0.17
Nodes (19): create_session(), _credentials(), _dump(), get_session(), post_message(), read_attachment(), remove_attachment(), request_review() (+11 more)

### Community 132 - "errors.py"
Cohesion: 0.26
Nodes (11): ModelUnavailable, test_review_after_failed_analysis_still_interprets_the_saved_message(), command(), create(), test_actual_app_restart_reconciles_failed_placeholder(), test_failed_review_retry_cannot_reopen_submitted_session(), test_original_payload_identity_survives_sanitization(), test_publication_failure_is_retryable_without_restart() (+3 more)

### Community 133 - "KnowledgeService"
Cohesion: 0.10
Nodes (14): Embedder, KnowledgeChunk, _abandoned(), _Claim, _error_cost(), IndexAttemptLostError, KnowledgeError, KnowledgeService (+6 more)

### Community 135 - "Customer Conversation Intake Implementation Plan"
Cohesion: 0.20
Nodes (8): Completion audit — 2026-10-18, Customer Conversation Intake Implementation Plan, Execution conventions and repository baseline, File map and dependency order, Global Constraints, Plan review and execution handoff, Review Focus, Spec coverage and acceptance map

### Community 136 - "find_candidates"
Cohesion: 0.25
Nodes (12): Candidate, _add(), find_candidates(), _overlaps(), test_amount_forms(), test_arabic_indic_amount_not_confused_with_phone(), test_dates_absolute_and_weekday(), test_dedupes_repeated_values() (+4 more)

### Community 137 - "intake/repository.py"
Cohesion: 0.20
Nodes (18): CustomerReview, Receipt, IntakeAttachmentRow, IntakeOperationRow, IntakeSubmissionRow, StaleReview, _attachment(), customer_review() (+10 more)

### Community 138 - "intake/api.ts"
Cohesion: 0.15
Nodes (13): createIntakeApi(), IntakeRequestError, isRecord(), parseJson(), parseReceipt(), parseSession(), readError(), stringList() (+5 more)

### Community 139 - "fakes.py"
Cohesion: 0.33
Nodes (11): FieldPick, finalize(), FakeExtractor, _setup(), test_fill_gaps_noop_and_failure_tolerant(), test_fill_gaps_only_asks_for_weak_required_fields(), test_gemini_span_not_in_text_is_null(), test_gemini_word_amount_uses_normalized_hint() (+3 more)

### Community 141 - "FakeJevRunnable"
Cohesion: 0.32
Nodes (10): FakeJevRunnable, _criteria(), _run(), test_low_top_probability_is_uncertain(), test_one_main_call_with_all_questions(), test_order_check_uses_reversed_options(), test_order_disagreement_is_uncertain(), test_priority_level_maps_to_p_label() (+2 more)

### Community 142 - "test_dbapi_commit_handoff_arbitrates_cancellation"
Cohesion: 0.15
Nodes (8): test_db_deadline_includes_pool_and_checkout_without_late_claim(), checked_in(), test_db_deadline_search_cancellation_is_nonblocking_and_retains_cost(), test_dbapi_commit_handoff_arbitrates_cancellation(), gate(), gate_before_dbapi(), gate_inside_dbapi(), test_index_deadline_or_cancellation_preserves_real_adapter_partial_cost()

### Community 143 - "resolve_date"
Cohesion: 0.36
Nodes (4): resolve_date(), _safe_date(), test_resolve(), test_unresolvable_is_none()

### Community 144 - "indexDocument"
Cohesion: 0.60
Nodes (5): beginMutation(), deleteDocument(), finishMutation(), indexDocument(), upload()

### Community 148 - "components-ai-thought-chain.tsx"
Cohesion: 0.08
Nodes (25): LanguageToggle(), Status, StatusIcon(), statusStyles, StepContext, StepContextType, ThoughtChain(), ThoughtChainContent() (+17 more)

### Community 149 - "db/repository.py"
Cohesion: 0.14
Nodes (20): TransactionRow, finish_run(), load_incidents(), load_transactions(), save_outcomes(), SqlTransactionRepo, _to_record(), _upsert() (+12 more)

### Community 151 - "workspace.py"
Cohesion: 0.50
Nodes (4): health(), insights(), workspace(), latest_results_query()

### Community 152 - "test_workspace_api.py"
Cohesion: 0.10
Nodes (21): _sessionmaker(), init_db(), make_engine(), make_sessionmaker(), reset_db(), create_app(), lifespan(), IndexJobs (+13 more)

### Community 153 - "test_serialize.py"
Cohesion: 0.60
Nodes (4): outcome_to_dict(), outcome_to_row(), test_failed_outcome_and_dict_form(), test_full_outcome_is_json_safe()

### Community 154 - "ZainCash support: architecture and ticket flow {#support-overview}"
Cohesion: 0.50
Nodes (3): 1 · System architecture {#system-architecture}, 2 · Ticket flow {#ticket-flow}, ZainCash support: architecture and ticket flow {#support-overview}

### Community 155 - "Synthetic demo readiness"
Cohesion: 0.50
Nodes (4): Evidence by layer, Known limitations and remaining work, Repeatable local walkthrough, Synthetic demo readiness

### Community 156 - "employee-frontend/src/components/theme-provider.tsx"
Cohesion: 0.21
Nodes (11): disableTransitionsTemporarily(), getSystemTheme(), isEditableTarget(), isTheme(), ResolvedTheme, Theme, THEME_VALUES, ThemeProvider() (+3 more)

### Community 158 - "lookup.py"
Cohesion: 0.17
Nodes (16): ExtractedField, _as_date(), _iqd_amount(), match_transaction(), TransactionRepo, txn_from_dict(), _ex(), _match() (+8 more)

### Community 164 - "factory.py"
Cohesion: 0.27
Nodes (8): make_draft_model(), response_payload(), run_provider_pipeline(), send(), search_response(), test_empty_choices_escalates_and_keeps_paid_response_usage(), test_failed_response_id_is_deduplicated_against_earlier_success(), test_other_conversion_value_errors_remain_unexpected()

### Community 167 - "build_pipeline"
Cohesion: 0.16
Nodes (17): build_pipeline(), ConfigError, make_jev_client(), run_batch(), ScriptedChat, _settings(), test_builds_jev_pipeline_with_injected_clients(), test_credential_checker_is_independent_of_jev_classification() (+9 more)

## Ambiguous Edges - Review These
- `Fraud Report` → `Plan 1 Live Smoke`  [AMBIGUOUS]
  README.md · relation: conceptually_related_to

## Knowledge Gaps
- **91 isolated node(s):** `zaincash-support`, `@base-ui/react`, `@fontsource-variable/plus-jakarta-sans`, `@fontsource/tajawal`, `@tailwindcss/vite` (+86 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 1025 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **44 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `HTTP contract (implemented in Tasks 4–5)` connect `intake/helpers.py` to `intake/model.py`, `Customer Conversation Intake Implementation Plan`, `controller.test.ts`, `TicketRow`, `test_attachments.py`, `canReview`, `guardrails.py`, `intake/types.ts`?**
  _High betweenness centrality (0.106) - this node is a cross-community bridge._
- **Are the 33 inferred relationships involving `Settings` (e.g. with `_command_settings()` and `_run_in_memory()`) actually correct?**
  _`Settings` has 33 INFERRED edges - model-reasoned connections that need verification._
- **What connects `zaincash-support`, `@base-ui/react`, `@fontsource-variable/plus-jakarta-sans` to the rest of the system?**
  _91 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `NewBatchPage.tsx` be split into smaller, more focused modules?**
  _Cohesion score 0.12258064516129032 - nodes in this community are weakly interconnected._
- **Why does `Settings` connect `Settings` to `intake/model.py`, `test_llm.py`, `pytest`, `investigation.py`, `KnowledgeService`, `agent.py`, `intake/repository.py`, `test_rag_api.py`, `make_ticket`, `TicketRow`, `db/repository.py`, `test_recovery_regressions.py`, `test_workspace_api.py`, `Synthetic demo readiness`, `test_embeddings.py`, `test_draft_tools.py`, `test_kb_service.py`, `factory.py`, `build_pipeline`, `fact`, `PipelineState`, `support_test`, `pipeline/graph.py`, `kb/service.py`, `EmbeddingError`, `main.py`, `test_final_fix_handoff.py`, `attachments.py`, `AttachmentStore`?**
  _High betweenness centrality (0.090) - this node is a cross-community bridge._
- **Are the 24 inferred relationships involving `KnowledgeService` (e.g. with `Settings` and `UploadedDocument`) actually correct?**
  _`KnowledgeService` has 24 INFERRED edges - model-reasoned connections that need verification._

### Low-confidence Hints
_AMBIGUOUS edges — the extractor was unsure. Verify before acting on these._

- **What is the exact relationship between `Fraud Report` and `Plan 1 Live Smoke`?**
  _Edge tagged AMBIGUOUS (relation: conceptually_related_to) - confidence is low._