# Observability

The backend exposes Prometheus metrics at `/metrics`. API-level metrics are also available through `/api/v1/metrics/usage`, `/api/v1/metrics/quality` and `/api/v1/metrics/latency`.

The Docker Compose stack includes Prometheus and Grafana so the project can be extended with operational dashboards.
