CREATE EXTENSION IF NOT EXISTS "pgcrypto";
CREATE TABLE IF NOT EXISTS collections (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  name VARCHAR(255) NOT NULL,
  description TEXT,
  embedding_model VARCHAR(100) NOT NULL DEFAULT 'text-embedding-3-small',
  chunking_strategy VARCHAR(50) NOT NULL DEFAULT 'semantic',
  qdrant_collection_name VARCHAR(255) UNIQUE NOT NULL,
  es_index_name VARCHAR(255) UNIQUE NOT NULL,
  document_count INTEGER DEFAULT 0,
  created_at TIMESTAMPTZ DEFAULT NOW()
);
CREATE TABLE IF NOT EXISTS documents (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  collection_id UUID REFERENCES collections(id),
  title VARCHAR(500),
  source_type VARCHAR(50) NOT NULL,
  source_uri TEXT,
  content_hash CHAR(64) UNIQUE,
  status VARCHAR(20) DEFAULT 'PENDING',
  language CHAR(2) DEFAULT 'en',
  page_count INTEGER,
  metadata JSONB DEFAULT '{}',
  error_message TEXT,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  indexed_at TIMESTAMPTZ
);
CREATE TABLE IF NOT EXISTS chunks (
  id UUID PRIMARY KEY,
  document_id UUID REFERENCES documents(id),
  chunk_index INTEGER NOT NULL,
  token_count INTEGER,
  start_page INTEGER,
  end_page INTEGER,
  heading_path TEXT,
  metadata JSONB DEFAULT '{}'
);
CREATE TABLE IF NOT EXISTS query_logs (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  session_id UUID,
  user_id UUID,
  collection_id UUID REFERENCES collections(id),
  question TEXT NOT NULL,
  answer TEXT,
  retrieved_chunk_ids UUID[],
  rerank_scores JSONB,
  llm_model VARCHAR(100),
  confidence_score FLOAT,
  latency_ms INTEGER,
  prompt_tokens INTEGER,
  completion_tokens INTEGER,
  cost_usd DECIMAL(10,6),
  created_at TIMESTAMPTZ DEFAULT NOW()
);
CREATE TABLE IF NOT EXISTS eval_datasets (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  name VARCHAR(255) NOT NULL,
  collection_id UUID REFERENCES collections(id),
  questions JSONB NOT NULL,
  created_at TIMESTAMPTZ DEFAULT NOW()
);
CREATE TABLE IF NOT EXISTS eval_runs (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  name VARCHAR(255),
  dataset_id UUID REFERENCES eval_datasets(id),
  pipeline_config JSONB NOT NULL,
  status VARCHAR(20) DEFAULT 'PENDING',
  faithfulness_score FLOAT,
  answer_relevancy_score FLOAT,
  context_precision_score FLOAT,
  context_recall_score FLOAT,
  hallucination_rate FLOAT,
  avg_latency_ms INTEGER,
  avg_cost_usd DECIMAL(10,6),
  total_questions INTEGER,
  results JSONB,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  completed_at TIMESTAMPTZ
);
CREATE INDEX IF NOT EXISTS idx_documents_collection ON documents(collection_id);
CREATE INDEX IF NOT EXISTS idx_documents_status ON documents(status);
CREATE INDEX IF NOT EXISTS idx_query_logs_collection ON query_logs(collection_id);
