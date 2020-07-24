import math
from functools import partial

import numpy as np
from kaggle_environments.envs.halite.helpers import ShipAction, Point

from utils.global_vars import GLOBALS

SHIP_MOVEMENT_ACTIONS = ShipAction.moves()


def singed_mod_diff(x1, x2, mod):
    max_x = max(x1, x2)
    min_x = min(x1, x2)
    d1 = max_x - min_x
    d2 = mod - d1
    if d1 < d2:
        return math.copysign(1, x2 - x1) * d1
    else:
        return math.copysign(1, x1 - x2) * d2


def diff_vector(point1, point2):
    """
    Get shortest difference vector point2 - point1
    :param point1:
    :param point2:
    :return: tuple (diff_x, diff_y)
    """
    return point1.map2(point2, partial(singed_mod_diff, mod=GLOBALS['config'].size))


def abs_xy_distances(point1, point2):
    """
    Get minimal distances in each axis
    :param point1:
    :param point2:
    :return: tuple (distance_x, distance_y)
    """
    return abs(diff_vector(point1, point2))


def manhattan_distance(point1, point2):
    """
    :param point1:
    :param point2:
    :return: manhattan distance between two points
    """
    return sum(abs_xy_distances(point1, point2))


def euclidean_distance(point1, point2):
    """
    :param point1:
    :param point2:
    :return: euclidean distance between two points
    """
    dx, dy = abs_xy_distances(point1, point2)
    return dx ** 2 + dy ** 2


def infinity_distance(point1, point2):
    """
    :param point1:
    :param point2:
    :return: infinity distance between two points
    """
    return max(abs_xy_distances(point1, point2))


def cells_within_distance(cell, distance, distance_fn):
    my_position = cell.position
    fov_xs = np.arange(0, GLOBALS['config'].size)
    fov_ys = np.arange(0, GLOBALS['config'].size)
    fov_points = [Point(x, y) for x in fov_xs for y in fov_ys if
                  distance_fn(Point(x, y), my_position) <= distance]
    return [GLOBALS['board'].cells[point] for point in fov_points]


def cell_within_euclidean_distance(cell, distance):
    """
    :param cell:
    :param distance:
    :return: all cells with (euclidean distance) <= distance from given cell
    """
    return cells_within_distance(cell, distance, euclidean_distance)


def cell_within_infinity_distance(cell, distance):
    """
    :param cell:
    :param distance:
    :return: all cells with (infinity distance) <= fov from given cell
    """
    return cells_within_distance(cell, distance, infinity_distance)


def cell_within_manhattan_distance(cell, distance):
    """
    :param cell:
    :param distance:
    :return: all cells with (manhattan distance) <= fov from given cell
    """
    return cells_within_distance(cell, distance, manhattan_distance)


def get_neighbors(point):
    return [(point + movement.to_point()) % GLOBALS['config'].size for movement in SHIP_MOVEMENT_ACTIONS]


def get_neighbor_cells(cell):
    return [GLOBALS['board'].cells[p] for p in get_neighbors(cell.position)]


def get_movements_and_neighbors(point):
    return [(movement, (point + movement.to_point()) % GLOBALS['config'].size) for movement in SHIP_MOVEMENT_ACTIONS]


def future_halite_in_cell(cell, steps):
    return min(cell.halite * (1 + GLOBALS['config'].regen_rate) ** steps, GLOBALS['config'].max_cell_halite)


def point_to_ship_action(point):
    return {
        Point(0, 0): None,
        Point(0, 1): ShipAction.NORTH,
        Point(1, 0): ShipAction.EAST,
        Point(0, -1): ShipAction.SOUTH,
        Point(-1, 0): ShipAction.WEST,
    }[point]
