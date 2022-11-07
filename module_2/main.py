import logging
import sys
# import vk_api
import multiprocessing as mp
import yaml

from src.downloader import Downloader, RequestDownloader
from src.parser import Parser
from src.queue import Queue, CachedQueue, MultiProcessQueue
from src.storage import Storage, PostgresDB

from src.crawler import Crawler, MultiProcessCrawler

logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)8.8s | %(name)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[logging.StreamHandler(sys.stdout)],
)

MODE = "single"  # single / multi

if __name__ == "__main__":
    with open("config.yaml", "r", encoding="utf-8") as f:
        cfg = yaml.load(f, Loader=yaml.FullLoader)

    # vk_session = vk_api.VkApi(**cfg["vk"])
    # vk_session.auth()
    # vk = vk_session.get_api()

    crawlers = {}
    if MODE == "single":
        for crawler_name in cfg["queries"]:
            crawlers[crawler_name] = Crawler(
                downloader=RequestDownloader(access_params=cfg["vk"], start_datetime=cfg["start_datetime"]),
                downloader_queue=CachedQueue(),
                parser=Parser(filter_words=cfg["filter_words"][crawler_name], start_datetime=cfg["start_datetime"]),
                parser_queue=CachedQueue(),
                storage=PostgresDB(crawler_name=crawler_name, **cfg["db"]),
                queries=cfg["queries"][crawler_name],
            )
    else:
        for crawler_name in cfg["queries"]:
            crawlers[crawler_name] = MultiProcessCrawler(
                downloader=Downloader(access_params=cfg["vk"], start_datetime=cfg["start_datetime"]),
                downloader_queue=MultiProcessQueue(),
                parser=Parser(cfg["filter_words"][crawler_name]),
                parser_queue=MultiProcessQueue(),
                storage=PostgresDB(crawler_name=crawler_name, **cfg["db"]),
                queries=cfg["queries"][crawler_name],
            )

    for crawler_name in crawlers:
        crawlers[crawler_name].crawl()
