import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';
import { useState } from 'react';
import { api } from '../api/client';
import { DocumentUploader } from '../components/DocumentUploader';

export function Collections() {
  const qc = useQueryClient();
  const [name, setName] = useState('Knowledge Base');
  const q = useQuery({ queryKey: ['collections'], queryFn: api.collections });
  const create = useMutation({ mutationFn: api.createCollection, onSuccess: () => qc.invalidateQueries({ queryKey: ['collections'] }) });
  return <section><h1>Collections</h1><p>Collections isolate documents, chunking strategy, embedding model and retrieval indexes.</p><div className="toolbar"><input value={name} onChange={(e) => setName(e.target.value)} /><button onClick={() => create.mutate({ name, description: 'Local RAG demo collection', chunking_strategy: 'semantic' })}>Create collection</button></div><div className="grid">{q.data?.map((c) => <div className="card" key={c.id}><h3>{c.name}</h3><p>{c.description}</p><small>{c.document_count} documents · {c.chunking_strategy} · {c.embedding_model}</small></div>)}</div><DocumentUploader /></section>;
}
