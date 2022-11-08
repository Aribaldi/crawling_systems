from os import path
import sqlite3
import unittest
from unittest.mock import patch
import psycopg2
from src.storage import PostgresDB
from src.post import Post

class TestStorage(unittest.TestCase):
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

        return super().setUp()

    def tearDown(self) -> None:
        self.postgres=None
        self.conn.close()
        return super().tearDown()

    def test_store_post(self):
        post = Post(0, 0, 0, 0, '', 0, 0, 0, 0)

        self.postgres.store_post(post)

        post_ids = self.conn.execute('SELECT post_id FROM post;').fetchall()
        self.assertEqual(post_ids, [(post.post_id, )])

    def test_load_posts(self):
        posts = [
            Post(0, 0, 0, 0, '', 0, 0, 0, 0),
            Post(1, 0, 0, 0, '', 0, 0, 0, 0),
            Post(2, 0, 0, 0, '', 0, 0, 0, 0),
        ]

        for post in posts:
            self.conn.execute("INSERT INTO post(post_id, group_id, publisher_id, date_unix, text, " +
                        "comments, likes, reposts, views, crawler_name)\n" +
                        f"VALUES ({post.post_id}, {post.group_id}, {post.publisher_id}, {post.date}, '{post.text}', " +
                        f"{post.comments}, {post.likes}, {post.reposts}, {post.views}, 'test_crawler');")
        self.conn.commit()

        loaded_posts = self.postgres.load_posts()

        self.assertListEqual([post.post_id for post in loaded_posts], [post.post_id for post in posts])

    def test_load_posts_empty(self):
        self.assertListEqual(self.postgres.load_posts(), [])

    def test_store_cache(self):
        cache = [(0, 'group1'), (1, 'group2'), (2, 'group3')]
        self.postgres.store_cache(cache)

        group_ids = self.conn.execute('SELECT group_id FROM group_cache;').fetchall()

        self.assertListEqual(group_ids, [(group_id, ) for group_id, _ in cache])

    def test_load_cache(self):
        cache = [(0, 'group1'), (1, 'group2'), (2, 'group3')]
        
        query = "INSERT INTO group_cache(group_id, group_name, crawler_name) VALUES " + \
                    ", ".join(
                        [f"({group_id}, '{group_name}', 'test_crawler')"
                         for group_id, group_name in cache]
                    )
        self.conn.execute(query)
        self.conn.commit()

        loaded_group_ids = self.postgres.load_cache()

        self.assertListEqual(loaded_group_ids, [(group_id, ) for group_id, _ in cache])

    def test_load_cache_empty(self):
        self.assertListEqual(self.postgres.load_cache(), [])

    def test_close(self):
        self.postgres.close()
        self.assertRaises(sqlite3.ProgrammingError, self.postgres.load_posts)
