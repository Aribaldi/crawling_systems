import logging

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

    def get_groups(self):
        for query in self.queries:
            logger.info(f"Searching groups by query {query}")
            group_ids = self.downloader.get_groups_by_query(query=query)
            if len(group_ids) > 0:
                self.downloader_queue.push(group_ids)

    def get_posts(self):
        while len(self.downloader_queue) > 0:
            new_posts = self.downloader.download_posts_from_group(self.downloader_queue.pop())
            if len(new_posts) > 0:
                self.parser_queue.push(new_posts)

    def parse_posts(self):
        while len(self.parser_queue) > 0:
            parsed_post = self.parser.parse(self.parser_queue.pop())
            if parsed_post is not None:
                logger.info("Saving new post to storage")
                self.storage.store_post(parsed_post)

    def close_storage(self):
        if isinstance(self.downloader_queue, CachedQueue) and isinstance(self.storage, PostgresDB):
            self.storage.store_cache(self.downloader_queue.cache)
        self.storage.close()

