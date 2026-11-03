# Graph Report - zaincash-support  (2026-11-03)

## Corpus Check
- 342 files · ~312,012 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 28 file(s) not represented in the graph (top: (none) 17, .jsonl 4, .css 4)

## Summary
- 3210 nodes · 9867 edges · 177 communities (126 shown, 51 thin omitted)
- Extraction: 88% EXTRACTED · 12% INFERRED · 0% AMBIGUOUS · INFERRED: 1193 edges (avg confidence: 0.93)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `f3ff14f1`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- NewBatchPage.tsx
- intake/types.ts
- pytest
- TurnStore
- investigation.py
- agent.py
- useCopy
- Customer conversation intake for ZainCash support
- TicketReviewPage.tsx
- IntakeController
- FakeJevRunnable
- test_rag_api.py
- employee-frontend/package.json
- QueuePage.tsx
- Support Taxonomy Categories
- ui/package.json
- employee-frontend/src/App.tsx
- users-frontend/package.json
- make_ticket
- test_draft_guardrails.py
- web/package.json
- test_recovery_regressions.py
- compilerOptions
- employee-frontend/components.json
- agent-chat.tsx
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
- attachments.py
- contracts.ts
- rules.py
- workspace-ui.tsx
- tools.py
- intake/types.ts
- tasks
- knowledge.py
- intake/contracts.py
- test_handoff.py
- PipelineState
- results.py
- build_tools
- taxonomy.py
- test_submission.py
- UploadedDocument
- use-knowledge-library.ts
- test-kb/README.md
- format.ts
- Embedder
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
- locale.tsx
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
- dispatch_intake
- IntakePage.test.tsx
- test_final_fix_handoff.py
- ZainCash Support Workspace
- negative/README.md
- scripts
- scripts
- compilerOptions
- Maintainability and stale-code refactor — design specification
- dependencies
- web/tsconfig.json
- employee-frontend/tsconfig.json
- exports
- Review Focus
- scripts
- users-frontend/README.md
- intake/contracts.py
- TurnContext
- ingest.py
- ar/failed_transfer.md
- guardrails.py
- test_cli.py
- session.ts
- intake/model.py
- test_llm.py
- intake.py
- Review Focus
- _DatabaseCall
- ReviewEditor
- Customer Conversation Intake Implementation Plan
- find_candidates
- SubmissionService
- FakeXHR
- fakes.py
- agent.py
- database.py
- test_dbapi_commit_handoff_arbitrates_cancellation
- resolve_date
- 5. Backend design
- components-ai-thought-chain.tsx
- kb/service.py
- intake/README.md
- TicketInput
- main.py
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
- LateEmbedder
- test_dbapi_commit_handoff_arbitrates_cancellation
- DraftSubmission
- 6. Employee frontend design
- _error_cost
- collapsible.tsx

## God Nodes (most connected - your core abstractions)
1. `Settings` - 109 edges
2. `KnowledgeService` - 80 edges
3. `IntakeController` - 54 edges
4. `fact()` - 53 edges
5. `PipelineState` - 48 edges
6. `context()` - 48 edges
7. `draft_state()` - 45 edges
8. `message()` - 43 edges
9. `build_pipeline()` - 42 edges
10. `make_ticket()` - 42 edges

## Surprising Connections (you probably didn't know these)
- `Repeatable local walkthrough` --references--> `Settings`  [INFERRED]
  docs/demo-readiness.md → backend/app/config.py
- `Task 9: Repair the Five-Record JSONL Baseline Fixture` --references--> `load_jsonl()`  [INFERRED]
  docs/superpowers/plans/2026-11-02-backend-maintainability.md → backend/app/ingest.py
- `5.3 Knowledge-service boundary` --references--> `_DatabaseCall`  [INFERRED]
  docs/superpowers/specs/2026-11-02-maintainability-refactor-design.md → backend/app/kb/database.py
- `الأصل ونتيجة التحقق` --references--> `parse_document()`  [INFERRED]
  data/test-kb/README.md → backend/app/kb/parse.py
- `Task 6: API/CLI indexing and persisted citation projection` --references--> `KnowledgeService`  [INFERRED]
  docs/superpowers/plans/2026-10-17-plan3-rag-drafting.md → backend/app/kb/service.py

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **Cascade Classification Path** — docs_superpowers_specs_2026_10_07_support_pipeline_design_cascade, docs_superpowers_plans_2026_10_07_plan1_core_pipeline_part2_jev_classifier, docs_superpowers_plans_2026_10_07_plan1_core_pipeline_part2_gemini_classifier, docs_superpowers_plans_2026_10_07_plan1_core_pipeline_part2_cascade_combine, readme_human_approval [EXTRACTED 1.00]
- **Drafting Agent Toolset** — backend_app_pipeline_runner_lookup_transaction, backend_app_pipeline_runner_search_transactions, backend_app_pipeline_runner_get_customer_recent_transactions, backend_app_pipeline_runner_get_customer_ticket_history, backend_app_pipeline_runner_check_service_status, backend_app_pipeline_runner_search_knowledge_base, backend_app_pipeline_runner_flag_for_human, backend_app_pipeline_runner_submit_draft [EXTRACTED 1.00]
- **Ticket Processing Stage Flow** — backend_app_pipeline_runner_prepare, backend_app_pipeline_runner_jev_classify, backend_app_pipeline_runner_gemini_classify, backend_app_pipeline_runner_extract, backend_app_pipeline_runner_lookup, backend_app_pipeline_runner_decide, backend_app_pipeline_runner_draft [EXTRACTED 1.00]

## Communities (177 total, 51 thin omitted)

### Community 0 - "NewBatchPage.tsx"
Cohesion: 0.14
Nodes (18): Metric(), Badge(), badgeVariants, Tabs(), TabsContent(), TabsList(), tabsListVariants, TabsTrigger() (+10 more)

### Community 1 - "intake/types.ts"
Cohesion: 0.14
Nodes (15): Task 4: Make pending operations discriminated and use one request identity, IntakeApi, parseJson(), readError(), INTAKE_FALLBACK_MESSAGE, IntakeRequestError, ControllerState, fileIdentity() (+7 more)

### Community 2 - "pytest"
Cohesion: 0.23
Nodes (33): answer(), call(), draft_state(), script(), submit(), drafter(), events(), test_anthropic_fallback_prices_and_provider_cost_precedence() (+25 more)

### Community 3 - "TurnStore"
Cohesion: 0.12
Nodes (24): OperationClaim, TurnResult, IntakeAttachmentRow, IntakeMessageRow, IntakeError, RevisionConflict, StaleReview, TurnBusy (+16 more)

### Community 4 - "investigation.py"
Cohesion: 0.17
Nodes (12): parse_dt(), _datetime(), _days(), _field(), _involves(), _phone(), _phones(), _record() (+4 more)

### Community 5 - "agent.py"
Cohesion: 0.15
Nodes (8): _error_cost(), _ModelUsage, _number(), RagDrafter, DraftContext, DraftExecutionError, test_real_search_fault_carries_safe_draft_execution_error(), Task 11: Use Draft-Model-Specific Fallback Token Prices

### Community 6 - "useCopy"
Cohesion: 0.17
Nodes (36): Task 5: Extract presentational DocumentList and KnowledgeReadiness components, 6.4 Focused view extraction, navigation, WorkspaceLayout(), EmptyState(), ErrorState(), LoadingState(), Button() (+28 more)

### Community 7 - "Customer conversation intake for ZainCash support"
Cohesion: 0.06
Nodes (31): 10. Verification and acceptance criteria, 11. Delivery and review, 1. Outcome and agreed requirements, 2. Current implementation and integration points, 3. Approach and boundaries, 4. Conversation state and turn flow, 5. Facts, evidence, and readiness, 6. Language and screenshot behavior (+23 more)

### Community 8 - "TicketReviewPage.tsx"
Cohesion: 0.07
Nodes (32): Task 8: Employee evidence panel and processing state, Task 2: Migrate active TicketFlow coverage, then retire the legacy trace/chart cluster, Task 4: Extract and test the pure queue projection, projectQueue(), QueueFilters, QueueProjection, QueueTab, source (+24 more)

### Community 9 - "IntakeController"
Cohesion: 0.17
Nodes (7): Task 6: Customer API client and resumable UI state, Task 1: Cleanup-first removal of reference-verified dead code and dependencies, IntakeController, isConflict(), isOffline(), safeMessage(), Language

### Community 10 - "FakeJevRunnable"
Cohesion: 0.10
Nodes (19): CredentialCheck, CredentialChecker, DegradedCredentialChecker, _finite_nonnegative(), _get(), JevCredentialChecker, ResponseRunnable, test_bad_usage_cannot_poison_cost() (+11 more)

### Community 11 - "test_rag_api.py"
Cohesion: 0.10
Nodes (24): KnowledgeExecutionError, client(), evidence_client(), pipeline(), submit(), test_actual_guardrail_failure_is_separate_from_reply(), test_concurrent_index_requests_share_active_work(), test_disabled_or_missing_provider_stores_without_indexing() (+16 more)

### Community 12 - "employee-frontend/package.json"
Cohesion: 0.06
Nodes (30): @base-ui/react, class-variance-authority, cn, eslint, @eslint/js, eslint-plugin-react-hooks, eslint-plugin-react-refresh, @fontsource/tajawal (+22 more)

### Community 14 - "QueuePage.tsx"
Cohesion: 0.18
Nodes (26): Task 3: Split RunDetailPage and introduce bounded run-result loading, PageHeader(), PriorityBadge(), StatusBadge(), Table(), TableBody(), TableCell(), TableHead() (+18 more)

### Community 15 - "Support Taxonomy Categories"
Cohesion: 0.21
Nodes (22): lookup, Account KYC, Account & Security, Agent Dispute, Agent Network, App Bug, Bill Payment, Card Issue (+14 more)

### Community 16 - "ui/package.json"
Cohesion: 0.08
Nodes (24): @base-ui/react, class-variance-authority, cn, eslint, @eslint/js, eslint-plugin-react-hooks, eslint-plugin-react-refresh, @fontsource/tajawal (+16 more)

### Community 17 - "employee-frontend/src/App.tsx"
Cohesion: 0.17
Nodes (14): App(), EvaluationPage, InsightsPage, KnowledgePage, NewBatchPage, QueuePage, RunDetailPage, RunsPage (+6 more)

### Community 18 - "users-frontend/package.json"
Cohesion: 0.08
Nodes (23): turbo, devDependencies, prettier, prettier-plugin-tailwindcss, turbo, typescript, engines, node (+15 more)

### Community 19 - "make_ticket"
Cohesion: 0.15
Nodes (30): build_graph(), PipelineDeps, load_taxonomy(), tax(), FakeClassifier, make_output(), make_ticket(), intake_client() (+22 more)

### Community 20 - "test_draft_guardrails.py"
Cohesion: 0.13
Nodes (28): requests_credentials(), check(), state(), test_aggregation_is_deduplicated_and_has_no_state_side_effects(), test_amount_occurrences_keep_their_own_currency_and_sign(), test_avoid_sharing_warning_does_not_excuse_a_later_request(), test_candidate_prompt_limit_does_not_hide_later_ungrounded_references(), test_candidate_transactions_cannot_authorize_reply_evidence() (+20 more)

### Community 21 - "web/package.json"
Cohesion: 0.08
Nodes (25): jsdom, @testing-library/jest-dom, @testing-library/react, @testing-library/user-event, @workspace/ui, eslint, @eslint/js, eslint-plugin-react-hooks (+17 more)

### Community 22 - "test_recovery_regressions.py"
Cohesion: 0.09
Nodes (24): _command_settings(), ingest_kb_cmd(), init_db_cmd(), Mode, run_batch_cmd(), _run_in_memory(), _run_with_db(), seed_db_cmd() (+16 more)

### Community 23 - "compilerOptions"
Cohesion: 0.08
Nodes (23): compilerOptions, allowArbitraryExtensions, allowImportingTsExtensions, erasableSyntaxOnly, jsx, lib, module, moduleDetection (+15 more)

### Community 24 - "employee-frontend/components.json"
Cohesion: 0.09
Nodes (21): aliases, components, hooks, lib, ui, utils, iconLibrary, menuAccent (+13 more)

### Community 25 - "agent-chat.tsx"
Cohesion: 0.15
Nodes (23): clsx, tailwind-merge, AgentChatProps, AgentMessage, AssistantText(), AttachedFile, AttachedImage, ChatStatus (+15 more)

### Community 26 - "compilerOptions"
Cohesion: 0.09
Nodes (22): compilerOptions, allowArbitraryExtensions, allowImportingTsExtensions, erasableSyntaxOnly, jsx, lib, module, moduleDetection (+14 more)

### Community 27 - "web/src/components/theme-provider.tsx"
Cohesion: 0.16
Nodes (13): App(), controller, disableTransitionsTemporarily(), getSystemTheme(), isEditableTarget(), isTheme(), ResolvedTheme, Theme (+5 more)

### Community 28 - "EmbeddingError"
Cohesion: 0.08
Nodes (43): EmbeddingBatch, EmbeddingError, _nonnegative_number(), OpenRouterEmbedder, _ordered_vectors(), _response_cost(), _percentile(), Embeddings (+35 more)

### Community 29 - "Classify and Extract Prompts"
Cohesion: 0.33
Nodes (7): extract, gemini_classify, Pipeline Graph Orchestration, jev_classify, prepare, GeminiClassifier, JevClassifier

### Community 30 - "test_draft_tools.py"
Cohesion: 0.12
Nodes (30): test_contracts_reject_extra_keys(), test_datetimes_must_be_timezone_aware(), ErrorEmbedder, test_all_eight_tools_and_seven_parallel_calls_execute_only_six(), test_context_copies_input_and_rejects_raising_hard_call_limit(), test_database_faults_remain_distinct_and_record_paid_search_cost(), test_discovered_ref_can_be_inspected_but_not_promoted_to_match(), test_exact_and_fuzzy_queries_are_scoped_and_never_confirm_candidates() (+22 more)

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
Cohesion: 0.15
Nodes (28): KnowledgeService, FakeEmbedder, GatedEmbedder, PaidEmbedder, count_chunks(), test_category_filters_include_general_policies_and_validate_tags(), test_claim_locks_source_even_before_index_row_exists(), test_competing_callers_refuse_active_attempt_and_release_transactions() (+20 more)

### Community 36 - "web/components.json"
Cohesion: 0.10
Nodes (19): aliases, components, hooks, lib, ui, utils, iconLibrary, menuAccent (+11 more)

### Community 38 - "jev.py"
Cohesion: 0.18
Nodes (14): Candidates, ClassificationResult, ClassifierOutput, NormalizedTicket, Classifier, build_order_check(), build_questions(), build_state() (+6 more)

### Community 39 - "ui/components.json"
Cohesion: 0.10
Nodes (19): aliases, components, hooks, lib, ui, utils, iconLibrary, menuAccent (+11 more)

### Community 40 - "Settings"
Cohesion: 0.11
Nodes (13): Settings, model_ids(), test_blank_intake_model_is_rejected(), test_non_positive_image_limit_is_rejected(), test_relative_upload_directory_is_rooted_in_the_repository(), test_anthropic_model_selects_the_draft_model_only(), test_defaults(), test_draft_token_prices_follow_the_selected_draft_model() (+5 more)

### Community 41 - "fact"
Cohesion: 0.29
Nodes (27): InvalidEvidence, merge_analysis(), checked_update(), context(), fact(), message(), proposal(), test_additional_issue_is_resolved_in_place_instead_of_appended() (+19 more)

### Community 43 - "Human Review Gate"
Cohesion: 0.25
Nodes (4): support CLI, Support Workspace UI Plan, Review API, Workspace UI Verification

### Community 44 - "compilerOptions"
Cohesion: 0.12
Nodes (16): compilerOptions, allowImportingTsExtensions, erasableSyntaxOnly, lib, module, moduleDetection, noEmit, noFallthroughCasesInSwitch (+8 more)

### Community 46 - "PipelineState"
Cohesion: 0.10
Nodes (14): DraftResult, _Nodes, Drafter, NullDrafter, UnavailableDrafter, PipelineState, draft(), draft() (+6 more)

### Community 47 - "compilerOptions"
Cohesion: 0.12
Nodes (16): compilerOptions, allowImportingTsExtensions, erasableSyntaxOnly, lib, module, moduleDetection, noEmit, noFallthroughCasesInSwitch (+8 more)

### Community 48 - "support_test"
Cohesion: 0.07
Nodes (29): ingest(), index_deadlines(), settings(), support_test(), expire_during_embedding(), Completion and review record — 2026-10-17, Execution handoff, File map and shared interfaces (+21 more)

### Community 57 - "parse_document"
Cohesion: 0.11
Nodes (29): TextChunk, _append_chunks(), _check_extracted_size(), DocumentParseError, parse_document(), _parse_pdf(), make_pdf(), test_arabic_text_and_bom_are_preserved() (+21 more)

### Community 58 - "attachments.py"
Cohesion: 0.09
Nodes (34): AttachmentStore, _display_name(), Credentials, SessionView, IntakeOperationRow, IntakeSessionRow, ImageRejected, NotOwned (+26 more)

### Community 59 - "contracts.ts"
Cohesion: 0.20
Nodes (27): Task 5: Add complete dependency-free API and persisted-session guards, createIntakeApi(), session, finiteNonnegative(), invalid(), isRecord(), language(), nullableString() (+19 more)

### Community 60 - "rules.py"
Cohesion: 0.14
Nodes (22): Decision, ExtractedField, LookupResult, _default_retry(), _retryable(), decide(), empty_ticket_decision(), merge_reasons() (+14 more)

### Community 61 - "workspace-ui.tsx"
Cohesion: 0.17
Nodes (16): ConfirmDialog(), FilterSelect(), Dialog(), DialogContent(), DialogDescription(), DialogFooter(), DialogHeader(), DialogOverlay() (+8 more)

### Community 62 - "tools.py"
Cohesion: 0.12
Nodes (15): DraftAlreadySubmitted, DraftToolLimit, _bounded(), visit(), guarded(), invoke(), _Flag, _History (+7 more)

### Community 63 - "intake/types.ts"
Cohesion: 0.08
Nodes (31): Global Constraints, Intake Chat UI Implementation Plan, Task 1: Put the summary and receipt in the thread, Task 2: Put screenshots inside the composer, Task 3: Apply the workspace chat styles, Task 4: Check the page in the browser, 1. Outcome, 2. Scope (+23 more)

### Community 64 - "tasks"
Cohesion: 0.11
Nodes (18): dependsOn, inputs, outputs, cache, persistent, dependsOn, dependsOn, $schema (+10 more)

### Community 65 - "knowledge.py"
Cohesion: 0.09
Nodes (17): get_session(), delete_document(), download_document(), index_document(), list_chunks(), list_documents(), _require_provider(), search_knowledge() (+9 more)

### Community 66 - "intake/contracts.py"
Cohesion: 0.17
Nodes (14): _aware(), EvidenceRef, Fact, IntakeModel, Message, remove_attachment_evidence(), image_evidence(), test_removal_invalidates_every_image_only_fact_status() (+6 more)

### Community 67 - "test_handoff.py"
Cohesion: 0.25
Nodes (15): Analysis, _amount(), analyze(), complete_conversation(), _dated(), _message(), _opening(), _png() (+7 more)

### Community 68 - "PipelineState"
Cohesion: 0.11
Nodes (18): 10. Remaining demo roadmap, 1. Intent and acceptance criteria, 3. Provider and configuration, 4. Knowledge ingestion and persistence, 5. Retrieval and evidence, 6. Bounded investigation agent, 7. Draft guardrails and failure outcomes, 8. Pipeline, API, CLI and UI integration (+10 more)

### Community 69 - "results.py"
Cohesion: 0.12
Nodes (19): get_result(), list_results(), read_intake_attachment(), review_result(), health(), insights(), workspace(), ReviewRow (+11 more)

### Community 70 - "build_tools"
Cohesion: 0.11
Nodes (11): DraftToolInputError, build_tools(), flag(), retrieve(), status(), _error_cost(), Backend Maintainability Implementation Plan, Global Constraints (+3 more)

### Community 71 - "taxonomy.py"
Cohesion: 0.18
Nodes (6): most_urgent(), priority_rank(), TaxonomyError, taxonomy(), test_priority_helpers(), test_rejects_unknown_team()

### Community 72 - "test_submission.py"
Cohesion: 0.32
Nodes (4): _payload(), test_concurrent_submit_dispatches_once(), test_second_request_id_reuses_the_approved_review(), test_submission_replay_creates_one_ticket()

### Community 73 - "UploadedDocument"
Cohesion: 0.16
Nodes (13): UploadedDocument, document_view(), store_document(), KnowledgeDocumentIndex, ingest_one(), ingest_status(), test_db_deadline_cancelled_publication_cannot_commit_late(), test_db_deadline_is_cumulative_across_publication_statements() (+5 more)

### Community 74 - "use-knowledge-library.ts"
Cohesion: 0.23
Nodes (14): acceptIndexRequest(), canRequestIndex(), PendingIndexes, persistPendingIndexes(), pollKnowledge(), refresh(), stop(), PollOptions (+6 more)

### Community 75 - "test-kb/README.md"
Cohesion: 0.15
Nodes (6): Fictional RAG walkthrough inputs, توثيق الحساب — سياسة خيالية للعرض التجريبي, نزاع مع وكيل — سياسة خيالية للعرض التجريبي, الطلبات غير الواضحة وخارج النطاق — سياسة خيالية للعرض التجريبي, الاستفسار المؤقت للدعم في المهمة ٨ — سياسة خيالية للعرض التجريبي, التحويل لمستلم بالخطأ — سياسة خيالية للعرض التجريبي

### Community 76 - "format.ts"
Cohesion: 0.23
Nodes (16): Confidence(), intakeFixture, factValue(), IntakeEvidence(), Screenshot(), highlightedText(), SourceEvidence(), categories (+8 more)

### Community 79 - "devDependencies"
Cohesion: 0.12
Nodes (16): devDependencies, eslint, @eslint/js, eslint-plugin-react-hooks, eslint-plugin-react-refresh, globals, prettier, prettier-plugin-tailwindcss (+8 more)

### Community 80 - "judge-demo.ar.md"
Cohesion: 0.14
Nodes (13): أعطال التطبيق — سياسة خيالية للعرض التجريبي, استرجاع مبلغ شراء — سياسة خيالية للعرض التجريبي, استعادة الدخول — سياسة خيالية للعرض التجريبي, الاستفسار الآمن من الدعم — سياسة خيالية للعرض التجريبي, الاستفسار المؤقت للدعم في المهمة ٨ — سياسة خيالية للعرض التجريبي, التحويل المعلّق — سياسة خيالية للعرض التجريبي, التحويل لمستلم بالخطأ — سياسة خيالية للعرض التجريبي, الطلبات غير الواضحة وخارج النطاق — سياسة خيالية للعرض التجريبي (+5 more)

### Community 93 - "locale.tsx"
Cohesion: 0.15
Nodes (12): LanguageToggle(), DocumentListProps, knowledgeDocument(), listProps(), originalLocale, applyDocumentLocale(), copies, listeners (+4 more)

### Community 94 - "devDependencies"
Cohesion: 0.11
Nodes (19): devDependencies, eslint, @eslint/js, eslint-plugin-react-hooks, eslint-plugin-react-refresh, globals, jsdom, @tailwindcss/vite (+11 more)

### Community 95 - "devDependencies"
Cohesion: 0.17
Nodes (12): devDependencies, eslint, @eslint/js, eslint-plugin-react-hooks, eslint-plugin-react-refresh, globals, tailwindcss, @types/node (+4 more)

### Community 96 - "normalize.py"
Cohesion: 0.15
Nodes (18): detect_arabizi(), fold_arabic(), has_latin_mix(), _latin_words(), normalize(), sanitize_for_storage(), mask_cards(), to_ascii_digits() (+10 more)

### Community 97 - "ticket-flow.ts"
Cohesion: 0.06
Nodes (60): Task 1: Sentence catalog, Task 2: Which step is open, Task 3: Received, produced, and drafting events, Task 4: Mermaid source, Task 5: Draw the charts on the ticket page, 1. Outcome, 2. Scope, 5. Language (+52 more)

### Community 98 - "review.py"
Cohesion: 0.16
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
Cohesion: 0.17
Nodes (15): canonical_digits(), normalize_reported_date(), _apply(), _check_reference(), _compact(), _newer_correction(), _normalize_precise(), _own_phone_quote() (+7 more)

### Community 104 - "dependencies"
Cohesion: 0.20
Nodes (10): dependencies, @base-ui/react, class-variance-authority, cn, @fontsource/tajawal, @fontsource-variable/plus-jakarta-sans, react, react-dom (+2 more)

### Community 105 - "compilerOptions"
Cohesion: 0.17
Nodes (11): compilerOptions, jsx, lib, module, moduleResolution, outDir, skipLibCheck, strict (+3 more)

### Community 106 - "dispatch_intake"
Cohesion: 0.39
Nodes (6): dispatch_intake(), test_review_to_employee_handoff(), _submit(), test_committed_but_unscheduled_ticket_survives_recovery(), test_failed_outcome_save_preserves_placeholder_and_reconciles_counts(), test_processing_ticket_rejects_review()

### Community 107 - "IntakePage.test.tsx"
Cohesion: 0.15
Nodes (21): HTTP contract (implemented in Tasks 4–5), Task 7: Bilingual customer chat, screenshots and reviewed submission, Task 9: End-to-end handoff, live vision evidence and runbook, copy(), UploadResult, malformed, populated, fakeApi() (+13 more)

### Community 108 - "test_final_fix_handoff.py"
Cohesion: 0.08
Nodes (26): Passage, SearchResult, process_batch(), Checker, Knowledge, ScriptedChat, assert_completed_evidence(), faulty_knowledge() (+18 more)

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

### Community 114 - "Maintainability and stale-code refactor — design specification"
Cohesion: 0.11
Nodes (17): Task 6: Repair ExtractedField fixtures and make standalone typecheck real, 10. Verification and acceptance, 1. Outcome and success criteria, 2. Audit baseline, 3. Selected approach and sequence, 4. Boundaries and non-goals, 8.1 Approved deletions, 8.2 Docker and documentation (+9 more)

### Community 115 - "dependencies"
Cohesion: 0.33
Nodes (6): dependencies, clsx, react, react-dom, tailwind-merge, @workspace/ui

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
Nodes (15): Customer Frontend Maintainability Implementation Plan, Global Constraints, Review Focus, Task 2: Make standalone typechecking and root test execution real, Task 3: Centralize test cleanup and shared intake fixtures mechanically, Task 6: Extract stable-ID sequential upload lifecycle with TDD, Task 9: Run the complete customer acceptance matrix and final diff review, 7.1 Verification and cleanup (+7 more)

### Community 120 - "scripts"
Cohesion: 0.50
Nodes (4): scripts, format, lint, typecheck

### Community 122 - "intake/contracts.py"
Cohesion: 0.22
Nodes (18): IntakeState, Question, Readiness, _asked_already(), asks_for_secret(), assess_readiness(), _can_ask(), canonical_category() (+10 more)

### Community 123 - "TurnContext"
Cohesion: 0.14
Nodes (9): QuestionRecord, TurnContext, IntakeGraph, _invitation(), builder(), grounded_analysis(), grounded_review(), ScriptedIntakeModel (+1 more)

### Community 124 - "ingest.py"
Cohesion: 0.26
Nodes (8): load_jsonl(), load_tickets(), _rows(), test_csv_with_bom_and_missing_columns(), test_duplicate_external_ids_keep_first(), test_json_object_without_ids(), test_jsonl_fixture_loads(), test_unsupported_format()

### Community 126 - "guardrails.py"
Cohesion: 0.20
Nodes (12): normalize_phone(), parse_amount(), _iso(), normalize_value(), check_draft(), _citation_findings(), _exact_amount(), _grounding_findings() (+4 more)

### Community 127 - "test_cli.py"
Cohesion: 0.18
Nodes (9): test_config_error_exits_2(), boom(), test_ingest_directory_is_deterministic_and_duplicate_is_free(), test_ingest_disabled_configuration_never_calls_provider(), test_ingest_failure_exit_and_retry_stored(), test_ingest_invalid_source_does_not_stop_other_files(), test_ingest_limits_batch_without_partial_side_effects(), test_retry_stored_indexes_old_uploads_without_recovering_other_process_jobs() (+1 more)

### Community 128 - "session.ts"
Cohesion: 0.17
Nodes (8): Task 7: Preserve resume-unavailable state across `startNew`, emptyState(), browserSessionStorage(), SessionStorage, credentials, invalidValues, messagePayload, SavedSession

### Community 129 - "intake/model.py"
Cohesion: 0.10
Nodes (29): Attachment, ImageInput, ModelCall, ModelUnavailable, _analysis_prompt(), _bounded_context(), _guard_size(), ModelBudget (+21 more)

### Community 130 - "test_llm.py"
Cohesion: 0.13
Nodes (11): GeminiStructuredLLM, make_gemini_llm(), _llm(), _S, test_draft_model_uses_millisecond_timeout_and_disables_sdk_retries(), test_openrouter_reported_cost_takes_precedence_over_token_estimate(), test_openrouter_retry_budget_is_bounded(), test_openrouter_structured_samples_use_configured_key_and_validate_output() (+3 more)

### Community 131 - "intake.py"
Cohesion: 0.16
Nodes (19): create_session(), _credentials(), _dump(), get_session(), post_message(), read_attachment(), remove_attachment(), request_review() (+11 more)

### Community 132 - "Review Focus"
Cohesion: 0.15
Nodes (12): api(), settings(), Global Constraints, Repository Hygiene Maintainability Implementation Plan, Review Focus, Task 1: Establish the safety baseline and remove tracked Graphify cache contents, Task 2: Delete the superseded architecture HTML after a fresh reference check, Task 3: Remove confirmed stale local runtime state and the duplicate screenshot (+4 more)

### Community 133 - "_DatabaseCall"
Cohesion: 0.10
Nodes (6): _DatabaseCall, _Claim, DocumentNotFoundError, IndexAttemptLostError, KnowledgeError, Task 14: Preserve Safe Knowledge 503s and Log Only Unexpected Diagnostic Types

### Community 134 - "ReviewEditor"
Cohesion: 0.20
Nodes (9): Employee Frontend Maintainability Implementation Plan, Global Constraints, Review Focus, Task 1: Remove reference-verified dead exports, components, and the Mermaid dependency, Task 7: Repair employee README paths/test-count guidance and run final acceptance, SelectSeparator(), ReviewEditor(), reviewerNote() (+1 more)

### Community 135 - "Customer Conversation Intake Implementation Plan"
Cohesion: 0.20
Nodes (8): Completion audit — 2026-10-18, Customer Conversation Intake Implementation Plan, Execution conventions and repository baseline, File map and dependency order, Global Constraints, Plan review and execution handoff, Review Focus, Spec coverage and acceptance map

### Community 136 - "find_candidates"
Cohesion: 0.25
Nodes (12): Candidate, _add(), find_candidates(), _overlaps(), test_amount_forms(), test_arabic_indic_amount_not_confused_with_phone(), test_dates_absolute_and_weekday(), test_dedupes_repeated_values() (+4 more)

### Community 137 - "SubmissionService"
Cohesion: 0.38
Nodes (4): Receipt, SubmissionResult, SubmissionService, Ticket

### Community 139 - "fakes.py"
Cohesion: 0.10
Nodes (26): LLMUnavailable, Sample, StructuredLLM, FieldPick, FieldExtractor, _field(), fill_gaps(), finalize() (+18 more)

### Community 140 - "agent.py"
Cohesion: 0.07
Nodes (4): TicketExecution, _Execution, DraftChatOpenRouter, DraftProviderResponseError

### Community 141 - "database.py"
Cohesion: 0.38
Nodes (4): _abandoned(), _check_deadline(), _consume(), Task 4: Extract KB Database Call Mechanics Without Changing Transactions

### Community 142 - "test_dbapi_commit_handoff_arbitrates_cancellation"
Cohesion: 0.22
Nodes (4): test_db_deadline_includes_pool_and_checkout_without_late_claim(), checked_in(), test_db_deadline_search_cancellation_is_nonblocking_and_retains_cost(), test_index_deadline_or_cancellation_preserves_real_adapter_partial_cost()

### Community 143 - "resolve_date"
Cohesion: 0.36
Nodes (4): resolve_date(), _safe_date(), test_resolve(), test_unresolvable_is_none()

### Community 144 - "5. Backend design"
Cohesion: 0.29
Nodes (5): 5.1 Dead-code cleanup, 5.2 Extraction ownership, 5.3 Knowledge-service boundary, 5.5 Confirmed backend defect fixes, 5. Backend design

### Community 148 - "components-ai-thought-chain.tsx"
Cohesion: 0.14
Nodes (16): Status, StatusIcon(), statusStyles, StepContext, StepContextType, ThoughtChain(), ThoughtChainContent(), ThoughtChainItem() (+8 more)

### Community 149 - "kb/service.py"
Cohesion: 0.07
Nodes (43): _safe_dispatch(), get_run(), list_runs(), start_run(), Base, IncidentRow, RunRow, TicketResultRow (+35 more)

### Community 152 - "main.py"
Cohesion: 0.05
Nodes (37): init_db(), initialize_database(), make_engine(), make_sessionmaker(), reset_db(), upgrade_workspace_schema(), create_app(), lifespan() (+29 more)

### Community 153 - "test_serialize.py"
Cohesion: 0.40
Nodes (7): TicketOutcome, outcome_from_state(), outcome_to_dict(), outcome_to_row(), process(), test_failed_outcome_and_dict_form(), test_full_outcome_is_json_safe()

### Community 154 - "ZainCash support: architecture and ticket flow {#support-overview}"
Cohesion: 0.50
Nodes (3): 1 · System architecture {#system-architecture}, 2 · Ticket flow {#ticket-flow}, ZainCash support: architecture and ticket flow {#support-overview}

### Community 155 - "Synthetic demo readiness"
Cohesion: 0.50
Nodes (4): Evidence by layer, Known limitations and remaining work, Repeatable local walkthrough, Synthetic demo readiness

### Community 156 - "employee-frontend/src/components/theme-provider.tsx"
Cohesion: 0.23
Nodes (11): disableTransitionsTemporarily(), getSystemTheme(), isEditableTarget(), isTheme(), ResolvedTheme, Theme, THEME_VALUES, ThemeProvider() (+3 more)

### Community 158 - "lookup.py"
Cohesion: 0.15
Nodes (16): TxnRecord, _as_date(), InMemoryTransactionRepo, _iqd_amount(), match_transaction(), TransactionRepo, _ex(), _match() (+8 more)

### Community 164 - "factory.py"
Cohesion: 0.27
Nodes (8): make_draft_model(), response_payload(), run_provider_pipeline(), send(), search_response(), test_empty_choices_escalates_and_keeps_paid_response_usage(), test_failed_response_id_is_deduplicated_against_earlier_success(), test_other_conversion_value_errors_remain_unexpected()

### Community 167 - "build_pipeline"
Cohesion: 0.11
Nodes (27): SqlTransactionRepo, build_pipeline(), ConfigError, make_jev_client(), run_batch(), FakeJevRunnable, FakeStructuredLLM, _settings() (+19 more)

### Community 170 - "test_dbapi_commit_handoff_arbitrates_cancellation"
Cohesion: 0.47
Nodes (4): test_dbapi_commit_handoff_arbitrates_cancellation(), gate(), gate_before_dbapi(), gate_inside_dbapi()

### Community 172 - "6. Employee frontend design"
Cohesion: 0.50
Nodes (4): 6.1 Verification and cleanup, 6.2 Retire the legacy trace/chart cluster, 6.3 Runs and request loading, 6. Employee frontend design

## Ambiguous Edges - Review These
- `Fraud Report` → `Plan 1 Live Smoke`  [AMBIGUOUS]
  README.md · relation: conceptually_related_to

## Knowledge Gaps
- **83 isolated node(s):** `zaincash-support`, `@base-ui/react`, `@fontsource-variable/plus-jakarta-sans`, `@fontsource/tajawal`, `@tailwindcss/vite` (+78 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 1054 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **51 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `ReviewEditor()` connect `ReviewEditor` to `NewBatchPage.tsx`, `Review Focus`, `useCopy`, `build_tools`, `TicketReviewPage.tsx`, `IntakePage.test.tsx`, `format.ts`, `QueuePage.tsx`, `Maintainability and stale-code refactor — design specification`, `components-ai-thought-chain.tsx`, `Review Focus`, `workspace-ui.tsx`?**
  _High betweenness centrality (0.087) - this node is a cross-community bridge._
- **Are the 36 inferred relationships involving `Settings` (e.g. with `_command_settings()` and `_run_in_memory()`) actually correct?**
  _`Settings` has 36 INFERRED edges - model-reasoned connections that need verification._
- **What connects `zaincash-support`, `@base-ui/react`, `@fontsource-variable/plus-jakarta-sans` to the rest of the system?**
  _83 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `NewBatchPage.tsx` be split into smaller, more focused modules?**
  _Cohesion score 0.14193548387096774 - nodes in this community are weakly interconnected._
- **Why does `build_tools()` connect `build_tools` to `test_kb_service.py`, `investigation.py`, `agent.py`, `Review Focus`, `test_rag_api.py`, `agent.py`, `DraftSubmission`, `Maintainability and stale-code refactor — design specification`, `Review Focus`, `test_draft_tools.py`, `tools.py`?**
  _High betweenness centrality (0.086) - this node is a cross-community bridge._
- **Are the 25 inferred relationships involving `KnowledgeService` (e.g. with `Settings` and `UploadedDocument`) actually correct?**
  _`KnowledgeService` has 25 INFERRED edges - model-reasoned connections that need verification._

### Low-confidence Hints
_AMBIGUOUS edges — the extractor was unsure. Verify before acting on these._

- **What is the exact relationship between `Fraud Report` and `Plan 1 Live Smoke`?**
  _Edge tagged AMBIGUOUS (relation: conceptually_related_to) - confidence is low._