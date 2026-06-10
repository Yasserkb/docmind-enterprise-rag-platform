import time

from app.generation.citation_extractor import build_source_citations
from app.generation.confidence import confidence_from_scores, estimate_cost
from app.generation.llm_router import get_llm
from app.generation.prompt_templates import build_context_block
from app.models import QueryLog, QueryMetadata, QueryRequest, QueryResponse
from app.observability.metrics import COST_TOTAL, QUERIES_TOTAL, QUERY_LATENCY, TOKENS_TOTAL
from app.retrieval.hybrid_search import HybridSearchEngine
from app.storage.store import Store


class RagPipeline:
    def __init__(self, store: Store):
        self.store = store
        self.search = HybridSearchEngine()

    def run(self, req: QueryRequest) -> QueryResponse:
        start = time.perf_counter()
        chunks = self.store.collection_chunks(req.collection_id)
        retrieved = self.search.search(
            req.question,
            req.collection_id,
            chunks,
            req.config.top_k,
            req.config.hyde,
            req.config.reranking,
        )

        context_blocks = [
            f"[DOCUMENT {index + 1} — {chunk.metadata.get('document_title', 'Uploaded document')}, Page {chunk.start_page}]\n{chunk.content}"
            for index, (chunk, _score) in enumerate(retrieved)
        ]
        context = build_context_block(context_blocks)
        answer = get_llm(req.config.model).generate(req.question, context)
        sources = build_source_citations(retrieved)

        latency_ms = int((time.perf_counter() - start) * 1000)
        prompt_tokens = len((context + req.question).split())
        completion_tokens = len(answer.split())
        cost_usd = estimate_cost(prompt_tokens, completion_tokens)
        confidence_score = confidence_from_scores([float(score) for _chunk, score in retrieved])
        retrieval_strategy = "hybrid+hyde+rrf+rerank" if req.config.reranking else "hybrid+hyde+rrf"

        response = QueryResponse(
            answer=answer,
            sources=sources,
            confidence_score=confidence_score,
            metadata=QueryMetadata(
                latency_ms=latency_ms,
                model=req.config.model,
                prompt_tokens=prompt_tokens,
                completion_tokens=completion_tokens,
                cost_usd=cost_usd,
                retrieval_strategy=retrieval_strategy,
                chunks_retrieved=len(retrieved),
            ),
        )
        self.store.query_logs[response.query_id] = QueryLog(
            id=response.query_id,
            collection_id=req.collection_id,
            question=req.question,
            answer=answer,
            retrieved_chunk_ids=[chunk.id for chunk, _score in retrieved],
            rerank_scores={str(chunk.id): float(score) for chunk, score in retrieved},
            llm_model=req.config.model,
            confidence_score=confidence_score,
            latency_ms=latency_ms,
            prompt_tokens=prompt_tokens,
            completion_tokens=completion_tokens,
            cost_usd=cost_usd,
        )

        QUERIES_TOTAL.labels(model=req.config.model, collection=str(req.collection_id), status="ok" if retrieved else "no_context").inc()
        QUERY_LATENCY.labels(model=req.config.model, retrieval_strategy=retrieval_strategy).observe(latency_ms / 1000)
        TOKENS_TOTAL.labels(model=req.config.model, type="prompt").inc(prompt_tokens)
        TOKENS_TOTAL.labels(model=req.config.model, type="completion").inc(completion_tokens)
        COST_TOTAL.labels(model=req.config.model).inc(cost_usd)
        return response
