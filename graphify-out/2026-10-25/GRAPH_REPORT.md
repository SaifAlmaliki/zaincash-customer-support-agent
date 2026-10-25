# Graph Report - zaincash-support  (2026-10-18)

## Corpus Check
- 281 files · ~223,607 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 26 file(s) not represented in the graph (top: (none) 15, .jsonl 4, .css 4)

## Summary
- 2843 nodes · 8560 edges · 155 communities (116 shown, 39 thin omitted)
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
- IntakeGraph
- TicketReviewPage.tsx
- InvalidEvidence
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
- KnowledgeError
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
- lib/types.ts
- IntakePage.tsx
- EmbeddingError
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
- factory.py
- TicketReviewPage.tsx
- compilerOptions
- قواعد المعرفة العربية للعرض أمام لجنة التحكيم
- pydantic
- dependencies
- employee-frontend/src/components/theme-provider.tsx
- dependencies
- compilerOptions
- response_payload
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
- context
- IntakePage.test.tsx
- intake/repository.py
- KnowledgePage.tsx
- review.py
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
- ref_vitest
- ingest.py
- test_dbapi_commit_handoff_arbitrates_cancellation
- IntakeState
- Customer intake verification — 2026-10-18
- @testing-library/react
- start_run
- health
- Plan 3 RAG Drafting Implementation Plan
- intake/README.md
- TicketInput
- task8-history-policy.md
- ar/failed_transfer.md
- ar/other.md

## God Nodes (most connected - your core abstractions)
1. `Settings` - 93 edges
2. `KnowledgeService` - 79 edges
3. `PipelineState` - 50 edges
4. `IntakeController` - 45 edges
5. `make_output()` - 44 edges
6. `make_ticket()` - 44 edges
7. `draft_state()` - 44 edges
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

## Communities (155 total, 39 thin omitted)

### Community 0 - "fakes.py"
Cohesion: 0.14
Nodes (22): LLMUnavailable, FieldPick, combine(), merge_picks(), verified_pick(), finalize(), FakeExtractor, test_both_missing_raises() (+14 more)

### Community 1 - "intake/types.ts"
Cohesion: 0.12
Nodes (21): IntakeApi, UploadResult, OwnedImage(), factText(), ReviewPanel(), Attachment, Credentials, EvidenceRef (+13 more)

### Community 2 - "test_rag_drafter.py"
Cohesion: 0.21
Nodes (30): Checker, draft_state(), script(), drafter(), events(), test_callback_partial_response_and_error_cost_are_alternatives(), test_checker_timeout_keeps_already_computed_deterministic_findings(), test_concurrent_tickets_cannot_exchange_citations_cost_or_callback_state() (+22 more)

### Community 3 - "IntakeGraph"
Cohesion: 0.16
Nodes (6): IntakeGraph, _invitation(), HTTP contract (implemented in Tasks 4–5), Task 2: Evidence merging and adaptive readiness, Task 4: Resumable graph turns, review and customer API, Task 9: End-to-end handoff, live vision evidence and runbook

### Community 4 - "TicketReviewPage.tsx"
Cohesion: 0.15
Nodes (27): Confidence(), Metric(), Badge(), Card(), CardContent(), CardHeader(), CardTitle(), EvaluationPage() (+19 more)

### Community 5 - "InvalidEvidence"
Cohesion: 0.19
Nodes (16): Fact, canonical_digits(), normalize_reported_date(), InvalidEvidence, _apply(), _check_reference(), _compact(), _newer_correction() (+8 more)

### Community 6 - "QueuePage.tsx"
Cohesion: 0.21
Nodes (29): EmptyState(), ErrorState(), LoadingState(), PageHeader(), PriorityBadge(), StatusBadge(), Table(), TableBody() (+21 more)

### Community 7 - "Customer conversation intake for ZainCash support"
Cohesion: 0.06
Nodes (31): 10. Verification and acceptance criteria, 11. Delivery and review, 1. Outcome and agreed requirements, 2. Current implementation and integration points, 3. Approach and boundaries, 4. Conversation state and turn flow, 5. Facts, evidence, and readiness, 6. Language and screenshot behavior (+23 more)

### Community 8 - "workspace-ui.tsx"
Cohesion: 0.15
Nodes (19): ConfirmDialog(), FilterSelect(), statusLabels, Button(), buttonVariants, Dialog(), DialogContent(), DialogDescription() (+11 more)

### Community 9 - "IntakeController"
Cohesion: 0.16
Nodes (6): Task 6: Customer API client and resumable UI state, IntakeController, isConflict(), isOffline(), safeMessage(), Language

### Community 10 - "test_lookup.py"
Cohesion: 0.22
Nodes (12): match_transaction(), TransactionRepo, _ex(), _match(), test_ambiguous_then_disambiguated_by_counterpart(), test_amount_and_date_mismatch(), test_no_phone_is_not_found(), test_not_applicable_category() (+4 more)

### Community 11 - "test_rag_api.py"
Cohesion: 0.15
Nodes (17): client(), evidence_client(), test_actual_guardrail_failure_is_separate_from_reply(), test_concurrent_index_requests_share_active_work(), test_disabled_or_missing_provider_stores_without_indexing(), test_explicit_retry_tags_search_and_chunk_pagination(), test_health_distinguishes_failed_from_empty(), test_health_requires_compatible_nonempty_index() (+9 more)

### Community 12 - "employee-frontend/package.json"
Cohesion: 0.07
Nodes (29): @base-ui/react, class-variance-authority, cn, eslint, @eslint/js, eslint-plugin-react-hooks, eslint-plugin-react-refresh, globals (+21 more)

### Community 14 - "test_draft_guardrails.py"
Cohesion: 0.14
Nodes (27): LookupResult, requests_credentials(), check(), state(), test_aggregation_is_deduplicated_and_has_no_state_side_effects(), test_amount_occurrences_keep_their_own_currency_and_sign(), test_avoid_sharing_warning_does_not_excuse_a_later_request(), test_candidate_prompt_limit_does_not_hide_later_ungrounded_references() (+19 more)

### Community 15 - "Support Taxonomy Categories"
Cohesion: 0.21
Nodes (22): lookup, Account KYC, Account & Security, Agent Dispute, Agent Network, App Bug, Bill Payment, Card Issue (+14 more)

### Community 16 - "ui/package.json"
Cohesion: 0.07
Nodes (28): @fontsource-variable/figtree, @turbo/gen, zod, @base-ui/react, class-variance-authority, cn, eslint, @eslint/js (+20 more)

### Community 17 - "employee-frontend/src/App.tsx"
Cohesion: 0.17
Nodes (17): App(), EvaluationPage, InsightsPage, KnowledgePage, NewBatchPage, QueuePage, RunDetailPage, RunsPage (+9 more)

### Community 18 - "users-frontend/package.json"
Cohesion: 0.09
Nodes (22): turbo, devDependencies, prettier, prettier-plugin-tailwindcss, turbo, typescript, engines, node (+14 more)

### Community 19 - "TicketRow"
Cohesion: 0.11
Nodes (20): get_session(), get_result(), list_results(), read_intake_attachment(), review_result(), get_run(), list_runs(), ReviewInput (+12 more)

### Community 20 - "UploadedDocument"
Cohesion: 0.10
Nodes (25): delete_document(), download_document(), index_document(), list_chunks(), list_documents(), _require_provider(), search_knowledge(), upload_document() (+17 more)

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

### Community 25 - "KnowledgeError"
Cohesion: 0.13
Nodes (5): KnowledgeError, KnowledgeExecutionError, test_db_deadline_cancelled_publication_cannot_commit_late(), test_db_deadline_is_cumulative_across_publication_statements(), changed_index()

### Community 26 - "compilerOptions"
Cohesion: 0.09
Nodes (21): compilerOptions, allowArbitraryExtensions, allowImportingTsExtensions, erasableSyntaxOnly, jsx, lib, module, moduleDetection (+13 more)

### Community 27 - "web/src/components/theme-provider.tsx"
Cohesion: 0.17
Nodes (12): App(), disableTransitionsTemporarily(), getSystemTheme(), isEditableTarget(), isTheme(), ResolvedTheme, Theme, THEME_VALUES (+4 more)

### Community 28 - "test_embeddings.py"
Cohesion: 0.17
Nodes (18): OpenRouterEmbedder, settings(), test_33_inputs_are_batched_and_each_batch_maps_its_own_indexes(), test_billed_batch_cost_survives_cancellation_without_cross_call_leakage(), test_cancellation_propagates_to_the_callers_deadline(), test_empty_input_returns_empty_batch_without_a_request(), unexpected_request(), test_invalid_rag_settings_are_rejected() (+10 more)

### Community 29 - "Classify and Extract Prompts"
Cohesion: 0.31
Nodes (9): extract, gemini_classify, Pipeline Graph Orchestration, jev_classify, prepare, Gemini Classify Prompt v1, Gemini Extract Prompt v1, GeminiClassifier (+1 more)

### Community 30 - "FakeJevRunnable"
Cohesion: 0.05
Nodes (59): CredentialCheck, DegradedCredentialChecker, _finite_nonnegative(), _get(), JevCredentialChecker, FakeJevRunnable, test_contracts_reject_extra_keys(), test_datetimes_must_be_timezone_aware() (+51 more)

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
Nodes (33): KnowledgeChunk, KnowledgeService, FakeEmbedder, GatedEmbedder, PaidEmbedder, count_chunks(), test_category_filters_include_general_policies_and_validate_tags(), test_claim_locks_source_even_before_index_row_exists() (+25 more)

### Community 36 - "web/components.json"
Cohesion: 0.10
Nodes (19): aliases, components, hooks, lib, ui, utils, iconLibrary, menuAccent (+11 more)

### Community 38 - "db/repository.py"
Cohesion: 0.12
Nodes (27): _run_with_db(), IncidentRow, create_run(), finish_run(), load_incidents(), load_transactions(), save_outcomes(), _to_record() (+19 more)

### Community 39 - "ui/components.json"
Cohesion: 0.10
Nodes (19): aliases, components, hooks, lib, ui, utils, iconLibrary, menuAccent (+11 more)

### Community 40 - "TicketResultRow"
Cohesion: 0.18
Nodes (15): _safe_dispatch(), RunRow, recover(), TicketExecution, run_job(), fail_intake_placeholders(), reconcile_intake_run(), recover_intake_processing() (+7 more)

### Community 41 - "Analysis"
Cohesion: 0.18
Nodes (29): Analysis, EvidenceRef, merge_analysis(), remove_attachment_evidence(), fact(), grounded_analysis(), message(), test_assistant_text_cannot_ground_a_customer_fact() (+21 more)

### Community 43 - "Human Review Gate"
Cohesion: 0.25
Nodes (4): support CLI, Support Workspace UI Plan, Review API, Workspace UI Verification

### Community 44 - "compilerOptions"
Cohesion: 0.12
Nodes (16): compilerOptions, allowImportingTsExtensions, erasableSyntaxOnly, lib, module, moduleDetection, noEmit, noFallthroughCasesInSwitch (+8 more)

### Community 46 - "pipeline/graph.py"
Cohesion: 0.11
Nodes (12): Candidates, ExtractedField, NormalizedTicket, _default_retry(), _retryable(), Classifier, FieldExtractor, _field() (+4 more)

### Community 47 - "compilerOptions"
Cohesion: 0.12
Nodes (16): compilerOptions, allowImportingTsExtensions, erasableSyntaxOnly, lib, module, moduleDetection, noEmit, noFallthroughCasesInSwitch (+8 more)

### Community 48 - "support_test"
Cohesion: 0.20
Nodes (12): support_test(), Task 3: Ticket-scoped investigation and all eight tools, Task 8: Demo corpus, full verification and readiness record, Citation IDs and provider evidence, Commands and automated verification — historical Task 8, Corpus and actual retrieval, Current final verification and review closure, Environment and isolation (+4 more)

### Community 57 - "parse_document"
Cohesion: 0.11
Nodes (28): _append_chunks(), _check_extracted_size(), DocumentParseError, parse_document(), _parse_pdf(), make_pdf(), test_arabic_text_and_bom_are_preserved(), test_blank_pdf_tells_operator_to_use_ocr() (+20 more)

### Community 58 - "tools.py"
Cohesion: 0.05
Nodes (25): _error_cost(), _Execution, _ModelUsage, _number(), DraftAlreadySubmitted, DraftContext, DraftSubmission, DraftToolLimit (+17 more)

### Community 59 - "intake/contracts.py"
Cohesion: 0.18
Nodes (11): _aware(), IntakeModel, Message, QuestionRecord, Readiness, ReviewSnapshot, TurnResult, repo() (+3 more)

### Community 60 - "SqlInvestigationRepo"
Cohesion: 0.16
Nodes (14): TxnRecord, parse_dt(), DraftToolInputError, _datetime(), _days(), _field(), _involves(), _phone() (+6 more)

### Community 61 - "NewBatchPage.tsx"
Cohesion: 0.12
Nodes (16): badgeVariants, Input(), Tabs(), TabsContent(), TabsList(), tabsListVariants, TabsTrigger(), readReport() (+8 more)

### Community 62 - "rules.py"
Cohesion: 0.20
Nodes (16): Decision, decide(), empty_ticket_decision(), merge_reasons(), note_for(), _unique(), Category, _decide() (+8 more)

### Community 63 - "cli.py"
Cohesion: 0.14
Nodes (13): _command_settings(), ingest_kb_cmd(), init_db_cmd(), Mode, run_batch_cmd(), _run_in_memory(), seed_db_cmd(), _sessionmaker() (+5 more)

### Community 64 - "tasks"
Cohesion: 0.12
Nodes (16): dependsOn, inputs, outputs, cache, persistent, dependsOn, dependsOn, $schema (+8 more)

### Community 65 - "lib/types.ts"
Cohesion: 0.11
Nodes (22): intakeFixture, factValue(), IntakeEvidence(), classifySentence(), FIELD_LABELS, fieldValue(), LOOKUP, quoted() (+14 more)

### Community 66 - "IntakePage.tsx"
Cohesion: 0.22
Nodes (10): ChatTranscript(), copy, IntakeCopy, IntakePage(), send(), MessageComposer(), ReceiptPanel(), ScreenshotPicker() (+2 more)

### Community 67 - "EmbeddingError"
Cohesion: 0.17
Nodes (6): EmbeddingError, _nonnegative_number(), _ordered_vectors(), _response_cost(), _percentile(), Embeddings

### Community 68 - "make_ticket"
Cohesion: 0.25
Nodes (19): NullDrafter, FakeClassifier, make_output(), make_ticket(), _deps(), _run(), test_cascade_confident_jev_skips_gemini(), test_cascade_degrades_when_jev_fails() (+11 more)

### Community 69 - "_DatabaseCall"
Cohesion: 0.12
Nodes (5): _check_deadline(), _Claim, _consume(), _DatabaseCall, IndexAttemptLostError

### Community 72 - "factory.py"
Cohesion: 0.13
Nodes (7): most_urgent(), priority_rank(), TaxonomyError, tax(), taxonomy(), test_priority_helpers(), test_rejects_unknown_team()

### Community 73 - "guardrails.py"
Cohesion: 0.06
Nodes (56): Candidate, _add(), find_candidates(), normalize_phone(), _overlaps(), parse_amount(), resolve_date(), _safe_date() (+48 more)

### Community 74 - "use-knowledge-library.ts"
Cohesion: 0.23
Nodes (14): acceptIndexRequest(), canRequestIndex(), PendingIndexes, persistPendingIndexes(), pollKnowledge(), refresh(), stop(), PollOptions (+6 more)

### Community 75 - "test-kb/README.md"
Cohesion: 0.09
Nodes (11): Fictional RAG walkthrough inputs, توثيق الحساب — سياسة خيالية للعرض التجريبي, نزاع مع وكيل — سياسة خيالية للعرض التجريبي, أعطال التطبيق — سياسة خيالية للعرض التجريبي, دفع الفواتير — سياسة خيالية للعرض التجريبي, مشاكل البطاقة — سياسة خيالية للعرض التجريبي, تصعيد شبهة الاحتيال — سياسة خيالية للعرض التجريبي, الاستفسار الآمن من الدعم — سياسة خيالية للعرض التجريبي (+3 more)

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
Cohesion: 0.18
Nodes (13): ClassificationResult, ClassifierOutput, GeminiClassifier, build_order_check(), build_questions(), build_state(), category_criteria(), _input_tokens() (+5 more)

### Community 94 - "devDependencies"
Cohesion: 0.11
Nodes (19): devDependencies, eslint, @eslint/js, eslint-plugin-react-hooks, eslint-plugin-react-refresh, globals, jsdom, @tailwindcss/vite (+11 more)

### Community 95 - "devDependencies"
Cohesion: 0.14
Nodes (14): devDependencies, eslint, @eslint/js, eslint-plugin-react-hooks, eslint-plugin-react-refresh, globals, tailwindcss, @tailwindcss/vite (+6 more)

### Community 96 - "FakeClassifier"
Cohesion: 0.19
Nodes (12): build_graph(), PipelineDeps, InMemoryTransactionRepo, load_taxonomy(), intake_client(), pipeline(), reviewed(), taxonomy() (+4 more)

### Community 97 - "factory.py"
Cohesion: 0.07
Nodes (12): Sample, StructuredLLM, DraftResult, GeminiExtractor, CredentialChecker, Drafter, DraftExecutionError, UnavailableDrafter (+4 more)

### Community 98 - "TicketReviewPage.tsx"
Cohesion: 0.26
Nodes (8): Task 8: Employee evidence panel and processing state, Textarea(), canReview(), REVIEWABLE, ReviewEditor(), save(), reviewerNote(), ReviewInput

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

### Community 106 - "response_payload"
Cohesion: 0.22
Nodes (16): embedder_for(), item(), response_payload(), respond(), respond(), test_billed_cost_survives_cancellation_during_client_close(), test_billed_response_cost_is_retained_when_its_vectors_are_invalid(), test_cost_uses_one_reported_value_or_configured_token_estimate() (+8 more)

### Community 107 - "controller.test.ts"
Cohesion: 0.15
Nodes (11): controller, ControllerState, emptyState(), fileIdentity(), emptySession(), fakeApi(), review, browserSessionStorage() (+3 more)

### Community 108 - "test_workspace_api.py"
Cohesion: 0.19
Nodes (7): start_run(), test_batch_and_queue_expose_real_results(), test_batch_failure_is_isolated_and_conflicting_ids_rejected(), test_openrouter_credentials_enable_api_modes_without_exposing_keys(), test_progress_counts_only_durable_results_after_save_failure(), fail_one_save(), test_review_requires_text_and_rejects_stale_updates()

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
Cohesion: 0.12
Nodes (9): Settings, test_blank_intake_model_is_rejected(), test_non_positive_image_limit_is_rejected(), test_defaults(), test_drafting_configuration_cannot_bypass_hard_limits(), test_drafting_limits_load_from_environment(), test_env_overrides(), test_legacy_gemini_model_names_are_qualified_for_openrouter() (+1 more)

### Community 120 - "scripts"
Cohesion: 0.50
Nodes (4): scripts, format, lint, typecheck

### Community 122 - "context"
Cohesion: 0.23
Nodes (19): Question, _asked_already(), asks_for_secret(), assess_readiness(), _can_ask(), canonical_category(), choose_question(), _fallback() (+11 more)

### Community 123 - "IntakePage.test.tsx"
Cohesion: 0.29
Nodes (10): Task 7: Bilingual customer chat, screenshots and reviewed submission, copy(), attachment, collectingController(), emptySession(), fakeApi(), readyController(), review (+2 more)

### Community 124 - "intake/repository.py"
Cohesion: 0.05
Nodes (62): AttachmentStore, _display_name(), Attachment, Credentials, CustomerReview, OperationClaim, Receipt, SessionView (+54 more)

### Community 125 - "KnowledgePage.tsx"
Cohesion: 0.24
Nodes (9): Resource, api, loadQueue(), ChunkPage, Health, KnowledgeSearchResult, WorkspaceContext, WorkspaceContextValue (+1 more)

### Community 126 - "review.py"
Cohesion: 0.20
Nodes (11): ReviewText, build_review(), _compact(), _render_value(), _ticket_text(), _tokens(), validate_review_numbers(), review() (+3 more)

### Community 127 - "build_pipeline"
Cohesion: 0.12
Nodes (20): SqlTransactionRepo, build_pipeline(), ConfigError, make_jev_client(), run_batch(), GeminiAnalysis, FakeStructuredLLM, ScriptedChat (+12 more)

### Community 128 - "answer"
Cohesion: 0.31
Nodes (7): answer(), call(), submit(), test_real_search_fault_carries_safe_draft_execution_error(), pipeline(), submit(), test_failed_tool_fences_queued_paid_calls_after_return()

### Community 129 - "intake/model.py"
Cohesion: 0.10
Nodes (23): ImageInput, ModelCall, TurnContext, IntakeError, ModelUnavailable, _analysis_prompt(), _bounded_context(), _guard_size() (+15 more)

### Community 130 - "Customer Conversation Intake Implementation Plan"
Cohesion: 0.25
Nodes (7): Customer Conversation Intake Implementation Plan, Execution conventions and repository baseline, File map and dependency order, Global Constraints, Plan review and execution handoff, Review Focus, Spec coverage and acceptance map

### Community 131 - "intake.py"
Cohesion: 0.16
Nodes (19): create_session(), _credentials(), _dump(), get_session(), post_message(), read_attachment(), remove_attachment(), request_review() (+11 more)

### Community 132 - "test_final_fix_handoff.py"
Cohesion: 0.11
Nodes (22): Passage, process_batch(), Knowledge, assert_completed_evidence(), faulty_knowledge(), read(), outer_deadlines(), PaidEmbeddings (+14 more)

### Community 133 - "Synthetic demo readiness"
Cohesion: 0.50
Nodes (4): Evidence by layer, Known limitations and remaining work, Repeatable local walkthrough, Synthetic demo readiness

### Community 134 - "EmbeddingBatch"
Cohesion: 0.13
Nodes (10): Embedder, EmbeddingBatch, SearchResult, TextChunk, _abandoned(), _error_cost(), LateEmbedder, test_lock_serializes_operations_and_submit_waits_for_inflight_search() (+2 more)

### Community 135 - "test_draft_model.py"
Cohesion: 0.25
Nodes (9): make_draft_model(), RagDrafter, response_payload(), run_provider_pipeline(), send(), search_response(), test_empty_choices_escalates_and_keeps_paid_response_usage(), test_failed_response_id_is_deduplicated_against_earlier_success() (+1 more)

### Community 136 - "main.py"
Cohesion: 0.09
Nodes (13): init_db(), make_engine(), make_sessionmaker(), reset_db(), upgrade_workspace_schema(), create_app(), lifespan(), IndexJobs (+5 more)

### Community 137 - "index_deadlines"
Cohesion: 0.40
Nodes (3): index_deadlines(), settings(), expire_during_embedding()

### Community 138 - "ref_vitest"
Cohesion: 0.13
Nodes (9): createIntakeApi(), IntakeRequestError, isRecord(), parseJson(), parseReceipt(), parseSession(), readError(), FakeXHR (+1 more)

### Community 139 - "ingest.py"
Cohesion: 0.26
Nodes (8): load_jsonl(), load_tickets(), _rows(), test_csv_with_bom_and_missing_columns(), test_duplicate_external_ids_keep_first(), test_json_object_without_ids(), test_jsonl_fixture_loads(), test_unsupported_format()

### Community 140 - "test_dbapi_commit_handoff_arbitrates_cancellation"
Cohesion: 0.47
Nodes (4): test_dbapi_commit_handoff_arbitrates_cancellation(), gate(), gate_before_dbapi(), gate_inside_dbapi()

### Community 141 - "IntakeState"
Cohesion: 0.24
Nodes (5): IntakeState, initial_state(), grounded_review(), image_evidence(), ScriptedIntakeModel

### Community 142 - "Customer intake verification — 2026-10-18"
Cohesion: 0.50
Nodes (3): Automated, Customer intake verification — 2026-10-18, Not verified live

### Community 144 - "start_run"
Cohesion: 0.22
Nodes (3): start_run(), BatchInput, model_ids()

### Community 148 - "health"
Cohesion: 0.31
Nodes (6): health(), insights(), workspace(), ingest(), Artifacts, servers and remaining concerns, start()

### Community 149 - "Plan 3 RAG Drafting Implementation Plan"
Cohesion: 0.22
Nodes (9): Completion and review record — 2026-10-17, Execution handoff, File map and shared interfaces, Global Constraints, Plan 3 RAG Drafting Implementation Plan, Plan self-review, Review Focus, Task 6: API/CLI indexing and persisted citation projection (+1 more)

## Ambiguous Edges - Review These
- `Fraud Report` → `Plan 1 Live Smoke`  [AMBIGUOUS]
  README.md · relation: conceptually_related_to

## Knowledge Gaps
- **88 isolated node(s):** `zaincash-support`, `@base-ui/react`, `@fontsource-variable/geist`, `@tailwindcss/vite`, `class-variance-authority` (+83 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 956 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **39 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `HTTP contract (implemented in Tasks 4–5)` connect `IntakeGraph` to `intake/model.py`, `Customer Conversation Intake Implementation Plan`, `TicketReviewPage.tsx`, `TicketResultRow`, `IntakeController`, `IntakePage.test.tsx`?**
  _High betweenness centrality (0.135) - this node is a cross-community bridge._
- **Are the 33 inferred relationships involving `Settings` (e.g. with `_command_settings()` and `_run_in_memory()`) actually correct?**
  _`Settings` has 33 INFERRED edges - model-reasoned connections that need verification._
- **What connects `zaincash-support`, `@base-ui/react`, `@fontsource-variable/geist` to the rest of the system?**
  _88 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `fakes.py` be split into smaller, more focused modules?**
  _Cohesion score 0.14204545454545456 - nodes in this community are weakly interconnected._
- **Why does `Settings` connect `Settings` to `intake/model.py`, `test_rag_drafter.py`, `test_final_fix_handoff.py`, `Synthetic demo readiness`, `EmbeddingBatch`, `test_draft_model.py`, `main.py`, `index_deadlines`, `test_rag_api.py`, `start_run`, `test_cli.py`, `test_embeddings.py`, `FakeJevRunnable`, `test_kb_service.py`, `db/repository.py`, `support_test`, `tools.py`, `cli.py`, `EmbeddingError`, `factory.py`, `FakeClassifier`, `factory.py`, `test_workspace_api.py`, `test_llm.py`, `context`, `intake/repository.py`, `build_pipeline`?**
  _High betweenness centrality (0.086) - this node is a cross-community bridge._
- **Are the 24 inferred relationships involving `KnowledgeService` (e.g. with `Settings` and `UploadedDocument`) actually correct?**
  _`KnowledgeService` has 24 INFERRED edges - model-reasoned connections that need verification._

### Low-confidence Hints
_AMBIGUOUS edges — the extractor was unsure. Verify before acting on these._

- **What is the exact relationship between `Fraud Report` and `Plan 1 Live Smoke`?**
  _Edge tagged AMBIGUOUS (relation: conceptually_related_to) - confidence is low._