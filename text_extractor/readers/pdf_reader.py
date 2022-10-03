from pdfx import PDFx
from common.document_reader import DocumentReader
from extraction_objects.pdf_extraction_object import PdfExtractionObject


class PdfReader(DocumentReader):
    def read(self, path: str) -> PdfExtractionObject:
        return PdfExtractionObject(PDFx(path))
