from typing import List


class Queue:
    def __init__(self, init_items: List = None):
        self._queue = []
        if init_items is not None:
            self._queue.extend(init_items)

    def pop(self):
        return self._queue.pop(0)

    def push(self, items):
        if isinstance(items, int):
            self._queue.append(items)
        else:
            self._queue.extend(items)

    def __len__(self):
        return len(self._queue)
