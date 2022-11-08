from datetime import datetime
import unittest
from unittest.mock import MagicMock, Mock
from src.queue import Queue
from src.downloader import Downloader

class MockVK:
    def __init__(self) -> None:
        self.wall = self.MockWall()
        self.newsfeed = self.MockNewsfeed()
        self.groups = self.MockGroups()

    class MockWall:
        def get(self):
            pass

    class MockNewsfeed:
        def search(self):
            pass

    class MockGroups:
        def search(self):
            pass

class TestDownloader(unittest.TestCase):
    def setUp(self) -> None:
        self.vk = MockVK()
        self.start_datetime = datetime.now()
        self.vk.newsfeed.search = Mock(return_value={'items':[]})
        self.vk.groups.search = Mock(return_value={'items':[]})
        self.vk.wall.get = Mock(return_value={'items':[]})
        self.downloader = Downloader(vk=self.vk, start_datetime=datetime(2022, 11, 4).isoformat())
        return super().setUp()

    def test_get_posts_by_query(self):
        queue = Queue()
        queue.push = MagicMock()
        self.vk.newsfeed.search = Mock(
            return_value={
                'items': [
                    {
                        'id': 0,
                        'owner_id': 0,
                        'from_id': 0,
                        'date': datetime(2022, 11, 3).isoformat(),
                        'text': 'test text',
                        'comments': {
                            'count': 0,
                        },
                        'likes': {
                            'count': 0,
                        },
                        'reposts': {
                            'count': 0,
                        },
                        'views': {
                            'count': 0,
                        },
                    },
                ]
            }
        )
        self.downloader.get_posts_by_query(query='test', queue_to_push=queue)

        queue.push.assert_not_called()

    def test_get_groups_by_query(self):
        queue = Queue()
        queue.push = MagicMock()

        self.downloader.get_groups_by_query(query='test', queue_to_push=queue)

        queue.push.assert_not_called()

    def test_get_posts_from_group(self):
        queue = Queue()
        queue.push = MagicMock()

        self.downloader.get_posts_from_group(group=(0, 'group'), queue_to_push=queue)

        queue.push.assert_not_called()
