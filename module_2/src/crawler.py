import logging
from typing import List, Optional

from src.downloader import Downloader
from src.queue import Queue
from src.parser import Parser

logger = logging.getLogger(__name__)


class Crawler:
    def __init__(
            self,
            vk,
            filter_words: List[str],
            queries: List[str],
            start_datetime: str,
            init_groups: Optional[List] = None
    ):
        self.downloader = Downloader(vk, start_datetime=start_datetime)
        self.downloader_queue = Queue(init_items=init_groups)
        self.parser = Parser(filter_words)
        self.parser_queue = Queue()
        self.queries = queries

    def surf(self):
        for query in self.queries:
            logger.info(f"Searching groups by query {query}")
            group_ids = self.downloader.get_groups_by_query(query=query)
            if len(group_ids) > 0:
                self.downloader_queue.push(group_ids)

        while len(self.downloader_queue) > 0:
            new_records = self.downloader.download_records_from_group(self.downloader_queue.pop())
            if len(new_records) > 0:
                self.parser_queue.push(new_records)
