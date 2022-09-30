from common.text_extractor import TextExtractor
from extraction_objects.pdf_extraction_object import PdfExtractionObject


class PdfTextExtractor(TextExtractor):
    def extract(self, extraction_object: PdfExtractionObject) -> str:
        return '\n'.join([page.extract_text() for page in extraction_object.content.pages])
