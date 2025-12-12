"""Game settings loaded from environment variables.

This module loads configuration from a .env file in the project root.
Create a .env file based on .env.example and set your values there.
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
env_path = Path(__file__).parent / '.env'
load_dotenv(dotenv_path=env_path)


class Settings:
    """Game configuration settings.

    All settings are loaded from environment variables defined in .env file.

    Attributes:
        SERVER (str): Vindinium server URL.
        KEY (str): Your bot's API key from the Vindinium website.
        HERO_NAME (str): Your hero's display name (for future use).
        BOT (str): Bot class to use (RandomBot, MinerBot, AggressiveBot, MinimaxBot).
        MODE (str): Game mode ('training' or 'arena').
        N_TURNS (int): Number of turns for training mode (10-300).
        OPEN_BROWSER (bool): Whether to open the game in browser automatically.
        DEBUG (bool): Enable debug logging (prints each move and timing).
    """

    # Vindinium server URL
    SERVER = os.getenv('SERVER', '')

    # Your bot's API key
    KEY = os.getenv('KEY', '')

    # Your hero's name
    HERO_NAME = os.getenv('HERO_NAME', '')

    # Bot class to use
    BOT = os.getenv('BOT', 'MinerBot')

    # Game mode (training or arena)
    MODE = os.getenv('MODE', 'training')

    # Number of turns (for training mode)
    N_TURNS = int(os.getenv('N_TURNS', '10'))

    # Open browser automatically
    OPEN_BROWSER = os.getenv('OPEN_BROWSER', 'true').lower() in ('true', '1', 'yes')

    # Debug mode (log each move and timing)
    DEBUG = os.getenv('DEBUG', 'false').lower() in ('true', '1', 'yes')
    
    @classmethod
    def validate(cls):
        """Validate that required settings are configured.
        
        Raises:
            ValueError: If required settings are missing.
        """
        if not cls.KEY:
            raise ValueError(
                "KEY is not set. "
                "Please create a .env file with your API key. "
                "See .env.example for reference."
            )
        
        if not cls.SERVER:
            raise ValueError("SERVER is not set.")
    
    @classmethod
    def display(cls):
        """Display current settings (with masked API key for security)."""
        masked_key = cls.KEY[:4] + '****' if len(cls.KEY) > 4 else '****'
        print("=" * 60)
        print("VINDINIUM SETTINGS")
        print("=" * 60)
        print(f"Server:       {cls.SERVER}")
        print(f"API Key:      {masked_key}")
        print(f"Hero Name:    {cls.HERO_NAME}")
        print(f"Bot:          {cls.BOT}")
        print(f"Mode:         {cls.MODE}")
        print(f"Turns:        {cls.N_TURNS}")
        print(f"Open Browser: {cls.OPEN_BROWSER}")
        print(f"Debug:        {cls.DEBUG}")
        print("=" * 60)


# Create a singleton instance
settings = Settings()


# Convenience exports
SERVER = settings.SERVER
KEY = settings.KEY
HERO_NAME = settings.HERO_NAME
BOT = settings.BOT
MODE = settings.MODE
N_TURNS = settings.N_TURNS
OPEN_BROWSER = settings.OPEN_BROWSER
DEBUG = settings.DEBUG

