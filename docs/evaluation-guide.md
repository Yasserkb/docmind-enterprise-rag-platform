# Evaluation Guide

DocMind evaluates RAG quality with deterministic local metrics that model production RAG evaluation workflows: faithfulness, answer relevance, context precision, context recall, hallucination rate, MRR, latency and cost estimate.

Create a dataset through `/api/v1/eval/datasets`, then launch a run through `/api/v1/eval/runs`.
