class GenerateTimelineTool:
    name = "generate_timeline"

    def run(self, events: list[dict]) -> dict:
        return {"timeline": sorted(events, key=lambda event: event.get("date", ""))}
