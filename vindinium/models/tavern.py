"""Tavern model representing a healing location on the map.

This module provides the Tavern class which represents a location
where heroes can heal in exchange for gold.
"""

__all__ = ['Tavern']


class Tavern:
    """Represents a tavern on the map.

    Taverns allow heroes to heal 50 HP in exchange for 2 gold.

    Attributes:
        x (int): The tavern's position on the X axis.
        y (int): The tavern's position on the Y axis.
    """

    def __init__(self, x, y):
        """Initialize a tavern at the given position.

        Args:
            x (int): The tavern's position on the X axis.
            y (int): The tavern's position on the Y axis.
        """
        self.x = x
        self.y = y


