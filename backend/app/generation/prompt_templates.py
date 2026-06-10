SYSTEM_PROMPT = """You are DocMind, a precise document analysis assistant.
Answer questions using only the provided context. If the context does not contain
sufficient information, say so explicitly. Always cite source documents when making
factual claims.
"""


def build_context_block(blocks: list[str]) -> str:
    return "\n\n".join(blocks)


def build_rag_prompt(question: str, context: str) -> str:
    return f"{SYSTEM_PROMPT}\n\nContext:\n{context}\n\nQuestion: {question}\n\nAnswer:"
