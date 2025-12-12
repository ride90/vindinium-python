# Code Snippets

Common patterns and examples for building Vindinium bots.

## Base Template

Unless stated otherwise, use this as your starting point:

```python
import vindinium

class MyBot(vindinium.bots.BaseBot):
    # Your code here
    pass
```

## Random Bot

A bot that moves randomly:

```python
import random
import vindinium

class RandomBot(vindinium.bots.BaseBot):
    def _do_move(self):
        moves = [
            vindinium.STAY,
            vindinium.NORTH,
            vindinium.EAST,
            vindinium.WEST,
            vindinium.SOUTH
        ]
        return random.choice(moves)
```

## Move to Specific Position

Use A* pathfinding to navigate to a specific location:

```python
def _do_start(self):
    self.search = vindinium.ai.AStar(self.game.map)

def _do_move(self):
    return self.go_to(3, 4)

def go_to(self, target_x, target_y):
    """Navigate to a specific position."""
    x = self.hero.x
    y = self.hero.y
    
    # Compute path to the target
    path = self.search.find(x, y, target_x, target_y)
    
    # Follow the path
    if path:
        next_x, next_y = path[0]
        return vindinium.utils.path_to_command(x, y, next_x, next_y)
    
    return vindinium.STAY
```

## Move to Nearest Tavern

Navigate to the closest tavern:

```python
def go_to_nearest_tavern(self):
    """Go to the nearest tavern to heal."""
    x = self.hero.x
    y = self.hero.y
    
    # Order taverns by distance
    taverns = vindinium.utils.order_by_distance(x, y, self.game.taverns)
    
    if taverns:
        return self.go_to(taverns[0].x, taverns[0].y)
    
    return vindinium.STAY
```

## Move to Nearest Enemy/Neutral Mine

Capture the closest mine that you don't own:

```python
def go_to_nearest_mine(self):
    """Go to the nearest mine we don't own."""
    x = self.hero.x
    y = self.hero.y
    
    # Order mines by distance
    mines = vindinium.utils.order_by_distance(x, y, self.game.mines)
    
    for mine in mines:
        # Find nearest mine not owned by this hero
        if mine.owner != self.id:
            return self.go_to(mine.x, mine.y)
    
    return vindinium.STAY
```

## Health Management

Check health and decide whether to heal or fight:

```python
def move(self):
    # Heal if health is low
    if self.hero.life < 30:
        return self.go_to_nearest_tavern()
    
    # Heal if we can't afford to take a mine
    if self.hero.life <= 20:
        return self.go_to_nearest_tavern()
    
    # Otherwise, go get mines
    return self.go_to_nearest_mine()
```

## Check if We Can Afford Tavern

Make sure we have enough gold before going to tavern:

```python
def should_heal(self):
    """Decide if we should go to a tavern."""
    # Need at least 2 gold to drink
    if self.hero.gold < 2:
        return False
    
    # Heal if health is low
    if self.hero.life < 40:
        return True
    
    return False

def move(self):
    if self.should_heal():
        return self.go_to_nearest_tavern()
    else:
        return self.go_to_nearest_mine()
```

## Find Weakest Enemy

Target the enemy with the lowest health:

```python
def find_weakest_enemy(self):
    """Find the enemy hero with the lowest health."""
    enemies = [h for h in self.game.heroes if h != self.hero]
    
    if enemies:
        return min(enemies, key=lambda h: h.life)
    
    return None

def move(self):
    enemy = self.find_weakest_enemy()
    
    if enemy and enemy.life < 30:
        # Chase weak enemies
        return self.go_to(enemy.x, enemy.y)
    else:
        # Otherwise get mines
        return self.go_to_nearest_mine()
```

## Count Owned Mines

Check how many mines you currently own:

```python
def move(self):
    owned_mines = self.hero.mine_count
    
    print(f'I own {owned_mines} mines')
    
    if owned_mines < 2:
        # Get more mines
        return self.go_to_nearest_mine()
    else:
        # Defend or attack
        return self.defend_territory()
```

## Calculate Distance to Target

Use Manhattan distance to check how far something is:

```python
def move(self):
    # Find nearest tavern
    taverns = vindinium.utils.order_by_distance(
        self.hero.x, self.hero.y, self.game.taverns
    )
    
    if taverns:
        distance = vindinium.utils.distance_manhattan(
            self.hero.x, self.hero.y,
            taverns[0].x, taverns[0].y
        )
        
        print(f'Nearest tavern is {distance} tiles away')
```

## Complete Example: Balanced Bot

A bot that balances mining, healing, and combat:

```python
import vindinium

class BalancedBot(vindinium.bots.BaseBot):
    def _do_start(self):
        """Initialize pathfinding."""
        self.search = vindinium.ai.AStar(self.game.map)

    def _do_move(self):
        """Main decision logic."""
        # Critical health - must heal
        if self.hero.life < 25 and self.hero.gold >= 2:
            return self.go_to_nearest_tavern()

        # Can't take mines - need to heal first
        if self.hero.life <= 20:
            if self.hero.gold >= 2:
                return self.go_to_nearest_tavern()
            else:
                return vindinium.STAY  # Wait to accumulate gold

        # Low on mines - prioritize capturing
        if self.hero.mine_count < 3:
            return self.go_to_nearest_mine()

        # Otherwise, get more mines
        return self.go_to_nearest_mine()
    
    def go_to(self, target_x, target_y):
        """Navigate to target position."""
        path = self.search.find(
            self.hero.x, self.hero.y,
            target_x, target_y
        )
        
        if path:
            next_x, next_y = path[0]
            return vindinium.utils.path_to_command(
                self.hero.x, self.hero.y,
                next_x, next_y
            )
        
        return vindinium.STAY
    
    def go_to_nearest_tavern(self):
        """Go to nearest tavern."""
        taverns = vindinium.utils.order_by_distance(
            self.hero.x, self.hero.y, self.game.taverns
        )
        
        if taverns:
            return self.go_to(taverns[0].x, taverns[0].y)
        
        return vindinium.STAY
    
    def go_to_nearest_mine(self):
        """Go to nearest unowned mine."""
        mines = vindinium.utils.order_by_distance(
            self.hero.x, self.hero.y, self.game.mines
        )
        
        for mine in mines:
            if mine.owner != self.id:
                return self.go_to(mine.x, mine.y)
        
        return vindinium.STAY
```

