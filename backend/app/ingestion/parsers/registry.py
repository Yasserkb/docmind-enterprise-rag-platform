from app.models import SourceType
from app.ingestion.parsers.txt_parser import TxtParser
from app.ingestion.parsers.pdf_parser import PdfParser
from app.ingestion.parsers.docx_parser import DocxParser
from app.ingestion.parsers.html_parser import HtmlParser
from app.ingestion.parsers.eml_parser import EmlParser

PARSERS = {
    SourceType.TXT: TxtParser(),
    SourceType.PDF: PdfParser(),
    SourceType.DOCX: DocxParser(),
    SourceType.HTML: HtmlParser(),
    SourceType.URL: HtmlParser(),
    SourceType.EML: EmlParser(),
    SourceType.S3: TxtParser(),
    SourceType.CONFLUENCE: TxtParser(),
}
