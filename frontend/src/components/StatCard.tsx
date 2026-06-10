export function StatCard({ label, value }: { label: string; value: any }) { return <div className="card metric"><small>{label}</small><strong>{value}</strong></div>; }
