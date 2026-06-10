from app.evaluation.metrics import answer_relevancy, hallucination_rate


def test_evaluation_metrics_are_bounded():
    assert 0 <= answer_relevancy("transaction limit", "transaction limit is EUR 50000") <= 1
    assert 0 <= hallucination_rate("The limit is EUR 50000.", ["The limit is EUR 50000."]) <= 1
