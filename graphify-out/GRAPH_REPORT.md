# Graph Report - zaincash-support  (2026-10-29)

## Corpus Check
- 304 files · ~254,546 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 32 file(s) not represented in the graph (top: (none) 20, .jsonl 4, .css 4)

## Summary
- 3082 nodes · 9469 edges · 168 communities (120 shown, 48 thin omitted)
- Extraction: 89% EXTRACTED · 11% INFERRED · 0% AMBIGUOUS · INFERRED: 1041 edges (avg confidence: 0.92)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `92cb3a1d`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- normalize.py
- intake/types.ts
- pytest
- TurnStore
- test_draft_guardrails.py
- agent.py
- QueuePage.tsx
- Customer conversation intake for ZainCash support
- KnowledgePage.tsx
- IntakeController
- FakeJevRunnable
- test_rag_api.py
- employee-frontend/package.json
- Fact
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
- agent-chat.tsx
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
- FieldPick
- ui/components.json
- Settings
- fact
- Vite Config
- Human Review Gate
- compilerOptions
- PipelineState
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
- attachments.py
- agent.py
- rules.py
- NewBatchPage.tsx
- investigation.py
- jev.py
- tasks
- find_candidates
- IntakePage.tsx
- test_handoff.py
- PipelineState
- main.py
- Credentials
- taxonomy.py
- test_submission.py
- ingest.py
- lib/types.ts
- test-kb/README.md
- db/repository.py
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
- pipeline/contracts.py
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
- TicketInput
- controller.test.ts
- test_final_fix_handoff.py
- ZainCash Support Workspace
- negative/README.md
- scripts
- scripts
- compilerOptions
- fakes.py
- dependencies
- web/tsconfig.json
- employee-frontend/tsconfig.json
- exports
- Customer intake verification — 2026-10-18
- scripts
- users-frontend/README.md
- intake/contracts.py
- TurnContext
- task8-history-policy.md
- ar/failed_transfer.md
- pipeline/graph.py
- test_gemini.py
- collapsible.tsx
- intake/model.py
- test_llm.py
- intake.py
- intake/conftest.py
- kb/service.py
- ar/general_inquiry.md
- Customer Conversation Intake Implementation Plan
- KnowledgeExecutionError
- submission.py
- intake/api.ts
- tools.py
- build_tools
- test_cli.py
- test_dbapi_commit_handoff_arbitrates_cancellation
- RunRow
- indexDocument
- components-ai-thought-chain.tsx
- json
- intake/README.md
- test_recovery_regressions.py
- dispatch_intake
- Ticket flow charts
- CredentialChecker
- employee-frontend/src/components/theme-provider.tsx
- @testing-library/react
- lookup.py
- 7. Review and submission
- ar/bill_payment.md
- ar/login_access.md
- bill-payment-biller-notice.md
- api-entrypoint.sh
- factory.py
- ar/refund_request.md
- ar/wrong_recipient.md
- build_pipeline

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
- `7. Draft guardrails and failure outcomes` --references--> `requests_credentials()`  [INFERRED]
  docs/superpowers/specs/2026-10-17-plan3-rag-drafting-design.md → backend/app/pipeline/stage6_draft/guardrails.py
- `Evidence by layer` --references--> `support_test()`  [INFERRED]
  docs/demo-readiness.md → backend/tests/test_kb_service.py

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **Cascade Classification Path** — docs_superpowers_specs_2026_10_07_support_pipeline_design_cascade, docs_superpowers_plans_2026_10_07_plan1_core_pipeline_part2_jev_classifier, docs_superpowers_plans_2026_10_07_plan1_core_pipeline_part2_gemini_classifier, docs_superpowers_plans_2026_10_07_plan1_core_pipeline_part2_cascade_combine, readme_human_approval [EXTRACTED 1.00]
- **Drafting Agent Toolset** — backend_app_pipeline_runner_lookup_transaction, backend_app_pipeline_runner_search_transactions, backend_app_pipeline_runner_get_customer_recent_transactions, backend_app_pipeline_runner_get_customer_ticket_history, backend_app_pipeline_runner_check_service_status, backend_app_pipeline_runner_search_knowledge_base, backend_app_pipeline_runner_flag_for_human, backend_app_pipeline_runner_submit_draft [EXTRACTED 1.00]
- **Ticket Processing Stage Flow** — backend_app_pipeline_runner_prepare, backend_app_pipeline_runner_jev_classify, backend_app_pipeline_runner_gemini_classify, backend_app_pipeline_runner_extract, backend_app_pipeline_runner_lookup, backend_app_pipeline_runner_decide, backend_app_pipeline_runner_draft [EXTRACTED 1.00]

## Communities (168 total, 48 thin omitted)

### Community 0 - "normalize.py"
Cohesion: 0.20
Nodes (16): detect_arabizi(), fold_arabic(), has_latin_mix(), _latin_words(), mask_cards(), normalize(), sanitize_for_storage(), test_arabizi_detection() (+8 more)

### Community 1 - "intake/types.ts"
Cohesion: 0.11
Nodes (21): IntakeApi, ControllerState, emptyState(), fileIdentity(), Credentials, CustomerReview, EvidenceRef, Fact (+13 more)

### Community 2 - "pytest"
Cohesion: 0.19
Nodes (37): test_contracts_reject_extra_keys(), test_datetimes_must_be_timezone_aware(), answer(), call(), draft_state(), script(), test_submission_is_terminal_including_invalid_later_calls(), submit() (+29 more)

### Community 3 - "TurnStore"
Cohesion: 0.19
Nodes (13): OperationClaim, TurnResult, IntakeMessageRow, RevisionConflict, session_view(), sanitize_intake_text(), _jsonable(), TurnStore (+5 more)

### Community 4 - "test_draft_guardrails.py"
Cohesion: 0.14
Nodes (29): requests_credentials(), make_ticket(), check(), state(), test_aggregation_is_deduplicated_and_has_no_state_side_effects(), test_amount_occurrences_keep_their_own_currency_and_sign(), test_avoid_sharing_warning_does_not_excuse_a_later_request(), test_candidate_prompt_limit_does_not_hide_later_ungrounded_references() (+21 more)

### Community 5 - "agent.py"
Cohesion: 0.13
Nodes (5): _error_cost(), _Execution, _ModelUsage, _number(), DraftContext

### Community 6 - "QueuePage.tsx"
Cohesion: 0.14
Nodes (43): 2. Scope, Confidence(), EmptyState(), ErrorState(), LoadingState(), PageHeader(), PriorityBadge(), StatusBadge() (+35 more)

### Community 7 - "Customer conversation intake for ZainCash support"
Cohesion: 0.07
Nodes (28): 10. Verification and acceptance criteria, 11. Delivery and review, 1. Outcome and agreed requirements, 2. Current implementation and integration points, 3. Approach and boundaries, 4. Conversation state and turn flow, 5. Facts, evidence, and readiness, 6. Language and screenshot behavior (+20 more)

### Community 8 - "KnowledgePage.tsx"
Cohesion: 0.16
Nodes (29): 6. How a result becomes the charts, Metric(), Badge(), badgeVariants, Card(), CardContent(), CardHeader(), CardTitle() (+21 more)

### Community 9 - "IntakeController"
Cohesion: 0.18
Nodes (6): Task 6: Customer API client and resumable UI state, IntakeController, isConflict(), isOffline(), safeMessage(), Language

### Community 10 - "FakeJevRunnable"
Cohesion: 0.09
Nodes (29): CredentialCheck, DegradedCredentialChecker, _finite_nonnegative(), _get(), JevCredentialChecker, FakeJevRunnable, Checker, ResponseRunnable (+21 more)

### Community 11 - "test_rag_api.py"
Cohesion: 0.08
Nodes (30): init_db(), make_engine(), make_sessionmaker(), reset_db(), create_app(), lifespan(), IndexJobs, intake_db() (+22 more)

### Community 12 - "employee-frontend/package.json"
Cohesion: 0.06
Nodes (31): @base-ui/react, class-variance-authority, cn, eslint, @eslint/js, eslint-plugin-react-hooks, eslint-plugin-react-refresh, @fontsource/tajawal (+23 more)

### Community 14 - "Fact"
Cohesion: 0.28
Nodes (10): EvidenceRef, Fact, remove_attachment_evidence(), image_evidence(), test_removal_invalidates_every_image_only_fact_status(), test_reinspection_keeps_current_images_and_new_observations(), again(), test_review_after_failed_analysis_still_interprets_the_saved_message() (+2 more)

### Community 15 - "Support Taxonomy Categories"
Cohesion: 0.21
Nodes (22): lookup, Account KYC, Account & Security, Agent Dispute, Agent Network, App Bug, Bill Payment, Card Issue (+14 more)

### Community 16 - "ui/package.json"
Cohesion: 0.07
Nodes (29): @turbo/gen, zod, @base-ui/react, class-variance-authority, cn, eslint, @eslint/js, eslint-plugin-react-hooks (+21 more)

### Community 17 - "employee-frontend/src/App.tsx"
Cohesion: 0.09
Nodes (28): App(), EvaluationPage, InsightsPage, KnowledgePage, NewBatchPage, QueuePage, RunDetailPage, RunsPage (+20 more)

### Community 18 - "users-frontend/package.json"
Cohesion: 0.09
Nodes (22): turbo, devDependencies, prettier, prettier-plugin-tailwindcss, turbo, typescript, engines, node (+14 more)

### Community 19 - "make_output"
Cohesion: 0.30
Nodes (17): FakeClassifier, make_output(), _deps(), _run(), test_cascade_confident_jev_skips_gemini(), test_cascade_degrades_when_jev_fails(), test_cascade_uncertain_jev_goes_to_gemini(), test_concurrency_is_limited() (+9 more)

### Community 20 - "UploadedDocument"
Cohesion: 0.08
Nodes (30): delete_document(), download_document(), index_document(), list_chunks(), list_documents(), _require_provider(), search_knowledge(), upload_document() (+22 more)

### Community 21 - "web/package.json"
Cohesion: 0.07
Nodes (26): clsx, jsdom, tailwind-merge, @workspace/ui, eslint, @eslint/js, eslint-plugin-react-hooks, eslint-plugin-react-refresh (+18 more)

### Community 22 - "test_recovery_regressions.py"
Cohesion: 0.14
Nodes (13): _command_settings(), ingest_kb_cmd(), init_db_cmd(), Mode, run_batch_cmd(), _run_in_memory(), _run_with_db(), seed_db_cmd() (+5 more)

### Community 23 - "compilerOptions"
Cohesion: 0.08
Nodes (23): compilerOptions, allowArbitraryExtensions, allowImportingTsExtensions, erasableSyntaxOnly, jsx, lib, module, moduleDetection (+15 more)

### Community 24 - "employee-frontend/components.json"
Cohesion: 0.09
Nodes (21): aliases, components, hooks, lib, ui, utils, iconLibrary, menuAccent (+13 more)

### Community 25 - "agent-chat.tsx"
Cohesion: 0.17
Nodes (22): AgentChat, AgentChatProps, AgentMessage, AssistantText(), AttachedFile, AttachedImage, ChatStatus, cn() (+14 more)

### Community 26 - "compilerOptions"
Cohesion: 0.09
Nodes (22): compilerOptions, allowArbitraryExtensions, allowImportingTsExtensions, erasableSyntaxOnly, jsx, lib, module, moduleDetection (+14 more)

### Community 27 - "web/src/components/theme-provider.tsx"
Cohesion: 0.12
Nodes (21): Task 7: Bilingual customer chat, screenshots and reviewed submission, copy(), @testing-library/user-event, disableTransitionsTemporarily(), getSystemTheme(), isEditableTarget(), isTheme(), ResolvedTheme (+13 more)

### Community 28 - "test_embeddings.py"
Cohesion: 0.08
Nodes (41): EmbeddingBatch, EmbeddingError, _nonnegative_number(), OpenRouterEmbedder, _ordered_vectors(), _response_cost(), Embeddings, embedder_for() (+33 more)

### Community 29 - "Classify and Extract Prompts"
Cohesion: 0.31
Nodes (9): extract, gemini_classify, Pipeline Graph Orchestration, jev_classify, prepare, Gemini Classify Prompt v1, Gemini Extract Prompt v1, GeminiClassifier (+1 more)

### Community 30 - "test_draft_tools.py"
Cohesion: 0.11
Nodes (31): IncidentRow, TransactionRow, api(), ErrorEmbedder, settings(), test_all_eight_tools_and_seven_parallel_calls_execute_only_six(), test_context_copies_input_and_rejects_raising_hard_call_limit(), test_database_faults_remain_distinct_and_record_paid_search_cost() (+23 more)

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
Cohesion: 0.08
Nodes (38): Embedder, KnowledgeChunk, KnowledgeService, FakeEmbedder, GatedEmbedder, LateEmbedder, PaidEmbedder, count_chunks() (+30 more)

### Community 36 - "web/components.json"
Cohesion: 0.10
Nodes (19): aliases, components, hooks, lib, ui, utils, iconLibrary, menuAccent (+11 more)

### Community 38 - "FieldPick"
Cohesion: 0.23
Nodes (11): Sample, FieldPick, finalize(), FakeExtractor, _setup(), test_fill_gaps_noop_and_failure_tolerant(), test_fill_gaps_only_asks_for_weak_required_fields(), test_gemini_span_not_in_text_is_null() (+3 more)

### Community 39 - "ui/components.json"
Cohesion: 0.10
Nodes (19): aliases, components, hooks, lib, ui, utils, iconLibrary, menuAccent (+11 more)

### Community 40 - "Settings"
Cohesion: 0.10
Nodes (11): Settings, test_blank_intake_model_is_rejected(), test_non_positive_image_limit_is_rejected(), test_relative_upload_directory_is_rooted_in_the_repository(), test_anthropic_model_selects_the_draft_model_only(), test_defaults(), test_drafting_configuration_cannot_bypass_hard_limits(), test_drafting_limits_load_from_environment() (+3 more)

### Community 41 - "fact"
Cohesion: 0.26
Nodes (29): Attachment, InvalidEvidence, merge_analysis(), checked_update(), context(), fact(), message(), proposal() (+21 more)

### Community 43 - "Human Review Gate"
Cohesion: 0.25
Nodes (4): support CLI, Support Workspace UI Plan, Review API, Workspace UI Verification

### Community 44 - "compilerOptions"
Cohesion: 0.12
Nodes (16): compilerOptions, allowImportingTsExtensions, erasableSyntaxOnly, lib, module, moduleDetection, noEmit, noFallthroughCasesInSwitch (+8 more)

### Community 46 - "PipelineState"
Cohesion: 0.20
Nodes (6): _Nodes, PipelineState, Global Constraints, Ticket Flow Charts Implementation Plan, 3. What the employee sees, 4. Which step is open

### Community 47 - "compilerOptions"
Cohesion: 0.12
Nodes (16): compilerOptions, allowImportingTsExtensions, erasableSyntaxOnly, lib, module, moduleDetection, noEmit, noFallthroughCasesInSwitch (+8 more)

### Community 48 - "support_test"
Cohesion: 0.08
Nodes (25): ingest(), index_deadlines(), settings(), support_test(), expire_during_embedding(), Completion and review record — 2026-10-17, Execution handoff, File map and shared interfaces (+17 more)

### Community 57 - "parse_document"
Cohesion: 0.11
Nodes (29): TextChunk, _append_chunks(), _check_extracted_size(), DocumentParseError, parse_document(), _parse_pdf(), make_pdf(), test_arabic_text_and_bom_are_preserved() (+21 more)

### Community 58 - "attachments.py"
Cohesion: 0.10
Nodes (32): AttachmentStore, _display_name(), IntakeAttachmentRow, IntakeSessionRow, ImageRejected, IntakeError, NotOwned, OperationConflict (+24 more)

### Community 60 - "rules.py"
Cohesion: 0.19
Nodes (16): Decision, decide(), empty_ticket_decision(), merge_reasons(), note_for(), _unique(), Category, _decide() (+8 more)

### Community 61 - "NewBatchPage.tsx"
Cohesion: 0.08
Nodes (32): ConfirmDialog(), FilterSelect(), Button(), buttonVariants, Dialog(), DialogContent(), DialogDescription(), DialogFooter() (+24 more)

### Community 62 - "investigation.py"
Cohesion: 0.16
Nodes (15): TxnRecord, parse_dt(), DraftToolInputError, _datetime(), _days(), _field(), _involves(), _phone() (+7 more)

### Community 63 - "jev.py"
Cohesion: 0.26
Nodes (10): ClassificationResult, build_order_check(), build_questions(), build_state(), category_criteria(), _input_tokens(), JevClassifier, _picks() (+2 more)

### Community 64 - "tasks"
Cohesion: 0.12
Nodes (16): dependsOn, inputs, outputs, cache, persistent, dependsOn, dependsOn, $schema (+8 more)

### Community 65 - "find_candidates"
Cohesion: 0.32
Nodes (10): find_candidates(), _overlaps(), test_amount_forms(), test_arabic_indic_amount_not_confused_with_phone(), test_dates_absolute_and_weekday(), test_dedupes_repeated_values(), test_normalize_phone(), test_parse_amount() (+2 more)

### Community 66 - "IntakePage.tsx"
Cohesion: 0.10
Nodes (21): Global Constraints, Intake Chat UI Implementation Plan, Task 1: Put the summary and receipt in the thread, Task 2: Put screenshots inside the composer, Task 3: Apply the workspace chat styles, Task 4: Check the page in the browser, 1. Outcome, 2. Scope (+13 more)

### Community 67 - "test_handoff.py"
Cohesion: 0.22
Nodes (17): Analysis, initial(), _amount(), analyze(), complete_conversation(), _dated(), _message(), _opening() (+9 more)

### Community 68 - "PipelineState"
Cohesion: 0.07
Nodes (25): DraftResult, Drafter, NullDrafter, draft(), draft(), draft(), 10. Remaining demo roadmap, 1. Intent and acceptance criteria (+17 more)

### Community 69 - "main.py"
Cohesion: 0.07
Nodes (21): get_session(), get_result(), list_results(), read_intake_attachment(), review_result(), ReviewInput, health(), insights() (+13 more)

### Community 70 - "Credentials"
Cohesion: 0.12
Nodes (7): Credentials, SessionView, IntakeRepository, IntakeService, make_intake_service(), builder(), repo()

### Community 71 - "taxonomy.py"
Cohesion: 0.14
Nodes (9): load_taxonomy(), most_urgent(), priority_rank(), TaxonomyError, tax(), taxonomy(), taxonomy(), test_priority_helpers() (+1 more)

### Community 72 - "test_submission.py"
Cohesion: 0.38
Nodes (4): _payload(), test_concurrent_submit_dispatches_once(), test_second_request_id_reuses_the_approved_review(), test_submission_replay_creates_one_ticket()

### Community 73 - "ingest.py"
Cohesion: 0.26
Nodes (8): load_jsonl(), load_tickets(), _rows(), test_csv_with_bom_and_missing_columns(), test_duplicate_external_ids_keep_first(), test_json_object_without_ids(), test_jsonl_fixture_loads(), test_unsupported_format()

### Community 74 - "lib/types.ts"
Cohesion: 0.08
Nodes (35): Task 8: Employee evidence panel and processing state, acceptIndexRequest(), canRequestIndex(), PendingIndexes, persistPendingIndexes(), pollKnowledge(), refresh(), stop() (+27 more)

### Community 75 - "test-kb/README.md"
Cohesion: 0.13
Nodes (7): Fictional RAG walkthrough inputs, توثيق الحساب — سياسة خيالية للعرض التجريبي, نزاع مع وكيل — سياسة خيالية للعرض التجريبي, أعطال التطبيق — سياسة خيالية للعرض التجريبي, مشاكل البطاقة — سياسة خيالية للعرض التجريبي, تصعيد شبهة الاحتيال — سياسة خيالية للعرض التجريبي, الطلبات غير الواضحة وخارج النطاق — سياسة خيالية للعرض التجريبي

### Community 76 - "db/repository.py"
Cohesion: 0.19
Nodes (17): create_run(), finish_run(), load_incidents(), load_transactions(), save_outcomes(), _to_record(), _upsert(), upsert_tickets() (+9 more)

### Community 77 - "Synthetic demo readiness"
Cohesion: 0.50
Nodes (4): Evidence by layer, Known limitations and remaining work, Repeatable local walkthrough, Synthetic demo readiness

### Community 79 - "devDependencies"
Cohesion: 0.12
Nodes (16): devDependencies, eslint, @eslint/js, eslint-plugin-react-hooks, eslint-plugin-react-refresh, globals, prettier, prettier-plugin-tailwindcss (+8 more)

### Community 80 - "judge-demo.ar.md"
Cohesion: 0.14
Nodes (13): أعطال التطبيق — سياسة خيالية للعرض التجريبي, استرجاع مبلغ شراء — سياسة خيالية للعرض التجريبي, استعادة الدخول — سياسة خيالية للعرض التجريبي, الاستفسار الآمن من الدعم — سياسة خيالية للعرض التجريبي, الاستفسار المؤقت للدعم في المهمة ٨ — سياسة خيالية للعرض التجريبي, التحويل المعلّق — سياسة خيالية للعرض التجريبي, التحويل لمستلم بالخطأ — سياسة خيالية للعرض التجريبي, الطلبات غير الواضحة وخارج النطاق — سياسة خيالية للعرض التجريبي (+5 more)

### Community 93 - "pipeline/contracts.py"
Cohesion: 0.18
Nodes (11): Candidate, Candidates, ClassifierOutput, NormalizedTicket, _add(), Classifier, FieldExtractor, _field() (+3 more)

### Community 94 - "devDependencies"
Cohesion: 0.11
Nodes (19): devDependencies, eslint, @eslint/js, eslint-plugin-react-hooks, eslint-plugin-react-refresh, globals, jsdom, @tailwindcss/vite (+11 more)

### Community 95 - "devDependencies"
Cohesion: 0.14
Nodes (14): devDependencies, eslint, @eslint/js, eslint-plugin-react-hooks, eslint-plugin-react-refresh, globals, tailwindcss, @tailwindcss/vite (+6 more)

### Community 96 - "guardrails.py"
Cohesion: 0.12
Nodes (18): Passage, normalize_phone(), parse_amount(), resolve_date(), _safe_date(), to_ascii_digits(), _iso(), normalize_value() (+10 more)

### Community 97 - "ticket-flow.ts"
Cohesion: 0.06
Nodes (72): Task 1: Sentence catalog, Task 2: Which step is open, Task 3: Received, produced, and drafting events, Task 4: Mermaid source, Task 5: Draw the charts on the ticket page, buildTicketFlow(), AR, channelName() (+64 more)

### Community 98 - "review.py"
Cohesion: 0.19
Nodes (14): ReviewSnapshot, ReviewText, build_review(), _compact(), _render_value(), _ticket_text(), _tokens(), validate_review_numbers() (+6 more)

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
Cohesion: 0.17
Nodes (14): canonical_digits(), normalize_reported_date(), _apply(), _check_reference(), _compact(), _newer_correction(), _normalize_precise(), _own_phone_quote() (+6 more)

### Community 104 - "dependencies"
Cohesion: 0.15
Nodes (13): dependencies, @base-ui/react, class-variance-authority, cn, @fontsource/tajawal, @fontsource-variable/plus-jakarta-sans, @hugeicons/core-free-icons, @hugeicons/react (+5 more)

### Community 105 - "compilerOptions"
Cohesion: 0.17
Nodes (11): compilerOptions, jsx, lib, module, moduleResolution, outDir, skipLibCheck, strict (+3 more)

### Community 107 - "controller.test.ts"
Cohesion: 0.17
Nodes (8): App(), controller, emptySession(), fakeApi(), review, browserSessionStorage(), SessionStorage, SavedSession

### Community 108 - "test_final_fix_handoff.py"
Cohesion: 0.09
Nodes (24): RagDrafter, DraftExecutionError, Knowledge, ScriptedChat, assert_completed_evidence(), faulty_knowledge(), read(), outer_deadlines() (+16 more)

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

### Community 114 - "fakes.py"
Cohesion: 0.17
Nodes (13): LLMUnavailable, combine(), merge_picks(), verified_pick(), render_prompt(), test_both_missing_raises(), test_cost_is_summed(), test_degraded_when_jev_missing() (+5 more)

### Community 115 - "dependencies"
Cohesion: 0.25
Nodes (8): dependencies, clsx, @hugeicons/core-free-icons, @hugeicons/react, react, react-dom, tailwind-merge, @workspace/ui

### Community 116 - "web/tsconfig.json"
Cohesion: 0.33
Nodes (5): compilerOptions, paths, files, @workspace/ui/*, references

### Community 117 - "employee-frontend/tsconfig.json"
Cohesion: 0.40
Nodes (4): compilerOptions, paths, files, references

### Community 118 - "exports"
Cohesion: 0.40
Nodes (5): exports, ./components/*, ./globals.css, ./hooks/*, ./lib/*

### Community 119 - "Customer intake verification — 2026-10-18"
Cohesion: 0.25
Nodes (6): Browser handoff, Customer intake verification — 2026-10-18, Final automated checks, Live vision and paired review, Repaired gaps and regression evidence, Review decisions and remaining limits

### Community 120 - "scripts"
Cohesion: 0.50
Nodes (4): scripts, format, lint, typecheck

### Community 122 - "intake/contracts.py"
Cohesion: 0.16
Nodes (18): _aware(), IntakeModel, IntakeState, Message, Question, Readiness, _asked_already(), asks_for_secret() (+10 more)

### Community 123 - "TurnContext"
Cohesion: 0.13
Nodes (11): QuestionRecord, TurnContext, IntakeGraph, _invitation(), grounded_analysis(), grounded_review(), ScriptedIntakeModel, HTTP contract (implemented in Tasks 4–5) (+3 more)

### Community 126 - "pipeline/graph.py"
Cohesion: 0.14
Nodes (12): recover(), TicketExecution, _default_retry(), outcome_from_state(), _percentile(), _retryable(), summarize(), process_batch() (+4 more)

### Community 127 - "test_gemini.py"
Cohesion: 0.18
Nodes (15): StructuredLLM, ExtractedSpan, _Fields, GeminiClassifier, GeminiExtractor, GeminiFields, _a(), _classify() (+7 more)

### Community 129 - "intake/model.py"
Cohesion: 0.10
Nodes (29): ImageInput, ModelCall, ModelUnavailable, _analysis_prompt(), _bounded_context(), _guard_size(), ModelBudget, OpenRouterIntakeModel (+21 more)

### Community 130 - "test_llm.py"
Cohesion: 0.13
Nodes (10): GeminiStructuredLLM, _llm(), _S, test_draft_model_uses_millisecond_timeout_and_disables_sdk_retries(), test_openrouter_reported_cost_takes_precedence_over_token_estimate(), test_openrouter_retry_budget_is_bounded(), test_openrouter_structured_samples_use_configured_key_and_validate_output(), send() (+2 more)

### Community 131 - "intake.py"
Cohesion: 0.17
Nodes (20): create_session(), _credentials(), _dump(), get_session(), post_message(), read_attachment(), remove_attachment(), request_review() (+12 more)

### Community 132 - "intake/conftest.py"
Cohesion: 0.11
Nodes (16): build_graph(), PipelineDeps, InMemoryTransactionRepo, intake_client(), pipeline(), reviewed(), test_run_batch_no_db_writes_summary_and_out(), fake_build() (+8 more)

### Community 133 - "kb/service.py"
Cohesion: 0.10
Nodes (6): _check_deadline(), _Claim, _consume(), _DatabaseCall, IndexAttemptLostError, KnowledgeError

### Community 135 - "Customer Conversation Intake Implementation Plan"
Cohesion: 0.25
Nodes (8): Completion audit — 2026-10-18, Customer Conversation Intake Implementation Plan, Execution conventions and repository baseline, File map and dependency order, Global Constraints, Plan review and execution handoff, Review Focus, Spec coverage and acceptance map

### Community 137 - "submission.py"
Cohesion: 0.20
Nodes (16): CustomerReview, Receipt, IntakeOperationRow, IntakeSubmissionRow, StaleReview, _attachment(), customer_review(), load_attachments() (+8 more)

### Community 138 - "intake/api.ts"
Cohesion: 0.15
Nodes (13): createIntakeApi(), IntakeRequestError, isRecord(), parseJson(), parseReceipt(), parseSession(), readError(), stringList() (+5 more)

### Community 139 - "tools.py"
Cohesion: 0.12
Nodes (15): DraftAlreadySubmitted, DraftToolLimit, _bounded(), visit(), guarded(), invoke(), _Flag, _History (+7 more)

### Community 140 - "build_tools"
Cohesion: 0.12
Nodes (5): DraftSubmission, build_tools(), retrieve(), status(), _error_cost()

### Community 141 - "test_cli.py"
Cohesion: 0.18
Nodes (9): test_config_error_exits_2(), boom(), test_ingest_directory_is_deterministic_and_duplicate_is_free(), test_ingest_disabled_configuration_never_calls_provider(), test_ingest_failure_exit_and_retry_stored(), test_ingest_invalid_source_does_not_stop_other_files(), test_ingest_limits_batch_without_partial_side_effects(), test_retry_stored_indexes_old_uploads_without_recovering_other_process_jobs() (+1 more)

### Community 142 - "test_dbapi_commit_handoff_arbitrates_cancellation"
Cohesion: 0.47
Nodes (4): test_dbapi_commit_handoff_arbitrates_cancellation(), gate(), gate_before_dbapi(), gate_inside_dbapi()

### Community 143 - "RunRow"
Cohesion: 0.33
Nodes (6): get_run(), list_runs(), start_run(), RunRow, Ticket, run_view()

### Community 144 - "indexDocument"
Cohesion: 0.60
Nodes (5): beginMutation(), deleteDocument(), finishMutation(), indexDocument(), upload()

### Community 148 - "components-ai-thought-chain.tsx"
Cohesion: 0.12
Nodes (17): Status, StatusIcon(), statusStyles, StepContext, StepContextType, ThoughtChain(), ThoughtChainContent(), ThoughtChainItem() (+9 more)

### Community 149 - "json"
Cohesion: 0.49
Nodes (5): TicketOutcome, outcome_to_dict(), outcome_to_row(), test_failed_outcome_and_dict_form(), test_full_outcome_is_json_safe()

### Community 151 - "test_recovery_regressions.py"
Cohesion: 0.40
Nodes (9): command(), create(), test_actual_app_restart_reconciles_failed_placeholder(), test_failed_review_retry_cannot_reopen_submitted_session(), test_original_payload_identity_survives_sanitization(), test_publication_failure_is_retryable_without_restart(), test_receipt_reference_is_preserved(), test_stale_attempt_audit_is_retained_once_with_attempt_identity() (+1 more)

### Community 152 - "dispatch_intake"
Cohesion: 0.39
Nodes (6): dispatch_intake(), test_review_to_employee_handoff(), _submit(), test_committed_but_unscheduled_ticket_survives_recovery(), test_failed_outcome_save_preserves_placeholder_and_reconciles_counts(), test_processing_ticket_rejects_review()

### Community 153 - "Ticket flow charts"
Cohesion: 0.29
Nodes (6): 1. Outcome, 5. Language, 7. Sentences, 8. Tests, 9. Files, Ticket flow charts

### Community 156 - "employee-frontend/src/components/theme-provider.tsx"
Cohesion: 0.21
Nodes (11): disableTransitionsTemporarily(), getSystemTheme(), isEditableTarget(), isTheme(), ResolvedTheme, Theme, THEME_VALUES, ThemeProvider() (+3 more)

### Community 158 - "lookup.py"
Cohesion: 0.17
Nodes (17): ExtractedField, LookupResult, _as_date(), _iqd_amount(), match_transaction(), TransactionRepo, state(), _ex() (+9 more)

### Community 159 - "7. Review and submission"
Cohesion: 0.50
Nodes (4): 7. Review and submission, Processing lifecycle, Review, Submission transaction

### Community 164 - "factory.py"
Cohesion: 0.20
Nodes (9): make_draft_model(), DraftChatOpenRouter, response_payload(), run_provider_pipeline(), send(), search_response(), test_empty_choices_escalates_and_keeps_paid_response_usage(), test_failed_response_id_is_deduplicated_against_earlier_success() (+1 more)

### Community 167 - "build_pipeline"
Cohesion: 0.13
Nodes (20): SqlTransactionRepo, build_pipeline(), ConfigError, make_gemini_llm(), make_jev_client(), model_ids(), run_batch(), GeminiAnalysis (+12 more)

## Ambiguous Edges - Review These
- `Fraud Report` → `Plan 1 Live Smoke`  [AMBIGUOUS]
  README.md · relation: conceptually_related_to

## Knowledge Gaps
- **91 isolated node(s):** `zaincash-support`, `@base-ui/react`, `@fontsource-variable/plus-jakarta-sans`, `@fontsource/tajawal`, `@tailwindcss/vite` (+86 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 1023 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **48 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Settings` connect `Settings` to `intake/model.py`, `test_llm.py`, `pytest`, `intake/conftest.py`, `agent.py`, `submission.py`, `test_rag_api.py`, `test_cli.py`, `UploadedDocument`, `test_recovery_regressions.py`, `CredentialChecker`, `test_embeddings.py`, `test_draft_tools.py`, `test_kb_service.py`, `factory.py`, `build_pipeline`, `fact`, `support_test`, `attachments.py`, `agent.py`, `main.py`, `Credentials`, `taxonomy.py`, `db/repository.py`, `Synthetic demo readiness`, `test_final_fix_handoff.py`?**
  _High betweenness centrality (0.102) - this node is a cross-community bridge._
- **Are the 33 inferred relationships involving `Settings` (e.g. with `_command_settings()` and `_run_in_memory()`) actually correct?**
  _`Settings` has 33 INFERRED edges - model-reasoned connections that need verification._
- **What connects `zaincash-support`, `@base-ui/react`, `@fontsource-variable/plus-jakarta-sans` to the rest of the system?**
  _91 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `intake/types.ts` be split into smaller, more focused modules?**
  _Cohesion score 0.11491935483870967 - nodes in this community are weakly interconnected._
- **Why does `HTTP contract (implemented in Tasks 4–5)` connect `TurnContext` to `guardrails.py`, `intake/model.py`, `Customer Conversation Intake Implementation Plan`, `IntakeController`, `lib/types.ts`, `db/repository.py`, `attachments.py`, `web/src/components/theme-provider.tsx`?**
  _High betweenness centrality (0.094) - this node is a cross-community bridge._
- **Are the 24 inferred relationships involving `KnowledgeService` (e.g. with `Settings` and `UploadedDocument`) actually correct?**
  _`KnowledgeService` has 24 INFERRED edges - model-reasoned connections that need verification._

### Low-confidence Hints
_AMBIGUOUS edges — the extractor was unsure. Verify before acting on these._

- **What is the exact relationship between `Fraud Report` and `Plan 1 Live Smoke`?**
  _Edge tagged AMBIGUOUS (relation: conceptually_related_to) - confidence is low._