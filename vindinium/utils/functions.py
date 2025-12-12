"""Utility functions for direction/command conversion and distance calculations.

This module provides helper functions for converting between directions and commands,
calculating distances, and ordering objects by distance.
"""

import vindinium

__all__ = [
    'dir_to_command',
    'command_to_dir',
    'path_to_command',
    'distance_manhattan',
    'order_by_distance',
]


def dir_to_command(dx, dy):
    """Convert a direction to a command.

    Args:
        dx (int): Direction on the X axis, must be 1, 0 or -1.
        dy (int): Direction on the Y axis, must be 1, 0 or -1.

    Returns:
        str: A command string ('North', 'South', 'East', 'West', 'Stay').

    Raises:
        ValueError: If direction is invalid.
    """
    if dx == -1 and dy == 0:
        return vindinium.WEST
    elif dx == 1 and dy == 0:
        return vindinium.EAST
    elif dx == 0 and dy == -1:
        return vindinium.NORTH
    elif dx == 0 and dy == 1:
        return vindinium.SOUTH
    elif dx == 0 and dy == 0:
        return vindinium.STAY

    raise ValueError('Invalid direction (%s, %s).' % (dx, dy))


def command_to_dir(command):
    """Convert a command to a direction.

    Args:
        command (str): The command string.

    Returns:
        tuple: A tuple (dx, dy) with the direction.

    Raises:
        ValueError: If command is invalid.
    """
    if command == vindinium.NORTH:
        return vindinium.DIR_NORTH
    elif command == vindinium.SOUTH:
        return vindinium.DIR_SOUTH
    elif command == vindinium.WEST:
        return vindinium.DIR_WEST
    elif command == vindinium.EAST:
        return vindinium.DIR_EAST
    elif command == vindinium.STAY:
        return vindinium.DIR_STAY

    raise ValueError('Invalid command "%s".' % command)


def path_to_command(x0, y0, x1, y1):
    """Convert adjacent positions to a command.

    Args:
        x0 (int): Initial position on the X axis.
        y0 (int): Initial position on the Y axis.
        x1 (int): Final position on the X axis.
        y1 (int): Final position on the Y axis.

    Returns:
        str: A command string.

    Raises:
        ValueError: If direction is invalid.
    """
    dx = x1 - x0
    dy = y1 - y0
    return dir_to_command(dx, dy)


def distance_manhattan(x0, y0, x1, y1):
    """Compute the Manhattan distance between two points.

    Args:
        x0 (int): Initial position on the X axis.
        y0 (int): Initial position on the Y axis.
        x1 (int): Final position on the X axis.
        y1 (int): Final position on the Y axis.

    Returns:
        int: The Manhattan distance.
    """
    return abs(x0 - x1) + abs(y0 - y1)


def order_by_distance(x, y, objects):
    """Return a list of objects ordered by distance from a given point.

    You can use this to order mines or taverns by their distances from the hero.

    Args:
        x (int): Position on the X axis.
        y (int): Position on the Y axis.
        objects (list): List of objects. The objects must have ``x`` and ``y`` attributes.

    Returns:
        list: An ordered copy of ``objects``.
    """
    return sorted(objects, key=lambda item: distance_manhattan(x, y, item.x, item.y))


