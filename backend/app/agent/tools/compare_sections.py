class CompareSectionsTool:
    name = "compare_sections"

    def run(self, sections: list[str]) -> dict:
        return {"sections_compared": len(sections), "note": "Local comparison adapter; replace with an LLM-based comparer in production."}
