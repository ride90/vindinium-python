"""Base bot implementation with game state processing.

This module provides the BaseBot class which extends RawBot to automatically
process the raw game state into structured Game and Hero objects.
"""

from vindinium.bots import RawBot
from vindinium.models import Game

__all__ = ['BaseBot']


class BaseBot(RawBot):
    """Base bot with automatic game state processing.

    This bot extends RawBot by automatically parsing the raw JSON state
    into structured Game and Hero objects, making it easier to access
    game information.

    Attributes:
        id (int): The bot's unique identifier.
        game (vindinium.models.Game): The game instance, automatically updated.
        hero (vindinium.models.Hero): The bot's hero instance, automatically updated.
        state (dict): The unprocessed state dictionary from the server.
    """

    id = None
    state = None
    game = None
    hero = None

    def _start(self, state):
        """Internal wrapper for the start method.

        Processes the initial state into Game and Hero objects before
        calling the user-defined start() method.

        Args:
            state (dict): The initial game state from the server.
        """
        self.id = state['hero']['id']
        self.state = state
        self.game = Game(state)
        self.hero = self.game.heroes[self.id - 1]
        self.start()

    def _move(self, state):
        """Internal wrapper for the move method.

        Updates the game state before calling the user-defined move() method.

        Args:
            state (dict): The current game state from the server.

        Returns:
            str: The direction to move ('North', 'South', 'East', 'West', 'Stay').
        """
        self.state = state
        self.game.update(state)
        return self.move()

    def _end(self):
        """Internal wrapper for the end method."""
        self.end()
        