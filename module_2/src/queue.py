from typing import List, Optional
import threading


class BaseQueue:
    _queue = None

    def pop(self):
        raise NotImplementedError

    def push(self, items):
        raise NotImplementedError

    def is_empty(self):
        raise NotImplementedError


class Queue(BaseQueue):
    def __init__(self, init_items: Optional[List] = None):
        self._queue = []
        if init_items is not None:
            self.push(init_items)

    def pop(self):
        return self._queue.pop(0)

    def push(self, items):
        if not isinstance(items, List):
            items = [items]
        self._queue.extend(items)

    def is_empty(self):
        return not bool(self._queue)


class CachedQueue(Queue):
    def __init__(self, init_items=None, cache=None):
        if cache is None:
            cache = []
        self.cache = set(cache)
        super(CachedQueue, self).__init__(init_items)

    def _push(self, item):
        key, item = item
        if key not in self.cache:
            self._queue.append(item)
            self.cache.add(key)

    def push(self, items):
        if not isinstance(items, List):
            items = [items]
        for item in items:
            self._push(item)


class MultiProcessQueue(BaseQueue):
    def __init__(self):
        self._queue = []
        self.lock = threading.Lock()

    def pop(self):
        with self.lock:
            self._queue.pop(0)

    def _push(self, item):
        with self.lock:
            self._queue.append(item)

    def push(self, items):
        if not isinstance(items, List):
            items = [items]
        for item in items:
            self._push(item)

    def is_empty(self):
        with self.lock:
            return bool(self._queue)




