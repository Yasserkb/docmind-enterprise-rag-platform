from email import message_from_bytes
from app.ingestion.parsers.base import DocumentParser, ParsedDocument

class EmlParser(DocumentParser):
    source_type = "EML"
    def parse(self, content: bytes, filename: str | None = None) -> ParsedDocument:
        msg = message_from_bytes(content)
        body = []
        if msg.is_multipart():
            for part in msg.walk():
                if part.get_content_type() == "text/plain":
                    payload = part.get_payload(decode=True)
                    if payload:
                        body.append(payload.decode(errors="ignore"))
        else:
            payload = msg.get_payload(decode=True)
            body.append(payload.decode(errors="ignore") if payload else str(msg.get_payload()))
        header = f"Subject: {msg.get('subject','')}\nFrom: {msg.get('from','')}\nTo: {msg.get('to','')}\n\n"
        text = header + "\n".join(body)
        return ParsedDocument(text=text, page_count=1, metadata={"filename": filename, "subject": msg.get('subject')})
