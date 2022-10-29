from datetime import datetime
import logging
import time
from typing import List
import vk_api

logger = logging.getLogger(__name__)


class Downloader:
    def __init__(self, vk, start_datetime):
        self.vk = vk
        self.start_datetime = datetime.fromisoformat(start_datetime)
        self.post_fields = ["id", "from_id", "date", "text", "comments", "likes", "reposts", "views", "signer_id"]

    def get_groups_by_query(self, query: str, count: int = 2) -> List:
        group_ids = []
        while len(group_ids) < count:
            try:
                new_group_ids = self.vk.groups.search(
                    q=query,
                    offset=len(group_ids),
                    count=max(count - len(group_ids), 100)
                )["items"]
                if len(new_group_ids) == 0:
                    break
                group_ids.extend([-new_group_ids[i]["id"] for i in range(count - len(group_ids))])
            except vk_api.exceptions.ApiError as err:
                logger.warning(f"Next error was caught: \"{str(err)}\". Continue downloading from the next query")

        if len(group_ids) == 0:
            logger.warning("No group was found")
        elif len(group_ids) < count:
            logger.warning(f"Only {len(group_ids)} out of {count} groups found")
        else:
            logger.info(f"Found {len(group_ids)} groups")
        return group_ids

    def download_posts_from_group(self, group_id: int) -> List:
        if group_id > 0:
            group_id = -group_id
        start_time = time.time()
        posts = []
        last_record_datetime = datetime.now()
        try:
            while last_record_datetime > self.start_datetime:
                new_posts = self.vk.wall.get(owner_id=[group_id], count=100, offset=len(posts),
                                             extended=1, field=self.post_fields)["items"]
                new_posts = list(filter(lambda post: datetime.fromtimestamp(post["date"]) > self.start_datetime,
                                        new_posts))
                if len(new_posts) == 0:
                    break
                posts.extend(new_posts)
                last_record_datetime = datetime.fromtimestamp(posts[-1]["date"])
            logger.info(f"Found {len(posts)} posts. Downloading took {int(time.time() - start_time)} seconds")
        except vk_api.exceptions.ApiError as err:
            logger.warning(f"Next error was caught: \"{str(err)}\"")
        return posts

