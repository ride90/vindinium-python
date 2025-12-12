"""Map model representing the game board.

This module provides the Map class which represents the game board
with static elements like walls, paths, taverns, mines, and spawn points.
"""

__all__ = ["Map"]


class Map:
    """Represents the game board with static elements.

    The map stores information about walls, paths, taverns, mines,
    and spawn points on the game board.

    Attributes:
        size (int): The board size (width and height are equal).
    """

    def __init__(self, size):
        """Initialize a map with the given size.

        Args:
            size (int): The board size (creates a size x size grid).
        """
        self.size = size
        self.__board = [[0 for i in range(size)] for j in range(size)]

    def __getitem__(self, key):
        """Get an item from the map at the given coordinates.

        Args:
            key (tuple): A tuple of (x, y) coordinates.

        Returns:
            int: The tile value at the given position.
        """
        return self.__board[key[0]][key[1]]

    def __setitem__(self, key, value):
        """Set an item in the map at the given coordinates.

        Args:
            key (tuple): A tuple of (x, y) coordinates.
            value (int): The tile value to set.
        """
        self.__board[key[0]][key[1]] = value

    def __str__(self):
        """Return a pretty string representation of the map.

        Returns:
            str: ASCII art representation of the map.
        """
        s = " "
        s += "-" * (self.size) + "\n"
        for y in range(self.size):
            s += "|"
            for x in range(self.size):
                s += str(self[x, y] or " ")
            s += "|\n"
        s += " " + "-" * (self.size)
        return s
