import os
from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    app_name: str = "DocMind"
    environment: str = os.getenv("ENVIRONMENT", "local")
    llm_provider: str = os.getenv("LLM_PROVIDER", "local")
    database_url: str = os.getenv("DATABASE_URL", "postgresql://docmind:docmind@localhost:5432/docmind")
    redis_url: str = os.getenv("REDIS_URL", "redis://localhost:6379/0")
    qdrant_url: str = os.getenv("QDRANT_URL", "http://localhost:6333")
    elasticsearch_url: str = os.getenv("ELASTICSEARCH_URL", "http://localhost:9200")


settings = Settings()
