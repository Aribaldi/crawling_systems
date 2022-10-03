from common.text_extractor import TextExtractor
from common.extraction_object import ExtractionObject
import re
from readers.word_document_reader import LocalWordReader
from pathlib import Path


class DocxTextExtractor(TextExtractor):
    def __init__(self) -> None:
        super().__init__()

    def extract(self, extracted_object: ExtractionObject) -> str:
        res_text = []
        document = extracted_object.content
        for para in document.paragraphs:
            if para.style.name != "Caption":
                temp_line = para.text
                res_text.append(temp_line)
            else:
                continue
        return self._clean_text(" ".join(res_text))


if __name__ == "__main__":
    extr = DocxTextExtractor()
    reader = LocalWordReader()
    doc = reader.read(Path("data_examples/test3.doc"))
    print(extr.extract(doc))
