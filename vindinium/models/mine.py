"""Mine model representing a gold mine on the map.

This module provides the Mine class which represents a capturable
gold mine that generates income for its owner.
"""

__all__ = ['Mine']


class Mine:
    """Represents a gold mine on the map.

    Mines can be captured by heroes and generate 1 gold per turn
    for their owner.

    Attributes:
        x (int): The mine's position on the X axis.
        y (int): The mine's position on the Y axis.
        owner (int): The hero ID that owns this mine (None if uncaptured).
    """

    def __init__(self, x, y):
        """Initialize a mine at the given position.

        Args:
            x (int): The mine's position on the X axis.
            y (int): The mine's position on the Y axis.
        """
        self.x = x
        self.y = y
        self.owner = None
