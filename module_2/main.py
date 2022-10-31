import logging
import sys
import vk_api
import yaml

from src.downloader import Downloader
from src.parser import Parser
from src.queue import Queue, CachedQueue
from src.storage import Storage, PostgresDB

from src.crawler import Crawler

logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)8.8s | %(name)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[logging.StreamHandler(sys.stdout)],
)

if __name__ == "__main__":
    with open("config.yaml", "r", encoding="utf-8") as f:
        cfg = yaml.load(f, Loader=yaml.FullLoader)

    vk_session = vk_api.VkApi(**cfg["vk"])
    vk_session.auth()
    vk = vk_session.get_api()

    crawlers = {}
    for crawler_name in cfg["queries"]:
        crawlers[crawler_name] = Crawler(
            downloader=Downloader(vk, start_datetime=cfg["start_datetime"]),
            downloader_queue=CachedQueue(),
            parser=Parser(cfg["filter_words"][crawler_name]),
            parser_queue=CachedQueue(),
            storage=PostgresDB(crawler_name=crawler_name, **cfg["db"]),
            queries=cfg["queries"][crawler_name],
        )

    for crawler_name in crawlers:
        crawlers[crawler_name].get_posts_by_query(count=1000000)
        crawlers[crawler_name].get_groups_by_query()
        crawlers[crawler_name].get_posts_from_groups()
        crawlers[crawler_name].parse_posts()
        crawlers[crawler_name].close_storage()
