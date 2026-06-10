def compare_runs(run_a, run_b) -> dict:
    return {
        "faithfulness_delta": (run_a.faithfulness_score or 0) - (run_b.faithfulness_score or 0),
        "hallucination_delta": (run_a.hallucination_rate or 0) - (run_b.hallucination_rate or 0),
        "latency_delta_ms": (run_a.avg_latency_ms or 0) - (run_b.avg_latency_ms or 0),
    }
