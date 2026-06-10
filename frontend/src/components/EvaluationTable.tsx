export function EvaluationTable({ runs }: { runs?: any[] }) {
  return <table><thead><tr><th>Name</th><th>Status</th><th>Faithfulness</th><th>Hallucination</th><th>Latency</th></tr></thead><tbody>{runs?.map((run) => <tr key={run.id}><td>{run.name}</td><td>{run.status}</td><td>{run.faithfulness_score ?? 'n/a'}</td><td>{run.hallucination_rate ?? 'n/a'}</td><td>{run.avg_latency_ms ?? 0} ms</td></tr>)}</tbody></table>;
}
