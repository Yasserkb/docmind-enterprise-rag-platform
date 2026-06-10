import { useMutation, useQueryClient } from '@tanstack/react-query';
import { api } from '../api/client';

export function Home() {
  const qc = useQueryClient();
  const seed = useMutation({ mutationFn: api.seedDemo, onSuccess: () => { qc.invalidateQueries(); } });
  return <section><div className="hero"><h1>DocMind</h1><p>RAG-powered document intelligence platform with ingestion, chunking, hybrid retrieval, reranking, grounded answers, citations, evaluation and LLMOps metrics.</p><button onClick={() => seed.mutate()}>{seed.isPending ? 'Seeding...' : 'Seed local demo data'}</button>{seed.data && <p className="success">{seed.data.message}</p>}</div><div className="grid"><div className="card"><h3>RAG Pipeline</h3><p>Query expansion, HyDE-style query representation, semantic retrieval, BM25-style retrieval, RRF fusion, reranking and grounded response generation.</p></div><div className="card"><h3>Evaluation</h3><p>Faithfulness, answer relevance, context precision, context recall, hallucination rate, MRR, latency and cost estimates.</p></div><div className="card"><h3>Operational Layer</h3><p>FastAPI core, Spring gateway, React UI, Prometheus metrics, Grafana dashboard config, Docker Compose and CI structure.</p></div></div></section>;
}
