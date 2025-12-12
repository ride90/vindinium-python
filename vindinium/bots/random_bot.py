"""Random bot implementation that makes random moves.

This module provides a simple bot that randomly selects moves,
useful for testing and as a baseline for comparison.
"""

import random
from vindinium.bots import RawBot

__all__ = ["RandomBot"]


class RandomBot(RawBot):
    """Bot that makes random moves.

    This bot randomly selects one of the five possible moves
    (North, South, East, West, Stay) at each turn.
    """

    def move(self):
        """Select a random move.

        Returns:
            str: A randomly chosen direction from 'Stay', 'North', 'West', 'East', 'South'.
        """
        return random.choice(["Stay", "North", "West", "East", "South"])
