from datetime import datetime
import logging
import random
import time
from typing import Optional, Tuple
import vk_api

from src.queue import Queue

logger = logging.getLogger(__name__)


class Downloader:
    def __init__(self, vk, start_datetime):
        self.vk = vk
        self.start_datetime = datetime.fromisoformat(start_datetime)
        self.post_fields = ["id", "from_id", "date", "text", "comments", "likes", "reposts", "views", "signer_id"]

    def get_posts_by_query(self, query: str, queue_to_push: Queue, count: Optional[int] = None):
        n_posts = 0
        last_record_datetime = datetime.now()
        start_time = time.time()
        while last_record_datetime > self.start_datetime and (count is not None and n_posts < count):
            next_count = 200 if count is None or count - n_posts > 200 else count - n_posts
            new_posts = self.vk.newsfeed.search(
                q=query,
                count=next_count,
                offset=n_posts,
                extended=1,
                field=self.post_fields,
                start_time=str(int(self.start_datetime.timestamp()))
            )["items"]
            if not new_posts:
                break
            last_record_datetime = datetime.fromtimestamp(new_posts[-1]["date"])
            new_posts = [
                ((post["id"], post["owner_id"]), post)
                for post in new_posts
                if datetime.fromtimestamp(post["date"]) > self.start_datetime
            ]
            if not new_posts:
                break
            queue_to_push.push(new_posts)
            n_posts += len(new_posts)
            if n_posts % 1_000 == 0:
                logger.info(f"Found {n_posts} posts by query \"{query}\". Continue downloading ...")
            time.sleep(random.uniform(0.1, 0.3))

        logger.info(f"Found {n_posts} posts by query \"{query}\". " +
                    f"Downloading took {int(time.time() - start_time)} seconds")

    def get_groups_by_query(self, query: str, queue_to_push: Queue, count: int = 100):
        n_groups = 0
        while n_groups < count:
            try:
                new_groups = self.vk.groups.search(
                    q=query,
                    offset=n_groups,
                    count=min(count - n_groups, 100)
                )["items"]
                if not new_groups:
                    break
                queue_to_push.push(
                    [((-new_groups[i]["id"], new_groups[i]["name"]), (-new_groups[i]["id"], new_groups[i]["name"]))
                     for i in range(count - n_groups)]  # keys for cache and items to insert into queue
                )
                n_groups += len(new_groups)
            except vk_api.exceptions.ApiError as err:
                logger.warning(f"Next error was caught: \"{str(err)}\". Continue downloading from the next query")

        if n_groups == 0:
            logger.warning("No group was found")
        elif n_groups < count:
            logger.warning(f"Only {n_groups} out of {count} groups found")
        else:
            logger.info(f"Found {n_groups} groups")

    def get_posts_from_group(self, group: Tuple, queue_to_push: Queue, count: Optional[int] = None):
        group_id, group_name = group
        if group_id > 0:
            group_id = -group_id
        start_time = time.time()
        n_posts = 0
        last_record_datetime = datetime.now()
        try:
            while last_record_datetime > self.start_datetime or (count is not None and n_posts < count):
                next_count = 100 if count is None or count - n_posts > 100 else count - n_posts
                new_posts = self.vk.wall.get(owner_id=[group_id], count=next_count, offset=n_posts,
                                             extended=1, field=self.post_fields)["items"]
                if not new_posts:
                    break
                last_record_datetime = datetime.fromtimestamp(new_posts[-1]["date"])
                new_posts = [
                    ((post["id"], post["owner_id"]), post)
                    for post in new_posts
                    if datetime.fromtimestamp(post["date"]) > self.start_datetime
                ]
                if not new_posts:
                    break
                queue_to_push.push(new_posts)
                n_posts += len(new_posts)
            logger.info(f"Found {n_posts} posts from group \"{group_name}\". " +
                        f"Downloading took {int(time.time() - start_time)} seconds")
        except vk_api.exceptions.ApiError as err:
            logger.warning(f"Next error was caught: \"{str(err)}\"")

