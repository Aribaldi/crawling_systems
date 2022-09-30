from common.extraction_object import ExtractionObject
from PyPDF2 import PdfReader


class PdfExtractionObject(ExtractionObject):
    def __init__(self, content: PdfReader):
        super().__init__(content)
