"""Bot implementations for Vindinium.

This package contains various bot implementations ranging from simple
random bots to more sophisticated AI-based bots using pathfinding and
game tree search algorithms.
"""

from .raw_bot import *
from .base_bot import *
from .random_bot import *

# simple bots
from .miner_bot import *
from .aggressive_bot import *

# smart bots
from .minimax_bot import *

# charming mole
from .charming_mole import *
from .charming_mole_v1 import *
from .charming_mole_v1_minimax import *
