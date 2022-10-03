import unittest
from os import path
import tempfile
from extractors.pdf_text_extractor import PdfTextExtractor
from extraction_objects.pdf_extraction_object import PdfExtractionObject
from reportlab.pdfgen import canvas
from readers.pdf_reader import PdfReader


class TestPdfTextExtractor(unittest.TestCase):
    def setUp(self) -> None:
        self.extractor = PdfTextExtractor()
        self.test_filepath = path.join(tempfile.gettempdir(), 'test.pdf')

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
