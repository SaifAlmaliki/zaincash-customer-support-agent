# Graph Report - zaincash-support  (2026-10-25)

## Corpus Check
- 296 files · ~244,591 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 30 file(s) not represented in the graph (top: (none) 18, .jsonl 4, .css 4)

## Summary
- 2965 nodes · 9137 edges · 163 communities (121 shown, 42 thin omitted)
- Extraction: 89% EXTRACTED · 11% INFERRED · 0% AMBIGUOUS · INFERRED: 1022 edges (avg confidence: 0.92)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `cb0d2800`
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
- test_credential_check.py
- test_rag_api.py
- employee-frontend/package.json
- test_draft_guardrails.py
- Support Taxonomy Categories
- ui/package.json
- employee-frontend/src/App.tsx
- users-frontend/package.json
- datetime
- UploadedDocument
- web/package.json
- test_cli.py
- compilerOptions
- employee-frontend/components.json
- test_workspace_api.py
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
- db/repository.py
- ui/components.json
- main.py
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
- investigation.py
- intake/repository.py
- guardrails.py
- NewBatchPage.tsx
- lookup.py
- test_llm.py
- tasks
- PipelineTrace.tsx
- IntakePage.tsx
- test_handoff.py
- make_output
- _DatabaseCall
- PipelineState
- intake/contracts.py
- factory.py
- Credentials
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
- cli.py
- RagDrafter
- useCopy
- compilerOptions
- قواعد المعرفة العربية للعرض أمام لجنة التحكيم
- pydantic
- dependencies
- attachments.py
- dependencies
- compilerOptions
- tools.py
- controller.test.ts
- AttachmentStore
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
- build_tools
- scripts
- users-frontend/README.md
- context
- TurnContext
- test_attachments.py
- DraftResult
- InvalidEvidence
- build_pipeline
- ar/app_bug.md
- intake/model.py
- Customer Conversation Intake Implementation Plan
- intake.py
- test_final_fix_handoff.py
- Synthetic demo readiness
- test_recovery_regressions.py
- ar/bill_payment.md
- intake/conftest.py
- ar/card_issue.md
- intake/api.ts
- ingest.py
- test_dbapi_commit_handoff_arbitrates_cancellation
- ar/fraud_report.md
- ar/general_inquiry.md
- @testing-library/react
- FakeJevRunnable
- test_draft_model.py
- ar/login_access.md
- intake/README.md
- TicketInput
- ar/refund_request.md
- ar/failed_transfer.md
- Plan 3 RAG Drafting Implementation Plan
- IntakePage.test.tsx
- employee-frontend/src/components/theme-provider.tsx
- errors.py
- test_rules.py
- ref_vitest
- Ticket flow charts
- Customer intake chat layout
- IndexJobs

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

## Communities (163 total, 42 thin omitted)

### Community 0 - "fakes.py"
Cohesion: 0.09
Nodes (14): LLMUnavailable, Sample, combine(), merge_picks(), DraftChatOpenRouter, DraftProviderResponseError, test_both_missing_raises(), test_cost_is_summed() (+6 more)

### Community 1 - "intake/types.ts"
Cohesion: 0.11
Nodes (23): IntakeApi, ControllerState, emptyState(), fileIdentity(), factText(), Attachment, Credentials, CustomerReview (+15 more)

### Community 2 - "test_rag_drafter.py"
Cohesion: 0.20
Nodes (35): test_contracts_reject_extra_keys(), test_datetimes_must_be_timezone_aware(), answer(), call(), draft_state(), script(), submit(), submit() (+27 more)

### Community 3 - "TurnStore"
Cohesion: 0.20
Nodes (9): OperationClaim, TurnResult, RevisionConflict, sanitize_intake_text(), _jsonable(), TurnStore, test_recovered_attempt_cannot_publish_stale_output(), test_review_publication_revision_matches_the_session() (+1 more)

### Community 4 - "TicketReviewPage.tsx"
Cohesion: 0.16
Nodes (19): Input(), reviewerNote(), Resource, api, ChunkPage, Health, Insights, IntakeFact (+11 more)

### Community 5 - "InvalidEvidence"
Cohesion: 0.16
Nodes (16): canonical_digits(), normalize_reported_date(), InvalidEvidence, _apply(), _check_reference(), _compact(), checked_update(), _newer_correction() (+8 more)

### Community 6 - "QueuePage.tsx"
Cohesion: 0.19
Nodes (31): EmptyState(), ErrorState(), LoadingState(), PageHeader(), PriorityBadge(), StatusBadge(), Table(), TableBody() (+23 more)

### Community 7 - "Customer conversation intake for ZainCash support"
Cohesion: 0.06
Nodes (31): 10. Verification and acceptance criteria, 11. Delivery and review, 1. Outcome and agreed requirements, 2. Current implementation and integration points, 3. Approach and boundaries, 4. Conversation state and turn flow, 5. Facts, evidence, and readiness, 6. Language and screenshot behavior (+23 more)

### Community 8 - "workspace-ui.tsx"
Cohesion: 0.15
Nodes (18): ConfirmDialog(), FilterSelect(), Button(), buttonVariants, Dialog(), DialogContent(), DialogDescription(), DialogFooter() (+10 more)

### Community 9 - "IntakeController"
Cohesion: 0.20
Nodes (5): IntakeController, isConflict(), isOffline(), safeMessage(), Language

### Community 10 - "test_credential_check.py"
Cohesion: 0.10
Nodes (19): CredentialCheck, CredentialChecker, DegradedCredentialChecker, _finite_nonnegative(), _get(), JevCredentialChecker, ResponseRunnable, test_bad_usage_cannot_poison_cost() (+11 more)

### Community 11 - "test_rag_api.py"
Cohesion: 0.13
Nodes (20): create_app(), client(), evidence_client(), test_actual_guardrail_failure_is_separate_from_reply(), test_concurrent_index_requests_share_active_work(), test_disabled_or_missing_provider_stores_without_indexing(), test_explicit_retry_tags_search_and_chunk_pagination(), test_health_distinguishes_failed_from_empty() (+12 more)

### Community 12 - "employee-frontend/package.json"
Cohesion: 0.06
Nodes (30): @base-ui/react, class-variance-authority, cn, eslint, @eslint/js, eslint-plugin-react-hooks, eslint-plugin-react-refresh, @fontsource/tajawal (+22 more)

### Community 14 - "test_draft_guardrails.py"
Cohesion: 0.14
Nodes (29): LookupResult, check_draft(), requests_credentials(), make_ticket(), check(), state(), test_aggregation_is_deduplicated_and_has_no_state_side_effects(), test_amount_occurrences_keep_their_own_currency_and_sign() (+21 more)

### Community 15 - "Support Taxonomy Categories"
Cohesion: 0.21
Nodes (22): lookup, Account KYC, Account & Security, Agent Dispute, Agent Network, App Bug, Bill Payment, Card Issue (+14 more)

### Community 16 - "ui/package.json"
Cohesion: 0.07
Nodes (29): @turbo/gen, zod, @base-ui/react, class-variance-authority, cn, eslint, @eslint/js, eslint-plugin-react-hooks (+21 more)

### Community 17 - "employee-frontend/src/App.tsx"
Cohesion: 0.17
Nodes (17): App(), EvaluationPage, InsightsPage, KnowledgePage, NewBatchPage, QueuePage, RunDetailPage, RunsPage (+9 more)

### Community 18 - "users-frontend/package.json"
Cohesion: 0.09
Nodes (22): turbo, devDependencies, prettier, prettier-plugin-tailwindcss, turbo, typescript, engines, node (+14 more)

### Community 19 - "datetime"
Cohesion: 0.09
Nodes (20): get_session(), get_result(), list_results(), read_intake_attachment(), review_result(), ReviewInput, health(), insights() (+12 more)

### Community 20 - "UploadedDocument"
Cohesion: 0.11
Nodes (23): delete_document(), download_document(), index_document(), list_chunks(), list_documents(), _require_provider(), search_knowledge(), upload_document() (+15 more)

### Community 21 - "web/package.json"
Cohesion: 0.08
Nodes (25): jsdom, @testing-library/user-event, @workspace/ui, eslint, @eslint/js, eslint-plugin-react-hooks, eslint-plugin-react-refresh, globals (+17 more)

### Community 22 - "test_cli.py"
Cohesion: 0.18
Nodes (9): test_config_error_exits_2(), boom(), test_ingest_directory_is_deterministic_and_duplicate_is_free(), test_ingest_disabled_configuration_never_calls_provider(), test_ingest_failure_exit_and_retry_stored(), test_ingest_invalid_source_does_not_stop_other_files(), test_ingest_limits_batch_without_partial_side_effects(), test_retry_stored_indexes_old_uploads_without_recovering_other_process_jobs() (+1 more)

### Community 23 - "compilerOptions"
Cohesion: 0.08
Nodes (23): compilerOptions, allowArbitraryExtensions, allowImportingTsExtensions, erasableSyntaxOnly, jsx, lib, module, moduleDetection (+15 more)

### Community 24 - "employee-frontend/components.json"
Cohesion: 0.09
Nodes (21): aliases, components, hooks, lib, ui, utils, iconLibrary, menuAccent (+13 more)

### Community 25 - "test_workspace_api.py"
Cohesion: 0.11
Nodes (16): build_graph(), PipelineDeps, InMemoryTransactionRepo, pipeline(), taxonomy(), test_run_batch_no_db_writes_summary_and_out(), fake_build(), client() (+8 more)

### Community 26 - "compilerOptions"
Cohesion: 0.09
Nodes (22): compilerOptions, allowArbitraryExtensions, allowImportingTsExtensions, erasableSyntaxOnly, jsx, lib, module, moduleDetection (+14 more)

### Community 27 - "web/src/components/theme-provider.tsx"
Cohesion: 0.17
Nodes (12): App(), disableTransitionsTemporarily(), getSystemTheme(), isEditableTarget(), isTheme(), ResolvedTheme, Theme, THEME_VALUES (+4 more)

### Community 28 - "test_embeddings.py"
Cohesion: 0.08
Nodes (42): EmbeddingBatch, EmbeddingError, _nonnegative_number(), OpenRouterEmbedder, _ordered_vectors(), _response_cost(), Embeddings, test_lock_serializes_operations_and_submit_waits_for_inflight_search() (+34 more)

### Community 29 - "Classify and Extract Prompts"
Cohesion: 0.31
Nodes (9): extract, gemini_classify, Pipeline Graph Orchestration, jev_classify, prepare, Gemini Classify Prompt v1, Gemini Extract Prompt v1, GeminiClassifier (+1 more)

### Community 30 - "test_draft_tools.py"
Cohesion: 0.12
Nodes (31): IncidentRow, TicketRow, TransactionRow, api(), ErrorEmbedder, settings(), test_all_eight_tools_and_seven_parallel_calls_execute_only_six(), test_context_copies_input_and_rejects_raising_hard_call_limit() (+23 more)

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
Nodes (38): Embedder, KnowledgeService, FakeEmbedder, GatedEmbedder, LateEmbedder, PaidEmbedder, count_chunks(), settings() (+30 more)

### Community 36 - "web/components.json"
Cohesion: 0.10
Nodes (19): aliases, components, hooks, lib, ui, utils, iconLibrary, menuAccent (+11 more)

### Community 38 - "db/repository.py"
Cohesion: 0.10
Nodes (24): finish_run(), load_incidents(), load_transactions(), save_outcomes(), SqlTransactionRepo, _to_record(), _upsert(), upsert_tickets() (+16 more)

### Community 39 - "ui/components.json"
Cohesion: 0.10
Nodes (19): aliases, components, hooks, lib, ui, utils, iconLibrary, menuAccent (+11 more)

### Community 40 - "main.py"
Cohesion: 0.11
Nodes (21): _safe_dispatch(), get_run(), list_runs(), start_run(), RunRow, create_run(), recover(), model_ids() (+13 more)

### Community 41 - "fact"
Cohesion: 0.17
Nodes (44): Analysis, EvidenceRef, Fact, merge_analysis(), context(), fact(), image_evidence(), message() (+36 more)

### Community 43 - "Human Review Gate"
Cohesion: 0.25
Nodes (4): support CLI, Support Workspace UI Plan, Review API, Workspace UI Verification

### Community 44 - "compilerOptions"
Cohesion: 0.12
Nodes (16): compilerOptions, allowImportingTsExtensions, erasableSyntaxOnly, lib, module, moduleDetection, noEmit, noFallthroughCasesInSwitch (+8 more)

### Community 46 - "agent.py"
Cohesion: 0.12
Nodes (3): _error_cost(), _number(), DraftToolLimit

### Community 47 - "compilerOptions"
Cohesion: 0.12
Nodes (16): compilerOptions, allowImportingTsExtensions, erasableSyntaxOnly, lib, module, moduleDetection, noEmit, noFallthroughCasesInSwitch (+8 more)

### Community 48 - "support_test"
Cohesion: 0.13
Nodes (16): index_deadlines(), support_test(), Citation IDs and provider evidence, Commands and automated verification — historical Task 8, Corpus and actual retrieval, Current final verification and review closure, Environment and isolation, Live browser and persistence evidence (+8 more)

### Community 57 - "parse_document"
Cohesion: 0.10
Nodes (30): TextChunk, _append_chunks(), _check_extracted_size(), DocumentParseError, parse_document(), _parse_pdf(), make_pdf(), test_arabic_text_and_bom_are_preserved() (+22 more)

### Community 58 - "investigation.py"
Cohesion: 0.17
Nodes (13): parse_dt(), DraftToolInputError, _datetime(), _days(), _field(), _involves(), _phone(), _phones() (+5 more)

### Community 59 - "intake/repository.py"
Cohesion: 0.19
Nodes (18): CustomerReview, Receipt, ReviewSnapshot, IntakeAttachmentRow, IntakeOperationRow, _attachment(), customer_review(), initial_state() (+10 more)

### Community 60 - "guardrails.py"
Cohesion: 0.06
Nodes (56): Candidate, _add(), find_candidates(), normalize_phone(), _overlaps(), parse_amount(), resolve_date(), _safe_date() (+48 more)

### Community 61 - "NewBatchPage.tsx"
Cohesion: 0.12
Nodes (15): Tabs(), TabsContent(), TabsList(), tabsListVariants, TabsTrigger(), Textarea(), readReport(), exampleTickets (+7 more)

### Community 62 - "lookup.py"
Cohesion: 0.18
Nodes (16): ExtractedField, TxnRecord, _as_date(), _iqd_amount(), match_transaction(), TransactionRepo, _ex(), _match() (+8 more)

### Community 63 - "test_llm.py"
Cohesion: 0.13
Nodes (11): GeminiStructuredLLM, make_gemini_llm(), _llm(), _S, test_draft_model_uses_millisecond_timeout_and_disables_sdk_retries(), test_openrouter_reported_cost_takes_precedence_over_token_estimate(), test_openrouter_retry_budget_is_bounded(), test_openrouter_structured_samples_use_configured_key_and_validate_output() (+3 more)

### Community 64 - "tasks"
Cohesion: 0.12
Nodes (16): dependsOn, inputs, outputs, cache, persistent, dependsOn, dependsOn, $schema (+8 more)

### Community 65 - "PipelineTrace.tsx"
Cohesion: 0.09
Nodes (46): Task 3: Received, produced, and drafting events, 2. Scope, 6. How a result becomes the charts, Confidence(), Metric(), Badge(), badgeVariants, Card() (+38 more)

### Community 66 - "IntakePage.tsx"
Cohesion: 0.14
Nodes (19): Global Constraints, Intake Chat UI Implementation Plan, Task 1: Put the summary and receipt in the thread, Task 2: Put screenshots inside the composer, Task 3: Apply the workspace chat styles, Task 4: Check the page in the browser, 4. Components, ChatTranscript() (+11 more)

### Community 67 - "test_handoff.py"
Cohesion: 0.36
Nodes (7): complete_conversation(), _dated(), _message(), _opening(), _png(), _review(), _user()

### Community 68 - "make_output"
Cohesion: 0.28
Nodes (17): FakeClassifier, make_output(), _deps(), _run(), test_cascade_confident_jev_skips_gemini(), test_cascade_degrades_when_jev_fails(), test_cascade_uncertain_jev_goes_to_gemini(), test_concurrency_is_limited() (+9 more)

### Community 69 - "_DatabaseCall"
Cohesion: 0.07
Nodes (11): SearchResult, _abandoned(), _check_deadline(), _Claim, _consume(), _DatabaseCall, DocumentNotFoundError, _error_cost() (+3 more)

### Community 70 - "PipelineState"
Cohesion: 0.18
Nodes (10): _Nodes, PipelineState, Global Constraints, Task 1: Sentence catalog, Task 2: Which step is open, Task 4: Mermaid source, Task 5: Draw the charts on the ticket page, Ticket Flow Charts Implementation Plan (+2 more)

### Community 71 - "intake/contracts.py"
Cohesion: 0.15
Nodes (8): Attachment, _aware(), IntakeModel, IntakeState, Message, grounded_analysis(), grounded_review(), ScriptedIntakeModel

### Community 72 - "factory.py"
Cohesion: 0.11
Nodes (17): Decision, decide(), empty_ticket_decision(), merge_reasons(), note_for(), _unique(), Category, load_taxonomy() (+9 more)

### Community 73 - "Credentials"
Cohesion: 0.18
Nodes (7): Credentials, SessionView, IntakeService, _payload(), test_concurrent_submit_dispatches_once(), test_second_request_id_reuses_the_approved_review(), test_submission_replay_creates_one_ticket()

### Community 74 - "use-knowledge-library.ts"
Cohesion: 0.19
Nodes (17): ingest(), Artifacts, servers and remaining concerns, acceptIndexRequest(), canRequestIndex(), PendingIndexes, persistPendingIndexes(), pollKnowledge(), refresh() (+9 more)

### Community 75 - "test-kb/README.md"
Cohesion: 0.15
Nodes (6): Fictional RAG walkthrough inputs, توثيق الحساب — سياسة خيالية للعرض التجريبي, نزاع مع وكيل — سياسة خيالية للعرض التجريبي, الطلبات غير الواضحة وخارج النطاق — سياسة خيالية للعرض التجريبي, الاستفسار المؤقت للدعم في المهمة ٨ — سياسة خيالية للعرض التجريبي, التحويل لمستلم بالخطأ — سياسة خيالية للعرض التجريبي

### Community 76 - "Plan 3 — Knowledge retrieval and grounded reply drafting"
Cohesion: 0.11
Nodes (18): 10. Remaining demo roadmap, 1. Intent and acceptance criteria, 3. Provider and configuration, 4. Knowledge ingestion and persistence, 5. Retrieval and evidence, 6. Bounded investigation agent, 7. Draft guardrails and failure outcomes, 8. Pipeline, API, CLI and UI integration (+10 more)

### Community 77 - "KnowledgePage"
Cohesion: 0.57
Nodes (7): BadgeLabel(), KnowledgePage(), beginMutation(), deleteDocument(), finishMutation(), indexDocument(), upload()

### Community 79 - "devDependencies"
Cohesion: 0.12
Nodes (16): devDependencies, eslint, @eslint/js, eslint-plugin-react-hooks, eslint-plugin-react-refresh, globals, prettier, prettier-plugin-tailwindcss (+8 more)

### Community 80 - "judge-demo.ar.md"
Cohesion: 0.14
Nodes (13): أعطال التطبيق — سياسة خيالية للعرض التجريبي, استرجاع مبلغ شراء — سياسة خيالية للعرض التجريبي, استعادة الدخول — سياسة خيالية للعرض التجريبي, الاستفسار الآمن من الدعم — سياسة خيالية للعرض التجريبي, الاستفسار المؤقت للدعم في المهمة ٨ — سياسة خيالية للعرض التجريبي, التحويل المعلّق — سياسة خيالية للعرض التجريبي, التحويل لمستلم بالخطأ — سياسة خيالية للعرض التجريبي, الطلبات غير الواضحة وخارج النطاق — سياسة خيالية للعرض التجريبي (+5 more)

### Community 93 - "agent.py"
Cohesion: 0.10
Nodes (33): StructuredLLM, Candidates, ClassificationResult, ClassifierOutput, FieldPick, NormalizedTicket, Classifier, FieldExtractor (+25 more)

### Community 94 - "devDependencies"
Cohesion: 0.11
Nodes (19): devDependencies, eslint, @eslint/js, eslint-plugin-react-hooks, eslint-plugin-react-refresh, globals, jsdom, @tailwindcss/vite (+11 more)

### Community 95 - "devDependencies"
Cohesion: 0.14
Nodes (14): devDependencies, eslint, @eslint/js, eslint-plugin-react-hooks, eslint-plugin-react-refresh, globals, tailwindcss, @tailwindcss/vite (+6 more)

### Community 96 - "cli.py"
Cohesion: 0.17
Nodes (13): _command_settings(), ingest_kb_cmd(), init_db_cmd(), Mode, run_batch_cmd(), _run_in_memory(), _run_with_db(), seed_db_cmd() (+5 more)

### Community 97 - "RagDrafter"
Cohesion: 0.17
Nodes (3): _Execution, _ModelUsage, DraftContext

### Community 98 - "useCopy"
Cohesion: 0.16
Nodes (16): LanguageToggle(), intakeFixture, factValue(), IntakeEvidence(), Screenshot(), applyDocumentLocale(), copies, Copy (+8 more)

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
Cohesion: 0.14
Nodes (14): dependencies, @base-ui/react, class-variance-authority, cn, @fontsource/tajawal, @fontsource-variable/plus-jakarta-sans, lucide-react, react (+6 more)

### Community 103 - "attachments.py"
Cohesion: 0.15
Nodes (11): _display_name(), IntakeMessageRow, IntakeSessionRow, assert_same_operation(), new_access_token(), operation_fingerprint(), repo(), test_changed_payload_cannot_reuse_operation_identity() (+3 more)

### Community 104 - "dependencies"
Cohesion: 0.15
Nodes (13): dependencies, @base-ui/react, class-variance-authority, cn, @fontsource/tajawal, @fontsource-variable/plus-jakarta-sans, @hugeicons/core-free-icons, @hugeicons/react (+5 more)

### Community 105 - "compilerOptions"
Cohesion: 0.17
Nodes (11): compilerOptions, jsx, lib, module, moduleResolution, outDir, skipLibCheck, strict (+3 more)

### Community 106 - "tools.py"
Cohesion: 0.14
Nodes (11): DraftSubmission, retrieve(), _error_cost(), _Flag, _History, _Input, _Knowledge, _Lookup (+3 more)

### Community 107 - "controller.test.ts"
Cohesion: 0.21
Nodes (7): controller, emptySession(), fakeApi(), review, browserSessionStorage(), SessionStorage, SavedSession

### Community 108 - "AttachmentStore"
Cohesion: 0.14
Nodes (6): AttachmentStore, IntakeRepository, make_intake_service(), builder(), repo(), store()

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
Cohesion: 0.11
Nodes (10): Settings, test_blank_intake_model_is_rejected(), test_non_positive_image_limit_is_rejected(), test_relative_upload_directory_is_rooted_in_the_repository(), test_defaults(), test_drafting_configuration_cannot_bypass_hard_limits(), test_drafting_limits_load_from_environment(), test_env_overrides() (+2 more)

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

### Community 119 - "build_tools"
Cohesion: 0.11
Nodes (9): DraftAlreadySubmitted, _bounded(), visit(), build_tools(), flag(), guarded(), invoke(), status() (+1 more)

### Community 120 - "scripts"
Cohesion: 0.50
Nodes (4): scripts, format, lint, typecheck

### Community 122 - "context"
Cohesion: 0.22
Nodes (16): Question, Readiness, _asked_already(), asks_for_secret(), assess_readiness(), _can_ask(), canonical_category(), choose_question() (+8 more)

### Community 123 - "TurnContext"
Cohesion: 0.22
Nodes (5): QuestionRecord, TurnContext, IntakeGraph, _invitation(), Shared contracts (implement in Task 1; extend only through explicit edits here)

### Community 124 - "test_attachments.py"
Cohesion: 0.20
Nodes (14): ImageRejected, NotOwned, png_bytes(), test_active_turn_rejects_upload(), test_changed_invalid_bytes_conflict_before_decoding_replay(), test_concurrent_uploads_stop_at_the_session_cap(), attempt(), test_cross_session_read_and_removal() (+6 more)

### Community 125 - "DraftResult"
Cohesion: 0.15
Nodes (8): DraftResult, Drafter, NullDrafter, UnavailableDrafter, draft(), draft(), draft(), 2. Current implementation and integration points

### Community 126 - "InvalidEvidence"
Cohesion: 0.19
Nodes (14): ReviewText, build_review(), _compact(), _render_value(), _ticket_text(), _tokens(), validate_review_numbers(), review() (+6 more)

### Community 127 - "build_pipeline"
Cohesion: 0.14
Nodes (19): build_pipeline(), ConfigError, make_jev_client(), run_batch(), GeminiAnalysis, FakeStructuredLLM, ScriptedChat, _settings() (+11 more)

### Community 129 - "intake/model.py"
Cohesion: 0.11
Nodes (27): ImageInput, ModelCall, ModelUnavailable, _analysis_prompt(), _bounded_context(), _guard_size(), ModelBudget, OpenRouterIntakeModel (+19 more)

### Community 130 - "Customer Conversation Intake Implementation Plan"
Cohesion: 0.20
Nodes (8): Completion audit — 2026-10-18, Customer Conversation Intake Implementation Plan, Execution conventions and repository baseline, File map and dependency order, Global Constraints, Plan review and execution handoff, Review Focus, Spec coverage and acceptance map

### Community 131 - "intake.py"
Cohesion: 0.16
Nodes (19): create_session(), _credentials(), _dump(), get_session(), post_message(), read_attachment(), remove_attachment(), request_review() (+11 more)

### Community 132 - "test_final_fix_handoff.py"
Cohesion: 0.09
Nodes (26): Passage, RagDrafter, DraftExecutionError, Checker, Knowledge, assert_completed_evidence(), faulty_knowledge(), read() (+18 more)

### Community 133 - "Synthetic demo readiness"
Cohesion: 0.50
Nodes (4): Evidence by layer, Known limitations and remaining work, Repeatable local walkthrough, Synthetic demo readiness

### Community 134 - "test_recovery_regressions.py"
Cohesion: 0.22
Nodes (12): command(), create(), test_actual_app_restart_reconciles_failed_placeholder(), test_failed_review_retry_cannot_reopen_submitted_session(), test_original_payload_identity_survives_sanitization(), test_publication_failure_is_retryable_without_restart(), fail_once(), test_receipt_reference_is_preserved() (+4 more)

### Community 136 - "intake/conftest.py"
Cohesion: 0.13
Nodes (15): init_db(), make_engine(), make_sessionmaker(), reset_db(), upgrade_workspace_schema(), lifespan(), intake_client(), intake_db() (+7 more)

### Community 138 - "intake/api.ts"
Cohesion: 0.15
Nodes (13): createIntakeApi(), IntakeRequestError, isRecord(), parseJson(), parseReceipt(), parseSession(), readError(), stringList() (+5 more)

### Community 139 - "ingest.py"
Cohesion: 0.15
Nodes (12): load_jsonl(), load_tickets(), _rows(), outcome_to_dict(), outcome_to_row(), test_csv_with_bom_and_missing_columns(), test_duplicate_external_ids_keep_first(), test_json_object_without_ids() (+4 more)

### Community 140 - "test_dbapi_commit_handoff_arbitrates_cancellation"
Cohesion: 0.47
Nodes (4): test_dbapi_commit_handoff_arbitrates_cancellation(), gate(), gate_before_dbapi(), gate_inside_dbapi()

### Community 144 - "FakeJevRunnable"
Cohesion: 0.32
Nodes (10): FakeJevRunnable, _criteria(), _run(), test_low_top_probability_is_uncertain(), test_one_main_call_with_all_questions(), test_order_check_uses_reversed_options(), test_order_disagreement_is_uncertain(), test_priority_level_maps_to_p_label() (+2 more)

### Community 148 - "test_draft_model.py"
Cohesion: 0.27
Nodes (8): make_draft_model(), response_payload(), run_provider_pipeline(), send(), search_response(), test_empty_choices_escalates_and_keeps_paid_response_usage(), test_failed_response_id_is_deduplicated_against_earlier_success(), test_other_conversion_value_errors_remain_unexpected()

### Community 151 - "TicketInput"
Cohesion: 0.21
Nodes (4): BatchInput, KnowledgeIndexInput, KnowledgeSearchInput, TicketInput

### Community 154 - "Plan 3 RAG Drafting Implementation Plan"
Cohesion: 0.15
Nodes (12): Completion and review record — 2026-10-17, Execution handoff, File map and shared interfaces, Global Constraints, Plan 3 RAG Drafting Implementation Plan, Plan self-review, Review Focus, Task 3: Ticket-scoped investigation and all eight tools (+4 more)

### Community 155 - "IntakePage.test.tsx"
Cohesion: 0.26
Nodes (10): Task 6: Customer API client and resumable UI state, Task 7: Bilingual customer chat, screenshots and reviewed submission, copy(), attachment, collectingController(), emptySession(), fakeApi(), readyController() (+2 more)

### Community 156 - "employee-frontend/src/components/theme-provider.tsx"
Cohesion: 0.21
Nodes (11): disableTransitionsTemporarily(), getSystemTheme(), isEditableTarget(), isTheme(), ResolvedTheme, Theme, THEME_VALUES, ThemeProvider() (+3 more)

### Community 157 - "errors.py"
Cohesion: 0.33
Nodes (6): IntakeError, OperationConflict, StaleReview, TurnBusy, HTTP contract (implemented in Tasks 4–5), Task 1: Durable intake sessions and ownership

### Community 158 - "test_rules.py"
Cohesion: 0.42
Nodes (8): _decide(), _ex(), test_classifier_reasons_come_first(), test_clean_ticket_not_escalated(), test_fraud_flag_forces_p1_and_escalates(), test_lookup_reason_mapping(), test_missing_required_fields_unless_matched(), test_money_lost_raises_to_p2_and_min_priority_applies()

### Community 159 - "ref_vitest"
Cohesion: 0.33
Nodes (3): Task 8: Employee evidence panel and processing state, canReview(), REVIEWABLE

### Community 160 - "Ticket flow charts"
Cohesion: 0.29
Nodes (6): 1. Outcome, 5. Language, 7. Sentences, 8. Tests, 9. Files, Ticket flow charts

### Community 161 - "Customer intake chat layout"
Cohesion: 0.33
Nodes (5): 1. Outcome, 2. Scope, 3. Layout, 5. Checks, Customer intake chat layout

## Ambiguous Edges - Review These
- `Fraud Report` → `Plan 1 Live Smoke`  [AMBIGUOUS]
  README.md · relation: conceptually_related_to

## Knowledge Gaps
- **90 isolated node(s):** `zaincash-support`, `@base-ui/react`, `@fontsource-variable/plus-jakarta-sans`, `@fontsource/tajawal`, `@tailwindcss/vite` (+85 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 986 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **42 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `HTTP contract (implemented in Tasks 4–5)` connect `errors.py` to `intake/model.py`, `Customer Conversation Intake Implementation Plan`, `TurnStore`, `main.py`, `intake/conftest.py`, `IntakePage.test.tsx`, `guardrails.py`, `ref_vitest`?**
  _High betweenness centrality (0.110) - this node is a cross-community bridge._
- **Are the 33 inferred relationships involving `Settings` (e.g. with `_command_settings()` and `_run_in_memory()`) actually correct?**
  _`Settings` has 33 INFERRED edges - model-reasoned connections that need verification._
- **What connects `zaincash-support`, `@base-ui/react`, `@fontsource-variable/plus-jakarta-sans` to the rest of the system?**
  _90 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `fakes.py` be split into smaller, more focused modules?**
  _Cohesion score 0.08708708708708708 - nodes in this community are weakly interconnected._
- **Why does `Settings` connect `Settings` to `intake/model.py`, `test_rag_drafter.py`, `test_final_fix_handoff.py`, `Synthetic demo readiness`, `intake/conftest.py`, `test_credential_check.py`, `test_rag_api.py`, `test_draft_model.py`, `test_cli.py`, `test_workspace_api.py`, `test_embeddings.py`, `test_draft_tools.py`, `test_kb_service.py`, `db/repository.py`, `main.py`, `fact`, `agent.py`, `support_test`, `intake/repository.py`, `test_llm.py`, `_DatabaseCall`, `cli.py`, `RagDrafter`, `attachments.py`, `AttachmentStore`, `build_pipeline`?**
  _High betweenness centrality (0.080) - this node is a cross-community bridge._
- **Are the 24 inferred relationships involving `KnowledgeService` (e.g. with `Settings` and `UploadedDocument`) actually correct?**
  _`KnowledgeService` has 24 INFERRED edges - model-reasoned connections that need verification._

### Low-confidence Hints
_AMBIGUOUS edges — the extractor was unsure. Verify before acting on these._

- **What is the exact relationship between `Fraud Report` and `Plan 1 Live Smoke`?**
  _Edge tagged AMBIGUOUS (relation: conceptually_related_to) - confidence is low._