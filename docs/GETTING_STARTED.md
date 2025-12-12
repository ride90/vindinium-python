# Getting Started

This guide will help you create your first Vindinium bot using the vindinium-python library.

## Basic Setup

To use vindinium, create a Python file (e.g., `my_bot.py`) with the following structure:

```python
import vindinium

# Create a vindinium client
client = vindinium.Client(
    server='<https://your-vindinium-server-url>',
    key='YOUR_API_KEY',           # Your bot API key
    mode='training',               # 'training' or 'arena'
    n_turns=300,                   # Only valid for training mode (10-300)
    open_browser=True              # Opens browser to watch the game
)

# Run your bot
url = client.run(vindinium.bots.MinerBot())
print('Replay at:', url)
```

The `client.run()` method receives a bot instance. See below for how to create your own bot.

## Creating Bots

All bots must inherit from either `vindinium.bots.RawBot` or `vindinium.bots.BaseBot`.

### RawBot vs BaseBot

- **RawBot**: Minimal interface, receives raw JSON state (no processing)
- **BaseBot**: Processes state and creates a `Game` instance with models (recommended)

It is **strongly recommended** to use `BaseBot` as your base class.

## Your First Bot

Here's a simple bot that inherits from `BaseBot`:

```python
import vindinium

class MyBot(vindinium.bots.BaseBot):
    def start(self):
        """Called when the game starts."""
        print('Game just started!')
    
    def move(self):
        """Called each turn to get the bot's next move."""
        print('Game asking for a movement')
        return vindinium.STAY
    
    def end(self):
        """Called when the game ends."""
        print('Game finished!')

# Run the bot
client = vindinium.Client(
    server='<https://your-vindinium-server-url>',
    key='YOUR_API_KEY',
    mode='training',
    n_turns=300
)
url = client.run(MyBot())
print('Replay at:', url)
```

## Bot Attributes

When you inherit from `BaseBot`, your bot has access to these attributes:

- **`self.id`** - Your hero's ID (1-4)
- **`self.game`** - The Game instance containing all game state
- **`self.hero`** - Your Hero instance (shortcut to `self.game.heroes[self.id]`)
- **`self.state`** - The raw JSON state from the server

### Hero Attributes

Your hero (`self.hero`) has these attributes:

- `x`, `y` - Current position
- `life` - Current health (0-100)
- `gold` - Current gold amount
- `mine_count` - Number of mines owned
- `spawn_x`, `spawn_y` - Respawn location

### Game Attributes

The game object (`self.game`) provides:

- `game.heroes` - List of all 4 heroes
- `game.mines` - List of all mines on the map
- `game.taverns` - List of all taverns
- `game.map` - The Map instance with terrain data

## Available Commands

The `move()` method **must return** one of these commands:

- `vindinium.NORTH` - Move north
- `vindinium.SOUTH` - Move south
- `vindinium.EAST` - Move east
- `vindinium.WEST` - Move west
- `vindinium.STAY` - Stay in place

**Important:** Staying on a tavern tile drinks (costs 2 gold, restores 50 HP). Staying on an enemy/neutral mine captures it (costs 20 HP).

## A More Useful Bot

Here's a bot that uses pathfinding to navigate to mines:

```python
import vindinium

class SmartMinerBot(vindinium.bots.BaseBot):
    def start(self):
        """Initialize the A* pathfinding algorithm."""
        self.search = vindinium.ai.AStar(self.game.map)
    
    def move(self):
        """Move towards the nearest enemy/neutral mine."""
        # Check if we need healing
        if self.hero.life < 30:
            return self.go_to_nearest_tavern()
        
        # Otherwise, go capture mines
        return self.go_to_nearest_mine()
    
    def go_to_nearest_tavern(self):
        """Navigate to the nearest tavern."""
        taverns = vindinium.utils.order_by_distance(
            self.hero.x, self.hero.y, self.game.taverns
        )
        
        if taverns:
            return self.go_to(taverns[0].x, taverns[0].y)
        
        return vindinium.STAY
    
    def go_to_nearest_mine(self):
        """Navigate to the nearest mine we don't own."""
        mines = vindinium.utils.order_by_distance(
            self.hero.x, self.hero.y, self.game.mines
        )
        
        for mine in mines:
            if mine.owner != self.id:
                return self.go_to(mine.x, mine.y)
        
        return vindinium.STAY
    
    def go_to(self, target_x, target_y):
        """Navigate to a specific position using A* pathfinding."""
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
```

## Game Modes

### Training Mode

Practice against server AI with configurable turns:

```python
client = vindinium.Client(
    server='<https://your-vindinium-server-url>',
    key='YOUR_API_KEY',
    mode='training',
    n_turns=100  # 10-300 turns
)
```

### Arena Mode

Compete against other players (always 300 turns):

```python
client = vindinium.Client(
    server='<https://your-vindinium-server-url>',
    key='YOUR_API_KEY',
    mode='arena'  # n_turns is ignored in arena mode
)
```

## Next Steps

1. Check out [SNIPPETS.md](SNIPPETS.md) for common bot patterns
2. Explore the built-in bots in `vindinium/bots/` for more examples
3. Read about the [A* pathfinding algorithm](../vindinium/ai/astar.py)
4. Study the [Minimax bot](../vindinium/bots/minimax_bot.py) for advanced strategy

## Tips

- Always check `self.hero.life` before capturing mines (costs 20 HP)
- Taverns cost 2 gold and restore 50 HP
- You lose 1 HP per turn (thirst)
- Attacking adjacent heroes deals 20 damage
- When you die, you respawn with 100 HP but lose all mines
- The game ends after 300 turns (or fewer in training mode)

