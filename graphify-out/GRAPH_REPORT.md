# Graph Report - zaincash-support  (2026-10-17)

## Corpus Check
- 199 files · ~186,210 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 15 file(s) not represented in the graph (top: (none) 7, .jsonl 4, .css 2)

## Summary
- 1826 nodes · 5512 edges · 118 communities (72 shown, 46 thin omitted)
- Extraction: 91% EXTRACTED · 9% INFERRED · 0% AMBIGUOUS · INFERRED: 470 edges (avg confidence: 0.92)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `18134c0c`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- jev.py
- guardrails.py
- PipelineDeps
- test_llm.py
- types.ts
- Shared UI States
- test_draft_tools.py
- Workspace Cards and Badges
- build_pipeline
- DraftResult
- lookup.py
- App and Database Bootstrap
- Dialogs and Pipeline Strip
- UI Package Metadata
- test_draft_guardrails.py
- Support Taxonomy Categories
- shadcn Component Config
- Workspace Routes
- App TypeScript Config
- Support CLI
- UploadedDocument
- Node TypeScript Config
- Pipeline Graph Nodes
- UI Dev Dependencies
- graph.py
- pytest
- UI Runtime Dependencies
- Theme Provider
- test_embeddings.py
- Classify and Extract Prompts
- FakeJevRunnable
- Pipeline Design Spec
- Workspace Plan Concepts
- Drafting Plan Concepts
- test_kb_service.py
- Null Drafter Boundaries
- UI npm Scripts
- Pipeline Spec Rules
- repository.py
- Vite Logo
- ZainCash Mark
- Root TypeScript Config
- Vite Config
- Human Review Gate
- React Logo
- KnowledgeService
- test_final_fix_handoff.py
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
- DraftContext
- SqlInvestigationRepo
- NewBatchPage.tsx
- rules.py
- extract.py
- Settings
- LLMUnavailable
- test_cli.py
- Plan 3 — Knowledge retrieval and grounded reply drafting
- make_ticket
- test_dbapi_commit_handoff_arbitrates_cancellation
- tools.py
- model.py
- taxonomy.py
- extract.py
- KnowledgePage.tsx
- test-kb/README.md
- factory.py
- test_workspace_api.py
- ingest.py
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
- test_draft_model.py
- KnowledgeError
- Plan 3 RAG Drafting Implementation Plan
- test_db_deadline_is_cumulative_across_publication_statements
- قواعد المعرفة العربية للعرض أمام لجنة التحكيم
- CredentialChecker
- demo-readiness.md
- Embedder
- ar/agent_dispute.md
- ar/bill_payment.md
- ar/general_inquiry.md
- ar/login_access.md
- ar/other.md
- task8-history-policy.md
- negative/README.md

## God Nodes (most connected - your core abstractions)
1. `KnowledgeService` - 65 edges
2. `Settings` - 65 edges
3. `draft_state()` - 44 edges
4. `make_ticket()` - 44 edges
5. `PipelineState` - 43 edges
6. `make_output()` - 42 edges
7. `build_pipeline()` - 41 edges
8. `script()` - 35 edges
9. `drafter()` - 33 edges
10. `parse_document()` - 32 edges

## Surprising Connections (you probably didn't know these)
- `Task 6: API/CLI indexing and persisted citation projection` --references--> `KnowledgeService`  [INFERRED]
  docs/superpowers/plans/2026-10-17-plan3-rag-drafting.md → backend/app/kb/service.py
- `Pipeline and CLI` --references--> `NullDrafter`  [INFERRED]
  docs/superpowers/specs/2026-10-17-plan3-rag-drafting-design.md → backend/app/pipeline/stage6_draft/drafting.py
- `Task 8: Demo corpus, full verification and readiness record` --references--> `support_test()`  [INFERRED]
  docs/superpowers/plans/2026-10-17-plan3-rag-drafting.md → backend/tests/test_kb_service.py
- `Repeatable local walkthrough` --references--> `Settings`  [INFERRED]
  docs/demo-readiness.md → backend/app/config.py
- `الأصل ونتيجة التحقق` --references--> `parse_document()`  [INFERRED]
  data/test-kb/README.md → backend/app/kb/parse.py

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **Cascade Classification Path** — docs_superpowers_specs_2026_10_07_support_pipeline_design_cascade, docs_superpowers_plans_2026_10_07_plan1_core_pipeline_part2_jev_classifier, docs_superpowers_plans_2026_10_07_plan1_core_pipeline_part2_gemini_classifier, docs_superpowers_plans_2026_10_07_plan1_core_pipeline_part2_cascade_combine, readme_human_approval [EXTRACTED 1.00]
- **ZainCash Mark Composition** — customer_support_ui_public_zaincash_mark_logo, customer_support_ui_public_zaincash_mark_crimson_square, customer_support_ui_public_zaincash_mark_stacked_bars [EXTRACTED 1.00]
- **Drafting Agent Toolset** — backend_app_pipeline_runner_lookup_transaction, backend_app_pipeline_runner_search_transactions, backend_app_pipeline_runner_get_customer_recent_transactions, backend_app_pipeline_runner_get_customer_ticket_history, backend_app_pipeline_runner_check_service_status, backend_app_pipeline_runner_search_knowledge_base, backend_app_pipeline_runner_flag_for_human, backend_app_pipeline_runner_submit_draft [EXTRACTED 1.00]
- **Ticket Processing Stage Flow** — backend_app_pipeline_runner_prepare, backend_app_pipeline_runner_jev_classify, backend_app_pipeline_runner_gemini_classify, backend_app_pipeline_runner_extract, backend_app_pipeline_runner_lookup, backend_app_pipeline_runner_decide, backend_app_pipeline_runner_draft [EXTRACTED 1.00]
- **Vite Logo Mark** — customer_support_ui_public_vite_vite_logo, customer_support_ui_public_vite_v_mark, customer_support_ui_public_vite_lightning_bolt [INFERRED 0.95]
- **React Brand Mark** — customer_support_ui_src_assets_react_logo, customer_support_ui_src_assets_react_atom, customer_support_ui_src_assets_react_brand [INFERRED 0.95]

## Communities (118 total, 46 thin omitted)

### Community 0 - "jev.py"
Cohesion: 0.29
Nodes (8): build_order_check(), build_questions(), build_state(), category_criteria(), _input_tokens(), JevClassifier, _picks(), _priority()

### Community 1 - "guardrails.py"
Cohesion: 0.06
Nodes (58): Passage, Candidate, _add(), find_candidates(), normalize_phone(), _overlaps(), parse_amount(), resolve_date() (+50 more)

### Community 2 - "PipelineDeps"
Cohesion: 0.60
Nodes (5): build_graph(), PipelineDeps, test_run_batch_no_db_writes_summary_and_out(), fake_build(), pipeline()

### Community 3 - "test_llm.py"
Cohesion: 0.14
Nodes (11): GeminiStructuredLLM, make_gemini_llm(), _llm(), _S, test_draft_model_uses_millisecond_timeout_and_disables_sdk_retries(), test_openrouter_reported_cost_takes_precedence_over_token_estimate(), test_openrouter_retry_budget_is_bounded(), test_openrouter_structured_samples_use_configured_key_and_validate_output() (+3 more)

### Community 4 - "types.ts"
Cohesion: 0.08
Nodes (29): examples, previewResults, previewRuns, source, renderableTrace(), reviewEvidence(), plannedTools, stages (+21 more)

### Community 5 - "Shared UI States"
Cohesion: 0.21
Nodes (30): EmptyState(), ErrorState(), LoadingState(), PageHeader(), PriorityBadge(), StatusBadge(), CardHeader(), Table() (+22 more)

### Community 6 - "test_draft_tools.py"
Cohesion: 0.11
Nodes (30): IncidentRow, api(), ErrorEmbedder, settings(), test_all_eight_tools_and_seven_parallel_calls_execute_only_six(), test_context_copies_input_and_rejects_raising_hard_call_limit(), test_database_faults_remain_distinct_and_record_paid_search_cost(), test_discovered_ref_can_be_inspected_but_not_promoted_to_match() (+22 more)

### Community 7 - "Workspace Cards and Badges"
Cohesion: 0.19
Nodes (16): Confidence(), Metric(), Card(), CardContent(), CardTitle(), EvaluationPage(), readReport(), PipelineTrace() (+8 more)

### Community 8 - "build_pipeline"
Cohesion: 0.11
Nodes (21): SqlTransactionRepo, build_pipeline(), ConfigError, make_jev_client(), model_ids(), run_batch(), GeminiAnalysis, FakeStructuredLLM (+13 more)

### Community 9 - "DraftResult"
Cohesion: 0.13
Nodes (8): DraftResult, Drafter, NullDrafter, UnavailableDrafter, draft(), draft(), draft(), 2. Current implementation and integration points

### Community 10 - "lookup.py"
Cohesion: 0.16
Nodes (15): _as_date(), _iqd_amount(), match_transaction(), TransactionRepo, txn_from_dict(), _ex(), _match(), test_ambiguous_then_disambiguated_by_counterpart() (+7 more)

### Community 11 - "App and Database Bootstrap"
Cohesion: 0.14
Nodes (10): init_db(), make_engine(), make_sessionmaker(), reset_db(), upgrade_workspace_schema(), create_app(), lifespan(), ingest_env() (+2 more)

### Community 12 - "Dialogs and Pipeline Strip"
Cohesion: 0.16
Nodes (19): PipelineStrip(), ConfirmDialog(), FilterSelect(), statusLabels, Button(), Dialog(), DialogContent(), DialogDescription() (+11 more)

### Community 13 - "UI Package Metadata"
Cohesion: 0.11
Nodes (20): name, private, type, version, eslint, @eslint/js, eslint-plugin-react-hooks, eslint-plugin-react-refresh (+12 more)

### Community 14 - "test_draft_guardrails.py"
Cohesion: 0.13
Nodes (29): LookupResult, requests_credentials(), check(), state(), test_aggregation_is_deduplicated_and_has_no_state_side_effects(), test_amount_occurrences_keep_their_own_currency_and_sign(), test_avoid_sharing_warning_does_not_excuse_a_later_request(), test_candidate_prompt_limit_does_not_hide_later_ungrounded_references() (+21 more)

### Community 15 - "Support Taxonomy Categories"
Cohesion: 0.22
Nodes (21): lookup, Account KYC, Account & Security, Agent Dispute, Agent Network, App Bug, Bill Payment, Card Issue (+13 more)

### Community 16 - "shadcn Component Config"
Cohesion: 0.09
Nodes (21): aliases, components, hooks, lib, ui, utils, iconLibrary, menuAccent (+13 more)

### Community 17 - "Workspace Routes"
Cohesion: 0.17
Nodes (17): App(), EvaluationPage, InsightsPage, KnowledgePage, NewBatchPage, QueuePage, RunDetailPage, RunsPage (+9 more)

### Community 18 - "App TypeScript Config"
Cohesion: 0.09
Nodes (21): compilerOptions, allowArbitraryExtensions, allowImportingTsExtensions, erasableSyntaxOnly, jsx, lib, module, moduleDetection (+13 more)

### Community 19 - "Support CLI"
Cohesion: 0.14
Nodes (9): _command_settings(), ingest_kb_cmd(), init_db_cmd(), Mode, run_batch_cmd(), _run_in_memory(), seed_db_cmd(), _sessionmaker() (+1 more)

### Community 20 - "UploadedDocument"
Cohesion: 0.11
Nodes (14): delete_document(), download_document(), list_documents(), upload_document(), UploadedDocument, Base, SearchResult, document_filename() (+6 more)

### Community 21 - "Node TypeScript Config"
Cohesion: 0.12
Nodes (16): compilerOptions, allowImportingTsExtensions, erasableSyntaxOnly, lib, module, moduleDetection, noEmit, noFallthroughCasesInSwitch (+8 more)

### Community 23 - "UI Dev Dependencies"
Cohesion: 0.12
Nodes (16): devDependencies, eslint, @eslint/js, eslint-plugin-react-hooks, eslint-plugin-react-refresh, globals, prettier, prettier-plugin-tailwindcss (+8 more)

### Community 24 - "graph.py"
Cohesion: 0.17
Nodes (3): Ticket, _default_retry(), _retryable()

### Community 25 - "pytest"
Cohesion: 0.17
Nodes (35): answer(), call(), Checker, draft_state(), Knowledge, test_outer_timeout_retains_tool_owned_cost_and_cancelled_waiter_does_not_execute(), submit(), drafter() (+27 more)

### Community 26 - "UI Runtime Dependencies"
Cohesion: 0.15
Nodes (13): dependencies, @base-ui/react, class-variance-authority, cn, @fontsource-variable/geist, lucide-react, react, react-dom (+5 more)

### Community 27 - "Theme Provider"
Cohesion: 0.21
Nodes (11): disableTransitionsTemporarily(), getSystemTheme(), isEditableTarget(), isTheme(), ResolvedTheme, Theme, THEME_VALUES, ThemeProvider() (+3 more)

### Community 28 - "test_embeddings.py"
Cohesion: 0.09
Nodes (40): EmbeddingBatch, EmbeddingError, _nonnegative_number(), OpenRouterEmbedder, _ordered_vectors(), _response_cost(), embedder_for(), item() (+32 more)

### Community 29 - "Classify and Extract Prompts"
Cohesion: 0.31
Nodes (8): extract, gemini_classify, jev_classify, prepare, Gemini Classify Prompt v1, Gemini Extract Prompt v1, GeminiClassifier, JevClassifier

### Community 30 - "FakeJevRunnable"
Cohesion: 0.10
Nodes (28): CredentialCheck, DegradedCredentialChecker, _finite_nonnegative(), _get(), JevCredentialChecker, FakeJevRunnable, ResponseRunnable, test_bad_usage_cannot_poison_cost() (+20 more)

### Community 31 - "Pipeline Design Spec"
Cohesion: 0.25
Nodes (7): pgvector Postgres Service, pgdata Volume, Support Pipeline Design, Gemini 3.8 Flash, Jev, OpenRouter, ZainCash Support Pipeline

### Community 32 - "Workspace Plan Concepts"
Cohesion: 0.24
Nodes (8): Pipeline Graph Orchestration, Support Workspace HTML Shell, Support Workspace, Batch Runner, support CLI, Live Batch API, Support Workspace UI Plan, Plan 1 Live Smoke

### Community 33 - "Drafting Plan Concepts"
Cohesion: 0.25
Nodes (7): check_service_status, decide, draft, Plan 1 Part 2, Plan 1 Core Pipeline, Five-Plan Roadmap, Weekly Pattern Report

### Community 34 - "test_kb_service.py"
Cohesion: 0.09
Nodes (36): _abandoned(), _error_cost(), FakeEmbedder, GatedEmbedder, LateEmbedder, PaidEmbedder, count_chunks(), test_category_filters_include_general_policies_and_validate_tags() (+28 more)

### Community 35 - "Null Drafter Boundaries"
Cohesion: 0.25
Nodes (4): search_knowledge_base, Workspace NullDrafter Boundary, NullDrafter, NullDrafter

### Community 36 - "UI npm Scripts"
Cohesion: 0.25
Nodes (8): scripts, build, dev, format, lint, preview, test, typecheck

### Community 38 - "repository.py"
Cohesion: 0.05
Nodes (50): get_session(), get_result(), list_results(), review_result(), get_run(), list_runs(), start_run(), BatchInput (+42 more)

### Community 39 - "Vite Logo"
Cohesion: 0.40
Nodes (5): Iconify Logos, Yellow-to-Orange Lightning Bolt, Cyan-to-Purple V Mark, Vite, Vite Logo

### Community 40 - "ZainCash Mark"
Cohesion: 0.50
Nodes (5): Stacked Cash or Cards Motif, Crimson Rounded Square (#da3345), ZainCash Mark, Three Tilted White Rounded Bars, ZainCash

### Community 41 - "Root TypeScript Config"
Cohesion: 0.40
Nodes (4): compilerOptions, paths, files, references

### Community 42 - "Vite Config"
Cohesion: 0.40
Nodes (3): @tailwindcss/vite, vite, @vitejs/plugin-react

### Community 44 - "React Logo"
Cohesion: 0.67
Nodes (4): React Atom Mark, React, Iconify Logos, React Logo

### Community 46 - "KnowledgeService"
Cohesion: 0.10
Nodes (6): _check_deadline(), _Claim, _consume(), _DatabaseCall, IndexAttemptLostError, KnowledgeService

### Community 47 - "test_final_fix_handoff.py"
Cohesion: 0.11
Nodes (23): RagDrafter, DraftExecutionError, process_batch(), script(), assert_completed_evidence(), faulty_knowledge(), outer_deadlines(), PaidEmbeddings (+15 more)

### Community 48 - "support_test"
Cohesion: 0.12
Nodes (17): ingest(), index_deadlines(), settings(), support_test(), test_source_validation_sanitizes_name_preserves_bom_and_caller_transaction(), start(), Evidence by layer, Known limitations and remaining work (+9 more)

### Community 57 - "parse_document"
Cohesion: 0.09
Nodes (29): TextChunk, _append_chunks(), _check_extracted_size(), DocumentParseError, parse_document(), _parse_pdf(), make_pdf(), test_arabic_text_and_bom_are_preserved() (+21 more)

### Community 58 - "tools.py"
Cohesion: 0.13
Nodes (6): DraftAlreadySubmitted, DraftToolLimit, build_tools(), flag(), guarded(), invoke()

### Community 59 - "DraftContext"
Cohesion: 0.08
Nodes (9): _error_cost(), _Execution, _ModelUsage, _number(), DraftContext, _bounded(), visit(), _json() (+1 more)

### Community 60 - "SqlInvestigationRepo"
Cohesion: 0.16
Nodes (15): TransactionRow, TxnRecord, parse_dt(), DraftToolInputError, _datetime(), _days(), _field(), _involves() (+7 more)

### Community 61 - "NewBatchPage.tsx"
Cohesion: 0.15
Nodes (17): Badge(), badgeVariants, buttonVariants, Input(), Tabs(), TabsContent(), TabsList(), tabsListVariants (+9 more)

### Community 62 - "rules.py"
Cohesion: 0.21
Nodes (18): Decision, ExtractedField, decide(), empty_ticket_decision(), merge_reasons(), note_for(), _unique(), Category (+10 more)

### Community 63 - "extract.py"
Cohesion: 0.33
Nodes (10): FieldPick, finalize(), FakeExtractor, _setup(), test_fill_gaps_noop_and_failure_tolerant(), test_fill_gaps_only_asks_for_weak_required_fields(), test_gemini_span_not_in_text_is_null(), test_gemini_word_amount_uses_normalized_hint() (+2 more)

### Community 64 - "Settings"
Cohesion: 0.18
Nodes (7): Settings, test_defaults(), test_drafting_configuration_cannot_bypass_hard_limits(), test_drafting_limits_load_from_environment(), test_env_overrides(), test_legacy_gemini_model_names_are_qualified_for_openrouter(), test_openrouter_key_is_loaded_from_environment()

### Community 65 - "LLMUnavailable"
Cohesion: 0.24
Nodes (11): LLMUnavailable, combine(), merge_picks(), test_both_missing_raises(), test_cost_is_summed(), test_degraded_when_jev_missing(), test_disagreement_when_jev_was_partly_confident(), test_gemini_low_confidence() (+3 more)

### Community 66 - "test_cli.py"
Cohesion: 0.18
Nodes (9): test_config_error_exits_2(), boom(), test_ingest_directory_is_deterministic_and_duplicate_is_free(), test_ingest_disabled_configuration_never_calls_provider(), test_ingest_failure_exit_and_retry_stored(), test_ingest_invalid_source_does_not_stop_other_files(), test_ingest_limits_batch_without_partial_side_effects(), test_retry_stored_indexes_old_uploads_without_recovering_other_process_jobs() (+1 more)

### Community 67 - "Plan 3 — Knowledge retrieval and grounded reply drafting"
Cohesion: 0.11
Nodes (18): 10. Remaining demo roadmap, 1. Intent and acceptance criteria, 3. Provider and configuration, 4. Knowledge ingestion and persistence, 5. Retrieval and evidence, 6. Bounded investigation agent, 7. Draft guardrails and failure outcomes, 8. Pipeline, API, CLI and UI integration (+10 more)

### Community 68 - "make_ticket"
Cohesion: 0.28
Nodes (18): FakeClassifier, make_output(), make_ticket(), _deps(), _run(), test_cascade_confident_jev_skips_gemini(), test_cascade_degrades_when_jev_fails(), test_cascade_uncertain_jev_goes_to_gemini() (+10 more)

### Community 69 - "test_dbapi_commit_handoff_arbitrates_cancellation"
Cohesion: 0.47
Nodes (4): test_dbapi_commit_handoff_arbitrates_cancellation(), gate(), gate_before_dbapi(), gate_inside_dbapi()

### Community 70 - "tools.py"
Cohesion: 0.14
Nodes (11): DraftSubmission, retrieve(), _error_cost(), _Flag, _History, _Input, _Knowledge, _Lookup (+3 more)

### Community 72 - "taxonomy.py"
Cohesion: 0.16
Nodes (8): load_taxonomy(), most_urgent(), priority_rank(), TaxonomyError, tax(), taxonomy(), test_priority_helpers(), test_rejects_unknown_team()

### Community 73 - "extract.py"
Cohesion: 0.33
Nodes (8): Candidates, ClassifierOutput, NormalizedTicket, Classifier, FieldExtractor, _field(), fill_gaps(), _is_weak()

### Community 74 - "KnowledgePage.tsx"
Cohesion: 0.20
Nodes (10): BadgeLabel(), KnowledgePage(), deleteDocument(), Resource, api, loadQueue(), request(), sizeLabel() (+2 more)

### Community 75 - "test-kb/README.md"
Cohesion: 0.13
Nodes (7): توثيق الحساب — سياسة خيالية للعرض التجريبي, أعطال التطبيق — سياسة خيالية للعرض التجريبي, مشاكل البطاقة — سياسة خيالية للعرض التجريبي, التحويل المعلّق — سياسة خيالية للعرض التجريبي, تصعيد شبهة الاحتيال — سياسة خيالية للعرض التجريبي, استرجاع مبلغ شراء — سياسة خيالية للعرض التجريبي, التحويل لمستلم بالخطأ — سياسة خيالية للعرض التجريبي

### Community 76 - "factory.py"
Cohesion: 0.14
Nodes (8): Sample, StructuredLLM, ClassificationResult, GeminiClassifier, GeminiExtractor, verified_pick(), render_prompt(), Taxonomy

### Community 77 - "test_workspace_api.py"
Cohesion: 0.17
Nodes (8): InMemoryTransactionRepo, start_run(), test_batch_and_queue_expose_real_results(), test_batch_failure_is_isolated_and_conflicting_ids_rejected(), test_openrouter_credentials_enable_api_modes_without_exposing_keys(), test_progress_counts_only_durable_results_after_save_failure(), fail_one_save(), test_review_requires_text_and_rejects_stale_updates()

### Community 79 - "ingest.py"
Cohesion: 0.25
Nodes (8): load_jsonl(), load_tickets(), _rows(), test_csv_with_bom_and_missing_columns(), test_duplicate_external_ids_keep_first(), test_json_object_without_ids(), test_jsonl_fixture_loads(), test_unsupported_format()

### Community 80 - "judge-demo.ar.md"
Cohesion: 0.14
Nodes (13): أعطال التطبيق — سياسة خيالية للعرض التجريبي, استرجاع مبلغ شراء — سياسة خيالية للعرض التجريبي, استعادة الدخول — سياسة خيالية للعرض التجريبي, الاستفسار الآمن من الدعم — سياسة خيالية للعرض التجريبي, الاستفسار المؤقت للدعم في المهمة ٨ — سياسة خيالية للعرض التجريبي, التحويل المعلّق — سياسة خيالية للعرض التجريبي, التحويل لمستلم بالخطأ — سياسة خيالية للعرض التجريبي, الطلبات غير الواضحة وخارج النطاق — سياسة خيالية للعرض التجريبي (+5 more)

### Community 96 - "test_draft_model.py"
Cohesion: 0.27
Nodes (8): make_draft_model(), response_payload(), run_provider_pipeline(), send(), search_response(), test_empty_choices_escalates_and_keeps_paid_response_usage(), test_failed_response_id_is_deduplicated_against_earlier_success(), test_other_conversion_value_errors_remain_unexpected()

### Community 97 - "KnowledgeError"
Cohesion: 0.20
Nodes (3): DocumentNotFoundError, KnowledgeError, KnowledgeExecutionError

### Community 98 - "Plan 3 RAG Drafting Implementation Plan"
Cohesion: 0.20
Nodes (10): Completion and review record — 2026-10-17, Execution handoff, File map and shared interfaces, Global Constraints, Plan 3 RAG Drafting Implementation Plan, Plan self-review, Review Focus, Task 6: API/CLI indexing and persisted citation projection (+2 more)

### Community 99 - "test_db_deadline_is_cumulative_across_publication_statements"
Cohesion: 0.29
Nodes (3): test_db_deadline_cancelled_publication_cannot_commit_late(), test_db_deadline_is_cumulative_across_publication_statements(), changed_index()

### Community 100 - "قواعد المعرفة العربية للعرض أمام لجنة التحكيم"
Cohesion: 0.33
Nodes (6): الأصل ونتيجة التحقق, توليد مسودة ومراجعتها, خريطة الملفات وأسئلة العرض, خطوات الرفع والفهرسة والبحث أمام اللجنة, قواعد المعرفة العربية للعرض أمام لجنة التحكيم, ماذا أرفع؟

## Ambiguous Edges - Review These
- `Fraud Report` → `Plan 1 Live Smoke`  [AMBIGUOUS]
  README.md · relation: conceptually_related_to
- `Stacked Cash or Cards Motif` → `Three Tilted White Rounded Bars`  [AMBIGUOUS]
  customer-support-ui/public/zaincash-mark.svg · relation: conceptually_related_to

## Knowledge Gaps
- **31 isolated node(s):** `@fontsource-variable/geist`, `prettier`, `prettier-plugin-tailwindcss`, `shadcn`, `tailwindcss` (+26 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 562 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **46 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Artifacts, servers and remaining concerns` connect `support_test` to `repository.py`?**
  _High betweenness centrality (0.201) - this node is a cross-community bridge._
- **Are the 13 inferred relationships involving `KnowledgeService` (e.g. with `RagDrafter` and `build_tools()`) actually correct?**
  _`KnowledgeService` has 13 INFERRED edges - model-reasoned connections that need verification._
- **What connects `@fontsource-variable/geist`, `prettier`, `prettier-plugin-tailwindcss` to the rest of the system?**
  _31 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `guardrails.py` be split into smaller, more focused modules?**
  _Cohesion score 0.05823293172690763 - nodes in this community are weakly interconnected._
- **Why does `start()` connect `support_test` to `NewBatchPage.tsx`?**
  _High betweenness centrality (0.200) - this node is a cross-community bridge._

### Low-confidence Hints
_AMBIGUOUS edges — the extractor was unsure. Verify before acting on these._

- **What is the exact relationship between `Fraud Report` and `Plan 1 Live Smoke`?**
  _Edge tagged AMBIGUOUS (relation: conceptually_related_to) - confidence is low._
- **What is the exact relationship between `Stacked Cash or Cards Motif` and `Three Tilted White Rounded Bars`?**
  _Edge tagged AMBIGUOUS (relation: conceptually_related_to) - confidence is low._