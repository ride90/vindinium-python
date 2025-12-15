"""Vindinium HTTP client for connecting to the game server.

This module provides the Client class which handles all communication
with the Vindinium server, including game initialization and move submission.
"""

import logging
import time
import webbrowser
import requests

__all__ = ["Client"]


class Client:
    """Base client for Vindinium.

    Example:
        Pass the configuration within constructor::

            client = vindinium.Client('<botskey>', mode='training')

        Or manually set the client attributes::

            client = vindinium.Client()
            client.key = '<botskey>'
            client.mode = 'training'

        Finally, run the bot passing it as parameter to the ``run`` method::

            client.run(MyBot())

    Attributes:
        key (str): the bot's key, you must create a key on your Vindinium server.
        mode (str): the game mode ('training' or 'arena'), defaults to 'training'.
        n_turns (int): number of turns in a game. Only valid in training mode;
          arena is fixed to 300. Defaults to 300.
        server (str): the address of the Vindinium server. Required parameter.
        open_browser (bool): if True, the client will open the default browser
          to show the current game. Defaults to False.
        timeout_move (int): movement timeout in seconds. Defaults to 15 seconds.
        timeout_connection (int): connection timeout in seconds. Defaults to 10
          minutes.
    """

    def __init__(
        self,
        key,
        mode="training",
        n_turns=300,
        server=None,
        open_browser=False,
        debug=False,
    ):
        """Constructor.

        Args:
            key (str): the bot's key, you must create a key on your Vindinium server.
            mode (str): the game mode ('training' or 'arena'), defaults to
             'training'.
            n_turns (int): number of turns in a game. Only valid in training
              mode; arena is fixed to 300. Defaults to 300.
            server (str): the address of the Vindinium server. Required parameter.
            open_browser (bool): if True, the client will open the default
              browser to show the current game. Defaults to False.
            debug (bool): if True, logs each move and timing information. Defaults to False.
        """

        if server is None:
            raise ValueError(
                "Server URL is required. Please provide the server parameter "
                "or use settings.SERVER from your .env configuration."
            )

        self.key = key
        self.mode = mode
        self.n_turns = n_turns
        self.server = server
        self.open_browser = open_browser
        self.debug = debug
        self.timeout_move = 15
        self.timeout_connection = 30 * 60

        self._session = None

    def run(self, bot):
        """Connects to the server waiting for a game.

        Args:
            bot (instance): the bot object.

        Returns:
            A url to watch the game replay.
        """
        try:
            # Connect
            state = self._connect()
            bot.start(state)
            play_url = state["playUrl"]

            # Move
            finished = False
            turn = 0
            while not finished:
                turn += 1

                # Time the bot's move (only if debug is enabled)
                if self.debug:
                    start_time = time.time()

                action = bot.move(state)

                if self.debug:
                    elapsed_time = time.time() - start_time

                state = self._send_move(play_url, action)

                # Debug logging
                if self.debug:
                    print(f"Turn {turn}: {action} (took {elapsed_time:.3f}s)")

                finished = state["game"]["finished"]

            return state["viewUrl"]

        finally:
            # End
            bot.end()
            self._disconnect()

    def _connect(self):
        """Connects to the server.

        Returns:
            A data from the server

        Raises:
            IOError if connection is aborted.
        """

        # Create requests session
        self._session = requests.session()

        # Set up parameters
        server = self.server
        if self.mode == "arena":
            params = {"key": self.key}
            endpoint = "/api/arena"
        else:
            params = {"key": self.key, "turns": self.n_turns, "map": "m2"}
            endpoint = "/api/training"

        # Connect
        logging.info("Trying to connect to %s%s", server, endpoint)
        r = self._session.post(server + endpoint, params, timeout=self.timeout_connection)

        # Get response
        if r.status_code == 200:
            state = r.json()
            logging.info("Connected! Playing game at: %s", state["viewUrl"])

            # Open browser if ``open_browser`` is True
            if self.open_browser:
                webbrowser.open(state["viewUrl"])

            return state
        else:
            logging.error('Error when connecting to server, message: "%s"', r.text)
            raise IOError("Connection error, check log for the message.")

    def _send_move(self, url, action):
        """Sends a movement command to the server.

        Returns:
            A data from the server

        Raises:
            IOError if connection is aborted.
        """

        r = self._session.post(url, {"dir": action}, timeout=self.timeout_move)

        if r.status_code == 200:
            return r.json()

        else:
            logging.error(
                'Connection error during game, message: "(%d) %s"',
                r.status_code,
                r.text,
            )
            raise IOError("Connection error, check log for the message.")

    def _disconnect(self):
        """Close the session.

        Properly closes the HTTP session to free up resources.
        """
        if self._session:
            self._session.close()
