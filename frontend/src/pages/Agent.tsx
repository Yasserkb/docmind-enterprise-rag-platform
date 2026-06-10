import { useMutation, useQuery } from '@tanstack/react-query';
import { useState } from 'react';
import { api } from '../api/client';

export function Agent() {
  const collections = useQuery({ queryKey: ['collections'], queryFn: api.collections });
  const [task, setTask] = useState('Summarize the document and extract key limits, penalties and compliance obligations');
  const [collectionId, setCollectionId] = useState('');
  const run = useMutation({ mutationFn: api.agent });
  const selected = collectionId || collections.data?.[0]?.id || '';
  return <section><h1>Document Analysis Agent</h1><p>A deterministic local multi-tool agent that searches documents, summarizes evidence and extracts simple entities.</p><div className="toolbar"><select value={selected} onChange={(e) => setCollectionId(e.target.value)}>{collections.data?.map((c) => <option key={c.id} value={c.id}>{c.name}</option>)}</select><input value={task} onChange={(e) => setTask(e.target.value)} /><button disabled={!selected} onClick={() => run.mutate({ collection_id: selected, task })}>Run agent</button></div>{run.data && <pre className="card">{JSON.stringify(run.data, null, 2)}</pre>}</section>;
}
