import logging
import threading

from typing import Optional, List

from src.downloader import Downloader
from src.parser import Parser
from src.queue import CachedQueue, BaseQueue
from src.storage import PostgresDB, Storage

logger = logging.getLogger(__name__)


class Crawler:
    def __init__(
            self,
            downloader,
            downloader_queue,
            parser,
            parser_queue,
            storage,
            queries,
    ):
        self.downloader: Downloader = downloader
        self.downloader_queue: BaseQueue = downloader_queue
        self.parser: Parser = parser
        self.parser_queue: BaseQueue = parser_queue
        self.storage: Storage = storage
        self.queries: List = queries

    def get_posts_by_query(self, count: Optional[int] = None):
        for query in self.queries:
            logger.info(f"Searching posts by query \"{query}\"")
            self.downloader.get_posts_by_query(query=query,
                                               queue_to_push=self.parser_queue,
                                               count=count)

    def get_groups_by_query(self, count: int = 100):
        for query in self.queries:
            logger.info(f"Searching groups by query \"{query}\"")
            self.downloader.get_groups_by_query(query=query,
                                                queue_to_push=self.downloader_queue,
                                                count=count)

    def get_posts_from_groups(self,  count: Optional[int] = None):
        while not self.downloader_queue.is_empty():
            self.downloader.get_posts_from_group(group=self.downloader_queue.pop(),
                                                 queue_to_push=self.parser_queue,
                                                 count=count)

    def parse_posts(self):
        while not self.parser_queue.is_empty():
            parsed_post = self.parser.parse(self.parser_queue.pop())
            if parsed_post is not None:
                self.storage.store_post(parsed_post)

    def close_storage(self):
        if isinstance(self.downloader_queue, CachedQueue) and isinstance(self.storage, PostgresDB):
            self.storage.store_cache(self.downloader_queue.cache)
        self.storage.close()

    def crawl(self):
        self.get_posts_by_query()
        self.get_groups_by_query(count=100)
        self.get_posts_from_groups()
        self.parse_posts()
        self.close_storage()


class MultiProcessCrawler(Crawler):
    def crawl(self):

        pr_posts_by_query = threading.Thread(target=self.get_groups_by_query, args=(100_000, ))
        pr_groups_by_query = threading.Thread(target=self.get_groups_by_query)
        pr_posts_from_groups = threading.Thread(target=self.get_posts_from_groups)
        pr_parse_posts = threading.Thread(target=self.parse_posts)

        pr_posts_by_query.start()
        pr_groups_by_query.start()
        pr_posts_from_groups.start()
        pr_parse_posts.start()

        pr_posts_by_query.join()
        pr_groups_by_query.join()
        pr_posts_from_groups.join()
        pr_parse_posts.join()
