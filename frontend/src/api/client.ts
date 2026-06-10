const BASE = import.meta.env.VITE_DOCMIND_API_URL ?? 'http://localhost:8000/api/v1';

async function json<T>(path: string, init?: RequestInit): Promise<T> {
  const headers = init?.body instanceof FormData ? undefined : { 'Content-Type': 'application/json' };
  const res = await fetch(`${BASE}${path}`, { headers, ...init });
  if (!res.ok) throw new Error(await res.text());
  return res.json();
}

export type Collection = { id: string; name: string; description?: string; document_count: number; chunking_strategy: string; embedding_model: string };
export type Document = { id: string; title: string; status: string; source_type: string; page_count: number; indexed_at?: string };
export type QueryResponse = { answer: string; confidence_score: number; sources: { document_title: string; page: number; chunk_content: string; relevance_score: number }[]; metadata: { latency_ms: number; cost_usd: number; retrieval_strategy: string; chunks_retrieved: number } };

export const api = {
  seedDemo: () => json<any>('/demo/seed', { method: 'POST' }),
  collections: () => json<Collection[]>('/collections'),
  createCollection: (body: { name: string; description?: string; chunking_strategy?: string }) => json<Collection>('/collections', { method: 'POST', body: JSON.stringify(body) }),
  documents: (collectionId: string) => json<Document[]>(`/collections/${collectionId}/documents`),
  query: (body: { question: string; collection_id: string; config?: any }) => json<QueryResponse>('/query', { method: 'POST', body: JSON.stringify(body) }),
  agent: (body: { collection_id: string; task: string }) => json<any>('/agent/run', { method: 'POST', body: JSON.stringify(body) }),
  datasets: () => json<any[]>('/eval/datasets'),
  evalRuns: () => json<any[]>('/eval/runs'),
  usage: () => json<any>('/metrics/usage'),
  quality: () => json<any>('/metrics/quality'),
  latency: () => json<any>('/metrics/latency'),
};
