"""CharmingMole bot - A survival-focused mining bot with configurable aggression.

This bot balances survival with mine acquisition using phase-aware decision making.
It can be tuned from very cautious (high survival, fewer mines) to aggressive
(more mines, more deaths) using class attributes.
"""

import random
import vindinium as vin
from vindinium.bots import BaseBot
from vindinium.ai import AStar

__all__ = ["CharmingMoleBotV1Minimax"]


class CharmingMoleBotV1Minimax(BaseBot):
    """A survival-focused mining bot with configurable aggression levels.

    ALGORITHM OVERVIEW
    ==================
    The bot uses a priority-based decision system, evaluated each turn:

    Priority 1: OPPORTUNISTIC HEALING
        If next to a tavern AND HP < NEARBY_TAVERN_HEAL_THRESHOLD AND gold >= 2:
        → Heal (almost free, 1 turn for +50 HP)

    Priority 2: FLEE FROM CRITICAL DANGER
        If danger_level >= FLEE_DANGER_THRESHOLD (enemy adjacent + would kill us):
        → Try to flee away from enemy
        → If can't flee, go to nearest tavern

    Priority 3: GO TO TAVERN (phase-aware)
        If HP < dynamic_threshold AND gold >= 2:
        → Go to nearest tavern
        Dynamic threshold = HP_THRESHOLD_{phase} + DANGER_HP_MODIFIER (if enemies near)

    Priority 4: OPPORTUNISTIC KILL (if OPPORTUNISTIC_KILLS_ENABLED)
        → Find weak enemies within OPPORTUNISTIC_KILL_MAX_DISTANCE
        → Target must have HP <= OPPORTUNISTIC_KILL_ENEMY_HP_THRESHOLD
        → We must have HP advantage >= OPPORTUNISTIC_KILL_HP_ADVANTAGE
        → Target must have >= OPPORTUNISTIC_KILL_MIN_ENEMY_MINES mines
        → We must have >= OPPORTUNISTIC_KILL_MIN_OUR_HP HP
        → Prioritize by: mines owned (desc), then low HP, then close distance

    Priority 5: MINE (with value calculation)
        → Go to nearest mine that passes value check:
          - Must hold for >= MIN_TURNS_TO_HOLD_MINE turns
          - Must have enough HP for journey + capture
        → Skip mines owned by self or friendly bots

    Safety Layer: Before executing move, check if it would walk into danger.
        If DANGER_CHECK_ENABLED and move is dangerous:
        → Try to find safe alternative
        → If ALLOW_STAY_AS_FALLBACK, may return "Stay"

    Friendly Fire: If FRIENDLY_FIRE_AVOIDANCE enabled:
        → Don't attack heroes with same name
        → Don't steal their mines
        → Use hero ID priority to break deadlocks

    Respawn Detection: If RESPAWN_DETECTION_ENABLED:
        → Detect death (HP <= 20 → 100)
        → Clear cached destination (don't path to old target)
        → Play aggressively for RESPAWN_AGGRESSIVE_TURNS turns
        → Use opening-phase HP thresholds during recovery

    GAME PHASES
    ===========
    - Opening (0% - PHASE_OPENING_END): Aggressive mining, low HP threshold
    - Mid (PHASE_OPENING_END - PHASE_MID_END): Balanced play
    - End (PHASE_MID_END - 100%): Conservative, protect lead
    - Post-Respawn: Temporary "opening" phase for RESPAWN_AGGRESSIVE_TURNS turns

    CONFIGURATION
    =============
    All behavior can be tuned via class attributes. Create a subclass to customize:

    ```python
    class AggressiveMole(CharmingMoleBotV1Minimax):
        HP_THRESHOLD_OPENING = 25      # Heal less often
        DANGER_HP_MODIFIER = 10        # Less scared of enemies
        MIN_TURNS_TO_HOLD_MINE = 2     # Take more mines
        FLEE_DANGER_THRESHOLD = 4      # Flee less often
        DANGER_CHECK_ENABLED = False   # Ignore danger, just mine
    ```

    CONFIGURABLE ATTRIBUTES
    =======================

    Friendly Fire Settings:
        FRIENDLY_FIRE_AVOIDANCE (bool): Don't attack same-name heroes. Default: True
        friendly_name (str): Name to match for friendlies. Default: None (use own name)

    Healing Thresholds:
        NEARBY_TAVERN_HEAL_THRESHOLD (int): Heal if next to tavern and HP below this.
            Default: 80. Range: 1-99. Higher = heal more often when convenient.

        HP_THRESHOLD_OPENING (int): HP threshold in opening phase. Default: 30
        HP_THRESHOLD_MID (int): HP threshold in mid phase. Default: 45
        HP_THRESHOLD_END (int): HP threshold in end phase. Default: 55
            Higher values = more conservative (heal more, mine less)

        DANGER_HP_MODIFIER (int): Added to HP threshold when enemies nearby.
            Default: 15. Range: 0-50. Higher = more scared of enemies.

    Game Phase Boundaries:
        PHASE_OPENING_END (float): End of opening phase. Default: 0.25 (25%)
        PHASE_MID_END (float): End of mid phase. Default: 0.85 (85%)

    # TODO: Adjust if rich and game phase.
    Mine Value Calculation:
        MIN_TURNS_TO_HOLD_MINE (int): Minimum turns to hold a mine for it to be
            worth taking. Default: 2. Range: 1-20.
            Lower = more aggressive (take distant mines late game)
            Higher = more conservative (skip mines that won't pay off)

    Danger/Fleeing Settings:
        FLEE_DANGER_THRESHOLD (int): Danger level at which to flee. Default: 3.
            Range: 1-4. Lower = flee more often. Higher = flee only when critical.
            Danger levels: 1=enemy nearby, 2=enemy close, 3=enemy adjacent, 4=certain death

        DANGER_CHECK_ENABLED (bool): Check if moves walk into danger. Default: True.
            Set False for more aggressive play (ignore enemies, just mine).

        DANGER_CHECK_HP_THRESHOLD (int): Only check danger if HP below this.
            Default: 50. Set to 100 to always check, 0 to never check.

        ALLOW_STAY_AS_FALLBACK (bool): Allow "Stay" when no safe move found.
            Default: False. If False, picks any non-dangerous move instead.

    Respawn Detection Settings:
        RESPAWN_DETECTION_ENABLED (bool): Enable respawn detection and strategy reset.
            Default: True. When enabled, bot detects death and resets strategy.

        RESPAWN_AGGRESSIVE_TURNS (int): Turns to play aggressively after respawn.
            Default: 10. During this period, uses opening-phase HP thresholds.
            Set to 0 to disable post-respawn aggressive behavior.

    Opportunistic Kills Settings:
        OPPORTUNISTIC_KILLS_ENABLED (bool): Enable hunting weak enemies.
            Default: True. When enabled, bot will chase and kill weak enemies.

        OPPORTUNISTIC_KILL_MAX_DISTANCE (int): Max distance to chase enemy.
            Default: 5. Lower = only attack nearby, Higher = chase further.

        OPPORTUNISTIC_KILL_ENEMY_HP_THRESHOLD (int): Enemy HP must be <= this.
            Default: 20. Only attack enemies with HP at or below this value.

        OPPORTUNISTIC_KILL_HP_ADVANTAGE (int): Required HP advantage over enemy.
            Default: 20. We attack if our_hp >= enemy_hp + this value.

        OPPORTUNISTIC_KILL_MIN_ENEMY_MINES (int): Min mines enemy must have.
            Default: 1. Set to 0 to attack any weak enemy.

        OPPORTUNISTIC_KILL_MIN_OUR_HP (int): Min HP we need to attempt kill.
            Default: 40. Don't chase if we're too weak ourselves.

    PERFORMANCE
    ===========
    - Pathfinding: O(V log V) per A* call, cached map
    - Enemy checks: O(E) where E = 3 enemies
    - Mine ordering: O(M log M) where M = number of mines
    - Overall: Fast enough for 15-second turn limit

    Attributes:
        search (AStar): The A* pathfinding instance for navigation.
    """

    # =========================================================================
    # FRIENDLY FIRE SETTINGS
    # =========================================================================

    # Enable/disable friendly fire avoidance (don't attack same-name heroes)
    FRIENDLY_FIRE_AVOIDANCE = True

    # Custom friendly name (None = use own hero name)
    friendly_name = None

    # =========================================================================
    # HEALING THRESHOLDS
    # =========================================================================

    # HP threshold for opportunistic healing at nearby tavern
    # If HP < this value and we're next to a tavern, heal immediately
    NEARBY_TAVERN_HEAL_THRESHOLD = 80

    # Phase-based HP thresholds for going to tavern
    HP_THRESHOLD_OPENING = 30  # Early game: aggressive, don't waste turns healing
    HP_THRESHOLD_MID = 45      # Mid game: balanced
    HP_THRESHOLD_END = 55      # Late game: conservative, protect mines

    # HP modifier when enemies are nearby (added to phase threshold)
    # Lower = more aggressive, Higher = more cautious
    DANGER_HP_MODIFIER = 15

    # =========================================================================
    # GAME PHASE BOUNDARIES
    # =========================================================================

    # Game phase boundaries (as percentage of max_turns)
    PHASE_OPENING_END = 0.25   # First 25% of game
    PHASE_MID_END = 0.85       # 25-85% is mid game, after 85% is endgame

    # =========================================================================
    # MINE VALUE CALCULATION
    # =========================================================================

    # Minimum turns to hold a mine for it to be worth taking
    # Lower = more aggressive (take mines even late game)
    # Higher = more conservative (skip mines that won't pay off)
    MIN_TURNS_TO_HOLD_MINE = 2. # Was 5

    # =========================================================================
    # DANGER / FLEEING SETTINGS
    # =========================================================================

    # Danger level threshold for fleeing (1-4, higher = flee less often)
    # 1 = flee if enemy within 3 tiles
    # 2 = flee if enemy within 2 tiles
    # 3 = flee if enemy adjacent (default)
    # 4 = flee only if certain death
    FLEE_DANGER_THRESHOLD = 4

    # Enable/disable danger checking before moves
    # Set False for aggressive play (ignore enemies, just mine)
    DANGER_CHECK_ENABLED = True

    # Only check danger if HP is below this threshold
    # Set to 100 to always check, 0 to never check
    DANGER_CHECK_HP_THRESHOLD = 15

    # Allow "Stay" as fallback when no safe move found
    # False = always move somewhere (more aggressive)
    # True = stay put if all moves seem dangerous (more cautious)
    ALLOW_STAY_AS_FALLBACK = False

    # =========================================================================
    # RESPAWN DETECTION SETTINGS
    # =========================================================================

    # Enable/disable respawn detection and strategy reset
    # When enabled, after dying the bot will:
    # 1. Clear any cached destination (don't path to old target)
    # 2. Play aggressively for RESPAWN_AGGRESSIVE_TURNS turns
    # 3. Prioritize nearby mines over distant ones
    RESPAWN_DETECTION_ENABLED = True

    # Number of turns to play aggressively after respawn
    # During this period, bot uses opening-phase HP thresholds
    # Set to 0 to disable aggressive post-respawn behavior
    RESPAWN_AGGRESSIVE_TURNS = 10

    # =========================================================================
    # OPPORTUNISTIC KILLS SETTINGS
    # =========================================================================

    # Enable/disable opportunistic kills
    # When enabled, bot will hunt weak enemies to steal their mines
    OPPORTUNISTIC_KILLS_ENABLED = True

    # Maximum distance to chase a weak enemy (Manhattan distance)
    # Lower = only attack very close enemies, Higher = chase further
    OPPORTUNISTIC_KILL_MAX_DISTANCE = 5

    # HP threshold for considering an enemy "weak" (absolute)
    # Enemy must have HP <= this value to be considered a target
    OPPORTUNISTIC_KILL_ENEMY_HP_THRESHOLD = 60

    # Minimum HP advantage we need over the enemy
    # We attack if: our_hp >= enemy_hp + this value
    OPPORTUNISTIC_KILL_HP_ADVANTAGE = 20

    # Minimum mines the enemy must have for us to bother chasing
    # Set to 0 to attack any weak enemy, higher to only chase mine-rich enemies
    OPPORTUNISTIC_KILL_MIN_ENEMY_MINES = 2

    # Minimum HP we need to attempt an opportunistic kill
    # Don't chase enemies if we're too weak ourselves
    OPPORTUNISTIC_KILL_MIN_OUR_HP = 40

    # =========================================================================
    # INTERNAL STATE
    # =========================================================================

    search = None
    _friendly_hero_ids = None  # Cache of friendly hero IDs
    _prev_life = None          # Track previous life for respawn detection
    _respawn_turn = None       # Turn when we last respawned
    _cached_destination = None # Cached destination (x, y) - cleared on respawn

    def _do_start(self):
        """Initialize the A* pathfinding algorithm and internal state.

        Called when the game starts to set up:
        - A* pathfinding system
        - Friendly hero detection
        - Respawn tracking state
        """
        self.search = AStar(self.game.map)
        self._update_friendly_heroes()
        # Initialize respawn tracking
        self._prev_life = self.hero.life
        self._respawn_turn = None
        self._cached_destination = None

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

    # =========================================================================
    # PHASE 1: SURVIVAL - Enemy Awareness & Danger Detection
    # =========================================================================

    def _get_enemies(self, include_crashed=False):
        """Get list of enemy heroes (non-friendly, non-self).

        Performance: O(3) iteration over other heroes. Negligible overhead.

        Args:
            include_crashed (bool): If True, include crashed/frozen enemies.
                Crashed enemies are disconnected bots that don't move or attack.
                Default is False (exclude crashed enemies).

        Returns:
            list: List of enemy Hero objects.
        """
        enemies = []
        for hero in self.game.heroes:
            if hero.id == self.hero.id:
                continue
            if self._is_friendly_hero(hero.id):
                continue
            # Skip crashed enemies unless explicitly requested
            if not include_crashed and hero.crashed:
                continue
            enemies.append(hero)
        return enemies

    def _get_nearby_enemies(self, max_distance=3):
        """Get enemies within a certain Manhattan distance.

        Performance: O(3) iteration with O(1) distance calc. Negligible overhead.

        Args:
            max_distance (int): Maximum Manhattan distance to consider "nearby".

        Returns:
            list: List of (enemy, distance) tuples, sorted by distance.
        """
        nearby = []
        for enemy in self._get_enemies():
            dist = vin.utils.distance_manhattan(
                self.hero.x, self.hero.y, enemy.x, enemy.y
            )
            if dist <= max_distance:
                nearby.append((enemy, dist))
        return sorted(nearby, key=lambda x: x[1])

    def _is_enemy_dangerous(self, enemy, distance):
        """Determine if an enemy is dangerous based on HP comparison and distance.

        Combat rules in Vindinium:
        - Each attack deals 20 damage
        - If HP <= 20, hero dies
        - Attacker (who moves into defender) attacks first

        Args:
            enemy: The enemy Hero object.
            distance (int): Manhattan distance to the enemy.

        Returns:
            bool: True if the enemy poses a significant threat.
        """
        # If enemy is next to us (distance=1), they can attack us next turn
        if distance == 1:
            # Enemy can kill us if our HP <= 20
            if self.hero.life <= 20:
                return True
            # Enemy is dangerous if they have more HP (they'd win a fight)
            if enemy.life >= self.hero.life:
                return True

        # If enemy is 2 tiles away, they could reach us next turn
        elif distance == 2:
            # Only dangerous if we're low HP and they're healthy
            if self.hero.life <= 40 and enemy.life > self.hero.life:
                return True

        return False

    def _get_danger_level(self):
        """Calculate overall danger level based on nearby enemies.

        Returns:
            tuple: (danger_level, closest_enemy) where:
                - danger_level: 0=safe, 1=caution, 2=danger, 3=critical
                - closest_enemy: The nearest enemy Hero or None
        """
        nearby = self._get_nearby_enemies(max_distance=3)

        if not nearby:
            return (0, None)  # Safe - no enemies nearby

        closest_enemy, closest_dist = nearby[0]

        # Critical: enemy next to us and we'd lose the fight
        if closest_dist == 1 and self._is_enemy_dangerous(closest_enemy, closest_dist):
            return (3, closest_enemy)

        # Danger: enemy very close (2 tiles) and dangerous
        if closest_dist == 2 and self._is_enemy_dangerous(closest_enemy, closest_dist):
            return (2, closest_enemy)

        # Caution: enemies nearby but not immediately threatening
        if closest_dist <= 3:
            return (1, closest_enemy)

        return (0, None)

    def _get_flee_direction(self, enemy):
        """Calculate the best direction to flee from an enemy.

        Tries to move away from the enemy. If blocked, tries perpendicular directions.

        Args:
            enemy: The enemy Hero to flee from.

        Returns:
            str: Direction to move ('North', 'South', 'East', 'West', 'Stay').
        """
        dx = self.hero.x - enemy.x  # Positive = we're to the right of enemy
        dy = self.hero.y - enemy.y  # Positive = we're below enemy

        # Prioritize moving away in the axis with greater distance
        flee_options = []

        if abs(dx) >= abs(dy):
            # Prioritize horizontal flee
            if dx > 0:
                flee_options = ["East", "North", "South", "West"]
            elif dx < 0:
                flee_options = ["West", "North", "South", "East"]
            else:
                flee_options = ["North", "South", "East", "West"]
        else:
            # Prioritize vertical flee
            if dy > 0:
                flee_options = ["South", "East", "West", "North"]
            elif dy < 0:
                flee_options = ["North", "East", "West", "South"]
            else:
                flee_options = ["East", "West", "North", "South"]

        # Try each flee direction, checking if it's safe
        for direction in flee_options:
            next_x, next_y = self._get_position_after_move(direction)

            # Check if the tile is walkable (not wall, not tavern, not mine)
            if not self._is_tile_walkable(next_x, next_y):
                continue

            # Check if we'd walk into another enemy
            if self._would_hit_enemy(direction):
                continue

            # Check friendly fire
            if self._would_hit_friendly(direction):
                continue

            return direction

        return "Stay"  # No safe flee direction

    def _is_tile_walkable(self, x, y):
        """Check if a tile can be walked on.

        Args:
            x (int): X coordinate.
            y (int): Y coordinate.

        Returns:
            bool: True if the tile is walkable (empty or spawn).
        """
        try:
            tile = self.game.map[x, y]
            # TILE_EMPTY = 0, TILE_SPAWN = 5 are walkable
            # TILE_WALL = 1, TILE_TAVERN = 3, TILE_MINE = 4 are not
            return tile in (0, 5)  # Empty or spawn point
        except (IndexError, KeyError):
            return False  # Out of bounds

    def _would_hit_enemy(self, command):
        """Check if a move would walk into an enemy hero.

        Args:
            command (str): The move command to check.

        Returns:
            bool: True if the move would walk into an enemy.
        """
        next_x, next_y = self._get_position_after_move(command)

        for enemy in self._get_enemies():
            if enemy.x == next_x and enemy.y == next_y:
                return True
        return False

    # =========================================================================
    # PHASE 3: OPPORTUNISTIC KILLS - Hunt Weak Enemies
    # =========================================================================

    def _is_enemy_worth_killing(self, enemy, distance):
        """Determine if an enemy is worth chasing for an opportunistic kill.

        An enemy is worth killing if:
        1. They're within OPPORTUNISTIC_KILL_MAX_DISTANCE
        2. They're weak (HP <= OPPORTUNISTIC_KILL_ENEMY_HP_THRESHOLD)
        3. We have HP advantage (our_hp >= enemy_hp + OPPORTUNISTIC_KILL_HP_ADVANTAGE)
        4. They have enough mines (>= OPPORTUNISTIC_KILL_MIN_ENEMY_MINES)
        5. We have enough HP ourselves (>= OPPORTUNISTIC_KILL_MIN_OUR_HP)

        Args:
            enemy: The enemy Hero to evaluate.
            distance (int): Manhattan distance to the enemy.

        Returns:
            bool: True if the enemy is worth killing.
        """
        # Check distance
        if distance > self.OPPORTUNISTIC_KILL_MAX_DISTANCE:
            return False

        # Check if we have enough HP
        if self.hero.life < self.OPPORTUNISTIC_KILL_MIN_OUR_HP:
            return False

        # Check if enemy is weak enough (absolute threshold)
        if enemy.mine_count <= 1:
            heuristics_modifier = 1
        else:
            heuristics_modifier = enemy.mine_count / 2
        heuristics_threshold = heuristics_modifier * self.OPPORTUNISTIC_KILL_ENEMY_HP_THRESHOLD
        if enemy.life > heuristics_threshold:
            return False

        # Check HP advantage
        if self.hero.life < enemy.life + self.OPPORTUNISTIC_KILL_HP_ADVANTAGE:
            return False

        # Check if enemy has enough mines to be worth chasing
        if enemy.mine_count < self.OPPORTUNISTIC_KILL_MIN_ENEMY_MINES:
            return False

        # Don't attack friendly bots
        if self.FRIENDLY_FIRE_AVOIDANCE and enemy.id in self._friendly_hero_ids:
            return False

        return True

    def _find_opportunistic_kill_target(self):
        """Find the best enemy to hunt for an opportunistic kill.

        Searches for weak enemies within range and returns the most valuable target.
        Value is determined by: mines owned, then HP (lower is better), then distance.

        Returns:
            tuple: (enemy, distance) of best target, or (None, None) if no target.
        """
        if not self.OPPORTUNISTIC_KILLS_ENABLED:
            return (None, None)

        candidates = []

        for enemy in self._get_enemies():
            distance = vin.utils.distance_manhattan(
                self.hero.x, self.hero.y, enemy.x, enemy.y
            )

            if self._is_enemy_worth_killing(enemy, distance):
                # Score: prioritize by mines (desc), then low HP, then close distance
                score = (enemy.mine_count, -enemy.life, -distance)
                candidates.append((enemy, distance, score))

        if not candidates:
            return (None, None)

        # Sort by score (highest first)
        candidates.sort(key=lambda x: x[2], reverse=True)
        best = candidates[0]
        return (best[0], best[1])

    def _go_to_enemy(self, enemy):
        """Navigate toward an enemy hero to attack them.

        Uses A* pathfinding to find the path to the enemy's position.

        Args:
            enemy: The enemy Hero to move toward.

        Returns:
            str: Direction to move ('North', 'South', 'East', 'West', 'Stay').
        """
        x = self.hero.x
        y = self.hero.y

        # Compute path to the enemy
        path = self.search.find(x, y, enemy.x, enemy.y)

        if path is None:
            return "Stay"

        if len(path) > 0:
            next_x, next_y = path[0]
            return vin.utils.path_to_command(x, y, next_x, next_y)

        return "Stay"

    # =========================================================================
    # PHASE 1: SURVIVAL - Nearby Tavern Optimization
    # =========================================================================

    def _get_nearby_tavern(self):
        """Find a tavern next to the hero's current position (1 tile away).

        Performance: O(T) where T is number of taverns (typically 4-8).
        With distance check, effectively O(1) per tavern.

        Returns:
            Tavern: A neighboring tavern, or None if no tavern is next to us.
        """
        for tavern in self.game.taverns:
            dist = vin.utils.distance_manhattan(
                self.hero.x, self.hero.y, tavern.x, tavern.y
            )
            if dist == 1:
                return tavern
        return None

    def _move_to_nearby_tavern(self, tavern):
        """Get the move command to step into a neighboring tavern.

        Args:
            tavern: The neighboring Tavern object.

        Returns:
            str: Direction to move to reach the tavern.
        """
        return vin.utils.path_to_command(
            self.hero.x, self.hero.y, tavern.x, tavern.y
        )

    def _should_heal_at_nearby_tavern(self):
        """Determine if we should heal at a neighboring tavern.

        Heals if:
        - There's a tavern next to us (1 tile away)
        - We have enough gold (>= 2)
        - HP is below NEARBY_TAVERN_HEAL_THRESHOLD, or < 100 if enemies nearby

        Returns:
            tuple: (should_heal, tavern) or (False, None)
        """
        if self.hero.gold < 2:
            return (False, None)

        tavern = self._get_nearby_tavern()
        if tavern is None:
            return (False, None)

        danger_level, _ = self._get_danger_level()

        # If in danger, heal more aggressively
        if danger_level >= 2 and self.hero.life < 100:
            return (True, tavern)

        # Normal case: heal if HP < threshold (configurable via class attribute)
        if self.hero.life < self.NEARBY_TAVERN_HEAL_THRESHOLD:
            return (True, tavern)

        return (False, None)

    # =========================================================================
    # PHASE 2: STOP WASTING - Game Phase Awareness & Mine Value
    # =========================================================================

    def _check_and_handle_respawn(self):
        """Check if we just respawned and handle strategy reset.

        Respawn is detected when:
        - Previous life was <= 20 (we were about to die or dead)
        - Current life is 100 (we respawned with full HP)

        When respawn is detected (and RESPAWN_DETECTION_ENABLED):
        1. Record the respawn turn for aggressive phase tracking
        2. Clear cached destination (don't path to old target)

        Returns:
            bool: True if we just respawned, False otherwise.
        """
        if not self.RESPAWN_DETECTION_ENABLED:
            return False

        # Detect respawn: previous life was very low, now at 100
        just_respawned = (
            self._prev_life is not None
            and self._prev_life <= 20
            and self.hero.life == 100
        )

        if just_respawned:
            # Record respawn turn for aggressive phase tracking
            self._respawn_turn = self.game.turn
            # Clear cached destination - don't path to old target
            self._cached_destination = None
            return True

        return False

    def _is_in_post_respawn_phase(self):
        """Check if we're still in the aggressive post-respawn phase.

        After respawning, we play aggressively for RESPAWN_AGGRESSIVE_TURNS
        turns to quickly recover mines and gold.

        Returns:
            bool: True if in post-respawn aggressive phase.
        """
        if not self.RESPAWN_DETECTION_ENABLED:
            return False

        if self._respawn_turn is None:
            return False

        turns_since_respawn = self.game.turn - self._respawn_turn
        return turns_since_respawn < self.RESPAWN_AGGRESSIVE_TURNS

    def _get_game_phase(self):
        """Determine the current game phase based on turn progress.

        Phases:
        - "opening": First PHASE_OPENING_END% of game OR post-respawn aggressive phase
        - "mid": PHASE_OPENING_END% to PHASE_MID_END% of game
        - "end": Last (100 - PHASE_MID_END)% of game

        Post-respawn behavior (if RESPAWN_DETECTION_ENABLED):
        - After dying, plays like "opening" for RESPAWN_AGGRESSIVE_TURNS turns
        - This allows quick recovery of mines without over-healing

        Returns:
            str: "opening", "mid", or "end"
        """
        # Calculate game progress
        turn = self.game.turn
        max_turns = self.game.max_turns
        progress = turn / max_turns if max_turns > 0 else 0

        # Check if in post-respawn aggressive phase
        if self._is_in_post_respawn_phase():
            return "opening"

        # Normal phase calculation
        if progress < self.PHASE_OPENING_END:
            return "opening"
        elif progress < self.PHASE_MID_END:
            return "mid"
        else:
            return "end"

    def _get_remaining_turns(self):
        """Get the number of turns remaining in the game.

        Note: In Vindinium, max_turns is total turns for ALL heroes.
        With 4 heroes, each hero gets max_turns/4 individual turns.

        Returns:
            int: Remaining turns for this hero.
        """
        total_remaining = self.game.max_turns - self.game.turn
        # Each hero gets 1/4 of total turns
        return total_remaining // 4

    def _get_dynamic_hp_threshold(self, danger_level=0):
        """Get the HP threshold for going to tavern based on game phase and danger.

        Uses class attributes for thresholds:
        - HP_THRESHOLD_OPENING, HP_THRESHOLD_MID, HP_THRESHOLD_END
        - DANGER_HP_MODIFIER (added when enemies nearby)

        Args:
            danger_level (int): Current danger level (0-3).

        Returns:
            int: HP threshold below which we should go to tavern.
        """
        phase = self._get_game_phase()

        if phase == "opening":
            base_threshold = self.HP_THRESHOLD_OPENING
        elif phase == "mid":
            base_threshold = self.HP_THRESHOLD_MID
        else:  # end
            base_threshold = self.HP_THRESHOLD_END

        # Add danger modifier: more conservative when enemies nearby
        danger_modifier = self.DANGER_HP_MODIFIER if danger_level >= 1 else 0

        return base_threshold + danger_modifier

    def _is_mine_worth_taking(self, mine_x, mine_y):
        """Calculate if taking a mine is worth it based on remaining turns.

        Uses MIN_TURNS_TO_HOLD_MINE to determine minimum payoff.

        A mine is worth taking if:
        1. We can reach it before the game ends
        2. We'll hold it for >= MIN_TURNS_TO_HOLD_MINE turns
        3. We have enough HP to survive the capture

        Args:
            mine_x (int): X coordinate of the mine.
            mine_y (int): Y coordinate of the mine.

        Returns:
            bool: True if the mine is worth taking.
        """
        # Calculate distance to mine
        distance = vin.utils.distance_manhattan(
            self.hero.x, self.hero.y, mine_x, mine_y
        )

        remaining = self._get_remaining_turns()

        # Can't reach it before game ends
        if distance >= remaining:
            return False

        # Turns we'd hold the mine
        turns_holding = remaining - distance

        # Not worth it if we'd hold for less than MIN_TURNS_TO_HOLD_MINE
        if turns_holding < self.MIN_TURNS_TO_HOLD_MINE:
            return False

        # Check if we have enough HP to survive the journey + capture
        # Need: travel HP loss (1 per turn) + capture cost (20) + small buffer (5)
        hp_needed = distance + 20 + 5
        if self.hero.life < hp_needed:
            return False

        return True

    # =========================================================================
    # MAIN DECISION LOGIC
    # =========================================================================

    def _do_move(self):
        """Decide the next move with configurable survival/aggression balance.

        Decision priority (configurable via class attributes):
        0. Check for respawn (reset strategy if just died)
        1. Nearby tavern healing (if HP < NEARBY_TAVERN_HEAL_THRESHOLD)
        2. Flee from danger (if danger_level >= FLEE_DANGER_THRESHOLD)
        3. Go to tavern if low HP (phase-aware + DANGER_HP_MODIFIER)
        4. Opportunistic kill (if OPPORTUNISTIC_KILLS_ENABLED and weak enemy nearby)
        5. Normal mining behavior (with MIN_TURNS_TO_HOLD_MINE check)

        Safety layer (if DANGER_CHECK_ENABLED):
        - Check if move walks into danger
        - Find safe alternative or use ALLOW_STAY_AS_FALLBACK

        Respawn handling (if RESPAWN_DETECTION_ENABLED):
        - Clears cached destination on respawn
        - Plays aggressively for RESPAWN_AGGRESSIVE_TURNS turns

        Returns:
            str: The direction to move ('North', 'South', 'East', 'West', 'Stay').
        """
        # Priority 0: Check for respawn and reset strategy
        self._check_and_handle_respawn()

        # Priority 1: Opportunistic healing at nearby tavern
        should_heal, tavern = self._should_heal_at_nearby_tavern()
        if should_heal:
            command = self._move_to_nearby_tavern(tavern)
            self._prev_life = self.hero.life
            return command

        # Priority 2: Flee from critical danger OR pub fight stalemate
        danger_level, closest_enemy = self._get_danger_level()

        # Check for pub fight stalemate: we're adjacent to enemy who is near ANY tavern
        is_pub_fight = False
        if closest_enemy is not None:
            enemy_dist = vin.utils.distance_manhattan(
                self.hero.x, self.hero.y,
                closest_enemy.x, closest_enemy.y
            )
            if enemy_dist == 1:  # We're fighting (adjacent to enemy)
                # Check if enemy is near ANY tavern (they can just heal)
                for tavern in self.game.taverns:
                    tavern_to_enemy = vin.utils.distance_manhattan(
                        tavern.x, tavern.y,
                        closest_enemy.x, closest_enemy.y
                    )
                    if tavern_to_enemy <= 1:  # Enemy adjacent to tavern
                        is_pub_fight = True
                        break

        if danger_level >= self.FLEE_DANGER_THRESHOLD or is_pub_fight:
            # Try to flee
            flee_cmd = self._get_flee_direction(closest_enemy)
            if flee_cmd != "Stay":
                self._prev_life = self.hero.life
                return flee_cmd
            # Can't flee - go to tavern if possible
            if self.hero.gold >= 2:
                command = self._go_to_nearest_tavern()
                self._prev_life = self.hero.life
                return command

        # Priority 3: Go to tavern if low HP (phase-aware threshold)
        hp_threshold = self._get_dynamic_hp_threshold(danger_level)

        if self.hero.life < hp_threshold and self.hero.gold >= 2:
            command = self._go_to_nearest_tavern()
            self._prev_life = self.hero.life
            return command

        # Priority 4: Opportunistic kill - hunt weak enemies with mines
        kill_target, kill_distance = self._find_opportunistic_kill_target()
        if kill_target is not None:
            command = self._go_to_enemy(kill_target)
            self._prev_life = self.hero.life
            if command != "Stay":
                return command

        # Priority 5: Normal mining behavior (with mine value calculation)
        command = self._go_to_nearest_mine()

        # Safety check: don't walk into enemies (configurable)
        if self.DANGER_CHECK_ENABLED and self.hero.life < self.DANGER_CHECK_HP_THRESHOLD:
            if self._would_walk_into_danger(command):
                safe_cmd = self._find_safe_alternative(command)
                if safe_cmd:
                    command = safe_cmd

        # Friendly fire avoidance
        if self._would_hit_friendly(command):
            self._prev_life = self.hero.life
            return "Stay"

        # Track life for respawn detection
        self._prev_life = self.hero.life
        return command

    def _would_walk_into_danger(self, command):
        """Check if a move would put us in a dangerous position.

        This check is RELAXED to avoid blocking good moves:
        - Only dangerous if walking INTO an enemy who would kill us
        - Adjacent enemies are NOT considered dangerous (we can fight)

        Args:
            command (str): The move command to check.

        Returns:
            bool: True if the move is dangerous (would result in death).
        """
        next_x, next_y = self._get_position_after_move(command)

        for enemy in self._get_enemies():
            dist = vin.utils.distance_manhattan(next_x, next_y, enemy.x, enemy.y)

            # Would walk into enemy - only dangerous if we'd die
            if dist == 0:
                # We attack first (we're moving into them), dealing 20 damage
                # Safe if: enemy dies (life <= 20)
                if enemy.life <= 20:
                    return False  # Safe - we kill them

                # Safe if: we have significantly more HP (we'd win the fight)
                if self.hero.life > enemy.life:
                    return False  # Safe - we're stronger

                # Dangerous only if we'd likely die
                if self.hero.life <= 20:
                    return True  # We'd die on their counter-attack

        return False  # Not dangerous - go for it

    def _find_safe_alternative(self, original_command):
        """Try to find a safer alternative to the original command.

        Uses ALLOW_STAY_AS_FALLBACK to determine behavior when no safe move found.

        Args:
            original_command (str): The original intended move.

        Returns:
            str: A safer alternative command, or original if ALLOW_STAY_AS_FALLBACK=False.
        """
        # Try all directions except the dangerous one (exclude Stay initially)
        movement_directions = ["North", "South", "East", "West"]

        for direction in movement_directions:
            if direction == original_command:
                continue

            if not self._would_walk_into_danger(direction):
                if not self._would_hit_friendly(direction):
                    next_x, next_y = self._get_position_after_move(direction)
                    if self._is_tile_walkable(next_x, next_y):
                        return direction

        # No safe movement found
        if self.ALLOW_STAY_AS_FALLBACK:
            return "Stay"
        else:
            # Return original command - be aggressive, don't stay still
            return original_command

    def _go_to_nearest_mine(self):
        """Navigate to the nearest worthwhile mine not owned by this bot or friendly bots.

        When FRIENDLY_FIRE_AVOIDANCE is enabled, this method will skip mines
        owned by heroes with the same name (friendly bots), treating them
        as if they were our own mines.

        Phase 2 Enhancement: Uses mine value calculation to skip mines that
        aren't worth taking (too far, not enough turns left, not enough HP).

        Returns:
            str: The direction to move toward the nearest worthwhile mine,
                or a random move if no worthwhile mine is found.
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

            # Phase 2: Skip mines that aren't worth taking
            if not self._is_mine_worth_taking(mine.x, mine.y):
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
