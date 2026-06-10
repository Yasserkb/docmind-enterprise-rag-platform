import hashlib
import math


class EmbeddingService:
    """Deterministic local embedding adapter for offline demos.

    The interface mirrors a real embedding service while keeping local runs free and repeatable.
    Swap this class with OpenAI, sentence-transformers, or another provider in production.
    """

    def __init__(self, dims: int = 64):
        self.dims = dims

    def embed(self, text: str) -> list[float]:
        vector = [0.0] * self.dims
        for term in [x.lower() for x in text.split() if x.strip()]:
            digest = hashlib.sha256(term.encode()).digest()
            idx = int.from_bytes(digest[:4], "big") % self.dims
            vector[idx] += 1 if digest[4] % 2 == 0 else -1
        norm = math.sqrt(sum(x * x for x in vector)) or 1.0
        return [x / norm for x in vector]

    def embed_batch(self, texts: list[str]) -> list[list[float]]:
        return [self.embed(text) for text in texts]


def cosine(a: list[float] | None, b: list[float] | None) -> float:
    if not a or not b:
        return 0.0
    left = math.sqrt(sum(x * x for x in a)) or 1.0
    right = math.sqrt(sum(y * y for y in b)) or 1.0
    return sum(x * y for x, y in zip(a, b)) / (left * right)
