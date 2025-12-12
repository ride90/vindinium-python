"""Hero model representing a player in the game.

This module provides the Hero class which represents a player/bot
in the Vindinium game with all their attributes and state.
"""

__all__ = ["Hero"]


class Hero:
    """Represents a hero (player/bot) in the game.

    Attributes:
        id (int): The hero's unique identifier.
        name (str): The bot's name.
        user_id (str): The bot's user ID (None in training mode).
        elo (int): The bot's ELO rating (None in training mode).
        crashed (bool): True if the bot has been disconnected.
        mine_count (int): The number of mines this hero owns.
        gold (int): Current amount of gold earned by this hero.
        life (int): Current hero's life points.
        last_dir (str): Last bot movement direction (may be None).
        x (int): The bot's position on the X axis.
        y (int): The bot's position on the Y axis.
        spawn_x (int): The bot's spawn position on the X axis.
        spawn_y (int): The bot's spawn position on the Y axis.
    """

    def __init__(self, hero):
        """Initialize a hero from server data.

        Args:
            hero (dict): The hero data dictionary from the server.
        """
        # Constants
        self.id = hero["id"]
        self.name = hero["name"]
        self.user_id = hero.get("userId")
        self.elo = hero.get("elo")

        # Variables
        self.crashed = hero["crashed"]
        self.mine_count = hero["mineCount"]
        self.gold = hero["gold"]
        self.life = hero["life"]
        self.last_dir = hero.get("lastDir")
        self.x = hero["pos"]["y"]
        self.y = hero["pos"]["x"]
        self.spawn_x = hero["spawnPos"]["y"]
        self.spawn_y = hero["spawnPos"]["x"]
