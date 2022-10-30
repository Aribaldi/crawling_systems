import unittest

from src.queue import Queue

class TestQueue(unittest.TestCase):
    def setUp(self) -> None:
        self.initial_items = [1, 2, 3]
        self.queue = Queue(init_items=self.initial_items)
        return super().setUp()

    def test_push_appends_value(self):
        self.queue.push(1)
        self.assertListEqual(self.queue._queue, self.initial_items + [1])

    def test_pop_removes_value(self):
        self.queue.pop()
        self.assertListEqual(self.queue._queue, self.initial_items[1:])

    def test_pop_returns_value(self):
        self.assertListEqual(self.queue.pop(), self.initial_items[0])

    def test_len(self):
        self.assertEqual(len(self.queue), len(self.initial_items))
