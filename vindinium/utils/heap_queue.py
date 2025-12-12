"""Priority queue implementation using heapq.

This module provides a priority queue implementation for use in
pathfinding algorithms like A*.
"""

import heapq

__all__ = ["HeapQueue"]


class HeapQueue:
    """A priority queue implementation using the heapq builtin module.

    Based on http://www.redblobgames.com/pathfinding/a-star/implementation.html
    """

    def __init__(self):
        """Initialize an empty priority queue."""
        self._queue = []

    def is_empty(self):
        """Check if the queue is empty.

        Returns:
            bool: True if the queue is empty, False otherwise.
        """
        return len(self._queue) == 0

    def push(self, item, priority):
        """Push an item to the queue with a given priority.

        Args:
            item (object): Any object to store.
            priority (int): A priority value (lower values have higher priority).
        """
        heapq.heappush(self._queue, (priority, item))

    def pop(self):
        """Pop the item with the highest priority from the queue.

        Returns:
            object: The stored item with the highest priority.
        """
        return heapq.heappop(self._queue)[1]
