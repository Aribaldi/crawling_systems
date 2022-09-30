from common.extraction_object import ExtractionObject
from docx import Document


class DocxExtractionObject(ExtractionObject):
    def __init__(self, content: Document):
        super().__init__(content)