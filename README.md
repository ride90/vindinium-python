# vindinium-python

A Python 3.13+ client for Vindinium - an AI programming challenge game.

## About Vindinium

Vindinium is an online turn-based competition where you control a bot to compete against other bots. Four heroes battle on a map to accumulate the most gold by capturing mines, fighting opponents, and managing resources.

**🚀 Quick Start:** This project includes a Docker setup to run a local Vindinium server - no external server needed! See [Local Server Guide](docs/LOCAL_SERVER.md).

## Features

This library provides a complete framework for building Vindinium bots:

### 🤖 Built-in Bots

- **RawBot** - Minimal bot interface (no state processing)
- **BaseBot** - Processes game state and provides Game object (recommended base class)
- **RandomBot** - Performs random movements
- **MinerBot** - Focuses on capturing and holding mines
- **AggressiveBot** - Attacks other heroes
- **MinimaxBot** - Uses minimax algorithm with game tree search

### 📊 Game Models

Used by `BaseBot` to represent the game state:

- **Game** - Main game state container
- **Map** - Static map information (walls, taverns, mines, spawn points)
- **Hero** - Hero attributes (position, health, gold, mines owned)
- **Mine** - Mine locations and ownership
- **Tavern** - Tavern locations

### 🧠 AI Algorithms

Pre-built algorithms specialized for Vindinium:

- **AStar** - A* pathfinding with Manhattan distance heuristic
- **Minimax** - Game tree search with alpha-beta pruning

### 🛠️ Utilities

- Direction/command conversion functions
- Manhattan distance calculations
- Object ordering by distance
- Priority queue (HeapQueue)
- Timer for performance measurement

**Note:** This client fixes the server's inconsistent coordinate system automatically.

## Requirements

- **Python 3.13+** (uses modern Python 3 features)
- **Dependencies:** See `requirements.txt`

## Installation

This project runs directly from source code - no package installation needed!

### 1. Clone the Repository

```bash
git clone https://github.com/ride90/vindinium-python.git
cd vindinium-python
```

### 2. Set Up Python Environment

Make sure you have Python 3.13+ installed:

```bash
python --version  # Should be 3.13 or higher
```

Optionally, create a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Start Local Server (Optional but Recommended)

Run your own Vindinium server locally:

```bash
cd docker
docker-compose up -d
```

Then open http://localhost in your browser. See [Local Server Guide](docs/LOCAL_SERVER.md) for details.

**Skip this step** if you have access to an external Vindinium server.

### 5. Get Your API Key

1. Go to your Vindinium server (http://localhost if using local server)
2. Register or log in
3. Click "Create a bot" and enter a name
4. Copy your API key

### 6. Configure Your Settings

Create a `.env` file from the example:

```bash
cp .env.example .env
```

Edit `.env` and add your server URL and API key:

```bash
# For local server:
SERVER=http://localhost
KEY=<your-api-key>
HERO_NAME=MyBot

# For external server:
# SERVER=<your-vindinium-server-url>
# KEY=<your-api-key>
# HERO_NAME=MyBot
```

See [Configuration Guide](docs/CONFIGURATION.md) for details.

### 7. Run Your Bot

```bash
python main.py
```

The settings will be loaded automatically from your `.env` file.

## Quick Start

### Basic Usage

```python
import vindinium

# Create a client
client = vindinium.Client(
    server='<https://your-vindinium-server-url>',
    key='YOUR_API_KEY',
    mode='training',
    n_turns=300,
    open_browser=True
)

# Run a bot
url = client.run(vindinium.bots.MinerBot())
print('Replay at:', url)
```

### Creating Your Own Bot

All bots should inherit from `BaseBot` (recommended) or `RawBot`:

```python
import vindinium

class MyBot(vindinium.bots.BaseBot):
    def _do_start(self):
        """Called when the game starts."""
        print('Game started!')
        # Initialize your bot here
        self.search = vindinium.ai.AStar(self.game.map)

    def _do_move(self):
        """Called each turn. Must return a command."""
        # Your bot logic here
        if self.hero.life < 30:
            return self.go_to_nearest_tavern()
        else:
            return self.go_to_nearest_mine()

    def _do_end(self):
        """Called when the game ends."""
        print(f'Game finished! Final gold: {self.hero.gold}')

    def go_to_nearest_tavern(self):
        """Navigate to the nearest tavern."""
        taverns = vindinium.utils.order_by_distance(
            self.hero.x, self.hero.y, self.game.taverns
        )
        if taverns:
            path = self.search.find(
                self.hero.x, self.hero.y,
                taverns[0].x, taverns[0].y
            )
            if path:
                return vindinium.utils.path_to_command(
                    self.hero.x, self.hero.y,
                    path[0][0], path[0][1]
                )
        return vindinium.STAY

    def go_to_nearest_mine(self):
        """Navigate to the nearest enemy/neutral mine."""
        mines = vindinium.utils.order_by_distance(
            self.hero.x, self.hero.y, self.game.mines
        )
        for mine in mines:
            if mine.owner != self.id:
                path = self.search.find(
                    self.hero.x, self.hero.y,
                    mine.x, mine.y
                )
                if path:
                    return vindinium.utils.path_to_command(
                        self.hero.x, self.hero.y,
                        path[0][0], path[0][1]
                    )
        return vindinium.STAY

# Run your bot
client = vindinium.Client(
    server='<https://your-vindinium-server-url>',
    key='YOUR_API_KEY',
    mode='training',
    n_turns=300
)
url = client.run(MyBot())
print('Replay at:', url)
```

### Available Bot Attributes

When you inherit from `BaseBot`, your bot has access to:

- `self.id` - Your hero's ID (1-4)
- `self.game` - The Game instance with full state
- `self.hero` - Your Hero instance (shortcut to `game.heroes[id]`)
- `self.state` - Raw JSON state from the server

### Available Commands

Your `move()` method must return one of these commands:

- `vindinium.NORTH` - Move north
- `vindinium.SOUTH` - Move south
- `vindinium.EAST` - Move east
- `vindinium.WEST` - Move west
- `vindinium.STAY` - Stay in place (to capture mine or drink at tavern)

## Project Structure

```
vindinium-python/
├── vindinium/           # Main package
│   ├── __init__.py     # Package initialization and constants
│   ├── client.py       # Vindinium client for server communication
│   ├── bots/           # Bot implementations
│   │   ├── raw_bot.py
│   │   ├── base_bot.py
│   │   ├── random_bot.py
│   │   ├── miner_bot.py
│   │   ├── aggressive_bot.py
│   │   └── minimax_bot.py
│   ├── models/         # Game state models
│   │   ├── game.py
│   │   ├── hero.py
│   │   ├── map.py
│   │   ├── mine.py
│   │   └── tavern.py
│   ├── ai/             # AI algorithms
│   │   ├── astar.py
│   │   └── minimax/
│   │       ├── minimax.py
│   │       ├── functions.py
│   │       ├── state.py
│   │       └── simulation.py
│   └── utils/          # Utility functions
│       ├── functions.py
│       ├── heap_queue.py
│       └── timer.py
├── main.py             # Example entry point
├── requirements.txt    # Python dependencies
├── setup.py           # Project metadata
└── README.md          # This file
```

## Testing Your Installation

```bash
# Test that the module imports correctly
python -c "import vindinium; print('✓ Import successful!')"

# List available bots
python -c "import vindinium; print(dir(vindinium.bots))"
```

## Game Modes

### Training Mode

Practice against the server AI with a configurable number of turns:

```python
client = vindinium.Client(
    server='<https://your-vindinium-server-url>',
    key='YOUR_API_KEY',
    mode='training',
    n_turns=300  # 10-300 turns
)
```

### Arena Mode

Compete against other players' bots (always 300 turns):

```python
client = vindinium.Client(
    server='<https://your-vindinium-server-url>',
    key='YOUR_API_KEY',
    mode='arena'
)
```

## Tips for Bot Development

1. **Start with BaseBot** - It handles state parsing and provides useful models
2. **Use A* pathfinding** - The built-in AStar class handles obstacles and spawn points
3. **Manage health carefully** - You lose 1 HP per turn and 20 HP when capturing mines
4. **Balance offense and defense** - Mines generate gold, but you need to survive
5. **Watch for spawn camping** - Avoid spawn points when possible
6. **Test in training mode** - Perfect your strategy before entering the arena

## Contributing

Contributions are welcome! This is a community-maintained project.

## License

MIT License - See LICENSE file for details

## Credits

- Original Python starter: [ornicar](https://github.com/ornicar/vindinium-starter-python)
- Python 3 & modernization: [ride90](https://github.com/ride90/vindinium-python)

## Links

- **Game Rules:** Check the official website for complete rules and mechanics
- **API Documentation:** Available on the Vindinium website