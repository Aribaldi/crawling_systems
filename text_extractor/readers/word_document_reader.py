from common.document_reader import DocumentReader
from extraction_objects.docx_extraction_object import DocxExtractionObject
import os
from docx import Document
from pathlib import Path

class LocalWordReader(DocumentReader):        
    def read(self, file_path : Path) -> DocxExtractionObject:
        if file_path.suffix == ".docx":
            res = DocxExtractionObject(Document(str(file_path)))
            return res
        elif file_path.suffix == ".doc":
            os.system(f"lowriter --convert-to docx ./{file_path}")
            return DocxExtractionObject(Document(f"{file_path.stem}.docx"))
