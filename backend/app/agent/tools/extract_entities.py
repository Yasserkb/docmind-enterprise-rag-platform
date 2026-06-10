import re


class ExtractEntitiesTool:
    name = "extract_entities"

    def run(self, text: str) -> dict:
        amounts = re.findall(r"(?:EUR|USD|MAD|€|\$)\s?\d[\d,]*(?:\.\d+)?", text)
        dates = re.findall(r"\b\d{4}-\d{2}-\d{2}\b", text)
        return {"amounts": amounts, "dates": dates}
