# Configuration Guide

This project uses environment variables for configuration, loaded from a `.env` file.

## Quick Setup

### 1. Create Your `.env` File

Copy the example file:

```bash
cp .env.example .env
```

### 2. Edit `.env` with Your Settings

Open `.env` in your text editor and update the values:

```bash
# Vindinium server URL
SERVER=<your-vindinium-server-url>

# Your bot's API key (get from the server)
KEY=<your-api-key>

# Your hero's display name
HERO_NAME=MyAwesomeBot

# Bot to use (RandomBot, MinerBot, AggressiveBot, MinimaxBot)
BOT=MinerBot
```

### 3. Get Your API Key

1. Visit your Vindinium server
2. Click **"Create a bot"**
3. Enter your bot name
4. Copy the API key
5. Paste it into your `.env` file as `KEY`

## Configuration Settings

### `SERVER`

The Vindinium server URL.

- **Required:** Yes
- **Example:** `https://your-vindinium-server.com`
- **Local server:** `http://localhost:9000` (if running your own server)

### `KEY`

Your bot's API key from the Vindinium server.

- **Required:** Yes
- **Example:** `abc123xyz`
- **Where to get it:** Your Vindinium server → Create a bot

### `HERO_NAME`

Your hero's display name (used for logging and display in your code).

- **Default:** `MyBot`

### `BOT`

The bot class to use when running `main.py`.

- **Required:** No
- **Default:** `MinerBot`
- **Available bots:**
  - `RandomBot` - Makes random moves
  - `MinerBot` - Focuses on capturing mines
  - `AggressiveBot` - Attacks other heroes
  - `MinimaxBot` - Uses minimax algorithm with game tree search
  - `BaseBot` - Base class (you need to extend it)
  - `RawBot` - Raw interface (you need to extend it)
- **Example:** `BOT=AggressiveBot`
- **Example:** `AggressiveMiner`
- **Note:** The actual in-game name is set on the Vindinium server when you create your bot

## Using Settings in Your Code

### Import Settings

```python
from settings import settings

# Access individual settings
print(settings.SERVER)      # Your configured server URL
print(settings.KEY)         # Your API key
print(settings.HERO_NAME)   # MyBot
```

### Use in Client

```python
import vindinium
from settings import settings

# Validate settings first
settings.validate()

# Create client with settings
client = vindinium.Client(
    server=settings.SERVER,
    key=settings.KEY,
    mode='training',
    n_turns=300
)
```

### Display Settings

```python
from settings import settings

# Show current configuration (API key is masked for security)
settings.display()
```

Output:
```
============================================================
VINDINIUM SETTINGS
============================================================
Server:     <your-configured-server-url>
API Key:    abc1****
Hero Name:  MyAwesomeBot
============================================================
```

## Security

### `.env` File is Ignored by Git

The `.env` file is automatically ignored by git (listed in `.gitignore`), so your API key won't be committed to version control.

**Never commit your `.env` file!**

### `.env.example` is Safe to Commit

The `.env.example` file contains placeholder values and is safe to commit. It serves as a template for other developers.

## Troubleshooting

### "KEY is not set"

You need to create a `.env` file with your API key:

```bash
cp .env.example .env
# Edit .env and add your API key
```

### Settings Not Loading

Make sure:
1. The `.env` file is in the project root directory (same level as `main.py`)
2. The file is named exactly `.env` (not `.env.txt` or anything else)
3. You've installed `python-dotenv`: `pip install -r requirements.txt`

### Wrong Server URL

If you're getting connection errors, check that `SERVER` is correct:
- Make sure you have the correct server URL from your Vindinium administrator
- For local servers: `http://localhost:9000`

## Example `.env` File

```bash
# Vindinium Game Settings

# Server URL
SERVER=<your-vindinium-server-url>

# Your API key from your Vindinium server
KEY=<your-api-key>

# Your hero's name (for display/logging)
HERO_NAME=MyAwesomeBot

# Bot to use
BOT=MinerBot
```

## Advanced Usage

### Multiple Bots

If you want to run multiple bots with different configurations, you can:

1. Create multiple `.env` files (e.g., `.env.bot1`, `.env.bot2`)
2. Load them explicitly in your code:

```python
from dotenv import load_dotenv

# Load specific env file
load_dotenv('.env.bot1')

from settings import settings
# Now settings will use values from .env.bot1
```

### Override Settings with Environment Variables

You can override any setting using environment variables without editing `.env`:

```bash
# Run with a different bot
BOT=AggressiveBot python main.py

# Run with different bot and hero name
BOT=MinimaxBot HERO_NAME=SmartBot python main.py

# Override multiple settings
SERVER=http://localhost KEY=test123 BOT=RandomBot python main.py
```

This is perfect for running multiple bots simultaneously:

```bash
# Terminal 1 - MinerBot
BOT=MinerBot python main.py

# Terminal 2 - AggressiveBot
BOT=AggressiveBot python main.py

# Terminal 3 - MinimaxBot
BOT=MinimaxBot python main.py

# Terminal 4 - RandomBot
BOT=RandomBot python main.py
```

### Override Settings in Code

You can also override settings in code if needed:

```python
from settings import settings

# Override for testing
settings.SERVER = 'http://localhost:9000'
settings.HERO_NAME = 'TestBot'
settings.BOT = 'AggressiveBot'
```

## See Also

- [Installation Guide](INSTALLATION.md)
- [Getting Started](GETTING_STARTED.md)
- Main [README](../README.md)

