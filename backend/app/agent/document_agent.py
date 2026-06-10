from uuid import UUID

from app.agent.tools import ExtractEntitiesTool, SearchDocumentsTool, SummarizeDocumentTool
from app.models import AgentRun, AgentStep


class DocumentAnalysisAgent:
    """Small deterministic document-analysis agent for local portfolio demos.

    The class mirrors the shape of a multi-tool agent while remaining offline-friendly.
    """

    def __init__(self, store):
        self.store = store
        self.search_tool = SearchDocumentsTool(store)
        self.summary_tool = SummarizeDocumentTool(store)
        self.entity_tool = ExtractEntitiesTool()

    def run(self, task: str, collection_id: UUID) -> AgentRun:
        search_results = self.search_tool.run(task, collection_id, top_k=5)
        summary = self.summary_tool.run(collection_id)
        entities = self.entity_tool.run(" ".join(item["preview"] for item in search_results))
        result = {
            "task": task,
            "summary": summary["summary"],
            "top_sources": search_results,
            "extracted_entities": entities,
            "recommendation": "Review the top cited chunks before making a business decision.",
        }
        run = AgentRun(
            collection_id=collection_id,
            task=task,
            steps=[
                AgentStep(name="search_documents", description="Retrieved relevant chunks", output={"results": search_results}),
                AgentStep(name="summarize_document", description="Built a short collection summary", output=summary),
                AgentStep(name="extract_entities", description="Extracted simple dates and amounts", output=entities),
            ],
            result=result,
        )
        self.store.agent_runs[run.id] = run
        return run
