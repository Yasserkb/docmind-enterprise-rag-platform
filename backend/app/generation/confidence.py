def confidence_from_scores(scores: list[float]) -> float:
    if not scores:
        return 0.0
    return round(min(0.99, max(0.10, sum(scores) / len(scores))), 2)


def estimate_cost(prompt_tokens: int, completion_tokens: int) -> float:
    return round(prompt_tokens * 0.00000015 + completion_tokens * 0.0000006, 6)
