"""Main entry point for running a Vindinium bot.

This module provides a simple example of how to create and run a bot
using the vindinium client library.
"""

import vindinium


def main():
    """Run a MinerBot in training mode.

    Creates a Vindinium client configured for training mode and runs
    a MinerBot instance. The game replay URL is printed after completion.
    """
    # Create a vindinium client
    client = vindinium.Client(
        server="http://localhost:9000",
        key="<my key>",
        mode="training",
        n_turns=300,
        open_browser=True,
    )

    url = client.run(vindinium.bots.MinerBot())
    print("Replay in:", url)


if __name__ == "__main__":
    main()
