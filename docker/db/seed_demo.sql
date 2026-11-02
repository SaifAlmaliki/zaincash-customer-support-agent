-- Synthetic workspace demo. Fictional tickets, transactions, and drafts only.
-- Does not index the knowledge base (no embeddings). Ingest policy files separately.
-- Expects empty tables. Run docker/db/cleanup.sql first.
--
--   docker compose exec -T db sh -c \
--     'psql -v ON_ERROR_STOP=1 -U "$(tr -d "\r\n" < /run/secrets/postgres_user)" -d "$(tr -d "\r\n" < /run/secrets/postgres_db)"' \
--     < docker/db/seed_demo.sql

BEGIN;

DO $$
BEGIN
    IF EXISTS (SELECT 1 FROM tickets)
        OR EXISTS (SELECT 1 FROM transactions)
        OR EXISTS (SELECT 1 FROM runs) THEN
        RAISE EXCEPTION 'Database is not empty. Run docker/db/cleanup.sql first.';
    END IF;
END $$;

INSERT INTO transactions (
    txn_ref, sender_phone, receiver_phone, receiver_name,
    amount_iqd, type, status, created_at, biller, agent_id, failure_reason
) VALUES
    ('ZC2410000123', '07809876543', '07701234567', 'علي حسين',
     50000, 'p2p', 'pending', '2026-10-06T18:10:00+03:00', NULL, NULL, NULL),
    ('ZC2410000456', '07723334455', NULL, NULL,
     35000, 'bill', 'completed', '2026-10-01T12:00:00+03:00', 'electricity', NULL, NULL),
    ('ZC2410000789', '07501112233', '07901234567', 'مجهول',
     200000, 'p2p', 'completed', '2026-10-07T08:00:00+03:00', NULL, NULL, NULL);

INSERT INTO service_incidents (id, service, started_at, ended_at, description) VALUES
    ('INC-01', 'bill_pay', '2026-10-01T08:00:00+03:00', '2026-10-01T16:00:00+03:00',
     'Electricity biller confirmation timeout: payments marked successful in the app but not posted to the biller');

INSERT INTO tickets (
    id, external_id, channel, customer_phone, text, received_at, source, batch_id
) VALUES
    (1, 'S-001', 'app', '07809876543',
     $t$حولت ٥٠ الف لاخوي على رقم 07701234567 امس وانقطعت من رصيدي بس ما وصلتله. رقم العملية ZC2410000123$t$,
     '2026-10-07T09:30:00+03:00', 'demo', 'demo-seed'),
    (2, 'S-002', 'whatsapp', '07501112233',
     $t$واحد اتصل بيه يكول انه موظف زين كاش وطلب الرمز اللي وصلني، انطيته وبعدها انسحب من حسابي 200 الف!! الحكوني$t$,
     '2026-10-07T10:05:00+03:00', 'demo', 'demo-seed'),
    (3, 'S-003', 'app', '07712223344',
     $t$ma da ywselni el code mal ta2keed, ma agdar afta7 el 7isab$t$,
     '2026-10-07T11:00:00+03:00', 'demo', 'demo-seed'),
    (4, 'S-004', 'app', '07723334455',
     $t$دفعت فاتورة الكهرباء 35,000 دينار يوم الخميس وطلعت ناجحة بس بعدها جاني اشعار انها ما مدفوعة$t$,
     '2026-10-07T12:15:00+03:00', 'demo', 'demo-seed'),
    (5, 'S-005', 'whatsapp', NULL,
     $t$شكد عمولة التحويل لحساب بنكي؟$t$,
     '2026-10-07T13:00:00+03:00', 'demo', 'demo-seed'),
    (6, 'RAG-DEMO-FAILED-TRANSFER', 'app', '07809876543',
     $t$حولت ٥٠ الف لاخوي على رقم 07701234567 امس وانقطعت من رصيدي بس ما وصلتله. رقم العملية ZC2410000123$t$,
     '2026-10-07T09:30:00+03:00', 'demo', 'demo-seed'),
    (7, 'RAG-DEMO-GENERAL', 'app', NULL,
     $t$شلون أشرح مشكلتي للدعم بأمان؟ شنو المعلومات غير السرية اللي أذكرها؟$t$,
     '2026-10-07T13:00:00+03:00', 'demo', 'demo-seed'),
    (8, 'RAG-DEMO-FRAUD', 'whatsapp', '07501112233',
     $t$واحد اتصل بيه يكول انه موظف زين كاش وطلب الرمز اللي وصلني، انطيته وبعدها انسحب من حسابي 200 الف!! الحكوني$t$,
     '2026-10-07T10:05:00+03:00', 'demo', 'demo-seed'),
    (9, 'RAG-DEMO-UNSUPPORTED', 'app', NULL,
     $t$اشرحلي بالتفصيل شلون التشابك الكمي يشتغل بين فوتونين داخل مختبر فيزياء؟$t$,
     '2026-10-07T14:00:00+03:00', 'demo', 'demo-seed');

INSERT INTO runs (
    id, started_at, finished_at, mode, prompt_version, model_ids,
    degraded, counts, total_cost_usd, status
) VALUES (
    1,
    '2026-10-07T15:00:00+03:00',
    '2026-10-07T15:04:00+03:00',
    'jev',
    'v1',
    '{"classifier":"jev","drafter":"demo-seed"}'::jsonb,
    FALSE,
    '{
      "total": 9,
      "by_status": {"pending_review": 5, "escalated": 3, "approved": 1},
      "by_category": {
        "failed_transfer": 2,
        "fraud_report": 2,
        "login_access": 1,
        "bill_payment": 1,
        "general_inquiry": 2,
        "other": 1
      },
      "by_team": {"Payments Ops": 3, "Account & Security": 3, "General Care": 3},
      "by_priority": {"P1": 2, "P2": 2, "P3": 2, "P4": 3},
      "escalation_reasons": {"fraud_suspected": 2, "no_kb_support": 1},
      "classifier_paths": {"jev": 9},
      "fallback_rate": 0.0,
      "degraded": false,
      "failed_ids": [],
      "latency_p50_ms": 900,
      "latency_p95_ms": 1400,
      "total_cost_usd": 0.0,
      "cost_per_ticket_usd": 0.0
    }'::jsonb,
    0.0,
    'completed'
);

INSERT INTO ticket_results (
    id, run_id, ticket_id, category, category_confidence, category_probs,
    priority, priority_confidence, flags, classifier_path, extracted,
    lookup_status, matched_txn_ref, team, escalated, escalation_reasons,
    escalation_note, draft_text, citations, agent_trace, status, error,
    latency_ms, cost_usd, jev_model_version, updated_at
) VALUES
(
    1, 1, 1, 'failed_transfer', 0.91,
    '{"failed_transfer": 0.91, "wrong_recipient": 0.05, "other": 0.04}'::jsonb,
    'P2', 0.88,
    '{"money_lost": 0.8}'::jsonb,
    'jev',
    '{
      "amount": {"value": 50000, "span": "٥٠ الف", "start": 6, "end": 12, "method": "span", "confidence": 0.9, "currency": "IQD"},
      "phone": {"value": "07701234567", "span": "07701234567", "start": 24, "end": 35, "method": "regex", "confidence": 0.99, "currency": null},
      "txn_ref": {"value": "ZC2410000123", "span": "ZC2410000123", "start": 70, "end": 82, "method": "regex", "confidence": 0.99, "currency": null},
      "date": {"value": "2026-10-06", "span": "امس", "start": 36, "end": 39, "method": "relative", "confidence": 0.8, "currency": null}
    }'::jsonb,
    'matched', 'ZC2410000123', 'Payments Ops', FALSE, '[]'::jsonb, NULL,
    $t$حسب السجل التجريبي، العملية ZC2410000123 بمبلغ 50000 دينار حالتها معلّقة، مو مكتملة. فريق Payments Ops يراجعها. هذا رد عرض خيالي وما يحرك أي مبلغ.$t$,
    '["failed_transfer.md#0"]'::jsonb,
    $tr$[
      {"kind": "tool", "tool": "lookup_transaction", "status": "ok", "arguments": {"txn_ref": "ZC2410000123"}},
      {"kind": "tool", "tool": "search_knowledge_base", "status": "ok", "arguments": {"query": "تحويل معلق"}},
      {"kind": "draft", "citation_sources": [{"id": "failed_transfer.md#0", "document_id": 1, "chunk_index": 0, "text": "إذا الحالة بالسجل pending، وضّح إن التحويل بعده معلّق حسب السجل.", "filename": "failed_transfer.md", "score": 0.84}]},
      {"kind": "guardrail", "findings": []}
    ]$tr$::jsonb,
    'pending_review', NULL, 980, 0.0, 'demo-seed', '2026-10-07T15:02:00+03:00'
),
(
    2, 1, 2, 'fraud_report', 0.96,
    '{"fraud_report": 0.96, "login_access": 0.03, "other": 0.01}'::jsonb,
    'P1', 0.97,
    '{"fraud_suspected": 0.98, "money_lost": 0.9}'::jsonb,
    'jev',
    '{
      "amount": {"value": 200000, "span": "200 الف", "start": 78, "end": 85, "method": "span", "confidence": 0.9, "currency": "IQD"},
      "phone": {"value": null, "span": null, "start": null, "end": null, "method": "none", "confidence": 0.0, "currency": null},
      "txn_ref": {"value": null, "span": null, "start": null, "end": null, "method": "none", "confidence": 0.0, "currency": null},
      "date": {"value": null, "span": null, "start": null, "end": null, "method": "none", "confidence": 0.0, "currency": null}
    }'::jsonb,
    'matched', 'ZC2410000789', 'Account & Security', TRUE,
    '["fraud_suspected"]'::jsonb,
    'Escalated: possible fraud or scam.',
    $t$هذه شبهة احتيال وتبقى أولوية عالية لفريق Account & Security. أوقف التواصل مع المتصل ولا تشارك أي رمز جديد. هذا رد عرض خيالي وما يعني تجميد الحساب أو استرجاع المبلغ.$t$,
    '["fraud_report.md#0"]'::jsonb,
    $tr$[
      {"kind": "tool", "tool": "lookup_transaction", "status": "ok", "arguments": {"txn_ref": "ZC2410000789"}},
      {"kind": "draft", "citation_sources": [{"id": "fraud_report.md#0", "document_id": 1, "chunk_index": 0, "text": "اعتبرها شبهة احتيال تحتاج إنسان بأولوية عالية.", "filename": "fraud_report.md", "score": 0.9}]},
      {"kind": "guardrail", "findings": []}
    ]$tr$::jsonb,
    'escalated', NULL, 1100, 0.0, 'demo-seed', '2026-10-07T15:02:10+03:00'
),
(
    3, 1, 3, 'login_access', 0.89,
    '{"login_access": 0.89, "account_kyc": 0.07, "other": 0.04}'::jsonb,
    'P3', 0.86, '{}'::jsonb, 'jev',
    '{
      "amount": {"value": null, "span": null, "start": null, "end": null, "method": "none", "confidence": 0.0, "currency": null},
      "phone": {"value": null, "span": null, "start": null, "end": null, "method": "none", "confidence": 0.0, "currency": null},
      "txn_ref": {"value": null, "span": null, "start": null, "end": null, "method": "none", "confidence": 0.0, "currency": null},
      "date": {"value": null, "span": null, "start": null, "end": null, "method": "none", "confidence": 0.0, "currency": null}
    }'::jsonb,
    'not_applicable', NULL, 'Account & Security', FALSE, '[]'::jsonb, NULL,
    $t$رمز التحقق ما يوصل، والحالة عند فريق Account & Security للمراجعة. جرّب طلب الرمز مرة ثانية من داخل التطبيق. هذا رد عرض خيالي.$t$,
    '["login_access.md#0"]'::jsonb,
    $tr$[
      {"kind": "tool", "tool": "search_knowledge_base", "status": "ok", "arguments": {"query": "رمز التحقق"}},
      {"kind": "draft", "citation_sources": [{"id": "login_access.md#0", "document_id": 1, "chunk_index": 0, "text": "مشكلة دخول أو رمز تحقق ما يوصل تروح لفريق Account & Security.", "filename": "login_access.md", "score": 0.8}]},
      {"kind": "guardrail", "findings": []}
    ]$tr$::jsonb,
    'pending_review', NULL, 760, 0.0, 'demo-seed', '2026-10-07T15:02:20+03:00'
),
(
    4, 1, 4, 'bill_payment', 0.9,
    '{"bill_payment": 0.9, "failed_transfer": 0.06, "other": 0.04}'::jsonb,
    'P3', 0.84, '{}'::jsonb, 'jev',
    '{
      "amount": {"value": 35000, "span": "35,000", "start": 22, "end": 28, "method": "span", "confidence": 0.95, "currency": "IQD"},
      "phone": {"value": null, "span": null, "start": null, "end": null, "method": "none", "confidence": 0.0, "currency": null},
      "txn_ref": {"value": null, "span": null, "start": null, "end": null, "method": "none", "confidence": 0.0, "currency": null},
      "date": {"value": "2026-10-01", "span": "يوم الخميس", "start": 36, "end": 46, "method": "relative", "confidence": 0.7, "currency": null}
    }'::jsonb,
    'matched', 'ZC2410000456', 'Payments Ops', FALSE, '[]'::jsonb, NULL,
    $t$العملية ZC2410000456 بمبلغ 35000 دينار للكهرباء ظاهرة مكتملة بالسجل التجريبي. إذا الجهة تكول غير مدفوعة، فريق Payments Ops يراجعها. ما نعد بوقت تصحيح. هذا رد عرض خيالي.$t$,
    '["bill_payment.md#0"]'::jsonb,
    $tr$[
      {"kind": "tool", "tool": "lookup_transaction", "status": "ok", "arguments": {"txn_ref": "ZC2410000456"}},
      {"kind": "draft", "citation_sources": [{"id": "bill_payment.md#0", "document_id": 1, "chunk_index": 0, "text": "دفعة فاتورة ظاهرة ناجحة وما انحسبت عند الجهة تراجعها Payments Ops.", "filename": "bill_payment.md", "score": 0.81}]},
      {"kind": "guardrail", "findings": []}
    ]$tr$::jsonb,
    'pending_review', NULL, 1020, 0.0, 'demo-seed', '2026-10-07T15:02:30+03:00'
),
(
    5, 1, 5, 'general_inquiry', 0.93,
    '{"general_inquiry": 0.93, "other": 0.07}'::jsonb,
    'P4', 0.9, '{}'::jsonb, 'jev',
    '{
      "amount": {"value": null, "span": null, "start": null, "end": null, "method": "none", "confidence": 0.0, "currency": null},
      "phone": {"value": null, "span": null, "start": null, "end": null, "method": "none", "confidence": 0.0, "currency": null},
      "txn_ref": {"value": null, "span": null, "start": null, "end": null, "method": "none", "confidence": 0.0, "currency": null},
      "date": {"value": null, "span": null, "start": null, "end": null, "method": "none", "confidence": 0.0, "currency": null}
    }'::jsonb,
    'not_applicable', NULL, 'General Care', FALSE, '[]'::jsonb, NULL,
    $t$دليل العرض التجريبي ما يحتوي رقم عمولة التحويل لحساب بنكي. فريق General Care يراجع السؤال من مصدر رسمي. ما نخمن الرسوم. هذا رد عرض خيالي.$t$,
    '["general_inquiry.md#0"]'::jsonb,
    $tr$[
      {"kind": "tool", "tool": "search_knowledge_base", "status": "ok", "arguments": {"query": "عمولة التحويل"}},
      {"kind": "draft", "citation_sources": [{"id": "general_inquiry.md#0", "document_id": 1, "chunk_index": 0, "text": "هذا المصدر ما يحتوي أرقام أو شروط حقيقية. لا تخمّن.", "filename": "general_inquiry.md", "score": 0.86}]},
      {"kind": "guardrail", "findings": []}
    ]$tr$::jsonb,
    'pending_review', NULL, 640, 0.0, 'demo-seed', '2026-10-07T15:02:40+03:00'
),
(
    6, 1, 6, 'failed_transfer', 0.91,
    '{"failed_transfer": 0.91, "wrong_recipient": 0.05, "other": 0.04}'::jsonb,
    'P2', 0.88, '{"money_lost": 0.8}'::jsonb, 'jev',
    '{
      "amount": {"value": 50000, "span": "٥٠ الف", "start": 6, "end": 12, "method": "span", "confidence": 0.9, "currency": "IQD"},
      "phone": {"value": "07701234567", "span": "07701234567", "start": 24, "end": 35, "method": "regex", "confidence": 0.99, "currency": null},
      "txn_ref": {"value": "ZC2410000123", "span": "ZC2410000123", "start": 70, "end": 82, "method": "regex", "confidence": 0.99, "currency": null},
      "date": {"value": "2026-10-06", "span": "امس", "start": 36, "end": 39, "method": "relative", "confidence": 0.8, "currency": null}
    }'::jsonb,
    'matched', 'ZC2410000123', 'Payments Ops', FALSE, '[]'::jsonb, NULL,
    $t$حسب السجل التجريبي، العملية ZC2410000123 بمبلغ 50000 دينار حالتها معلّقة، مو مكتملة. فريق Payments Ops يراجعها. هذا رد عرض خيالي وما يحرك أي مبلغ.$t$,
    '["failed_transfer.md#0"]'::jsonb,
    $tr$[
      {"kind": "tool", "tool": "lookup_transaction", "status": "ok", "arguments": {"txn_ref": "ZC2410000123"}},
      {"kind": "draft", "citation_sources": [{"id": "failed_transfer.md#0", "document_id": 1, "chunk_index": 0, "text": "إذا الحالة بالسجل pending، وضّح إن التحويل بعده معلّق حسب السجل.", "filename": "failed_transfer.md", "score": 0.84}]},
      {"kind": "guardrail", "findings": []}
    ]$tr$::jsonb,
    'pending_review', NULL, 990, 0.0, 'demo-seed', '2026-10-07T15:03:00+03:00'
),
(
    7, 1, 7, 'general_inquiry', 0.94,
    '{"general_inquiry": 0.94, "other": 0.06}'::jsonb,
    'P4', 0.91, '{}'::jsonb, 'jev',
    '{
      "amount": {"value": null, "span": null, "start": null, "end": null, "method": "none", "confidence": 0.0, "currency": null},
      "phone": {"value": null, "span": null, "start": null, "end": null, "method": "none", "confidence": 0.0, "currency": null},
      "txn_ref": {"value": null, "span": null, "start": null, "end": null, "method": "none", "confidence": 0.0, "currency": null},
      "date": {"value": null, "span": null, "start": null, "end": null, "method": "none", "confidence": 0.0, "currency": null}
    }'::jsonb,
    'not_applicable', NULL, 'General Care', FALSE, '[]'::jsonb, NULL,
    $t$اكتب وصف مختصر للمشكلة ورسالة الخطأ ومرجع العملية غير السري إذا عندك. لا ترسل رمز التحقق أو الرقم السري أو صورة المستمسكات. هذا رد عرض خيالي.$t$,
    '["general_inquiry.md#0"]'::jsonb,
    $tr$[
      {"kind": "tool", "tool": "search_knowledge_base", "status": "ok", "arguments": {"query": "معلومات آمنة للدعم"}},
      {"kind": "draft", "citation_sources": [{"id": "general_inquiry.md#0", "document_id": 1, "chunk_index": 0, "text": "يذكر المعلومات المطلوبة للمشكلة فقط، بدون إرسال أسرار الحساب.", "filename": "general_inquiry.md", "score": 0.88}]},
      {"kind": "guardrail", "findings": []}
    ]$tr$::jsonb,
    'approved', NULL, 700, 0.0, 'demo-seed', '2026-10-07T15:05:00+03:00'
),
(
    8, 1, 8, 'fraud_report', 0.96,
    '{"fraud_report": 0.96, "login_access": 0.03, "other": 0.01}'::jsonb,
    'P1', 0.97,
    '{"fraud_suspected": 0.98, "money_lost": 0.9}'::jsonb,
    'jev',
    '{
      "amount": {"value": 200000, "span": "200 الف", "start": 78, "end": 85, "method": "span", "confidence": 0.9, "currency": "IQD"},
      "phone": {"value": null, "span": null, "start": null, "end": null, "method": "none", "confidence": 0.0, "currency": null},
      "txn_ref": {"value": null, "span": null, "start": null, "end": null, "method": "none", "confidence": 0.0, "currency": null},
      "date": {"value": null, "span": null, "start": null, "end": null, "method": "none", "confidence": 0.0, "currency": null}
    }'::jsonb,
    'matched', 'ZC2410000789', 'Account & Security', TRUE,
    '["fraud_suspected"]'::jsonb,
    'Escalated: possible fraud or scam.',
    $t$هذه شبهة احتيال وتبقى أولوية عالية لفريق Account & Security. أوقف التواصل مع المتصل ولا تشارك أي رمز جديد. هذا رد عرض خيالي وما يعني تجميد الحساب أو استرجاع المبلغ.$t$,
    '["fraud_report.md#0"]'::jsonb,
    $tr$[
      {"kind": "tool", "tool": "lookup_transaction", "status": "ok", "arguments": {"txn_ref": "ZC2410000789"}},
      {"kind": "draft", "citation_sources": [{"id": "fraud_report.md#0", "document_id": 1, "chunk_index": 0, "text": "اعتبرها شبهة احتيال تحتاج إنسان بأولوية عالية.", "filename": "fraud_report.md", "score": 0.9}]},
      {"kind": "guardrail", "findings": []}
    ]$tr$::jsonb,
    'escalated', NULL, 1120, 0.0, 'demo-seed', '2026-10-07T15:03:20+03:00'
),
(
    9, 1, 9, 'other', 0.72,
    '{"other": 0.72, "general_inquiry": 0.2, "app_bug": 0.08}'::jsonb,
    'P4', 0.6, '{}'::jsonb, 'jev',
    '{
      "amount": {"value": null, "span": null, "start": null, "end": null, "method": "none", "confidence": 0.0, "currency": null},
      "phone": {"value": null, "span": null, "start": null, "end": null, "method": "none", "confidence": 0.0, "currency": null},
      "txn_ref": {"value": null, "span": null, "start": null, "end": null, "method": "none", "confidence": 0.0, "currency": null},
      "date": {"value": null, "span": null, "start": null, "end": null, "method": "none", "confidence": 0.0, "currency": null}
    }'::jsonb,
    'not_applicable', NULL, 'General Care', TRUE,
    '["no_kb_support"]'::jsonb,
    'Escalated: no policy document supports a reply.',
    $t$هذا السؤال خارج دليل الدعم التجريبي، وما أكدر أشرح موضوع علمي من خارج المصادر. فريق General Care يراجع إذا أكو طلب يخص المحفظة. هذا رد عرض خيالي.$t$,
    '[]'::jsonb,
    '[{"kind": "tool", "tool": "search_knowledge_base", "status": "ok", "arguments": {"query": "تشابك كمي"}}]'::jsonb,
    'escalated', NULL, 540, 0.0, 'demo-seed', '2026-10-07T15:03:40+03:00'
);

INSERT INTO reviews (id, result_id, reviewer, action, final_text, edit_distance, created_at) VALUES
(
    1, 7, 'demo.reviewer', 'approve',
    $t$اكتب وصف مختصر للمشكلة ورسالة الخطأ ومرجع العملية غير السري إذا عندك. لا ترسل رمز التحقق أو الرقم السري أو صورة المستمسكات. راجعنا النص وثبتناه للعرض فقط.$t$,
    42,
    '2026-10-07T15:05:00+03:00'
);

SELECT setval(pg_get_serial_sequence('tickets', 'id'), (SELECT MAX(id) FROM tickets));
SELECT setval(pg_get_serial_sequence('runs', 'id'), (SELECT MAX(id) FROM runs));
SELECT setval(pg_get_serial_sequence('ticket_results', 'id'), (SELECT MAX(id) FROM ticket_results));
SELECT setval(pg_get_serial_sequence('reviews', 'id'), (SELECT MAX(id) FROM reviews));

COMMIT;
