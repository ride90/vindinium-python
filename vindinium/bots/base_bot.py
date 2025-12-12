"""Base bot implementation with game state processing.

This module provides the BaseBot class which extends RawBot to automatically
process the raw game state into structured Game and Hero objects.
"""

from vindinium.bots import RawBot
from vindinium.models import Game

__all__ = ["BaseBot"]


class BaseBot(RawBot):
    """Base bot with automatic game state processing.

    This bot extends RawBot by automatically parsing the raw JSON state
    into structured Game and Hero objects, making it easier to access
    game information.

    Override _do_start(), _do_move(), and _do_end() to implement your bot logic.

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

    def start(self, state):
        """Called by the Client when the game starts.

        Processes the initial state into Game and Hero objects before
        calling the user-defined _do_start() method.

        Args:
            state (dict): The initial game state from the server.
        """
        self.id = state["hero"]["id"]
        self.state = state
        self.game = Game(state)
        self.hero = self.game.heroes[self.id - 1]
        self._do_start()

    def move(self, state):
        """Called by the Client when a move is requested.

        Updates the game state before calling the user-defined _do_move() method.

        Args:
            state (dict): The current game state from the server.

        Returns:
            str: The direction to move ('North', 'South', 'East', 'West', 'Stay').
        """
        self.state = state
        self.game.update(state)
        return self._do_move()

    def end(self):
        """Called by the Client when the game finishes.

        Calls the user-defined _do_end() for cleanup.
        """
        self._do_end()
