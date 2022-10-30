import logging
from typing import Optional

from src.queue import CachedQueue
from src.storage import PostgresDB

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
        self.downloader = downloader
        self.downloader_queue = downloader_queue
        self.parser = parser
        self.parser_queue = parser_queue
        self.storage = storage
        self.queries = queries

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
        while len(self.downloader_queue) > 0:
            self.downloader.get_posts_from_group(group=self.downloader_queue.pop(),
                                                 queue_to_push=self.parser_queue,
                                                 count=count)

    def parse_posts(self):
        while len(self.parser_queue) > 0:
            parsed_post = self.parser.parse(self.parser_queue.pop())
            if parsed_post is not None:
                self.storage.store_post(parsed_post)

    def close_storage(self):
        if isinstance(self.downloader_queue, CachedQueue) and isinstance(self.storage, PostgresDB):
            self.storage.store_cache(self.downloader_queue.cache)
        self.storage.close()

