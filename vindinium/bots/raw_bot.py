"""Raw bot implementation that provides the base interface for all bots.

This module defines the RawBot class which serves as the minimal bot
interface without any state processing.
"""

__all__ = ["RawBot"]


class RawBot:
    """Raw bot that does not process the game state.

    This is the most basic bot interface. Subclasses should implement
    the start(), move(), and end() methods to create a functional bot.

    Implement the following methods to use:
    - start(state): called when the game starts.
    - move(state): called when the game requests a move from this bot.
    - end(): called after the game finishes.

    Attributes:
        id (int): The bot's unique identifier.
        state (dict): The unprocessed state dictionary from the server.
    """

    id = None
    state = None

    def _start(self, state):
        """Internal wrapper for the start method.

        Args:
            state (dict): The initial game state from the server.
        """
        self.id = state["hero"]["id"]
        self.state = state
        self.start()

    def _move(self, state):
        """Internal wrapper for the move method.

        Args:
            state (dict): The current game state from the server.

        Returns:
            str: The direction to move ('North', 'South', 'East', 'West', 'Stay').
        """
        self.state = state
        return self.move()

    def _end(self):
        """Internal wrapper for the end method."""
        self.end()

    def start(self):
        """Called when the game starts.

        Override this method to initialize your bot's state.
        """
        pass

    def move(self):
        """Called when the game requests a move from this bot.

        Override this method to implement your bot's decision logic.

        Returns:
            str: The direction to move ('North', 'South', 'East', 'West', 'Stay').
        """
        pass

    def end(self):
        """Called after the game finishes.

        Override this method to perform cleanup or logging.
        """
        pass
