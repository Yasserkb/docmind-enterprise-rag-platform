def terms(text: str) -> set[str]:
    return {term.strip(".,;:!?()[]{}\"'").lower() for term in text.split() if len(term.strip()) > 3}


def hallucination_rate(answer: str, contexts: list[str]) -> float:
    context_terms = terms(" ".join(contexts))
    sentences = [sentence for sentence in answer.split(".") if len(sentence.strip()) > 20]
    if not sentences:
        return 0.0
    unsupported = 0
    for sentence in sentences:
        sentence_terms = terms(sentence)
        if sentence_terms and len(sentence_terms & context_terms) / max(1, len(sentence_terms)) < 0.15:
            unsupported += 1
    return round(unsupported / len(sentences), 4)


def answer_relevancy(question: str, answer: str) -> float:
    return round(len(terms(question) & terms(answer)) / max(1, len(terms(question))), 4)


def context_precision(question: str, contexts: list[str]) -> float:
    if not contexts:
        return 0.0
    return round(sum(1 for context in contexts if terms(question) & terms(context)) / len(contexts), 4)


def context_recall(relevant_ids: list[str], retrieved_ids: list[str]) -> float:
    if not relevant_ids and retrieved_ids:
        return 1.0
    if not relevant_ids:
        return 0.0
    return round(len(set(relevant_ids) & set(retrieved_ids)) / len(set(relevant_ids)), 4)


def mean_reciprocal_rank(relevant_ids: list[str], retrieved_ids: list[str]) -> float:
    relevant = set(relevant_ids)
    for index, chunk_id in enumerate(retrieved_ids, start=1):
        if chunk_id in relevant:
            return round(1 / index, 4)
    return 0.0
