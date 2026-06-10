from prometheus_client import Counter, Histogram, Gauge, generate_latest, CONTENT_TYPE_LATEST
from starlette.responses import Response
QUERIES_TOTAL=Counter("docmind_queries_total","Total DocMind queries",["model","collection","status"])
QUERY_LATENCY=Histogram("docmind_query_latency_seconds","DocMind query latency",["model","retrieval_strategy"])
TOKENS_TOTAL=Counter("docmind_tokens_total","DocMind tokens",["model","type"])
COST_TOTAL=Counter("docmind_cost_usd_total","DocMind estimated cost",["model"])
FAITHFULNESS=Gauge("docmind_faithfulness_score","Latest faithfulness score",["collection"])
HALLUCINATION_RATE=Gauge("docmind_hallucination_rate","Latest hallucination rate",["collection"])
RETRIEVAL_MRR=Gauge("docmind_retrieval_mrr","Latest retrieval MRR",["collection"])
DOCUMENTS_INDEXED=Counter("docmind_documents_indexed_total","Documents indexed",["collection","source_type"])
def metrics_response(): return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)
