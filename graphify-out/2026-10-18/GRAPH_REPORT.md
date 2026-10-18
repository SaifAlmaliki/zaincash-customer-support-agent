# Graph Report - zaincash-support  (2026-10-18)

## Corpus Check
- 258 files · ~214,568 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 25 file(s) not represented in the graph (top: (none) 15, .jsonl 4, .css 3)

## Summary
- 2660 nodes · 8052 edges · 148 communities (108 shown, 40 thin omitted)
- Extraction: 89% EXTRACTED · 11% INFERRED · 0% AMBIGUOUS · INFERRED: 917 edges (avg confidence: 0.93)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `15ab063f`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- LLMUnavailable
- guardrails.py
- test_rag_drafter.py
- intake/repository.py
- TicketReviewPage.tsx
- TicketRow
- QueuePage.tsx
- Customer conversation intake for ZainCash support
- workspace-ui.tsx
- DraftExecutionError
- lookup.py
- test_rag_api.py
- employee-frontend/package.json
- test_draft_guardrails.py
- Support Taxonomy Categories
- ui/package.json
- employee-frontend/src/App.tsx
- users-frontend/package.json
- db/models.py
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
- repository.py
- ui/components.json
- TicketResultRow
- test_draft_tools.py
- Human Review Gate
- compilerOptions
- test_extract.py
- compilerOptions
- RAG drafting verification — 2026-10-17
- Human Flag Tool
- Recent Transactions Tool
- Ticket History Tool
- Lookup Transaction Tool
- Search Transactions Tool
- Submit Draft Tool
- Project Root
- parse_document
- tools.py
- agent.py
- SqlInvestigationRepo
- NewBatchPage.tsx
- rules.py
- cli.py
- tasks
- types.ts
- graph.py
- intake/contracts.py
- make_ticket
- _DatabaseCall
- PipelineState
- stage6_draft/model.py
- taxonomy.py
- normalize.py
- use-knowledge-library.ts
- test-kb/README.md
- ingest.py
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
- rag_fakes.py
- Plan 3 — Knowledge retrieval and grounded reply drafting
- Plan 3 RAG Drafting Implementation Plan
- compilerOptions
- قواعد المعرفة العربية للعرض أمام لجنة التحكيم
- pydantic
- dependencies
- employee-frontend/src/components/theme-provider.tsx
- dependencies
- compilerOptions
- TicketInput
- test_gemini.py
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
- shadcn/ui monorepo template
- evidence.py
- ar/fraud_report.md
- attachments.py
- extract.py
- IntakeState
- build_pipeline
- ar/wrong_recipient.md
- intake/model.py
- Customer Conversation Intake Implementation Plan
- intake.py
- test_final_fix_handoff.py
- Synthetic demo readiness
- kb/service.py
- factory.py
- main.py
- tools.py
- canonical_digits
- test_submission.py
- test_dbapi_commit_handoff_arbitrates_cancellation
- index_deadlines
- tmp-graphify-update.sh
- ar/refund_request.md

## God Nodes (most connected - your core abstractions)
1. `Settings` - 93 edges
2. `KnowledgeService` - 79 edges
3. `PipelineState` - 50 edges
4. `make_output()` - 44 edges
5. `make_ticket()` - 44 edges
6. `draft_state()` - 44 edges
7. `build_pipeline()` - 43 edges
8. `AttachmentStore` - 35 edges
9. `EmbeddingError` - 35 edges
10. `script()` - 35 edges

## Surprising Connections (you probably didn't know these)
- `Repeatable local walkthrough` --references--> `Settings`  [INFERRED]
  docs/demo-readiness.md → backend/app/config.py
- `الأصل ونتيجة التحقق` --references--> `parse_document()`  [INFERRED]
  data/test-kb/README.md → backend/app/kb/parse.py
- `Task 6: API/CLI indexing and persisted citation projection` --references--> `KnowledgeService`  [INFERRED]
  docs/superpowers/plans/2026-10-17-plan3-rag-drafting.md → backend/app/kb/service.py
- `7. Draft guardrails and failure outcomes` --references--> `requests_credentials()`  [INFERRED]
  docs/superpowers/specs/2026-10-17-plan3-rag-drafting-design.md → backend/app/pipeline/stage6_draft/guardrails.py
- `Task 9: End-to-end handoff, live vision evidence and runbook` --references--> `intake_client()`  [INFERRED]
  docs/superpowers/plans/2026-10-18-customer-intake.md → backend/tests/intake/conftest.py

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **Cascade Classification Path** — docs_superpowers_specs_2026_10_07_support_pipeline_design_cascade, docs_superpowers_plans_2026_10_07_plan1_core_pipeline_part2_jev_classifier, docs_superpowers_plans_2026_10_07_plan1_core_pipeline_part2_gemini_classifier, docs_superpowers_plans_2026_10_07_plan1_core_pipeline_part2_cascade_combine, readme_human_approval [EXTRACTED 1.00]
- **Drafting Agent Toolset** — backend_app_pipeline_runner_lookup_transaction, backend_app_pipeline_runner_search_transactions, backend_app_pipeline_runner_get_customer_recent_transactions, backend_app_pipeline_runner_get_customer_ticket_history, backend_app_pipeline_runner_check_service_status, backend_app_pipeline_runner_search_knowledge_base, backend_app_pipeline_runner_flag_for_human, backend_app_pipeline_runner_submit_draft [EXTRACTED 1.00]
- **Ticket Processing Stage Flow** — backend_app_pipeline_runner_prepare, backend_app_pipeline_runner_jev_classify, backend_app_pipeline_runner_gemini_classify, backend_app_pipeline_runner_extract, backend_app_pipeline_runner_lookup, backend_app_pipeline_runner_decide, backend_app_pipeline_runner_draft [EXTRACTED 1.00]

## Communities (148 total, 40 thin omitted)

### Community 0 - "LLMUnavailable"
Cohesion: 0.24
Nodes (11): LLMUnavailable, combine(), merge_picks(), test_both_missing_raises(), test_cost_is_summed(), test_degraded_when_jev_missing(), test_disagreement_when_jev_was_partly_confident(), test_gemini_low_confidence() (+3 more)

### Community 1 - "guardrails.py"
Cohesion: 0.14
Nodes (23): Candidate, _add(), find_candidates(), normalize_phone(), _overlaps(), parse_amount(), to_ascii_digits(), check_draft() (+15 more)

### Community 2 - "test_rag_drafter.py"
Cohesion: 0.22
Nodes (33): answer(), call(), draft_state(), script(), submit(), submit(), drafter(), events() (+25 more)

### Community 3 - "intake/repository.py"
Cohesion: 0.07
Nodes (39): OperationClaim, Receipt, ReviewSnapshot, TurnResult, IntakeMessageRow, IntakeOperationRow, IntakeSessionRow, RevisionConflict (+31 more)

### Community 4 - "TicketReviewPage.tsx"
Cohesion: 0.27
Nodes (16): Confidence(), Metric(), Badge(), badgeVariants, Card(), CardContent(), CardHeader(), CardTitle() (+8 more)

### Community 5 - "TicketRow"
Cohesion: 0.09
Nodes (22): get_session(), get_result(), list_results(), read_intake_attachment(), review_result(), get_run(), list_runs(), start_run() (+14 more)

### Community 6 - "QueuePage.tsx"
Cohesion: 0.22
Nodes (30): EmptyState(), ErrorState(), LoadingState(), PageHeader(), PriorityBadge(), StatusBadge(), Table(), TableBody() (+22 more)

### Community 7 - "Customer conversation intake for ZainCash support"
Cohesion: 0.06
Nodes (31): 10. Verification and acceptance criteria, 11. Delivery and review, 1. Outcome and agreed requirements, 2. Current implementation and integration points, 3. Approach and boundaries, 4. Conversation state and turn flow, 5. Facts, evidence, and readiness, 6. Language and screenshot behavior (+23 more)

### Community 8 - "workspace-ui.tsx"
Cohesion: 0.10
Nodes (19): ConfirmDialog(), FilterSelect(), statusLabels, Button(), buttonVariants, Dialog(), DialogContent(), DialogDescription() (+11 more)

### Community 10 - "lookup.py"
Cohesion: 0.15
Nodes (17): ExtractedField, TxnRecord, _as_date(), InMemoryTransactionRepo, _iqd_amount(), match_transaction(), TransactionRepo, _ex() (+9 more)

### Community 11 - "test_rag_api.py"
Cohesion: 0.14
Nodes (18): create_app(), client(), evidence_client(), test_actual_guardrail_failure_is_separate_from_reply(), test_concurrent_index_requests_share_active_work(), test_disabled_or_missing_provider_stores_without_indexing(), test_explicit_retry_tags_search_and_chunk_pagination(), test_health_distinguishes_failed_from_empty() (+10 more)

### Community 12 - "employee-frontend/package.json"
Cohesion: 0.07
Nodes (28): @base-ui/react, class-variance-authority, cn, eslint, @eslint/js, eslint-plugin-react-hooks, eslint-plugin-react-refresh, globals (+20 more)

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
Cohesion: 0.15
Nodes (19): App(), EvaluationPage, InsightsPage, KnowledgePage, NewBatchPage, QueuePage, RunDetailPage, RunsPage (+11 more)

### Community 18 - "users-frontend/package.json"
Cohesion: 0.09
Nodes (22): turbo, devDependencies, prettier, prettier-plugin-tailwindcss, turbo, typescript, engines, node (+14 more)

### Community 19 - "db/models.py"
Cohesion: 0.15
Nodes (6): Base, IncidentRow, TransactionRow, IntakeSubmissionRow, employee_attachment(), intake_result_view()

### Community 20 - "UploadedDocument"
Cohesion: 0.10
Nodes (24): delete_document(), download_document(), index_document(), list_chunks(), list_documents(), _require_provider(), search_knowledge(), upload_document() (+16 more)

### Community 21 - "web/package.json"
Cohesion: 0.09
Nodes (22): @workspace/ui, eslint, @eslint/js, eslint-plugin-react-hooks, eslint-plugin-react-refresh, globals, @hugeicons/core-free-icons, @hugeicons/react (+14 more)

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
Cohesion: 0.14
Nodes (14): KnowledgeChunk, _Claim, IndexAttemptLostError, KnowledgeError, KnowledgeService, FakeEmbedder, test_category_filters_include_general_policies_and_validate_tags(), test_claim_locks_source_even_before_index_row_exists() (+6 more)

### Community 26 - "compilerOptions"
Cohesion: 0.09
Nodes (21): compilerOptions, allowArbitraryExtensions, allowImportingTsExtensions, erasableSyntaxOnly, jsx, lib, module, moduleDetection (+13 more)

### Community 27 - "web/src/components/theme-provider.tsx"
Cohesion: 0.15
Nodes (14): App(), disableTransitionsTemporarily(), getSystemTheme(), isEditableTarget(), isTheme(), ResolvedTheme, Theme, THEME_VALUES (+6 more)

### Community 28 - "test_embeddings.py"
Cohesion: 0.08
Nodes (40): EmbeddingError, _nonnegative_number(), OpenRouterEmbedder, _ordered_vectors(), _response_cost(), _percentile(), Embeddings, embedder_for() (+32 more)

### Community 29 - "Classify and Extract Prompts"
Cohesion: 0.31
Nodes (9): extract, gemini_classify, Pipeline Graph Orchestration, jev_classify, prepare, Gemini Classify Prompt v1, Gemini Extract Prompt v1, GeminiClassifier (+1 more)

### Community 30 - "FakeJevRunnable"
Cohesion: 0.08
Nodes (29): CredentialCheck, CredentialChecker, DegradedCredentialChecker, _finite_nonnegative(), _get(), JevCredentialChecker, FakeJevRunnable, ResponseRunnable (+21 more)

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
Nodes (26): GatedEmbedder, LateEmbedder, PaidEmbedder, count_chunks(), test_competing_callers_refuse_active_attempt_and_release_transactions(), test_cosine_ranking_cutoff_and_duplicate_stable_ids(), test_db_deadline_cancelled_publication_cannot_commit_late(), test_db_deadline_includes_pool_and_checkout_without_late_claim() (+18 more)

### Community 36 - "web/components.json"
Cohesion: 0.10
Nodes (19): aliases, components, hooks, lib, ui, utils, iconLibrary, menuAccent (+11 more)

### Community 38 - "repository.py"
Cohesion: 0.18
Nodes (18): _run_with_db(), create_run(), finish_run(), load_incidents(), load_transactions(), save_outcomes(), _to_record(), _upsert() (+10 more)

### Community 39 - "ui/components.json"
Cohesion: 0.10
Nodes (19): aliases, components, hooks, lib, ui, utils, iconLibrary, menuAccent (+11 more)

### Community 40 - "TicketResultRow"
Cohesion: 0.20
Nodes (14): _safe_dispatch(), RunRow, TicketResultRow, recover(), run_job(), fail_intake_placeholders(), reconcile_intake_run(), recover_intake_processing() (+6 more)

### Community 41 - "test_draft_tools.py"
Cohesion: 0.11
Nodes (30): api(), ErrorEmbedder, settings(), test_all_eight_tools_and_seven_parallel_calls_execute_only_six(), test_context_copies_input_and_rejects_raising_hard_call_limit(), test_database_faults_remain_distinct_and_record_paid_search_cost(), test_discovered_ref_can_be_inspected_but_not_promoted_to_match(), test_exact_and_fuzzy_queries_are_scoped_and_never_confirm_candidates() (+22 more)

### Community 43 - "Human Review Gate"
Cohesion: 0.25
Nodes (4): support CLI, Support Workspace UI Plan, Review API, Workspace UI Verification

### Community 44 - "compilerOptions"
Cohesion: 0.12
Nodes (16): compilerOptions, allowImportingTsExtensions, erasableSyntaxOnly, lib, module, moduleDetection, noEmit, noFallthroughCasesInSwitch (+8 more)

### Community 46 - "test_extract.py"
Cohesion: 0.33
Nodes (10): FieldPick, finalize(), FakeExtractor, _setup(), test_fill_gaps_noop_and_failure_tolerant(), test_fill_gaps_only_asks_for_weak_required_fields(), test_gemini_span_not_in_text_is_null(), test_gemini_word_amount_uses_normalized_hint() (+2 more)

### Community 47 - "compilerOptions"
Cohesion: 0.12
Nodes (16): compilerOptions, allowImportingTsExtensions, erasableSyntaxOnly, lib, module, moduleDetection, noEmit, noFallthroughCasesInSwitch (+8 more)

### Community 48 - "RAG drafting verification — 2026-10-17"
Cohesion: 0.15
Nodes (15): ingest(), support_test(), Task 3: Ticket-scoped investigation and all eight tools, Task 8: Demo corpus, full verification and readiness record, Artifacts, servers and remaining concerns, Citation IDs and provider evidence, Commands and automated verification — historical Task 8, Corpus and actual retrieval (+7 more)

### Community 57 - "parse_document"
Cohesion: 0.11
Nodes (28): _append_chunks(), _check_extracted_size(), DocumentParseError, parse_document(), _parse_pdf(), make_pdf(), test_arabic_text_and_bom_are_preserved(), test_blank_pdf_tells_operator_to_use_ocr() (+20 more)

### Community 58 - "tools.py"
Cohesion: 0.09
Nodes (10): DraftAlreadySubmitted, DraftSubmission, DraftToolLimit, build_tools(), flag(), guarded(), invoke(), retrieve() (+2 more)

### Community 59 - "agent.py"
Cohesion: 0.09
Nodes (7): _error_cost(), _Execution, _ModelUsage, _number(), DraftContext, _bounded(), visit()

### Community 60 - "SqlInvestigationRepo"
Cohesion: 0.18
Nodes (13): parse_dt(), DraftToolInputError, _datetime(), _days(), _field(), _involves(), _phone(), _phones() (+5 more)

### Community 61 - "NewBatchPage.tsx"
Cohesion: 0.19
Nodes (15): Tabs(), TabsContent(), TabsList(), tabsListVariants, TabsTrigger(), Textarea(), readReport(), exampleTickets (+7 more)

### Community 62 - "rules.py"
Cohesion: 0.20
Nodes (17): Decision, decide(), empty_ticket_decision(), merge_reasons(), note_for(), _unique(), Category, state() (+9 more)

### Community 63 - "cli.py"
Cohesion: 0.08
Nodes (26): _command_settings(), ingest_kb_cmd(), init_db_cmd(), Mode, run_batch_cmd(), _run_in_memory(), seed_db_cmd(), _sessionmaker() (+18 more)

### Community 64 - "tasks"
Cohesion: 0.12
Nodes (16): dependsOn, inputs, outputs, cache, persistent, dependsOn, dependsOn, $schema (+8 more)

### Community 65 - "types.ts"
Cohesion: 0.09
Nodes (35): source, PipelineTrace(), STAGE_NODES, timing(), renderableTrace(), reviewEvidence(), source, save() (+27 more)

### Community 66 - "graph.py"
Cohesion: 0.13
Nodes (10): TicketOutcome, TicketExecution, _default_retry(), outcome_from_state(), _retryable(), outcome_to_dict(), outcome_to_row(), process() (+2 more)

### Community 67 - "intake/contracts.py"
Cohesion: 0.13
Nodes (15): _aware(), Credentials, CustomerReview, IntakeModel, Message, QuestionRecord, SessionView, IntakeService (+7 more)

### Community 68 - "make_ticket"
Cohesion: 0.24
Nodes (24): build_graph(), PipelineDeps, FakeClassifier, make_output(), make_ticket(), pipeline(), test_run_batch_no_db_writes_summary_and_out(), fake_build() (+16 more)

### Community 69 - "_DatabaseCall"
Cohesion: 0.17
Nodes (3): _check_deadline(), _consume(), _DatabaseCall

### Community 72 - "taxonomy.py"
Cohesion: 0.14
Nodes (9): load_taxonomy(), most_urgent(), priority_rank(), TaxonomyError, tax(), taxonomy(), taxonomy(), test_priority_helpers() (+1 more)

### Community 73 - "normalize.py"
Cohesion: 0.22
Nodes (16): detect_arabizi(), fold_arabic(), has_latin_mix(), _latin_words(), mask_cards(), normalize(), sanitize_for_storage(), test_arabizi_detection() (+8 more)

### Community 74 - "use-knowledge-library.ts"
Cohesion: 0.16
Nodes (19): Input(), acceptIndexRequest(), canRequestIndex(), PendingIndexes, persistPendingIndexes(), pollKnowledge(), refresh(), stop() (+11 more)

### Community 75 - "test-kb/README.md"
Cohesion: 0.09
Nodes (11): Fictional RAG walkthrough inputs, توثيق الحساب — سياسة خيالية للعرض التجريبي, نزاع مع وكيل — سياسة خيالية للعرض التجريبي, أعطال التطبيق — سياسة خيالية للعرض التجريبي, دفع الفواتير — سياسة خيالية للعرض التجريبي, مشاكل البطاقة — سياسة خيالية للعرض التجريبي, التحويل المعلّق — سياسة خيالية للعرض التجريبي, الاستفسار الآمن من الدعم — سياسة خيالية للعرض التجريبي (+3 more)

### Community 76 - "ingest.py"
Cohesion: 0.26
Nodes (8): load_jsonl(), load_tickets(), _rows(), test_csv_with_bom_and_missing_columns(), test_duplicate_external_ids_keep_first(), test_json_object_without_ids(), test_jsonl_fixture_loads(), test_unsupported_format()

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
Cohesion: 0.24
Nodes (14): Candidates, ClassificationResult, ClassifierOutput, NormalizedTicket, Classifier, GeminiClassifier, build_order_check(), build_questions() (+6 more)

### Community 94 - "devDependencies"
Cohesion: 0.14
Nodes (14): devDependencies, eslint, @eslint/js, eslint-plugin-react-hooks, eslint-plugin-react-refresh, globals, @tailwindcss/vite, @types/node (+6 more)

### Community 95 - "devDependencies"
Cohesion: 0.14
Nodes (14): devDependencies, eslint, @eslint/js, eslint-plugin-react-hooks, eslint-plugin-react-refresh, globals, tailwindcss, @tailwindcss/vite (+6 more)

### Community 96 - "rag_fakes.py"
Cohesion: 0.17
Nodes (12): make_draft_model(), RagDrafter, Checker, response_payload(), run_provider_pipeline(), send(), search_response(), test_empty_choices_escalates_and_keeps_paid_response_usage() (+4 more)

### Community 97 - "Plan 3 — Knowledge retrieval and grounded reply drafting"
Cohesion: 0.07
Nodes (26): DraftResult, Drafter, NullDrafter, UnavailableDrafter, draft(), draft(), draft(), 10. Remaining demo roadmap (+18 more)

### Community 98 - "Plan 3 RAG Drafting Implementation Plan"
Cohesion: 0.22
Nodes (9): Completion and review record — 2026-10-17, Execution handoff, File map and shared interfaces, Global Constraints, Plan 3 RAG Drafting Implementation Plan, Plan self-review, Review Focus, Task 6: API/CLI indexing and persisted citation projection (+1 more)

### Community 99 - "compilerOptions"
Cohesion: 0.14
Nodes (13): compilerOptions, jsx, lib, module, moduleResolution, noEmit, paths, skipLibCheck (+5 more)

### Community 100 - "قواعد المعرفة العربية للعرض أمام لجنة التحكيم"
Cohesion: 0.33
Nodes (6): الأصل ونتيجة التحقق, توليد مسودة ومراجعتها, خريطة الملفات وأسئلة العرض, خطوات الرفع والفهرسة والبحث أمام اللجنة, قواعد المعرفة العربية للعرض أمام لجنة التحكيم, ماذا أرفع؟

### Community 101 - "pydantic"
Cohesion: 0.21
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

### Community 107 - "test_gemini.py"
Cohesion: 0.31
Nodes (12): ExtractedSpan, _Fields, GeminiFields, _a(), _classify(), test_all_samples_failing_raises(), test_extractor_requests_only_named_fields(), test_failed_samples_count_against_confidence() (+4 more)

### Community 108 - "test_workspace_api.py"
Cohesion: 0.23
Nodes (7): start_run(), test_batch_and_queue_expose_real_results(), test_batch_failure_is_isolated_and_conflicting_ids_rejected(), test_openrouter_credentials_enable_api_modes_without_exposing_keys(), test_progress_counts_only_durable_results_after_save_failure(), fail_one_save(), test_review_requires_text_and_rejects_stale_updates()

### Community 109 - "ZainCash Support Workspace"
Cohesion: 0.25
Nodes (8): Current capability boundaries, Data source, Modular file map, Open the right project, Run locally, shadcn conventions, Workflow, ZainCash Support Workspace

### Community 111 - "scripts"
Cohesion: 0.25
Nodes (8): scripts, build, dev, format, lint, preview, test, typecheck

### Community 112 - "scripts"
Cohesion: 0.29
Nodes (7): scripts, build, dev, format, lint, preview, typecheck

### Community 113 - "compilerOptions"
Cohesion: 0.29
Nodes (6): compilerOptions, module, moduleResolution, skipLibCheck, strict, target

### Community 114 - "test_llm.py"
Cohesion: 0.14
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
Cohesion: 0.13
Nodes (9): Settings, test_blank_intake_model_is_rejected(), test_non_positive_image_limit_is_rejected(), test_defaults(), test_drafting_configuration_cannot_bypass_hard_limits(), test_drafting_limits_load_from_environment(), test_env_overrides(), test_legacy_gemini_model_names_are_qualified_for_openrouter() (+1 more)

### Community 120 - "scripts"
Cohesion: 0.50
Nodes (4): scripts, format, lint, typecheck

### Community 121 - "shadcn/ui monorepo template"
Cohesion: 0.50
Nodes (3): Adding components, shadcn/ui monorepo template, Using components

### Community 122 - "evidence.py"
Cohesion: 0.11
Nodes (47): Analysis, EvidenceRef, Fact, Question, Readiness, _apply(), _check_reference(), _compact() (+39 more)

### Community 124 - "attachments.py"
Cohesion: 0.11
Nodes (26): AttachmentStore, _display_name(), Attachment, ImageInput, IntakeAttachmentRow, ImageRejected, IntakeError, NotOwned (+18 more)

### Community 125 - "extract.py"
Cohesion: 0.16
Nodes (10): resolve_date(), _safe_date(), FieldExtractor, _field(), fill_gaps(), _is_weak(), _iso(), normalize_value() (+2 more)

### Community 126 - "IntakeState"
Cohesion: 0.10
Nodes (18): IntakeState, ReviewText, TurnContext, InvalidEvidence, IntakeGraph, _invitation(), build_review(), _compact() (+10 more)

### Community 127 - "build_pipeline"
Cohesion: 0.12
Nodes (21): SqlTransactionRepo, build_pipeline(), ConfigError, make_jev_client(), run_batch(), GeminiAnalysis, FakeStructuredLLM, ScriptedChat (+13 more)

### Community 129 - "intake/model.py"
Cohesion: 0.12
Nodes (20): ModelCall, ModelUnavailable, _analysis_prompt(), _bounded_context(), _guard_size(), ModelBudget, OpenRouterIntakeModel, _record() (+12 more)

### Community 130 - "Customer Conversation Intake Implementation Plan"
Cohesion: 0.25
Nodes (7): Customer Conversation Intake Implementation Plan, Execution conventions and repository baseline, File map and dependency order, Global Constraints, Plan review and execution handoff, Review Focus, Spec coverage and acceptance map

### Community 131 - "intake.py"
Cohesion: 0.15
Nodes (19): create_session(), _credentials(), _dump(), get_session(), post_message(), read_attachment(), remove_attachment(), request_review() (+11 more)

### Community 132 - "test_final_fix_handoff.py"
Cohesion: 0.11
Nodes (22): Passage, process_batch(), Knowledge, assert_completed_evidence(), faulty_knowledge(), read(), outer_deadlines(), PaidEmbeddings (+14 more)

### Community 133 - "Synthetic demo readiness"
Cohesion: 0.50
Nodes (4): Evidence by layer, Known limitations and remaining work, Repeatable local walkthrough, Synthetic demo readiness

### Community 134 - "kb/service.py"
Cohesion: 0.13
Nodes (8): Embedder, EmbeddingBatch, SearchResult, TextChunk, _abandoned(), _error_cost(), KnowledgeExecutionError, Task 1: Testable parsing and embedding boundary

### Community 135 - "factory.py"
Cohesion: 0.16
Nodes (5): Sample, StructuredLLM, GeminiExtractor, verified_pick(), render_prompt()

### Community 137 - "tools.py"
Cohesion: 0.24
Nodes (8): _Flag, _History, _Input, _Knowledge, _Lookup, _Recent, _Search, _Service

### Community 138 - "canonical_digits"
Cohesion: 0.33
Nodes (5): canonical_digits(), normalize_reported_date(), test_ambiguous_slash_date_is_not_fabricated(), test_utc_instant_just_before_baghdad_midnight_stays_on_the_previous_day(), test_yesterday_is_anchored_to_message_in_baghdad()

### Community 139 - "test_submission.py"
Cohesion: 0.32
Nodes (4): _payload(), test_concurrent_submit_dispatches_once(), test_second_request_id_reuses_the_approved_review(), test_submission_replay_creates_one_ticket()

### Community 140 - "test_dbapi_commit_handoff_arbitrates_cancellation"
Cohesion: 0.47
Nodes (4): test_dbapi_commit_handoff_arbitrates_cancellation(), gate(), gate_before_dbapi(), gate_inside_dbapi()

### Community 141 - "index_deadlines"
Cohesion: 0.40
Nodes (3): index_deadlines(), settings(), expire_during_embedding()

## Ambiguous Edges - Review These
- `Fraud Report` → `Plan 1 Live Smoke`  [AMBIGUOUS]
  README.md · relation: conceptually_related_to

## Knowledge Gaps
- **86 isolated node(s):** `zaincash-support`, `@base-ui/react`, `@fontsource-variable/geist`, `@tailwindcss/vite`, `class-variance-authority` (+81 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 911 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **40 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Settings` connect `Settings` to `intake/model.py`, `test_rag_drafter.py`, `intake/repository.py`, `test_final_fix_handoff.py`, `TicketRow`, `kb/service.py`, `factory.py`, `main.py`, `Synthetic demo readiness`, `test_rag_api.py`, `index_deadlines`, `test_cli.py`, `KnowledgeService`, `test_embeddings.py`, `FakeJevRunnable`, `test_kb_service.py`, `repository.py`, `test_draft_tools.py`, `RAG drafting verification — 2026-10-17`, `agent.py`, `cli.py`, `taxonomy.py`, `rag_fakes.py`, `test_workspace_api.py`, `test_llm.py`, `evidence.py`, `attachments.py`, `build_pipeline`?**
  _High betweenness centrality (0.113) - this node is a cross-community bridge._
- **Are the 33 inferred relationships involving `Settings` (e.g. with `_command_settings()` and `_run_in_memory()`) actually correct?**
  _`Settings` has 33 INFERRED edges - model-reasoned connections that need verification._
- **What connects `zaincash-support`, `@base-ui/react`, `@fontsource-variable/geist` to the rest of the system?**
  _86 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `guardrails.py` be split into smaller, more focused modules?**
  _Cohesion score 0.1361344537815126 - nodes in this community are weakly interconnected._
- **Why does `Task 3: Validated attachments and bounded multimodal interpretation` connect `intake/model.py` to `evidence.py`, `intake/contracts.py`, `IntakeState`, `test_llm.py`?**
  _High betweenness centrality (0.072) - this node is a cross-community bridge._
- **Are the 24 inferred relationships involving `KnowledgeService` (e.g. with `Settings` and `UploadedDocument`) actually correct?**
  _`KnowledgeService` has 24 INFERRED edges - model-reasoned connections that need verification._

### Low-confidence Hints
_AMBIGUOUS edges — the extractor was unsure. Verify before acting on these._

- **What is the exact relationship between `Fraud Report` and `Plan 1 Live Smoke`?**
  _Edge tagged AMBIGUOUS (relation: conceptually_related_to) - confidence is low._