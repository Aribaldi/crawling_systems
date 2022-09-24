import unittest
from extractors.html_text_extractor import HtmlTextExtractor


class TestHtmlTextExtractor(unittest.TestCase):
    def setUp(self):
        self.extractor = HtmlTextExtractor()

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
        self.assertEqual(self.extractor.extract(markup), 'Test paragraph')

    def test_header_removal(self):
        header_markup = '''
            <body>
                <header>
                    Test header
                </header>
                <p>
                    Some test text
                </p>
            </body>
        '''
        self.assertEqual(
            self.extractor.extract(header_markup),
            'Some test text'
        )

    def test_footer_removal(self):
        footer_markup = '''
            <body>
                <p>
                    Some test text
                </p>
                <footer>
                    Test footer
                </footer>
            </body>
        '''
        self.assertEqual(
            self.extractor.extract(footer_markup),
            'Some test text'
        )

    def test_code_removal(self):
        code_markup = '''
            <body>
                <code>
                    main :: IO ()
                    main = putStrLn "Hello, World!"
                </code>
                result
            </body>
        '''
        self.assertEqual(self.extractor.extract(code_markup), 'result')

    def test_table_removal(self):
        table_markup = '''
        <body>
            <table>
                cell goes brrrrrr
            </table>
            result
        </body>
        '''
        self.assertEqual(self.extractor.extract(table_markup), 'result')

    def test_image_removal(self):
        image_markup = '''
            <body>
                <img src="me_testing_this_code.jpg">
                result
            </body>
        '''
        self.assertEqual(self.extractor.extract(image_markup), 'result')

    def test_link_anchors_removal(self):
        image_markup = '''
            <body>
                <a href="example.com">example.com</a>
                <p>Test</p>
            </body>
        '''
        self.assertEqual(self.extractor.extract(image_markup), 'Test')

    def test_text_anchors_saving(self):
        image_markup = '''
            <body>
                <a href="example.com">link</a>
                <p>Test</p>
            </body>
        '''
        self.assertEqual(self.extractor.extract(image_markup), 'link\nTest')

    def test_link_removal_from_text(self):
        markup = '''
            <body>
                <p>example.com</p>
                <p>Test</p>
            </body>
        '''
        self.assertEqual(self.extractor.extract(markup), 'Test')

    def test_multiple_spaces_replacing(self):
        spaces_markup = '''
            <body>
                <p>Test         Test</p>
                <p>Test     Test</p>
            </body>
        '''

        self.assertEqual(
            self.extractor.extract(spaces_markup),
            'Test Test\nTest Test'
        )

    def test_strings_trimming(self):
        spaces_markup = '''
            <body>
                <p>  Test    </p>
                <p> Test         </p>
            </body>
        '''

        self.assertEqual(
            self.extractor.extract(spaces_markup),
            'Test\nTest'
        )


if __name__ == '__main__':
    unittest.main()
