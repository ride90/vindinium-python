"""Raw bot implementation that provides the base interface for all bots.

This module defines the RawBot class which serves as the minimal bot
interface without any state processing.
"""

__all__ = ["RawBot"]


class RawBot:
    """Raw bot that does not process the game state.

    This is the most basic bot interface. The Client calls the public
    start(), move(), and end() methods. Subclasses should override the
    _do_start(), _do_move(), and _do_end() methods to implement bot logic.

    Override the following methods to create your bot:
    - _do_start(): called when the game starts.
    - _do_move(): called when the game requests a move from this bot.
    - _do_end(): called after the game finishes.

    Attributes:
        id (int): The bot's unique identifier.
        state (dict): The unprocessed state dictionary from the server.
    """

    id = None
    state = None

    def start(self, state):
        """Called by the Client when the game starts.

        Sets up the bot's ID and state, then calls the user-defined _do_start().

        Args:
            state (dict): The initial game state from the server.
        """
        self.id = state["hero"]["id"]
        self.state = state
        self._do_start()

    def move(self, state):
        """Called by the Client when a move is requested.

        Updates the state, then calls the user-defined _do_move().

        Args:
            state (dict): The current game state from the server.

        Returns:
            str: The direction to move ('North', 'South', 'East', 'West', 'Stay').
        """
        self.state = state
        return self._do_move()

    def end(self):
        """Called by the Client when the game finishes.

        Calls the user-defined _do_end() for cleanup.
        """
        self._do_end()

    def _do_start(self):
        """Override this method to initialize your bot's state.

        Called when the game starts, after id and state are set.
        """
        pass

    def _do_move(self):
        """Override this method to implement your bot's decision logic.

        Called each turn to decide the next move.

        Returns:
            str: The direction to move ('North', 'South', 'East', 'West', 'Stay').
        """
        pass

    def _do_end(self):
        """Override this method to perform cleanup or logging.

        Called after the game finishes.
        """
        pass
