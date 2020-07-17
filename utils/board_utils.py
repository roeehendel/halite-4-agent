import math
from functools import partial

import numpy as np
from kaggle_environments.envs.halite.helpers import ShipAction, Point, Ship, Shipyard

# TODO: make this less ugly
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


def diff_vector(point1, point2, config):
    """
    Get shortest difference vector point2 - point1
    :param point1:
    :param point2:
    :param config:
    :return: tuple (diff_x, diff_y)
    """
    return point1.map2(point2, partial(singed_mod_diff, mod=config.size))


def abs_xy_distances(point1, point2, config):
    """
    Get minimal distances in each axis
    :param point1:
    :param point2:
    :param config:
    :return: tuple (distance_x, distance_y)
    """
    # print(point1, point2, diff_vector(point1, point2, config), abs(diff_vector(point1, point2, config)))
    return abs(diff_vector(point1, point2, config))


def manhattan_distance(point1, point2, config):
    """
    :param point1:
    :param point2:
    :param config: the board size
    :return: manhattan distance between two points
    """
    return sum(abs_xy_distances(point1, point2, config))


def euclidean_distance(point1, point2, config):
    """
    :param point1:
    :param point2:
    :param config: the board size
    :return: euclidean distance between two points
    """
    dx, dy = abs_xy_distances(point1, point2, config)
    return dx ** 2 + dy ** 2


def infinity_distance(point1, point2, config):
    """
    :param point1:
    :param point2:
    :param config: the board size
    :return: infinity distance between two points
    """
    return max(abs_xy_distances(point1, point2, config))


def cells_within_distance(board, cell, distance, distance_fn, config):
    my_position = cell.position
    fov_xs = np.arange(0, config.size)
    fov_ys = np.arange(0, config.size)
    fov_points = [Point(x, y) for x in fov_xs for y in fov_ys if
                  distance_fn(Point(x, y), my_position, config) <= distance]
    return [board.cells[point] for point in fov_points]


def cell_within_euclidean_distance(board, cell, distance, config):
    """
    :param board:
    :param cell:
    :param distance:
    :param config: the board size
    :return: all cells with (euclidean distance) <= distance from given cell
    """
    return cells_within_distance(board, cell, distance, euclidean_distance, config)


def cell_within_infinity_distance(board, cell, distance, config):
    """
    :param board:
    :param cell:
    :param distance:
    :param config: the board size
    :return: all cells with (infinity distance) <= fov from given cell
    """
    return cells_within_distance(board, cell, distance, infinity_distance, config)


def cell_within_manhattan_distance(board, cell, distance, config):
    """
    :param board:
    :param cell:
    :param distance:
    :param config: the board size
    :return: all cells with (manhattan distance) <= fov from given cell
    """
    return cells_within_distance(board, cell, distance, manhattan_distance, config)


def get_neighbors(point, config):
    return [(point + movement.to_point()) % config.size for movement in SHIP_MOVEMENT_ACTIONS]


def get_neighbor_cells(cell, board):
    return [board.cells[p] for p in get_neighbors(cell.position, board.configuration)]


def get_movements_and_neighbors(point, config):
    return [(movement, (point + movement.to_point()) % config.size) for movement in SHIP_MOVEMENT_ACTIONS]


def future_halite_in_cell(cell, steps, config):
    return min(cell.halite * (1 + config.regen_rate) ** steps, config.max_cell_halite)


def point_to_ship_action(point):
    return {
        Point(0, 0): None,
        Point(0, 1): ShipAction.NORTH,
        Point(1, 0): ShipAction.EAST,
        Point(0, -1): ShipAction.SOUTH,
        Point(-1, 0): ShipAction.WEST,
    }[point]
