# Documentation

Welcome to the vindinium-python documentation!

## Quick Links

- **[Local Server Guide](LOCAL_SERVER.md)** - Run your own Vindinium server (recommended!)
- **[Installation Guide](INSTALLATION.md)** - How to set up the project
- **[Configuration Guide](CONFIGURATION.md)** - Environment variables and settings
- **[Getting Started](GETTING_STARTED.md)** - Create your first bot
- **[Code Snippets](SNIPPETS.md)** - Common patterns and examples

## Overview

This is a Python 3.13+ client for Vindinium, an AI programming challenge where you build bots to compete in a turn-based strategy game.

## Documentation Structure

### 1. Installation
Start here if you're new to the project. Learn how to:
- Clone the repository
- Install Python 3.13+
- Set up dependencies
- Get your API key
- Run your first bot

### 2. Getting Started
Learn the basics of bot development:
- Understanding RawBot vs BaseBot
- Creating your first bot
- Available bot attributes and commands
- Game modes (training vs arena)
- Basic bot examples

### 3. Code Snippets
Ready-to-use code examples:
- Random movement
- Pathfinding with A*
- Health management
- Mine capturing strategies
- Enemy targeting
- Complete bot examples

## Additional Resources

### Built-in Bots

Study these for inspiration:
- `vindinium/bots/random_bot.py` - Random movements
- `vindinium/bots/miner_bot.py` - Mine-focused strategy
- `vindinium/bots/aggressive_bot.py` - Combat-focused strategy
- `vindinium/bots/minimax_bot.py` - Advanced game tree search

### AI Algorithms

- `vindinium/ai/astar.py` - A* pathfinding implementation
- `vindinium/ai/minimax/` - Minimax with alpha-beta pruning

### Game Models

- `vindinium/models/game.py` - Main game state
- `vindinium/models/hero.py` - Hero attributes
- `vindinium/models/map.py` - Map representation
- `vindinium/models/mine.py` - Mine objects
- `vindinium/models/tavern.py` - Tavern objects

## Quick Start

```python
import vindinium

# Create your bot
class MyBot(vindinium.bots.BaseBot):
    def start(self):
        self.search = vindinium.ai.AStar(self.game.map)
    
    def move(self):
        if self.hero.life < 30:
            return self.go_to_nearest_tavern()
        return self.go_to_nearest_mine()

# Run it
client = vindinium.Client(
    server='<https://your-vindinium-server-url>',
    key='YOUR_API_KEY',
    mode='training',
    n_turns=300
)
url = client.run(MyBot())
print('Replay at:', url)
```

## Need Help?

1. Check the [main README](../README.md) for project overview
2. Read the [Getting Started guide](GETTING_STARTED.md)
3. Browse [Code Snippets](SNIPPETS.md) for examples
4. Study the built-in bots in `vindinium/bots/`
5. Visit [<https://your-vindinium-server-url>/](<https://your-vindinium-server-url>/) for game rules

Happy coding! 🤖

