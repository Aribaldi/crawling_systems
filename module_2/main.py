import logging
import sys
import vk_api
import yaml

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

    vk_session = vk_api.VkApi(**cfg["access_params"])
    vk_session.auth()
    vk = vk_session.get_api()

    crawlers = {key: Crawler(
        vk,
        filter_words=cfg["filter_words"][key],
        queries=cfg["queries"][key],
        start_datetime=cfg["start_datetime"]
    ) for key in cfg["queries"]}

    for crawler_name in crawlers:
        crawlers[crawler_name].surf()
