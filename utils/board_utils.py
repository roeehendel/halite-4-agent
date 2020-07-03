import numpy as np
from kaggle_environments.envs.halite.helpers import ShipAction, Point, Ship, Shipyard

# TODO: make this less ugly
SHIP_MOVEMENT_ACTIONS = list(ShipAction)[:4]


def get_xy_distances(point1, point2, config):
    """
    Get minimal distances in each axis
    :param point1:
    :param point2:
    :param config:
    :return: tuple (distance_x, distance_y)
    """
    max_x = max(point1.x, point2.x)
    min_x = min(point1.x, point2.x)
    distance_x = min(max_x - min_x, min_x - max_x + config.size)

    max_y = max(point1.y, point2.y)
    min_y = min(point1.y, point2.y)
    distance_y = min(max_y - min_y, min_y - max_y + config.size)

    return distance_x, distance_y


def manhattan_distance(point1, point2, config):
    """
    :param point1:
    :param point2:
    :param config: the board size
    :return: manhattan distance between two points
    """
    return sum(get_xy_distances(point1, point2, config))


def euclidean_distance(point1, point2, config):
    """
    :param point1:
    :param point2:
    :param config: the board size
    :return: euclidean distance between two points
    """
    return np.linalg.norm(get_xy_distances(point1, point2, config))


def infinity_distance(point1, point2, config):
    """
    :param point1:
    :param point2:
    :param config: the board size
    :return: infinity distance between two points
    """
    return max(get_xy_distances(point1, point2, config))


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
