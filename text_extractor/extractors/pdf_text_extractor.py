from common.text_extractor import TextExtractor
from extraction_objects.pdf_extraction_object import PdfExtractionObject


class PdfTextExtractor(TextExtractor):
    def __init__(self):
        TextExtractor.__init__(self)

    def extract(self, extraction_object: PdfExtractionObject) -> str:
        text = extraction_object.content.get_text()
        extraction_object.content.stream.close()
        text = self.clean_text(text)
        return text
