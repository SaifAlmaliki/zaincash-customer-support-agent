# Graph Report - zaincash-support  (2026-10-18)

## Corpus Check
- 221 files · ~199,048 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 24 file(s) not represented in the graph (top: (none) 15, .jsonl 4, .css 3)

## Summary
- 2264 nodes · 6350 edges · 136 communities (98 shown, 38 thin omitted)
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
- GeminiStructuredLLM
- TicketReviewPage.tsx
- TicketRow
- QueuePage.tsx
- Customer conversation intake for ZainCash support
- workspace-ui.tsx
- PipelineState
- lookup.py
- test_rag_api.py
- employee-frontend/package.json
- test_draft_guardrails.py
- Support Taxonomy Categories
- ui/package.json
- employee-frontend/src/App.tsx
- users-frontend/package.json
- service.py
- UploadedDocument
- web/package.json
- test_cli.py
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
- build_pipeline
- test_draft_tools.py
- Human Review Gate
- compilerOptions
- FieldPick
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
- _ModelUsage
- SqlInvestigationRepo
- NewBatchPage.tsx
- rules.py
- cli.py
- tasks
- LLMUnavailable
- graph.py
- HTTP contract (implemented in Tasks 4–5)
- make_ticket
- _DatabaseCall
- build_tools
- model.py
- taxonomy.py
- normalize.py
- types.ts
- test-kb/README.md
- ingest.py
- EmbeddingBatch
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
- Plan 3 — Knowledge retrieval and grounded reply drafting
- Plan 3 RAG Drafting Implementation Plan
- compilerOptions
- قواعد المعرفة العربية للعرض أمام لجنة التحكيم
- pydantic
- dependencies
- employee-frontend/src/components/theme-provider.tsx
- dependencies
- compilerOptions
- pipeline/contracts.py
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
- ar/app_bug.md
- ar/fraud_report.md
- DraftContext
- resolve_date
- test_dbapi_commit_handoff_arbitrates_cancellation
- ar/bill_payment.md
- ar/other.md
- Customer Conversation Intake Implementation Plan
- DraftToolLimit
- DraftSubmission
- Synthetic demo readiness
- ar/account_kyc.md
- task8-history-policy.md

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

## Communities (136 total, 38 thin omitted)

### Community 0 - "pipeline/contracts.py"
Cohesion: 0.13
Nodes (19): StructuredLLM, Candidates, ClassificationResult, ClassifierOutput, NormalizedTicket, Classifier, GeminiClassifier, GeminiExtractor (+11 more)

### Community 1 - "guardrails.py"
Cohesion: 0.15
Nodes (21): Candidate, _add(), find_candidates(), normalize_phone(), _overlaps(), parse_amount(), to_ascii_digits(), normalize_value() (+13 more)

### Community 2 - "pytest"
Cohesion: 0.21
Nodes (34): answer(), call(), draft_state(), script(), test_context_copies_input_and_rejects_raising_hard_call_limit(), test_submission_is_terminal_including_invalid_later_calls(), submit(), drafter() (+26 more)

### Community 4 - "TicketReviewPage.tsx"
Cohesion: 0.13
Nodes (29): Confidence(), Metric(), Badge(), badgeVariants, Card(), CardContent(), CardHeader(), CardTitle() (+21 more)

### Community 5 - "TicketRow"
Cohesion: 0.12
Nodes (15): get_result(), list_results(), review_result(), KnowledgeIndexInput, KnowledgeSearchInput, ReviewInput, TicketInput, ReviewRow (+7 more)

### Community 6 - "QueuePage.tsx"
Cohesion: 0.23
Nodes (30): EmptyState(), ErrorState(), LoadingState(), PageHeader(), PriorityBadge(), StatusBadge(), Table(), TableBody() (+22 more)

### Community 7 - "Customer conversation intake for ZainCash support"
Cohesion: 0.07
Nodes (28): 10. Verification and acceptance criteria, 11. Delivery and review, 1. Outcome and agreed requirements, 2. Current implementation and integration points, 3. Approach and boundaries, 4. Conversation state and turn flow, 5. Facts, evidence, and readiness, 6. Language and screenshot behavior (+20 more)

### Community 8 - "workspace-ui.tsx"
Cohesion: 0.16
Nodes (20): PipelineStrip(), ConfirmDialog(), FilterSelect(), statusLabels, Button(), Dialog(), DialogContent(), DialogDescription() (+12 more)

### Community 9 - "PipelineState"
Cohesion: 0.12
Nodes (10): DraftResult, _Nodes, Drafter, DraftExecutionError, NullDrafter, UnavailableDrafter, PipelineState, draft() (+2 more)

### Community 10 - "lookup.py"
Cohesion: 0.13
Nodes (16): _as_date(), InMemoryTransactionRepo, _iqd_amount(), match_transaction(), TransactionRepo, txn_from_dict(), _ex(), _match() (+8 more)

### Community 11 - "test_rag_api.py"
Cohesion: 0.08
Nodes (32): init_db(), make_engine(), make_sessionmaker(), reset_db(), KnowledgeDocumentIndex, create_app(), lifespan(), ingest_env() (+24 more)

### Community 12 - "employee-frontend/package.json"
Cohesion: 0.07
Nodes (28): @base-ui/react, class-variance-authority, cn, eslint, @eslint/js, eslint-plugin-react-hooks, eslint-plugin-react-refresh, globals (+20 more)

### Community 14 - "test_draft_guardrails.py"
Cohesion: 0.14
Nodes (27): check_draft(), _citation_findings(), requests_credentials(), check(), test_aggregation_is_deduplicated_and_has_no_state_side_effects(), test_amount_occurrences_keep_their_own_currency_and_sign(), test_avoid_sharing_warning_does_not_excuse_a_later_request(), test_candidate_prompt_limit_does_not_hide_later_ungrounded_references() (+19 more)

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

### Community 19 - "service.py"
Cohesion: 0.07
Nodes (11): health(), insights(), workspace(), Base, upgrade_workspace_schema(), KnowledgeChunk, _abandoned(), _error_cost() (+3 more)

### Community 20 - "UploadedDocument"
Cohesion: 0.12
Nodes (19): delete_document(), download_document(), index_document(), list_chunks(), list_documents(), _require_provider(), search_knowledge(), upload_document() (+11 more)

### Community 21 - "web/package.json"
Cohesion: 0.09
Nodes (22): @workspace/ui, eslint, @eslint/js, eslint-plugin-react-hooks, eslint-plugin-react-refresh, globals, @hugeicons/core-free-icons, @hugeicons/react (+14 more)

### Community 22 - "test_cli.py"
Cohesion: 0.14
Nodes (14): build_graph(), PipelineDeps, test_config_error_exits_2(), boom(), test_ingest_directory_is_deterministic_and_duplicate_is_free(), test_ingest_disabled_configuration_never_calls_provider(), test_ingest_failure_exit_and_retry_stored(), test_ingest_invalid_source_does_not_stop_other_files() (+6 more)

### Community 23 - "compilerOptions"
Cohesion: 0.09
Nodes (22): compilerOptions, allowArbitraryExtensions, allowImportingTsExtensions, erasableSyntaxOnly, jsx, lib, module, moduleDetection (+14 more)

### Community 24 - "employee-frontend/components.json"
Cohesion: 0.09
Nodes (21): aliases, components, hooks, lib, ui, utils, iconLibrary, menuAccent (+13 more)

### Community 25 - "test_final_fix_handoff.py"
Cohesion: 0.11
Nodes (23): Passage, process_batch(), Knowledge, assert_completed_evidence(), faulty_knowledge(), read(), outer_deadlines(), PaidEmbeddings (+15 more)

### Community 26 - "compilerOptions"
Cohesion: 0.09
Nodes (21): compilerOptions, allowArbitraryExtensions, allowImportingTsExtensions, erasableSyntaxOnly, jsx, lib, module, moduleDetection (+13 more)

### Community 27 - "web/src/components/theme-provider.tsx"
Cohesion: 0.14
Nodes (14): App(), disableTransitionsTemporarily(), getSystemTheme(), isEditableTarget(), isTheme(), ResolvedTheme, Theme, THEME_VALUES (+6 more)

### Community 28 - "test_embeddings.py"
Cohesion: 0.10
Nodes (38): EmbeddingError, _nonnegative_number(), OpenRouterEmbedder, _ordered_vectors(), _response_cost(), embedder_for(), item(), response_payload() (+30 more)

### Community 29 - "Classify and Extract Prompts"
Cohesion: 0.31
Nodes (9): extract, gemini_classify, Pipeline Graph Orchestration, jev_classify, prepare, Gemini Classify Prompt v1, Gemini Extract Prompt v1, GeminiClassifier (+1 more)

### Community 30 - "FakeJevRunnable"
Cohesion: 0.10
Nodes (28): CredentialCheck, DegradedCredentialChecker, _finite_nonnegative(), _get(), JevCredentialChecker, FakeJevRunnable, ResponseRunnable, test_bad_usage_cannot_poison_cost() (+20 more)

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
Cohesion: 0.07
Nodes (42): SearchResult, _Claim, DocumentNotFoundError, IndexAttemptLostError, KnowledgeError, KnowledgeService, FakeEmbedder, GatedEmbedder (+34 more)

### Community 36 - "web/components.json"
Cohesion: 0.10
Nodes (19): aliases, components, hooks, lib, ui, utils, iconLibrary, menuAccent (+11 more)

### Community 38 - "repository.py"
Cohesion: 0.12
Nodes (28): get_run(), list_runs(), start_run(), BatchInput, _run_with_db(), RunRow, create_run(), finish_run() (+20 more)

### Community 39 - "ui/components.json"
Cohesion: 0.10
Nodes (19): aliases, components, hooks, lib, ui, utils, iconLibrary, menuAccent (+11 more)

### Community 40 - "build_pipeline"
Cohesion: 0.14
Nodes (19): SqlTransactionRepo, build_pipeline(), ConfigError, make_jev_client(), model_ids(), GeminiAnalysis, FakeStructuredLLM, _settings() (+11 more)

### Community 41 - "test_draft_tools.py"
Cohesion: 0.10
Nodes (29): IncidentRow, KnowledgeExecutionError, api(), ErrorEmbedder, settings(), test_all_eight_tools_and_seven_parallel_calls_execute_only_six(), test_database_faults_remain_distinct_and_record_paid_search_cost(), test_discovered_ref_can_be_inspected_but_not_promoted_to_match() (+21 more)

### Community 43 - "Human Review Gate"
Cohesion: 0.25
Nodes (4): support CLI, Support Workspace UI Plan, Review API, Workspace UI Verification

### Community 44 - "compilerOptions"
Cohesion: 0.12
Nodes (16): compilerOptions, allowImportingTsExtensions, erasableSyntaxOnly, lib, module, moduleDetection, noEmit, noFallthroughCasesInSwitch (+8 more)

### Community 46 - "FieldPick"
Cohesion: 0.20
Nodes (15): FieldPick, FieldExtractor, _field(), fill_gaps(), finalize(), _is_weak(), _iso(), FakeExtractor (+7 more)

### Community 47 - "compilerOptions"
Cohesion: 0.12
Nodes (16): compilerOptions, allowImportingTsExtensions, erasableSyntaxOnly, lib, module, moduleDetection, noEmit, noFallthroughCasesInSwitch (+8 more)

### Community 48 - "RAG drafting verification — 2026-10-17"
Cohesion: 0.18
Nodes (11): ingest(), Artifacts, servers and remaining concerns, Citation IDs and provider evidence, Commands and automated verification — historical Task 8, Corpus and actual retrieval, Current final verification and review closure, Environment and isolation, Live browser and persistence evidence (+3 more)

### Community 57 - "parse_document"
Cohesion: 0.10
Nodes (30): TextChunk, _append_chunks(), _check_extracted_size(), DocumentParseError, parse_document(), _parse_pdf(), make_pdf(), test_arabic_text_and_bom_are_preserved() (+22 more)

### Community 58 - "tools.py"
Cohesion: 0.24
Nodes (8): _Flag, _History, _Input, _Knowledge, _Lookup, _Recent, _Search, _Service

### Community 59 - "_ModelUsage"
Cohesion: 0.21
Nodes (5): _error_cost(), _ModelUsage, _number(), _bounded(), visit()

### Community 60 - "SqlInvestigationRepo"
Cohesion: 0.18
Nodes (15): TransactionRow, TxnRecord, parse_dt(), DraftToolInputError, _datetime(), _days(), _field(), _involves() (+7 more)

### Community 61 - "NewBatchPage.tsx"
Cohesion: 0.12
Nodes (15): buttonVariants, Tabs(), TabsContent(), TabsList(), tabsListVariants, TabsTrigger(), Textarea(), exampleTickets (+7 more)

### Community 62 - "rules.py"
Cohesion: 0.19
Nodes (17): LookupResult, decide(), empty_ticket_decision(), merge_reasons(), note_for(), _unique(), Category, state() (+9 more)

### Community 63 - "cli.py"
Cohesion: 0.18
Nodes (11): _command_settings(), ingest_kb_cmd(), init_db_cmd(), Mode, run_batch_cmd(), _run_in_memory(), seed_db_cmd(), _sessionmaker() (+3 more)

### Community 64 - "tasks"
Cohesion: 0.12
Nodes (16): dependsOn, inputs, outputs, cache, persistent, dependsOn, dependsOn, $schema (+8 more)

### Community 65 - "LLMUnavailable"
Cohesion: 0.16
Nodes (12): LLMUnavailable, Sample, combine(), merge_picks(), test_both_missing_raises(), test_cost_is_summed(), test_degraded_when_jev_missing(), test_disagreement_when_jev_was_partly_confident() (+4 more)

### Community 66 - "graph.py"
Cohesion: 0.10
Nodes (11): get_session(), TicketOutcome, TicketExecution, _default_retry(), outcome_from_state(), _percentile(), _retryable(), run_batch() (+3 more)

### Community 67 - "HTTP contract (implemented in Tasks 4–5)"
Cohesion: 0.20
Nodes (10): fail(), HTTP contract (implemented in Tasks 4–5), Task 2: Evidence merging and adaptive readiness, Task 3: Validated attachments and bounded multimodal interpretation, Task 4: Resumable graph turns, review and customer API, Task 7: Bilingual customer chat, screenshots and reviewed submission, Task 8: Employee evidence panel and processing state, Task 9: End-to-end handoff, live vision evidence and runbook (+2 more)

### Community 68 - "make_ticket"
Cohesion: 0.26
Nodes (18): FakeClassifier, make_output(), make_ticket(), _deps(), _run(), test_cascade_confident_jev_skips_gemini(), test_cascade_degrades_when_jev_fails(), test_cascade_uncertain_jev_goes_to_gemini() (+10 more)

### Community 69 - "_DatabaseCall"
Cohesion: 0.15
Nodes (4): _check_deadline(), _consume(), _DatabaseCall, Task 6: Customer API client and resumable UI state

### Community 70 - "build_tools"
Cohesion: 0.17
Nodes (4): build_tools(), flag(), retrieve(), _error_cost()

### Community 72 - "taxonomy.py"
Cohesion: 0.16
Nodes (8): load_taxonomy(), most_urgent(), priority_rank(), TaxonomyError, tax(), taxonomy(), test_priority_helpers(), test_rejects_unknown_team()

### Community 73 - "normalize.py"
Cohesion: 0.22
Nodes (16): detect_arabizi(), fold_arabic(), has_latin_mix(), _latin_words(), mask_cards(), normalize(), sanitize_for_storage(), test_arabizi_detection() (+8 more)

### Community 74 - "types.ts"
Cohesion: 0.10
Nodes (36): Input(), acceptIndexRequest(), canRequestIndex(), PendingIndexes, persistPendingIndexes(), pollKnowledge(), refresh(), stop() (+28 more)

### Community 75 - "test-kb/README.md"
Cohesion: 0.12
Nodes (8): Fictional RAG walkthrough inputs, نزاع مع وكيل — سياسة خيالية للعرض التجريبي, مشاكل البطاقة — سياسة خيالية للعرض التجريبي, التحويل المعلّق — سياسة خيالية للعرض التجريبي, الاستفسار الآمن من الدعم — سياسة خيالية للعرض التجريبي, استعادة الدخول — سياسة خيالية للعرض التجريبي, استرجاع مبلغ شراء — سياسة خيالية للعرض التجريبي, التحويل لمستلم بالخطأ — سياسة خيالية للعرض التجريبي

### Community 76 - "ingest.py"
Cohesion: 0.26
Nodes (8): load_jsonl(), load_tickets(), _rows(), test_csv_with_bom_and_missing_columns(), test_duplicate_external_ids_keep_first(), test_json_object_without_ids(), test_jsonl_fixture_loads(), test_unsupported_format()

### Community 77 - "EmbeddingBatch"
Cohesion: 0.17
Nodes (4): Embedder, EmbeddingBatch, Embeddings, embed()

### Community 79 - "devDependencies"
Cohesion: 0.12
Nodes (16): devDependencies, eslint, @eslint/js, eslint-plugin-react-hooks, eslint-plugin-react-refresh, globals, prettier, prettier-plugin-tailwindcss (+8 more)

### Community 80 - "judge-demo.ar.md"
Cohesion: 0.14
Nodes (13): أعطال التطبيق — سياسة خيالية للعرض التجريبي, استرجاع مبلغ شراء — سياسة خيالية للعرض التجريبي, استعادة الدخول — سياسة خيالية للعرض التجريبي, الاستفسار الآمن من الدعم — سياسة خيالية للعرض التجريبي, الاستفسار المؤقت للدعم في المهمة ٨ — سياسة خيالية للعرض التجريبي, التحويل المعلّق — سياسة خيالية للعرض التجريبي, التحويل لمستلم بالخطأ — سياسة خيالية للعرض التجريبي, الطلبات غير الواضحة وخارج النطاق — سياسة خيالية للعرض التجريبي (+5 more)

### Community 93 - "ScriptedChat"
Cohesion: 0.21
Nodes (7): Checker, ScriptedChat, evidence_client(), pipeline(), submit(), test_concurrent_tickets_cannot_exchange_citations_cost_or_callback_state(), Task 5: Agent, failure conversion and pipeline wiring

### Community 94 - "devDependencies"
Cohesion: 0.14
Nodes (14): devDependencies, eslint, @eslint/js, eslint-plugin-react-hooks, eslint-plugin-react-refresh, globals, @tailwindcss/vite, @types/node (+6 more)

### Community 95 - "devDependencies"
Cohesion: 0.14
Nodes (14): devDependencies, eslint, @eslint/js, eslint-plugin-react-hooks, eslint-plugin-react-refresh, globals, tailwindcss, @tailwindcss/vite (+6 more)

### Community 96 - "test_draft_model.py"
Cohesion: 0.15
Nodes (11): make_draft_model(), make_gemini_llm(), RagDrafter, CredentialChecker, response_payload(), run_provider_pipeline(), send(), search_response() (+3 more)

### Community 97 - "Plan 3 — Knowledge retrieval and grounded reply drafting"
Cohesion: 0.11
Nodes (18): 10. Remaining demo roadmap, 1. Intent and acceptance criteria, 3. Provider and configuration, 4. Knowledge ingestion and persistence, 5. Retrieval and evidence, 6. Bounded investigation agent, 7. Draft guardrails and failure outcomes, 8. Pipeline, API, CLI and UI integration (+10 more)

### Community 98 - "Plan 3 RAG Drafting Implementation Plan"
Cohesion: 0.20
Nodes (10): Completion and review record — 2026-10-17, Execution handoff, File map and shared interfaces, Global Constraints, Plan 3 RAG Drafting Implementation Plan, Plan self-review, Review Focus, Task 6: API/CLI indexing and persisted citation projection (+2 more)

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

### Community 106 - "pipeline/contracts.py"
Cohesion: 0.24
Nodes (8): Decision, ExtractedField, Ticket, outcome_to_dict(), outcome_to_row(), state(), test_failed_outcome_and_dict_form(), test_full_outcome_is_json_safe()

### Community 107 - "test_gemini.py"
Cohesion: 0.31
Nodes (12): ExtractedSpan, _Fields, GeminiFields, _a(), _classify(), test_all_samples_failing_raises(), test_extractor_requests_only_named_fields(), test_failed_samples_count_against_confidence() (+4 more)

### Community 108 - "test_workspace_api.py"
Cohesion: 0.21
Nodes (7): start_run(), test_batch_and_queue_expose_real_results(), test_batch_failure_is_isolated_and_conflicting_ids_rejected(), test_openrouter_credentials_enable_api_modes_without_exposing_keys(), test_progress_counts_only_durable_results_after_save_failure(), fail_one_save(), test_review_requires_text_and_rejects_stale_updates()

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

### Community 114 - "test_llm.py"
Cohesion: 0.27
Nodes (8): _llm(), _S, test_draft_model_uses_millisecond_timeout_and_disables_sdk_retries(), test_openrouter_reported_cost_takes_precedence_over_token_estimate(), test_openrouter_structured_samples_use_configured_key_and_validate_output(), send(), test_to_sample_exception_and_parse_error(), test_to_sample_parsed_with_cost()

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
Cohesion: 0.18
Nodes (7): Settings, test_defaults(), test_drafting_configuration_cannot_bypass_hard_limits(), test_drafting_limits_load_from_environment(), test_env_overrides(), test_legacy_gemini_model_names_are_qualified_for_openrouter(), test_openrouter_key_is_loaded_from_environment()

### Community 120 - "scripts"
Cohesion: 0.50
Nodes (4): scripts, format, lint, typecheck

### Community 121 - "shadcn/ui monorepo template"
Cohesion: 0.50
Nodes (3): Adding components, shadcn/ui monorepo template, Using components

### Community 125 - "resolve_date"
Cohesion: 0.36
Nodes (4): resolve_date(), _safe_date(), test_resolve(), test_unresolvable_is_none()

### Community 126 - "test_dbapi_commit_handoff_arbitrates_cancellation"
Cohesion: 0.47
Nodes (4): test_dbapi_commit_handoff_arbitrates_cancellation(), gate(), gate_before_dbapi(), gate_inside_dbapi()

### Community 130 - "Customer Conversation Intake Implementation Plan"
Cohesion: 0.22
Nodes (8): Customer Conversation Intake Implementation Plan, Execution conventions and repository baseline, File map and dependency order, Global Constraints, Plan review and execution handoff, Review Focus, Shared contracts (implement in Task 1; extend only through explicit edits here), Spec coverage and acceptance map

### Community 131 - "DraftToolLimit"
Cohesion: 0.29
Nodes (5): DraftAlreadySubmitted, DraftToolLimit, guarded(), invoke(), _json()

### Community 133 - "Synthetic demo readiness"
Cohesion: 0.50
Nodes (4): Evidence by layer, Known limitations and remaining work, Repeatable local walkthrough, Synthetic demo readiness

## Ambiguous Edges - Review These
- `Fraud Report` → `Plan 1 Live Smoke`  [AMBIGUOUS]
  README.md · relation: conceptually_related_to

## Knowledge Gaps
- **85 isolated node(s):** `zaincash-support`, `@base-ui/react`, `@fontsource-variable/geist`, `@tailwindcss/vite`, `class-variance-authority` (+80 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 850 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **38 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `GeminiStructuredLLM` connect `GeminiStructuredLLM` to `test_draft_model.py`, `LLMUnavailable`, `test_llm.py`, `HTTP contract (implemented in Tasks 4–5)`?**
  _High betweenness centrality (0.113) - this node is a cross-community bridge._
- **Are the 24 inferred relationships involving `KnowledgeService` (e.g. with `Settings` and `UploadedDocument`) actually correct?**
  _`KnowledgeService` has 24 INFERRED edges - model-reasoned connections that need verification._
- **What connects `zaincash-support`, `@base-ui/react`, `@fontsource-variable/geist` to the rest of the system?**
  _85 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `pipeline/contracts.py` be split into smaller, more focused modules?**
  _Cohesion score 0.13360323886639677 - nodes in this community are weakly interconnected._
- **Why does `Task 3: Validated attachments and bounded multimodal interpretation` connect `HTTP contract (implemented in Tasks 4–5)` to `GeminiStructuredLLM`?**
  _High betweenness centrality (0.109) - this node is a cross-community bridge._
- **Are the 27 inferred relationships involving `Settings` (e.g. with `_command_settings()` and `_run_in_memory()`) actually correct?**
  _`Settings` has 27 INFERRED edges - model-reasoned connections that need verification._

### Low-confidence Hints
_AMBIGUOUS edges — the extractor was unsure. Verify before acting on these._

- **What is the exact relationship between `Fraud Report` and `Plan 1 Live Smoke`?**
  _Edge tagged AMBIGUOUS (relation: conceptually_related_to) - confidence is low._