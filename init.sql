-- Runs automatically the first time the postgres container initializes its data volume.
-- (It will NOT re-run on subsequent restarts, only on a fresh volume.)

-- Label Studio needs its own database, separate from your app/ML data
CREATE DATABASE labelstudio;

-- Enable pgvector in the main app database, for storing embeddings alongside your data
\connect "Postgre_ECO"
CREATE EXTENSION IF NOT EXISTS vector;

-- Example table for storing text + embeddings (adjust dimensions to your model)
-- CREATE TABLE IF NOT EXISTS embeddings (
--     id SERIAL PRIMARY KEY,
--     content TEXT NOT NULL,
--     embedding VECTOR(1536),
--     created_at TIMESTAMPTZ DEFAULT now()
-- );