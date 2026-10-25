# Graph Report - zaincash-support  (2026-10-25)

## Corpus Check
- 305 files · ~252,753 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 30 file(s) not represented in the graph (top: (none) 18, .jsonl 4, .css 4)

## Summary
- 3062 nodes · 9455 edges · 158 communities (113 shown, 45 thin omitted)
- Extraction: 89% EXTRACTED · 11% INFERRED · 0% AMBIGUOUS · INFERRED: 1049 edges (avg confidence: 0.93)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `244e23ff`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- stage6_draft/model.py
- intake/types.ts
- pytest
- TurnStore
- test_draft_guardrails.py
- tools.py
- QueuePage.tsx
- Customer conversation intake for ZainCash support
- trace-facts.ts
- IntakeController
- FakeJevRunnable
- test_rag_api.py
- employee-frontend/package.json
- intake/helpers.py
- Support Taxonomy Categories
- ui/package.json
- employee-frontend/src/App.tsx
- users-frontend/package.json
- make_output
- UploadedDocument
- web/package.json
- test_recovery_regressions.py
- compilerOptions
- employee-frontend/components.json
- intake/test_repository.py
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
- fakes.py
- ui/components.json
- Settings
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
- AttachmentStore
- intake/repository.py
- batch_jobs.py
- NewBatchPage.tsx
- investigation.py
- test_llm.py
- tasks
- PipelineTrace.tsx
- IntakePage.tsx
- test_handoff.py
- PipelineState
- main.py
- test_submission.py
- taxonomy.py
- Credentials
- lib/types.ts
- test-kb/README.md
- cli.py
- Synthetic demo readiness
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
- guardrails.py
- ticket-flow.ts
- review.py
- compilerOptions
- قواعد المعرفة العربية للعرض أمام لجنة التحكيم
- pydantic
- dependencies
- InvalidEvidence
- dependencies
- compilerOptions
- ar/app_bug.md
- controller.test.ts
- test_final_fix_handoff.py
- ZainCash Support Workspace
- negative/README.md
- scripts
- scripts
- compilerOptions
- ar/bill_payment.md
- dependencies
- web/tsconfig.json
- employee-frontend/tsconfig.json
- exports
- ar/card_issue.md
- scripts
- users-frontend/README.md
- intake/contracts.py
- TurnContext
- AttachmentStore
- ar/failed_transfer.md
- workspace-ui.tsx
- test_gemini.py
- ar/fraud_report.md
- intake/model.py
- KnowledgeExecutionError
- intake.py
- IntakePage.test.tsx
- kb/service.py
- ar/general_inquiry.md
- Customer Conversation Intake Implementation Plan
- test_workspace_api.py
- ar/login_access.md
- intake/api.ts
- DraftContext
- kb/service.py
- ar/refund_request.md
- test_dbapi_commit_handoff_arbitrates_cancellation
- @testing-library/react
- components-ai-thought-chain.tsx
- intake/README.md
- errors.py
- schemas.py
- employee-frontend/src/components/theme-provider.tsx
- load_taxonomy
- Customer intake chat layout
- bill-payment-biller-notice.md
- test_draft_model.py
- KnowledgePage
- rag_fakes.py

## God Nodes (most connected - your core abstractions)
1. `Settings` - 103 edges
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

## Communities (158 total, 45 thin omitted)

### Community 1 - "intake/types.ts"
Cohesion: 0.12
Nodes (20): IntakeApi, ControllerState, emptyState(), fileIdentity(), Credentials, EvidenceRef, Fact, IntakeMessage (+12 more)

### Community 2 - "pytest"
Cohesion: 0.23
Nodes (32): answer(), call(), draft_state(), script(), submit(), drafter(), events(), test_callback_partial_response_and_error_cost_are_alternatives() (+24 more)

### Community 3 - "TurnStore"
Cohesion: 0.18
Nodes (11): OperationClaim, TurnResult, sanitize_intake_text(), _jsonable(), TurnStore, fail_once(), repo(), test_recovered_attempt_cannot_publish_stale_output() (+3 more)

### Community 4 - "test_draft_guardrails.py"
Cohesion: 0.14
Nodes (26): requests_credentials(), check(), state(), test_aggregation_is_deduplicated_and_has_no_state_side_effects(), test_amount_occurrences_keep_their_own_currency_and_sign(), test_avoid_sharing_warning_does_not_excuse_a_later_request(), test_candidate_prompt_limit_does_not_hide_later_ungrounded_references(), test_candidate_transactions_cannot_authorize_reply_evidence() (+18 more)

### Community 5 - "tools.py"
Cohesion: 0.06
Nodes (23): DraftAlreadySubmitted, DraftSubmission, DraftToolLimit, _bounded(), visit(), build_tools(), flag(), guarded() (+15 more)

### Community 6 - "QueuePage.tsx"
Cohesion: 0.18
Nodes (43): EmptyState(), ErrorState(), LoadingState(), Metric(), PageHeader(), PriorityBadge(), StatusBadge(), Button() (+35 more)

### Community 7 - "Customer conversation intake for ZainCash support"
Cohesion: 0.06
Nodes (31): 10. Verification and acceptance criteria, 11. Delivery and review, 1. Outcome and agreed requirements, 2. Current implementation and integration points, 3. Approach and boundaries, 4. Conversation state and turn flow, 5. Facts, evidence, and readiness, 6. Language and screenshot behavior (+23 more)

### Community 8 - "trace-facts.ts"
Cohesion: 0.19
Nodes (23): Confidence(), highlightedText(), SourceEvidence(), save(), classifySentence(), FIELD_LABELS, fieldValue(), FLOW_STAGES (+15 more)

### Community 9 - "IntakeController"
Cohesion: 0.19
Nodes (5): IntakeController, isConflict(), isOffline(), safeMessage(), Language

### Community 10 - "FakeJevRunnable"
Cohesion: 0.08
Nodes (30): JevClassifier, CredentialCheck, CredentialChecker, DegradedCredentialChecker, _finite_nonnegative(), _get(), JevCredentialChecker, FakeJevRunnable (+22 more)

### Community 11 - "test_rag_api.py"
Cohesion: 0.15
Nodes (16): client(), test_actual_guardrail_failure_is_separate_from_reply(), test_concurrent_index_requests_share_active_work(), test_disabled_or_missing_provider_stores_without_indexing(), test_explicit_retry_tags_search_and_chunk_pagination(), test_health_distinguishes_failed_from_empty(), test_health_requires_compatible_nonempty_index(), test_index_background_admission_is_bounded_and_releases_capacity() (+8 more)

### Community 12 - "employee-frontend/package.json"
Cohesion: 0.06
Nodes (31): @base-ui/react, class-variance-authority, cn, eslint, @eslint/js, eslint-plugin-react-hooks, eslint-plugin-react-refresh, @fontsource/tajawal (+23 more)

### Community 14 - "intake/helpers.py"
Cohesion: 0.24
Nodes (4): grounded_analysis(), grounded_review(), image_evidence(), ScriptedIntakeModel

### Community 15 - "Support Taxonomy Categories"
Cohesion: 0.21
Nodes (22): lookup, Account KYC, Account & Security, Agent Dispute, Agent Network, App Bug, Bill Payment, Card Issue (+14 more)

### Community 16 - "ui/package.json"
Cohesion: 0.07
Nodes (29): @turbo/gen, zod, @base-ui/react, class-variance-authority, cn, eslint, @eslint/js, eslint-plugin-react-hooks (+21 more)

### Community 17 - "employee-frontend/src/App.tsx"
Cohesion: 0.10
Nodes (26): App(), EvaluationPage, InsightsPage, KnowledgePage, NewBatchPage, QueuePage, RunDetailPage, RunsPage (+18 more)

### Community 18 - "users-frontend/package.json"
Cohesion: 0.09
Nodes (22): turbo, devDependencies, prettier, prettier-plugin-tailwindcss, turbo, typescript, engines, node (+14 more)

### Community 19 - "make_output"
Cohesion: 0.20
Nodes (22): outcome_to_dict(), outcome_to_row(), FakeClassifier, make_output(), make_ticket(), _deps(), _run(), test_cascade_confident_jev_skips_gemini() (+14 more)

### Community 20 - "UploadedDocument"
Cohesion: 0.12
Nodes (23): delete_document(), download_document(), index_document(), list_chunks(), list_documents(), _require_provider(), search_knowledge(), upload_document() (+15 more)

### Community 21 - "web/package.json"
Cohesion: 0.08
Nodes (25): jsdom, @testing-library/user-event, @workspace/ui, eslint, @eslint/js, eslint-plugin-react-hooks, eslint-plugin-react-refresh, globals (+17 more)

### Community 22 - "test_recovery_regressions.py"
Cohesion: 0.32
Nodes (10): IntakeOperationRow, command(), create(), test_actual_app_restart_reconciles_failed_placeholder(), test_failed_review_retry_cannot_reopen_submitted_session(), test_original_payload_identity_survives_sanitization(), test_publication_failure_is_retryable_without_restart(), test_receipt_reference_is_preserved() (+2 more)

### Community 23 - "compilerOptions"
Cohesion: 0.08
Nodes (23): compilerOptions, allowArbitraryExtensions, allowImportingTsExtensions, erasableSyntaxOnly, jsx, lib, module, moduleDetection (+15 more)

### Community 24 - "employee-frontend/components.json"
Cohesion: 0.09
Nodes (21): aliases, components, hooks, lib, ui, utils, iconLibrary, menuAccent (+13 more)

### Community 25 - "intake/test_repository.py"
Cohesion: 0.20
Nodes (10): IntakeMessageRow, repo(), test_blank_intake_model_is_rejected(), test_contracts_reject_extra_keys(), test_datetimes_must_be_timezone_aware(), test_message_sequence_is_unique(), test_messages_keep_sequence_and_unicode(), test_non_positive_image_limit_is_rejected() (+2 more)

### Community 26 - "compilerOptions"
Cohesion: 0.09
Nodes (22): compilerOptions, allowArbitraryExtensions, allowImportingTsExtensions, erasableSyntaxOnly, jsx, lib, module, moduleDetection (+14 more)

### Community 27 - "web/src/components/theme-provider.tsx"
Cohesion: 0.17
Nodes (12): App(), disableTransitionsTemporarily(), getSystemTheme(), isEditableTarget(), isTheme(), ResolvedTheme, Theme, THEME_VALUES (+4 more)

### Community 28 - "test_embeddings.py"
Cohesion: 0.08
Nodes (41): EmbeddingBatch, EmbeddingError, _nonnegative_number(), OpenRouterEmbedder, _ordered_vectors(), _response_cost(), _percentile(), embedder_for() (+33 more)

### Community 29 - "Classify and Extract Prompts"
Cohesion: 0.31
Nodes (9): extract, gemini_classify, Pipeline Graph Orchestration, jev_classify, prepare, Gemini Classify Prompt v1, Gemini Extract Prompt v1, GeminiClassifier (+1 more)

### Community 30 - "test_draft_tools.py"
Cohesion: 0.12
Nodes (28): IncidentRow, ErrorEmbedder, test_all_eight_tools_and_seven_parallel_calls_execute_only_six(), test_context_copies_input_and_rejects_raising_hard_call_limit(), test_database_faults_remain_distinct_and_record_paid_search_cost(), test_discovered_ref_can_be_inspected_but_not_promoted_to_match(), test_exact_and_fuzzy_queries_are_scoped_and_never_confirm_candidates(), test_exact_reference_still_requires_customer_and_excludes_future() (+20 more)

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
Nodes (38): KnowledgeChunk, KnowledgeService, FakeEmbedder, GatedEmbedder, LateEmbedder, PaidEmbedder, test_real_knowledge_search_snapshots_are_isolated_and_json_ready(), count_chunks() (+30 more)

### Community 36 - "web/components.json"
Cohesion: 0.10
Nodes (19): aliases, components, hooks, lib, ui, utils, iconLibrary, menuAccent (+11 more)

### Community 38 - "fakes.py"
Cohesion: 0.08
Nodes (37): LLMUnavailable, StructuredLLM, Candidates, ClassificationResult, ClassifierOutput, FieldPick, NormalizedTicket, _default_retry() (+29 more)

### Community 39 - "ui/components.json"
Cohesion: 0.10
Nodes (19): aliases, components, hooks, lib, ui, utils, iconLibrary, menuAccent (+11 more)

### Community 40 - "Settings"
Cohesion: 0.07
Nodes (28): Settings, build_pipeline(), ConfigError, make_draft_model(), make_gemini_llm(), make_jev_client(), model_ids(), run_batch() (+20 more)

### Community 41 - "fact"
Cohesion: 0.18
Nodes (40): Analysis, EvidenceRef, Fact, merge_analysis(), remove_attachment_evidence(), assess_readiness(), field_is_resolved(), context() (+32 more)

### Community 43 - "Human Review Gate"
Cohesion: 0.25
Nodes (4): support CLI, Support Workspace UI Plan, Review API, Workspace UI Verification

### Community 44 - "compilerOptions"
Cohesion: 0.12
Nodes (16): compilerOptions, allowImportingTsExtensions, erasableSyntaxOnly, lib, module, moduleDetection, noEmit, noFallthroughCasesInSwitch (+8 more)

### Community 46 - "agent.py"
Cohesion: 0.07
Nodes (13): DraftResult, _Nodes, Drafter, NullDrafter, UnavailableDrafter, PipelineState, test_explicit_even_falsy_drafter_wins_over_default_wiring(), draft() (+5 more)

### Community 47 - "compilerOptions"
Cohesion: 0.12
Nodes (16): compilerOptions, allowImportingTsExtensions, erasableSyntaxOnly, lib, module, moduleDetection, noEmit, noFallthroughCasesInSwitch (+8 more)

### Community 48 - "support_test"
Cohesion: 0.07
Nodes (32): ingest(), index_deadlines(), settings(), support_test(), expire_during_embedding(), Completion and review record — 2026-10-17, Execution handoff, File map and shared interfaces (+24 more)

### Community 57 - "parse_document"
Cohesion: 0.11
Nodes (28): _append_chunks(), _check_extracted_size(), DocumentParseError, parse_document(), _parse_pdf(), make_pdf(), test_arabic_text_and_bom_are_preserved(), test_blank_pdf_tells_operator_to_use_ocr() (+20 more)

### Community 58 - "AttachmentStore"
Cohesion: 0.15
Nodes (5): AttachmentStore, NotOwned, IntakeRepository, make_intake_service(), builder()

### Community 59 - "intake/repository.py"
Cohesion: 0.20
Nodes (14): _display_name(), CustomerReview, IntakeAttachmentRow, IntakeSessionRow, _attachment(), customer_review(), load_attachments(), load_messages() (+6 more)

### Community 60 - "batch_jobs.py"
Cohesion: 0.17
Nodes (19): _safe_dispatch(), get_run(), list_runs(), start_run(), RunRow, save_outcomes(), recover(), TicketOutcome (+11 more)

### Community 61 - "NewBatchPage.tsx"
Cohesion: 0.09
Nodes (26): Badge(), badgeVariants, buttonVariants, Tabs(), TabsContent(), TabsList(), tabsListVariants, TabsTrigger() (+18 more)

### Community 62 - "investigation.py"
Cohesion: 0.14
Nodes (16): TxnRecord, parse_dt(), txn_from_dict(), DraftToolInputError, _datetime(), _days(), _field(), _involves() (+8 more)

### Community 63 - "test_llm.py"
Cohesion: 0.13
Nodes (9): GeminiStructuredLLM, _llm(), _S, test_draft_model_uses_millisecond_timeout_and_disables_sdk_retries(), test_openrouter_reported_cost_takes_precedence_over_token_estimate(), test_openrouter_retry_budget_is_bounded(), send(), test_to_sample_exception_and_parse_error() (+1 more)

### Community 64 - "tasks"
Cohesion: 0.12
Nodes (16): dependsOn, inputs, outputs, cache, persistent, dependsOn, dependsOn, $schema (+8 more)

### Community 65 - "PipelineTrace.tsx"
Cohesion: 0.10
Nodes (24): Ticket Flow Charts Implementation Plan, 1. Outcome, 2. Scope, 5. Language, 6. How a result becomes the charts, 7. Sentences, 8. Tests, 9. Files (+16 more)

### Community 66 - "IntakePage.tsx"
Cohesion: 0.13
Nodes (22): Global Constraints, Intake Chat UI Implementation Plan, Task 1: Put the summary and receipt in the thread, Task 2: Put screenshots inside the composer, Task 3: Apply the workspace chat styles, Task 4: Check the page in the browser, 4. Components, ChatTranscript() (+14 more)

### Community 67 - "test_handoff.py"
Cohesion: 0.10
Nodes (21): dispatch_intake(), _amount(), analyze(), complete_conversation(), _dated(), _message(), _opening(), _png() (+13 more)

### Community 68 - "PipelineState"
Cohesion: 0.11
Nodes (18): 10. Remaining demo roadmap, 1. Intent and acceptance criteria, 3. Provider and configuration, 4. Knowledge ingestion and persistence, 5. Retrieval and evidence, 6. Bounded investigation agent, 7. Draft guardrails and failure outcomes, 8. Pipeline, API, CLI and UI integration (+10 more)

### Community 69 - "main.py"
Cohesion: 0.08
Nodes (18): get_session(), get_result(), list_results(), read_intake_attachment(), review_result(), ReviewInput, health(), insights() (+10 more)

### Community 70 - "test_submission.py"
Cohesion: 0.32
Nodes (4): _payload(), test_concurrent_submit_dispatches_once(), test_second_request_id_reuses_the_approved_review(), test_submission_replay_creates_one_ticket()

### Community 71 - "taxonomy.py"
Cohesion: 0.13
Nodes (7): most_urgent(), priority_rank(), TaxonomyError, tax(), taxonomy(), test_priority_helpers(), test_rejects_unknown_team()

### Community 73 - "Credentials"
Cohesion: 0.26
Nodes (4): Credentials, SessionView, IntakeService, test_only_token_owner_can_resume()

### Community 74 - "lib/types.ts"
Cohesion: 0.10
Nodes (31): acceptIndexRequest(), canRequestIndex(), PendingIndexes, persistPendingIndexes(), pollKnowledge(), refresh(), stop(), PollOptions (+23 more)

### Community 75 - "test-kb/README.md"
Cohesion: 0.15
Nodes (6): Fictional RAG walkthrough inputs, توثيق الحساب — سياسة خيالية للعرض التجريبي, نزاع مع وكيل — سياسة خيالية للعرض التجريبي, الطلبات غير الواضحة وخارج النطاق — سياسة خيالية للعرض التجريبي, الاستفسار المؤقت للدعم في المهمة ٨ — سياسة خيالية للعرض التجريبي, التحويل لمستلم بالخطأ — سياسة خيالية للعرض التجريبي

### Community 76 - "cli.py"
Cohesion: 0.09
Nodes (28): _command_settings(), ingest_kb_cmd(), init_db_cmd(), Mode, run_batch_cmd(), _run_in_memory(), _run_with_db(), seed_db_cmd() (+20 more)

### Community 77 - "Synthetic demo readiness"
Cohesion: 0.50
Nodes (4): Evidence by layer, Known limitations and remaining work, Repeatable local walkthrough, Synthetic demo readiness

### Community 79 - "devDependencies"
Cohesion: 0.12
Nodes (16): devDependencies, eslint, @eslint/js, eslint-plugin-react-hooks, eslint-plugin-react-refresh, globals, prettier, prettier-plugin-tailwindcss (+8 more)

### Community 80 - "judge-demo.ar.md"
Cohesion: 0.14
Nodes (13): أعطال التطبيق — سياسة خيالية للعرض التجريبي, استرجاع مبلغ شراء — سياسة خيالية للعرض التجريبي, استعادة الدخول — سياسة خيالية للعرض التجريبي, الاستفسار الآمن من الدعم — سياسة خيالية للعرض التجريبي, الاستفسار المؤقت للدعم في المهمة ٨ — سياسة خيالية للعرض التجريبي, التحويل المعلّق — سياسة خيالية للعرض التجريبي, التحويل لمستلم بالخطأ — سياسة خيالية للعرض التجريبي, الطلبات غير الواضحة وخارج النطاق — سياسة خيالية للعرض التجريبي (+5 more)

### Community 93 - "jev.py"
Cohesion: 0.25
Nodes (8): build_order_check(), build_questions(), build_state(), category_criteria(), _input_tokens(), _picks(), _priority(), Taxonomy

### Community 94 - "devDependencies"
Cohesion: 0.11
Nodes (19): devDependencies, eslint, @eslint/js, eslint-plugin-react-hooks, eslint-plugin-react-refresh, globals, jsdom, @tailwindcss/vite (+11 more)

### Community 95 - "devDependencies"
Cohesion: 0.14
Nodes (14): devDependencies, eslint, @eslint/js, eslint-plugin-react-hooks, eslint-plugin-react-refresh, globals, tailwindcss, @tailwindcss/vite (+6 more)

### Community 96 - "guardrails.py"
Cohesion: 0.05
Nodes (55): load_jsonl(), load_tickets(), _rows(), Passage, Candidate, _add(), find_candidates(), normalize_phone() (+47 more)

### Community 97 - "ticket-flow.ts"
Cohesion: 0.08
Nodes (58): Global Constraints, Task 1: Sentence catalog, Task 2: Which step is open, Task 3: Received, produced, and drafting events, Task 4: Mermaid source, Task 5: Draw the charts on the ticket page, buildTicketFlow(), AR (+50 more)

### Community 98 - "review.py"
Cohesion: 0.32
Nodes (14): ReviewText, InvalidEvidence, build_review(), _compact(), _render_value(), _ticket_text(), _tokens(), validate_review_numbers() (+6 more)

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
Nodes (17): dependencies, @base-ui/react, class-variance-authority, cn, @fontsource/tajawal, @fontsource-variable/plus-jakarta-sans, lucide-react, mermaid (+9 more)

### Community 103 - "InvalidEvidence"
Cohesion: 0.18
Nodes (14): canonical_digits(), normalize_reported_date(), _apply(), _check_reference(), _compact(), checked_update(), _newer_correction(), _normalize_precise() (+6 more)

### Community 104 - "dependencies"
Cohesion: 0.15
Nodes (13): dependencies, @base-ui/react, class-variance-authority, cn, @fontsource/tajawal, @fontsource-variable/plus-jakarta-sans, @hugeicons/core-free-icons, @hugeicons/react (+5 more)

### Community 105 - "compilerOptions"
Cohesion: 0.17
Nodes (11): compilerOptions, jsx, lib, module, moduleResolution, outDir, skipLibCheck, strict (+3 more)

### Community 107 - "controller.test.ts"
Cohesion: 0.21
Nodes (7): controller, emptySession(), fakeApi(), review, browserSessionStorage(), SessionStorage, SavedSession

### Community 108 - "test_final_fix_handoff.py"
Cohesion: 0.11
Nodes (22): RagDrafter, DraftExecutionError, Knowledge, assert_completed_evidence(), faulty_knowledge(), outer_deadlines(), PaidEmbeddings, runner_env() (+14 more)

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

### Community 122 - "intake/contracts.py"
Cohesion: 0.16
Nodes (20): _aware(), IntakeModel, IntakeState, Message, Question, QuestionRecord, Readiness, ReviewSnapshot (+12 more)

### Community 123 - "TurnContext"
Cohesion: 0.23
Nodes (3): TurnContext, IntakeGraph, _invitation()

### Community 124 - "AttachmentStore"
Cohesion: 0.26
Nodes (14): ImageRejected, png_bytes(), repo(), store(), test_active_turn_rejects_upload(), test_changed_invalid_bytes_conflict_before_decoding_replay(), test_concurrent_uploads_stop_at_the_session_cap(), attempt() (+6 more)

### Community 126 - "workspace-ui.tsx"
Cohesion: 0.16
Nodes (17): ConfirmDialog(), FilterSelect(), Dialog(), DialogContent(), DialogDescription(), DialogFooter(), DialogHeader(), DialogOverlay() (+9 more)

### Community 127 - "test_gemini.py"
Cohesion: 0.18
Nodes (15): Sample, ExtractedSpan, _Fields, GeminiAnalysis, GeminiFields, FakeStructuredLLM, _a(), _classify() (+7 more)

### Community 129 - "intake/model.py"
Cohesion: 0.10
Nodes (29): Attachment, ImageInput, ModelCall, ModelUnavailable, _analysis_prompt(), _bounded_context(), _guard_size(), ModelBudget (+21 more)

### Community 131 - "intake.py"
Cohesion: 0.17
Nodes (19): create_session(), _credentials(), _dump(), get_session(), post_message(), read_attachment(), remove_attachment(), request_review() (+11 more)

### Community 132 - "IntakePage.test.tsx"
Cohesion: 0.20
Nodes (13): HTTP contract (implemented in Tasks 4–5), Task 6: Customer API client and resumable UI state, Task 7: Bilingual customer chat, screenshots and reviewed submission, Task 8: Employee evidence panel and processing state, Task 9: End-to-end handoff, live vision evidence and runbook, copy(), attachment, collectingController() (+5 more)

### Community 133 - "kb/service.py"
Cohesion: 0.07
Nodes (12): Embedder, SearchResult, TextChunk, _abandoned(), _check_deadline(), _Claim, _consume(), _DatabaseCall (+4 more)

### Community 135 - "Customer Conversation Intake Implementation Plan"
Cohesion: 0.20
Nodes (8): Completion audit — 2026-10-18, Customer Conversation Intake Implementation Plan, Execution conventions and repository baseline, File map and dependency order, Global Constraints, Plan review and execution handoff, Review Focus, Spec coverage and acceptance map

### Community 136 - "test_workspace_api.py"
Cohesion: 0.06
Nodes (39): init_db(), make_engine(), make_sessionmaker(), reset_db(), upgrade_workspace_schema(), create_app(), lifespan(), build_graph() (+31 more)

### Community 138 - "intake/api.ts"
Cohesion: 0.15
Nodes (13): createIntakeApi(), IntakeRequestError, isRecord(), parseJson(), parseReceipt(), parseSession(), readError(), stringList() (+5 more)

### Community 139 - "DraftContext"
Cohesion: 0.13
Nodes (5): _error_cost(), _Execution, _ModelUsage, _number(), DraftContext

### Community 140 - "kb/service.py"
Cohesion: 0.14
Nodes (9): Base, TicketResultRow, Receipt, IntakeSubmissionRow, employee_attachment(), current_session_view(), SubmissionResult, SubmissionService (+1 more)

### Community 142 - "test_dbapi_commit_handoff_arbitrates_cancellation"
Cohesion: 0.47
Nodes (4): test_dbapi_commit_handoff_arbitrates_cancellation(), gate(), gate_before_dbapi(), gate_inside_dbapi()

### Community 148 - "components-ai-thought-chain.tsx"
Cohesion: 0.12
Nodes (16): Status, StatusIcon(), statusStyles, StepContext, StepContextType, ThoughtChain(), ThoughtChainContent(), ThoughtChainItem() (+8 more)

### Community 151 - "errors.py"
Cohesion: 0.23
Nodes (9): IntakeError, OperationConflict, RevisionConflict, StaleReview, TurnBusy, assert_same_operation(), operation_fingerprint(), test_changed_payload_cannot_reuse_operation_identity() (+1 more)

### Community 153 - "schemas.py"
Cohesion: 0.21
Nodes (4): BatchInput, KnowledgeIndexInput, KnowledgeSearchInput, TicketInput

### Community 156 - "employee-frontend/src/components/theme-provider.tsx"
Cohesion: 0.21
Nodes (11): disableTransitionsTemporarily(), getSystemTheme(), isEditableTarget(), isTheme(), ResolvedTheme, Theme, THEME_VALUES, ThemeProvider() (+3 more)

### Community 158 - "load_taxonomy"
Cohesion: 0.11
Nodes (32): Decision, ExtractedField, LookupResult, _as_date(), _iqd_amount(), match_transaction(), TransactionRepo, decide() (+24 more)

### Community 161 - "Customer intake chat layout"
Cohesion: 0.33
Nodes (5): 1. Outcome, 2. Scope, 3. Layout, 5. Checks, Customer intake chat layout

### Community 164 - "test_draft_model.py"
Cohesion: 0.33
Nodes (7): response_payload(), run_provider_pipeline(), send(), search_response(), test_empty_choices_escalates_and_keeps_paid_response_usage(), test_failed_response_id_is_deduplicated_against_earlier_success(), test_other_conversion_value_errors_remain_unexpected()

### Community 166 - "KnowledgePage"
Cohesion: 0.60
Nodes (5): beginMutation(), deleteDocument(), finishMutation(), indexDocument(), upload()

### Community 167 - "rag_fakes.py"
Cohesion: 0.15
Nodes (8): Checker, ScriptedChat, test_gemini_mode_builds_real_jev_checker_when_only_key_is_supplied(), evidence_client(), pipeline(), submit(), test_concurrent_tickets_cannot_exchange_citations_cost_or_callback_state(), Task 5: Agent, failure conversion and pipeline wiring

## Ambiguous Edges - Review These
- `Fraud Report` → `Plan 1 Live Smoke`  [AMBIGUOUS]
  README.md · relation: conceptually_related_to

## Knowledge Gaps
- **91 isolated node(s):** `zaincash-support`, `@base-ui/react`, `@fontsource-variable/plus-jakarta-sans`, `@fontsource/tajawal`, `@tailwindcss/vite` (+86 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 1013 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **45 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `HTTP contract (implemented in Tasks 4–5)` connect `IntakePage.test.tsx` to `guardrails.py`, `intake/model.py`, `TurnStore`, `Customer Conversation Intake Implementation Plan`, `errors.py`, `batch_jobs.py`?**
  _High betweenness centrality (0.100) - this node is a cross-community bridge._
- **Are the 33 inferred relationships involving `Settings` (e.g. with `_command_settings()` and `_run_in_memory()`) actually correct?**
  _`Settings` has 33 INFERRED edges - model-reasoned connections that need verification._
- **What connects `zaincash-support`, `@base-ui/react`, `@fontsource-variable/plus-jakarta-sans` to the rest of the system?**
  _91 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `intake/types.ts` be split into smaller, more focused modules?**
  _Cohesion score 0.12043010752688173 - nodes in this community are weakly interconnected._
- **Why does `Settings` connect `Settings` to `intake/model.py`, `pytest`, `kb/service.py`, `tools.py`, `test_workspace_api.py`, `FakeJevRunnable`, `DraftContext`, `kb/service.py`, `test_rag_api.py`, `intake/test_repository.py`, `test_embeddings.py`, `test_draft_tools.py`, `test_kb_service.py`, `test_draft_model.py`, `rag_fakes.py`, `fact`, `agent.py`, `support_test`, `AttachmentStore`, `intake/repository.py`, `test_llm.py`, `main.py`, `cli.py`, `Synthetic demo readiness`, `test_final_fix_handoff.py`?**
  _High betweenness centrality (0.091) - this node is a cross-community bridge._
- **Are the 24 inferred relationships involving `KnowledgeService` (e.g. with `Settings` and `UploadedDocument`) actually correct?**
  _`KnowledgeService` has 24 INFERRED edges - model-reasoned connections that need verification._

### Low-confidence Hints
_AMBIGUOUS edges — the extractor was unsure. Verify before acting on these._

- **What is the exact relationship between `Fraud Report` and `Plan 1 Live Smoke`?**
  _Edge tagged AMBIGUOUS (relation: conceptually_related_to) - confidence is low._