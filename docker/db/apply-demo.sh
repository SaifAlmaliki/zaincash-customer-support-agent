#!/bin/sh
set -eu
docker exec -i zaincash-customer-support-agent-db-1 psql -U support -d support -v ON_ERROR_STOP=1 \
  < /mnt/c/Dev/zaincash-customer-support-agent/docker/db/apply_demo_transactions.sql
docker exec -i zaincash-customer-support-agent-db-1 psql -U support -d support -c \
  "SELECT t.external_id, r.lookup_status, r.matched_txn_ref FROM tickets t JOIN ticket_results r ON r.ticket_id = t.id WHERE t.external_id LIKE 'RAG-DEMO-%' ORDER BY t.external_id;"
