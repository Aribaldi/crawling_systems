import unittest

from src.parser import Parser

class TestParser(unittest.TestCase):
    def setUp(self) -> None:
        self.parser = Parser([])
        return super().setUp()

    def test_parse_should_pass(self):
        self.assertEqual(self.parser.parse(), None)