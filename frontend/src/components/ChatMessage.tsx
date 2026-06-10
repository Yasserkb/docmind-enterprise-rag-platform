import ReactMarkdown from 'react-markdown';

export function ChatMessage({ answer }: { answer: string }) {
  return <div className="answer"><ReactMarkdown>{answer}</ReactMarkdown></div>;
}
