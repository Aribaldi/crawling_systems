import unittest
from extractors.docx_text_extractor import DocxTextExtractor
from extraction_objects.docx_extraction_object import DocxExtractionObject
from docx import Document


class TestDocxTextExtractor(unittest.TestCase):
    def setUp(self):
        self.extractor = DocxTextExtractor()

    def _read_file(self, path: str) -> DocxExtractionObject:
        return DocxExtractionObject(Document(path))

    def test_table_removal(self):
        pass

    def test_running_lines_removal(self):
        pass

    def test_image_removal(self):
        pass

    def test_multiple_spaces_replacing(self):
        pass

    def test_multiple_breaklines_replacing(self):
        pass

    def test_formula_removal(self):
        pass

    def test_strings_trimming(self):
        pass
