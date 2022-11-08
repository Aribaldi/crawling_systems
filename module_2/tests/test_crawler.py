from datetime import datetime
from os import path
import sqlite3
import unittest
from unittest.mock import MagicMock, Mock, call, patch
import psycopg2
from src.queue import CachedQueue, Queue
from src.storage import PostgresDB
from src.downloader import Downloader
from src.crawler import Crawler
from src.parser import Parser

class TestCrawler(unittest.TestCase):
    def setUp(self) -> None:
        self.conn = sqlite3.connect(":memory:")

        tests_dir_path = path.abspath(path.dirname(__file__))
        with open(path.join(tests_dir_path, '..', 'create_table_script'), "r") as f:
            creation_script = f.read()

            self.conn.executescript(creation_script)
            self.conn.commit()

        with patch.object(psycopg2, 'connect', return_value=self.conn):
            self.postgres = PostgresDB(
                'test_crawler',
                'localhost',
                'test_db',
                'test_user',
                'test_password',
            )

        self.crawler = Crawler(
            downloader=Downloader('2008-09-03T20:56:35.450686'),
            downloader_queue=Queue(['1', '2', '3']) ,
            parser=Parser(start_datetime=datetime.now().isoformat(),filter_words=['test']),
            parser_queue=Queue(['4', '5', '6', '7']),
            storage=self.postgres,
            queries=['spbu'],
        )
        return super().setUp()

    def test_get_posts_by_query(self):
        self.crawler.downloader.get_posts_by_query = MagicMock()
        self.crawler.get_posts_by_query()

        self.crawler.downloader.get_posts_by_query.assert_called_once()

    def test_get_groups_by_query(self):
        self.crawler.downloader.get_groups_by_query = MagicMock()
        self.crawler.get_groups_by_query()

        self.crawler.downloader.get_groups_by_query.assert_called_once()

    def test_get_posts_from_groups(self):
        self.crawler.downloader.get_posts_from_group = MagicMock()
        self.crawler.get_posts_from_groups()

        self.crawler.downloader.get_posts_from_group.assert_has_calls(
            calls=[
                call(group='1', queue_to_push=self.crawler.parser_queue, count=None),
                call(group='2', queue_to_push=self.crawler.parser_queue, count=None),
                call(group='3', queue_to_push=self.crawler.parser_queue, count=None),
            ],
            any_order=True
        )

    def test_parse_posts(self):
        fake_post = 'fake_post'
        self.crawler.parser.parse = Mock(return_value=fake_post)
        self.crawler.storage.store_post = MagicMock()
        self.crawler.parse_posts()

        self.crawler.parser.parse.assert_has_calls(
            calls=[
                call('4'),
                call('5'),
                call('6'),
                call('7'),
            ],
            any_order=True
        )

        self.crawler.storage.store_post.assert_has_calls(
            calls=[
                call(fake_post),
                call(fake_post),
                call(fake_post),
                call(fake_post),
            ]
        )

    def test_close_storage(self):
        self.crawler.storage.close = MagicMock()
        self.crawler.storage.store_cache = MagicMock()

        self.crawler.downloader_queue = CachedQueue()
        self.crawler.downloader_queue.cache = {'1', '2', '3'}

        self.crawler.close_storage()

        self.crawler.storage.store_cache.assert_has_calls(
            calls=[
                call(self.crawler.downloader_queue.cache),
            ]
        )

        self.crawler.storage.close.assert_called_once()
