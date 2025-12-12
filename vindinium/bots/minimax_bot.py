"""Minimax bot implementation using game tree search.

This module provides a bot that uses the minimax algorithm to
evaluate possible future game states and select optimal moves.
"""

import random
import vindinium as vin
from vindinium.bots import BaseBot
from vindinium.ai import Minimax

__all__ = ["MinimaxBot"]


class MinimaxBot(BaseBot):
    """Bot that uses minimax algorithm for decision making.

    This bot uses game tree search with the minimax algorithm to
    evaluate possible future states and select the best move.

    Attributes:
        search (Minimax): The minimax search instance with depth 8.
    """

    search = None

    def _do_start(self):
        """Initialize the minimax search algorithm.

        Called when the game starts to set up the minimax search
        with a depth of 8 plies.
        """
        self.search = Minimax(self.game, 8)

    def _do_move(self):
        """Use minimax to find the best move.

        Returns:
            str: The best move according to minimax evaluation.
        """
        moves = self.search.find()
        return moves[0]
