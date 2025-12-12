"""Aggressive bot implementation that attacks other heroes.

This module provides a bot that focuses on attacking other heroes,
particularly those with the most mines.
"""

import random
import vindinium as vin
from vindinium.bots import BaseBot
from vindinium.ai import AStar

__all__ = ["AggressiveBot"]


class AggressiveBot(BaseBot):
    """Bot that aggressively attacks other heroes.

    This bot targets the hero with the most mines and attempts to
    attack them. It visits taverns when health is low to stay alive.

    Attributes:
        search (AStar): The A* pathfinding instance for navigation.
        target (Hero): The current target hero to attack.
    """

    search = None

    def start(self):
        """Initialize the A* pathfinding algorithm and target.

        Called when the game starts to set up the pathfinding system.
        """
        self.search = AStar(self.game.map)
        self.target = None

    def move(self):
        """Decide the next move based on health and target proximity.

        Returns:
            str: The direction to move ('North', 'South', 'East', 'West', 'Stay').
        """
        print(self.hero.life)
        self.target = self._get_best_target()
        distance = vin.utils.distance_manhattan(
            self.hero.x, self.hero.y, self.target.x, self.target.y
        )
        in_spawn = (
            self.target.x == self.target.spawn_x
            and self.target.y == self.target.spawn_y
        )

        if self.hero.life <= 40 and self.hero.gold > 2:
            return self._go_to_nearest_tavern()

        elif distance < 5 and not in_spawn:
            return self._go_to(self.target.x, self.target.y)

        elif self.hero.life <= 60 and self.hero.gold > 2:
            return self._go_to_nearest_tavern()

        else:
            return self._go_to(self.target.x, self.target.y)

    def _get_best_target(self):
        """Select the best hero to target.

        Targets the hero with the most mines.

        Returns:
            Hero: The hero with the most mines.
        """
        target = None
        for hero in self.game.heroes:
            if hero.id == self.id:
                continue

            if target is None or hero.mine_count > target.mine_count:
                target = hero

        return target

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
        return random.choice(["Stay", "North", "West", "East", "South"])
