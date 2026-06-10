from app.evaluation.metrics import hallucination_rate


class HallucinationDetector:
    def score(self, answer: str, contexts: list[str]) -> float:
        return hallucination_rate(answer, contexts)
