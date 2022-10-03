from common.document_reader import DocumentReader
from extraction_objects.docx_extraction_object import DocxExtractionObject
import os
from docx import Document
import os

class LocalWordReader(DocumentReader):        
    def read(self, file_path : str) -> DocxExtractionObject:
        file, extension = os.path.splitext(file_path)
        if extension == ".docx":
            res = DocxExtractionObject(Document(file_path))
            return res
        elif extension == ".doc":
            os.system(f"lowriter --convert-to docx {file_path} --outdir ./data_examples")
            return DocxExtractionObject(Document(f"{file}.docx"))
