from common.text_extractor import TextExtractor
from docx import Document
from common.extraction_object import ExtractionObject
import re

class DocxTextExtractor(TextExtractor):
    def __init__(self) -> None:
        super().__init__()

    def extract(self, extracted_object: ExtractionObject) -> str:
        res_text = []
        document = extracted_object.content
        for para in document.paragraphs:
            if para.style.name != "Caption":
                temp_line = para.text
                temp_line = re.sub(r'[^\S\r\n]+', ' ', temp_line)
                temp_line = temp_line.strip()
                res_text.append(temp_line)
            else:
                continue
        return " ".join(res_text)


if __name__ == "__main__":
    doc = ExtractionObject(Document("./test.docx"))
    extr = DocxTextExtractor()
    print(extr.extract(doc))

