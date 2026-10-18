# Graph Report - zaincash-support  (2026-10-18)

## Corpus Check
- 262 files · ~217,303 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 25 file(s) not represented in the graph (top: (none) 15, .jsonl 4, .css 3)

## Summary
- 2751 nodes · 8286 edges · 157 communities (112 shown, 45 thin omitted)
- Extraction: 89% EXTRACTED · 11% INFERRED · 0% AMBIGUOUS · INFERRED: 918 edges (avg confidence: 0.93)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `b1dd3fda`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- LLMUnavailable
- guardrails.py
- test_rag_drafter.py
- TurnStore
- TicketReviewPage.tsx
- workspace.py
- QueuePage.tsx
- Customer conversation intake for ZainCash support
- workspace-ui.tsx
- IntakeController
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
- RunRow
- intake/repository.py
- Human Review Gate
- compilerOptions
- fakes.py
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
- IntakeState
- Credentials
- make_ticket
- _DatabaseCall
- PipelineState
- agent.py
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
- RagDrafter
- TurnContext
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
- context
- ar/fraud_report.md
- attachments.py
- resolve_date
- InvalidEvidence
- build_pipeline
- ar/wrong_recipient.md
- intake/model.py
- Customer Conversation Intake Implementation Plan
- intake.py
- test_final_fix_handoff.py
- Synthetic demo readiness
- kb/service.py
- find_candidates
- main.py
- IntakeRepository
- evidence.py
- test_submission.py
- test_dbapi_commit_handoff_arbitrates_cancellation
- SubmissionService
- tmp-graphify-update.sh
- GeminiStructuredLLM
- ar/refund_request.md
- intake/test_repository.py
- KnowledgeExecutionError
- ar/app_bug.md
- ar/bill_payment.md
- ar/card_issue.md
- ar/failed_transfer.md
- ar/general_inquiry.md
- ar/login_access.md
- ar/other.md

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
- `Pipeline and CLI` --references--> `NullDrafter`  [INFERRED]
  docs/superpowers/specs/2026-10-17-plan3-rag-drafting-design.md → backend/app/pipeline/stage6_draft/drafting.py
- `Task 9: End-to-end handoff, live vision evidence and runbook` --references--> `intake_client()`  [INFERRED]
  docs/superpowers/plans/2026-10-18-customer-intake.md → backend/tests/intake/conftest.py

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **Cascade Classification Path** — docs_superpowers_specs_2026_10_07_support_pipeline_design_cascade, docs_superpowers_plans_2026_10_07_plan1_core_pipeline_part2_jev_classifier, docs_superpowers_plans_2026_10_07_plan1_core_pipeline_part2_gemini_classifier, docs_superpowers_plans_2026_10_07_plan1_core_pipeline_part2_cascade_combine, readme_human_approval [EXTRACTED 1.00]
- **Drafting Agent Toolset** — backend_app_pipeline_runner_lookup_transaction, backend_app_pipeline_runner_search_transactions, backend_app_pipeline_runner_get_customer_recent_transactions, backend_app_pipeline_runner_get_customer_ticket_history, backend_app_pipeline_runner_check_service_status, backend_app_pipeline_runner_search_knowledge_base, backend_app_pipeline_runner_flag_for_human, backend_app_pipeline_runner_submit_draft [EXTRACTED 1.00]
- **Ticket Processing Stage Flow** — backend_app_pipeline_runner_prepare, backend_app_pipeline_runner_jev_classify, backend_app_pipeline_runner_gemini_classify, backend_app_pipeline_runner_extract, backend_app_pipeline_runner_lookup, backend_app_pipeline_runner_decide, backend_app_pipeline_runner_draft [EXTRACTED 1.00]

## Communities (157 total, 45 thin omitted)

### Community 0 - "LLMUnavailable"
Cohesion: 0.16
Nodes (12): LLMUnavailable, combine(), merge_picks(), _Execution, test_both_missing_raises(), test_cost_is_summed(), test_degraded_when_jev_missing(), test_disagreement_when_jev_was_partly_confident() (+4 more)

### Community 1 - "guardrails.py"
Cohesion: 0.20
Nodes (12): normalize_phone(), parse_amount(), _iso(), normalize_value(), check_draft(), _citation_findings(), _exact_amount(), _grounding_findings() (+4 more)

### Community 2 - "test_rag_drafter.py"
Cohesion: 0.19
Nodes (34): answer(), call(), Checker, draft_state(), script(), submit(), drafter(), events() (+26 more)

### Community 3 - "TurnStore"
Cohesion: 0.20
Nodes (11): OperationClaim, TurnResult, RevisionConflict, turn_context(), _jsonable(), TurnStore, repo(), test_recovered_attempt_cannot_publish_stale_output() (+3 more)

### Community 4 - "TicketReviewPage.tsx"
Cohesion: 0.26
Nodes (18): Confidence(), Metric(), Badge(), badgeVariants, Card(), CardContent(), CardHeader(), CardTitle() (+10 more)

### Community 5 - "workspace.py"
Cohesion: 0.19
Nodes (6): get_session(), health(), insights(), workspace(), knowledge_configured(), latest_results_query()

### Community 6 - "QueuePage.tsx"
Cohesion: 0.21
Nodes (30): EmptyState(), ErrorState(), LoadingState(), PageHeader(), PriorityBadge(), StatusBadge(), Table(), TableBody() (+22 more)

### Community 7 - "Customer conversation intake for ZainCash support"
Cohesion: 0.06
Nodes (31): 10. Verification and acceptance criteria, 11. Delivery and review, 1. Outcome and agreed requirements, 2. Current implementation and integration points, 3. Approach and boundaries, 4. Conversation state and turn flow, 5. Facts, evidence, and readiness, 6. Language and screenshot behavior (+23 more)

### Community 8 - "workspace-ui.tsx"
Cohesion: 0.09
Nodes (22): ConfirmDialog(), FilterSelect(), statusLabels, Button(), buttonVariants, Dialog(), DialogContent(), DialogDescription() (+14 more)

### Community 9 - "IntakeController"
Cohesion: 0.06
Nodes (38): Task 6: Customer API client and resumable UI state, IntakeApi, IntakeRequestError, isRecord(), parseJson(), parseReceipt(), parseSession(), readError() (+30 more)

### Community 10 - "lookup.py"
Cohesion: 0.18
Nodes (15): ExtractedField, _as_date(), _iqd_amount(), match_transaction(), TransactionRepo, _ex(), _match(), test_ambiguous_then_disambiguated_by_counterpart() (+7 more)

### Community 11 - "test_rag_api.py"
Cohesion: 0.11
Nodes (22): FakeStructuredLLM, client(), evidence_client(), pipeline(), submit(), test_actual_guardrail_failure_is_separate_from_reply(), test_concurrent_index_requests_share_active_work(), test_disabled_or_missing_provider_stores_without_indexing() (+14 more)

### Community 12 - "employee-frontend/package.json"
Cohesion: 0.07
Nodes (28): @base-ui/react, class-variance-authority, cn, eslint, @eslint/js, eslint-plugin-react-hooks, eslint-plugin-react-refresh, globals (+20 more)

### Community 14 - "test_draft_guardrails.py"
Cohesion: 0.07
Nodes (44): LookupResult, requests_credentials(), check(), state(), test_aggregation_is_deduplicated_and_has_no_state_side_effects(), test_amount_occurrences_keep_their_own_currency_and_sign(), test_avoid_sharing_warning_does_not_excuse_a_later_request(), test_candidate_prompt_limit_does_not_hide_later_ungrounded_references() (+36 more)

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

### Community 19 - "db/models.py"
Cohesion: 0.11
Nodes (16): get_result(), list_results(), read_intake_attachment(), review_result(), ReviewInput, Base, ReviewRow, TicketResultRow (+8 more)

### Community 20 - "UploadedDocument"
Cohesion: 0.12
Nodes (19): delete_document(), download_document(), index_document(), list_chunks(), list_documents(), _require_provider(), search_knowledge(), upload_document() (+11 more)

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
Cohesion: 0.15
Nodes (11): KnowledgeChunk, KnowledgeDocumentIndex, _Claim, IndexAttemptLostError, KnowledgeError, KnowledgeService, test_incompatible_or_unowned_chunks_cannot_be_searched(), test_model_changes_require_reindex_and_keep_chunk_ids() (+3 more)

### Community 26 - "compilerOptions"
Cohesion: 0.09
Nodes (21): compilerOptions, allowArbitraryExtensions, allowImportingTsExtensions, erasableSyntaxOnly, jsx, lib, module, moduleDetection (+13 more)

### Community 27 - "web/src/components/theme-provider.tsx"
Cohesion: 0.21
Nodes (11): disableTransitionsTemporarily(), getSystemTheme(), isEditableTarget(), isTheme(), ResolvedTheme, Theme, THEME_VALUES, ThemeProvider() (+3 more)

### Community 28 - "test_embeddings.py"
Cohesion: 0.08
Nodes (41): EmbeddingBatch, EmbeddingError, _nonnegative_number(), OpenRouterEmbedder, _ordered_vectors(), _response_cost(), Embeddings, embed() (+33 more)

### Community 29 - "Classify and Extract Prompts"
Cohesion: 0.31
Nodes (9): extract, gemini_classify, Pipeline Graph Orchestration, jev_classify, prepare, Gemini Classify Prompt v1, Gemini Extract Prompt v1, GeminiClassifier (+1 more)

### Community 30 - "FakeJevRunnable"
Cohesion: 0.05
Nodes (61): IncidentRow, CredentialCheck, DegradedCredentialChecker, _finite_nonnegative(), _get(), JevCredentialChecker, FakeJevRunnable, test_contracts_reject_extra_keys() (+53 more)

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
Nodes (26): FakeEmbedder, GatedEmbedder, LateEmbedder, PaidEmbedder, count_chunks(), test_category_filters_include_general_policies_and_validate_tags(), test_claim_locks_source_even_before_index_row_exists(), test_competing_callers_refuse_active_attempt_and_release_transactions() (+18 more)

### Community 36 - "web/components.json"
Cohesion: 0.10
Nodes (19): aliases, components, hooks, lib, ui, utils, iconLibrary, menuAccent (+11 more)

### Community 38 - "repository.py"
Cohesion: 0.12
Nodes (24): finish_run(), load_incidents(), load_transactions(), save_outcomes(), _to_record(), _upsert(), upsert_tickets(), TicketOutcome (+16 more)

### Community 39 - "ui/components.json"
Cohesion: 0.10
Nodes (19): aliases, components, hooks, lib, ui, utils, iconLibrary, menuAccent (+11 more)

### Community 40 - "RunRow"
Cohesion: 0.13
Nodes (19): _safe_dispatch(), get_run(), list_runs(), start_run(), BatchInput, RunRow, create_run(), recover() (+11 more)

### Community 41 - "intake/repository.py"
Cohesion: 0.14
Nodes (17): _display_name(), Attachment, CustomerReview, IntakeAttachmentRow, IntakeMessageRow, _attachment(), customer_review(), initial_state() (+9 more)

### Community 43 - "Human Review Gate"
Cohesion: 0.25
Nodes (4): support CLI, Support Workspace UI Plan, Review API, Workspace UI Verification

### Community 44 - "compilerOptions"
Cohesion: 0.12
Nodes (16): compilerOptions, allowImportingTsExtensions, erasableSyntaxOnly, lib, module, moduleDetection, noEmit, noFallthroughCasesInSwitch (+8 more)

### Community 46 - "fakes.py"
Cohesion: 0.19
Nodes (17): Candidates, FieldPick, NormalizedTicket, Classifier, FieldExtractor, _field(), fill_gaps(), finalize() (+9 more)

### Community 47 - "compilerOptions"
Cohesion: 0.12
Nodes (16): compilerOptions, allowImportingTsExtensions, erasableSyntaxOnly, lib, module, moduleDetection, noEmit, noFallthroughCasesInSwitch (+8 more)

### Community 48 - "support_test"
Cohesion: 0.09
Nodes (23): ingest(), index_deadlines(), settings(), support_test(), Completion and review record — 2026-10-17, Execution handoff, File map and shared interfaces, Global Constraints (+15 more)

### Community 57 - "parse_document"
Cohesion: 0.10
Nodes (30): TextChunk, _append_chunks(), _check_extracted_size(), DocumentParseError, parse_document(), _parse_pdf(), make_pdf(), test_arabic_text_and_bom_are_preserved() (+22 more)

### Community 58 - "tools.py"
Cohesion: 0.07
Nodes (20): DraftAlreadySubmitted, DraftSubmission, DraftToolLimit, _bounded(), visit(), build_tools(), flag(), guarded() (+12 more)

### Community 59 - "intake/contracts.py"
Cohesion: 0.20
Nodes (10): _aware(), EvidenceRef, IntakeModel, Message, Question, QuestionRecord, Readiness, ReviewSnapshot (+2 more)

### Community 60 - "SqlInvestigationRepo"
Cohesion: 0.16
Nodes (14): TxnRecord, parse_dt(), DraftToolInputError, _datetime(), _days(), _field(), _involves(), _phone() (+6 more)

### Community 61 - "NewBatchPage.tsx"
Cohesion: 0.20
Nodes (14): Tabs(), TabsContent(), TabsList(), tabsListVariants, TabsTrigger(), Textarea(), readReport(), exampleTickets (+6 more)

### Community 62 - "rules.py"
Cohesion: 0.13
Nodes (19): ClassifierOutput, Decision, _default_retry(), _retryable(), decide(), empty_ticket_decision(), merge_reasons(), note_for() (+11 more)

### Community 63 - "cli.py"
Cohesion: 0.14
Nodes (13): _command_settings(), ingest_kb_cmd(), init_db_cmd(), Mode, run_batch_cmd(), _run_in_memory(), seed_db_cmd(), _sessionmaker() (+5 more)

### Community 64 - "tasks"
Cohesion: 0.12
Nodes (16): dependsOn, inputs, outputs, cache, persistent, dependsOn, dependsOn, $schema (+8 more)

### Community 65 - "types.ts"
Cohesion: 0.11
Nodes (25): source, STAGE_NODES, timing(), renderableTrace(), reviewEvidence(), source, save(), checkFact() (+17 more)

### Community 66 - "IntakeState"
Cohesion: 0.24
Nodes (13): IntakeState, _asked_already(), asks_for_secret(), assess_readiness(), _can_ask(), canonical_category(), choose_question(), _fallback() (+5 more)

### Community 67 - "Credentials"
Cohesion: 0.18
Nodes (5): Credentials, SessionView, IntakeService, _error_cost(), _number()

### Community 68 - "make_ticket"
Cohesion: 0.28
Nodes (18): FakeClassifier, make_output(), make_ticket(), _deps(), _run(), test_cascade_confident_jev_skips_gemini(), test_cascade_degrades_when_jev_fails(), test_cascade_uncertain_jev_goes_to_gemini() (+10 more)

### Community 71 - "agent.py"
Cohesion: 0.08
Nodes (4): Sample, CredentialChecker, DraftChatOpenRouter, DraftProviderResponseError

### Community 72 - "taxonomy.py"
Cohesion: 0.13
Nodes (9): load_taxonomy(), most_urgent(), priority_rank(), TaxonomyError, tax(), taxonomy(), taxonomy(), test_priority_helpers() (+1 more)

### Community 73 - "normalize.py"
Cohesion: 0.18
Nodes (17): detect_arabizi(), fold_arabic(), has_latin_mix(), _latin_words(), mask_cards(), normalize(), sanitize_for_storage(), to_ascii_digits() (+9 more)

### Community 74 - "use-knowledge-library.ts"
Cohesion: 0.12
Nodes (27): acceptIndexRequest(), canRequestIndex(), PendingIndexes, persistPendingIndexes(), pollKnowledge(), refresh(), stop(), PollOptions (+19 more)

### Community 75 - "test-kb/README.md"
Cohesion: 0.22
Nodes (4): Fictional RAG walkthrough inputs, توثيق الحساب — سياسة خيالية للعرض التجريبي, نزاع مع وكيل — سياسة خيالية للعرض التجريبي, الاستفسار المؤقت للدعم في المهمة ٨ — سياسة خيالية للعرض التجريبي

### Community 76 - "ingest.py"
Cohesion: 0.26
Nodes (8): load_jsonl(), load_tickets(), _rows(), test_csv_with_bom_and_missing_columns(), test_duplicate_external_ids_keep_first(), test_json_object_without_ids(), test_jsonl_fixture_loads(), test_unsupported_format()

### Community 77 - "KnowledgePage"
Cohesion: 0.36
Nodes (9): Input(), BadgeLabel(), KnowledgePage(), beginMutation(), deleteDocument(), finishMutation(), indexDocument(), upload() (+1 more)

### Community 79 - "devDependencies"
Cohesion: 0.12
Nodes (16): devDependencies, eslint, @eslint/js, eslint-plugin-react-hooks, eslint-plugin-react-refresh, globals, prettier, prettier-plugin-tailwindcss (+8 more)

### Community 80 - "judge-demo.ar.md"
Cohesion: 0.14
Nodes (13): أعطال التطبيق — سياسة خيالية للعرض التجريبي, استرجاع مبلغ شراء — سياسة خيالية للعرض التجريبي, استعادة الدخول — سياسة خيالية للعرض التجريبي, الاستفسار الآمن من الدعم — سياسة خيالية للعرض التجريبي, الاستفسار المؤقت للدعم في المهمة ٨ — سياسة خيالية للعرض التجريبي, التحويل المعلّق — سياسة خيالية للعرض التجريبي, التحويل لمستلم بالخطأ — سياسة خيالية للعرض التجريبي, الطلبات غير الواضحة وخارج النطاق — سياسة خيالية للعرض التجريبي (+5 more)

### Community 93 - "jev.py"
Cohesion: 0.24
Nodes (10): ClassificationResult, build_order_check(), build_questions(), build_state(), category_criteria(), _input_tokens(), JevClassifier, _picks() (+2 more)

### Community 94 - "devDependencies"
Cohesion: 0.14
Nodes (14): devDependencies, eslint, @eslint/js, eslint-plugin-react-hooks, eslint-plugin-react-refresh, globals, @tailwindcss/vite, @types/node (+6 more)

### Community 95 - "devDependencies"
Cohesion: 0.14
Nodes (14): devDependencies, eslint, @eslint/js, eslint-plugin-react-hooks, eslint-plugin-react-refresh, globals, tailwindcss, @tailwindcss/vite (+6 more)

### Community 96 - "rag_fakes.py"
Cohesion: 0.18
Nodes (15): make_draft_model(), build_graph(), PipelineDeps, InMemoryTransactionRepo, pipeline(), test_run_batch_no_db_writes_summary_and_out(), fake_build(), response_payload() (+7 more)

### Community 97 - "RagDrafter"
Cohesion: 0.09
Nodes (16): DraftResult, _ModelUsage, RagDrafter, DraftContext, Drafter, DraftExecutionError, NullDrafter, UnavailableDrafter (+8 more)

### Community 98 - "TurnContext"
Cohesion: 0.16
Nodes (5): TurnContext, IntakeGraph, _invitation(), grounded_review(), ScriptedIntakeModel

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

### Community 106 - "TicketInput"
Cohesion: 0.31
Nodes (3): KnowledgeIndexInput, KnowledgeSearchInput, TicketInput

### Community 107 - "test_gemini.py"
Cohesion: 0.16
Nodes (17): StructuredLLM, ExtractedSpan, _Fields, GeminiClassifier, GeminiExtractor, GeminiFields, verified_pick(), render_prompt() (+9 more)

### Community 108 - "test_workspace_api.py"
Cohesion: 0.19
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
Cohesion: 0.21
Nodes (10): make_gemini_llm(), _llm(), _S, test_draft_model_uses_millisecond_timeout_and_disables_sdk_retries(), test_openrouter_reported_cost_takes_precedence_over_token_estimate(), test_openrouter_retry_budget_is_bounded(), test_openrouter_structured_samples_use_configured_key_and_validate_output(), send() (+2 more)

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
Cohesion: 0.11
Nodes (9): Settings, test_blank_intake_model_is_rejected(), test_non_positive_image_limit_is_rejected(), test_defaults(), test_drafting_configuration_cannot_bypass_hard_limits(), test_drafting_limits_load_from_environment(), test_env_overrides(), test_legacy_gemini_model_names_are_qualified_for_openrouter() (+1 more)

### Community 120 - "scripts"
Cohesion: 0.50
Nodes (4): scripts, format, lint, typecheck

### Community 121 - "shadcn/ui monorepo template"
Cohesion: 0.50
Nodes (3): Adding components, shadcn/ui monorepo template, Using components

### Community 122 - "context"
Cohesion: 0.35
Nodes (20): Analysis, merge_analysis(), context(), fact(), grounded_analysis(), message(), test_assistant_text_cannot_ground_a_customer_fact(), test_foreign_message_cannot_ground_fact() (+12 more)

### Community 124 - "attachments.py"
Cohesion: 0.17
Nodes (17): AttachmentStore, IntakeSessionRow, ImageRejected, NotOwned, png_bytes(), repo(), store(), test_active_turn_rejects_upload() (+9 more)

### Community 125 - "resolve_date"
Cohesion: 0.36
Nodes (4): resolve_date(), _safe_date(), test_resolve(), test_unresolvable_is_none()

### Community 126 - "InvalidEvidence"
Cohesion: 0.16
Nodes (14): ReviewText, IntakeError, InvalidEvidence, StaleReview, build_review(), _compact(), _render_value(), _ticket_text() (+6 more)

### Community 127 - "build_pipeline"
Cohesion: 0.13
Nodes (21): _run_with_db(), SqlTransactionRepo, build_pipeline(), ConfigError, make_jev_client(), model_ids(), run_batch(), GeminiAnalysis (+13 more)

### Community 129 - "intake/model.py"
Cohesion: 0.13
Nodes (20): ImageInput, ModelCall, ModelUnavailable, _analysis_prompt(), _bounded_context(), _guard_size(), ModelBudget, OpenRouterIntakeModel (+12 more)

### Community 130 - "Customer Conversation Intake Implementation Plan"
Cohesion: 0.15
Nodes (12): Customer Conversation Intake Implementation Plan, Execution conventions and repository baseline, File map and dependency order, Global Constraints, HTTP contract (implemented in Tasks 4–5), Plan review and execution handoff, Review Focus, Spec coverage and acceptance map (+4 more)

### Community 131 - "intake.py"
Cohesion: 0.17
Nodes (19): create_session(), _credentials(), _dump(), get_session(), post_message(), read_attachment(), remove_attachment(), request_review() (+11 more)

### Community 132 - "test_final_fix_handoff.py"
Cohesion: 0.12
Nodes (21): process_batch(), Knowledge, assert_completed_evidence(), faulty_knowledge(), read(), outer_deadlines(), PaidEmbeddings, runner_env() (+13 more)

### Community 133 - "Synthetic demo readiness"
Cohesion: 0.50
Nodes (4): Evidence by layer, Known limitations and remaining work, Repeatable local walkthrough, Synthetic demo readiness

### Community 134 - "kb/service.py"
Cohesion: 0.15
Nodes (7): Embedder, Passage, SearchResult, _abandoned(), _consume(), DocumentNotFoundError, _error_cost()

### Community 135 - "find_candidates"
Cohesion: 0.25
Nodes (12): Candidate, _add(), find_candidates(), _overlaps(), test_amount_forms(), test_arabic_indic_amount_not_confused_with_phone(), test_dates_absolute_and_weekday(), test_dedupes_repeated_values() (+4 more)

### Community 136 - "main.py"
Cohesion: 0.09
Nodes (17): init_db(), make_engine(), make_sessionmaker(), reset_db(), upgrade_workspace_schema(), create_app(), lifespan(), IndexJobs (+9 more)

### Community 137 - "IntakeRepository"
Cohesion: 0.17
Nodes (3): IntakeRepository, make_intake_service(), builder()

### Community 138 - "evidence.py"
Cohesion: 0.18
Nodes (15): Fact, canonical_digits(), normalize_reported_date(), _apply(), _check_reference(), _compact(), _newer_correction(), _normalize_precise() (+7 more)

### Community 139 - "test_submission.py"
Cohesion: 0.32
Nodes (4): _payload(), test_concurrent_submit_dispatches_once(), test_second_request_id_reuses_the_approved_review(), test_submission_replay_creates_one_ticket()

### Community 140 - "test_dbapi_commit_handoff_arbitrates_cancellation"
Cohesion: 0.19
Nodes (7): test_db_deadline_includes_pool_and_checkout_without_late_claim(), checked_in(), test_db_deadline_search_cancellation_is_nonblocking_and_retains_cost(), test_dbapi_commit_handoff_arbitrates_cancellation(), gate(), gate_before_dbapi(), gate_inside_dbapi()

### Community 141 - "SubmissionService"
Cohesion: 0.44
Nodes (6): Receipt, IntakeOperationRow, TurnBusy, SubmissionResult, SubmissionService, Ticket

### Community 148 - "intake/test_repository.py"
Cohesion: 0.39
Nodes (6): OperationConflict, assert_same_operation(), operation_fingerprint(), repo(), test_changed_payload_cannot_reuse_operation_identity(), test_token_is_hashed_and_absent_from_the_view()

## Ambiguous Edges - Review These
- `Fraud Report` → `Plan 1 Live Smoke`  [AMBIGUOUS]
  README.md · relation: conceptually_related_to

## Knowledge Gaps
- **86 isolated node(s):** `zaincash-support`, `@base-ui/react`, `@fontsource-variable/geist`, `@tailwindcss/vite`, `class-variance-authority` (+81 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 929 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **45 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Artifacts, servers and remaining concerns` connect `support_test` to `use-knowledge-library.ts`, `workspace.py`?**
  _High betweenness centrality (0.113) - this node is a cross-community bridge._
- **Are the 33 inferred relationships involving `Settings` (e.g. with `_command_settings()` and `_run_in_memory()`) actually correct?**
  _`Settings` has 33 INFERRED edges - model-reasoned connections that need verification._
- **What connects `zaincash-support`, `@base-ui/react`, `@fontsource-variable/geist` to the rest of the system?**
  _86 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Customer conversation intake for ZainCash support` be split into smaller, more focused modules?**
  _Cohesion score 0.0625 - nodes in this community are weakly interconnected._
- **Why does `Settings` connect `Settings` to `intake/model.py`, `test_rag_drafter.py`, `test_final_fix_handoff.py`, `Synthetic demo readiness`, `kb/service.py`, `main.py`, `IntakeRepository`, `test_rag_api.py`, `SubmissionService`, `db/models.py`, `intake/test_repository.py`, `test_cli.py`, `KnowledgeService`, `test_embeddings.py`, `FakeJevRunnable`, `test_kb_service.py`, `repository.py`, `intake/repository.py`, `support_test`, `cli.py`, `agent.py`, `taxonomy.py`, `rag_fakes.py`, `RagDrafter`, `test_workspace_api.py`, `test_llm.py`, `context`, `attachments.py`, `build_pipeline`?**
  _High betweenness centrality (0.107) - this node is a cross-community bridge._
- **Are the 24 inferred relationships involving `KnowledgeService` (e.g. with `Settings` and `UploadedDocument`) actually correct?**
  _`KnowledgeService` has 24 INFERRED edges - model-reasoned connections that need verification._

### Low-confidence Hints
_AMBIGUOUS edges — the extractor was unsure. Verify before acting on these._

- **What is the exact relationship between `Fraud Report` and `Plan 1 Live Smoke`?**
  _Edge tagged AMBIGUOUS (relation: conceptually_related_to) - confidence is low._