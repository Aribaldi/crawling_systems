from os import path
import unittest
from extractors.docx_text_extractor import DocxTextExtractor
from extraction_objects.docx_extraction_object import DocxExtractionObject
from docx import Document


class TestDocxTextExtractor(unittest.TestCase):
    def setUp(self):
        self.extractor = DocxTextExtractor()
        tests_dir_path = path.abspath(path.dirname(__file__))
        self.samples_dir = path.join(tests_dir_path, 'test_examples')

    def _read_file(self, path: str) -> DocxExtractionObject:
        return DocxExtractionObject(Document(path))

    def test_table_removal(self):
        filepath = path.join(self.samples_dir, 'table_text.docx')
        eo = self._read_file(filepath)
        self.assertEqual(
            self.extractor.extract(eo),
            'А это тестовый текст.'
        )

    def test_running_lines_removal(self):
        filepath = path.join(self.samples_dir, 'colontitle_text.docx')
        eo = self._read_file(filepath)
        self.assertEqual(
            self.extractor.extract(eo),
            'Это текст в тестовом документе с колонтитулами.'
        )

    def test_image_removal(self):
        filepath = path.join(self.samples_dir, 'picture_text.docx')
        eo = self._read_file(filepath)
        self.assertEqual(
            self.extractor.extract(eo),
            'Это текст в документе с пдописанным изображением'
        )

    def test_multiple_spaces_replacing(self):
        filepath = path.join(self.samples_dir, 'multi_spaces.docx')
        eo = self._read_file(filepath)
        self.assertEqual(
            self.extractor.extract(eo),
            'Это первое предлжение текста с несколькими пробелами в некоторых местах '
            'например в этом и ещё вот в этом.'
        )

    def test_multiple_breaklines_replacing(self):
        filepath = path.join(
            self.samples_dir, 'multiline_multi_line_breaks.docx'
        )
        eo = self._read_file(filepath)
        self.assertEqual(
            self.extractor.extract(eo),
            'And more text. And more text. And more text. And more text. And more\n'
            'text. And more text. Boring, zzzzz. And more text. And more text. And\n'
            'more text. And more text. And more text. And more text. And more text.'
        )

    def test_formula_removal(self):
        filepath = path.join(self.samples_dir, 'formula_text.docx')
        eo = self._read_file(filepath)
        self.assertEqual(
            self.extractor.extract(eo),
            'Это текст в файле с формулой'
        )

    def test_strings_trimming(self):
        filepath = path.join(self.samples_dir, 'tabulation.docx')
        eo = self._read_file(filepath)
        self.assertEqual(
            self.extractor.extract(eo),
            'And more text. And more text. And more text. And more text. '
            'And more text. And more text. Boring, zzzzz. And more text. '
            'And more text. And more text. And more text. And more text. '
            'And more text. And more text. And more text. And more text. '
            'And more text. And more text. And more text. And more text. '
            'Boring, zzzzz. And more text. And more text. And more text. '
            'And more text. And more text. And more text. And more text'
        )
