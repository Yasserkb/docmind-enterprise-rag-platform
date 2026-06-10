from fastapi import APIRouter

from app.evaluation.runner import EvaluationRunner
from app.generation.rag_pipeline import RagPipeline
from app.ingestion.pipeline import IngestionPipeline
from app.models import Collection, EvalDataset, EvalQuestion, EvalRun, QueryRequest, SourceType
from app.storage.store import store

router = APIRouter(prefix="/demo", tags=["demo"])

SAMPLE_POLICY = b"""
# Retail Banking Policy
Retail customers have a maximum daily transaction limit of EUR 50,000.
Late payment penalties apply after a grace period of 15 days from the due date.
High-risk customers require enhanced due diligence before account activation.
Compliance analysts must cite the source policy section when answering operational questions.
"""


@router.post("/seed")
def seed_demo() -> dict:
    collection = Collection(
        name="Demo Knowledge Base",
        description="Seeded local documents for a RAG demo",
        embedding_model="local-hash-embedding",
        chunking_strategy="structural",
    )
    store.add_collection(collection)
    document = IngestionPipeline(store).ingest_bytes(
        collection,
        "retail_banking_policy.txt",
        SourceType.TXT,
        SAMPLE_POLICY,
        {"document_title": "retail_banking_policy.txt", "type": "policy"},
    )
    query = RagPipeline(store).run(
        QueryRequest(question="What is the maximum daily transaction limit for retail customers?", collection_id=collection.id)
    )
    dataset = EvalDataset(
        name="Demo Evaluation Dataset",
        collection_id=collection.id,
        questions=[
            EvalQuestion(
                question="What is the maximum daily transaction limit for retail customers?",
                ground_truth="The maximum daily transaction limit for retail customers is EUR 50,000.",
            ),
            EvalQuestion(
                question="When do late payment penalties apply?",
                ground_truth="Late payment penalties apply after a 15 day grace period.",
            ),
        ],
    )
    store.eval_datasets[dataset.id] = dataset
    run = EvalRun(name="Demo RAG Evaluation", dataset_id=dataset.id, pipeline_config={"top_k": 5, "reranking": True, "hyde": True})
    store.eval_runs[run.id] = EvaluationRunner(store).run(run)
    return {
        "collection_id": str(collection.id),
        "document_id": str(document.id),
        "query_id": str(query.query_id),
        "evaluation_run_id": str(run.id),
        "message": "Demo data created: collection, document, query log, dataset and evaluation run.",
    }
