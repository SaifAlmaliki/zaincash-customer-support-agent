FROM ghcr.io/astral-sh/uv:python3.11-bookworm-slim

RUN apt-get update \
    && apt-get install -y --no-install-recommends ca-certificates \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app/backend

ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    UV_NO_DEV=1

COPY backend/pyproject.toml backend/uv.lock ./
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-install-project --no-dev

COPY backend/app ./app
COPY backend/tests/fixtures ./tests/fixtures
COPY data/taxonomy.yaml /app/data/taxonomy.yaml
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-dev

ENV PATH="/app/backend/.venv/bin:$PATH" \
    SSL_CERT_FILE=/etc/ssl/certs/ca-certificates.crt \
    REQUESTS_CA_BUNDLE=/etc/ssl/certs/ca-certificates.crt \
    CURL_CA_BUNDLE=/etc/ssl/certs/ca-certificates.crt

EXPOSE 8000

# seed-db creates the schema and upserts the demo rows, so a restart is safe.
CMD ["sh", "-c", "support seed-db --transactions tests/fixtures/sample_transactions.jsonl --incidents tests/fixtures/sample_incidents.jsonl && exec uvicorn app.main:app --host 0.0.0.0 --port 8000"]
