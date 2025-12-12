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
    """
    
    # Vindinium server URL
    SERVER = os.getenv('VINDINIUM_SERVER', '')
    
    # Your bot's API key
    KEY = os.getenv('VINDINIUM_KEY', '')
    
    # Your hero's name
    HERO_NAME = os.getenv('VINDINIUM_HERO_NAME', '')
    
    @classmethod
    def validate(cls):
        """Validate that required settings are configured.
        
        Raises:
            ValueError: If required settings are missing.
        """
        if not cls.KEY:
            raise ValueError(
                "VINDINIUM_KEY is not set. "
                "Please create a .env file with your API key. "
                "See .env.example for reference."
            )
        
        if not cls.SERVER:
            raise ValueError("VINDINIUM_SERVER is not set.")
    
    @classmethod
    def display(cls):
        """Display current settings (with masked API key for security)."""
        masked_key = cls.KEY[:4] + '****' if len(cls.KEY) > 4 else '****'
        print("=" * 60)
        print("VINDINIUM SETTINGS")
        print("=" * 60)
        print(f"Server:     {cls.SERVER}")
        print(f"API Key:    {masked_key}")
        print(f"Hero Name:  {cls.HERO_NAME}")
        print("=" * 60)


# Create a singleton instance
settings = Settings()


# Convenience exports
SERVER = settings.SERVER
KEY = settings.KEY
HERO_NAME = settings.HERO_NAME

