-- Empty application data. Schema, extensions, and the support_test database stay.
-- Run against the application database (the Compose POSTGRES_DB), not support_test.
--
--   docker compose exec -T db sh -c \
--     'psql -v ON_ERROR_STOP=1 -U "$(tr -d "\r\n" < /run/secrets/postgres_user)" -d "$(tr -d "\r\n" < /run/secrets/postgres_db)"' \
--     < docker/db/cleanup.sql

BEGIN;

DO $$
DECLARE
    existing text;
BEGIN
    SELECT string_agg(format('%I', name), ', ' ORDER BY ordinality)
    INTO existing
    FROM unnest(ARRAY[
        'reviews',
        'intake_submissions',
        'intake_attachments',
        'intake_messages',
        'intake_operations',
        'intake_sessions',
        'ticket_results',
        'kb_chunks',
        'kb_document_indexes',
        'uploaded_documents',
        'tickets',
        'runs',
        'transactions',
        'service_incidents'
    ]) WITH ORDINALITY AS listed(name, ordinality)
    WHERE EXISTS (
        SELECT 1
        FROM information_schema.tables
        WHERE table_schema = current_schema()
          AND table_name = listed.name
    );

    IF existing IS NULL THEN
        RAISE NOTICE 'No application tables found in schema %.', current_schema();
        RETURN;
    END IF;

    EXECUTE 'TRUNCATE TABLE ' || existing || ' RESTART IDENTITY CASCADE';
END $$;

COMMIT;
