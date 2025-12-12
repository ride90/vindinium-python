"""Main entry point for running a Vindinium bot.

This module provides a simple example of how to create and run a bot
using the vindinium client library.
"""

import vindinium
from settings import settings


def get_bot_class(bot_name):
    """Get the bot class by name.

    Args:
        bot_name (str): Name of the bot class (e.g., 'MinerBot', 'AggressiveBot').

    Returns:
        class: The bot class.

    Raises:
        ValueError: If the bot name is not recognized.
    """
    # Available bots
    available_bots = {
        'RandomBot': vindinium.bots.RandomBot,
        'MinerBot': vindinium.bots.MinerBot,
        'AggressiveBot': vindinium.bots.AggressiveBot,
        'MinimaxBot': vindinium.bots.MinimaxBot,
        'BaseBot': vindinium.bots.BaseBot,
        'RawBot': vindinium.bots.RawBot,
    }

    if bot_name not in available_bots:
        available = ', '.join(available_bots.keys())
        raise ValueError(
            f"Unknown bot: {bot_name}\n"
            f"Available bots: {available}"
        )

    return available_bots[bot_name]


def main():
    """Run a bot in training mode.

    Creates a Vindinium client configured for training mode and runs
    the bot specified in settings. The game replay URL is printed after completion.
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

    # Get the bot class
    try:
        BotClass = get_bot_class(settings.BOT)
    except ValueError as e:
        print(f"\nError: {e}")
        return

    # Create a vindinium client using settings from .env
    client = vindinium.Client(
        server=settings.SERVER,
        key=settings.KEY,
        mode=settings.MODE,
        n_turns=settings.N_TURNS,
        open_browser=settings.OPEN_BROWSER,
        debug=settings.DEBUG,
    )

    print(f"\nStarting game with {settings.HERO_NAME} using {settings.BOT}...")
    url = client.run(BotClass())
    print(f"\nReplay at: {url}")


if __name__ == "__main__":
    main()
