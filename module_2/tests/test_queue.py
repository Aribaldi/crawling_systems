import unittest

from src.queue import Queue, CachedQueue

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
        self.assertEqual(self.queue.pop(), self.initial_items[0])

    def test_len(self):
        self.assertEqual(len(self.queue._queue), len(self.initial_items))

class TestCachedQueue(unittest.TestCase):
    def setUp(self) -> None:
        self.initial_items = [1, 2, 3]
        return super().setUp()

    def test_cache_empty_on_init(self):
        queue = CachedQueue()
        self.assertListEqual(list(queue.cache), [])

    def test_cache_inits_with_unique_entries(self):
        input_cache = ['key1', 'key1', 'key2', 'key2', 'key3']

        queue = CachedQueue(cache=input_cache)

        target_cache = ['key1', 'key2', 'key3']
        self.assertListEqual(sorted(list(queue.cache)), sorted(target_cache))

    def test_push_adds_to_cache_and_queue(self):
        initial_items_dict = {f'item{n}' : n for n in self.initial_items}
        queue = CachedQueue(init_items=list(initial_items_dict.items()))

        items = [5, 6, 7]
        items_dict = {f'item{n}' : n for n in items}

        queue.push(list(items_dict.items()))

        self.assertListEqual(sorted(queue._queue), sorted(self.initial_items + items))

        target_cache =  list(initial_items_dict.keys()) + list(items_dict.keys())
        self.assertListEqual(sorted(list(queue.cache)), sorted(target_cache))
