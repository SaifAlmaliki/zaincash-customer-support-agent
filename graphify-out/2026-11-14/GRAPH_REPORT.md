# Graph Report - zaincash-support  (2026-11-13)

## Corpus Check
- 401 files · ~446,178 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 25 file(s) not represented in the graph (top: (none) 15, .jsonl 4, .css 4)

## Summary
- 4014 nodes · 13360 edges · 152 communities (126 shown, 26 thin omitted)
- Extraction: 85% EXTRACTED · 15% INFERRED · 0% AMBIGUOUS · INFERRED: 2018 edges (avg confidence: 0.93)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `cf827ee0`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- TypeSafeProvider
- Step
- pytest
- TurnStore
- investigation.py
- test_catalog.py
- Card
- Customer conversation intake for ZainCash support
- lib/api.ts
- IntakeController
- FakeJevRunnable
- test_rag_api.py
- employee-frontend/package.json
- QueuePage.tsx
- Support Taxonomy Categories
- ui/package.json
- ModelsPage.tsx
- users-frontend/package.json
- make_output
- test_draft_guardrails.py
- web/package.json
- test_interview_scenarios.py
- compilerOptions
- employee-frontend/components.json
- FakeProvider
- compilerOptions
- web/src/components/theme-provider.tsx
- EmbeddingError
- Classify and Extract Prompts
- test_draft_tools.py
- Pipeline Design Spec
- Batch Runner
- Drafting Plan Concepts
- test_kb_service.py
- search_knowledge_base
- web/components.json
- NewBatchPage.tsx
- ui/components.json
- Settings
- Guided intake interview — design
- Vite Config
- Human Review Gate
- compilerOptions
- PipelineState
- compilerOptions
- KnowledgeError
- Human Flag Tool
- Recent Transactions Tool
- Ticket History Tool
- Lookup Transaction Tool
- Search Transactions Tool
- Submit Draft Tool
- Project Root
- parse_document
- pytest
- contracts.ts
- fact
- Plan 3 RAG Drafting Implementation Plan
- lib/types.ts
- IntakePage.tsx
- tasks
- knowledge.py
- ChangeModelDialog.tsx
- Review Focus
- PipelineState
- main.py
- demo-readiness.md
- Customer Conversation Intake Implementation Plan
- ZainCash Support Workspace
- ModelSettingsStore
- FakeJevRunnable
- parse.py
- test_workspace_api.py
- test_interview_api.py
- devDependencies
- tools.py
- factory.py
- uuid
- devDependencies
- devDependencies
- fakes.py
- ticket-flow.ts
- compilerOptions
- collapsible.tsx
- pydantic
- dependencies
- InvalidEvidence
- dependencies
- compilerOptions
- ref_vitest
- intake/api.ts
- test_final_fix_handoff.py
- scripts
- lookup.py
- compilerOptions
- Maintainability and stale-code refactor — design specification
- web/tsconfig.json
- employee-frontend/tsconfig.json
- exports
- IntakePage.tsx
- scripts
- users-frontend/README.md
- policy.py
- TurnContext
- admin.py
- guardrails.py
- intake/model.py
- test_llm.py
- intake.py
- Review Focus
- _DatabaseCall
- test_dbapi_commit_handoff_arbitrates_cancellation
- config.py
- jev.py
- submission.py
- db/repository.py
- cli.py
- knowledge_runtime.py
- probe.py
- components-ai-thought-chain.tsx
- intake/README.md
- taxonomy.py
- create_app
- create_app
- ZainCash support: architecture and ticket flow {#support-overview}
- IntakePage.test.tsx
- employee-frontend/src/components/theme-provider.tsx
- agent.py
- TicketRow
- test_embedding_switch.py
- Customer phone identity design
- api-entrypoint.sh
- ProviderRegistry
- test_workspace_schema.py
- build_pipeline
- support_test
- intake/contracts.py
- Deviations from the spec (intentional, small)
- test_submission.py

## God Nodes (most connected - your core abstractions)
1. `Settings` - 189 edges
2. `Step` - 108 edges
3. `ModelChoice` - 91 edges
4. `KnowledgeService` - 85 edges
5. `ActiveModels` - 74 edges
6. `fact()` - 72 edges
7. `useCopy()` - 68 edges
8. `context()` - 65 edges
9. `message()` - 60 edges
10. `IntakeController` - 55 edges

## Surprising Connections (you probably didn't know these)
- `Repeatable local walkthrough` --references--> `Settings`  [INFERRED]
  docs/demo-readiness.md → backend/app/config.py
- `Task 1: Canonical phone helper (backend)` --references--> `InvalidPhone`  [INFERRED]
  docs/superpowers/plans/2026-11-13-customer-phone-identity.md → backend/app/customers/phone.py
- `Ticket write paths` --references--> `upsert_tickets()`  [INFERRED]
  docs/superpowers/specs/2026-11-13-customer-phone-identity-design.md → backend/app/db/repository.py
- `Existing data` --references--> `upgrade_workspace_schema()`  [INFERRED]
  docs/superpowers/specs/2026-11-13-customer-phone-identity-design.md → backend/app/db/workspace_schema.py
- `Task 9: Repair the Five-Record JSONL Baseline Fixture` --references--> `load_jsonl()`  [INFERRED]
  docs/superpowers/plans/2026-11-02-backend-maintainability.md → backend/app/ingest.py

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **Cascade Classification Path** — docs_superpowers_specs_2026_10_07_support_pipeline_design_cascade, docs_superpowers_plans_2026_10_07_plan1_core_pipeline_part2_jev_classifier, docs_superpowers_plans_2026_10_07_plan1_core_pipeline_part2_gemini_classifier, docs_superpowers_plans_2026_10_07_plan1_core_pipeline_part2_cascade_combine, readme_human_approval [EXTRACTED 1.00]
- **Drafting Agent Toolset** — backend_app_pipeline_runner_lookup_transaction, backend_app_pipeline_runner_search_transactions, backend_app_pipeline_runner_get_customer_recent_transactions, backend_app_pipeline_runner_get_customer_ticket_history, backend_app_pipeline_runner_check_service_status, backend_app_pipeline_runner_search_knowledge_base, backend_app_pipeline_runner_flag_for_human, backend_app_pipeline_runner_submit_draft [EXTRACTED 1.00]
- **Ticket Processing Stage Flow** — backend_app_pipeline_runner_prepare, backend_app_pipeline_runner_jev_classify, backend_app_pipeline_runner_gemini_classify, backend_app_pipeline_runner_extract, backend_app_pipeline_runner_lookup, backend_app_pipeline_runner_decide, backend_app_pipeline_runner_draft [EXTRACTED 1.00]

## Communities (152 total, 26 thin omitted)

### Community 0 - "TypeSafeProvider"
Cohesion: 0.13
Nodes (8): UnsupportedOperation, TypeSafeProvider, test_typesafe_status_and_unsupported_chat(), 4.2 Provider protocol, 4.6 Options, 4.7 Timeouts, 4.8 Embedding switch (short pause), 4. Backend design

### Community 1 - "Step"
Cohesion: 0.08
Nodes (35): ActiveModels, ModelChoice, Step, batch_concurrency(), _current_models(), _local_pipeline(), ticket_timeout_s(), fake_registry() (+27 more)

### Community 2 - "pytest"
Cohesion: 0.20
Nodes (36): _tool_chat(), answer(), call(), draft_state(), script(), submit(), submit(), drafter() (+28 more)

### Community 3 - "TurnStore"
Cohesion: 0.18
Nodes (10): OperationClaim, RevisionConflict, _jsonable(), TurnStore, test_recovered_attempt_cannot_publish_stale_output(), HTTP contract (implemented in Tasks 4–5), Task 4: Resumable graph turns, review and customer API, Task 9: End-to-end handoff, live vision evidence and runbook (+2 more)

### Community 4 - "investigation.py"
Cohesion: 0.11
Nodes (21): parse_dt(), TxnRecord, DraftToolInputError, _datetime(), _days(), _field(), _involves(), _phone() (+13 more)

### Community 5 - "test_catalog.py"
Cohesion: 0.20
Nodes (9): CatalogCache, step_catalog(), ProbeResult, BrokenStatusProvider, test_a_provider_whose_status_check_raises_is_listed_as_unreachable(), test_catalog_errors_stay_per_provider_and_cache_respects_ttl(), test_classify_catalog_only_offers_typesafe(), test_step_catalog_filters_and_marks_unknown() (+1 more)

### Community 6 - "Card"
Cohesion: 0.17
Nodes (41): Task 5: Extract presentational DocumentList and KnowledgeReadiness components, Task 9: Employee app — required phone, queue identity and search, batch entry, 6.4 Focused view extraction, Card(), CardContent(), CardHeader(), CardTitle(), Input() (+33 more)

### Community 7 - "Customer conversation intake for ZainCash support"
Cohesion: 0.06
Nodes (31): 10. Verification and acceptance criteria, 11. Delivery and review, 1. Outcome and agreed requirements, 2. Current implementation and integration points, 3. Approach and boundaries, 4. Conversation state and turn flow, 5. Facts, evidence, and readiness, 6. Language and screenshot behavior (+23 more)

### Community 8 - "lib/api.ts"
Cohesion: 0.09
Nodes (39): Admin model configuration — employee frontend implementation plan, Backend API contract used here, File structure, Global Constraints, Review Focus, Task 1: API types, admin session and admin requests, Task 3: Model choice logic and the change dialog, Task 14: Evaluation view helpers (+31 more)

### Community 9 - "IntakeController"
Cohesion: 0.15
Nodes (12): Task 6: Customer API client and resumable UI state, Task 1: Cleanup-first removal of reference-verified dead code and dependencies, Task 7: Preserve resume-unavailable state across `startNew`, Task 7: Intake app data layer — phone helper, contracts, API, controller, Task 7: Customer frontend data layer, ControllerState, emptyState(), IntakeController (+4 more)

### Community 10 - "FakeJevRunnable"
Cohesion: 0.12
Nodes (19): CredentialCheck, CredentialChecker, DegradedCredentialChecker, _finite_nonnegative(), _get(), JevCredentialChecker, ResponseRunnable, test_bad_usage_cannot_poison_cost() (+11 more)

### Community 11 - "test_rag_api.py"
Cohesion: 0.09
Nodes (25): KnowledgeExecutionError, index_deadlines(), settings(), client(), evidence_client(), test_actual_guardrail_failure_is_separate_from_reply(), test_concurrent_index_requests_share_active_work(), test_disabled_or_missing_provider_stores_without_indexing() (+17 more)

### Community 12 - "employee-frontend/package.json"
Cohesion: 0.06
Nodes (30): @base-ui/react, class-variance-authority, cn, eslint, @eslint/js, eslint-plugin-react-hooks, eslint-plugin-react-refresh, @fontsource/tajawal (+22 more)

### Community 14 - "QueuePage.tsx"
Cohesion: 0.10
Nodes (54): Task 3: Split RunDetailPage and introduce bounded run-result loading, Global Constraints, Per-model Evaluation Implementation Plan — Part 3 of 3 (frontend, translations, verification), Task 12: Locale parity test and translated Runs pages, Task 15: Provenance, headline metrics, comparison table and empty state, Task 17: Run dialog, progress, page assembly, route and styles, Task 18: Documentation, full verification and manual check, Task 10: Employee app — customer page and ticket header link (+46 more)

### Community 15 - "Support Taxonomy Categories"
Cohesion: 0.21
Nodes (22): lookup, Account KYC, Account & Security, Agent Dispute, Agent Network, App Bug, Bill Payment, Card Issue (+14 more)

### Community 16 - "ui/package.json"
Cohesion: 0.08
Nodes (24): @base-ui/react, class-variance-authority, cn, eslint, @eslint/js, eslint-plugin-react-hooks, eslint-plugin-react-refresh, @fontsource/tajawal (+16 more)

### Community 17 - "ModelsPage.tsx"
Cohesion: 0.08
Nodes (40): Task 2: Strings, the AI locality chip, run models and the batch switch message, App(), CustomerPage, EvaluationPage, InsightsPage, KnowledgePage, ModelsPage, NewBatchPage (+32 more)

### Community 18 - "users-frontend/package.json"
Cohesion: 0.08
Nodes (23): turbo, devDependencies, prettier, prettier-plugin-tailwindcss, turbo, typescript, engines, node (+15 more)

### Community 19 - "make_output"
Cohesion: 0.09
Nodes (41): build_graph(), PipelineDeps, InMemoryTransactionRepo, load_taxonomy(), tax(), FakeClassifier, make_output(), pipeline() (+33 more)

### Community 20 - "test_draft_guardrails.py"
Cohesion: 0.15
Nodes (28): LookupResult, requests_credentials(), make_ticket(), check(), state(), test_aggregation_is_deduplicated_and_has_no_state_side_effects(), test_amount_occurrences_keep_their_own_currency_and_sign(), test_avoid_sharing_warning_does_not_excuse_a_later_request() (+20 more)

### Community 21 - "web/package.json"
Cohesion: 0.05
Nodes (41): clsx, jsdom, tailwind-merge, @testing-library/jest-dom, @testing-library/react, @testing-library/user-event, @workspace/ui, dependencies (+33 more)

### Community 22 - "test_interview_scenarios.py"
Cohesion: 0.31
Nodes (9): analyze_calls(), Chat, source_of(), summary(), test_complete_report_goes_straight_to_review(), test_no_reference_number_still_gives_a_complete_report(), test_vague_report_is_interviewed_into_a_complete_ticket(), updates() (+1 more)

### Community 23 - "compilerOptions"
Cohesion: 0.08
Nodes (23): compilerOptions, allowArbitraryExtensions, allowImportingTsExtensions, erasableSyntaxOnly, jsx, lib, module, moduleDetection (+15 more)

### Community 24 - "employee-frontend/components.json"
Cohesion: 0.09
Nodes (21): aliases, components, hooks, lib, ui, utils, iconLibrary, menuAccent (+13 more)

### Community 25 - "FakeProvider"
Cohesion: 0.13
Nodes (13): probe(), FakeProvider, _registry(), StructuredChat, test_draft_probe_requires_a_correct_tool_call(), test_embed_and_classify_probes(), test_every_step_has_a_probe(), test_intake_probe_sends_an_image_and_needs_parsed_output() (+5 more)

### Community 26 - "compilerOptions"
Cohesion: 0.09
Nodes (22): compilerOptions, allowArbitraryExtensions, allowImportingTsExtensions, erasableSyntaxOnly, jsx, lib, module, moduleDetection (+14 more)

### Community 27 - "web/src/components/theme-provider.tsx"
Cohesion: 0.10
Nodes (19): App(), controller, disableTransitionsTemporarily(), getSystemTheme(), isEditableTarget(), isTheme(), ResolvedTheme, Theme (+11 more)

### Community 28 - "EmbeddingError"
Cohesion: 0.06
Nodes (46): EmbeddingBatch, EmbeddingError, _nonnegative_number(), OpenAICompatibleEmbedder, OpenRouterEmbedder, _ordered_vectors(), _response_cost(), _percentile() (+38 more)

### Community 29 - "Classify and Extract Prompts"
Cohesion: 0.33
Nodes (7): extract, gemini_classify, Pipeline Graph Orchestration, jev_classify, prepare, GeminiClassifier, JevClassifier

### Community 30 - "test_draft_tools.py"
Cohesion: 0.10
Nodes (30): ErrorEmbedder, settings(), state(), test_all_eight_tools_and_seven_parallel_calls_execute_only_six(), test_context_copies_input_and_rejects_raising_hard_call_limit(), test_database_faults_remain_distinct_and_record_paid_search_cost(), test_discovered_ref_can_be_inspected_but_not_promoted_to_match(), test_exact_and_fuzzy_queries_are_scoped_and_never_confirm_candidates() (+22 more)

### Community 31 - "Pipeline Design Spec"
Cohesion: 0.25
Nodes (7): pgvector Postgres Service, pgdata Volume, Support Pipeline Design, Gemini 3.8 Flash, Jev, OpenRouter, ZainCash Support Pipeline

### Community 32 - "Batch Runner"
Cohesion: 0.29
Nodes (7): Plan 1 Part 2, Batch Runner, NullDrafter, Plan 1 Core Pipeline, Live Batch API, Plan 1 Live Smoke, NullDrafter

### Community 33 - "Drafting Plan Concepts"
Cohesion: 0.25
Nodes (5): check_service_status, decide, draft, Five-Plan Roadmap, Weekly Pattern Report

### Community 34 - "test_kb_service.py"
Cohesion: 0.08
Nodes (39): Embedder, KnowledgeChunk, KnowledgeService, FakeEmbedder, GatedEmbedder, LateEmbedder, PaidEmbedder, count_chunks() (+31 more)

### Community 36 - "web/components.json"
Cohesion: 0.10
Nodes (19): aliases, components, hooks, lib, ui, utils, iconLibrary, menuAccent (+11 more)

### Community 38 - "NewBatchPage.tsx"
Cohesion: 0.08
Nodes (32): Task 16: Model detail, confusion matrix and predictions drawer, 6.1 Route and access, 6.2 Page, 6.3 Change dialog, 6.5 Text and direction, 6. Employee-frontend design, 5.2 Page structure, 5.3 Text and direction (+24 more)

### Community 39 - "ui/components.json"
Cohesion: 0.10
Nodes (19): aliases, components, hooks, lib, ui, utils, iconLibrary, menuAccent (+11 more)

### Community 40 - "Settings"
Cohesion: 0.07
Nodes (22): Settings, draft_timeout_s(), env_defaults(), intake_timeout_s(), test_relative_upload_directory_is_rooted_in_the_repository(), _settings(), test_eligibility(), test_env_defaults_match_todays_settings() (+14 more)

### Community 41 - "Guided intake interview — design"
Cohesion: 0.07
Nodes (27): 2. API contract, 3. Chat screen, 4. Review card, Actions, Additional issues, Approach, Composer hints, Copy (+19 more)

### Community 43 - "Human Review Gate"
Cohesion: 0.25
Nodes (4): support CLI, Support Workspace UI Plan, Review API, Workspace UI Verification

### Community 44 - "compilerOptions"
Cohesion: 0.12
Nodes (16): compilerOptions, allowImportingTsExtensions, erasableSyntaxOnly, lib, module, moduleDetection, noEmit, noFallthroughCasesInSwitch (+8 more)

### Community 46 - "PipelineState"
Cohesion: 0.06
Nodes (18): DraftResult, _default_retry(), _Nodes, _retryable(), _error_cost(), _has_response_usage(), _number(), Drafter (+10 more)

### Community 47 - "compilerOptions"
Cohesion: 0.12
Nodes (16): compilerOptions, allowImportingTsExtensions, erasableSyntaxOnly, lib, module, moduleDetection, noEmit, noFallthroughCasesInSwitch (+8 more)

### Community 48 - "KnowledgeError"
Cohesion: 0.24
Nodes (4): DocumentNotFoundError, IndexAttemptLostError, KnowledgeError, Task 14: Preserve Safe Knowledge 503s and Log Only Unexpected Diagnostic Types

### Community 57 - "parse_document"
Cohesion: 0.15
Nodes (22): DocumentParseError, parse_document(), make_pdf(), test_arabic_text_and_bom_are_preserved(), test_blank_pdf_tells_operator_to_use_ocr(), test_chunk_limit_is_enforced(), test_chunking_is_deterministic_bounded_and_overlapping(), test_empty_text_has_an_actionable_error() (+14 more)

### Community 58 - "pytest"
Cohesion: 0.05
Nodes (65): AttachmentStore, _display_name(), Attachment, Credentials, ImageInput, Message, SessionView, IntakeAttachmentRow (+57 more)

### Community 59 - "contracts.ts"
Cohesion: 0.17
Nodes (33): Task 5: Add complete dependency-free API and persisted-session guards, createIntakeApi(), ANSWER_KINDS, CHOICES, FACT_STATUSES, finiteNonnegative(), invalid(), isRecord() (+25 more)

### Community 60 - "fact"
Cohesion: 0.11
Nodes (58): Analysis, EvidenceRef, Fact, Readiness, merge_analysis(), remove_attachment_evidence(), context(), fact() (+50 more)

### Community 61 - "Plan 3 RAG Drafting Implementation Plan"
Cohesion: 0.18
Nodes (11): Completion and review record — 2026-10-17, Execution handoff, File map and shared interfaces, Global Constraints, Plan 3 RAG Drafting Implementation Plan, Plan self-review, Review Focus, Task 1: Testable parsing and embedding boundary (+3 more)

### Community 62 - "lib/types.ts"
Cohesion: 0.07
Nodes (35): Task 13: Evaluation types, API client, formatters, copy and report import, acceptIndexRequest(), canRequestIndex(), PendingIndexes, persistPendingIndexes(), pollKnowledge(), refresh(), stop() (+27 more)

### Community 63 - "IntakePage.tsx"
Cohesion: 0.10
Nodes (30): Task 8: Chat screen — instant bubble, typing, reasons, quick replies, composer hints, users-frontend, AgentChat, AgentChatProps, AgentMessage, AssistantText(), AttachedFile, AttachedImage (+22 more)

### Community 64 - "tasks"
Cohesion: 0.11
Nodes (18): dependsOn, inputs, outputs, cache, persistent, dependsOn, dependsOn, $schema (+10 more)

### Community 65 - "knowledge.py"
Cohesion: 0.08
Nodes (28): session(), _configured(), delete_document(), download_document(), index_document(), list_chunks(), list_documents(), _require_provider() (+20 more)

### Community 66 - "ChangeModelDialog.tsx"
Cohesion: 0.12
Nodes (33): ConfirmDialog(), Button(), Dialog(), DialogContent(), DialogDescription(), DialogFooter(), DialogHeader(), DialogOverlay() (+25 more)

### Community 67 - "Review Focus"
Cohesion: 0.20
Nodes (10): Customer Phone Identity Implementation Plan, Global Constraints, Review Focus, Spec refinements (decided while planning), Task 11: Whole-system verification, Task 1: Canonical phone helper (backend), Task 8: Intake app UI — phone screen, profile chip, change number, receipt, Task 10: Grouped review card with answer buttons (+2 more)

### Community 68 - "PipelineState"
Cohesion: 0.11
Nodes (18): 10. Remaining demo roadmap, 1. Intent and acceptance criteria, 3. Provider and configuration, 4. Knowledge ingestion and persistence, 5. Retrieval and evidence, 6. Bounded investigation agent, 7. Draft guardrails and failure outcomes, 8. Pipeline, API, CLI and UI integration (+10 more)

### Community 69 - "main.py"
Cohesion: 0.07
Nodes (29): get_customer(), get_session(), get_result(), list_results(), read_intake_attachment(), review_result(), get_run(), list_runs() (+21 more)

### Community 70 - "demo-readiness.md"
Cohesion: 0.24
Nodes (5): Fictional RAG walkthrough inputs, Evidence by layer, Known limitations and remaining work, Repeatable local walkthrough, Synthetic demo readiness

### Community 71 - "Customer Conversation Intake Implementation Plan"
Cohesion: 0.20
Nodes (8): Completion audit — 2026-10-18, Customer Conversation Intake Implementation Plan, Execution conventions and repository baseline, File map and dependency order, Global Constraints, Plan review and execution handoff, Review Focus, Spec coverage and acceptance map

### Community 72 - "ZainCash Support Workspace"
Cohesion: 0.22
Nodes (9): Current capability boundaries, Data source, Modular file map, Open the right project, Run locally, shadcn conventions, Verification, Workflow (+1 more)

### Community 73 - "ModelSettingsStore"
Cohesion: 0.21
Nodes (5): _iso(), ModelSettingsStore, knowledge_configured(), make_knowledge_service(), test_only_jev_mode_is_configured_and_retired_modes_are_rejected()

### Community 74 - "FakeJevRunnable"
Cohesion: 0.32
Nodes (10): FakeJevRunnable, _criteria(), _run(), test_low_top_probability_is_uncertain(), test_one_main_call_with_all_questions(), test_order_check_uses_reversed_options(), test_order_disagreement_is_uncertain(), test_priority_level_maps_to_p_label() (+2 more)

### Community 75 - "parse.py"
Cohesion: 0.48
Nodes (4): TextChunk, _append_chunks(), _check_extracted_size(), _parse_pdf()

### Community 76 - "test_workspace_api.py"
Cohesion: 0.15
Nodes (14): review_payload(), start_run(), test_batch_and_queue_expose_real_results(), test_batch_failure_is_isolated_and_conflicting_ids_rejected(), test_customer_profile_lists_the_latest_result_of_each_ticket(), test_progress_counts_only_durable_results_after_save_failure(), fail_one_save(), test_result_list_paginates_filters_and_run_id() (+6 more)

### Community 77 - "test_interview_api.py"
Cohesion: 0.22
Nodes (18): analyze_calls(), ask(), complete_without_reference(), opening(), opening_with_amount(), reference_answer(), send(), start() (+10 more)

### Community 79 - "devDependencies"
Cohesion: 0.12
Nodes (16): devDependencies, eslint, @eslint/js, eslint-plugin-react-hooks, eslint-plugin-react-refresh, globals, prettier, prettier-plugin-tailwindcss (+8 more)

### Community 81 - "tools.py"
Cohesion: 0.07
Nodes (20): DraftAlreadySubmitted, DraftSubmission, DraftToolLimit, _bounded(), visit(), build_tools(), flag(), guarded() (+12 more)

### Community 82 - "factory.py"
Cohesion: 0.33
Nodes (7): response_payload(), run_provider_pipeline(), send(), search_response(), test_empty_choices_escalates_and_keeps_paid_response_usage(), test_failed_response_id_is_deduplicated_against_earlier_success(), test_other_conversion_value_errors_remain_unexpected()

### Community 93 - "uuid"
Cohesion: 0.35
Nodes (9): command(), create(), test_actual_app_restart_reconciles_failed_placeholder(), test_failed_review_retry_cannot_reopen_submitted_session(), test_original_payload_identity_survives_sanitization(), test_publication_failure_is_retryable_without_restart(), test_receipt_reference_is_preserved(), test_stale_attempt_audit_is_retained_once_with_attempt_identity() (+1 more)

### Community 94 - "devDependencies"
Cohesion: 0.11
Nodes (19): devDependencies, eslint, @eslint/js, eslint-plugin-react-hooks, eslint-plugin-react-refresh, globals, jsdom, @tailwindcss/vite (+11 more)

### Community 95 - "devDependencies"
Cohesion: 0.17
Nodes (12): devDependencies, eslint, @eslint/js, eslint-plugin-react-hooks, eslint-plugin-react-refresh, globals, tailwindcss, @types/node (+4 more)

### Community 96 - "fakes.py"
Cohesion: 0.11
Nodes (27): LLMUnavailable, FieldPick, normalize(), FieldExtractor, _field(), fill_gaps(), finalize(), _is_weak() (+19 more)

### Community 97 - "ticket-flow.ts"
Cohesion: 0.06
Nodes (63): Task 1: Sentence catalog, Task 2: Which step is open, Task 3: Received, produced, and drafting events, Task 4: Mermaid source, Task 5: Draw the charts on the ticket page, 1. Outcome, 2. Scope, 4. Which step is open (+55 more)

### Community 99 - "compilerOptions"
Cohesion: 0.14
Nodes (13): compilerOptions, jsx, lib, module, moduleResolution, noEmit, paths, skipLibCheck (+5 more)

### Community 101 - "pydantic"
Cohesion: 0.23
Nodes (6): CitationSource, _Draft, draft_evidence(), _Guardrail, _TraceModel, _validated()

### Community 102 - "dependencies"
Cohesion: 0.12
Nodes (16): dependencies, @base-ui/react, class-variance-authority, cn, @fontsource/tajawal, @fontsource-variable/plus-jakarta-sans, lucide-react, motion (+8 more)

### Community 103 - "InvalidEvidence"
Cohesion: 0.11
Nodes (31): ReviewText, canonical_digits(), normalize_reported_date(), InvalidEvidence, _apply(), _check_reference(), _compact(), checked_update() (+23 more)

### Community 104 - "dependencies"
Cohesion: 0.20
Nodes (10): dependencies, @base-ui/react, class-variance-authority, cn, @fontsource/tajawal, @fontsource-variable/plus-jakarta-sans, react, react-dom (+2 more)

### Community 105 - "compilerOptions"
Cohesion: 0.17
Nodes (11): compilerOptions, jsx, lib, module, moduleResolution, outDir, skipLibCheck, strict (+3 more)

### Community 106 - "ref_vitest"
Cohesion: 0.06
Nodes (38): Task 8: Employee evidence panel and processing state, Employee Frontend Maintainability Implementation Plan, Global Constraints, Review Focus, Task 1: Remove reference-verified dead exports, components, and the Mermaid dependency, Task 2: Migrate active TicketFlow coverage, then retire the legacy trace/chart cluster, Task 4: Extract and test the pure queue projection, Task 6: Repair ExtractedField fixtures and make standalone typecheck real (+30 more)

### Community 107 - "intake/api.ts"
Cohesion: 0.09
Nodes (29): Task 4: Make pending operations discriminated and use one request identity, IntakeApi, INTAKE_FALLBACK_MESSAGE, fileIdentity(), OwnedImage(), factText(), ReviewPanel(), AnswerKind (+21 more)

### Community 108 - "test_final_fix_handoff.py"
Cohesion: 0.09
Nodes (22): Passage, Checker, Knowledge, assert_completed_evidence(), faulty_knowledge(), read(), outer_deadlines(), PaidEmbeddings (+14 more)

### Community 111 - "scripts"
Cohesion: 0.25
Nodes (8): scripts, build, dev, format, lint, preview, test, typecheck

### Community 112 - "lookup.py"
Cohesion: 0.16
Nodes (17): ExtractedField, _as_date(), _iqd_amount(), match_transaction(), TransactionRepo, txn_from_dict(), _ex(), _match() (+9 more)

### Community 113 - "compilerOptions"
Cohesion: 0.29
Nodes (6): compilerOptions, module, moduleResolution, skipLibCheck, strict, target

### Community 114 - "Maintainability and stale-code refactor — design specification"
Cohesion: 0.12
Nodes (15): 10. Verification and acceptance, 1. Outcome and success criteria, 2. Audit baseline, 3. Selected approach and sequence, 4. Boundaries and non-goals, 8.1 Approved deletions, 8.2 Docker and documentation, 8.3 Graphify outputs (+7 more)

### Community 116 - "web/tsconfig.json"
Cohesion: 0.33
Nodes (5): compilerOptions, paths, files, @workspace/ui/*, references

### Community 117 - "employee-frontend/tsconfig.json"
Cohesion: 0.40
Nodes (4): compilerOptions, paths, files, references

### Community 118 - "exports"
Cohesion: 0.40
Nodes (5): exports, ./components/*, ./globals.css, ./hooks/*, ./lib/*

### Community 119 - "IntakePage.tsx"
Cohesion: 0.06
Nodes (32): Global Constraints, Intake Chat UI Implementation Plan, Task 1: Put the summary and receipt in the thread, Task 2: Put screenshots inside the composer, Task 3: Apply the workspace chat styles, Task 4: Check the page in the browser, Customer Frontend Maintainability Implementation Plan, Global Constraints (+24 more)

### Community 120 - "scripts"
Cohesion: 0.50
Nodes (4): scripts, format, lint, typecheck

### Community 122 - "policy.py"
Cohesion: 0.08
Nodes (61): AskedQuestion, IntakeState, Question, QuestionRecord, answer_choices(), answer_kind(), ask_for(), ask_once_keys() (+53 more)

### Community 123 - "TurnContext"
Cohesion: 0.16
Nodes (10): quick_answer(), TurnContext, TurnResult, IntakeGraph, _invitation(), test_graph_budget_uses_the_pinned_choice_and_timeout(), choice_for(), test_pin_failure_is_reported_as_model_unavailable() (+2 more)

### Community 125 - "admin.py"
Cohesion: 0.12
Nodes (18): audit(), catalog(), _check_provider(), ChoiceInput, embedding_switch(), ModelOptions, models(), ProbeInput (+10 more)

### Community 126 - "guardrails.py"
Cohesion: 0.07
Nodes (45): sanitize_intake_text(), Candidate, _add(), find_candidates(), normalize_phone(), _overlaps(), parse_amount(), resolve_date() (+37 more)

### Community 129 - "intake/model.py"
Cohesion: 0.09
Nodes (29): ModelCall, ModelUnavailable, _analysis_prompt(), _bounded_context(), _guard_size(), IntakeModel, ModelBudget, _record() (+21 more)

### Community 130 - "test_llm.py"
Cohesion: 0.09
Nodes (15): Sample, StructuredChatLLM, StructuredLLM, make_draft_model(), make_gemini_llm(), _llm(), _S, test_draft_model_uses_millisecond_timeout_and_disables_sdk_retries() (+7 more)

### Community 131 - "intake.py"
Cohesion: 0.17
Nodes (22): ask_question(), create_session(), _credentials(), _dump(), get_session(), post_message(), read_attachment(), remove_attachment() (+14 more)

### Community 132 - "Review Focus"
Cohesion: 0.11
Nodes (18): api(), Global Constraints, Repository Hygiene Maintainability Implementation Plan, Review Focus, Task 1: Establish the safety baseline and remove tracked Graphify cache contents, Task 2: Delete the superseded architecture HTML after a fresh reference check, Task 3: Remove confirmed stale local runtime state and the duplicate screenshot, Task 4: Repair only current setup and processing documentation (+10 more)

### Community 133 - "_DatabaseCall"
Cohesion: 0.13
Nodes (5): _abandoned(), _check_deadline(), _consume(), _DatabaseCall, Task 4: Extract KB Database Call Mechanics Without Changing Transactions

### Community 134 - "test_dbapi_commit_handoff_arbitrates_cancellation"
Cohesion: 0.47
Nodes (4): test_dbapi_commit_handoff_arbitrates_cancellation(), gate(), gate_before_dbapi(), gate_inside_dbapi()

### Community 137 - "config.py"
Cohesion: 0.06
Nodes (22): OllamaProvider, _capabilities(), OpenRouterProvider, _per_million(), eligibility(), Capability, CatalogEntry, ProviderStatus (+14 more)

### Community 139 - "jev.py"
Cohesion: 0.08
Nodes (37): Candidates, ClassificationResult, ClassifierOutput, NormalizedTicket, Classifier, build_order_check(), build_questions(), build_state() (+29 more)

### Community 140 - "submission.py"
Cohesion: 0.41
Nodes (6): Receipt, IntakeOperationRow, IntakeSubmissionRow, SubmissionResult, SubmissionService, Ticket

### Community 141 - "db/repository.py"
Cohesion: 0.14
Nodes (5): Base, IncidentRow, ModelSettingAuditRow, ModelSettingRow, test_rows_for_unknown_providers_are_ignored()

### Community 142 - "cli.py"
Cohesion: 0.09
Nodes (36): _command_settings(), ingest_kb_cmd(), init_db_cmd(), Mode, run_batch_cmd(), _run_in_memory(), _run_with_db(), seed_db_cmd() (+28 more)

### Community 143 - "knowledge_runtime.py"
Cohesion: 0.19
Nodes (4): ConfiguredEmbedder, _Store, _Store, test_configured_embedder_follows_the_current_setting()

### Community 144 - "probe.py"
Cohesion: 0.11
Nodes (13): _chat(), _classify(), _describe(), _draft(), _embed(), _extract(), _intake(), _ProbeAnswer (+5 more)

### Community 148 - "components-ai-thought-chain.tsx"
Cohesion: 0.15
Nodes (15): Status, StatusIcon(), statusStyles, StepContext, StepContextType, ThoughtChain(), ThoughtChainContent(), ThoughtChainItem() (+7 more)

### Community 151 - "taxonomy.py"
Cohesion: 0.09
Nodes (28): Decision, decide(), empty_ticket_decision(), merge_reasons(), note_for(), _unique(), Category, most_urgent() (+20 more)

### Community 152 - "create_app"
Cohesion: 0.08
Nodes (26): init_db(), initialize_database(), make_engine(), make_sessionmaker(), reset_db(), intake_client(), intake_db(), reviewed() (+18 more)

### Community 153 - "create_app"
Cohesion: 0.11
Nodes (27): _safe_dispatch(), RunRow, _accepts(), create_app(), intake_failed(), lifespan(), recover(), TicketExecution (+19 more)

### Community 154 - "ZainCash support: architecture and ticket flow {#support-overview}"
Cohesion: 0.50
Nodes (3): 1 · System architecture {#system-architecture}, 2 · Ticket flow {#ticket-flow}, ZainCash support: architecture and ticket flow {#support-overview}

### Community 155 - "IntakePage.test.tsx"
Cohesion: 0.10
Nodes (26): Task 7: Bilingual customer chat, screenshots and reviewed submission, copy(), parseJson(), readError(), FakeXHR, session, UploadResult, IntakeRequestError (+18 more)

### Community 156 - "employee-frontend/src/components/theme-provider.tsx"
Cohesion: 0.23
Nodes (11): disableTransitionsTemporarily(), getSystemTheme(), isEditableTarget(), isTheme(), ResolvedTheme, Theme, THEME_VALUES, ThemeProvider() (+3 more)

### Community 157 - "agent.py"
Cohesion: 0.11
Nodes (12): _Execution, _ModelUsage, RagDrafter, DraftContext, DraftExecutionError, DraftModelInfo, test_real_search_fault_carries_safe_draft_execution_error(), test_anthropic_fallback_prices_and_provider_cost_precedence() (+4 more)

### Community 159 - "TicketRow"
Cohesion: 0.08
Nodes (27): BatchInput, KnowledgeIndexInput, KnowledgeSearchInput, TicketInput, customer_phone_or_none(), InvalidPhone, normalize_customer_phone(), CustomerRow (+19 more)

### Community 160 - "test_embedding_switch.py"
Cohesion: 0.13
Nodes (13): EmbeddingSwitchRow, EmbeddingSwitches, _view(), _client(), _documents(), test_failed_documents_are_listed(), test_run_start_locks_the_switch_table_before_its_first_write(), test_runs_are_blocked_while_a_switch_runs_and_restart_recovers() (+5 more)

### Community 161 - "Customer phone identity design"
Cohesion: 0.13
Nodes (14): Backend, Canonical phone format, Customer phone identity design, Data model, Decisions, Employee API, employee-frontend, Error handling (+6 more)

### Community 164 - "ProviderRegistry"
Cohesion: 0.06
Nodes (20): DraftProviderResponseError, OpenRouterChat, provider_errors(), ProviderRegistry, UnknownProvider, test_registry_includes_ollama_and_its_errors(), _provider(), test_chat_catalog_maps_capabilities_and_prices() (+12 more)

### Community 165 - "test_workspace_schema.py"
Cohesion: 0.29
Nodes (8): assert_customer_schema(), LegacySchemaError, _nullable(), _table_exists(), upgrade_workspace_schema(), test_fresh_schema_passes_the_customer_check(), test_intake_sessions_without_a_customer_phone_stop_startup(), test_nullable_ticket_phone_stops_startup_with_a_reset_instruction()

### Community 167 - "build_pipeline"
Cohesion: 0.15
Nodes (21): build_pipeline(), ConfigError, model_ids(), run_batch(), FakeStructuredLLM, ScriptedChat, _settings(), test_builds_jev_pipeline_with_injected_clients() (+13 more)

### Community 168 - "support_test"
Cohesion: 0.12
Nodes (19): ingest(), support_test(), Backend Maintainability Implementation Plan, Global Constraints, Artifacts, servers and remaining concerns, Citation IDs and provider evidence, Commands and automated verification — historical Task 8, Corpus and actual retrieval (+11 more)

### Community 169 - "intake/contracts.py"
Cohesion: 0.16
Nodes (10): _aware(), CustomerReview, IntakeModel, PendingQuestion, ProgressItem, ReviewSnapshot, fail_once(), repo() (+2 more)

### Community 171 - "Deviations from the spec (intentional, small)"
Cohesion: 0.17
Nodes (7): Deviations from the spec (intentional, small), Global Constraints, Per-model Evaluation Implementation Plan — Part 2 of 3 (evaluation engine), Task 11: `support eval` CLI and v2 export, Task 7: Metrics, Task 8: Evaluation storage and views, Task 9: Runner, request validation and cost estimate

### Community 172 - "test_submission.py"
Cohesion: 0.32
Nodes (4): _payload(), test_concurrent_submit_dispatches_once(), test_second_request_id_reuses_the_approved_review(), test_submission_replay_creates_one_ticket()

## Ambiguous Edges - Review These
- `Fraud Report` → `Plan 1 Live Smoke`  [AMBIGUOUS]
  README.md · relation: conceptually_related_to

## Knowledge Gaps
- **83 isolated node(s):** `zaincash-support`, `@base-ui/react`, `@fontsource-variable/plus-jakarta-sans`, `@fontsource/tajawal`, `@tailwindcss/vite` (+78 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 1200 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **26 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Settings` connect `Settings` to `TypeSafeProvider`, `intake/model.py`, `Step`, `test_llm.py`, `pytest`, `test_catalog.py`, `Review Focus`, `config.py`, `test_rag_api.py`, `submission.py`, `db/repository.py`, `cli.py`, `knowledge_runtime.py`, `jev.py`, `make_output`, `create_app`, `create_app`, `FakeProvider`, `EmbeddingError`, `agent.py`, `test_draft_tools.py`, `test_embedding_switch.py`, `test_kb_service.py`, `ProviderRegistry`, `test_workspace_schema.py`, `build_pipeline`, `support_test`, `PipelineState`, `pytest`, `fact`, `knowledge.py`, `main.py`, `demo-readiness.md`, `ModelSettingsStore`, `test_workspace_api.py`, `factory.py`, `test_final_fix_handoff.py`, `policy.py`, `TurnContext`?**
  _High betweenness centrality (0.092) - this node is a cross-community bridge._
- **Are the 54 inferred relationships involving `Settings` (e.g. with `_command_settings()` and `_run_in_memory()`) actually correct?**
  _`Settings` has 54 INFERRED edges - model-reasoned connections that need verification._
- **What connects `zaincash-support`, `@base-ui/react`, `@fontsource-variable/plus-jakarta-sans` to the rest of the system?**
  _83 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `TypeSafeProvider` be split into smaller, more focused modules?**
  _Cohesion score 0.12631578947368421 - nodes in this community are weakly interconnected._
- **Why does `2. Current state` connect `jev.py` to `Card`, `NewBatchPage.tsx`, `build_pipeline`, `make_output`, `taxonomy.py`?**
  _High betweenness centrality (0.076) - this node is a cross-community bridge._
- **Are the 68 inferred relationships involving `Step` (e.g. with `catalog()` and `_check_provider()`) actually correct?**
  _`Step` has 68 INFERRED edges - model-reasoned connections that need verification._

### Low-confidence Hints
_AMBIGUOUS edges — the extractor was unsure. Verify before acting on these._

- **What is the exact relationship between `Fraud Report` and `Plan 1 Live Smoke`?**
  _Edge tagged AMBIGUOUS (relation: conceptually_related_to) - confidence is low._