# Known limitations

- The default repository and search adapters are in-memory; restart durability is not claimed.
- Local identity headers are suitable only behind a trusted developer boundary. Production requires verified JWT/OIDC claims.
- Qdrant and Elasticsearch containers are provisioned, but the deterministic local adapters remain the default execution path.
- The worker is a boundary placeholder rather than a durable distributed job state machine.
- No OCR support is claimed, and provider-backed LLM behavior requires separate credentials and evaluation.
