"""CharmingMole bot implementation that focuses on being a charming mole."""

import random
import vindinium as vin
from vindinium.bots import BaseBot
from vindinium.ai import AStar

__all__ = ["CharmingMoleBot"]


class CharmingMoleBot(BaseBot):
    """
    CharmingMole bot implementation that focuses on being a charming mole.

    Attributes:
        search (AStar): The A* pathfinding instance for navigation.
        FRIENDLY_FIRE_AVOIDANCE (bool): Class attribute to enable/disable friendly
            fire avoidance. When enabled, the bot will not attack or steal mines
            from heroes with the same name. Defaults to True.
        friendly_name (str): The name to use for identifying friendly bots.
            If None, uses the bot's own hero name. Can be set to a custom value
            to coordinate with bots using different display names.
    """

    # Configuration: Enable/disable friendly fire avoidance
    FRIENDLY_FIRE_AVOIDANCE = True

    # Custom friendly name (None = use own hero name)
    friendly_name = None

    search = None
    _friendly_hero_ids = None  # Cache of friendly hero IDs

    def _do_start(self):
        """Initialize the A* pathfinding algorithm and friendly hero detection.

        Called when the game starts to set up the pathfinding system
        and identify friendly heroes (same name) for friendly fire avoidance.
        """
        self.search = AStar(self.game.map)
        self._update_friendly_heroes()

    def _update_friendly_heroes(self):
        """Identify and cache friendly hero IDs based on name matching.

        Friendly heroes are those with the same name as our hero (or the
        configured friendly_name). This is useful in tournaments where
        multiple instances of the same bot may be matched together.

        Note: This should be called at game start. Hero names don't change
        during a game, so we only need to compute this once.
        """
        if not self.FRIENDLY_FIRE_AVOIDANCE:
            self._friendly_hero_ids = set()
            return

        # Determine the name to match against
        match_name = self.friendly_name if self.friendly_name else self.hero.name

        # Find all heroes with the same name (excluding ourselves)
        self._friendly_hero_ids = set()
        for hero in self.game.heroes:
            if hero.id != self.hero.id and hero.name == match_name:
                self._friendly_hero_ids.add(hero.id)

    def _is_friendly_hero(self, hero_id):
        """Check if a hero is friendly (same team/name).

        Args:
            hero_id (int): The hero ID to check.

        Returns:
            bool: True if the hero is friendly and should not be attacked.
        """
        if not self.FRIENDLY_FIRE_AVOIDANCE:
            return False
        if self._friendly_hero_ids is None:
            return False
        return hero_id in self._friendly_hero_ids

    def _is_friendly_mine(self, mine):
        """Check if a mine is owned by a friendly hero.

        Args:
            mine: The mine object to check.

        Returns:
            bool: True if the mine is owned by a friendly hero.
        """
        if mine.owner is None:
            return False
        return self._is_friendly_hero(mine.owner)

    def _get_position_after_move(self, command):
        """Calculate the position after executing a move command.

        Args:
            command (str): The move command ('North', 'South', 'East', 'West', 'Stay').

        Returns:
            tuple: (x, y) coordinates after the move.
        """
        x, y = self.hero.x, self.hero.y
        if command == "North":
            return (x, y - 1)
        elif command == "South":
            return (x, y + 1)
        elif command == "West":
            return (x - 1, y)
        elif command == "East":
            return (x + 1, y)
        return (x, y)  # Stay

    def _would_hit_friendly(self, command):
        """Check if executing a move would result in attacking a friendly hero.

        This method implements smart deadlock prevention:
        1. Critical HP (<25): Always move
        2. Normal HP: Use hero ID priority - lower ID yields to higher ID

        This prevents symmetric deadlocks (e.g., two heroes wanting to swap positions)
        and ensures heroes can reach taverns when critically low on health.

        Performance: This check is O(3) - iterates over max 3 other heroes with
        O(1) set lookup for friendly check. Total overhead is ~0.001ms, negligible.
        Safe to call every turn.

        Args:
            command (str): The move command to check.

        Returns:
            bool: True if we should yield (stay) to avoid hitting a friendly hero.
                  False if we should proceed with the move.
        """
        if not self.FRIENDLY_FIRE_AVOIDANCE:
            return False

        next_x, next_y = self._get_position_after_move(command)

        # Check if any friendly hero is at the target position
        for hero in self.game.heroes:
            if hero.id == self.hero.id:
                continue
            if self._is_friendly_hero(hero.id):
                if hero.x == next_x and hero.y == next_y:
                    # Critical HP exception: survival trumps friendly fire avoidance
                    # If we're about to die, we must move even if it means hitting a friendly
                    if self.hero.life < 25:
                        return False  # Don't yield, move anyway

                    # Deadlock prevention: use hero ID priority
                    # Lower ID yields to higher ID, ensuring one always moves
                    if self.hero.id < hero.id:
                        return True   # We yield (stay)
                    else:
                        return False  # They should yield (we move)
        return False

    def _do_move(self):
        """Decide the next move based on health and mine ownership.

        Returns:
            str: The direction to move ('North', 'South', 'East', 'West', 'Stay').
        """
        if self.hero.life < 50 and self.hero.gold > 2:
            command = self._go_to_nearest_tavern()
        else:
            command = self._go_to_nearest_mine()

        # Friendly fire avoidance: don't walk into friendly heroes
        # Performance: O(3) check with O(1) set lookup
        if self._would_hit_friendly(command):
            return "Stay"

        return command

    def _go_to_nearest_mine(self):
        """Navigate to the nearest mine not owned by this bot or friendly bots.

        When FRIENDLY_FIRE_AVOIDANCE is enabled, this method will skip mines
        owned by heroes with the same name (friendly bots), treating them
        as if they were our own mines.

        Returns:
            str: The direction to move toward the nearest uncaptured mine,
                or a random move if no path is found.
        """
        x = self.hero.x
        y = self.hero.y

        # Order mines by distance
        mines = vin.utils.order_by_distance(x, y, self.game.mines)
        for mine in mines:
            # Skip mines owned by this hero
            if mine.owner == self.hero.id:
                continue

            # Skip mines owned by friendly heroes (same name)
            if self._is_friendly_mine(mine):
                continue

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
        return random.choice(["Stay", "North", "West", "East", "South"])
