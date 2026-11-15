-- Idempotent add for a database that already has the original demo seed.
-- Fresh setups get the same rows from seed_demo.sql.

INSERT INTO customers (phone) VALUES
    ('07821110001'), ('07831110002'), ('07841110003'), ('07851110004'),
    ('07861110005'), ('07871110006'), ('07881110007'), ('07891110008'),
    ('07921110009')
ON CONFLICT DO NOTHING;

INSERT INTO transactions (
    txn_ref, sender_phone, receiver_phone, receiver_name,
    amount_iqd, type, status, created_at, biller, agent_id, failure_reason
) VALUES
    ('ZC2410001001', '07821110001', '07706543210', 'شخص غير معروف',
     100000, 'p2p', 'completed', '2026-10-07T11:00:00+03:00', NULL, NULL, NULL),
    ('ZC2410001002', '07841110003', NULL, NULL,
     200000, 'cash_in', 'failed', '2026-10-07T08:30:00+03:00', NULL, 'AG-JU', 'الشحن ما نزل بالحساب'),
    ('ZC2410001003', '07861110005', NULL, NULL,
     10000, 'bill', 'completed', '2026-10-07T14:40:00+03:00', 'آسيا سيل', NULL, NULL),
    ('ZC2410001004', '07881110007', '07890001122', 'متجر النور',
     25000, 'merchant', 'completed', '2026-10-07T12:00:00+03:00', NULL, NULL, NULL)
ON CONFLICT (txn_ref) DO NOTHING;

UPDATE ticket_results AS result
SET lookup_status = 'matched',
    matched_txn_ref = match.ref
FROM tickets AS ticket
JOIN (VALUES
    ('RAG-DEMO-WRONG-RECIPIENT', 'ZC2410001001'),
    ('RAG-DEMO-AGENT', 'ZC2410001002'),
    ('RAG-DEMO-BILL', 'ZC2410001003'),
    ('RAG-DEMO-REFUND', 'ZC2410001004')
) AS match(external_id, ref) ON ticket.external_id = match.external_id
WHERE result.ticket_id = ticket.id
  AND result.matched_txn_ref IS NULL;
