import { NavLink, Outlet } from 'react-router-dom';

const links = [
  ['/', 'Home'],
  ['/collections', 'Collections'],
  ['/chat', 'Chat'],
  ['/agent', 'Agent'],
  ['/evaluation', 'Evaluation'],
  ['/metrics', 'LLMOps'],
  ['/settings', 'Settings'],
];

export function Layout() {
  return <div className="app"><aside><h2>DocMind</h2><p>RAG Document Intelligence</p>{links.map(([to, label]) => <NavLink key={to} to={to}>{label}</NavLink>)}</aside><main><Outlet /></main></div>;
}
