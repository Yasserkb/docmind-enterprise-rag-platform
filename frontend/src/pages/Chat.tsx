import { useMutation, useQuery } from '@tanstack/react-query';
import { useState } from 'react';
import { api } from '../api/client';
import { ChatMessage } from '../components/ChatMessage';
import { SourceCitation } from '../components/SourceCitation';

export function Chat() {
  const [collectionId, setCollectionId] = useState('');
  const [question, setQuestion] = useState('What is the maximum daily transaction limit for retail customers?');
  const collections = useQuery({ queryKey: ['collections'], queryFn: api.collections });
  const query = useMutation({ mutationFn: api.query });
  const selected = collectionId || collections.data?.[0]?.id || '';
  return <section><h1>Chat Q&A</h1><p>Ask a question and inspect the retrieved sources behind the generated answer.</p><div className="toolbar"><select value={selected} onChange={(e) => setCollectionId(e.target.value)}>{collections.data?.map((c) => <option key={c.id} value={c.id}>{c.name}</option>)}</select><input value={question} onChange={(e) => setQuestion(e.target.value)} /><button disabled={!selected} onClick={() => query.mutate({ collection_id: selected, question, config: { top_k: 5, reranking: true, hyde: true } })}>Ask</button></div>{query.data && <div className="card"><h3>Answer</h3><ChatMessage answer={query.data.answer} /><p>Confidence: {(query.data.confidence_score * 100).toFixed(0)}% · {query.data.metadata.retrieval_strategy} · {query.data.metadata.latency_ms} ms · ${query.data.metadata.cost_usd}</p><h4>Sources</h4>{query.data.sources.map((s, i) => <SourceCitation key={i} source={s} />)}</div>}</section>;
}
