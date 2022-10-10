import unittest
import unicodedata
import re
from bs4 import BeautifulSoup
from hypothesis import given, note, settings, strategies as st
from extractors.html_text_extractor import HtmlTextExtractor
from readers.html_reader import RemoteHtmlReader
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

    def test_no_alphabetic_chars(self):
        markup = '''
            <body>
                <p>!"#$%&'()*+,-./0123456789:;<=>?@[\]^_`{|}‘’‚‛“”„</p>
            </body>
        '''

        obj = self._make_object(markup)
        self.assertEqual(
            self.extractor.extract(obj),
            '!"#$%&\'()*+,-./0123456789:;<=>?@[\]^_`{|}‘’‚‛“”„'
        )

    def test_latin_alphabet(self):
        markup = '''
            <body>
                <p>ABCDEFGHIJKLMNOPQRSTUVWXYZ</p>
                <p>abcdefghijklmnopqrstuvwxyz</p>
            </body>
        '''
        obj = self._make_object(markup)
        self.assertEqual(
            self.extractor.extract(obj),
            'ABCDEFGHIJKLMNOPQRSTUVWXYZ\nabcdefghijklmnopqrstuvwxyz'
        )

    def test_cyrillic_alphabet(self):
        markup = '''
            <body>
                <p>АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ</p>
                <p>абвгдеёжзийклмнопрстуфхцчшщъыьэюя</p>
            </body>
        '''
        obj = self._make_object(markup)
        self.assertEqual(
            self.extractor.extract(obj),
            'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ\nабвгдеёжзийклмнопрстуфхцчшщъыьэюя'
        )

    @settings(max_examples=50)
    @given(st.text(
        st.characters(blacklist_categories=("Cc", "Cs"),
        blacklist_characters=('<', '>')), min_size=1)
    )
    def test_random_characters(self, s):
        markup = '''
            <body>
                <p>{}</p>
            </body>
        '''
        obj = self._make_object(markup.format(s))
        res = self.extractor.extract(obj)
        note(f"Raw data: {s}")
        note(f"Result: {res}")
        norm_s = unicodedata.normalize("NFKC", s)
        self.assertEqual(res, self.extractor.clean_text(norm_s))

    def test_empty_markup(self):
        markup = ''
        obj = self._make_object(markup)
        self.assertEqual(
            self.extractor.extract(obj),
            ''
        )

    def test_long_multilang(self):
        remote_reader = RemoteHtmlReader(headers={})
        obj = remote_reader.read(
            'https://ru.wikipedia.org/wiki/%D0%92%D0%BE%D0%B9%D0%BD%D0%B0_%D0%B8_%D0%BC%D0%B8%D1%80#cite_note-31'
        )
        res = self.extractor.extract(obj)

        res_predicate = all([re.search(phrase, res) for phrase in [
            "Главная тема — историческая судьба русского народа в Отечественной войне 1812 года",
            "La Guerre et la Paix",
            "The 10 Greatest Books of All Time"
            ]
        ])
        self.assertTrue(res_predicate)


if __name__ == '__main__':
    unittest.main()
