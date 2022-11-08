from datetime import datetime
import unittest
from src.post import Post
from src.parser import Parser

class TestParser(unittest.TestCase):
    def setUp(self) -> None:
        self.parser = Parser(start_datetime=datetime.now().isoformat(),filter_words=['test'])

        self.payload = {
            'id': 0,
            'owner_id': 0,
            'from_id': 0,
            'date': datetime(2048, 1, 1).timestamp(),
            'text': 'test text',
            'comments': {
                'count': 0,
            },
            'likes': {
                'count': 0,
            },
            'reposts': {
                'count': 0,
            },
            'views': {
                'count': 0,
            },
        }

        self.post = Post(
            post_id=self.payload['id'],
            group_id=self.payload['owner_id'],
            publisher_id=self.payload['from_id'],
            date=self.payload['date'],
            text=self.payload['text'],
            comments=self.payload['comments']['count'],
            likes=self.payload['likes']['count'],
            reposts=self.payload['reposts']['count'],
            views=self.payload['views']['count'],
        )
        return super().setUp()

    def test_parser_parse_with_filter_words(self):
        post = self.parser.parse(self.payload)
        self.assertEqual(post, self.post)

    def test_parser_parse_without_filter_words(self):
        parser = Parser(start_datetime=datetime.now().isoformat(),filter_words=['test'])
        post = parser.parse(self.payload)
        self.assertEqual(post, self.post)

    def test_parser_parse_without_views(self):
        del self.payload['views']
        post = self.parser.parse(self.payload)
        self.assertEqual(post.views, 'NULL')

    def test_parser_trimming_text(self):
        self.payload['text'] = '        test text           \n'
        post = self.parser.parse(self.payload)
        self.assertEqual(post.text, 'test text')

    def test_parser_e_replacing(self):
        self.payload['text'] = 'test tёxt ёж'
        post = self.parser.parse(self.payload)
        self.assertEqual(post.text, 'test tеxt еж')

    def test_parser_lowercase_transition(self):
        self.payload['text'] = 'TEST TEXT'
        post = self.parser.parse(self.payload)
        self.assertEqual(post.text, 'test text')

    def test_parser_space_symbols_removal(self):
        self.payload['text'] = '\n\rtest\ntext\t\n'
        post = self.parser.parse(self.payload)
        self.assertEqual(post.text, 'test text')

    def test_parser_multiple_spaces_replacing(self):
        self.payload['text'] = 'test            text'
        post = self.parser.parse(self.payload)
        self.assertEqual(post.text, 'test text')

    def test_parser_links_removal(self):
        self.payload['text'] = 'test https://vk.com https://spbu.ru text'
        post = self.parser.parse(self.payload)
        self.assertEqual(post.text, 'test text')

    def test_random_characters(self):
        s = '$_?@..$(,:[#}{*?.{%?/@?&!@*&,#'
        self.payload['text'] = f'test text {s}'
        post = self.parser.parse(self.payload)
        self.assertEqual(post.text, 'test text ? .. (,: *?. %?/ ? ! * ,')

    def test_cyrillic_alphabet(self):
        alphabet='АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ абвгдеёжзийклмнопрстуфхцчшщъыьэюя'
        self.payload['text'] = f'test text {alphabet}'
        post = self.parser.parse(self.payload)
        self.assertEqual(post.text, 'test text абвгдеежзийклмнопрстуфхцчшщъыьэюя абвгдеежзийклмнопрстуфхцчшщъыьэюя')

    def test_latin_alphabet(self):
        alphabet='ABCDEFGHIJKLMNOPQRSTUVWXYZ abcdefghijklmnopqrstuvwxyz'
        self.payload['text'] = f'test text {alphabet}'
        post = self.parser.parse(self.payload)
        self.assertEqual(post.text, 'test text abcdefghijklmnopqrstuvwxyz abcdefghijklmnopqrstuvwxyz')
