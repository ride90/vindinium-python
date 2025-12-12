"""Game model representing the complete game state.

This module provides the Game class which holds all information about
the current game state including the map, heroes, mines, and taverns.
"""

import vindinium as vin
from vindinium.models import Hero, Map, Tavern, Mine

__all__ = ["Game"]


class Game:
    """Represents a complete game state.

    A game object holds information about the game and is updated automatically
    by ``BaseBot``. It processes the raw JSON state into structured objects.

    Attributes:
        id (int): The unique game identifier.
        max_turns (int): Maximum turns of the game (each turn only a single hero moves).
        turn (int): Current turn number.
        map (vindinium.models.Map): The game map instance.
        heroes (list): List of Hero instances representing all players.
        mines (list): List of Mine instances on the map.
        taverns (list): List of Tavern instances on the map.
    """

    def __init__(self, state):
        """Initialize the game from a state dictionary.

        Args:
            state (dict): The state object from the server.
        """
        # Constants
        self.id = state["game"]["id"]
        self.max_turns = state["game"]["maxTurns"]

        # Variables
        self.turn = state["game"]["turn"]

        # Processed objects
        self.map = None
        self.heroes = []
        self.mines = []
        self.taverns = []

        # Process the state, creating the objects
        self.__processState(state)

    def update(self, state):
        """Update the game with new information from the server.

        This function does not re-create the objects, it just updates
        the current objects with new information.

        Args:
            state (dict): The state object from the server.
        """
        size = state["game"]["board"]["size"]
        tiles = state["game"]["board"]["tiles"]
        heroes = state["game"]["heroes"]

        self.turn = state["game"]["turn"]

        for hero, hero_state in zip(self.heroes, heroes):
            hero.crashed = hero_state["crashed"]
            hero.mine_count = hero_state["mineCount"]
            hero.gold = hero_state["gold"]
            hero.life = hero_state["life"]
            hero.last_dir = hero_state.get("lastDir")
            hero.x = hero_state["pos"]["y"]
            hero.y = hero_state["pos"]["x"]

        for mine in self.mines:
            char = tiles[mine.x * 2 + mine.y * 2 * size + 1]
            mine.owner = None if char == "-" else int(char)

    def __processState(self, state):
        """Process the raw state into structured objects.

        Parses the board tiles and creates Map, Mine, Tavern, and Hero objects.

        Args:
            state (dict): The state object from the server.
        """
        # helper variables
        board = state["game"]["board"]
        size = board["size"]
        tiles = board["tiles"]
        tiles = [tiles[i : i + 2] for i in range(0, len(tiles), 2)]

        # run through the map and update map, mines and taverns
        self.map = Map(size)
        for y in range(size):
            for x in range(size):
                tile = tiles[y * size + x]
                if tile == "##":
                    self.map[x, y] = vin.TILE_WALL
                elif tile == "[]":
                    self.map[x, y] = vin.TILE_TAVERN
                    self.taverns.append(Tavern(x, y))
                elif tile.startswith("$"):
                    self.map[x, y] = vin.TILE_MINE
                    self.mines.append(Mine(x, y))
                else:
                    self.map[x, y] = vin.TILE_EMPTY

        # create heroes
        for hero in state["game"]["heroes"]:
            pos = hero["spawnPos"]
            self.map[pos["y"], pos["x"]] = vin.TILE_SPAWN
            self.heroes.append(Hero(hero))

    def __str__(self):
        """Return a pretty string representation of the map.

        Returns:
            str: ASCII art representation of the game map.
        """
        s = " "
        s += "-" * (self.map.size) + "\n"
        for y in range(self.map.size):
            s += "|"
            for x in range(self.map.size):
                tile = self.map[x, y]
                hero = [h for h in self.heroes if h.x == x and h.y == y]

                if tile == vin.TILE_WALL:
                    s += "."
                elif any(hero):
                    s += str(hero[0].id)
                elif tile == vin.TILE_SPAWN:
                    s += "s"
                elif tile == vin.TILE_MINE:
                    s += "M"
                elif tile == vin.TILE_TAVERN:
                    s += "T"
                else:
                    s += " "
            s += "|\n"
        s += " " + "-" * (self.map.size)
        return s
