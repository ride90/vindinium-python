"""Awesome Python client for Vindinium.

Vindinium is an online and continuous competition where you control a bot in a
turn-based game. See https://vindinium.josefelixh.net/ for more information.

Note: This client is based on ornicar's client:
https://github.com/ornicar/vindinium-starter-python

This library provides several base and simple bots, helper structures and
common algorithms that allow you to create bots in an easy and fast way,
focusing on the strategy and specific techniques of your bot.

The library has the following features:

- Bots:
    - RawBot: A bot that does nothing.
    - BaseBot: A bot that processes the state and creates/updates a Game object.
    - RandomBot: A bot that performs random movements.
    - MinerBot: A bot that looks for mines continuously.
    - AggressiveBot: A bot that only goes after other bots.
    - MinimaxBot: A bot that uses minimax algorithm for decision making.

- Models (used by BaseBot to create the game structure):
    - Game: Stores all other models.
    - Map: Stores static information about the map.
    - Mine: Represents a mine on the map.
    - Hero: Represents a hero in the game.
    - Tavern: Represents a tavern in the game.

- AI algorithms (specialized for Vindinium):
    - AStar: The A* pathfinding algorithm.
    - Minimax: The minimax game tree search algorithm.

Note: This client fixes the inconsistent axis of the server, so you don't have to
worry about that (if you're using the game model).
"""

from .client import *
from . import bots
from . import models
from . import ai
from . import utils

# CONSTANTS
# Tile values
TILE_EMPTY = 0
TILE_WALL = 1
TILE_SPAWN = 2
TILE_TAVERN = 3
TILE_MINE = 4

# Command values
NORTH = 'North'
SOUTH = 'South'
WEST = 'West'
EAST = 'East'
STAY = 'Stay'

# Direction tuples
DIR_NORTH = (0, -1)
DIR_SOUTH = (0, 1)
DIR_WEST = (-1, 0)
DIR_EAST = (1, 0)
DIR_STAY = (0, 0)
