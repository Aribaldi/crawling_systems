from PyPDF2 import PdfReader
from common.document_reader import DocumentReader
from extraction_objects.pdf_extraction_object import PdfExtractionObject


class PdfDocumentReader(DocumentReader):
    def read(self, path: str) -> PdfExtractionObject:
        return PdfExtractionObject(PdfReader(path))
