from datetime import datetime
import unittest
import vk_api
import yaml
from src.downloader import Downloader

class TestDownloader(unittest.TestCase):
    def setUp(self) -> None:
        with open("config.yaml", "r", encoding="utf-8") as f:
            cfg = yaml.load(f, Loader=yaml.FullLoader)

        vk_session = vk_api.VkApi(**cfg["access_params"])
        vk_session.auth()
        vk = vk_session.get_api()
        self.downloader = Downloader(vk, datetime.now())
        return super().setUp()

    def test_should_download(self):
        pass