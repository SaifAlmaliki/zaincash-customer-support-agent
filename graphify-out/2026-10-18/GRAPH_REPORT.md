# Graph Report - zaincash-support  (2026-10-18)

## Corpus Check
- 282 files · ~223,641 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 26 file(s) not represented in the graph (top: (none) 15, .jsonl 4, .css 4)

## Summary
- 2844 nodes · 8570 edges · 156 communities (111 shown, 45 thin omitted)
- Extraction: 89% EXTRACTED · 11% INFERRED · 0% AMBIGUOUS · INFERRED: 936 edges (avg confidence: 0.92)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `eaa95e61`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- fakes.py
- intake/types.ts
- test_rag_drafter.py
- TurnStore
- TicketReviewPage.tsx
- db/repository.py
- QueuePage.tsx
- Customer conversation intake for ZainCash support
- workspace-ui.tsx
- IntakeController
- test_lookup.py
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
- KnowledgeService
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
- tests/test_repository.py
- ui/components.json
- TicketResultRow
- Analysis
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
- SqlInvestigationRepo
- NewBatchPage.tsx
- rules.py
- cli.py
- tasks
- types.ts
- IntakePage.tsx
- submission.py
- make_ticket
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
- jev.py
- devDependencies
- devDependencies
- FakeClassifier
- DraftResult
- TicketReviewPage.tsx
- compilerOptions
- قواعد المعرفة العربية للعرض أمام لجنة التحكيم
- pydantic
- dependencies
- employee-frontend/src/components/theme-provider.tsx
- dependencies
- compilerOptions
- IntakeApi
- controller.test.ts
- test_workspace_api.py
- ZainCash Support Workspace
- negative/README.md
- scripts
- scripts
- compilerOptions
- test_llm.py
- dependencies
- web/tsconfig.json
- employee-frontend/tsconfig.json
- exports
- Settings
- scripts
- users-frontend/README.md
- fact
- IntakePage.test.tsx
- intake/repository.py
- TicketOutcome
- InvalidEvidence
- build_pipeline
- answer
- intake/model.py
- Customer Conversation Intake Implementation Plan
- intake.py
- test_final_fix_handoff.py
- Synthetic demo readiness
- EmbeddingBatch
- test_draft_model.py
- main.py
- index_deadlines
- FakeXHR
- test_draft_tools.py
- test_dbapi_commit_handoff_arbitrates_cancellation
- Customer intake verification — 2026-10-18
- @testing-library/react
- state
- agent.py
- intake/README.md
- ar/agent_dispute.md
- task8-history-policy.md
- ar/failed_transfer.md
- ar/general_inquiry.md
- ar/other.md

## God Nodes (most connected - your core abstractions)
1. `Settings` - 94 edges
2. `KnowledgeService` - 79 edges
3. `PipelineState` - 50 edges
4. `make_output()` - 44 edges
5. `make_ticket()` - 44 edges
6. `draft_state()` - 44 edges
7. `IntakeController` - 44 edges
8. `build_pipeline()` - 43 edges
9. `fact()` - 36 edges
10. `AttachmentStore` - 35 edges

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

## Communities (156 total, 45 thin omitted)

### Community 0 - "fakes.py"
Cohesion: 0.13
Nodes (22): LLMUnavailable, Sample, FieldPick, combine(), merge_picks(), finalize(), FakeExtractor, test_both_missing_raises() (+14 more)

### Community 1 - "intake/types.ts"
Cohesion: 0.09
Nodes (26): createIntakeApi(), IntakeRequestError, isRecord(), parseJson(), parseReceipt(), parseSession(), readError(), session (+18 more)

### Community 2 - "test_rag_drafter.py"
Cohesion: 0.24
Nodes (28): Checker, draft_state(), script(), drafter(), events(), test_callback_partial_response_and_error_cost_are_alternatives(), test_checker_timeout_keeps_already_computed_deterministic_findings(), test_concurrent_tickets_cannot_exchange_citations_cost_or_callback_state() (+20 more)

### Community 3 - "TurnStore"
Cohesion: 0.18
Nodes (11): OperationClaim, TurnResult, RevisionConflict, TurnBusy, _jsonable(), TurnStore, repo(), test_recovered_attempt_cannot_publish_stale_output() (+3 more)

### Community 4 - "TicketReviewPage.tsx"
Cohesion: 0.25
Nodes (17): Confidence(), Metric(), Badge(), badgeVariants, Card(), CardContent(), CardHeader(), CardTitle() (+9 more)

### Community 5 - "db/repository.py"
Cohesion: 0.14
Nodes (7): Base, TransactionRow, load_incidents(), load_transactions(), _to_record(), _upsert(), test_sql_transaction_repo()

### Community 6 - "QueuePage.tsx"
Cohesion: 0.25
Nodes (25): EmptyState(), ErrorState(), LoadingState(), PageHeader(), PriorityBadge(), StatusBadge(), Table(), TableBody() (+17 more)

### Community 7 - "Customer conversation intake for ZainCash support"
Cohesion: 0.06
Nodes (31): 10. Verification and acceptance criteria, 11. Delivery and review, 1. Outcome and agreed requirements, 2. Current implementation and integration points, 3. Approach and boundaries, 4. Conversation state and turn flow, 5. Facts, evidence, and readiness, 6. Language and screenshot behavior (+23 more)

### Community 8 - "workspace-ui.tsx"
Cohesion: 0.15
Nodes (19): ConfirmDialog(), FilterSelect(), statusLabels, Button(), buttonVariants, Dialog(), DialogContent(), DialogDescription() (+11 more)

### Community 9 - "IntakeController"
Cohesion: 0.16
Nodes (7): Task 6: Customer API client and resumable UI state, emptyState(), IntakeController, isConflict(), isOffline(), safeMessage(), Language

### Community 10 - "test_lookup.py"
Cohesion: 0.35
Nodes (10): _ex(), _match(), test_ambiguous_then_disambiguated_by_counterpart(), test_amount_and_date_mismatch(), test_no_phone_is_not_found(), test_not_applicable_category(), test_ref_matched(), test_ref_not_found() (+2 more)

### Community 11 - "test_rag_api.py"
Cohesion: 0.09
Nodes (31): init_db(), make_engine(), make_sessionmaker(), reset_db(), create_app(), lifespan(), intake_client(), intake_db() (+23 more)

### Community 12 - "employee-frontend/package.json"
Cohesion: 0.07
Nodes (29): @base-ui/react, class-variance-authority, cn, eslint, @eslint/js, eslint-plugin-react-hooks, eslint-plugin-react-refresh, globals (+21 more)

### Community 14 - "test_draft_guardrails.py"
Cohesion: 0.13
Nodes (28): check_draft(), _citation_findings(), requests_credentials(), check(), test_aggregation_is_deduplicated_and_has_no_state_side_effects(), test_amount_occurrences_keep_their_own_currency_and_sign(), test_avoid_sharing_warning_does_not_excuse_a_later_request(), test_candidate_prompt_limit_does_not_hide_later_ungrounded_references() (+20 more)

### Community 15 - "Support Taxonomy Categories"
Cohesion: 0.21
Nodes (22): lookup, Account KYC, Account & Security, Agent Dispute, Agent Network, App Bug, Bill Payment, Card Issue (+14 more)

### Community 16 - "ui/package.json"
Cohesion: 0.07
Nodes (28): @fontsource-variable/figtree, @turbo/gen, zod, @base-ui/react, class-variance-authority, cn, eslint, @eslint/js (+20 more)

### Community 17 - "employee-frontend/src/App.tsx"
Cohesion: 0.19
Nodes (17): App(), EvaluationPage, InsightsPage, KnowledgePage, NewBatchPage, QueuePage, RunDetailPage, RunsPage (+9 more)

### Community 18 - "users-frontend/package.json"
Cohesion: 0.09
Nodes (22): turbo, devDependencies, prettier, prettier-plugin-tailwindcss, turbo, typescript, engines, node (+14 more)

### Community 19 - "TicketRow"
Cohesion: 0.13
Nodes (15): get_session(), get_result(), list_results(), read_intake_attachment(), review_result(), ReviewInput, health(), insights() (+7 more)

### Community 20 - "UploadedDocument"
Cohesion: 0.09
Nodes (23): delete_document(), download_document(), index_document(), list_chunks(), list_documents(), _require_provider(), search_knowledge(), upload_document() (+15 more)

### Community 21 - "web/package.json"
Cohesion: 0.08
Nodes (25): jsdom, @testing-library/user-event, @workspace/ui, eslint, @eslint/js, eslint-plugin-react-hooks, eslint-plugin-react-refresh, globals (+17 more)

### Community 22 - "test_cli.py"
Cohesion: 0.18
Nodes (9): test_config_error_exits_2(), boom(), test_ingest_directory_is_deterministic_and_duplicate_is_free(), test_ingest_disabled_configuration_never_calls_provider(), test_ingest_failure_exit_and_retry_stored(), test_ingest_invalid_source_does_not_stop_other_files(), test_ingest_limits_batch_without_partial_side_effects(), test_retry_stored_indexes_old_uploads_without_recovering_other_process_jobs() (+1 more)

### Community 23 - "compilerOptions"
Cohesion: 0.09
Nodes (22): compilerOptions, allowArbitraryExtensions, allowImportingTsExtensions, erasableSyntaxOnly, jsx, lib, module, moduleDetection (+14 more)

### Community 24 - "employee-frontend/components.json"
Cohesion: 0.09
Nodes (21): aliases, components, hooks, lib, ui, utils, iconLibrary, menuAccent (+13 more)

### Community 25 - "KnowledgeService"
Cohesion: 0.11
Nodes (17): _abandoned(), _Claim, DocumentNotFoundError, _error_cost(), KnowledgeError, KnowledgeService, FakeEmbedder, test_category_filters_include_general_policies_and_validate_tags() (+9 more)

### Community 26 - "compilerOptions"
Cohesion: 0.09
Nodes (21): compilerOptions, allowArbitraryExtensions, allowImportingTsExtensions, erasableSyntaxOnly, jsx, lib, module, moduleDetection (+13 more)

### Community 27 - "web/src/components/theme-provider.tsx"
Cohesion: 0.17
Nodes (12): App(), disableTransitionsTemporarily(), getSystemTheme(), isEditableTarget(), isTheme(), ResolvedTheme, Theme, THEME_VALUES (+4 more)

### Community 28 - "test_embeddings.py"
Cohesion: 0.08
Nodes (40): EmbeddingError, _nonnegative_number(), OpenRouterEmbedder, _ordered_vectors(), _response_cost(), _percentile(), Embeddings, embedder_for() (+32 more)

### Community 29 - "Classify and Extract Prompts"
Cohesion: 0.31
Nodes (9): extract, gemini_classify, Pipeline Graph Orchestration, jev_classify, prepare, Gemini Classify Prompt v1, Gemini Extract Prompt v1, GeminiClassifier (+1 more)

### Community 30 - "FakeJevRunnable"
Cohesion: 0.09
Nodes (27): CredentialCheck, DegradedCredentialChecker, _finite_nonnegative(), _get(), JevCredentialChecker, FakeJevRunnable, ResponseRunnable, test_bad_usage_cannot_poison_cost() (+19 more)

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
Nodes (26): KnowledgeChunk, KnowledgeDocumentIndex, IndexAttemptLostError, GatedEmbedder, PaidEmbedder, count_chunks(), test_competing_callers_refuse_active_attempt_and_release_transactions(), test_db_deadline_cancelled_publication_cannot_commit_late() (+18 more)

### Community 36 - "web/components.json"
Cohesion: 0.10
Nodes (19): aliases, components, hooks, lib, ui, utils, iconLibrary, menuAccent (+11 more)

### Community 38 - "tests/test_repository.py"
Cohesion: 0.13
Nodes (27): get_run(), list_runs(), start_run(), BatchInput, RunRow, create_run(), finish_run(), save_outcomes() (+19 more)

### Community 39 - "ui/components.json"
Cohesion: 0.10
Nodes (19): aliases, components, hooks, lib, ui, utils, iconLibrary, menuAccent (+11 more)

### Community 40 - "TicketResultRow"
Cohesion: 0.18
Nodes (12): _safe_dispatch(), TicketResultRow, IntakeSubmissionRow, employee_attachment(), intake_result_view(), recover(), fail_intake_placeholders(), reconcile_intake_run() (+4 more)

### Community 41 - "Analysis"
Cohesion: 0.17
Nodes (20): Analysis, _amount(), analyze(), complete_conversation(), _dated(), _message(), _opening(), _png() (+12 more)

### Community 43 - "Human Review Gate"
Cohesion: 0.25
Nodes (4): support CLI, Support Workspace UI Plan, Review API, Workspace UI Verification

### Community 44 - "compilerOptions"
Cohesion: 0.12
Nodes (16): compilerOptions, allowImportingTsExtensions, erasableSyntaxOnly, lib, module, moduleDetection, noEmit, noFallthroughCasesInSwitch (+8 more)

### Community 46 - "pipeline/graph.py"
Cohesion: 0.10
Nodes (20): Candidates, ClassifierOutput, ExtractedField, LookupResult, NormalizedTicket, _default_retry(), _retryable(), Classifier (+12 more)

### Community 47 - "compilerOptions"
Cohesion: 0.12
Nodes (16): compilerOptions, allowImportingTsExtensions, erasableSyntaxOnly, lib, module, moduleDetection, noEmit, noFallthroughCasesInSwitch (+8 more)

### Community 48 - "support_test"
Cohesion: 0.16
Nodes (14): ingest(), support_test(), Execution conventions and repository baseline, Artifacts, servers and remaining concerns, Citation IDs and provider evidence, Commands and automated verification — historical Task 8, Corpus and actual retrieval, Current final verification and review closure (+6 more)

### Community 57 - "parse_document"
Cohesion: 0.08
Nodes (40): TextChunk, _append_chunks(), _check_extracted_size(), DocumentParseError, parse_document(), _parse_pdf(), make_pdf(), test_arabic_text_and_bom_are_preserved() (+32 more)

### Community 58 - "tools.py"
Cohesion: 0.06
Nodes (20): Passage, SearchResult, DraftAlreadySubmitted, DraftSubmission, DraftToolLimit, build_tools(), flag(), guarded() (+12 more)

### Community 59 - "intake/contracts.py"
Cohesion: 0.26
Nodes (8): _aware(), CustomerReview, IntakeModel, Message, Question, QuestionRecord, ReviewSnapshot, Shared contracts (implement in Task 1; extend only through explicit edits here)

### Community 60 - "SqlInvestigationRepo"
Cohesion: 0.16
Nodes (14): TxnRecord, parse_dt(), DraftToolInputError, _datetime(), _days(), _field(), _involves(), _phone() (+6 more)

### Community 61 - "NewBatchPage.tsx"
Cohesion: 0.12
Nodes (15): Input(), Tabs(), TabsContent(), TabsList(), tabsListVariants, TabsTrigger(), readReport(), exampleTickets (+7 more)

### Community 62 - "rules.py"
Cohesion: 0.20
Nodes (16): Decision, decide(), empty_ticket_decision(), merge_reasons(), note_for(), _unique(), Category, _decide() (+8 more)

### Community 63 - "cli.py"
Cohesion: 0.10
Nodes (23): _command_settings(), ingest_kb_cmd(), init_db_cmd(), Mode, run_batch_cmd(), _run_in_memory(), _run_with_db(), seed_db_cmd() (+15 more)

### Community 64 - "tasks"
Cohesion: 0.12
Nodes (16): dependsOn, inputs, outputs, cache, persistent, dependsOn, dependsOn, $schema (+8 more)

### Community 65 - "types.ts"
Cohesion: 0.13
Nodes (25): source, PipelineTrace(), STAGE_NODES, timing(), renderableTrace(), reviewEvidence(), source, checkFact() (+17 more)

### Community 66 - "IntakePage.tsx"
Cohesion: 0.22
Nodes (10): ChatTranscript(), copy, IntakeCopy, IntakePage(), send(), MessageComposer(), ReceiptPanel(), ScreenshotPicker() (+2 more)

### Community 67 - "submission.py"
Cohesion: 0.12
Nodes (11): Credentials, Receipt, SessionView, IntakeOperationRow, IntakeRepository, IntakeService, current_session_view(), SubmissionResult (+3 more)

### Community 68 - "make_ticket"
Cohesion: 0.35
Nodes (16): make_output(), make_ticket(), _deps(), _run(), test_cascade_confident_jev_skips_gemini(), test_cascade_degrades_when_jev_fails(), test_cascade_uncertain_jev_goes_to_gemini(), test_concurrency_is_limited() (+8 more)

### Community 69 - "_DatabaseCall"
Cohesion: 0.17
Nodes (3): _check_deadline(), _consume(), _DatabaseCall

### Community 72 - "factory.py"
Cohesion: 0.08
Nodes (14): StructuredLLM, build_pipeline(), make_draft_model(), make_jev_client(), GeminiExtractor, UnavailableDrafter, load_taxonomy(), most_urgent() (+6 more)

### Community 73 - "guardrails.py"
Cohesion: 0.05
Nodes (60): canonical_digits(), normalize_reported_date(), Candidate, _add(), find_candidates(), normalize_phone(), _overlaps(), parse_amount() (+52 more)

### Community 74 - "use-knowledge-library.ts"
Cohesion: 0.09
Nodes (31): acceptIndexRequest(), canRequestIndex(), PendingIndexes, persistPendingIndexes(), pollKnowledge(), refresh(), stop(), PollOptions (+23 more)

### Community 75 - "test-kb/README.md"
Cohesion: 0.11
Nodes (9): Fictional RAG walkthrough inputs, توثيق الحساب — سياسة خيالية للعرض التجريبي, أعطال التطبيق — سياسة خيالية للعرض التجريبي, دفع الفواتير — سياسة خيالية للعرض التجريبي, مشاكل البطاقة — سياسة خيالية للعرض التجريبي, تصعيد شبهة الاحتيال — سياسة خيالية للعرض التجريبي, استعادة الدخول — سياسة خيالية للعرض التجريبي, استرجاع مبلغ شراء — سياسة خيالية للعرض التجريبي (+1 more)

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

### Community 93 - "jev.py"
Cohesion: 0.26
Nodes (10): ClassificationResult, build_order_check(), build_questions(), build_state(), category_criteria(), _input_tokens(), JevClassifier, _picks() (+2 more)

### Community 94 - "devDependencies"
Cohesion: 0.11
Nodes (19): devDependencies, eslint, @eslint/js, eslint-plugin-react-hooks, eslint-plugin-react-refresh, globals, jsdom, @tailwindcss/vite (+11 more)

### Community 95 - "devDependencies"
Cohesion: 0.14
Nodes (14): devDependencies, eslint, @eslint/js, eslint-plugin-react-hooks, eslint-plugin-react-refresh, globals, tailwindcss, @tailwindcss/vite (+6 more)

### Community 96 - "FakeClassifier"
Cohesion: 0.22
Nodes (11): build_graph(), PipelineDeps, InMemoryTransactionRepo, FakeClassifier, pipeline(), test_run_batch_no_db_writes_summary_and_out(), fake_build(), run_provider_pipeline() (+3 more)

### Community 97 - "DraftResult"
Cohesion: 0.17
Nodes (7): DraftResult, Drafter, NullDrafter, draft(), draft(), draft(), 2. Current implementation and integration points

### Community 98 - "TicketReviewPage.tsx"
Cohesion: 0.18
Nodes (11): Textarea(), canReview(), REVIEWABLE, ReviewEditor(), save(), reviewerNote(), Resource, teams (+3 more)

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

### Community 103 - "employee-frontend/src/components/theme-provider.tsx"
Cohesion: 0.21
Nodes (11): disableTransitionsTemporarily(), getSystemTheme(), isEditableTarget(), isTheme(), ResolvedTheme, Theme, THEME_VALUES, ThemeProvider() (+3 more)

### Community 104 - "dependencies"
Cohesion: 0.17
Nodes (12): dependencies, @base-ui/react, class-variance-authority, cn, @fontsource-variable/figtree, @hugeicons/core-free-icons, @hugeicons/react, react (+4 more)

### Community 105 - "compilerOptions"
Cohesion: 0.17
Nodes (11): compilerOptions, jsx, lib, module, moduleResolution, outDir, skipLibCheck, strict (+3 more)

### Community 106 - "IntakeApi"
Cohesion: 0.26
Nodes (7): IntakeApi, OwnedImage(), factText(), ReviewPanel(), Attachment, Credentials, SessionView

### Community 107 - "controller.test.ts"
Cohesion: 0.20
Nodes (7): controller, emptySession(), fakeApi(), review, browserSessionStorage(), SessionStorage, SavedSession

### Community 108 - "test_workspace_api.py"
Cohesion: 0.25
Nodes (6): start_run(), test_batch_and_queue_expose_real_results(), test_batch_failure_is_isolated_and_conflicting_ids_rejected(), test_progress_counts_only_durable_results_after_save_failure(), fail_one_save(), test_review_requires_text_and_rejects_stale_updates()

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

### Community 114 - "test_llm.py"
Cohesion: 0.13
Nodes (11): GeminiStructuredLLM, make_gemini_llm(), _llm(), _S, test_draft_model_uses_millisecond_timeout_and_disables_sdk_retries(), test_openrouter_reported_cost_takes_precedence_over_token_estimate(), test_openrouter_retry_budget_is_bounded(), test_openrouter_structured_samples_use_configured_key_and_validate_output() (+3 more)

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

### Community 119 - "Settings"
Cohesion: 0.10
Nodes (11): Settings, taxonomy(), test_blank_intake_model_is_rejected(), test_non_positive_image_limit_is_rejected(), test_defaults(), test_drafting_configuration_cannot_bypass_hard_limits(), test_drafting_limits_load_from_environment(), test_env_overrides() (+3 more)

### Community 120 - "scripts"
Cohesion: 0.50
Nodes (4): scripts, format, lint, typecheck

### Community 122 - "fact"
Cohesion: 0.13
Nodes (45): EvidenceRef, Fact, IntakeState, Readiness, _apply(), _check_reference(), _compact(), merge_analysis() (+37 more)

### Community 123 - "IntakePage.test.tsx"
Cohesion: 0.31
Nodes (9): Task 7: Bilingual customer chat, screenshots and reviewed submission, copy(), attachment, collectingController(), emptySession(), fakeApi(), readyController(), review (+1 more)

### Community 124 - "intake/repository.py"
Cohesion: 0.08
Nodes (44): AttachmentStore, _display_name(), Attachment, IntakeAttachmentRow, IntakeMessageRow, IntakeSessionRow, ImageRejected, IntakeError (+36 more)

### Community 125 - "TicketOutcome"
Cohesion: 0.53
Nodes (5): TicketOutcome, outcome_to_dict(), outcome_to_row(), test_failed_outcome_and_dict_form(), test_full_outcome_is_json_safe()

### Community 126 - "InvalidEvidence"
Cohesion: 0.16
Nodes (14): ReviewText, TurnContext, InvalidEvidence, IntakeGraph, _invitation(), build_review(), _compact(), _render_value() (+6 more)

### Community 127 - "build_pipeline"
Cohesion: 0.12
Nodes (18): SqlTransactionRepo, ConfigError, run_batch(), GeminiAnalysis, FakeStructuredLLM, ScriptedChat, _settings(), test_all_modes_use_credential_checker_independently_of_classifier() (+10 more)

### Community 128 - "answer"
Cohesion: 0.42
Nodes (9): answer(), call(), submit(), test_real_search_fault_carries_safe_draft_execution_error(), pipeline(), submit(), test_graph_recursion_bounds_unknown_tool_loop(), test_invalid_tool_arguments_are_traced_and_not_accepted() (+1 more)

### Community 129 - "intake/model.py"
Cohesion: 0.10
Nodes (22): ImageInput, ModelCall, ModelUnavailable, _analysis_prompt(), _bounded_context(), _guard_size(), ModelBudget, OpenRouterIntakeModel (+14 more)

### Community 130 - "Customer Conversation Intake Implementation Plan"
Cohesion: 0.29
Nodes (6): Customer Conversation Intake Implementation Plan, File map and dependency order, Global Constraints, Plan review and execution handoff, Review Focus, Spec coverage and acceptance map

### Community 131 - "intake.py"
Cohesion: 0.15
Nodes (19): create_session(), _credentials(), _dump(), get_session(), post_message(), read_attachment(), remove_attachment(), request_review() (+11 more)

### Community 132 - "test_final_fix_handoff.py"
Cohesion: 0.11
Nodes (20): Knowledge, assert_completed_evidence(), faulty_knowledge(), read(), outer_deadlines(), PaidEmbeddings, runner_env(), build() (+12 more)

### Community 133 - "Synthetic demo readiness"
Cohesion: 0.50
Nodes (4): Evidence by layer, Known limitations and remaining work, Repeatable local walkthrough, Synthetic demo readiness

### Community 134 - "EmbeddingBatch"
Cohesion: 0.15
Nodes (5): Embedder, EmbeddingBatch, LateEmbedder, test_lock_serializes_operations_and_submit_waits_for_inflight_search(), embed()

### Community 135 - "test_draft_model.py"
Cohesion: 0.33
Nodes (6): response_payload(), send(), search_response(), test_empty_choices_escalates_and_keeps_paid_response_usage(), test_failed_response_id_is_deduplicated_against_earlier_success(), test_other_conversion_value_errors_remain_unexpected()

### Community 137 - "index_deadlines"
Cohesion: 0.40
Nodes (3): index_deadlines(), settings(), expire_during_embedding()

### Community 139 - "test_draft_tools.py"
Cohesion: 0.09
Nodes (33): IncidentRow, _payload(), test_concurrent_submit_dispatches_once(), test_second_request_id_reuses_the_approved_review(), test_submission_replay_creates_one_ticket(), api(), ErrorEmbedder, settings() (+25 more)

### Community 140 - "test_dbapi_commit_handoff_arbitrates_cancellation"
Cohesion: 0.47
Nodes (4): test_dbapi_commit_handoff_arbitrates_cancellation(), gate(), gate_before_dbapi(), gate_inside_dbapi()

### Community 142 - "Customer intake verification — 2026-10-18"
Cohesion: 0.50
Nodes (3): Automated, Customer intake verification — 2026-10-18, Not verified live

### Community 149 - "agent.py"
Cohesion: 0.07
Nodes (12): KnowledgeExecutionError, _error_cost(), _Execution, _ModelUsage, _number(), RagDrafter, DraftContext, CredentialChecker (+4 more)

## Ambiguous Edges - Review These
- `Fraud Report` → `Plan 1 Live Smoke`  [AMBIGUOUS]
  README.md · relation: conceptually_related_to

## Knowledge Gaps
- **88 isolated node(s):** `zaincash-support`, `@base-ui/react`, `@fontsource-variable/geist`, `@tailwindcss/vite`, `class-variance-authority` (+83 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 957 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **45 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `HTTP contract (implemented in Tasks 4–5)` connect `Analysis` to `intake/model.py`, `Customer Conversation Intake Implementation Plan`, `TurnStore`, `tests/test_repository.py`, `guardrails.py`, `IntakeController`, `IntakePage.test.tsx`, `intake/repository.py`?**
  _High betweenness centrality (0.136) - this node is a cross-community bridge._
- **Are the 33 inferred relationships involving `Settings` (e.g. with `_command_settings()` and `_run_in_memory()`) actually correct?**
  _`Settings` has 33 INFERRED edges - model-reasoned connections that need verification._
- **What connects `zaincash-support`, `@base-ui/react`, `@fontsource-variable/geist` to the rest of the system?**
  _88 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `fakes.py` be split into smaller, more focused modules?**
  _Cohesion score 0.12857142857142856 - nodes in this community are weakly interconnected._
- **Why does `Settings` connect `Settings` to `intake/model.py`, `test_rag_drafter.py`, `test_final_fix_handoff.py`, `Synthetic demo readiness`, `test_draft_model.py`, `main.py`, `index_deadlines`, `test_rag_api.py`, `test_draft_tools.py`, `agent.py`, `test_cli.py`, `KnowledgeService`, `test_embeddings.py`, `test_kb_service.py`, `tests/test_repository.py`, `support_test`, `tools.py`, `cli.py`, `submission.py`, `factory.py`, `FakeClassifier`, `test_workspace_api.py`, `test_llm.py`, `fact`, `intake/repository.py`, `build_pipeline`?**
  _High betweenness centrality (0.084) - this node is a cross-community bridge._
- **Are the 24 inferred relationships involving `KnowledgeService` (e.g. with `Settings` and `UploadedDocument`) actually correct?**
  _`KnowledgeService` has 24 INFERRED edges - model-reasoned connections that need verification._

### Low-confidence Hints
_AMBIGUOUS edges — the extractor was unsure. Verify before acting on these._

- **What is the exact relationship between `Fraud Report` and `Plan 1 Live Smoke`?**
  _Edge tagged AMBIGUOUS (relation: conceptually_related_to) - confidence is low._