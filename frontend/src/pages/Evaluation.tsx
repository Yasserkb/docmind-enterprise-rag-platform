import { useQuery } from '@tanstack/react-query';
import { api } from '../api/client';
import { EvaluationTable } from '../components/EvaluationTable';

export function Evaluation() {
  const runs = useQuery({ queryKey: ['evalRuns'], queryFn: api.evalRuns });
  return <section><h1>Evaluation Dashboard</h1><p>RAG quality should be measured. This page displays faithfulness, answer relevance, context precision, context recall, hallucination rate and latency.</p><EvaluationTable runs={runs.data} /></section>;
}
