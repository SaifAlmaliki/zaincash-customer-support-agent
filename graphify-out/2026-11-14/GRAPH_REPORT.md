# Graph Report - zaincash-support  (2026-11-14)

## Corpus Check
- 409 files · ~488,120 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 25 file(s) not represented in the graph (top: (none) 15, .jsonl 4, .css 4)

## Summary
- 4114 nodes · 13688 edges · 161 communities (130 shown, 31 thin omitted)
- Extraction: 84% EXTRACTED · 16% INFERRED · 0% AMBIGUOUS · INFERRED: 2137 edges (avg confidence: 0.93)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `39351a66`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- EmbeddingError
- ActiveModels
- pytest
- main.py
- investigation.py
- InvalidPhone
- Card
- Customer conversation intake for ZainCash support
- RunDetailPage.tsx
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
- intake/repository.py
- compilerOptions
- web/src/components/theme-provider.tsx
- Settings
- Classify and Extract Prompts
- test_draft_tools.py
- Pipeline Design Spec
- Batch Runner
- Drafting Plan Concepts
- test_kb_service.py
- search_knowledge_base
- web/components.json
- workspace-ui.tsx
- ui/components.json
- fact
- Guided intake interview — design
- Vite Config
- Human Review Gate
- compilerOptions
- NewBatchPage.tsx
- compilerOptions
- AI usage and performance dashboard (`/evaluation`) — design specification
- Human Flag Tool
- Recent Transactions Tool
- Ticket History Tool
- Lookup Transaction Tool
- Search Transactions Tool
- Submit Draft Tool
- Project Root
- parse_document
- intake/test_repository.py
- contracts.ts
- test_llm.py
- TicketRow
- lib/types.ts
- locale.tsx
- tasks
- knowledge.py
- ChangeModelDialog.tsx
- IntakePage.tsx
- PipelineState
- agent-chat.tsx
- httpx
- collapsible.tsx
- tests/test_repository.py
- fake_registry
- ChangeModelDialog.tsx
- PipelineState
- test_workspace_api.py
- test_interview_api.py
- devDependencies
- cli.py
- support_test
- Step
- queue-projection.ts
- test_rag_api.py
- Guided intake interview verification — 2026-11-13
- fact
- test_recovery_regressions.py
- InvalidEvidence
- test_lookup.py
- Customer intake chat layout
- Plan 3 RAG Drafting Implementation Plan
- RAG drafting verification — 2026-10-17
- tools.py
- devDependencies
- devDependencies
- test_jev.py
- ticket-flow.ts
- Per-model evaluation (quality, system, cost) — design specification
- compilerOptions
- fakes.py
- ZainCash Support Workspace
- dependencies
- InvalidEvidence
- dependencies
- compilerOptions
- KnowledgeError
- intake/api.ts
- test_final_fix_handoff.py
- TicketInput
- pydantic
- scripts
- Deviations from the spec (intentional, small)
- compilerOptions
- Maintainability and stale-code refactor — design specification
- demo-readiness.md
- web/tsconfig.json
- employee-frontend/tsconfig.json
- exports
- Review Focus
- scripts
- users-frontend/README.md
- policy.py
- TurnContext
- Admin-managed, model-agnostic pipeline configuration — design specification
- admin.py
- guardrails.py
- .session_factory
- DraftExecutionError
- intake/model.py
- Synthetic demo readiness
- intake.py
- Review Focus
- EmbeddingBatch
- Global Constraints
- FakeXHR
- types.py
- pipeline/contracts.py
- pipeline/graph.py
- probe.py
- components-ai-thought-chain.tsx
- intake/README.md
- test_taxonomy.py
- ZainCash support: architecture and ticket flow {#support-overview}
- IntakePage.test.tsx
- employee-frontend/src/components/theme-provider.tsx
- _ModelUsage
- .save
- Customer phone identity design
- api-entrypoint.sh
- build_pipeline
- Customer Conversation Intake Implementation Plan
- 4. Backend design
- test_submission.py

## God Nodes (most connected - your core abstractions)
1. `Settings` - 190 edges
2. `Step` - 109 edges
3. `ModelChoice` - 92 edges
4. `KnowledgeService` - 86 edges
5. `ActiveModels` - 74 edges
6. `fact()` - 73 edges
7. `context()` - 68 edges
8. `useCopy()` - 68 edges
9. `message()` - 63 edges
10. `IntakeController` - 59 edges

## Surprising Connections (you probably didn't know these)
- `Repeatable local walkthrough` --references--> `Settings`  [INFERRED]
  docs/demo-readiness.md → backend/app/config.py
- `Ticket write paths` --references--> `upsert_tickets()`  [INFERRED]
  docs/superpowers/specs/2026-11-13-customer-phone-identity-design.md → backend/app/db/repository.py
- `Existing data` --references--> `upgrade_workspace_schema()`  [INFERRED]
  docs/superpowers/specs/2026-11-13-customer-phone-identity-design.md → backend/app/db/workspace_schema.py
- `Task 9: Repair the Five-Record JSONL Baseline Fixture` --references--> `load_jsonl()`  [INFERRED]
  docs/superpowers/plans/2026-11-02-backend-maintainability.md → backend/app/ingest.py
- `Re-ask once` --references--> `QuestionRecord`  [INFERRED]
  docs/superpowers/specs/2026-11-13-guided-intake-interview-design.md → backend/app/intake/contracts.py

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **Cascade Classification Path** — docs_superpowers_specs_2026_10_07_support_pipeline_design_cascade, docs_superpowers_plans_2026_10_07_plan1_core_pipeline_part2_jev_classifier, docs_superpowers_plans_2026_10_07_plan1_core_pipeline_part2_gemini_classifier, docs_superpowers_plans_2026_10_07_plan1_core_pipeline_part2_cascade_combine, readme_human_approval [EXTRACTED 1.00]
- **Drafting Agent Toolset** — backend_app_pipeline_runner_lookup_transaction, backend_app_pipeline_runner_search_transactions, backend_app_pipeline_runner_get_customer_recent_transactions, backend_app_pipeline_runner_get_customer_ticket_history, backend_app_pipeline_runner_check_service_status, backend_app_pipeline_runner_search_knowledge_base, backend_app_pipeline_runner_flag_for_human, backend_app_pipeline_runner_submit_draft [EXTRACTED 1.00]
- **Ticket Processing Stage Flow** — backend_app_pipeline_runner_prepare, backend_app_pipeline_runner_jev_classify, backend_app_pipeline_runner_gemini_classify, backend_app_pipeline_runner_extract, backend_app_pipeline_runner_lookup, backend_app_pipeline_runner_decide, backend_app_pipeline_runner_draft [EXTRACTED 1.00]

## Communities (161 total, 31 thin omitted)

### Community 0 - "EmbeddingError"
Cohesion: 0.08
Nodes (43): EmbeddingError, _nonnegative_number(), OpenAICompatibleEmbedder, OpenRouterEmbedder, _ordered_vectors(), _response_cost(), _percentile(), embedder_for() (+35 more)

### Community 1 - "ActiveModels"
Cohesion: 0.14
Nodes (10): ActiveModels, _local_pipeline(), test_local_draft_uses_local_timeout_zero_prices_and_option_temperature(), test_model_ids_keep_colons_in_model_names(), Admin model configuration — backend implementation plan, Review Focus, Task 4: Stored settings, the ActiveModels snapshot and intake pinning, Task 8: Live model tests and the model catalog (+2 more)

### Community 2 - "pytest"
Cohesion: 0.17
Nodes (34): test_blank_intake_model_is_rejected(), test_contracts_reject_extra_keys(), test_datetimes_must_be_timezone_aware(), test_non_positive_image_limit_is_rejected(), Checker, draft_state(), Knowledge, drafter() (+26 more)

### Community 3 - "main.py"
Cohesion: 0.07
Nodes (26): get_session(), _safe_dispatch(), get_run(), list_runs(), start_run(), BatchInput, Base, IncidentRow (+18 more)

### Community 4 - "investigation.py"
Cohesion: 0.14
Nodes (14): parse_dt(), TxnRecord, DraftToolInputError, _datetime(), _days(), _field(), _involves(), _phone() (+6 more)

### Community 5 - "InvalidPhone"
Cohesion: 0.07
Nodes (29): customer_phone_or_none(), InvalidPhone, normalize_customer_phone(), ensure_customers(), _ticket_phone(), load_jsonl(), load_tickets(), _rows() (+21 more)

### Community 6 - "Card"
Cohesion: 0.17
Nodes (44): Task 5: Extract presentational DocumentList and KnowledgeReadiness components, Task 12: Locale parity test and translated Runs pages, 6.4 Focused view extraction, EmptyState(), ErrorState(), Card(), CardContent(), CardHeader() (+36 more)

### Community 7 - "Customer conversation intake for ZainCash support"
Cohesion: 0.06
Nodes (31): 10. Verification and acceptance criteria, 11. Delivery and review, 1. Outcome and agreed requirements, 2. Current implementation and integration points, 3. Approach and boundaries, 4. Conversation state and turn flow, 5. Facts, evidence, and readiness, 6. Language and screenshot behavior (+23 more)

### Community 8 - "RunDetailPage.tsx"
Cohesion: 0.12
Nodes (19): Task 3: Split RunDetailPage and introduce bounded run-result loading, Task 2: Strings, the AI locality chip, run models and the batch switch message, 6.1 Verification and cleanup, 6.2 Retire the legacy trace/chart cluster, 6.3 Runs and request loading, 6. Employee frontend design, 6.4 Visible to all employees, LEGACY (+11 more)

### Community 9 - "IntakeController"
Cohesion: 0.16
Nodes (11): Task 1: Cleanup-first removal of reference-verified dead code and dependencies, Task 7: Preserve resume-unavailable state across `startNew`, Task 7: Intake app data layer — phone helper, contracts, API, controller, Task 7: Customer frontend data layer, ControllerState, emptyState(), IntakeController, isConflict() (+3 more)

### Community 10 - "FakeJevRunnable"
Cohesion: 0.12
Nodes (18): CredentialCheck, DegradedCredentialChecker, _finite_nonnegative(), _get(), JevCredentialChecker, ResponseRunnable, test_bad_usage_cannot_poison_cost(), test_cancellation_propagates_with_cost_for_outer_timeout_owner() (+10 more)

### Community 11 - "test_rag_api.py"
Cohesion: 0.06
Nodes (43): CustomerRow, init_db(), initialize_database(), make_engine(), make_sessionmaker(), reset_db(), assert_customer_schema(), LegacySchemaError (+35 more)

### Community 12 - "employee-frontend/package.json"
Cohesion: 0.06
Nodes (30): @base-ui/react, class-variance-authority, cn, eslint, @eslint/js, eslint-plugin-react-hooks, eslint-plugin-react-refresh, @fontsource/tajawal (+22 more)

### Community 14 - "QueuePage.tsx"
Cohesion: 0.15
Nodes (36): Task 10: Employee app — customer page and ticket header link, Task 9: Employee app — required phone, queue identity and search, batch entry, Task 15: Ticket cost table and AI timeline, 5.1 Data access, Confidence(), LoadingState(), PageHeader(), PriorityBadge() (+28 more)

### Community 15 - "Support Taxonomy Categories"
Cohesion: 0.21
Nodes (22): lookup, Account KYC, Account & Security, Agent Dispute, Agent Network, App Bug, Bill Payment, Card Issue (+14 more)

### Community 16 - "ui/package.json"
Cohesion: 0.08
Nodes (24): @base-ui/react, class-variance-authority, cn, eslint, @eslint/js, eslint-plugin-react-hooks, eslint-plugin-react-refresh, @fontsource/tajawal (+16 more)

### Community 17 - "ModelsPage.tsx"
Cohesion: 0.13
Nodes (28): App(), CustomerPage, EvaluationPage, InsightsPage, KnowledgePage, ModelsPage, NewBatchPage, QueuePage (+20 more)

### Community 18 - "users-frontend/package.json"
Cohesion: 0.08
Nodes (23): turbo, devDependencies, prettier, prettier-plugin-tailwindcss, turbo, typescript, engines, node (+15 more)

### Community 19 - "make_output"
Cohesion: 0.07
Nodes (55): build_graph(), PipelineDeps, InMemoryTransactionRepo, load_taxonomy(), tax(), FakeClassifier, make_output(), make_ticket() (+47 more)

### Community 20 - "test_draft_guardrails.py"
Cohesion: 0.14
Nodes (26): requests_credentials(), check(), state(), test_aggregation_is_deduplicated_and_has_no_state_side_effects(), test_amount_occurrences_keep_their_own_currency_and_sign(), test_avoid_sharing_warning_does_not_excuse_a_later_request(), test_candidate_prompt_limit_does_not_hide_later_ungrounded_references(), test_candidate_transactions_cannot_authorize_reply_evidence() (+18 more)

### Community 21 - "web/package.json"
Cohesion: 0.05
Nodes (38): jsdom, @testing-library/jest-dom, @testing-library/react, @workspace/ui, dependencies, clsx, react, react-dom (+30 more)

### Community 22 - "test_interview_scenarios.py"
Cohesion: 0.19
Nodes (9): analyze_calls(), Chat, source_of(), summary(), test_complete_report_goes_straight_to_review(), test_no_reference_number_still_gives_a_complete_report(), test_vague_report_is_interviewed_into_a_complete_ticket(), updates() (+1 more)

### Community 23 - "compilerOptions"
Cohesion: 0.08
Nodes (23): compilerOptions, allowArbitraryExtensions, allowImportingTsExtensions, erasableSyntaxOnly, jsx, lib, module, moduleDetection (+15 more)

### Community 24 - "employee-frontend/components.json"
Cohesion: 0.09
Nodes (21): aliases, components, hooks, lib, ui, utils, iconLibrary, menuAccent (+13 more)

### Community 25 - "intake/repository.py"
Cohesion: 0.09
Nodes (39): OperationClaim, Receipt, TurnResult, IntakeAttachmentRow, IntakeMessageRow, IntakeOperationRow, IntakeSessionRow, IntakeSubmissionRow (+31 more)

### Community 26 - "compilerOptions"
Cohesion: 0.09
Nodes (22): compilerOptions, allowArbitraryExtensions, allowImportingTsExtensions, erasableSyntaxOnly, jsx, lib, module, moduleDetection (+14 more)

### Community 27 - "web/src/components/theme-provider.tsx"
Cohesion: 0.16
Nodes (13): App(), controller, disableTransitionsTemporarily(), getSystemTheme(), isEditableTarget(), isTheme(), ResolvedTheme, Theme (+5 more)

### Community 28 - "Settings"
Cohesion: 0.05
Nodes (40): Settings, ConfiguredEmbedder, _Store, draft_timeout_s(), eligibility(), env_defaults(), intake_timeout_s(), ModelChoice (+32 more)

### Community 29 - "Classify and Extract Prompts"
Cohesion: 0.33
Nodes (7): extract, gemini_classify, Pipeline Graph Orchestration, jev_classify, prepare, GeminiClassifier, JevClassifier

### Community 30 - "test_draft_tools.py"
Cohesion: 0.12
Nodes (28): ErrorEmbedder, settings(), test_all_eight_tools_and_seven_parallel_calls_execute_only_six(), test_context_copies_input_and_rejects_raising_hard_call_limit(), test_database_faults_remain_distinct_and_record_paid_search_cost(), test_discovered_ref_can_be_inspected_but_not_promoted_to_match(), test_exact_and_fuzzy_queries_are_scoped_and_never_confirm_candidates(), test_exact_reference_still_requires_customer_and_excludes_future() (+20 more)

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
Cohesion: 0.09
Nodes (42): KnowledgeChunk, KnowledgeDocumentIndex, KnowledgeService, FakeEmbedder, GatedEmbedder, PaidEmbedder, embedder(), count_chunks() (+34 more)

### Community 36 - "web/components.json"
Cohesion: 0.10
Nodes (19): aliases, components, hooks, lib, ui, utils, iconLibrary, menuAccent (+11 more)

### Community 38 - "workspace-ui.tsx"
Cohesion: 0.08
Nodes (34): Global Constraints, Per-model Evaluation Implementation Plan — Part 3 of 3 (frontend, translations, verification), Task 13: Evaluation types, API client, formatters, copy and report import, Task 15: Provenance, headline metrics, comparison table and empty state, Task 16: Model detail, confusion matrix and predictions drawer, Task 17: Run dialog, progress, page assembly, route and styles, Task 18: Documentation, full verification and manual check, AI Usage and Performance Dashboard Implementation Plan — Part 2 of 2 (frontend, docs, verification) (+26 more)

### Community 39 - "ui/components.json"
Cohesion: 0.10
Nodes (19): aliases, components, hooks, lib, ui, utils, iconLibrary, menuAccent (+11 more)

### Community 40 - "fact"
Cohesion: 0.16
Nodes (41): Attachment, Question, merge_analysis(), assess_readiness(), choose_question(), context(), message(), proposal() (+33 more)

### Community 41 - "Guided intake interview — design"
Cohesion: 0.06
Nodes (30): 1. Question rules (backend), 3. Chat screen, 4. Review card, Actions, Additional issues, Approach, Composer hints, Copy (+22 more)

### Community 43 - "Human Review Gate"
Cohesion: 0.25
Nodes (4): support CLI, Support Workspace UI Plan, Review API, Workspace UI Verification

### Community 44 - "compilerOptions"
Cohesion: 0.12
Nodes (16): compilerOptions, allowImportingTsExtensions, erasableSyntaxOnly, lib, module, moduleDetection, noEmit, noFallthroughCasesInSwitch (+8 more)

### Community 46 - "NewBatchPage.tsx"
Cohesion: 0.13
Nodes (22): 6.1 Route and access, 6.2 Page, 6.3 Change dialog, 6.5 Text and direction, 6. Employee-frontend design, Tabs(), TabsContent(), TabsList() (+14 more)

### Community 47 - "compilerOptions"
Cohesion: 0.12
Nodes (16): compilerOptions, allowImportingTsExtensions, erasableSyntaxOnly, lib, module, moduleDetection, noEmit, noFallthroughCasesInSwitch (+8 more)

### Community 48 - "AI usage and performance dashboard (`/evaluation`) — design specification"
Cohesion: 0.11
Nodes (17): recent(), 10. Phase 2 (for reference, not designed here), 1. Outcome and success criteria, 3. Decisions, 4.2 Processes, 4.5 Prices for estimates, 4.6 Reporting API, 4. Backend design (+9 more)

### Community 57 - "parse_document"
Cohesion: 0.13
Nodes (26): TextChunk, _append_chunks(), _check_extracted_size(), DocumentParseError, parse_document(), _parse_pdf(), make_pdf(), test_arabic_text_and_bom_are_preserved() (+18 more)

### Community 58 - "intake/test_repository.py"
Cohesion: 0.07
Nodes (33): AttachmentStore, _display_name(), Credentials, SessionView, ImageRejected, InvalidCustomerPhone, NotOwned, IntakeRepository (+25 more)

### Community 59 - "contracts.ts"
Cohesion: 0.17
Nodes (34): Task 5: Add complete dependency-free API and persisted-session guards, createIntakeApi(), ANSWER_KINDS, CHOICES, FACT_STATUSES, finiteNonnegative(), invalid(), isRecord() (+26 more)

### Community 60 - "test_llm.py"
Cohesion: 0.11
Nodes (12): StructuredChatLLM, make_draft_model(), make_gemini_llm(), _llm(), _S, test_draft_model_uses_millisecond_timeout_and_disables_sdk_retries(), test_openrouter_reported_cost_takes_precedence_over_token_estimate(), test_openrouter_retry_budget_is_bounded() (+4 more)

### Community 61 - "TicketRow"
Cohesion: 0.08
Nodes (30): get_customer(), get_result(), list_results(), read_intake_attachment(), review_result(), ReviewInput, health(), insights() (+22 more)

### Community 62 - "lib/types.ts"
Cohesion: 0.10
Nodes (28): acceptIndexRequest(), canRequestIndex(), PendingIndexes, persistPendingIndexes(), pollKnowledge(), refresh(), stop(), PollOptions (+20 more)

### Community 63 - "locale.tsx"
Cohesion: 0.07
Nodes (30): Task 8: Employee evidence panel and processing state, Task 2: Migrate active TicketFlow coverage, then retire the legacy trace/chart cluster, LanguageToggle(), originalLocale, DocumentListProps, knowledgeDocument(), listProps(), originalLocale (+22 more)

### Community 64 - "tasks"
Cohesion: 0.11
Nodes (18): dependsOn, inputs, outputs, cache, persistent, dependsOn, dependsOn, $schema (+10 more)

### Community 65 - "knowledge.py"
Cohesion: 0.10
Nodes (25): session(), _configured(), delete_document(), download_document(), index_document(), list_chunks(), list_documents(), _require_provider() (+17 more)

### Community 66 - "ChangeModelDialog.tsx"
Cohesion: 0.09
Nodes (38): Admin model configuration — employee frontend implementation plan, Backend API contract used here, File structure, Global Constraints, Review Focus, Task 1: API types, admin session and admin requests, Task 3: Model choice logic and the change dialog, Task 14: Evaluation view helpers (+30 more)

### Community 67 - "IntakePage.tsx"
Cohesion: 0.06
Nodes (57): Global Constraints, Intake Chat UI Implementation Plan, Task 1: Put the summary and receipt in the thread, Task 2: Put screenshots inside the composer, Task 3: Apply the workspace chat styles, Task 4: Check the page in the browser, Task 8: Intake app UI — phone screen, profile chip, change number, receipt, Review Focus (+49 more)

### Community 68 - "PipelineState"
Cohesion: 0.11
Nodes (18): 10. Remaining demo roadmap, 1. Intent and acceptance criteria, 3. Provider and configuration, 4. Knowledge ingestion and persistence, 5. Retrieval and evidence, 6. Bounded investigation agent, 7. Draft guardrails and failure outcomes, 8. Pipeline, API, CLI and UI integration (+10 more)

### Community 69 - "agent-chat.tsx"
Cohesion: 0.15
Nodes (25): Task 8: Chat screen — instant bubble, typing, reasons, quick replies, composer hints, clsx, tailwind-merge, @testing-library/user-event, AgentChat, AgentChatProps, AgentMessage, AssistantText() (+17 more)

### Community 70 - "httpx"
Cohesion: 0.11
Nodes (14): OllamaProvider, _provider(), _tags_handler(), test_catalog_lists_installed_models_with_reported_capabilities(), handler(), test_chat_model_sets_the_configured_context_window(), test_chat_model_targets_the_configured_server(), test_embedder_uses_openai_compatible_endpoint_without_dimensions() (+6 more)

### Community 72 - "tests/test_repository.py"
Cohesion: 0.10
Nodes (30): finish_run(), load_incidents(), load_transactions(), save_outcomes(), SqlTransactionRepo, _to_record(), _upsert(), upsert_tickets() (+22 more)

### Community 73 - "fake_registry"
Cohesion: 0.11
Nodes (24): CatalogCache, step_catalog(), fake_registry(), FakeProvider, make_client(), build(), test_admin_is_disabled_without_a_token(), test_models_and_catalog() (+16 more)

### Community 74 - "ChangeModelDialog.tsx"
Cohesion: 0.18
Nodes (26): ConfirmDialog(), Button(), Dialog(), DialogContent(), DialogDescription(), DialogFooter(), DialogHeader(), DialogOverlay() (+18 more)

### Community 75 - "PipelineState"
Cohesion: 0.12
Nodes (14): DraftResult, _Nodes, Drafter, NullDrafter, UnavailableDrafter, PipelineState, draft(), draft() (+6 more)

### Community 76 - "test_workspace_api.py"
Cohesion: 0.12
Nodes (19): review_payload(), start_run(), test_batch_and_queue_expose_real_results(), test_batch_failure_is_isolated_and_conflicting_ids_rejected(), test_customer_profile_lists_the_latest_result_of_each_ticket(), test_only_jev_mode_is_configured_and_retired_modes_are_rejected(), test_progress_counts_only_durable_results_after_save_failure(), test_result_list_paginates_filters_and_run_id() (+11 more)

### Community 77 - "test_interview_api.py"
Cohesion: 0.25
Nodes (15): analyze_calls(), ask(), opening(), send(), start(), summary(), test_ask_rejects_a_detail_outside_the_plan(), test_attach_is_not_a_message_answer() (+7 more)

### Community 79 - "devDependencies"
Cohesion: 0.12
Nodes (16): devDependencies, eslint, @eslint/js, eslint-plugin-react-hooks, eslint-plugin-react-refresh, globals, prettier, prettier-plugin-tailwindcss (+8 more)

### Community 80 - "cli.py"
Cohesion: 0.07
Nodes (21): _command_settings(), ingest_kb_cmd(), init_db_cmd(), Mode, run_batch_cmd(), _run_in_memory(), _run_with_db(), seed_db_cmd() (+13 more)

### Community 81 - "support_test"
Cohesion: 0.17
Nodes (12): support_test(), Task 3: Ticket-scoped investigation and all eight tools, Task 8: Demo corpus, full verification and readiness record, Backend Maintainability Implementation Plan, Global Constraints, Global Constraints, Browser handoff, Customer intake verification — 2026-10-18 (+4 more)

### Community 82 - "Step"
Cohesion: 0.18
Nodes (13): probe(), Step, _registry(), StructuredChat, test_draft_probe_requires_a_correct_tool_call(), test_embed_and_classify_probes(), test_every_step_has_a_probe(), test_intake_probe_sends_an_image_and_needs_parsed_output() (+5 more)

### Community 83 - "queue-projection.ts"
Cohesion: 0.14
Nodes (13): Employee Frontend Maintainability Implementation Plan, Global Constraints, Review Focus, Task 1: Remove reference-verified dead exports, components, and the Mermaid dependency, Task 4: Extract and test the pure queue projection, Task 6: Repair ExtractedField fixtures and make standalone typecheck real, Task 7: Repair employee README paths/test-count guidance and run final acceptance, SelectSeparator() (+5 more)

### Community 84 - "test_rag_api.py"
Cohesion: 0.11
Nodes (22): index_deadlines(), settings(), client(), evidence_client(), test_actual_guardrail_failure_is_separate_from_reply(), test_concurrent_index_requests_share_active_work(), test_disabled_or_missing_provider_stores_without_indexing(), test_explicit_retry_tags_search_and_chunk_pagination() (+14 more)

### Community 85 - "Guided intake interview verification — 2026-11-13"
Cohesion: 0.20
Nodes (9): Arabic at 390×844, starting from the vague message, English at 1280×900, with the complete message, Final automated checks, Guided intake interview verification — 2026-11-13, Live browser run, Live probe output (facts only), Live transfer probe, Observations (+1 more)

### Community 86 - "fact"
Cohesion: 0.13
Nodes (36): Analysis, EvidenceRef, fact(), grounded_analysis(), image_evidence(), test_assistant_text_cannot_ground_a_customer_fact(), test_foreign_message_cannot_ground_fact(), test_hallucinated_amount_normalization_is_rejected() (+28 more)

### Community 87 - "test_recovery_regressions.py"
Cohesion: 0.27
Nodes (11): command(), create(), test_failed_review_retry_cannot_reopen_submitted_session(), test_original_payload_identity_survives_sanitization(), test_publication_failure_is_retryable_without_restart(), fail_once(), test_receipt_reference_is_preserved(), test_stale_attempt_audit_is_retained_once_with_attempt_identity() (+3 more)

### Community 88 - "InvalidEvidence"
Cohesion: 0.23
Nodes (17): ReviewText, InvalidEvidence, validate(), build_review(), _compact(), _render_value(), _ticket_text(), _tokens() (+9 more)

### Community 89 - "test_lookup.py"
Cohesion: 0.17
Nodes (14): _as_date(), _iqd_amount(), match_transaction(), TransactionRepo, _ex(), _match(), test_ambiguous_then_disambiguated_by_counterpart(), test_amount_and_date_mismatch() (+6 more)

### Community 90 - "Customer intake chat layout"
Cohesion: 0.33
Nodes (5): 1. Outcome, 2. Scope, 3. Layout, 5. Checks, Customer intake chat layout

### Community 91 - "Plan 3 RAG Drafting Implementation Plan"
Cohesion: 0.18
Nodes (10): Completion and review record — 2026-10-17, Execution handoff, File map and shared interfaces, Global Constraints, Plan 3 RAG Drafting Implementation Plan, Plan self-review, Review Focus, Task 5: Agent, failure conversion and pipeline wiring (+2 more)

### Community 92 - "RAG drafting verification — 2026-10-17"
Cohesion: 0.20
Nodes (10): ingest(), Artifacts, servers and remaining concerns, Citation IDs and provider evidence, Commands and automated verification — historical Task 8, Corpus and actual retrieval, Current final verification and review closure, Environment and isolation, Live browser and persistence evidence (+2 more)

### Community 93 - "tools.py"
Cohesion: 0.07
Nodes (21): DraftAlreadySubmitted, DraftSubmission, DraftToolLimit, _bounded(), visit(), build_tools(), flag(), guarded() (+13 more)

### Community 94 - "devDependencies"
Cohesion: 0.11
Nodes (19): devDependencies, eslint, @eslint/js, eslint-plugin-react-hooks, eslint-plugin-react-refresh, globals, jsdom, @tailwindcss/vite (+11 more)

### Community 95 - "devDependencies"
Cohesion: 0.17
Nodes (12): devDependencies, eslint, @eslint/js, eslint-plugin-react-hooks, eslint-plugin-react-refresh, globals, tailwindcss, @types/node (+4 more)

### Community 96 - "test_jev.py"
Cohesion: 0.40
Nodes (9): _criteria(), _run(), test_low_top_probability_is_uncertain(), test_one_main_call_with_all_questions(), test_order_check_uses_reversed_options(), test_order_disagreement_is_uncertain(), test_priority_level_maps_to_p_label(), test_state_is_truncated() (+1 more)

### Community 97 - "ticket-flow.ts"
Cohesion: 0.06
Nodes (63): Global Constraints, Task 1: Sentence catalog, Task 2: Which step is open, Task 3: Received, produced, and drafting events, Task 4: Mermaid source, Task 5: Draw the charts on the ticket page, Ticket Flow Charts Implementation Plan, 1. Outcome (+55 more)

### Community 98 - "Per-model evaluation (quality, system, cost) — design specification"
Cohesion: 0.20
Nodes (9): 1. Outcome and success criteria, 3. Decisions, 5.3 Text and direction, 5.4 Runs pages, 5.5 Import format, 5. Employee-frontend design, 6. Error handling, 8. Out of scope (+1 more)

### Community 99 - "compilerOptions"
Cohesion: 0.14
Nodes (13): compilerOptions, jsx, lib, module, moduleResolution, noEmit, paths, skipLibCheck (+5 more)

### Community 100 - "fakes.py"
Cohesion: 0.08
Nodes (32): LLMUnavailable, Sample, StructuredLLM, ExtractedField, FieldPick, FieldExtractor, _field(), fill_gaps() (+24 more)

### Community 101 - "ZainCash Support Workspace"
Cohesion: 0.22
Nodes (9): Current capability boundaries, Data source, Modular file map, Open the right project, Run locally, shadcn conventions, Verification, Workflow (+1 more)

### Community 102 - "dependencies"
Cohesion: 0.12
Nodes (16): dependencies, @base-ui/react, class-variance-authority, cn, @fontsource/tajawal, @fontsource-variable/plus-jakarta-sans, lucide-react, motion (+8 more)

### Community 103 - "InvalidEvidence"
Cohesion: 0.16
Nodes (17): Fact, canonical_digits(), normalize_reported_date(), _apply(), _check_reference(), _compact(), checked_update(), _newer_correction() (+9 more)

### Community 104 - "dependencies"
Cohesion: 0.20
Nodes (10): dependencies, @base-ui/react, class-variance-authority, cn, @fontsource/tajawal, @fontsource-variable/plus-jakarta-sans, react, react-dom (+2 more)

### Community 105 - "compilerOptions"
Cohesion: 0.17
Nodes (11): compilerOptions, jsx, lib, module, moduleResolution, outDir, skipLibCheck, strict (+3 more)

### Community 106 - "KnowledgeError"
Cohesion: 0.06
Nodes (15): _abandoned(), _check_deadline(), _consume(), _DatabaseCall, _Claim, DocumentNotFoundError, _error_cost(), IndexAttemptLostError (+7 more)

### Community 107 - "intake/api.ts"
Cohesion: 0.12
Nodes (18): Task 4: Make pending operations discriminated and use one request identity, IntakeApi, parseJson(), readError(), UploadResult, ANSWER_KINDS, INTAKE_FALLBACK_MESSAGE, IntakeRequestError (+10 more)

### Community 108 - "test_final_fix_handoff.py"
Cohesion: 0.10
Nodes (30): RagDrafter, _tool_chat(), answer(), call(), script(), submit(), assert_completed_evidence(), faulty_knowledge() (+22 more)

### Community 110 - "pydantic"
Cohesion: 0.23
Nodes (6): CitationSource, _Draft, draft_evidence(), _Guardrail, _TraceModel, _validated()

### Community 111 - "scripts"
Cohesion: 0.25
Nodes (8): scripts, build, dev, format, lint, preview, test, typecheck

### Community 112 - "Deviations from the spec (intentional, small)"
Cohesion: 0.29
Nodes (6): Deviations from the spec (intentional, small), Global Constraints, Per-model Evaluation Implementation Plan — Part 2 of 3 (evaluation engine), Task 11: `support eval` CLI and v2 export, Task 7: Metrics, Task 9: Runner, request validation and cost estimate

### Community 113 - "compilerOptions"
Cohesion: 0.29
Nodes (6): compilerOptions, module, moduleResolution, skipLibCheck, strict, target

### Community 114 - "Maintainability and stale-code refactor — design specification"
Cohesion: 0.09
Nodes (20): 10. Verification and acceptance, 1. Outcome and success criteria, 2. Audit baseline, 3. Selected approach and sequence, 4. Boundaries and non-goals, 5.1 Dead-code cleanup, 5.3 Knowledge-service boundary, 5.4 Shared backend boundaries (+12 more)

### Community 116 - "web/tsconfig.json"
Cohesion: 0.33
Nodes (5): compilerOptions, paths, files, @workspace/ui/*, references

### Community 117 - "employee-frontend/tsconfig.json"
Cohesion: 0.40
Nodes (4): compilerOptions, paths, files, references

### Community 118 - "exports"
Cohesion: 0.40
Nodes (5): exports, ./components/*, ./globals.css, ./hooks/*, ./lib/*

### Community 119 - "Review Focus"
Cohesion: 0.12
Nodes (15): Customer Frontend Maintainability Implementation Plan, Global Constraints, Review Focus, Task 2: Make standalone typechecking and root test execution real, Task 3: Centralize test cleanup and shared intake fixtures mechanically, Task 6: Extract stable-ID sequential upload lifecycle with TDD, Task 8: Disable streaming Stop when no handler exists, Task 9: Run the complete customer acceptance matrix and final diff review (+7 more)

### Community 120 - "scripts"
Cohesion: 0.50
Nodes (4): scripts, format, lint, typecheck

### Community 122 - "policy.py"
Cohesion: 0.08
Nodes (48): AskedQuestion, _aware(), CustomerReview, IntakeModel, IntakeState, Message, PendingQuestion, ProgressItem (+40 more)

### Community 123 - "TurnContext"
Cohesion: 0.14
Nodes (9): TurnContext, IntakeGraph, _invitation(), grounded_review(), ScriptedIntakeModel, test_graph_budget_uses_the_pinned_choice_and_timeout(), test_pin_failure_is_reported_as_model_unavailable(), test_without_pinning_the_budget_uses_settings() (+1 more)

### Community 124 - "Admin-managed, model-agnostic pipeline configuration — design specification"
Cohesion: 0.33
Nodes (5): 10. Out of scope, 1. Outcome and success criteria, 3. Decisions, 7. Error handling, Admin-managed, model-agnostic pipeline configuration — design specification

### Community 125 - "admin.py"
Cohesion: 0.12
Nodes (21): audit(), catalog(), _check_provider(), ChoiceInput, embedding_switch(), ModelOptions, models(), ProbeInput (+13 more)

### Community 126 - "guardrails.py"
Cohesion: 0.07
Nodes (45): Candidate, _add(), find_candidates(), normalize_phone(), _overlaps(), parse_amount(), resolve_date(), _safe_date() (+37 more)

### Community 129 - "intake/model.py"
Cohesion: 0.08
Nodes (32): quick_answer(), ImageInput, ModelCall, ModelUnavailable, _analysis_prompt(), _bounded_context(), _guard_size(), IntakeModel (+24 more)

### Community 130 - "Synthetic demo readiness"
Cohesion: 0.50
Nodes (4): Evidence by layer, Known limitations and remaining work, Repeatable local walkthrough, Synthetic demo readiness

### Community 131 - "intake.py"
Cohesion: 0.15
Nodes (22): ask_question(), create_session(), _credentials(), _dump(), get_session(), post_message(), read_attachment(), remove_attachment() (+14 more)

### Community 132 - "Review Focus"
Cohesion: 0.22
Nodes (10): api(), Review Focus, Task 1: Establish the safety baseline and remove tracked Graphify cache contents, Task 2: Delete the superseded architecture HTML after a fresh reference check, Task 3: Remove confirmed stale local runtime state and the duplicate screenshot, Task 4: Repair only current setup and processing documentation, Task 5: Restrict Docker build context without deleting installed dependencies, Task 6: Regenerate current Graphify outputs as the final mutating task (+2 more)

### Community 133 - "EmbeddingBatch"
Cohesion: 0.10
Nodes (9): EmbeddingBatch, Passage, SearchResult, Embeddings, LateEmbedder, NamedEmbedder, test_lock_serializes_operations_and_submit_waits_for_inflight_search(), embed() (+1 more)

### Community 137 - "types.py"
Cohesion: 0.05
Nodes (30): UnsupportedOperation, _capabilities(), DraftProviderResponseError, OpenRouterChat, OpenRouterProvider, _per_million(), provider_errors(), ProviderRegistry (+22 more)

### Community 139 - "pipeline/contracts.py"
Cohesion: 0.11
Nodes (27): Candidates, ClassificationResult, ClassifierOutput, NormalizedTicket, Classifier, build_order_check(), build_questions(), build_state() (+19 more)

### Community 142 - "pipeline/graph.py"
Cohesion: 0.07
Nodes (25): Decision, LookupResult, _default_retry(), _retryable(), decide(), empty_ticket_decision(), merge_reasons(), note_for() (+17 more)

### Community 144 - "probe.py"
Cohesion: 0.09
Nodes (20): Embedder, _chat(), _classify(), _describe(), _draft(), _embed(), _extract(), _intake() (+12 more)

### Community 148 - "components-ai-thought-chain.tsx"
Cohesion: 0.15
Nodes (15): Status, StatusIcon(), statusStyles, StepContext, StepContextType, ThoughtChain(), ThoughtChainContent(), ThoughtChainItem() (+7 more)

### Community 151 - "test_taxonomy.py"
Cohesion: 0.20
Nodes (3): TaxonomyError, taxonomy(), test_rejects_unknown_team()

### Community 154 - "ZainCash support: architecture and ticket flow {#support-overview}"
Cohesion: 0.50
Nodes (3): 1 · System architecture {#system-architecture}, 2 · Ticket flow {#ticket-flow}, ZainCash support: architecture and ticket flow {#support-overview}

### Community 155 - "IntakePage.test.tsx"
Cohesion: 0.07
Nodes (37): HTTP contract (implemented in Tasks 4–5), Task 6: Customer API client and resumable UI state, Task 7: Bilingual customer chat, screenshots and reviewed submission, copy(), session, malformed, populated, fakeApi() (+29 more)

### Community 156 - "employee-frontend/src/components/theme-provider.tsx"
Cohesion: 0.23
Nodes (11): disableTransitionsTemporarily(), getSystemTheme(), isEditableTarget(), isTheme(), ResolvedTheme, Theme, THEME_VALUES, ThemeProvider() (+3 more)

### Community 157 - "_ModelUsage"
Cohesion: 0.11
Nodes (12): _error_cost(), _Execution, _has_response_usage(), _ModelUsage, _number(), DraftContext, DraftModelInfo, test_anthropic_fallback_prices_and_provider_cost_precedence() (+4 more)

### Community 160 - ".save"
Cohesion: 0.11
Nodes (5): _view(), ProbeResult, test_choice_round_trip_keeps_colons_and_rejects_blank_model(), test_save_updates_cache_database_and_audit(), Task 4: The Models page, navigation and route

### Community 161 - "Customer phone identity design"
Cohesion: 0.13
Nodes (14): Backend, Canonical phone format, Customer phone identity design, Data model, Decisions, Employee API, employee-frontend, Error handling (+6 more)

### Community 167 - "build_pipeline"
Cohesion: 0.14
Nodes (20): build_pipeline(), ConfigError, model_ids(), run_batch(), FakeJevRunnable, FakeStructuredLLM, ScriptedChat, _settings() (+12 more)

### Community 168 - "Customer Conversation Intake Implementation Plan"
Cohesion: 0.20
Nodes (8): Completion audit — 2026-10-18, Customer Conversation Intake Implementation Plan, Execution conventions and repository baseline, File map and dependency order, Global Constraints, Plan review and execution handoff, Review Focus, Spec coverage and acceptance map

### Community 171 - "4. Backend design"
Cohesion: 0.20
Nodes (10): 9. Testing, 4.10 API, 4.11 CLI, 4.2 Usage metering, 4.4 Evaluation model list, 4.6 Runner, 4.7 Metrics, 4.8 Cost estimate (+2 more)

### Community 172 - "test_submission.py"
Cohesion: 0.32
Nodes (4): _payload(), test_concurrent_submit_dispatches_once(), test_second_request_id_reuses_the_approved_review(), test_submission_replay_creates_one_ticket()

## Ambiguous Edges - Review These
- `Fraud Report` → `Plan 1 Live Smoke`  [AMBIGUOUS]
  README.md · relation: conceptually_related_to

## Knowledge Gaps
- **83 isolated node(s):** `zaincash-support`, `@base-ui/react`, `@fontsource-variable/plus-jakarta-sans`, `@fontsource/tajawal`, `@tailwindcss/vite` (+78 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 1230 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **31 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Settings` connect `Settings` to `EmbeddingError`, `intake/model.py`, `ActiveModels`, `main.py`, `pytest`, `Synthetic demo readiness`, `types.py`, `test_rag_api.py`, `pipeline/contracts.py`, `pipeline/graph.py`, `make_output`, `intake/repository.py`, `_ModelUsage`, `test_draft_tools.py`, `test_kb_service.py`, `build_pipeline`, `fact`, `intake/test_repository.py`, `test_llm.py`, `httpx`, `tests/test_repository.py`, `fake_registry`, `test_workspace_api.py`, `cli.py`, `Step`, `test_rag_api.py`, `RAG drafting verification — 2026-10-17`, `KnowledgeError`, `test_final_fix_handoff.py`, `TurnContext`, `admin.py`?**
  _High betweenness centrality (0.095) - this node is a cross-community bridge._
- **Are the 55 inferred relationships involving `Settings` (e.g. with `_command_settings()` and `_run_in_memory()`) actually correct?**
  _`Settings` has 55 INFERRED edges - model-reasoned connections that need verification._
- **What connects `zaincash-support`, `@base-ui/react`, `@fontsource-variable/plus-jakarta-sans` to the rest of the system?**
  _83 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `EmbeddingError` be split into smaller, more focused modules?**
  _Cohesion score 0.07960199004975124 - nodes in this community are weakly interconnected._
- **Why does `2. Current state` connect `pipeline/contracts.py` to `Per-model evaluation (quality, system, cost) — design specification`, `workspace-ui.tsx`, `Card`, `build_pipeline`, `pipeline/graph.py`, `make_output`?**
  _High betweenness centrality (0.063) - this node is a cross-community bridge._
- **Are the 69 inferred relationships involving `Step` (e.g. with `catalog()` and `_check_provider()`) actually correct?**
  _`Step` has 69 INFERRED edges - model-reasoned connections that need verification._

### Low-confidence Hints
_AMBIGUOUS edges — the extractor was unsure. Verify before acting on these._

- **What is the exact relationship between `Fraud Report` and `Plan 1 Live Smoke`?**
  _Edge tagged AMBIGUOUS (relation: conceptually_related_to) - confidence is low._