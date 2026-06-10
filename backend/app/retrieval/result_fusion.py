from app.models import Chunk


def reciprocal_rank_fusion(result_sets: list[list[tuple[Chunk, float]]], k: int = 60) -> tuple[list[Chunk], dict[str, float]]:
    scores: dict[str, float] = {}
    chunks_by_id: dict[str, Chunk] = {}
    for results in result_sets:
        for rank, (chunk, _score) in enumerate(results, start=1):
            chunk_id = str(chunk.id)
            chunks_by_id[chunk_id] = chunk
            scores[chunk_id] = scores.get(chunk_id, 0.0) + 1 / (k + rank)
    ordered_ids = sorted(scores, key=scores.get, reverse=True)
    return [chunks_by_id[chunk_id] for chunk_id in ordered_ids], scores
