-- ME/CE/AM 295 — knowledge base schema (Postgres + pgvector)
-- Embedding dimension = 1024 (Voyage voyage-3). If you switch embedding models,
-- change the vector(1024) dimension and re-index.

CREATE EXTENSION IF NOT EXISTS vector;

-- One row per normalized content file (content/**/*.md).
CREATE TABLE IF NOT EXISTS documents (
    id            BIGSERIAL PRIMARY KEY,
    source        TEXT UNIQUE NOT NULL,   -- original materials/ path (stable id)
    content_path  TEXT NOT NULL,          -- content/**/*.md
    title         TEXT,
    week          INTEGER NOT NULL DEFAULT 0,
    doc_type      TEXT NOT NULL,
    access        TEXT NOT NULL DEFAULT 'all_students',
    agents        TEXT[] NOT NULL DEFAULT ARRAY['all_student_agents'],
    content_hash  TEXT NOT NULL,          -- hash of the normalized .md (index incrementality)
    updated_at    TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- One row per chunk. Filter columns are denormalized from documents for speed.
CREATE TABLE IF NOT EXISTS chunks (
    id            BIGSERIAL PRIMARY KEY,
    document_id   BIGINT NOT NULL REFERENCES documents(id) ON DELETE CASCADE,
    chunk_index   INTEGER NOT NULL,
    section_title TEXT,
    text          TEXT NOT NULL,
    token_count   INTEGER,
    week          INTEGER NOT NULL DEFAULT 0,
    doc_type      TEXT NOT NULL,
    access        TEXT NOT NULL DEFAULT 'all_students',
    agents        TEXT[] NOT NULL DEFAULT ARRAY['all_student_agents'],
    embedding     vector(1024)
);

-- Week-gating and access filters run on every query.
CREATE INDEX IF NOT EXISTS chunks_week_idx   ON chunks (week);
CREATE INDEX IF NOT EXISTS chunks_access_idx ON chunks (access);
CREATE INDEX IF NOT EXISTS chunks_agents_idx ON chunks USING GIN (agents);

-- Approximate nearest-neighbor over cosine distance.
-- (HNSW is robust without training; build after first bulk load for best recall.)
CREATE INDEX IF NOT EXISTS chunks_embed_idx
    ON chunks USING hnsw (embedding vector_cosine_ops);
