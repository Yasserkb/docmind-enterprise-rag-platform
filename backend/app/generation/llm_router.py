class LocalGroundedLLM:
    """Deterministic local LLM adapter for free and repeatable demos."""

    def generate(self, question: str, context: str) -> str:
        if not context.strip():
            return "I do not have enough information in the provided context to answer this question."

        sentences: list[str] = []
        for raw in context.replace("\n", " ").split("."):
            sentence = raw.strip()
            if len(sentence) > 35 and not sentence.startswith("[DOCUMENT"):
                sentences.append(sentence)
            if len(sentences) >= 3:
                break

        if not sentences:
            return "Relevant context was found, but it is insufficient for a reliable answer. [Doc1, p.1]"
        return "Based on the retrieved documents: " + " ".join(
            f"{sentence}. [Doc{index + 1}, p.1]" for index, sentence in enumerate(sentences)
        )


def get_llm(model_name: str = "local-grounded") -> LocalGroundedLLM:
    return LocalGroundedLLM()
