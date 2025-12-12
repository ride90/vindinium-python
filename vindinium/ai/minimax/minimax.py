"""Minimax algorithm implementation with alpha-beta pruning.

This module provides a negamax algorithm with alpha-beta pruning
for game tree search in Vindinium.
"""

import random
import vindinium
from .state import State
from . import functions as f

__all__ = ['Minimax']


class Minimax:
    """Minimax algorithm with alpha-beta pruning.

    This class implements a negamax algorithm with alpha-beta pruning.
    You can pass specific functions to this class to override the
    default behavior. See ``vindinium.ai.minimax.functions`` for the
    default implementation of these functions.

    Attributes:
        game (vindinium.models.Game): The game instance.
        max_depth (int): Maximum depth of the search tree.
    """

    def __init__(
        self,
        game,
        max_depth=5,
        f_terminal=f.terminal,
        f_evaluate=f.evaluate,
        f_generate=f.generate,
        f_sort=f.sort,
    ):
        """Initialize the minimax algorithm.

        Args:
            game (vindinium.models.Game): The game instance.
            max_depth (int): Maximum depth of the algorithm. Defaults to 5.
            f_terminal (function): Function to verify if a state is terminal.
            f_evaluate (function): Function to evaluate the value of a state.
            f_generate (function): Function to generate a state's children.
            f_sort (function): Function to sort the state children list.
        """
        self.game = game
        self.max_depth = max_depth
        self._f_terminal = f_terminal
        self._f_evaluate = f_evaluate
        self._f_generate = f_generate
        self._f_sort = f_sort

    def find(self):
        """Find the best move using minimax search.

        Returns:
            list: A list of next expected commands (from your bot and the enemies).
        """
        state = State(self.game)
        value, state = self._minimax(state, self.max_depth)
        result = []

        while state.last_move:
            result.append(state.last_move)
            state = state.parent

        return result

    def _minimax(
        self, state, depth, alpha=-float('inf'), beta=float('inf'), color=0
    ):
        """Negamax function with alpha-beta pruning.

        Args:
            state (State): The current game state.
            depth (int): Remaining search depth.
            alpha (float): Alpha value for pruning.
            beta (float): Beta value for pruning.
            color (int): Current player color/turn.

        Returns:
            tuple: (best_value, best_state) tuple.
        """
        state._value = 0
        game = self.game
        mod = 1 if color % 4 == 0 else -1

        if depth == 0 or self._f_terminal(self, game, state):
            return (mod * self._f_evaluate(self, game, state), state)

        best_value = -float('inf')
        best_state = None
        next_states = self._f_generate(self, game, state)
        next_states = self._f_sort(self, game, next_states)

        for next_state in next_states:
            value, state_ = self._minimax(
                next_state, depth - 1, -beta, -alpha, color + 1
            )
            if color % 4 == 0 or (color + 1) % 4 == 0:
                value = -value

            if (value > best_value) or (
                value == best_state and random.random() < 0.3
            ):
                best_state = next_state
                best_value = value

            alpha = max(alpha, value)
            if alpha >= beta:
                break

        return (best_value, best_state)
