# Graph Report - zaincash-support  (2026-10-18)

## Corpus Check
- 222 files · ~199,139 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 24 file(s) not represented in the graph (top: (none) 15, .jsonl 4, .css 3)

## Summary
- 2266 nodes · 6351 edges · 131 communities (92 shown, 39 thin omitted)
- Extraction: 90% EXTRACTED · 10% INFERRED · 0% AMBIGUOUS · INFERRED: 630 edges (avg confidence: 0.92)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `b7ba9cf9`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- pipeline/contracts.py
- guardrails.py
- pytest
- test_llm.py
- TicketReviewPage.tsx
- db/models.py
- QueuePage.tsx
- Customer conversation intake for ZainCash support
- workspace-ui.tsx
- graph.py
- test_lookup.py
- test_rag_api.py
- employee-frontend/package.json
- test_draft_guardrails.py
- Support Taxonomy Categories
- ui/package.json
- employee-frontend/src/App.tsx
- users-frontend/package.json
- test_workspace_api.py
- UploadedDocument
- web/package.json
- Pipeline Graph Nodes
- compilerOptions
- employee-frontend/components.json
- test_final_fix_handoff.py
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
- service.py
- test_draft_tools.py
- Human Review Gate
- compilerOptions
- KnowledgeService
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
- DraftContext
- SqlInvestigationRepo
- NewBatchPage.tsx
- rules.py
- cli.py
- tasks
- fakes.py
- asyncio
- HTTP contract (implemented in Tasks 4–5)
- make_ticket
- _DatabaseCall
- tools.py
- model.py
- taxonomy.py
- .index_document
- types.ts
- test-kb/README.md
- ingest.py
- PaidEmbedder
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
- ScriptedChat
- devDependencies
- devDependencies
- test_draft_model.py
- KnowledgeError
- Plan 3 RAG Drafting Implementation Plan
- compilerOptions
- قواعد المعرفة العربية للعرض أمام لجنة التحكيم
- pydantic
- dependencies
- employee-frontend/src/components/theme-provider.tsx
- dependencies
- compilerOptions
- ar/general_inquiry.md
- ar/login_access.md
- test_db_deadline_cancelled_publication_cannot_commit_late
- ZainCash Support Workspace
- negative/README.md
- scripts
- scripts
- compilerOptions
- IncidentRow
- dependencies
- web/tsconfig.json
- employee-frontend/tsconfig.json
- exports
- Settings
- scripts
- shadcn/ui monorepo template
- ar/app_bug.md
- ar/fraud_report.md
- ar/refund_request.md
- ar/wrong_recipient.md
- test_dbapi_commit_handoff_arbitrates_cancellation
- ar/bill_payment.md
- ar/failed_transfer.md
- ar/other.md
- .inspect-users-frontend.sh

## God Nodes (most connected - your core abstractions)
1. `KnowledgeService` - 79 edges
2. `Settings` - 70 edges
3. `PipelineState` - 50 edges
4. `make_ticket()` - 44 edges
5. `draft_state()` - 44 edges
6. `build_pipeline()` - 43 edges
7. `make_output()` - 42 edges
8. `EmbeddingError` - 35 edges
9. `script()` - 35 edges
10. `UploadedDocument` - 33 edges

## Surprising Connections (you probably didn't know these)
- `الأصل ونتيجة التحقق` --references--> `parse_document()`  [INFERRED]
  data/test-kb/README.md → backend/app/kb/parse.py
- `Task 6: API/CLI indexing and persisted citation projection` --references--> `KnowledgeService`  [INFERRED]
  docs/superpowers/plans/2026-10-17-plan3-rag-drafting.md → backend/app/kb/service.py
- `Pipeline and CLI` --references--> `NullDrafter`  [INFERRED]
  docs/superpowers/specs/2026-10-17-plan3-rag-drafting-design.md → backend/app/pipeline/stage6_draft/drafting.py
- `Evidence by layer` --references--> `support_test()`  [INFERRED]
  docs/demo-readiness.md → backend/tests/test_kb_service.py
- `Task 8: Demo corpus, full verification and readiness record` --references--> `support_test()`  [INFERRED]
  docs/superpowers/plans/2026-10-17-plan3-rag-drafting.md → backend/tests/test_kb_service.py

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **Cascade Classification Path** — docs_superpowers_specs_2026_10_07_support_pipeline_design_cascade, docs_superpowers_plans_2026_10_07_plan1_core_pipeline_part2_jev_classifier, docs_superpowers_plans_2026_10_07_plan1_core_pipeline_part2_gemini_classifier, docs_superpowers_plans_2026_10_07_plan1_core_pipeline_part2_cascade_combine, readme_human_approval [EXTRACTED 1.00]
- **Drafting Agent Toolset** — backend_app_pipeline_runner_lookup_transaction, backend_app_pipeline_runner_search_transactions, backend_app_pipeline_runner_get_customer_recent_transactions, backend_app_pipeline_runner_get_customer_ticket_history, backend_app_pipeline_runner_check_service_status, backend_app_pipeline_runner_search_knowledge_base, backend_app_pipeline_runner_flag_for_human, backend_app_pipeline_runner_submit_draft [EXTRACTED 1.00]
- **Ticket Processing Stage Flow** — backend_app_pipeline_runner_prepare, backend_app_pipeline_runner_jev_classify, backend_app_pipeline_runner_gemini_classify, backend_app_pipeline_runner_extract, backend_app_pipeline_runner_lookup, backend_app_pipeline_runner_decide, backend_app_pipeline_runner_draft [EXTRACTED 1.00]

## Communities (131 total, 39 thin omitted)

### Community 0 - "pipeline/contracts.py"
Cohesion: 0.13
Nodes (20): StructuredLLM, Candidates, ClassificationResult, ClassifierOutput, NormalizedTicket, Classifier, FieldExtractor, GeminiClassifier (+12 more)

### Community 1 - "guardrails.py"
Cohesion: 0.05
Nodes (57): TicketInput, Candidate, _add(), find_candidates(), normalize_phone(), _overlaps(), parse_amount(), resolve_date() (+49 more)

### Community 2 - "pytest"
Cohesion: 0.23
Nodes (33): answer(), call(), draft_state(), script(), submit(), drafter(), events(), test_callback_partial_response_and_error_cost_are_alternatives() (+25 more)

### Community 3 - "test_llm.py"
Cohesion: 0.14
Nodes (11): GeminiStructuredLLM, make_gemini_llm(), _llm(), _S, test_draft_model_uses_millisecond_timeout_and_disables_sdk_retries(), test_openrouter_reported_cost_takes_precedence_over_token_estimate(), test_openrouter_retry_budget_is_bounded(), test_openrouter_structured_samples_use_configured_key_and_validate_output() (+3 more)

### Community 4 - "TicketReviewPage.tsx"
Cohesion: 0.13
Nodes (29): Confidence(), Metric(), Badge(), badgeVariants, Card(), CardContent(), CardHeader(), CardTitle() (+21 more)

### Community 5 - "db/models.py"
Cohesion: 0.11
Nodes (20): get_session(), get_result(), list_results(), review_result(), get_run(), list_runs(), start_run(), BatchInput (+12 more)

### Community 6 - "QueuePage.tsx"
Cohesion: 0.23
Nodes (30): EmptyState(), ErrorState(), LoadingState(), PageHeader(), PriorityBadge(), StatusBadge(), Table(), TableBody() (+22 more)

### Community 7 - "Customer conversation intake for ZainCash support"
Cohesion: 0.06
Nodes (31): 10. Verification and acceptance criteria, 11. Delivery and review, 1. Outcome and agreed requirements, 2. Current implementation and integration points, 3. Approach and boundaries, 4. Conversation state and turn flow, 5. Facts, evidence, and readiness, 6. Language and screenshot behavior (+23 more)

### Community 8 - "workspace-ui.tsx"
Cohesion: 0.16
Nodes (20): PipelineStrip(), ConfirmDialog(), FilterSelect(), statusLabels, Button(), Dialog(), DialogContent(), DialogDescription() (+12 more)

### Community 9 - "graph.py"
Cohesion: 0.08
Nodes (14): DraftResult, _default_retry(), _retryable(), _as_date(), _iqd_amount(), match_transaction(), TransactionRepo, Drafter (+6 more)

### Community 10 - "test_lookup.py"
Cohesion: 0.35
Nodes (10): _ex(), _match(), test_ambiguous_then_disambiguated_by_counterpart(), test_amount_and_date_mismatch(), test_no_phone_is_not_found(), test_not_applicable_category(), test_ref_matched(), test_ref_not_found() (+2 more)

### Community 11 - "test_rag_api.py"
Cohesion: 0.15
Nodes (17): client(), evidence_client(), test_actual_guardrail_failure_is_separate_from_reply(), test_concurrent_index_requests_share_active_work(), test_disabled_or_missing_provider_stores_without_indexing(), test_explicit_retry_tags_search_and_chunk_pagination(), test_health_distinguishes_failed_from_empty(), test_health_requires_compatible_nonempty_index() (+9 more)

### Community 12 - "employee-frontend/package.json"
Cohesion: 0.07
Nodes (28): @base-ui/react, class-variance-authority, cn, eslint, @eslint/js, eslint-plugin-react-hooks, eslint-plugin-react-refresh, globals (+20 more)

### Community 14 - "test_draft_guardrails.py"
Cohesion: 0.07
Nodes (46): requests_credentials(), check(), state(), test_aggregation_is_deduplicated_and_has_no_state_side_effects(), test_amount_occurrences_keep_their_own_currency_and_sign(), test_avoid_sharing_warning_does_not_excuse_a_later_request(), test_candidate_prompt_limit_does_not_hide_later_ungrounded_references(), test_candidate_transactions_cannot_authorize_reply_evidence() (+38 more)

### Community 15 - "Support Taxonomy Categories"
Cohesion: 0.21
Nodes (22): lookup, Account KYC, Account & Security, Agent Dispute, Agent Network, App Bug, Bill Payment, Card Issue (+14 more)

### Community 16 - "ui/package.json"
Cohesion: 0.07
Nodes (28): @fontsource-variable/figtree, @turbo/gen, zod, @base-ui/react, class-variance-authority, cn, eslint, @eslint/js (+20 more)

### Community 17 - "employee-frontend/src/App.tsx"
Cohesion: 0.14
Nodes (20): App(), EvaluationPage, InsightsPage, KnowledgePage, NewBatchPage, QueuePage, RunDetailPage, RunsPage (+12 more)

### Community 18 - "users-frontend/package.json"
Cohesion: 0.09
Nodes (22): turbo, devDependencies, prettier, prettier-plugin-tailwindcss, turbo, typescript, engines, node (+14 more)

### Community 19 - "test_workspace_api.py"
Cohesion: 0.07
Nodes (19): Base, init_db(), make_engine(), make_sessionmaker(), reset_db(), upgrade_workspace_schema(), create_app(), lifespan() (+11 more)

### Community 20 - "UploadedDocument"
Cohesion: 0.14
Nodes (13): delete_document(), download_document(), index_document(), list_chunks(), list_documents(), _require_provider(), search_knowledge(), upload_document() (+5 more)

### Community 21 - "web/package.json"
Cohesion: 0.09
Nodes (22): @workspace/ui, eslint, @eslint/js, eslint-plugin-react-hooks, eslint-plugin-react-refresh, globals, @hugeicons/core-free-icons, @hugeicons/react (+14 more)

### Community 23 - "compilerOptions"
Cohesion: 0.09
Nodes (22): compilerOptions, allowArbitraryExtensions, allowImportingTsExtensions, erasableSyntaxOnly, jsx, lib, module, moduleDetection (+14 more)

### Community 24 - "employee-frontend/components.json"
Cohesion: 0.09
Nodes (21): aliases, components, hooks, lib, ui, utils, iconLibrary, menuAccent (+13 more)

### Community 25 - "test_final_fix_handoff.py"
Cohesion: 0.09
Nodes (24): Passage, SearchResult, Checker, Knowledge, assert_completed_evidence(), faulty_knowledge(), read(), outer_deadlines() (+16 more)

### Community 26 - "compilerOptions"
Cohesion: 0.09
Nodes (21): compilerOptions, allowArbitraryExtensions, allowImportingTsExtensions, erasableSyntaxOnly, jsx, lib, module, moduleDetection (+13 more)

### Community 27 - "web/src/components/theme-provider.tsx"
Cohesion: 0.14
Nodes (14): App(), disableTransitionsTemporarily(), getSystemTheme(), isEditableTarget(), isTheme(), ResolvedTheme, Theme, THEME_VALUES (+6 more)

### Community 28 - "test_embeddings.py"
Cohesion: 0.08
Nodes (43): Embedder, EmbeddingBatch, EmbeddingError, _nonnegative_number(), OpenRouterEmbedder, _ordered_vectors(), _response_cost(), Embeddings (+35 more)

### Community 29 - "Classify and Extract Prompts"
Cohesion: 0.31
Nodes (9): extract, gemini_classify, Pipeline Graph Orchestration, jev_classify, prepare, Gemini Classify Prompt v1, Gemini Extract Prompt v1, GeminiClassifier (+1 more)

### Community 30 - "FakeJevRunnable"
Cohesion: 0.05
Nodes (51): _run_with_db(), SqlTransactionRepo, Sample, build_pipeline(), ConfigError, make_jev_client(), model_ids(), run_batch() (+43 more)

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
Cohesion: 0.14
Nodes (24): IndexAttemptLostError, FakeEmbedder, count_chunks(), index_deadlines(), settings(), test_category_filters_include_general_policies_and_validate_tags(), test_claim_locks_source_even_before_index_row_exists(), test_cosine_ranking_cutoff_and_duplicate_stable_ids() (+16 more)

### Community 36 - "web/components.json"
Cohesion: 0.10
Nodes (19): aliases, components, hooks, lib, ui, utils, iconLibrary, menuAccent (+11 more)

### Community 38 - "repository.py"
Cohesion: 0.18
Nodes (17): RunRow, create_run(), finish_run(), load_incidents(), load_transactions(), _to_record(), _upsert(), upsert_tickets() (+9 more)

### Community 39 - "ui/components.json"
Cohesion: 0.10
Nodes (19): aliases, components, hooks, lib, ui, utils, iconLibrary, menuAccent (+11 more)

### Community 40 - "service.py"
Cohesion: 0.14
Nodes (12): UploadedDocument, document_view(), DocumentValidationError, store_document(), KnowledgeDocumentIndex, ingest_one(), ingest_paths(), ingest_status() (+4 more)

### Community 41 - "test_draft_tools.py"
Cohesion: 0.15
Nodes (24): TransactionRow, ErrorEmbedder, test_all_eight_tools_and_seven_parallel_calls_execute_only_six(), test_context_copies_input_and_rejects_raising_hard_call_limit(), test_database_faults_remain_distinct_and_record_paid_search_cost(), test_discovered_ref_can_be_inspected_but_not_promoted_to_match(), test_exact_and_fuzzy_queries_are_scoped_and_never_confirm_candidates(), test_exact_reference_still_requires_customer_and_excludes_future() (+16 more)

### Community 43 - "Human Review Gate"
Cohesion: 0.25
Nodes (4): support CLI, Support Workspace UI Plan, Review API, Workspace UI Verification

### Community 44 - "compilerOptions"
Cohesion: 0.12
Nodes (16): compilerOptions, allowImportingTsExtensions, erasableSyntaxOnly, lib, module, moduleDetection, noEmit, noFallthroughCasesInSwitch (+8 more)

### Community 46 - "KnowledgeService"
Cohesion: 0.18
Nodes (4): KnowledgeChunk, _Claim, KnowledgeService, test_search_database_failure_preserves_completed_query_cost()

### Community 47 - "compilerOptions"
Cohesion: 0.12
Nodes (16): compilerOptions, allowImportingTsExtensions, erasableSyntaxOnly, lib, module, moduleDetection, noEmit, noFallthroughCasesInSwitch (+8 more)

### Community 48 - "RAG drafting verification — 2026-10-17"
Cohesion: 0.22
Nodes (11): ingest(), support_test(), Task 1: Durable intake sessions and ownership, Artifacts, servers and remaining concerns, Commands and automated verification — historical Task 8, Corpus and actual retrieval, Current final verification and review closure, Environment and isolation (+3 more)

### Community 57 - "parse_document"
Cohesion: 0.10
Nodes (30): TextChunk, _append_chunks(), _check_extracted_size(), DocumentParseError, parse_document(), _parse_pdf(), make_pdf(), test_arabic_text_and_bom_are_preserved() (+22 more)

### Community 58 - "tools.py"
Cohesion: 0.15
Nodes (12): _bounded(), visit(), retrieve(), _error_cost(), _Flag, _History, _Input, _Knowledge (+4 more)

### Community 59 - "DraftContext"
Cohesion: 0.09
Nodes (7): _error_cost(), _Execution, _ModelUsage, _number(), RagDrafter, DraftContext, DraftExecutionError

### Community 60 - "SqlInvestigationRepo"
Cohesion: 0.18
Nodes (14): TxnRecord, parse_dt(), DraftToolInputError, _datetime(), _days(), _field(), _involves(), _phone() (+6 more)

### Community 61 - "NewBatchPage.tsx"
Cohesion: 0.12
Nodes (15): buttonVariants, Tabs(), TabsContent(), TabsList(), tabsListVariants, TabsTrigger(), Textarea(), exampleTickets (+7 more)

### Community 62 - "rules.py"
Cohesion: 0.17
Nodes (20): Decision, ExtractedField, LookupResult, Ticket, decide(), empty_ticket_decision(), merge_reasons(), note_for() (+12 more)

### Community 63 - "cli.py"
Cohesion: 0.14
Nodes (12): _command_settings(), ingest_kb_cmd(), init_db_cmd(), Mode, run_batch_cmd(), _run_in_memory(), seed_db_cmd(), _sessionmaker() (+4 more)

### Community 64 - "tasks"
Cohesion: 0.12
Nodes (16): dependsOn, inputs, outputs, cache, persistent, dependsOn, dependsOn, $schema (+8 more)

### Community 65 - "fakes.py"
Cohesion: 0.13
Nodes (24): LLMUnavailable, FieldPick, combine(), merge_picks(), _field(), fill_gaps(), finalize(), _is_weak() (+16 more)

### Community 66 - "asyncio"
Cohesion: 0.18
Nodes (14): save_outcomes(), TicketOutcome, TicketExecution, outcome_from_state(), _percentile(), summarize(), outcome_to_dict(), outcome_to_row() (+6 more)

### Community 67 - "HTTP contract (implemented in Tasks 4–5)"
Cohesion: 0.11
Nodes (18): fail(), Customer Conversation Intake Implementation Plan, Execution conventions and repository baseline, File map and dependency order, Global Constraints, HTTP contract (implemented in Tasks 4–5), Plan review and execution handoff, Review Focus (+10 more)

### Community 68 - "make_ticket"
Cohesion: 0.25
Nodes (23): build_graph(), PipelineDeps, FakeClassifier, make_output(), make_ticket(), test_run_batch_no_db_writes_summary_and_out(), fake_build(), _deps() (+15 more)

### Community 69 - "_DatabaseCall"
Cohesion: 0.16
Nodes (3): _consume(), _DatabaseCall, Task 6: Customer API client and resumable UI state

### Community 70 - "tools.py"
Cohesion: 0.08
Nodes (10): DraftAlreadySubmitted, DraftSubmission, DraftToolLimit, build_tools(), flag(), guarded(), invoke(), _json() (+2 more)

### Community 72 - "taxonomy.py"
Cohesion: 0.09
Nodes (17): load_taxonomy(), most_urgent(), priority_rank(), TaxonomyError, tax(), test_config_error_exits_2(), boom(), test_ingest_directory_is_deterministic_and_duplicate_is_free() (+9 more)

### Community 73 - ".index_document"
Cohesion: 0.15
Nodes (8): _abandoned(), _check_deadline(), _error_cost(), test_db_deadline_includes_pool_and_checkout_without_late_claim(), checked_in(), test_db_deadline_search_cancellation_is_nonblocking_and_retains_cost(), test_db_deadline_second_cancel_during_failure_bookkeeping_keeps_cost(), test_deletion_during_embedding_never_resurrects_source()

### Community 74 - "types.ts"
Cohesion: 0.10
Nodes (36): Input(), acceptIndexRequest(), canRequestIndex(), PendingIndexes, persistPendingIndexes(), pollKnowledge(), refresh(), stop() (+28 more)

### Community 75 - "test-kb/README.md"
Cohesion: 0.18
Nodes (5): Fictional RAG walkthrough inputs, توثيق الحساب — سياسة خيالية للعرض التجريبي, نزاع مع وكيل — سياسة خيالية للعرض التجريبي, مشاكل البطاقة — سياسة خيالية للعرض التجريبي, الاستفسار المؤقت للدعم في المهمة ٨ — سياسة خيالية للعرض التجريبي

### Community 76 - "ingest.py"
Cohesion: 0.26
Nodes (8): load_jsonl(), load_tickets(), _rows(), test_csv_with_bom_and_missing_columns(), test_duplicate_external_ids_keep_first(), test_json_object_without_ids(), test_jsonl_fixture_loads(), test_unsupported_format()

### Community 77 - "PaidEmbedder"
Cohesion: 0.19
Nodes (5): GatedEmbedder, LateEmbedder, PaidEmbedder, test_competing_callers_refuse_active_attempt_and_release_transactions(), test_failed_reindex_keeps_previous_chunks_atomically_and_is_retryable()

### Community 79 - "devDependencies"
Cohesion: 0.12
Nodes (16): devDependencies, eslint, @eslint/js, eslint-plugin-react-hooks, eslint-plugin-react-refresh, globals, prettier, prettier-plugin-tailwindcss (+8 more)

### Community 80 - "judge-demo.ar.md"
Cohesion: 0.14
Nodes (13): أعطال التطبيق — سياسة خيالية للعرض التجريبي, استرجاع مبلغ شراء — سياسة خيالية للعرض التجريبي, استعادة الدخول — سياسة خيالية للعرض التجريبي, الاستفسار الآمن من الدعم — سياسة خيالية للعرض التجريبي, الاستفسار المؤقت للدعم في المهمة ٨ — سياسة خيالية للعرض التجريبي, التحويل المعلّق — سياسة خيالية للعرض التجريبي, التحويل لمستلم بالخطأ — سياسة خيالية للعرض التجريبي, الطلبات غير الواضحة وخارج النطاق — سياسة خيالية للعرض التجريبي (+5 more)

### Community 93 - "ScriptedChat"
Cohesion: 0.25
Nodes (3): ScriptedChat, pipeline(), submit()

### Community 94 - "devDependencies"
Cohesion: 0.14
Nodes (14): devDependencies, eslint, @eslint/js, eslint-plugin-react-hooks, eslint-plugin-react-refresh, globals, @tailwindcss/vite, @types/node (+6 more)

### Community 95 - "devDependencies"
Cohesion: 0.14
Nodes (14): devDependencies, eslint, @eslint/js, eslint-plugin-react-hooks, eslint-plugin-react-refresh, globals, tailwindcss, @tailwindcss/vite (+6 more)

### Community 96 - "test_draft_model.py"
Cohesion: 0.19
Nodes (9): make_draft_model(), InMemoryTransactionRepo, response_payload(), run_provider_pipeline(), send(), search_response(), test_empty_choices_escalates_and_keeps_paid_response_usage(), test_failed_response_id_is_deduplicated_against_earlier_success() (+1 more)

### Community 97 - "KnowledgeError"
Cohesion: 0.15
Nodes (4): DocumentNotFoundError, KnowledgeError, KnowledgeExecutionError, test_pdf_page_metadata_and_repeated_text_chunk_identity()

### Community 98 - "Plan 3 RAG Drafting Implementation Plan"
Cohesion: 0.18
Nodes (11): Completion and review record — 2026-10-17, Execution handoff, File map and shared interfaces, Global Constraints, Plan 3 RAG Drafting Implementation Plan, Plan self-review, Review Focus, Task 3: Ticket-scoped investigation and all eight tools (+3 more)

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

### Community 108 - "test_db_deadline_cancelled_publication_cannot_commit_late"
Cohesion: 0.29
Nodes (3): test_db_deadline_cancelled_publication_cannot_commit_late(), test_db_deadline_is_cumulative_across_publication_statements(), changed_index()

### Community 109 - "ZainCash Support Workspace"
Cohesion: 0.22
Nodes (9): Current capability boundaries, Data source, Modular file map, Open the right project, Run locally, shadcn conventions, Verification, Workflow (+1 more)

### Community 111 - "scripts"
Cohesion: 0.25
Nodes (8): scripts, build, dev, format, lint, preview, test, typecheck

### Community 112 - "scripts"
Cohesion: 0.29
Nodes (7): scripts, build, dev, format, lint, preview, typecheck

### Community 113 - "compilerOptions"
Cohesion: 0.29
Nodes (6): compilerOptions, module, moduleResolution, skipLibCheck, strict, target

### Community 114 - "IncidentRow"
Cohesion: 0.47
Nodes (4): IncidentRow, test_incident_windows_are_inclusive_bounded_and_read_only(), observe(), test_search_and_incidents_limit_ten_and_all_database_calls_run_off_loop()

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
Nodes (12): Settings, test_defaults(), test_drafting_configuration_cannot_bypass_hard_limits(), test_drafting_limits_load_from_environment(), test_env_overrides(), test_legacy_gemini_model_names_are_qualified_for_openrouter(), test_openrouter_key_is_loaded_from_environment(), test_openrouter_credentials_enable_api_modes_without_exposing_keys() (+4 more)

### Community 120 - "scripts"
Cohesion: 0.50
Nodes (4): scripts, format, lint, typecheck

### Community 121 - "shadcn/ui monorepo template"
Cohesion: 0.50
Nodes (3): Adding components, shadcn/ui monorepo template, Using components

### Community 126 - "test_dbapi_commit_handoff_arbitrates_cancellation"
Cohesion: 0.47
Nodes (4): test_dbapi_commit_handoff_arbitrates_cancellation(), gate(), gate_before_dbapi(), gate_inside_dbapi()

## Ambiguous Edges - Review These
- `Fraud Report` → `Plan 1 Live Smoke`  [AMBIGUOUS]
  README.md · relation: conceptually_related_to

## Knowledge Gaps
- **85 isolated node(s):** `zaincash-support`, `@base-ui/react`, `@fontsource-variable/geist`, `@tailwindcss/vite`, `class-variance-authority` (+80 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 852 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **39 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Artifacts, servers and remaining concerns` connect `RAG drafting verification — 2026-10-17` to `types.ts`, `db/models.py`?**
  _High betweenness centrality (0.096) - this node is a cross-community bridge._
- **Are the 24 inferred relationships involving `KnowledgeService` (e.g. with `Settings` and `UploadedDocument`) actually correct?**
  _`KnowledgeService` has 24 INFERRED edges - model-reasoned connections that need verification._
- **What connects `zaincash-support`, `@base-ui/react`, `@fontsource-variable/geist` to the rest of the system?**
  _85 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `pipeline/contracts.py` be split into smaller, more focused modules?**
  _Cohesion score 0.13205128205128205 - nodes in this community are weakly interconnected._
- **Why does `Task 3: Validated attachments and bounded multimodal interpretation` connect `HTTP contract (implemented in Tasks 4–5)` to `test_llm.py`?**
  _High betweenness centrality (0.096) - this node is a cross-community bridge._
- **Are the 27 inferred relationships involving `Settings` (e.g. with `_command_settings()` and `_run_in_memory()`) actually correct?**
  _`Settings` has 27 INFERRED edges - model-reasoned connections that need verification._

### Low-confidence Hints
_AMBIGUOUS edges — the extractor was unsure. Verify before acting on these._

- **What is the exact relationship between `Fraud Report` and `Plan 1 Live Smoke`?**
  _Edge tagged AMBIGUOUS (relation: conceptually_related_to) - confidence is low._