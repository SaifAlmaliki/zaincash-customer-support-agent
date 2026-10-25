# Graph Report - zaincash-support  (2026-10-25)

## Corpus Check
- 291 files · ~237,517 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 30 file(s) not represented in the graph (top: (none) 18, .jsonl 4, .css 4)

## Summary
- 2936 nodes · 9021 edges · 154 communities (108 shown, 46 thin omitted)
- Extraction: 89% EXTRACTED · 11% INFERRED · 0% AMBIGUOUS · INFERRED: 1007 edges (avg confidence: 0.92)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `cca5206d`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- fakes.py
- intake/types.ts
- test_rag_drafter.py
- TurnStore
- TicketReviewPage.tsx
- InvalidEvidence
- QueuePage.tsx
- Customer conversation intake for ZainCash support
- workspace-ui.tsx
- IntakeController
- test_gemini.py
- test_rag_api.py
- employee-frontend/package.json
- test_draft_guardrails.py
- Support Taxonomy Categories
- ui/package.json
- employee-frontend/src/App.tsx
- users-frontend/package.json
- TicketRow
- UploadedDocument
- web/package.json
- test_cli.py
- compilerOptions
- employee-frontend/components.json
- test_db_deadline_cancelled_publication_cannot_commit_late
- compilerOptions
- web/src/components/theme-provider.tsx
- test_embeddings.py
- Classify and Extract Prompts
- FakeJevRunnable
- Pipeline Design Spec
- Batch Runner
- Drafting Plan Concepts
- test_kb_service.py
- search_knowledge_base
- web/components.json
- Pipeline Spec Rules
- db/repository.py
- ui/components.json
- TicketResultRow
- fact
- Vite Config
- Human Review Gate
- compilerOptions
- pipeline/graph.py
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
- tools.py
- intake/contracts.py
- normalize.py
- NewBatchPage.tsx
- lookup.py
- kb/service.py
- tasks
- PipelineTrace.tsx
- IntakePage.tsx
- test_handoff.py
- make_output
- _DatabaseCall
- PipelineState
- stage6_draft/model.py
- factory.py
- guardrails.py
- use-knowledge-library.ts
- test-kb/README.md
- Plan 3 — Knowledge retrieval and grounded reply drafting
- KnowledgePage
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
- agent.py
- devDependencies
- devDependencies
- submission.py
- RagDrafter
- TicketReviewPage.tsx
- compilerOptions
- قواعد المعرفة العربية للعرض أمام لجنة التحكيم
- pydantic
- dependencies
- find_candidates
- dependencies
- compilerOptions
- resolve_date
- controller.test.ts
- KnowledgeExecutionError
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
- FakeXHR
- scripts
- users-frontend/README.md
- context
- _abandoned
- intake/repository.py
- 7. Review and submission
- InvalidEvidence
- build_pipeline
- ar/app_bug.md
- intake/model.py
- Customer Conversation Intake Implementation Plan
- intake.py
- test_final_fix_handoff.py
- Synthetic demo readiness
- kb_fakes.py
- ar/bill_payment.md
- cli.py
- ar/card_issue.md
- intake/api.ts
- ingest.py
- test_dbapi_commit_handoff_arbitrates_cancellation
- ar/fraud_report.md
- ar/general_inquiry.md
- @testing-library/react
- start_run
- health
- ar/login_access.md
- intake/README.md
- TicketInput
- ar/refund_request.md
- ar/failed_transfer.md

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

## Communities (154 total, 46 thin omitted)

### Community 0 - "fakes.py"
Cohesion: 0.13
Nodes (25): LLMUnavailable, FieldPick, FieldExtractor, combine(), merge_picks(), _field(), fill_gaps(), finalize() (+17 more)

### Community 1 - "intake/types.ts"
Cohesion: 0.11
Nodes (20): HTTP contract (implemented in Tasks 4–5), Task 7: Bilingual customer chat, screenshots and reviewed submission, Task 9: End-to-end handoff, live vision evidence and runbook, copy(), IntakeApi, IntakeCopy, OwnedImage(), Attachment (+12 more)

### Community 2 - "test_rag_drafter.py"
Cohesion: 0.21
Nodes (35): answer(), call(), Checker, draft_state(), script(), submit(), pipeline(), submit() (+27 more)

### Community 3 - "TurnStore"
Cohesion: 0.11
Nodes (23): OperationClaim, TurnResult, IntakeOperationRow, RevisionConflict, session_view(), sanitize_intake_text(), _jsonable(), TurnStore (+15 more)

### Community 4 - "TicketReviewPage.tsx"
Cohesion: 0.28
Nodes (16): Confidence(), Metric(), Badge(), Card(), CardContent(), CardHeader(), CardTitle(), EvaluationPage() (+8 more)

### Community 5 - "InvalidEvidence"
Cohesion: 0.18
Nodes (14): canonical_digits(), normalize_reported_date(), _apply(), _check_reference(), _compact(), checked_update(), _newer_correction(), _normalize_precise() (+6 more)

### Community 6 - "QueuePage.tsx"
Cohesion: 0.25
Nodes (25): EmptyState(), ErrorState(), LoadingState(), PageHeader(), PriorityBadge(), StatusBadge(), Table(), TableBody() (+17 more)

### Community 7 - "Customer conversation intake for ZainCash support"
Cohesion: 0.07
Nodes (28): 10. Verification and acceptance criteria, 11. Delivery and review, 1. Outcome and agreed requirements, 2. Current implementation and integration points, 3. Approach and boundaries, 4. Conversation state and turn flow, 5. Facts, evidence, and readiness, 6. Language and screenshot behavior (+20 more)

### Community 8 - "workspace-ui.tsx"
Cohesion: 0.15
Nodes (19): ConfirmDialog(), FilterSelect(), statusLabels, Button(), buttonVariants, Dialog(), DialogContent(), DialogDescription() (+11 more)

### Community 9 - "IntakeController"
Cohesion: 0.18
Nodes (6): Task 6: Customer API client and resumable UI state, IntakeController, isConflict(), isOffline(), safeMessage(), Language

### Community 10 - "test_gemini.py"
Cohesion: 0.18
Nodes (14): Sample, ExtractedSpan, _Fields, GeminiFields, FakeStructuredLLM, _a(), _classify(), test_all_samples_failing_raises() (+6 more)

### Community 11 - "test_rag_api.py"
Cohesion: 0.11
Nodes (21): _payload(), test_concurrent_submit_dispatches_once(), test_second_request_id_reuses_the_approved_review(), test_submission_replay_creates_one_ticket(), client(), evidence_client(), test_actual_guardrail_failure_is_separate_from_reply(), test_concurrent_index_requests_share_active_work() (+13 more)

### Community 12 - "employee-frontend/package.json"
Cohesion: 0.07
Nodes (29): @base-ui/react, class-variance-authority, cn, eslint, @eslint/js, eslint-plugin-react-hooks, eslint-plugin-react-refresh, globals (+21 more)

### Community 14 - "test_draft_guardrails.py"
Cohesion: 0.13
Nodes (28): requests_credentials(), check(), state(), test_aggregation_is_deduplicated_and_has_no_state_side_effects(), test_amount_occurrences_keep_their_own_currency_and_sign(), test_avoid_sharing_warning_does_not_excuse_a_later_request(), test_candidate_prompt_limit_does_not_hide_later_ungrounded_references(), test_candidate_transactions_cannot_authorize_reply_evidence() (+20 more)

### Community 15 - "Support Taxonomy Categories"
Cohesion: 0.21
Nodes (22): lookup, Account KYC, Account & Security, Agent Dispute, Agent Network, App Bug, Bill Payment, Card Issue (+14 more)

### Community 16 - "ui/package.json"
Cohesion: 0.07
Nodes (29): @fontsource/tajawal, @fontsource-variable/plus-jakarta-sans, @turbo/gen, zod, @base-ui/react, class-variance-authority, cn, eslint (+21 more)

### Community 17 - "employee-frontend/src/App.tsx"
Cohesion: 0.15
Nodes (21): App(), EvaluationPage, InsightsPage, KnowledgePage, NewBatchPage, QueuePage, RunDetailPage, RunsPage (+13 more)

### Community 18 - "users-frontend/package.json"
Cohesion: 0.09
Nodes (22): turbo, devDependencies, prettier, prettier-plugin-tailwindcss, turbo, typescript, engines, node (+14 more)

### Community 19 - "TicketRow"
Cohesion: 0.14
Nodes (17): get_session(), get_result(), list_results(), read_intake_attachment(), review_result(), ReviewInput, ReviewRow, TicketResultRow (+9 more)

### Community 20 - "UploadedDocument"
Cohesion: 0.12
Nodes (21): delete_document(), download_document(), index_document(), list_chunks(), list_documents(), _require_provider(), search_knowledge(), upload_document() (+13 more)

### Community 21 - "web/package.json"
Cohesion: 0.08
Nodes (25): jsdom, @testing-library/user-event, @workspace/ui, eslint, @eslint/js, eslint-plugin-react-hooks, eslint-plugin-react-refresh, globals (+17 more)

### Community 22 - "test_cli.py"
Cohesion: 0.27
Nodes (6): test_ingest_directory_is_deterministic_and_duplicate_is_free(), test_ingest_disabled_configuration_never_calls_provider(), test_ingest_failure_exit_and_retry_stored(), test_ingest_invalid_source_does_not_stop_other_files(), test_ingest_limits_batch_without_partial_side_effects(), test_retry_stored_indexes_old_uploads_without_recovering_other_process_jobs()

### Community 23 - "compilerOptions"
Cohesion: 0.08
Nodes (23): compilerOptions, allowArbitraryExtensions, allowImportingTsExtensions, erasableSyntaxOnly, jsx, lib, module, moduleDetection (+15 more)

### Community 24 - "employee-frontend/components.json"
Cohesion: 0.09
Nodes (21): aliases, components, hooks, lib, ui, utils, iconLibrary, menuAccent (+13 more)

### Community 25 - "test_db_deadline_cancelled_publication_cannot_commit_late"
Cohesion: 0.29
Nodes (3): test_db_deadline_cancelled_publication_cannot_commit_late(), test_db_deadline_is_cumulative_across_publication_statements(), changed_index()

### Community 26 - "compilerOptions"
Cohesion: 0.09
Nodes (21): compilerOptions, allowArbitraryExtensions, allowImportingTsExtensions, erasableSyntaxOnly, jsx, lib, module, moduleDetection (+13 more)

### Community 27 - "web/src/components/theme-provider.tsx"
Cohesion: 0.09
Nodes (22): disableTransitionsTemporarily(), getSystemTheme(), isEditableTarget(), isTheme(), ResolvedTheme, Theme, THEME_VALUES, ThemeProvider() (+14 more)

### Community 28 - "test_embeddings.py"
Cohesion: 0.08
Nodes (42): Embedder, EmbeddingBatch, EmbeddingError, _nonnegative_number(), OpenRouterEmbedder, _ordered_vectors(), _response_cost(), Embeddings (+34 more)

### Community 29 - "Classify and Extract Prompts"
Cohesion: 0.31
Nodes (9): extract, gemini_classify, Pipeline Graph Orchestration, jev_classify, prepare, Gemini Classify Prompt v1, Gemini Extract Prompt v1, GeminiClassifier (+1 more)

### Community 30 - "FakeJevRunnable"
Cohesion: 0.05
Nodes (59): IncidentRow, CredentialCheck, DegradedCredentialChecker, _finite_nonnegative(), _get(), JevCredentialChecker, FakeJevRunnable, ResponseRunnable (+51 more)

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
Cohesion: 0.12
Nodes (32): KnowledgeService, FakeEmbedder, GatedEmbedder, PaidEmbedder, count_chunks(), test_category_filters_include_general_policies_and_validate_tags(), test_claim_locks_source_even_before_index_row_exists(), test_competing_callers_refuse_active_attempt_and_release_transactions() (+24 more)

### Community 36 - "web/components.json"
Cohesion: 0.10
Nodes (19): aliases, components, hooks, lib, ui, utils, iconLibrary, menuAccent (+11 more)

### Community 38 - "db/repository.py"
Cohesion: 0.14
Nodes (24): _run_with_db(), RunRow, create_run(), finish_run(), load_incidents(), load_transactions(), save_outcomes(), _to_record() (+16 more)

### Community 39 - "ui/components.json"
Cohesion: 0.10
Nodes (19): aliases, components, hooks, lib, ui, utils, iconLibrary, menuAccent (+11 more)

### Community 40 - "TicketResultRow"
Cohesion: 0.23
Nodes (11): _safe_dispatch(), recover(), fail_intake_placeholders(), reconcile_intake_run(), recover_intake_processing(), dispatch_intake(), test_review_to_employee_handoff(), _submit() (+3 more)

### Community 41 - "fact"
Cohesion: 0.17
Nodes (41): Analysis, EvidenceRef, Fact, Readiness, merge_analysis(), remove_attachment_evidence(), context(), fact() (+33 more)

### Community 43 - "Human Review Gate"
Cohesion: 0.25
Nodes (4): support CLI, Support Workspace UI Plan, Review API, Workspace UI Verification

### Community 44 - "compilerOptions"
Cohesion: 0.12
Nodes (16): compilerOptions, allowImportingTsExtensions, erasableSyntaxOnly, lib, module, moduleDetection, noEmit, noFallthroughCasesInSwitch (+8 more)

### Community 46 - "pipeline/graph.py"
Cohesion: 0.13
Nodes (9): TicketOutcome, _default_retry(), outcome_from_state(), _percentile(), _retryable(), outcome_to_dict(), outcome_to_row(), test_failed_outcome_and_dict_form() (+1 more)

### Community 47 - "compilerOptions"
Cohesion: 0.12
Nodes (16): compilerOptions, allowImportingTsExtensions, erasableSyntaxOnly, lib, module, moduleDetection, noEmit, noFallthroughCasesInSwitch (+8 more)

### Community 48 - "support_test"
Cohesion: 0.07
Nodes (30): ingest(), index_deadlines(), settings(), support_test(), expire_during_embedding(), Completion and review record — 2026-10-17, Execution handoff, File map and shared interfaces (+22 more)

### Community 57 - "parse_document"
Cohesion: 0.10
Nodes (29): TextChunk, _append_chunks(), _check_extracted_size(), DocumentParseError, parse_document(), _parse_pdf(), make_pdf(), test_arabic_text_and_bom_are_preserved() (+21 more)

### Community 58 - "tools.py"
Cohesion: 0.05
Nodes (36): TxnRecord, parse_dt(), txn_from_dict(), DraftAlreadySubmitted, DraftSubmission, DraftToolInputError, _datetime(), _days() (+28 more)

### Community 59 - "intake/contracts.py"
Cohesion: 0.17
Nodes (14): Attachment, _aware(), CustomerReview, Message, IntakeAttachmentRow, IntakeMessageRow, _attachment(), customer_review() (+6 more)

### Community 60 - "normalize.py"
Cohesion: 0.21
Nodes (17): detect_arabizi(), fold_arabic(), has_latin_mix(), _latin_words(), mask_cards(), normalize(), sanitize_for_storage(), to_ascii_digits() (+9 more)

### Community 61 - "NewBatchPage.tsx"
Cohesion: 0.11
Nodes (17): badgeVariants, Input(), Tabs(), TabsContent(), TabsList(), tabsListVariants, TabsTrigger(), Textarea() (+9 more)

### Community 62 - "lookup.py"
Cohesion: 0.10
Nodes (32): Decision, ExtractedField, LookupResult, _as_date(), _iqd_amount(), match_transaction(), TransactionRepo, decide() (+24 more)

### Community 63 - "kb/service.py"
Cohesion: 0.21
Nodes (4): Base, KnowledgeChunk, KnowledgeDocumentIndex, retry_ids()

### Community 64 - "tasks"
Cohesion: 0.12
Nodes (16): dependsOn, inputs, outputs, cache, persistent, dependsOn, dependsOn, $schema (+8 more)

### Community 65 - "PipelineTrace.tsx"
Cohesion: 0.09
Nodes (33): 1. Outcome, 2. Scope, 5. Language, 6. How a result becomes the charts, 7. Sentences, 8. Tests, 9. Files, Ticket flow charts (+25 more)

### Community 66 - "IntakePage.tsx"
Cohesion: 0.12
Nodes (23): Global Constraints, Intake Chat UI Implementation Plan, Task 1: Put the summary and receipt in the thread, Task 2: Put screenshots inside the composer, Task 3: Apply the workspace chat styles, Task 4: Check the page in the browser, 1. Outcome, 2. Scope (+15 more)

### Community 67 - "test_handoff.py"
Cohesion: 0.20
Nodes (15): _amount(), analyze(), complete_conversation(), _dated(), _message(), _opening(), _png(), _review() (+7 more)

### Community 68 - "make_output"
Cohesion: 0.14
Nodes (33): make_draft_model(), build_graph(), PipelineDeps, InMemoryTransactionRepo, FakeClassifier, make_output(), make_ticket(), pipeline() (+25 more)

### Community 69 - "_DatabaseCall"
Cohesion: 0.08
Nodes (7): _check_deadline(), _Claim, _consume(), _DatabaseCall, DocumentNotFoundError, IndexAttemptLostError, KnowledgeError

### Community 70 - "PipelineState"
Cohesion: 0.13
Nodes (12): DraftResult, _Nodes, Drafter, NullDrafter, UnavailableDrafter, PipelineState, draft(), draft() (+4 more)

### Community 72 - "factory.py"
Cohesion: 0.14
Nodes (9): load_taxonomy(), most_urgent(), priority_rank(), TaxonomyError, tax(), taxonomy(), taxonomy(), test_priority_helpers() (+1 more)

### Community 73 - "guardrails.py"
Cohesion: 0.20
Nodes (12): normalize_phone(), parse_amount(), _iso(), normalize_value(), check_draft(), _citation_findings(), _exact_amount(), _grounding_findings() (+4 more)

### Community 74 - "use-knowledge-library.ts"
Cohesion: 0.12
Nodes (27): acceptIndexRequest(), canRequestIndex(), PendingIndexes, persistPendingIndexes(), pollKnowledge(), refresh(), stop(), PollOptions (+19 more)

### Community 75 - "test-kb/README.md"
Cohesion: 0.15
Nodes (6): Fictional RAG walkthrough inputs, توثيق الحساب — سياسة خيالية للعرض التجريبي, نزاع مع وكيل — سياسة خيالية للعرض التجريبي, الطلبات غير الواضحة وخارج النطاق — سياسة خيالية للعرض التجريبي, الاستفسار المؤقت للدعم في المهمة ٨ — سياسة خيالية للعرض التجريبي, التحويل لمستلم بالخطأ — سياسة خيالية للعرض التجريبي

### Community 76 - "Plan 3 — Knowledge retrieval and grounded reply drafting"
Cohesion: 0.11
Nodes (18): 10. Remaining demo roadmap, 1. Intent and acceptance criteria, 3. Provider and configuration, 4. Knowledge ingestion and persistence, 5. Retrieval and evidence, 6. Bounded investigation agent, 7. Draft guardrails and failure outcomes, 8. Pipeline, API, CLI and UI integration (+10 more)

### Community 77 - "KnowledgePage"
Cohesion: 0.46
Nodes (8): BadgeLabel(), KnowledgePage(), beginMutation(), deleteDocument(), finishMutation(), indexDocument(), upload(), sizeLabel()

### Community 79 - "devDependencies"
Cohesion: 0.12
Nodes (16): devDependencies, eslint, @eslint/js, eslint-plugin-react-hooks, eslint-plugin-react-refresh, globals, prettier, prettier-plugin-tailwindcss (+8 more)

### Community 80 - "judge-demo.ar.md"
Cohesion: 0.14
Nodes (13): أعطال التطبيق — سياسة خيالية للعرض التجريبي, استرجاع مبلغ شراء — سياسة خيالية للعرض التجريبي, استعادة الدخول — سياسة خيالية للعرض التجريبي, الاستفسار الآمن من الدعم — سياسة خيالية للعرض التجريبي, الاستفسار المؤقت للدعم في المهمة ٨ — سياسة خيالية للعرض التجريبي, التحويل المعلّق — سياسة خيالية للعرض التجريبي, التحويل لمستلم بالخطأ — سياسة خيالية للعرض التجريبي, الطلبات غير الواضحة وخارج النطاق — سياسة خيالية للعرض التجريبي (+5 more)

### Community 93 - "agent.py"
Cohesion: 0.07
Nodes (23): StructuredLLM, Candidates, ClassificationResult, ClassifierOutput, NormalizedTicket, Classifier, GeminiClassifier, GeminiExtractor (+15 more)

### Community 94 - "devDependencies"
Cohesion: 0.11
Nodes (19): devDependencies, eslint, @eslint/js, eslint-plugin-react-hooks, eslint-plugin-react-refresh, globals, jsdom, @tailwindcss/vite (+11 more)

### Community 95 - "devDependencies"
Cohesion: 0.14
Nodes (14): devDependencies, eslint, @eslint/js, eslint-plugin-react-hooks, eslint-plugin-react-refresh, globals, tailwindcss, @tailwindcss/vite (+6 more)

### Community 96 - "submission.py"
Cohesion: 0.32
Nodes (9): Receipt, IntakeSubmissionRow, processing_status(), receipt_for(), current_session_view(), SubmissionResult, SubmissionService, Ticket (+1 more)

### Community 97 - "RagDrafter"
Cohesion: 0.09
Nodes (9): _Execution, _ModelUsage, RagDrafter, DraftContext, DraftExecutionError, ScriptedChat, test_real_search_fault_carries_safe_draft_execution_error(), test_concurrent_tickets_cannot_exchange_citations_cost_or_callback_state() (+1 more)

### Community 98 - "TicketReviewPage.tsx"
Cohesion: 0.18
Nodes (12): Task 8: Employee evidence panel and processing state, intakeFixture, factValue(), IntakeEvidence(), Screenshot(), canReview(), REVIEWABLE, ReviewEditor() (+4 more)

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
Cohesion: 0.15
Nodes (13): dependencies, @base-ui/react, class-variance-authority, cn, @fontsource-variable/geist, lucide-react, react, react-dom (+5 more)

### Community 103 - "find_candidates"
Cohesion: 0.25
Nodes (12): Candidate, _add(), find_candidates(), _overlaps(), test_amount_forms(), test_arabic_indic_amount_not_confused_with_phone(), test_dates_absolute_and_weekday(), test_dedupes_repeated_values() (+4 more)

### Community 104 - "dependencies"
Cohesion: 0.15
Nodes (13): dependencies, @base-ui/react, class-variance-authority, cn, @fontsource/tajawal, @fontsource-variable/plus-jakarta-sans, @hugeicons/core-free-icons, @hugeicons/react (+5 more)

### Community 105 - "compilerOptions"
Cohesion: 0.17
Nodes (11): compilerOptions, jsx, lib, module, moduleResolution, outDir, skipLibCheck, strict (+3 more)

### Community 106 - "resolve_date"
Cohesion: 0.36
Nodes (4): resolve_date(), _safe_date(), test_resolve(), test_unresolvable_is_none()

### Community 107 - "controller.test.ts"
Cohesion: 0.13
Nodes (16): App(), controller, emptySession(), fakeApi(), review, attachment, collectingController(), emptySession() (+8 more)

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
Cohesion: 0.05
Nodes (23): Settings, GeminiStructuredLLM, make_gemini_llm(), test_blank_intake_model_is_rejected(), test_non_positive_image_limit_is_rejected(), test_relative_upload_directory_is_rooted_in_the_repository(), test_settings_validation_is_safe_field_diagnostic_exit_2(), test_defaults() (+15 more)

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

### Community 120 - "scripts"
Cohesion: 0.50
Nodes (4): scripts, format, lint, typecheck

### Community 122 - "context"
Cohesion: 0.17
Nodes (18): IntakeState, Question, _asked_already(), asks_for_secret(), assess_readiness(), _can_ask(), canonical_category(), choose_question() (+10 more)

### Community 124 - "intake/repository.py"
Cohesion: 0.07
Nodes (40): AttachmentStore, _display_name(), Credentials, IntakeModel, SessionView, IntakeSessionRow, ImageRejected, IntakeError (+32 more)

### Community 125 - "7. Review and submission"
Cohesion: 0.67
Nodes (3): 7. Review and submission, Review, Submission transaction

### Community 126 - "InvalidEvidence"
Cohesion: 0.12
Nodes (20): QuestionRecord, ReviewSnapshot, ReviewText, TurnContext, InvalidEvidence, IntakeGraph, _invitation(), validate() (+12 more)

### Community 127 - "build_pipeline"
Cohesion: 0.15
Nodes (19): SqlTransactionRepo, build_pipeline(), ConfigError, make_jev_client(), run_batch(), GeminiAnalysis, test_config_error_exits_2(), boom() (+11 more)

### Community 129 - "intake/model.py"
Cohesion: 0.11
Nodes (26): ImageInput, ModelCall, ModelUnavailable, _analysis_prompt(), _bounded_context(), _guard_size(), ModelBudget, OpenRouterIntakeModel (+18 more)

### Community 130 - "Customer Conversation Intake Implementation Plan"
Cohesion: 0.20
Nodes (8): Completion audit — 2026-10-18, Customer Conversation Intake Implementation Plan, Execution conventions and repository baseline, File map and dependency order, Global Constraints, Plan review and execution handoff, Review Focus, Spec coverage and acceptance map

### Community 131 - "intake.py"
Cohesion: 0.16
Nodes (19): create_session(), _credentials(), _dump(), get_session(), post_message(), read_attachment(), remove_attachment(), request_review() (+11 more)

### Community 132 - "test_final_fix_handoff.py"
Cohesion: 0.11
Nodes (23): Passage, SearchResult, process_batch(), Knowledge, assert_completed_evidence(), faulty_knowledge(), read(), outer_deadlines() (+15 more)

### Community 133 - "Synthetic demo readiness"
Cohesion: 0.50
Nodes (4): Evidence by layer, Known limitations and remaining work, Repeatable local walkthrough, Synthetic demo readiness

### Community 136 - "cli.py"
Cohesion: 0.05
Nodes (32): _command_settings(), ingest_kb_cmd(), init_db_cmd(), Mode, run_batch_cmd(), _run_in_memory(), seed_db_cmd(), _sessionmaker() (+24 more)

### Community 138 - "intake/api.ts"
Cohesion: 0.14
Nodes (19): createIntakeApi(), IntakeRequestError, isRecord(), parseJson(), parseReceipt(), parseSession(), readError(), stringList() (+11 more)

### Community 139 - "ingest.py"
Cohesion: 0.25
Nodes (8): load_jsonl(), load_tickets(), _rows(), test_csv_with_bom_and_missing_columns(), test_duplicate_external_ids_keep_first(), test_json_object_without_ids(), test_jsonl_fixture_loads(), test_unsupported_format()

### Community 140 - "test_dbapi_commit_handoff_arbitrates_cancellation"
Cohesion: 0.47
Nodes (4): test_dbapi_commit_handoff_arbitrates_cancellation(), gate(), gate_before_dbapi(), gate_inside_dbapi()

### Community 144 - "start_run"
Cohesion: 0.18
Nodes (4): get_run(), list_runs(), start_run(), BatchInput

### Community 148 - "health"
Cohesion: 0.48
Nodes (4): health(), insights(), workspace(), latest_results_query()

### Community 151 - "TicketInput"
Cohesion: 0.31
Nodes (3): KnowledgeIndexInput, KnowledgeSearchInput, TicketInput

## Ambiguous Edges - Review These
- `Fraud Report` → `Plan 1 Live Smoke`  [AMBIGUOUS]
  README.md · relation: conceptually_related_to

## Knowledge Gaps
- **89 isolated node(s):** `zaincash-support`, `@base-ui/react`, `@fontsource-variable/geist`, `@tailwindcss/vite`, `class-variance-authority` (+84 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 974 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **46 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `HTTP contract (implemented in Tasks 4–5)` connect `intake/types.ts` to `intake/model.py`, `Customer Conversation Intake Implementation Plan`, `TurnStore`, `TicketReviewPage.tsx`, `db/repository.py`, `guardrails.py`, `IntakeController`, `intake/repository.py`?**
  _High betweenness centrality (0.148) - this node is a cross-community bridge._
- **Are the 33 inferred relationships involving `Settings` (e.g. with `_command_settings()` and `_run_in_memory()`) actually correct?**
  _`Settings` has 33 INFERRED edges - model-reasoned connections that need verification._
- **What connects `zaincash-support`, `@base-ui/react`, `@fontsource-variable/geist` to the rest of the system?**
  _89 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `fakes.py` be split into smaller, more focused modules?**
  _Cohesion score 0.1282051282051282 - nodes in this community are weakly interconnected._
- **Why does `Settings` connect `Settings` to `intake/model.py`, `test_rag_drafter.py`, `test_final_fix_handoff.py`, `Synthetic demo readiness`, `cli.py`, `test_rag_api.py`, `test_cli.py`, `test_embeddings.py`, `FakeJevRunnable`, `test_kb_service.py`, `db/repository.py`, `fact`, `support_test`, `kb/service.py`, `make_output`, `_DatabaseCall`, `factory.py`, `agent.py`, `submission.py`, `RagDrafter`, `intake/repository.py`, `build_pipeline`?**
  _High betweenness centrality (0.077) - this node is a cross-community bridge._
- **Are the 24 inferred relationships involving `KnowledgeService` (e.g. with `Settings` and `UploadedDocument`) actually correct?**
  _`KnowledgeService` has 24 INFERRED edges - model-reasoned connections that need verification._

### Low-confidence Hints
_AMBIGUOUS edges — the extractor was unsure. Verify before acting on these._

- **What is the exact relationship between `Fraud Report` and `Plan 1 Live Smoke`?**
  _Edge tagged AMBIGUOUS (relation: conceptually_related_to) - confidence is low._