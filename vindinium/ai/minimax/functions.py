"""Helper functions for minimax algorithm.

This module provides default implementations of functions used by
the minimax algorithm for terminal state checking, state generation,
evaluation, and sorting.
"""

import random

MOVES = {
    # 'Stay'  : (0, 0),
    'North': (0, -1),
    'West': (-1, 0),
    'South': (0, 1),
    'East': (1, 0),
}


def terminal(minimax, game, state):
    """Check if a given state is terminal.

    Args:
        minimax (Minimax): The minimax instance.
        game (Game): The game instance.
        state (State): The state to check.

    Returns:
        bool: True if the state is terminal (game over).
    """
    return state.turn >= game.max_turns * 4


def generate(minimax, game, state):
    """Generate the children states of a given state.

    Args:
        minimax (Minimax): The minimax instance.
        game (Game): The game instance.
        state (State): The current state.

    Returns:
        list: List of child states.
    """
    id = state.turn % 4
    hero = state.heroes[id]
    x = hero['x']
    y = hero['y']
    size = game.map.size

    result = []
    for move, dir in MOVES.items():
        x_, y_ = x + dir[0], y + dir[1]
        if not (-1 < x_ < size and -1 < y_ < size):
            continue
        s = state.clone()
        s.simulate(move)
        result.append(s)
    return result


def evaluate(minimax, game, state):
    """Evaluate the value of a state.

    Args:
        minimax (Minimax): The minimax instance.
        game (Game): The game instance.
        state (State): The state to evaluate.

    Returns:
        float: The evaluated value of the state.
    """
    id = (game.turn % 4) + 1
    hero = state.heroes[id - 1]

    value = 0
    distance = None
    for (x, y), owner in state.mines.items():
        mod = 1 if (owner == id) else -1

        # mine ownership
        value += 0 if owner is None else mod * 1000

        # mine distance
        if mod != 1:
            d = abs(hero['x'] - x) + abs(hero['y'] - y)
            if distance is None or d < distance:
                distance = d

    value -= distance or 0

    # life
    value += round(hero['life'] / 10)

    return value


def sort(minimax, game, states):
    """Sort the state children.

    Args:
        minimax (Minimax): The minimax instance.
        game (Game): The game instance.
        states (list): List of states to sort.

    Returns:
        list: Sorted list of states.
    """
    return reversed(states)