from datetime import datetime

from app.evaluation.metrics import (
    answer_relevancy,
    context_precision,
    context_recall,
    hallucination_rate,
    mean_reciprocal_rank,
)
from app.generation.rag_pipeline import RagPipeline
from app.models import EvalRun, QueryConfig, QueryRequest
from app.observability.metrics import FAITHFULNESS, HALLUCINATION_RATE, RETRIEVAL_MRR


class EvaluationRunner:
    def __init__(self, store):
        self.store = store
        self.pipeline = RagPipeline(store)

    def run(self, run: EvalRun) -> EvalRun:
        dataset = self.store.eval_datasets[run.dataset_id]
        records = []
        sums = {"faith": 0.0, "rel": 0.0, "prec": 0.0, "rec": 0.0, "hall": 0.0, "mrr": 0.0, "lat": 0.0, "cost": 0.0}
        run.status = "RUNNING"

        for question in dataset.questions:
            response = self.pipeline.run(
                QueryRequest(
                    collection_id=dataset.collection_id,
                    question=question.question,
                    config=QueryConfig(
                        top_k=int(run.pipeline_config.get("top_k", 5)),
                        reranking=bool(run.pipeline_config.get("reranking", True)),
                        hyde=bool(run.pipeline_config.get("hyde", True)),
                    ),
                )
            )
            contexts = [source.chunk_content for source in response.sources]
            retrieved_ids = [str(source.chunk_id) for source in response.sources]
            relevant_ids = [str(chunk_id) for chunk_id in question.relevant_chunk_ids]
            hallucination = hallucination_rate(response.answer, contexts)
            record = {
                "question": question.question,
                "answer": response.answer,
                "faithfulness": 1 - hallucination,
                "answer_relevancy": answer_relevancy(question.question, response.answer),
                "context_precision": context_precision(question.question, contexts),
                "context_recall": context_recall(relevant_ids, retrieved_ids),
                "hallucination_rate": hallucination,
                "mrr": mean_reciprocal_rank(relevant_ids, retrieved_ids),
                "latency_ms": response.metadata.latency_ms,
                "cost_usd": response.metadata.cost_usd,
            }
            records.append(record)
            sums["faith"] += record["faithfulness"]
            sums["rel"] += record["answer_relevancy"]
            sums["prec"] += record["context_precision"]
            sums["rec"] += record["context_recall"]
            sums["hall"] += hallucination
            sums["mrr"] += record["mrr"]
            sums["lat"] += record["latency_ms"]
            sums["cost"] += record["cost_usd"]

        n = max(1, len(records))
        run.status = "COMPLETED"
        run.faithfulness_score = round(sums["faith"] / n, 4)
        run.answer_relevancy_score = round(sums["rel"] / n, 4)
        run.context_precision_score = round(sums["prec"] / n, 4)
        run.context_recall_score = round(sums["rec"] / n, 4)
        run.hallucination_rate = round(sums["hall"] / n, 4)
        run.avg_latency_ms = int(sums["lat"] / n)
        run.avg_cost_usd = round(sums["cost"] / n, 6)
        run.total_questions = len(records)
        run.results = {"records": records}
        run.completed_at = datetime.utcnow()

        FAITHFULNESS.labels(collection=str(dataset.collection_id)).set(run.faithfulness_score)
        HALLUCINATION_RATE.labels(collection=str(dataset.collection_id)).set(run.hallucination_rate)
        RETRIEVAL_MRR.labels(collection=str(dataset.collection_id)).set(round(sums["mrr"] / n, 4))
        return run
