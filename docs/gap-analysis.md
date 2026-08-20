# Gap analysis

| Requirement | Current state | Action |
|---|---|---|
| Hybrid retrieval | Deterministic semantic/keyword adapters, RRF and reranking exist | Complete real Qdrant/Elasticsearch indexing adapters and integration tests |
| Authorization before retrieval | Workspace and optional user ACL filters are applied to stored chunks | Replace trusted headers with verified gateway JWT claims |
| Cache isolation | Redis is deployed but query caching is not enabled | Include workspace, user/ACL fingerprint and retrieval version in any future cache key |
| Durable ingestion | Parser/chunker pipeline and worker boundary exist | Persist jobs/state transitions and implement bounded retry/cancellation |
| Grounded answers | Context-only local generator, citations and abstention behavior exist | Add adversarial prompt-injection regression fixtures |
| Evaluation | Deterministic evaluation modules and tests exist | Commit a labeled corpus and CI quality threshold report |
| Storage | PostgreSQL schema and external services exist | Switch the default production profile from the in-memory repository |
| Health | Live and ready endpoints exist | Add bounded dependency checks for production adapters |
| Observability | Prometheus metrics and Grafana dashboard exist | Add traces and per-stage latency metrics |
| Deployment | Compose is available | Add Kubernetes resources, NetworkPolicies and secret references |
