import unittest
from os import path
import tempfile
from reportlab.pdfgen import canvas
from extractors.pdf_text_extractor import PdfTextExtractor
from extraction_objects.pdf_extraction_object import PdfExtractionObject
from readers.pdf_reader import PdfReader


class TestPdfTextExtractor(unittest.TestCase):
    def setUp(self) -> None:
        self.extractor = PdfTextExtractor()
        self.test_filepath = path.join(tempfile.gettempdir(), 'test.pdf')

        tests_dir_path = path.abspath(path.dirname(__file__))
        self.samples_dir = path.join(tests_dir_path, 'test_examples')

    def _generate_pdf(self, text: str, filename: str) -> PdfExtractionObject:
        script_path = path.abspath(path.dirname(__file__))

        c = canvas.Canvas(filename)
        c.drawImage(path.join(script_path, 'test.jpeg'), 15, 720)

        text_obj = c.beginText(15, 720)
        for line in text.splitlines():
            text_obj.textLine(line)
        c.drawText(text_obj)

        c.save()

        return PdfReader().read(filename)
    
    def _read_file(self, path: str) -> PdfExtractionObject:
        return PdfReader().read(path)

    def test_image_removal(self):
        text = ''
        eo = self._generate_pdf(text, self.test_filepath)
        self.assertEqual(self.extractor.extract(eo), text)

    def test_text_extraction(self):
        text = 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, ' \
            'sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.'
        eo = self._generate_pdf(text, self.test_filepath)
        self.assertEqual(
            self.extractor.extract(eo),
            text
        )

    def test_link_removal_from_text(self):
        text = '''
            Test
            example.com
            Test
        '''
        eo = self._generate_pdf(text, self.test_filepath)
        self.assertEqual(
            self.extractor.extract(eo),
            'Test\nTest'
        )

    def test_multiple_spaces_replacing(self):
        text = '''
                Test         Test
                Test     Test
        '''
        eo = self._generate_pdf(text, self.test_filepath)
        self.assertEqual(
            self.extractor.extract(eo),
            'Test Test\nTest Test'
        )

    def test_strings_trimming(self):
        text = '''
                            Test    
                     Test         
        '''
        eo = self._generate_pdf(text, self.test_filepath)
        self.assertEqual(
            self.extractor.extract(eo),
            'Test\nTest'
        )

    def test_no_alphabetic_chars(self):
        filepath = path.join(self.samples_dir, 'symbols.pdf')
        eo = self._read_file(filepath)
        self.assertEqual(
            self.extractor.extract(eo),
            '!"#$%&\'()*+,-./0123456789:;<=>?@[\]^_`{|}‘’‚‛“”„'
        )

    def test_latin_alphabet(self):
        filepath = path.join(self.samples_dir, 'latin.pdf')
        eo = self._read_file(filepath)
        self.assertEqual(
            self.extractor.extract(eo),
            'ABCDEFGHIJKLMNOPQRSTUVWXYZ\nabcdefghijklmnopqrstuvwxyz'
        )

    def test_cyrillic_alphabet(self):
        filepath = path.join(self.samples_dir, 'cyrillic.pdf')
        eo = self._read_file(filepath)
        self.assertEqual(
            self.extractor.extract(eo),
            'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ\nабвгдеёжзийклмнопрстуфхцчшщъыьэюя'
        )

    def test_empty_text(self):
        text = ''
        obj = self._generate_pdf(text, self.test_filepath)
        self.assertEqual(
            self.extractor.extract(obj),
            text
        )