# DocMind — RAG-Powered Document Intelligence Platform

![Python](https://img.shields.io/badge/Python-3.12-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-Backend-009688)
![React](https://img.shields.io/badge/React-Frontend-61DAFB)
![TypeScript](https://img.shields.io/badge/TypeScript-UI-blue)
![Spring Boot](https://img.shields.io/badge/Spring%20Boot-Gateway-6DB33F)
![Docker](https://img.shields.io/badge/Docker-Compose-2496ED)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-336791)
![Redis](https://img.shields.io/badge/Redis-Cache%20%26%20Queue-DC382D)
![Qdrant](https://img.shields.io/badge/Qdrant-Vector%20DB-orange)
![Elasticsearch](https://img.shields.io/badge/Elasticsearch-BM25%20Search-005571)
![RAG](https://img.shields.io/badge/RAG-Hybrid%20Retrieval-purple)
![LLMOps](https://img.shields.io/badge/LLMOps-Evaluation%20%26%20Metrics-black)
![Prometheus](https://img.shields.io/badge/Prometheus-Monitoring-E6522C)
![Grafana](https://img.shields.io/badge/Grafana-Dashboards-F46800)

---

## Overview

**DocMind** is a production-style document intelligence platform powered by **Retrieval-Augmented Generation**.

The project demonstrates how a serious AI document system can be designed, structured, tested, monitored and prepared for production. It ingests documents, chunks them, retrieves relevant context using hybrid search, reranks the candidates, generates grounded answers with citations and evaluates RAG quality through measurable metrics.

This is not a simple chatbot wrapper. It is structured as a full software engineering project with a FastAPI AI core, React UI, Java/Spring gateway, Docker Compose infrastructure, tests, Prometheus metrics and clear production extension points.

```text
Document ingestion
→ text extraction
→ cleaning and normalization
→ chunking strategy selection
→ local embedding generation
→ semantic + keyword retrieval
→ Reciprocal Rank Fusion
→ reranking
→ context assembly
→ grounded answer generation
→ source citation
→ evaluation
→ metrics and observability
```

The default runtime uses deterministic local adapters, so the project can run without external AI keys. Production adapters can be added behind the existing boundaries.

---

## What DocMind does

DocMind helps users ask questions over documents while keeping answers grounded in retrieved evidence.

It combines:

- document ingestion and parser adapters;
- multiple chunking strategies;
- semantic search boundary prepared for Qdrant;
- BM25-style keyword search boundary prepared for Elasticsearch;
- Reciprocal Rank Fusion;
- reranking adapter prepared for a cross-encoder model;
- grounded answer generation;
- source citations;
- RAG quality evaluation;
- hallucination scoring;
- LLMOps-style usage, cost and latency metrics.

---

## High-level architecture

```text
┌─────────────────────────────────────────────────────────────┐
│                         React UI                            │
│       Collections · Documents · Chat · Evaluation · Metrics │
└─────────────────────────────┬───────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                    Spring Boot Gateway                      │
│           Routing · Rate-limit-ready · API boundary         │
└─────────────────────────────┬───────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                         FastAPI Core                        │
│                                                             │
│  Ingestion → Retrieval → Generation → Evaluation → Metrics  │
│                                                             │
│  Parsers · Chunkers · Embeddings · Hybrid Search · Rerank   │
│  Citations · Confidence · Hallucination Scoring · LLMOps    │
└─────────────────────────────┬───────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                      Storage and Infra                      │
│                                                             │
│ PostgreSQL · Redis · Qdrant · Elasticsearch · Prometheus    │
│ Grafana · Flower                                            │
└─────────────────────────────────────────────────────────────┘
```

---

## Technology stack

| Layer | Technology |
|---|---|
| Backend API | FastAPI |
| AI core language | Python 3.12 |
| Frontend | React, TypeScript, Vite |
| Gateway | Java 17, Spring Boot, Spring Cloud Gateway |
| Metadata database | PostgreSQL 16 |
| Cache and queue broker | Redis 7 |
| Vector search boundary | Qdrant |
| Keyword search boundary | Elasticsearch |
| Background worker | Local worker placeholder, Celery-ready boundary |
| Metrics | Prometheus |
| Dashboards | Grafana |
| Containerization | Docker, Docker Compose |
| Testing | Pytest |
| CI/CD | GitHub Actions |

---

## Local run with Docker Compose

```bash
docker compose up --build
```

On Windows PowerShell:

```powershell
docker compose up --build
```

Open:

| Service | URL |
|---|---|
| React UI | http://localhost:3000 |
| FastAPI Swagger | http://localhost:8000/docs |
| Spring Boot Gateway | http://localhost:8080/docmind/docs |
| Prometheus | http://localhost:9090 |
| Grafana | http://localhost:3001 |
| Flower | http://localhost:5555 |
| Qdrant | http://localhost:6333 |
| Elasticsearch | http://localhost:9200 |

Stop everything:

```bash
docker compose down
```

Clean reset:

```bash
docker compose down -v
```

Use `down -v` only when you want to delete local volumes.

---

## Demo flow

After startup, the UI can be empty because no documents exist yet.

Fastest demo:

1. Open `http://localhost:3000`.
2. Click **Seed local demo data**.
3. Go to **Collections** to see the created collection.
4. Go to **Chat** and ask a question.
5. Go to **Evaluation** to inspect RAG quality.
6. Go to **LLMOps** to inspect query, cost and latency metrics.

The seed endpoint is also available at:

```text
POST /api/v1/demo/seed
```

---

## Lightweight backend-only run

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

Windows PowerShell:

```powershell
cd backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

Open:

```text
http://localhost:8000/docs
```

---

## Main API flows

### Create a collection

```bash
curl -X POST http://localhost:8000/api/v1/collections \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Knowledge Base",
    "description": "Demo document collection",
    "embedding_model": "local-hash-embedding",
    "chunking_strategy": "structural"
  }'
```

### Upload a document

```text
POST /api/v1/collections/{collection_id}/documents
```

### Ask a RAG question

```text
POST /api/v1/query
```

### Create and run an evaluation

```text
POST /api/v1/eval/datasets
POST /api/v1/eval/runs
```

### View metrics

```text
GET /api/v1/metrics/usage
GET /api/v1/metrics/quality
GET /api/v1/metrics/latency
GET /metrics
```

---

## Full project structure

```text
docmind-enterprise-rag-platform/
├── .github/
│   └── workflows/
│       └── ci.yml
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   ├── api/
│   │   │   ├── __init__.py
│   │   │   ├── agent.py
│   │   │   ├── collections.py
│   │   │   ├── demo.py
│   │   │   ├── documents.py
│   │   │   ├── evaluation.py
│   │   │   ├── metrics.py
│   │   │   ├── query.py
│   │   │   └── schemas.py
│   │   ├── core/
│   │   │   ├── config.py
│   │   │   ├── dependencies.py
│   │   │   └── security.py
│   │   ├── models/
│   │   │   ├── __init__.py
│   │   │   ├── agent.py
│   │   │   ├── chunk.py
│   │   │   ├── collection.py
│   │   │   ├── common.py
│   │   │   ├── document.py
│   │   │   ├── evaluation.py
│   │   │   └── query.py
│   │   ├── ingestion/
│   │   │   ├── pipeline.py
│   │   │   ├── embeddings.py
│   │   │   ├── chunking/
│   │   │   │   ├── base.py
│   │   │   │   ├── fixed_chunker.py
│   │   │   │   ├── recursive_chunker.py
│   │   │   │   ├── semantic_chunker.py
│   │   │   │   ├── strategy_selector.py
│   │   │   │   └── structural_chunker.py
│   │   │   └── parsers/
│   │   │       ├── base.py
│   │   │       ├── confluence_connector.py
│   │   │       ├── docx_parser.py
│   │   │       ├── eml_parser.py
│   │   │       ├── html_parser.py
│   │   │       ├── pdf_parser.py
│   │   │       ├── registry.py
│   │   │       └── txt_parser.py
│   │   ├── retrieval/
│   │   │   ├── elasticsearch_client.py
│   │   │   ├── hybrid_search.py
│   │   │   ├── qdrant_client.py
│   │   │   ├── reranker.py
│   │   │   ├── result_fusion.py
│   │   │   └── search.py
│   │   ├── generation/
│   │   │   ├── citation_extractor.py
│   │   │   ├── confidence.py
│   │   │   ├── llm_router.py
│   │   │   ├── prompt_templates.py
│   │   │   └── rag_pipeline.py
│   │   ├── evaluation/
│   │   │   ├── comparison.py
│   │   │   ├── dataset_loader.py
│   │   │   ├── hallucination_detector.py
│   │   │   ├── metrics.py
│   │   │   └── runner.py
│   │   ├── agent/
│   │   │   ├── document_agent.py
│   │   │   └── tools/
│   │   │       ├── compare_sections.py
│   │   │       ├── extract_entities.py
│   │   │       ├── generate_timeline.py
│   │   │       ├── search_documents.py
│   │   │       └── summarize_document.py
│   │   ├── observability/
│   │   │   └── metrics.py
│   │   └── storage/
│   │       ├── in_memory_store.py
│   │       ├── postgres_store.py
│   │       ├── repository.py
│   │       └── store.py
│   ├── tests/
│   │   ├── integration/
│   │   │   └── test_api_flow.py
│   │   └── unit/
│   │       ├── test_chunking.py
│   │       ├── test_evaluation.py
│   │       ├── test_generation.py
│   │       └── test_retrieval.py
│   ├── Dockerfile
│   ├── requirements.txt
│   └── worker.py
├── frontend/
│   ├── src/
│   │   ├── api/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── store/
│   │   └── styles/
│   ├── Dockerfile
│   ├── index.html
│   ├── package.json
│   ├── tsconfig.json
│   └── vite.config.ts
├── gateway/
│   ├── src/main/java/com/docmind/gateway/
│   ├── src/main/resources/application.yml
│   ├── Dockerfile
│   └── pom.xml
├── infra/
│   ├── elasticsearch/
│   ├── grafana/
│   ├── postgres/
│   └── prometheus/
├── samples/
├── docs/
├── docker-compose.yml
├── Makefile
├── .env
├── .gitignore
└── README.md
```

---

## Design principles

### Clean boundaries

The project separates ingestion, retrieval, generation, evaluation, API, frontend, gateway and infrastructure concerns.

### Replaceable adapters

The local adapters can be replaced with production implementations without changing the business flow:

- embedding adapter;
- LLM adapter;
- vector search adapter;
- keyword search adapter;
- reranker adapter;
- persistence adapter.

### Measurable RAG quality

The system is designed around quality metrics instead of intuition. RAG changes should be evaluated through faithfulness, context recall, context precision, hallucination rate, latency and cost.

### Grounded generation

Answers should be based on retrieved context. When context is insufficient, the system should say so instead of inventing facts.

---

## Tests

```bash
make test-python
```

Or directly:

```bash
cd backend
python -m pytest
```

---

## Production upgrade path

Possible production upgrades:

- real embedding provider;
- real LLM provider;
- persistent PostgreSQL repositories;
- real Qdrant vector indexing;
- real Elasticsearch BM25 indexing;
- cross-encoder reranker model;
- object storage for uploaded documents;
- JWT authentication and authorization;
- streaming responses in the UI;
- distributed Celery workers;
- Kubernetes manifests;
- Terraform infrastructure;
- CI quality gates based on evaluation metrics.

---

## Summary

DocMind is a RAG-powered document intelligence platform built as a complete software engineering project. It demonstrates document ingestion, chunking, hybrid retrieval, reranking, grounded answer generation, source citation, evaluation, hallucination detection, LLMOps metrics, Docker-based local deployment, a Java gateway, a React UI and clean modular architecture.
