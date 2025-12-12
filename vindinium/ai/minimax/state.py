"""State representation for minimax algorithm.

This module provides the State class which represents a game state
for use in minimax tree search.
"""

from . import simulation


class State:
    """Represents a game state for minimax search.

    This class can be initialized from a Game instance or cloned from
    another State instance.

    Attributes:
        last_move (str): The last move that led to this state.
        parent (State): The parent state.
        turn (int): The current turn number.
        heroes (list): List of hero dictionaries.
        mines (dict): Dictionary mapping (x, y) positions to owner IDs.
    """

    def __init__(self, game=None):
        """Initialize a state from a game or clone from another state.

        Args:
            game (Game or State): Either a Game instance to create initial state,
                or a State instance to clone.
        """
        if isinstance(game, State):
            self.last_move = game.last_move
            self.parent = game
            self._game = game._game
            self.turn = game.turn
            self.heroes = [h.copy() for h in game.heroes]
            self.mines = game.mines.copy()
        else:
            self.last_move = None
            self.parent = None
            self._game = game
            self.turn = game.turn
            self.heroes = []
            self.mines = {}
            self._populate()

    def _populate(self):
        """Populate the state from the game instance."""
        for hero in self._game.heroes:
            h = dict(
                x=hero.x,
                y=hero.y,
                gold=hero.gold,
                mine_count=hero.mine_count,
                life=hero.life,
                spawn_x=hero.spawn_x,
                spawn_y=hero.spawn_y,
            )
            self.heroes.append(h)

        for mine in self._game.mines:
            self.mines[(mine.x, mine.y)] = mine.owner

    def clone(self):
        """Create a copy of this state.

        Returns:
            State: A new State instance cloned from this one.
        """
        return State(self)

    def simulate(self, move):
        """Simulate a move and update the state.

        Args:
            move (str): The move to simulate ('North', 'South', 'East', 'West', 'Stay').
        """
        self.last_move = move
        simulation.simulate(self, move)

    def __str__(self):
        """Return a string representation of the state.

        Returns:
            str: A formatted string showing heroes and their stats.
        """
        s = "Heroes (turn %d/%s): \n" % (self.turn, self.last_move or "")
        for i, hero in enumerate(self.heroes):
            s += "    %d: (%d, %d, l%03d, $%d, m%d)\n" % (
                i,
                hero["x"],
                hero["y"],
                hero["life"],
                hero["gold"],
                hero["mine_count"],
            )

        return s
