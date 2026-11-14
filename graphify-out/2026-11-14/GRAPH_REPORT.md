# Graph Report - zaincash-support  (2026-11-14)

## Corpus Check
- 409 files · ~487,900 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 25 file(s) not represented in the graph (top: (none) 15, .jsonl 4, .css 4)

## Summary
- 4113 nodes · 13687 edges · 169 communities (138 shown, 31 thin omitted)
- Extraction: 84% EXTRACTED · 16% INFERRED · 0% AMBIGUOUS · INFERRED: 2137 edges (avg confidence: 0.93)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `b698403e`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- EmbeddingError
- ActiveModels
- pytest
- asyncio
- investigation.py
- test_admin_api.py
- Card
- Customer conversation intake for ZainCash support
- lib/types.ts
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
- main.py
- compilerOptions
- web/src/components/theme-provider.tsx
- Step
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
- AttachmentStore
- contracts.ts
- test_llm.py
- TicketRow
- knowledge-view.test.tsx
- File structure
- tasks
- knowledge.py
- ChangeModelDialog.tsx
- IntakePage.tsx
- PipelineState
- agent-chat.tsx
- httpx
- collapsible.tsx
- guardrails.py
- ProviderRegistry
- IntakeRepository
- PipelineState
- test_workspace_api.py
- test_interview_api.py
- devDependencies
- cli.py
- build_tools
- FakeProvider
- Review Focus
- KnowledgeError
- Guided intake interview verification — 2026-11-13
- test_handoff.py
- test_recovery_regressions.py
- find_candidates
- Credentials
- Customer intake chat layout
- turns.py
- test_draft_model.py
- tools.py
- devDependencies
- devDependencies
- pipeline/contracts.py
- ticket-flow.ts
- compilerOptions
- LLMUnavailable
- Task 5: Pipeline and knowledge base use ActiveModels
- dependencies
- InvalidEvidence
- dependencies
- compilerOptions
- KnowledgeError
- intake/api.ts
- test_final_fix_handoff.py
- DraftToolLimit
- pydantic
- scripts
- resolve_date
- compilerOptions
- Maintainability and stale-code refactor — design specification
- 5. Backend design
- web/tsconfig.json
- employee-frontend/tsconfig.json
- exports
- Review Focus
- scripts
- users-frontend/README.md
- policy.py
- TurnContext
- Backend
- admin.py
- to_ascii_digits
- DraftSubmission
- IndexJobs
- intake/model.py
- Settings
- intake.py
- Review Focus
- EmbeddingError
- 10. Verification and acceptance
- FakeXHR
- 7. Customer frontend design
- types.py
- 8. Repository hygiene and current documentation
- pipeline/contracts.py
- TurnStore
- scripts
- pipeline/graph.py
- probe.py
- components-ai-thought-chain.tsx
- intake/README.md
- test_taxonomy.py
- ZainCash support: architecture and ticket flow {#support-overview}
- IntakePage.test.tsx
- employee-frontend/src/components/theme-provider.tsx
- _ModelUsage
- EmbeddingSwitches
- Customer phone identity design
- api-entrypoint.sh
- test_workspace_schema.py
- build_pipeline
- support_test
- dependencies
- 4. Backend design
- test_submission.py
- setup.ts

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

## Communities (169 total, 31 thin omitted)

### Community 0 - "EmbeddingError"
Cohesion: 0.12
Nodes (36): OpenRouterEmbedder, embedder_for(), item(), response_payload(), settings(), test_33_inputs_are_batched_and_each_batch_maps_its_own_indexes(), respond(), test_billed_batch_cost_survives_cancellation_without_cross_call_leakage() (+28 more)

### Community 1 - "ActiveModels"
Cohesion: 0.09
Nodes (30): ActiveModels, make_gemini_llm(), batch_concurrency(), _current_models(), _local_pipeline(), ticket_timeout_s(), fake_registry(), FakeProvider (+22 more)

### Community 2 - "pytest"
Cohesion: 0.13
Nodes (48): DraftModelInfo, test_blank_intake_model_is_rejected(), test_contracts_reject_extra_keys(), test_datetimes_must_be_timezone_aware(), test_non_positive_image_limit_is_rejected(), _tool_chat(), answer(), call() (+40 more)

### Community 3 - "asyncio"
Cohesion: 0.09
Nodes (32): session(), _safe_dispatch(), get_run(), list_runs(), start_run(), RunRow, create_run(), save_outcomes() (+24 more)

### Community 4 - "investigation.py"
Cohesion: 0.17
Nodes (13): parse_dt(), DraftToolInputError, _datetime(), _days(), _field(), _involves(), _phone(), _phones() (+5 more)

### Community 5 - "test_admin_api.py"
Cohesion: 0.43
Nodes (6): make_client(), test_admin_is_disabled_without_a_token(), test_models_and_catalog(), test_non_ascii_and_blank_tokens_are_rejected(), test_save_rejections_change_nothing(), test_test_save_and_audit()

### Community 6 - "Card"
Cohesion: 0.13
Nodes (46): Task 5: Extract presentational DocumentList and KnowledgeReadiness components, 6.4 Focused view extraction, Card(), CardContent(), CardHeader(), CardTitle(), Input(), AdminUnlock() (+38 more)

### Community 7 - "Customer conversation intake for ZainCash support"
Cohesion: 0.06
Nodes (31): 10. Verification and acceptance criteria, 11. Delivery and review, 1. Outcome and agreed requirements, 2. Current implementation and integration points, 3. Approach and boundaries, 4. Conversation state and turn flow, 5. Facts, evidence, and readiness, 6. Language and screenshot behavior (+23 more)

### Community 8 - "lib/types.ts"
Cohesion: 0.06
Nodes (29): Task 8: Employee evidence panel and processing state, Task 4: Extract and test the pure queue projection, projectQueue(), QueueFilters, QueueProjection, QueueTab, receivedAt(), source (+21 more)

### Community 9 - "IntakeController"
Cohesion: 0.15
Nodes (12): Task 6: Customer API client and resumable UI state, Task 1: Cleanup-first removal of reference-verified dead code and dependencies, Task 7: Preserve resume-unavailable state across `startNew`, Task 7: Intake app data layer — phone helper, contracts, API, controller, Task 7: Customer frontend data layer, ControllerState, emptyState(), IntakeController (+4 more)

### Community 10 - "FakeJevRunnable"
Cohesion: 0.09
Nodes (28): CredentialCheck, DegradedCredentialChecker, _finite_nonnegative(), _get(), JevCredentialChecker, FakeJevRunnable, ResponseRunnable, test_bad_usage_cannot_poison_cost() (+20 more)

### Community 11 - "test_rag_api.py"
Cohesion: 0.06
Nodes (45): init_db(), initialize_database(), make_engine(), make_sessionmaker(), reset_db(), create_app(), intake_db(), reviewed() (+37 more)

### Community 12 - "employee-frontend/package.json"
Cohesion: 0.06
Nodes (30): @base-ui/react, class-variance-authority, cn, eslint, @eslint/js, eslint-plugin-react-hooks, eslint-plugin-react-refresh, @fontsource/tajawal (+22 more)

### Community 14 - "QueuePage.tsx"
Cohesion: 0.12
Nodes (52): Task 3: Split RunDetailPage and introduce bounded run-result loading, Task 12: Locale parity test and translated Runs pages, Task 10: Employee app — customer page and ticket header link, Task 9: Employee app — required phone, queue identity and search, batch entry, Task 15: Ticket cost table and AI timeline, 6.4 Visible to all employees, 5.1 Data access, 7. Testing (+44 more)

### Community 15 - "Support Taxonomy Categories"
Cohesion: 0.21
Nodes (22): lookup, Account KYC, Account & Security, Agent Dispute, Agent Network, App Bug, Bill Payment, Card Issue (+14 more)

### Community 16 - "ui/package.json"
Cohesion: 0.08
Nodes (24): @base-ui/react, class-variance-authority, cn, eslint, @eslint/js, eslint-plugin-react-hooks, eslint-plugin-react-refresh, @fontsource/tajawal (+16 more)

### Community 17 - "ModelsPage.tsx"
Cohesion: 0.09
Nodes (36): App(), CustomerPage, EvaluationPage, InsightsPage, KnowledgePage, ModelsPage, NewBatchPage, QueuePage (+28 more)

### Community 18 - "users-frontend/package.json"
Cohesion: 0.08
Nodes (23): turbo, devDependencies, prettier, prettier-plugin-tailwindcss, turbo, typescript, engines, node (+15 more)

### Community 19 - "make_output"
Cohesion: 0.09
Nodes (41): build_graph(), PipelineDeps, InMemoryTransactionRepo, load_taxonomy(), tax(), FakeClassifier, make_output(), make_ticket() (+33 more)

### Community 20 - "test_draft_guardrails.py"
Cohesion: 0.13
Nodes (28): requests_credentials(), check(), state(), test_aggregation_is_deduplicated_and_has_no_state_side_effects(), test_amount_occurrences_keep_their_own_currency_and_sign(), test_avoid_sharing_warning_does_not_excuse_a_later_request(), test_candidate_prompt_limit_does_not_hide_later_ungrounded_references(), test_candidate_transactions_cannot_authorize_reply_evidence() (+20 more)

### Community 21 - "web/package.json"
Cohesion: 0.09
Nodes (22): jsdom, @workspace/ui, eslint, @eslint/js, eslint-plugin-react-hooks, eslint-plugin-react-refresh, globals, react (+14 more)

### Community 22 - "test_interview_scenarios.py"
Cohesion: 0.31
Nodes (9): analyze_calls(), Chat, source_of(), summary(), test_complete_report_goes_straight_to_review(), test_no_reference_number_still_gives_a_complete_report(), test_vague_report_is_interviewed_into_a_complete_ticket(), updates() (+1 more)

### Community 23 - "compilerOptions"
Cohesion: 0.08
Nodes (23): compilerOptions, allowArbitraryExtensions, allowImportingTsExtensions, erasableSyntaxOnly, jsx, lib, module, moduleDetection (+15 more)

### Community 24 - "employee-frontend/components.json"
Cohesion: 0.09
Nodes (21): aliases, components, hooks, lib, ui, utils, iconLibrary, menuAccent (+13 more)

### Community 25 - "main.py"
Cohesion: 0.06
Nodes (32): ensure_customers(), Base, CustomerRow, Receipt, IntakeOperationRow, IntakeSessionRow, IntakeSubmissionRow, IntakeError (+24 more)

### Community 26 - "compilerOptions"
Cohesion: 0.09
Nodes (22): compilerOptions, allowArbitraryExtensions, allowImportingTsExtensions, erasableSyntaxOnly, jsx, lib, module, moduleDetection (+14 more)

### Community 27 - "web/src/components/theme-provider.tsx"
Cohesion: 0.10
Nodes (19): App(), controller, disableTransitionsTemporarily(), getSystemTheme(), isEditableTarget(), isTheme(), ResolvedTheme, Theme (+11 more)

### Community 28 - "Step"
Cohesion: 0.12
Nodes (15): ConfiguredEmbedder, _Store, draft_timeout_s(), eligibility(), env_defaults(), intake_timeout_s(), Step, _Store (+7 more)

### Community 29 - "Classify and Extract Prompts"
Cohesion: 0.33
Nodes (7): extract, gemini_classify, Pipeline Graph Orchestration, jev_classify, prepare, GeminiClassifier, JevClassifier

### Community 30 - "test_draft_tools.py"
Cohesion: 0.12
Nodes (29): IncidentRow, TicketRow, TransactionRow, test_repeated_init_db_keeps_existing_tickets(), settings(), test_all_eight_tools_and_seven_parallel_calls_execute_only_six(), test_database_faults_remain_distinct_and_record_paid_search_cost(), test_discovered_ref_can_be_inspected_but_not_promoted_to_match() (+21 more)

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
Nodes (45): UploadedDocument, KnowledgeChunk, KnowledgeDocumentIndex, KnowledgeService, FakeEmbedder, GatedEmbedder, LateEmbedder, PaidEmbedder (+37 more)

### Community 36 - "web/components.json"
Cohesion: 0.10
Nodes (19): aliases, components, hooks, lib, ui, utils, iconLibrary, menuAccent (+11 more)

### Community 38 - "workspace-ui.tsx"
Cohesion: 0.06
Nodes (49): Global Constraints, Per-model Evaluation Implementation Plan — Part 3 of 3 (frontend, translations, verification), Task 13: Evaluation types, API client, formatters, copy and report import, Task 15: Provenance, headline metrics, comparison table and empty state, Task 16: Model detail, confusion matrix and predictions drawer, Task 17: Run dialog, progress, page assembly, route and styles, Task 18: Documentation, full verification and manual check, AI Usage and Performance Dashboard Implementation Plan — Part 2 of 2 (frontend, docs, verification) (+41 more)

### Community 39 - "ui/components.json"
Cohesion: 0.10
Nodes (19): aliases, components, hooks, lib, ui, utils, iconLibrary, menuAccent (+11 more)

### Community 40 - "fact"
Cohesion: 0.13
Nodes (61): Analysis, Attachment, EvidenceRef, Fact, Question, merge_analysis(), remove_attachment_evidence(), assess_readiness() (+53 more)

### Community 41 - "Guided intake interview — design"
Cohesion: 0.06
Nodes (33): 1. Question rules (backend), 2. API contract, 3. Chat screen, 4. Review card, Actions, Additional issues, Approach, Composer hints (+25 more)

### Community 43 - "Human Review Gate"
Cohesion: 0.25
Nodes (4): support CLI, Support Workspace UI Plan, Review API, Workspace UI Verification

### Community 44 - "compilerOptions"
Cohesion: 0.12
Nodes (16): compilerOptions, allowImportingTsExtensions, erasableSyntaxOnly, lib, module, moduleDetection, noEmit, noFallthroughCasesInSwitch (+8 more)

### Community 46 - "NewBatchPage.tsx"
Cohesion: 0.13
Nodes (19): Tabs(), TabsContent(), TabsList(), tabsListVariants, TabsTrigger(), Textarea(), exampleTickets, NewBatchPage() (+11 more)

### Community 47 - "compilerOptions"
Cohesion: 0.12
Nodes (16): compilerOptions, allowImportingTsExtensions, erasableSyntaxOnly, lib, module, moduleDetection, noEmit, noFallthroughCasesInSwitch (+8 more)

### Community 48 - "AI usage and performance dashboard (`/evaluation`) — design specification"
Cohesion: 0.15
Nodes (12): 10. Phase 2 (for reference, not designed here), 1. Outcome and success criteria, 3. Decisions, 5.1 Page, 5.2 Components and data, 5.3 Text and direction, 5. Frontend design, 6. Error handling (+4 more)

### Community 57 - "parse_document"
Cohesion: 0.10
Nodes (29): SearchResult, TextChunk, _append_chunks(), _check_extracted_size(), DocumentParseError, parse_document(), _parse_pdf(), _error_cost() (+21 more)

### Community 58 - "AttachmentStore"
Cohesion: 0.16
Nodes (19): AttachmentStore, _display_name(), ImageRejected, NotOwned, png_bytes(), repo(), store(), test_active_turn_rejects_upload() (+11 more)

### Community 59 - "contracts.ts"
Cohesion: 0.17
Nodes (34): Task 5: Add complete dependency-free API and persisted-session guards, createIntakeApi(), ANSWER_KINDS, CHOICES, FACT_STATUSES, finiteNonnegative(), invalid(), isRecord() (+26 more)

### Community 60 - "test_llm.py"
Cohesion: 0.13
Nodes (11): Sample, StructuredChatLLM, _llm(), _S, test_draft_model_uses_millisecond_timeout_and_disables_sdk_retries(), test_openrouter_reported_cost_takes_precedence_over_token_estimate(), test_openrouter_retry_budget_is_bounded(), test_openrouter_structured_samples_use_configured_key_and_validate_output() (+3 more)

### Community 61 - "TicketRow"
Cohesion: 0.06
Nodes (40): get_customer(), get_session(), get_result(), list_results(), read_intake_attachment(), review_result(), health(), insights() (+32 more)

### Community 62 - "knowledge-view.test.tsx"
Cohesion: 0.22
Nodes (14): Artifacts, servers and remaining concerns, acceptIndexRequest(), canRequestIndex(), PendingIndexes, persistPendingIndexes(), pollKnowledge(), refresh(), stop() (+6 more)

### Community 63 - "File structure"
Cohesion: 0.10
Nodes (10): DraftProviderResponseError, OpenRouterChat, provider_errors(), test_registry_includes_ollama_and_its_errors(), File structure, Task 11: Configuration, Docker and documentation, Task 2: OpenRouter and TypeSafe providers, registry, generic embedder, Task 3: Ollama provider (+2 more)

### Community 64 - "tasks"
Cohesion: 0.11
Nodes (18): dependsOn, inputs, outputs, cache, persistent, dependsOn, dependsOn, $schema (+10 more)

### Community 65 - "knowledge.py"
Cohesion: 0.09
Nodes (19): _configured(), delete_document(), download_document(), index_document(), list_chunks(), list_documents(), _require_provider(), search_knowledge() (+11 more)

### Community 66 - "ChangeModelDialog.tsx"
Cohesion: 0.07
Nodes (57): Admin model configuration — employee frontend implementation plan, Backend API contract used here, File structure, Global Constraints, Review Focus, Task 1: API types, admin session and admin requests, Task 2: Strings, the AI locality chip, run models and the batch switch message, Task 3: Model choice logic and the change dialog (+49 more)

### Community 67 - "IntakePage.tsx"
Cohesion: 0.07
Nodes (46): Global Constraints, Intake Chat UI Implementation Plan, Task 1: Put the summary and receipt in the thread, Task 2: Put screenshots inside the composer, Task 3: Apply the workspace chat styles, Task 4: Check the page in the browser, Task 8: Intake app UI — phone screen, profile chip, change number, receipt, Task 9: Progress strip (+38 more)

### Community 68 - "PipelineState"
Cohesion: 0.12
Nodes (15): 10. Remaining demo roadmap, 1. Intent and acceptance criteria, 3. Provider and configuration, 4. Knowledge ingestion and persistence, 5. Retrieval and evidence, 7. Draft guardrails and failure outcomes, 8. Pipeline, API, CLI and UI integration, 9. Demo policies and verification (+7 more)

### Community 69 - "agent-chat.tsx"
Cohesion: 0.16
Nodes (24): Task 8: Chat screen — instant bubble, typing, reasons, quick replies, composer hints, clsx, tailwind-merge, AgentChat, AgentChatProps, AgentMessage, AssistantText(), AttachedFile (+16 more)

### Community 70 - "httpx"
Cohesion: 0.11
Nodes (14): OllamaProvider, _provider(), _tags_handler(), test_catalog_lists_installed_models_with_reported_capabilities(), handler(), test_chat_model_sets_the_configured_context_window(), test_chat_model_targets_the_configured_server(), test_embedder_uses_openai_compatible_endpoint_without_dimensions() (+6 more)

### Community 72 - "guardrails.py"
Cohesion: 0.19
Nodes (14): normalize_phone(), parse_amount(), fold_arabic(), _iso(), normalize_value(), check_draft(), _citation_findings(), _exact_amount() (+6 more)

### Community 73 - "ProviderRegistry"
Cohesion: 0.17
Nodes (10): CatalogCache, step_catalog(), ProviderRegistry, UnknownProvider, BrokenStatusProvider, test_a_provider_whose_status_check_raises_is_listed_as_unreachable(), test_catalog_errors_stay_per_provider_and_cache_respects_ttl(), test_classify_catalog_only_offers_typesafe() (+2 more)

### Community 74 - "IntakeRepository"
Cohesion: 0.13
Nodes (6): IntakeRepository, builder(), fail_once(), repo(), repo(), turns()

### Community 75 - "PipelineState"
Cohesion: 0.07
Nodes (25): DraftResult, _Nodes, Drafter, DraftExecutionError, NullDrafter, UnavailableDrafter, PipelineState, draft() (+17 more)

### Community 76 - "test_workspace_api.py"
Cohesion: 0.11
Nodes (20): review_payload(), start_run(), test_batch_and_queue_expose_real_results(), test_batch_failure_is_isolated_and_conflicting_ids_rejected(), test_customer_profile_lists_the_latest_result_of_each_ticket(), test_only_jev_mode_is_configured_and_retired_modes_are_rejected(), test_progress_counts_only_durable_results_after_save_failure(), fail_one_save() (+12 more)

### Community 77 - "test_interview_api.py"
Cohesion: 0.21
Nodes (19): analyze_calls(), ask(), complete_without_reference(), opening(), opening_with_amount(), reference_answer(), send(), start() (+11 more)

### Community 79 - "devDependencies"
Cohesion: 0.12
Nodes (16): devDependencies, eslint, @eslint/js, eslint-plugin-react-hooks, eslint-plugin-react-refresh, globals, prettier, prettier-plugin-tailwindcss (+8 more)

### Community 80 - "cli.py"
Cohesion: 0.07
Nodes (28): _command_settings(), ingest_kb_cmd(), ingest(), init_db_cmd(), Mode, run_batch_cmd(), _run_in_memory(), _run_with_db() (+20 more)

### Community 81 - "build_tools"
Cohesion: 0.13
Nodes (7): build_tools(), flag(), retrieve(), _error_cost(), Backend Maintainability Implementation Plan, Global Constraints, Task 2: Separate Historical Escalation Text from Current Tool Reasons

### Community 82 - "FakeProvider"
Cohesion: 0.07
Nodes (24): probe(), ModelChoice, ProbeResult, recent(), test_start_updates_the_cache_without_reloading_from_the_database(), _registry(), StructuredChat, test_draft_probe_requires_a_correct_tool_call() (+16 more)

### Community 83 - "Review Focus"
Cohesion: 0.25
Nodes (7): Employee Frontend Maintainability Implementation Plan, Global Constraints, Review Focus, Task 1: Remove reference-verified dead exports, components, and the Mermaid dependency, Task 6: Repair ExtractedField fixtures and make standalone typecheck real, Task 7: Repair employee README paths/test-count guidance and run final acceptance, SelectSeparator()

### Community 84 - "KnowledgeError"
Cohesion: 0.15
Nodes (8): DocumentNotFoundError, IndexAttemptLostError, KnowledgeError, KnowledgeExecutionError, ErrorEmbedder, test_search_unexpected_fault_logs_only_safe_type(), fail_search(), Task 14: Preserve Safe Knowledge 503s and Log Only Unexpected Diagnostic Types

### Community 85 - "Guided intake interview verification — 2026-11-13"
Cohesion: 0.20
Nodes (9): Arabic at 390×844, starting from the vague message, English at 1280×900, with the complete message, Final automated checks, Guided intake interview verification — 2026-11-13, Live browser run, Live probe output (facts only), Live transfer probe, Observations (+1 more)

### Community 86 - "test_handoff.py"
Cohesion: 0.19
Nodes (15): _amount(), analyze(), complete_conversation(), _dated(), _message(), _opening(), _png(), _review() (+7 more)

### Community 87 - "test_recovery_regressions.py"
Cohesion: 0.36
Nodes (10): TurnResult, command(), create(), test_actual_app_restart_reconciles_failed_placeholder(), test_failed_review_retry_cannot_reopen_submitted_session(), test_original_payload_identity_survives_sanitization(), test_publication_failure_is_retryable_without_restart(), test_receipt_reference_is_preserved() (+2 more)

### Community 88 - "find_candidates"
Cohesion: 0.23
Nodes (12): Candidate, _add(), find_candidates(), _overlaps(), test_amount_forms(), test_arabic_indic_amount_not_confused_with_phone(), test_dates_absolute_and_weekday(), test_dedupes_repeated_values() (+4 more)

### Community 89 - "Credentials"
Cohesion: 0.33
Nodes (3): Credentials, SessionView, IntakeService

### Community 90 - "Customer intake chat layout"
Cohesion: 0.25
Nodes (6): Task 10: Grouped review card with answer buttons, 1. Outcome, 2. Scope, 3. Layout, 5. Checks, Customer intake chat layout

### Community 91 - "turns.py"
Cohesion: 0.31
Nodes (10): IntakeAttachmentRow, IntakeMessageRow, attachment_from_row(), load_attachments(), load_messages(), _message(), session_view(), turn_context() (+2 more)

### Community 92 - "test_draft_model.py"
Cohesion: 0.27
Nodes (8): make_draft_model(), response_payload(), run_provider_pipeline(), send(), search_response(), test_empty_choices_escalates_and_keeps_paid_response_usage(), test_failed_response_id_is_deduplicated_against_earlier_success(), test_other_conversion_value_errors_remain_unexpected()

### Community 93 - "tools.py"
Cohesion: 0.24
Nodes (8): _Flag, _History, _Input, _Knowledge, _Lookup, _Recent, _Search, _Service

### Community 94 - "devDependencies"
Cohesion: 0.11
Nodes (19): devDependencies, eslint, @eslint/js, eslint-plugin-react-hooks, eslint-plugin-react-refresh, globals, jsdom, @tailwindcss/vite (+11 more)

### Community 95 - "devDependencies"
Cohesion: 0.17
Nodes (12): devDependencies, eslint, @eslint/js, eslint-plugin-react-hooks, eslint-plugin-react-refresh, globals, tailwindcss, @types/node (+4 more)

### Community 96 - "pipeline/contracts.py"
Cohesion: 0.23
Nodes (16): FieldPick, NormalizedTicket, FieldExtractor, _field(), fill_gaps(), finalize(), _is_weak(), FakeExtractor (+8 more)

### Community 97 - "ticket-flow.ts"
Cohesion: 0.06
Nodes (62): Global Constraints, Task 1: Sentence catalog, Task 2: Which step is open, Task 3: Received, produced, and drafting events, Task 4: Mermaid source, Task 5: Draw the charts on the ticket page, Ticket Flow Charts Implementation Plan, Task 2: Migrate active TicketFlow coverage, then retire the legacy trace/chart cluster (+54 more)

### Community 99 - "compilerOptions"
Cohesion: 0.14
Nodes (13): compilerOptions, jsx, lib, module, moduleResolution, noEmit, paths, skipLibCheck (+5 more)

### Community 100 - "LLMUnavailable"
Cohesion: 0.10
Nodes (14): LLMUnavailable, StructuredLLM, ExtractedSpan, _Fields, GeminiExtractor, GeminiFields, verified_pick(), render_prompt() (+6 more)

### Community 101 - "Task 5: Pipeline and knowledge base use ActiveModels"
Cohesion: 0.20
Nodes (4): Embedder, Task 5: Pipeline and knowledge base use ActiveModels, 2. Current state, 4.9 Runtime embedder

### Community 102 - "dependencies"
Cohesion: 0.12
Nodes (16): dependencies, @base-ui/react, class-variance-authority, cn, @fontsource/tajawal, @fontsource-variable/plus-jakarta-sans, lucide-react, motion (+8 more)

### Community 103 - "InvalidEvidence"
Cohesion: 0.12
Nodes (28): ReviewText, canonical_digits(), normalize_reported_date(), InvalidEvidence, _apply(), _check_reference(), _compact(), checked_update() (+20 more)

### Community 104 - "dependencies"
Cohesion: 0.20
Nodes (10): dependencies, @base-ui/react, class-variance-authority, cn, @fontsource/tajawal, @fontsource-variable/plus-jakarta-sans, react, react-dom (+2 more)

### Community 105 - "compilerOptions"
Cohesion: 0.17
Nodes (11): compilerOptions, jsx, lib, module, moduleResolution, outDir, skipLibCheck, strict (+3 more)

### Community 106 - "KnowledgeError"
Cohesion: 0.09
Nodes (8): _abandoned(), _check_deadline(), _consume(), _DatabaseCall, document_view(), _Claim, Task 2: Atomic pgvector indexing and retrieval, Task 4: Extract KB Database Call Mechanics Without Changing Transactions

### Community 107 - "intake/api.ts"
Cohesion: 0.10
Nodes (24): Task 4: Make pending operations discriminated and use one request identity, IntakeApi, ANSWER_KINDS, INTAKE_FALLBACK_MESSAGE, Activity, fileIdentity(), AnswerKind, AskCommand (+16 more)

### Community 108 - "test_final_fix_handoff.py"
Cohesion: 0.09
Nodes (24): Passage, RagDrafter, ScriptedChat, assert_completed_evidence(), faulty_knowledge(), read(), outer_deadlines(), PaidEmbeddings (+16 more)

### Community 109 - "DraftToolLimit"
Cohesion: 0.20
Nodes (7): DraftAlreadySubmitted, DraftToolLimit, _bounded(), visit(), guarded(), invoke(), _json()

### Community 110 - "pydantic"
Cohesion: 0.23
Nodes (6): CitationSource, _Draft, draft_evidence(), _Guardrail, _TraceModel, _validated()

### Community 111 - "scripts"
Cohesion: 0.25
Nodes (8): scripts, build, dev, format, lint, preview, test, typecheck

### Community 112 - "resolve_date"
Cohesion: 0.36
Nodes (4): resolve_date(), _safe_date(), test_resolve(), test_unresolvable_is_none()

### Community 113 - "compilerOptions"
Cohesion: 0.29
Nodes (6): compilerOptions, module, moduleResolution, skipLibCheck, strict, target

### Community 114 - "Maintainability and stale-code refactor — design specification"
Cohesion: 0.18
Nodes (10): 1. Outcome and success criteria, 2. Audit baseline, 3. Selected approach and sequence, 4. Boundaries and non-goals, 6.1 Verification and cleanup, 6.2 Retire the legacy trace/chart cluster, 6.3 Runs and request loading, 6. Employee frontend design (+2 more)

### Community 115 - "5. Backend design"
Cohesion: 0.25
Nodes (6): 5.1 Dead-code cleanup, 5.2 Extraction ownership, 5.3 Knowledge-service boundary, 5.4 Shared backend boundaries, 5.5 Confirmed backend defect fixes, 5. Backend design

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
Cohesion: 0.22
Nodes (8): Customer Frontend Maintainability Implementation Plan, Global Constraints, Review Focus, Task 2: Make standalone typechecking and root test execution real, Task 3: Centralize test cleanup and shared intake fixtures mechanically, Task 6: Extract stable-ID sequential upload lifecycle with TDD, Task 8: Disable streaming Stop when no handler exists, Task 9: Run the complete customer acceptance matrix and final diff review

### Community 120 - "scripts"
Cohesion: 0.50
Nodes (4): scripts, format, lint, typecheck

### Community 122 - "policy.py"
Cohesion: 0.07
Nodes (52): AskedQuestion, _aware(), CustomerReview, IntakeModel, IntakeState, Message, PendingQuestion, ProgressItem (+44 more)

### Community 123 - "TurnContext"
Cohesion: 0.09
Nodes (17): quick_answer(), ModelCall, TurnContext, ModelUnavailable, IntakeGraph, _invitation(), make_intake_service(), grounded_analysis() (+9 more)

### Community 124 - "Backend"
Cohesion: 0.33
Nodes (6): Backend, Data model, Employee API, Existing data, Intake, Ticket write paths

### Community 125 - "admin.py"
Cohesion: 0.12
Nodes (20): audit(), catalog(), _check_provider(), ChoiceInput, embedding_switch(), ModelOptions, models(), ProbeInput (+12 more)

### Community 126 - "to_ascii_digits"
Cohesion: 0.18
Nodes (16): detect_arabizi(), has_latin_mix(), _latin_words(), normalize(), sanitize_for_storage(), mask_cards(), to_ascii_digits(), test_arabizi_detection() (+8 more)

### Community 129 - "intake/model.py"
Cohesion: 0.10
Nodes (29): ImageInput, _analysis_prompt(), _bounded_context(), _guard_size(), IntakeModel, validate(), ModelBudget, _record() (+21 more)

### Community 130 - "Settings"
Cohesion: 0.09
Nodes (16): get_settings(), Settings, test_relative_upload_directory_is_rooted_in_the_repository(), test_anthropic_model_selects_the_draft_model_only(), test_defaults(), test_draft_token_prices_follow_the_selected_draft_model(), test_drafting_configuration_cannot_bypass_hard_limits(), test_drafting_limits_load_from_environment() (+8 more)

### Community 131 - "intake.py"
Cohesion: 0.15
Nodes (22): ask_question(), create_session(), _credentials(), _dump(), get_session(), post_message(), read_attachment(), remove_attachment() (+14 more)

### Community 132 - "Review Focus"
Cohesion: 0.11
Nodes (18): api(), Global Constraints, Repository Hygiene Maintainability Implementation Plan, Review Focus, Task 1: Establish the safety baseline and remove tracked Graphify cache contents, Task 2: Delete the superseded architecture HTML after a fresh reference check, Task 3: Remove confirmed stale local runtime state and the duplicate screenshot, Task 4: Repair only current setup and processing documentation (+10 more)

### Community 133 - "EmbeddingError"
Cohesion: 0.09
Nodes (11): EmbeddingBatch, EmbeddingError, _nonnegative_number(), OpenAICompatibleEmbedder, _ordered_vectors(), _response_cost(), Embeddings, NamedEmbedder (+3 more)

### Community 134 - "10. Verification and acceptance"
Cohesion: 0.40
Nodes (5): 10. Verification and acceptance, Backend, Customer frontend, Employee frontend, Repository and Docker

### Community 136 - "7. Customer frontend design"
Cohesion: 0.50
Nodes (4): 7.1 Verification and cleanup, 7.2 Runtime contracts and persisted operations, 7.4 Controller, chat, and tests, 7. Customer frontend design

### Community 137 - "types.py"
Cohesion: 0.07
Nodes (18): UnsupportedOperation, _capabilities(), OpenRouterProvider, _per_million(), TypeSafeProvider, Capability, CatalogEntry, ProviderStatus (+10 more)

### Community 138 - "8. Repository hygiene and current documentation"
Cohesion: 0.50
Nodes (4): 8.1 Approved deletions, 8.2 Docker and documentation, 8.3 Graphify outputs, 8. Repository hygiene and current documentation

### Community 139 - "pipeline/contracts.py"
Cohesion: 0.13
Nodes (23): Candidates, ClassificationResult, ClassifierOutput, Classifier, build_order_check(), build_questions(), build_state(), category_criteria() (+15 more)

### Community 140 - "TurnStore"
Cohesion: 0.20
Nodes (11): OperationClaim, RevisionConflict, sanitize_intake_text(), _jsonable(), TurnStore, test_recovered_attempt_cannot_publish_stale_output(), test_review_publication_revision_matches_the_session(), Task 4: Resumable graph turns, review and customer API (+3 more)

### Community 141 - "scripts"
Cohesion: 0.25
Nodes (8): scripts, build, dev, format, lint, preview, test, typecheck

### Community 142 - "pipeline/graph.py"
Cohesion: 0.05
Nodes (67): finish_run(), load_incidents(), load_transactions(), SqlTransactionRepo, _ticket_phone(), _to_record(), _upsert(), upsert_tickets() (+59 more)

### Community 144 - "probe.py"
Cohesion: 0.09
Nodes (18): _chat(), _classify(), _describe(), _draft(), _embed(), _extract(), _intake(), _ProbeAnswer (+10 more)

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
Cohesion: 0.08
Nodes (37): HTTP contract (implemented in Tasks 4–5), Task 7: Bilingual customer chat, screenshots and reviewed submission, Task 9: End-to-end handoff, live vision evidence and runbook, copy(), @testing-library/react, @testing-library/user-event, parseJson(), readError() (+29 more)

### Community 156 - "employee-frontend/src/components/theme-provider.tsx"
Cohesion: 0.23
Nodes (11): disableTransitionsTemporarily(), getSystemTheme(), isEditableTarget(), isTheme(), ResolvedTheme, Theme, THEME_VALUES, ThemeProvider() (+3 more)

### Community 157 - "_ModelUsage"
Cohesion: 0.16
Nodes (9): _error_cost(), _has_response_usage(), _ModelUsage, _number(), DraftContext, Review Focus, Task 1: Telemetry core — `AiCall`, recording context, ledger table, `processed_at`, Task 3: Ticket outcomes carry their calls; batch and CLI write them with the result (+1 more)

### Community 160 - "EmbeddingSwitches"
Cohesion: 0.18
Nodes (5): EmbeddingSwitchRow, EmbeddingSwitches, _view(), test_runs_are_blocked_while_a_switch_runs_and_restart_recovers(), Task 4: The Models page, navigation and route

### Community 161 - "Customer phone identity design"
Cohesion: 0.22
Nodes (8): Canonical phone format, Customer phone identity design, Decisions, employee-frontend, Error handling, Intent, Out of scope, Testing

### Community 165 - "test_workspace_schema.py"
Cohesion: 0.29
Nodes (8): assert_customer_schema(), LegacySchemaError, _nullable(), _table_exists(), upgrade_workspace_schema(), test_fresh_schema_passes_the_customer_check(), test_intake_sessions_without_a_customer_phone_stop_startup(), test_nullable_ticket_phone_stops_startup_with_a_reset_instruction()

### Community 167 - "build_pipeline"
Cohesion: 0.13
Nodes (21): build_pipeline(), ConfigError, model_ids(), run_batch(), CredentialChecker, FakeStructuredLLM, test_config_error_exits_2(), boom() (+13 more)

### Community 168 - "support_test"
Cohesion: 0.04
Nodes (52): index_deadlines(), settings(), support_test(), test_source_validation_sanitizes_name_preserves_bom_and_caller_transaction(), expire_during_embedding(), Fictional RAG walkthrough inputs, Evidence by layer, Known limitations and remaining work (+44 more)

### Community 169 - "dependencies"
Cohesion: 0.33
Nodes (6): dependencies, clsx, react, react-dom, tailwind-merge, @workspace/ui

### Community 171 - "4. Backend design"
Cohesion: 0.06
Nodes (25): Deviations from the spec (intentional, small), Global Constraints, Per-model Evaluation Implementation Plan — Part 2 of 3 (evaluation engine), Task 11: `support eval` CLI and v2 export, Task 7: Metrics, Task 8: Evaluation storage and views, Task 9: Runner, request validation and cost estimate, 1. Outcome and success criteria (+17 more)

### Community 172 - "test_submission.py"
Cohesion: 0.32
Nodes (4): _payload(), test_concurrent_submit_dispatches_once(), test_second_request_id_reuses_the_approved_review(), test_submission_replay_creates_one_ticket()

## Ambiguous Edges - Review These
- `Fraud Report` → `Plan 1 Live Smoke`  [AMBIGUOUS]
  README.md · relation: conceptually_related_to

## Knowledge Gaps
- **83 isolated node(s):** `zaincash-support`, `@base-ui/react`, `@fontsource-variable/plus-jakarta-sans`, `@fontsource/tajawal`, `@tailwindcss/vite` (+78 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 1229 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **31 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Settings` connect `Settings` to `EmbeddingError`, `intake/model.py`, `ActiveModels`, `pytest`, `EmbeddingError`, `test_admin_api.py`, `types.py`, `test_rag_api.py`, `pipeline/contracts.py`, `pipeline/graph.py`, `make_output`, `main.py`, `Step`, `test_draft_tools.py`, `test_kb_service.py`, `test_workspace_schema.py`, `build_pipeline`, `fact`, `support_test`, `parse_document`, `AttachmentStore`, `test_llm.py`, `File structure`, `httpx`, `ProviderRegistry`, `IntakeRepository`, `test_workspace_api.py`, `cli.py`, `FakeProvider`, `test_draft_model.py`, `Task 5: Pipeline and knowledge base use ActiveModels`, `test_final_fix_handoff.py`, `TurnContext`, `admin.py`?**
  _High betweenness centrality (0.094) - this node is a cross-community bridge._
- **Are the 55 inferred relationships involving `Settings` (e.g. with `_command_settings()` and `_run_in_memory()`) actually correct?**
  _`Settings` has 55 INFERRED edges - model-reasoned connections that need verification._
- **What connects `zaincash-support`, `@base-ui/react`, `@fontsource-variable/plus-jakarta-sans` to the rest of the system?**
  _83 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `EmbeddingError` be split into smaller, more focused modules?**
  _Cohesion score 0.12323232323232323 - nodes in this community are weakly interconnected._
- **Why does `Choice` connect `intake/api.ts` to `probe.py`, `IntakeController`, `policy.py`, `IntakePage.test.tsx`?**
  _High betweenness centrality (0.062) - this node is a cross-community bridge._
- **Are the 69 inferred relationships involving `Step` (e.g. with `catalog()` and `_check_provider()`) actually correct?**
  _`Step` has 69 INFERRED edges - model-reasoned connections that need verification._

### Low-confidence Hints
_AMBIGUOUS edges — the extractor was unsure. Verify before acting on these._

- **What is the exact relationship between `Fraud Report` and `Plan 1 Live Smoke`?**
  _Edge tagged AMBIGUOUS (relation: conceptually_related_to) - confidence is low._