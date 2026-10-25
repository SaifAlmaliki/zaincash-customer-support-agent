# Graph Report - zaincash-support  (2026-10-25)

## Corpus Check
- 304 files · ~252,370 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 30 file(s) not represented in the graph (top: (none) 18, .jsonl 4, .css 4)

## Summary
- 3056 nodes · 9437 edges · 166 communities (118 shown, 48 thin omitted)
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
- test_draft_guardrails.py
- tools.py
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
- make_output
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
- submission.py
- intake/repository.py
- RunRow
- workspace-ui.tsx
- investigation.py
- test_llm.py
- tasks
- PipelineTrace.tsx
- IntakePage.tsx
- test_handoff.py
- PipelineState
- datetime
- normalize.py
- knowledge.py
- lookup.py
- Credentials
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
- factory.py
- devDependencies
- devDependencies
- guardrails.py
- ticket-flow.ts
- NewBatchPage.tsx
- compilerOptions
- قواعد المعرفة العربية للعرض أمام لجنة التحكيم
- pydantic
- dependencies
- InvalidEvidence
- dependencies
- compilerOptions
- KnowledgeError
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
- rag_fakes.py
- scripts
- users-frontend/README.md
- context
- IntakeState
- AttachmentStore
- ar/failed_transfer.md
- find_candidates
- test_gemini.py
- workspace.py
- intake/model.py
- Plan 3 RAG Drafting Implementation Plan
- intake.py
- build_tools
- KnowledgeService
- cli.py
- Customer Conversation Intake Implementation Plan
- main.py
- KnowledgePage
- intake/api.ts
- DraftContext
- test_dbapi_commit_handoff_arbitrates_cancellation
- ar/refund_request.md
- task8-history-policy.md
- @testing-library/react
- ar/wrong_recipient.md
- collapsible.tsx
- resolve_date
- intake/README.md
- errors.py
- _bounded
- TicketInput
- Ticket flow charts
- _ModelUsage
- employee-frontend/src/components/theme-provider.tsx
- recover_intake_processing
- load_taxonomy
- DraftSubmission
- Customer intake chat layout
- ar/agent_dispute.md
- ar/app_bug.md
- ar/bill_payment.md
- ar/fraud_report.md

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

## Communities (166 total, 48 thin omitted)

### Community 1 - "intake/types.ts"
Cohesion: 0.10
Nodes (26): Task 7: Bilingual customer chat, screenshots and reviewed submission, copy(), IntakeApi, ControllerState, emptyState(), fileIdentity(), IntakeCopy, OwnedImage() (+18 more)

### Community 2 - "pytest"
Cohesion: 0.21
Nodes (34): answer(), call(), draft_state(), Knowledge, script(), submit(), drafter(), events() (+26 more)

### Community 3 - "TurnStore"
Cohesion: 0.23
Nodes (9): OperationClaim, TurnResult, RevisionConflict, sanitize_intake_text(), _jsonable(), TurnStore, test_recovered_attempt_cannot_publish_stale_output(), test_review_publication_revision_matches_the_session() (+1 more)

### Community 4 - "test_draft_guardrails.py"
Cohesion: 0.14
Nodes (27): requests_credentials(), check(), test_aggregation_is_deduplicated_and_has_no_state_side_effects(), test_amount_occurrences_keep_their_own_currency_and_sign(), test_avoid_sharing_warning_does_not_excuse_a_later_request(), test_candidate_prompt_limit_does_not_hide_later_ungrounded_references(), test_candidate_transactions_cannot_authorize_reply_evidence(), test_citations_must_have_been_retrieved_for_this_ticket() (+19 more)

### Community 5 - "tools.py"
Cohesion: 0.24
Nodes (8): _Flag, _History, _Input, _Knowledge, _Lookup, _Recent, _Search, _Service

### Community 6 - "QueuePage.tsx"
Cohesion: 0.15
Nodes (55): Confidence(), EmptyState(), ErrorState(), LoadingState(), Metric(), PageHeader(), PriorityBadge(), StatusBadge() (+47 more)

### Community 7 - "Customer conversation intake for ZainCash support"
Cohesion: 0.06
Nodes (32): 10. Verification and acceptance criteria, 11. Delivery and review, 1. Outcome and agreed requirements, 2. Current implementation and integration points, 3. Approach and boundaries, 4. Conversation state and turn flow, 5. Facts, evidence, and readiness, 6. Language and screenshot behavior (+24 more)

### Community 8 - "components-ai-thought-chain.tsx"
Cohesion: 0.08
Nodes (24): LanguageToggle(), Status, StatusIcon(), statusStyles, StepContext, StepContextType, ThoughtChain(), ThoughtChainContent() (+16 more)

### Community 9 - "IntakeController"
Cohesion: 0.19
Nodes (5): IntakeController, isConflict(), isOffline(), safeMessage(), Language

### Community 10 - "FakeJevRunnable"
Cohesion: 0.12
Nodes (20): CredentialCheck, DegradedCredentialChecker, _finite_nonnegative(), _get(), JevCredentialChecker, test_contracts_reject_extra_keys(), test_datetimes_must_be_timezone_aware(), ResponseRunnable (+12 more)

### Community 11 - "test_rag_api.py"
Cohesion: 0.15
Nodes (17): client(), test_actual_guardrail_failure_is_separate_from_reply(), test_concurrent_index_requests_share_active_work(), test_disabled_or_missing_provider_stores_without_indexing(), test_explicit_retry_tags_search_and_chunk_pagination(), test_health_distinguishes_failed_from_empty(), test_health_requires_compatible_nonempty_index(), test_index_background_admission_is_bounded_and_releases_capacity() (+9 more)

### Community 12 - "employee-frontend/package.json"
Cohesion: 0.06
Nodes (31): @base-ui/react, class-variance-authority, cn, eslint, @eslint/js, eslint-plugin-react-hooks, eslint-plugin-react-refresh, @fontsource/tajawal (+23 more)

### Community 14 - "intake/contracts.py"
Cohesion: 0.13
Nodes (19): _aware(), EvidenceRef, Fact, IntakeModel, Message, Readiness, _apply(), _newer_correction() (+11 more)

### Community 15 - "Support Taxonomy Categories"
Cohesion: 0.21
Nodes (22): lookup, Account KYC, Account & Security, Agent Dispute, Agent Network, App Bug, Bill Payment, Card Issue (+14 more)

### Community 16 - "ui/package.json"
Cohesion: 0.07
Nodes (29): @turbo/gen, zod, @base-ui/react, class-variance-authority, cn, eslint, @eslint/js, eslint-plugin-react-hooks (+21 more)

### Community 17 - "employee-frontend/src/App.tsx"
Cohesion: 0.13
Nodes (21): App(), EvaluationPage, InsightsPage, KnowledgePage, NewBatchPage, QueuePage, RunDetailPage, RunsPage (+13 more)

### Community 18 - "users-frontend/package.json"
Cohesion: 0.09
Nodes (22): turbo, devDependencies, prettier, prettier-plugin-tailwindcss, turbo, typescript, engines, node (+14 more)

### Community 19 - "make_output"
Cohesion: 0.13
Nodes (31): build_graph(), PipelineDeps, InMemoryTransactionRepo, FakeClassifier, make_output(), make_ticket(), pipeline(), test_ingest_directory_is_deterministic_and_duplicate_is_free() (+23 more)

### Community 20 - "UploadedDocument"
Cohesion: 0.12
Nodes (16): UploadedDocument, SearchResult, document_view(), DocumentValidationError, store_document(), KnowledgeDocumentIndex, _abandoned(), _error_cost() (+8 more)

### Community 21 - "web/package.json"
Cohesion: 0.08
Nodes (24): jsdom, @workspace/ui, eslint, @eslint/js, eslint-plugin-react-hooks, eslint-plugin-react-refresh, globals, @hugeicons/core-free-icons (+16 more)

### Community 22 - "test_recovery_regressions.py"
Cohesion: 0.22
Nodes (12): command(), create(), test_actual_app_restart_reconciles_failed_placeholder(), test_failed_review_retry_cannot_reopen_submitted_session(), test_original_payload_identity_survives_sanitization(), test_publication_failure_is_retryable_without_restart(), fail_once(), test_receipt_reference_is_preserved() (+4 more)

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
Cohesion: 0.21
Nodes (11): disableTransitionsTemporarily(), getSystemTheme(), isEditableTarget(), isTheme(), ResolvedTheme, Theme, THEME_VALUES, ThemeProvider() (+3 more)

### Community 28 - "test_embeddings.py"
Cohesion: 0.08
Nodes (43): EmbeddingBatch, EmbeddingError, _nonnegative_number(), OpenRouterEmbedder, _ordered_vectors(), _response_cost(), Embeddings, test_lock_serializes_operations_and_submit_waits_for_inflight_search() (+35 more)

### Community 29 - "Classify and Extract Prompts"
Cohesion: 0.31
Nodes (9): extract, gemini_classify, Pipeline Graph Orchestration, jev_classify, prepare, Gemini Classify Prompt v1, Gemini Extract Prompt v1, GeminiClassifier (+1 more)

### Community 30 - "test_draft_tools.py"
Cohesion: 0.11
Nodes (32): IncidentRow, TicketRow, TransactionRow, api(), ErrorEmbedder, settings(), sf(), test_all_eight_tools_and_seven_parallel_calls_execute_only_six() (+24 more)

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
Nodes (33): FakeEmbedder, GatedEmbedder, LateEmbedder, PaidEmbedder, count_chunks(), settings(), test_category_filters_include_general_policies_and_validate_tags(), test_claim_locks_source_even_before_index_row_exists() (+25 more)

### Community 36 - "web/components.json"
Cohesion: 0.10
Nodes (19): aliases, components, hooks, lib, ui, utils, iconLibrary, menuAccent (+11 more)

### Community 38 - "fakes.py"
Cohesion: 0.11
Nodes (27): LLMUnavailable, Sample, ExtractedField, FieldPick, FieldExtractor, combine(), merge_picks(), _field() (+19 more)

### Community 39 - "ui/components.json"
Cohesion: 0.10
Nodes (19): aliases, components, hooks, lib, ui, utils, iconLibrary, menuAccent (+11 more)

### Community 40 - "Settings"
Cohesion: 0.11
Nodes (11): Settings, test_blank_intake_model_is_rejected(), test_non_positive_image_limit_is_rejected(), test_relative_upload_directory_is_rooted_in_the_repository(), test_settings_validation_is_safe_field_diagnostic_exit_2(), test_defaults(), test_drafting_configuration_cannot_bypass_hard_limits(), test_drafting_limits_load_from_environment() (+3 more)

### Community 41 - "fact"
Cohesion: 0.24
Nodes (32): Analysis, ReviewText, InvalidEvidence, _check_reference(), merge_analysis(), checked_update(), _validate_fact(), context() (+24 more)

### Community 43 - "Human Review Gate"
Cohesion: 0.25
Nodes (4): support CLI, Support Workspace UI Plan, Review API, Workspace UI Verification

### Community 44 - "compilerOptions"
Cohesion: 0.12
Nodes (16): compilerOptions, allowImportingTsExtensions, erasableSyntaxOnly, lib, module, moduleDetection, noEmit, noFallthroughCasesInSwitch (+8 more)

### Community 46 - "agent.py"
Cohesion: 0.07
Nodes (15): DraftResult, _Nodes, _error_cost(), _number(), DraftToolLimit, Drafter, NullDrafter, UnavailableDrafter (+7 more)

### Community 47 - "compilerOptions"
Cohesion: 0.12
Nodes (16): compilerOptions, allowImportingTsExtensions, erasableSyntaxOnly, lib, module, moduleDetection, noEmit, noFallthroughCasesInSwitch (+8 more)

### Community 48 - "support_test"
Cohesion: 0.12
Nodes (18): index_deadlines(), support_test(), Evidence by layer, Known limitations and remaining work, Repeatable local walkthrough, Synthetic demo readiness, Commands and automated verification — historical Task 8, Corpus and actual retrieval (+10 more)

### Community 57 - "parse_document"
Cohesion: 0.11
Nodes (29): TextChunk, _append_chunks(), _check_extracted_size(), DocumentParseError, parse_document(), _parse_pdf(), make_pdf(), test_arabic_text_and_bom_are_preserved() (+21 more)

### Community 58 - "submission.py"
Cohesion: 0.14
Nodes (9): Receipt, IntakeOperationRow, IntakeRepository, processing_status(), current_session_view(), SubmissionResult, SubmissionService, make_intake_service() (+1 more)

### Community 59 - "intake/repository.py"
Cohesion: 0.14
Nodes (21): _display_name(), CustomerReview, IntakeAttachmentRow, IntakeMessageRow, IntakeSessionRow, assert_same_operation(), _attachment(), customer_review() (+13 more)

### Community 60 - "RunRow"
Cohesion: 0.15
Nodes (14): get_run(), list_runs(), start_run(), BatchInput, RunRow, intake_result_view(), model_ids(), run_job() (+6 more)

### Community 61 - "workspace-ui.tsx"
Cohesion: 0.11
Nodes (19): ConfirmDialog(), FilterSelect(), badgeVariants, Button(), buttonVariants, Dialog(), DialogContent(), DialogDescription() (+11 more)

### Community 62 - "investigation.py"
Cohesion: 0.16
Nodes (14): TxnRecord, parse_dt(), DraftToolInputError, _datetime(), _days(), _field(), _involves(), _phone() (+6 more)

### Community 63 - "test_llm.py"
Cohesion: 0.13
Nodes (11): GeminiStructuredLLM, make_gemini_llm(), _llm(), _S, test_draft_model_uses_millisecond_timeout_and_disables_sdk_retries(), test_openrouter_reported_cost_takes_precedence_over_token_estimate(), test_openrouter_retry_budget_is_bounded(), test_openrouter_structured_samples_use_configured_key_and_validate_output() (+3 more)

### Community 64 - "tasks"
Cohesion: 0.12
Nodes (16): dependsOn, inputs, outputs, cache, persistent, dependsOn, dependsOn, $schema (+8 more)

### Community 65 - "PipelineTrace.tsx"
Cohesion: 0.14
Nodes (14): Task 8: Employee evidence panel and processing state, source, STAGE_NODES, timing(), canReview(), REVIEWABLE, renderableTrace(), reviewEvidence() (+6 more)

### Community 66 - "IntakePage.tsx"
Cohesion: 0.12
Nodes (19): Global Constraints, Intake Chat UI Implementation Plan, Task 1: Put the summary and receipt in the thread, Task 2: Put screenshots inside the composer, Task 3: Apply the workspace chat styles, Task 4: Check the page in the browser, 4. Components, App() (+11 more)

### Community 67 - "test_handoff.py"
Cohesion: 0.13
Nodes (17): dispatch_intake(), _amount(), analyze(), complete_conversation(), _dated(), _message(), _opening(), _png() (+9 more)

### Community 68 - "PipelineState"
Cohesion: 0.11
Nodes (18): 10. Remaining demo roadmap, 1. Intent and acceptance criteria, 3. Provider and configuration, 4. Knowledge ingestion and persistence, 5. Retrieval and evidence, 6. Bounded investigation agent, 7. Draft guardrails and failure outcomes, 8. Pipeline, API, CLI and UI integration (+10 more)

### Community 69 - "datetime"
Cohesion: 0.11
Nodes (12): get_session(), get_result(), list_results(), read_intake_attachment(), review_result(), ReviewInput, Base, ReviewRow (+4 more)

### Community 70 - "normalize.py"
Cohesion: 0.19
Nodes (17): detect_arabizi(), fold_arabic(), has_latin_mix(), _latin_words(), mask_cards(), normalize(), sanitize_for_storage(), to_ascii_digits() (+9 more)

### Community 71 - "knowledge.py"
Cohesion: 0.12
Nodes (14): delete_document(), download_document(), index_document(), list_chunks(), list_documents(), _require_provider(), search_knowledge(), upload_document() (+6 more)

### Community 72 - "lookup.py"
Cohesion: 0.17
Nodes (14): _as_date(), _iqd_amount(), match_transaction(), TransactionRepo, _ex(), _match(), test_ambiguous_then_disambiguated_by_counterpart(), test_amount_and_date_mismatch() (+6 more)

### Community 73 - "Credentials"
Cohesion: 0.18
Nodes (7): Credentials, SessionView, IntakeService, _payload(), test_concurrent_submit_dispatches_once(), test_second_request_id_reuses_the_approved_review(), test_submission_replay_creates_one_ticket()

### Community 74 - "lib/types.ts"
Cohesion: 0.10
Nodes (33): acceptIndexRequest(), canRequestIndex(), PendingIndexes, persistPendingIndexes(), pollKnowledge(), refresh(), stop(), PollOptions (+25 more)

### Community 75 - "test-kb/README.md"
Cohesion: 0.18
Nodes (5): Fictional RAG walkthrough inputs, توثيق الحساب — سياسة خيالية للعرض التجريبي, الاستفسار الآمن من الدعم — سياسة خيالية للعرض التجريبي, استعادة الدخول — سياسة خيالية للعرض التجريبي, الطلبات غير الواضحة وخارج النطاق — سياسة خيالية للعرض التجريبي

### Community 76 - "pipeline/graph.py"
Cohesion: 0.08
Nodes (33): _run_with_db(), create_run(), finish_run(), load_incidents(), load_transactions(), save_outcomes(), SqlTransactionRepo, _to_record() (+25 more)

### Community 77 - "build_pipeline"
Cohesion: 0.12
Nodes (20): build_pipeline(), ConfigError, make_jev_client(), GeminiAnalysis, FakeStructuredLLM, ScriptedChat, test_config_error_exits_2(), boom() (+12 more)

### Community 79 - "devDependencies"
Cohesion: 0.12
Nodes (16): devDependencies, eslint, @eslint/js, eslint-plugin-react-hooks, eslint-plugin-react-refresh, globals, prettier, prettier-plugin-tailwindcss (+8 more)

### Community 80 - "judge-demo.ar.md"
Cohesion: 0.14
Nodes (13): أعطال التطبيق — سياسة خيالية للعرض التجريبي, استرجاع مبلغ شراء — سياسة خيالية للعرض التجريبي, استعادة الدخول — سياسة خيالية للعرض التجريبي, الاستفسار الآمن من الدعم — سياسة خيالية للعرض التجريبي, الاستفسار المؤقت للدعم في المهمة ٨ — سياسة خيالية للعرض التجريبي, التحويل المعلّق — سياسة خيالية للعرض التجريبي, التحويل لمستلم بالخطأ — سياسة خيالية للعرض التجريبي, الطلبات غير الواضحة وخارج النطاق — سياسة خيالية للعرض التجريبي (+5 more)

### Community 93 - "factory.py"
Cohesion: 0.11
Nodes (20): StructuredLLM, Candidates, ClassificationResult, ClassifierOutput, NormalizedTicket, Classifier, GeminiClassifier, GeminiExtractor (+12 more)

### Community 94 - "devDependencies"
Cohesion: 0.11
Nodes (19): devDependencies, eslint, @eslint/js, eslint-plugin-react-hooks, eslint-plugin-react-refresh, globals, jsdom, @tailwindcss/vite (+11 more)

### Community 95 - "devDependencies"
Cohesion: 0.14
Nodes (14): devDependencies, eslint, @eslint/js, eslint-plugin-react-hooks, eslint-plugin-react-refresh, globals, tailwindcss, @tailwindcss/vite (+6 more)

### Community 96 - "guardrails.py"
Cohesion: 0.15
Nodes (15): Passage, normalize_phone(), parse_amount(), _iso(), normalize_value(), check_draft(), _citation_findings(), _exact_amount() (+7 more)

### Community 97 - "ticket-flow.ts"
Cohesion: 0.06
Nodes (75): Global Constraints, Task 1: Sentence catalog, Task 2: Which step is open, Task 3: Received, produced, and drafting events, Task 4: Mermaid source, Task 5: Draw the charts on the ticket page, Ticket Flow Charts Implementation Plan, PipelineTrace() (+67 more)

### Community 98 - "NewBatchPage.tsx"
Cohesion: 0.20
Nodes (14): Tabs(), TabsContent(), TabsList(), tabsListVariants, TabsTrigger(), Textarea(), readReport(), exampleTickets (+6 more)

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
Cohesion: 0.26
Nodes (9): canonical_digits(), normalize_reported_date(), _compact(), _normalize_precise(), _own_phone_quote(), _value_supported(), test_ambiguous_slash_date_is_not_fabricated(), test_utc_instant_just_before_baghdad_midnight_stays_on_the_previous_day() (+1 more)

### Community 104 - "dependencies"
Cohesion: 0.15
Nodes (13): dependencies, @base-ui/react, class-variance-authority, cn, @fontsource/tajawal, @fontsource-variable/plus-jakarta-sans, @hugeicons/core-free-icons, @hugeicons/react (+5 more)

### Community 105 - "compilerOptions"
Cohesion: 0.17
Nodes (11): compilerOptions, jsx, lib, module, moduleResolution, outDir, skipLibCheck, strict (+3 more)

### Community 106 - "KnowledgeError"
Cohesion: 0.12
Nodes (5): KnowledgeError, KnowledgeExecutionError, test_db_deadline_cancelled_publication_cannot_commit_late(), test_db_deadline_is_cumulative_across_publication_statements(), changed_index()

### Community 107 - "IntakePage.test.tsx"
Cohesion: 0.12
Nodes (18): HTTP contract (implemented in Tasks 4–5), Task 6: Customer API client and resumable UI state, Task 9: End-to-end handoff, live vision evidence and runbook, @testing-library/user-event, emptySession(), fakeApi(), review, attachment (+10 more)

### Community 108 - "test_final_fix_handoff.py"
Cohesion: 0.10
Nodes (22): RagDrafter, DraftExecutionError, process_batch(), assert_completed_evidence(), faulty_knowledge(), outer_deadlines(), PaidEmbeddings, runner_env() (+14 more)

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

### Community 119 - "rag_fakes.py"
Cohesion: 0.15
Nodes (12): make_draft_model(), Checker, response_payload(), run_provider_pipeline(), send(), search_response(), test_empty_choices_escalates_and_keeps_paid_response_usage(), test_failed_response_id_is_deduplicated_against_earlier_success() (+4 more)

### Community 120 - "scripts"
Cohesion: 0.50
Nodes (4): scripts, format, lint, typecheck

### Community 122 - "context"
Cohesion: 0.20
Nodes (17): Question, _asked_already(), asks_for_secret(), assess_readiness(), _can_ask(), canonical_category(), choose_question(), _fallback() (+9 more)

### Community 123 - "IntakeState"
Cohesion: 0.11
Nodes (19): IntakeState, QuestionRecord, ReviewSnapshot, TurnContext, IntakeGraph, _invitation(), validate(), material_keys() (+11 more)

### Community 124 - "AttachmentStore"
Cohesion: 0.16
Nodes (18): AttachmentStore, ImageRejected, NotOwned, builder(), png_bytes(), repo(), store(), test_active_turn_rejects_upload() (+10 more)

### Community 126 - "find_candidates"
Cohesion: 0.28
Nodes (11): Candidate, _add(), find_candidates(), _overlaps(), test_amount_forms(), test_arabic_indic_amount_not_confused_with_phone(), test_dates_absolute_and_weekday(), test_dedupes_repeated_values() (+3 more)

### Community 127 - "test_gemini.py"
Cohesion: 0.31
Nodes (12): ExtractedSpan, _Fields, GeminiFields, _a(), _classify(), test_all_samples_failing_raises(), test_extractor_requests_only_named_fields(), test_failed_samples_count_against_confidence() (+4 more)

### Community 128 - "workspace.py"
Cohesion: 0.27
Nodes (7): health(), insights(), workspace(), ingest(), latest_results_query(), Artifacts, servers and remaining concerns, start()

### Community 129 - "intake/model.py"
Cohesion: 0.11
Nodes (27): Attachment, ImageInput, ModelCall, ModelUnavailable, _analysis_prompt(), _bounded_context(), _guard_size(), ModelBudget (+19 more)

### Community 130 - "Plan 3 RAG Drafting Implementation Plan"
Cohesion: 0.20
Nodes (10): Completion and review record — 2026-10-17, Execution handoff, File map and shared interfaces, Global Constraints, Plan 3 RAG Drafting Implementation Plan, Plan self-review, Review Focus, Task 6: API/CLI indexing and persisted citation projection (+2 more)

### Community 131 - "intake.py"
Cohesion: 0.15
Nodes (20): create_session(), _credentials(), _dump(), get_session(), post_message(), read_attachment(), remove_attachment(), request_review() (+12 more)

### Community 132 - "build_tools"
Cohesion: 0.17
Nodes (5): build_tools(), flag(), retrieve(), status(), _error_cost()

### Community 133 - "KnowledgeService"
Cohesion: 0.09
Nodes (8): Embedder, KnowledgeChunk, _check_deadline(), _Claim, _consume(), _DatabaseCall, IndexAttemptLostError, KnowledgeService

### Community 134 - "cli.py"
Cohesion: 0.10
Nodes (19): _command_settings(), ingest_kb_cmd(), init_db_cmd(), Mode, run_batch_cmd(), _run_in_memory(), seed_db_cmd(), _sessionmaker() (+11 more)

### Community 135 - "Customer Conversation Intake Implementation Plan"
Cohesion: 0.20
Nodes (8): Completion audit — 2026-10-18, Customer Conversation Intake Implementation Plan, Execution conventions and repository baseline, File map and dependency order, Global Constraints, Plan review and execution handoff, Review Focus, Spec coverage and acceptance map

### Community 136 - "main.py"
Cohesion: 0.07
Nodes (24): init_db(), make_engine(), make_sessionmaker(), reset_db(), upgrade_workspace_schema(), create_app(), lifespan(), recover() (+16 more)

### Community 137 - "KnowledgePage"
Cohesion: 0.60
Nodes (5): beginMutation(), deleteDocument(), finishMutation(), indexDocument(), upload()

### Community 138 - "intake/api.ts"
Cohesion: 0.15
Nodes (13): createIntakeApi(), IntakeRequestError, isRecord(), parseJson(), parseReceipt(), parseSession(), readError(), stringList() (+5 more)

### Community 139 - "DraftContext"
Cohesion: 0.22
Nodes (3): _Execution, DraftContext, Task 3: Ticket-scoped investigation and all eight tools

### Community 140 - "test_dbapi_commit_handoff_arbitrates_cancellation"
Cohesion: 0.47
Nodes (4): test_dbapi_commit_handoff_arbitrates_cancellation(), gate(), gate_before_dbapi(), gate_inside_dbapi()

### Community 149 - "resolve_date"
Cohesion: 0.36
Nodes (4): resolve_date(), _safe_date(), test_resolve(), test_unresolvable_is_none()

### Community 151 - "errors.py"
Cohesion: 0.39
Nodes (5): IntakeError, OperationConflict, StaleReview, TurnBusy, Task 1: Durable intake sessions and ownership

### Community 152 - "_bounded"
Cohesion: 0.22
Nodes (6): DraftAlreadySubmitted, _bounded(), visit(), guarded(), invoke(), _json()

### Community 154 - "Ticket flow charts"
Cohesion: 0.22
Nodes (8): 1. Outcome, 2. Scope, 5. Language, 6. How a result becomes the charts, 7. Sentences, 8. Tests, 9. Files, Ticket flow charts

### Community 156 - "employee-frontend/src/components/theme-provider.tsx"
Cohesion: 0.21
Nodes (11): disableTransitionsTemporarily(), getSystemTheme(), isEditableTarget(), isTheme(), ResolvedTheme, Theme, THEME_VALUES, ThemeProvider() (+3 more)

### Community 157 - "recover_intake_processing"
Cohesion: 0.48
Nodes (5): recover_intake_processing(), _submit(), test_committed_but_unscheduled_ticket_survives_recovery(), test_failed_outcome_save_preserves_placeholder_and_reconciles_counts(), test_processing_ticket_rejects_review()

### Community 158 - "load_taxonomy"
Cohesion: 0.08
Nodes (26): LookupResult, decide(), empty_ticket_decision(), merge_reasons(), note_for(), _unique(), Category, load_taxonomy() (+18 more)

### Community 161 - "Customer intake chat layout"
Cohesion: 0.33
Nodes (5): 1. Outcome, 2. Scope, 3. Layout, 5. Checks, Customer intake chat layout

## Ambiguous Edges - Review These
- `Fraud Report` → `Plan 1 Live Smoke`  [AMBIGUOUS]
  README.md · relation: conceptually_related_to

## Knowledge Gaps
- **91 isolated node(s):** `zaincash-support`, `@base-ui/react`, `@fontsource-variable/plus-jakarta-sans`, `@fontsource/tajawal`, `@tailwindcss/vite` (+86 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 1011 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **48 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `HTTP contract (implemented in Tasks 4–5)` connect `IntakePage.test.tsx` to `guardrails.py`, `intake/model.py`, `intake/types.ts`, `TurnStore`, `PipelineTrace.tsx`, `Customer Conversation Intake Implementation Plan`, `errors.py`, `RunRow`?**
  _High betweenness centrality (0.096) - this node is a cross-community bridge._
- **Are the 33 inferred relationships involving `Settings` (e.g. with `_command_settings()` and `_run_in_memory()`) actually correct?**
  _`Settings` has 33 INFERRED edges - model-reasoned connections that need verification._
- **What connects `zaincash-support`, `@base-ui/react`, `@fontsource-variable/plus-jakarta-sans` to the rest of the system?**
  _91 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `intake/types.ts` be split into smaller, more focused modules?**
  _Cohesion score 0.10121951219512196 - nodes in this community are weakly interconnected._
- **Why does `Task 3: Received, produced, and drafting events` connect `ticket-flow.ts` to `pytest`, `QueuePage.tsx`?**
  _High betweenness centrality (0.075) - this node is a cross-community bridge._
- **Are the 24 inferred relationships involving `KnowledgeService` (e.g. with `Settings` and `UploadedDocument`) actually correct?**
  _`KnowledgeService` has 24 INFERRED edges - model-reasoned connections that need verification._

### Low-confidence Hints
_AMBIGUOUS edges — the extractor was unsure. Verify before acting on these._

- **What is the exact relationship between `Fraud Report` and `Plan 1 Live Smoke`?**
  _Edge tagged AMBIGUOUS (relation: conceptually_related_to) - confidence is low._