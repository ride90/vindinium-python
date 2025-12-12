"""Miner bot implementation that focuses on capturing mines.

This module provides a bot that prioritizes capturing mines and
visiting taverns when health is low.
"""

import random
import vindinium as vin
from vindinium.bots import BaseBot
from vindinium.ai import AStar

__all__ = ['MinerBot']


class MinerBot(BaseBot):
    """Bot that focuses on capturing mines.

    This bot uses A* pathfinding to navigate to the nearest uncaptured
    mine. When health drops below 50 and the bot has enough gold, it
    visits a tavern to heal.

    Attributes:
        search (AStar): The A* pathfinding instance for navigation.
    """

    search = None

    def start(self):
        """Initialize the A* pathfinding algorithm.

        Called when the game starts to set up the pathfinding system.
        """
        self.search = AStar(self.game.map)

    def move(self):
        """Decide the next move based on health and mine ownership.

        Returns:
            str: The direction to move ('North', 'South', 'East', 'West', 'Stay').
        """
        if self.hero.life < 50 and self.hero.gold > 2:
            return self._go_to_nearest_tavern()
        else:
            return self._go_to_nearest_mine()

    def _go_to_nearest_mine(self):
        """Navigate to the nearest mine not owned by this bot.

        Returns:
            str: The direction to move toward the nearest uncaptured mine,
                or a random move if no path is found.
        """
        x = self.hero.x
        y = self.hero.y

        # Order mines by distance
        mines = vin.utils.order_by_distance(x, y, self.game.mines)
        for mine in mines:
            # Grab nearest mine that is not owned by this hero
            if mine.owner != self.hero.id:
                command = self._go_to(mine.x, mine.y)

                if command:
                    return command

        return self._random()

    def _go_to_nearest_tavern(self):
        """Navigate to the nearest tavern to heal.

        Returns:
            str: The direction to move toward the nearest tavern,
                or a random move if no path is found.
        """
        x = self.hero.x
        y = self.hero.y

        # Order taverns by distance
        taverns = vin.utils.order_by_distance(x, y, self.game.taverns)
        for tavern in taverns:
            command = self._go_to(tavern.x, tavern.y)

            if command:
                return command

        return self._random()

    def _go_to(self, x_, y_):
        """Calculate path to target and return the next move.

        Args:
            x_ (int): Target x coordinate.
            y_ (int): Target y coordinate.

        Returns:
            str: The direction to move toward the target, or None if no path exists.
        """
        x = self.hero.x
        y = self.hero.y

        # Compute path to the target
        path = self.search.find(x, y, x_, y_)

        # Send command to follow that path
        if path is None:
            return None

        if len(path) > 0:
            x_, y_ = path[0]

        return vin.utils.path_to_command(x, y, x_, y_)

    def _random(self):
        """Return a random move.

        Returns:
            str: A randomly chosen direction.
        """
        return random.choice(['Stay', 'North', 'West', 'East', 'South'])