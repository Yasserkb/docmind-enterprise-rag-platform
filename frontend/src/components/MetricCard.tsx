export function MetricCard({ label, value, hint }: { label: string; value: any; hint?: string }) {
  return <div className="card metric"><small>{label}</small><strong>{value}</strong>{hint && <span>{hint}</span>}</div>;
}
