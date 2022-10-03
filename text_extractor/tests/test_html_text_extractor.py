import unittest

from bs4 import BeautifulSoup
from extractors.html_text_extractor import HtmlTextExtractor
from extraction_objects.html_extraction_object import HtmlExtractionObject


class TestHtmlTextExtractor(unittest.TestCase):
    def setUp(self):
        self.extractor = HtmlTextExtractor()

    def _make_object(self, markup: str) -> HtmlExtractionObject:
        return HtmlExtractionObject(BeautifulSoup(markup, features='html.parser'))

    def test_only_body_text_extraction(self):
        markup = '''
            <!DOCTYPE html>
            <html>
                <head>
                    <meta charset="utf-8" />
                    <title>Test HTML Document</title>
                </head>
                <body>
                    <p>
                        Test paragraph
                    </p>
                </body>
            </html>
        '''
        obj = self._make_object(markup)
        self.assertEqual(self.extractor.extract(obj), 'Test paragraph')

    def test_header_removal(self):
        markup = '''
            <body>
                <header>
                    Test header
                </header>
                <p>
                    Some test text
                </p>
            </body>
        '''
        obj = self._make_object(markup)

        self.assertEqual(
            self.extractor.extract(obj),
            'Some test text'
        )

    def test_footer_removal(self):
        markup = '''
            <body>
                <p>
                    Some test text
                </p>
                <footer>
                    Test footer
                </footer>
            </body>
        '''
        obj = self._make_object(markup)
        self.assertEqual(
            self.extractor.extract(obj),
            'Some test text'
        )

    def test_code_removal(self):
        markup = '''
            <body>
                <code>
                    main :: IO ()
                    main = putStrLn "Hello, World!"
                </code>
                result
            </body>
        '''
        obj = self._make_object(markup)
        self.assertEqual(self.extractor.extract(obj), 'result')

    def test_table_removal(self):
        markup = '''
        <body>
            <table>
                cell goes brrrrrr
            </table>
            result
        </body>
        '''
        obj = self._make_object(markup)
        self.assertEqual(self.extractor.extract(obj), 'result')

    def test_image_removal(self):
        markup = '''
            <body>
                <img src="me_testing_this_code.jpg">
                result
            </body>
        '''
        obj = self._make_object(markup)
        self.assertEqual(self.extractor.extract(obj), 'result')

    def test_link_anchors_removal(self):
        markup = '''
            <body>
                <a href="example.com">example.com</a>
                <p>Test</p>
            </body>
        '''
        obj = self._make_object(markup)
        self.assertEqual(self.extractor.extract(obj), 'Test')

    def test_text_anchors_saving(self):
        markup = '''
            <body>
                <a href="example.com">link</a>
                <p>Test</p>
            </body>
        '''
        obj = self._make_object(markup)
        self.assertEqual(self.extractor.extract(obj), 'link\nTest')

    def test_link_removal_from_text(self):
        markup = '''
            <body>
                <p>example.com</p>
                <p>Test</p>
            </body>
        '''
        obj = self._make_object(markup)
        self.assertEqual(self.extractor.extract(obj), 'Test')

    def test_multiple_spaces_replacing(self):
        markup = '''
            <body>
                <p>Test         Test</p>
                <p>Test     Test</p>
            </body>
        '''
        obj = self._make_object(markup)
        self.assertEqual(
            self.extractor.extract(obj),
            'Test Test\nTest Test'
        )

    def test_strings_trimming(self):
        markup = '''
            <body>
                <p>  Test    </p>
                <p> Test         </p>
            </body>
        '''
        obj = self._make_object(markup)
        self.assertEqual(
            self.extractor.extract(obj),
            'Test\nTest'
        )


if __name__ == '__main__':
    unittest.main()
