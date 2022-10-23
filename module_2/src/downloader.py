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

    def get_groups_by_query(self, query: str, count: int = 100) -> List:
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

    def download_records_from_group(self, group_id: int) -> List:
        if group_id > 0:
            group_id = -group_id
        start_time = time.time()
        records = []
        last_record_datetime = datetime.now()
        try:
            while last_record_datetime > self.start_datetime:
                new_records = self.vk.wall.get(owner_id=[group_id], count=100, offset=len(records))["items"]
                if len(new_records) == 0:
                    break
                records.extend(new_records)
                last_record_datetime = datetime.fromtimestamp(records[-1]["date"])
                records.extend([
                    record
                    for record in new_records
                    if datetime.fromtimestamp(record["date"]) > self.start_datetime
                ])
            logger.info(f"Found {len(records)} records. Downloading took {int(time.time() - start_time)} seconds")
        except vk_api.exceptions.ApiError as err:
            print(f"Next error was caught: \"{str(err)}\"")
        return records

