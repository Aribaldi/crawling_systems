import unittest

from src.crawler import Crawler

class TestCrawler(unittest.TestCase):
    def setUp(self) -> None:
        self.parser = Crawler()
        return super().setUp()

    def test_parse_should_pass(self):
        self.assertEqual(self.parser.parse(), None)