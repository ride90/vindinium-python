"""Main entry point for running a Vindinium bot.

This module provides a simple example of how to create and run a bot
using the vindinium client library.
"""

import vindinium
from settings import settings


def main():
    """Run a MinerBot in training mode.

    Creates a Vindinium client configured for training mode and runs
    a MinerBot instance. The game replay URL is printed after completion.
    """
    # Validate settings
    try:
        settings.validate()
    except ValueError as e:
        print(f"Configuration Error: {e}")
        print("\nPlease create a .env file based on .env.example")
        return

    # Display current settings
    settings.display()

    # Create a vindinium client using settings from .env
    client = vindinium.Client(
        server=settings.SERVER,
        key=settings.KEY,
        mode="training",
        n_turns=10,
        open_browser=True,
    )

    print(f"\nStarting game with {settings.HERO_NAME}...")
    url = client.run(vindinium.bots.MinerBot())
    print(f"\n🎮 Replay at: {url}")


if __name__ == "__main__":
    main()
