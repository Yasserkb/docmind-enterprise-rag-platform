export function SourceCitation({ source }: { source: { document_title: string; page: number; chunk_content: string; relevance_score: number } }) {
  return <blockquote><b>{source.document_title} · page {source.page} · score {source.relevance_score}</b><br />{source.chunk_content}</blockquote>;
}
