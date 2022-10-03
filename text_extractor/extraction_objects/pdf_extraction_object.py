from common.extraction_object import ExtractionObject
from pdfx import PDFx


class PdfExtractionObject(ExtractionObject):
    def __init__(self, content: PDFx):
        super().__init__(content)
