import { useQuery } from '@tanstack/react-query';
import { BarChart, Bar, XAxis, YAxis, Tooltip } from 'recharts';
import { api } from '../api/client';
import { MetricCard } from '../components/MetricCard';

export function Metrics() {
  const usage = useQuery({ queryKey: ['usage'], queryFn: api.usage });
  const quality = useQuery({ queryKey: ['quality'], queryFn: api.quality });
  const latency = useQuery({ queryKey: ['latency'], queryFn: api.latency });
  const data = [{ name: 'p50', value: latency.data?.p50 || 0 }, { name: 'p95', value: latency.data?.p95 || 0 }, { name: 'p99', value: latency.data?.p99 || 0 }];
  return <section><h1>LLMOps Metrics</h1><div className="grid"><MetricCard label="Queries" value={usage.data?.queries ?? 0} /><MetricCard label="Cost USD" value={usage.data?.cost_usd ?? 0} /><MetricCard label="Faithfulness" value={quality.data?.latest_faithfulness ?? 'n/a'} /><MetricCard label="Hallucination" value={quality.data?.latest_hallucination_rate ?? 'n/a'} /></div><div className="card"><BarChart width={520} height={260} data={data}><XAxis dataKey="name" /><YAxis /><Tooltip /><Bar dataKey="value" /></BarChart></div></section>;
}
