from fastapi import APIRouter

from app.storage.store import store

router = APIRouter(prefix="/metrics", tags=["metrics"])


@router.get("/usage")
def usage() -> dict:
    logs = list(store.query_logs.values())
    return {
        "queries": len(logs),
        "prompt_tokens": sum(query.prompt_tokens for query in logs),
        "completion_tokens": sum(query.completion_tokens for query in logs),
        "cost_usd": round(sum(query.cost_usd for query in logs), 6),
    }


@router.get("/quality")
def quality() -> dict:
    runs = [run for run in store.eval_runs.values() if run.status == "COMPLETED"]
    latest = runs[-1] if runs else None
    return {
        "latest_faithfulness": latest.faithfulness_score if latest else None,
        "latest_hallucination_rate": latest.hallucination_rate if latest else None,
        "latest_context_recall": latest.context_recall_score if latest else None,
    }


@router.get("/latency")
def latency() -> dict:
    values = sorted(query.latency_ms for query in store.query_logs.values())
    if not values:
        return {"p50": 0, "p95": 0, "p99": 0}
    return {
        "p50": values[min(len(values) - 1, int(len(values) * 0.50))],
        "p95": values[min(len(values) - 1, int(len(values) * 0.95))],
        "p99": values[min(len(values) - 1, int(len(values) * 0.99))],
    }
