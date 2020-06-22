import numpy as np
from kaggle_environments.envs.halite.helpers import ShipAction, Point, Ship, Shipyard

# TODO: make this less ugly
SHIP_MOVEMENT_ACTIONS = list(ShipAction)[:4]
ENTITY_NAME_TO_TYPE = {
    'ship': Ship,
    'shipyard': Shipyard
}
ENTITY_TYPE_TO_NAME = {v: k for k, v in ENTITY_NAME_TO_TYPE.items()}


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


class CellList(list):
    def __init__(self, cells):
        super().__init__(cells)

    @property
    def entity_list(self):
        return EntityList(
            filter(lambda x: x is not None, [cell.ship for cell in self] + [cell.shipyard for cell in self])
        )


class EntityList(list):
    def __init__(self, entities):
        super().__init__(entities)

    def nearest_entity_to(self, point, config, distance_fn=manhattan_distance):
        return min(self, key=lambda entity: distance_fn(entity.position, point, config))

    @property
    def positions(self):
        return [e.position for e in self]

    def filter(self, players=None, entity_types=('ship', 'shipyard'), friendly_only=False, enemy_only=False,
               excluded_ids=()):
        def predicate(e):
            return (players is None or e.player in players) and \
                   (ENTITY_TYPE_TO_NAME[type(e)] in entity_types) and \
                   (not friendly_only or e.player.is_current_player) and \
                   (not enemy_only or not e.player.is_current_player) and \
                   (e.id not in excluded_ids)

        return EntityList(list(filter(lambda e: predicate(e), self)))

    def amount(self, **kwargs):
        return len(self.filter(**kwargs))


def get_neighbors(point, config):
    return [(movement, (point + movement.to_point()) % config.size) for movement in SHIP_MOVEMENT_ACTIONS]


def future_halite_in_cell(cell, steps, config):
    return min(cell.halite * (1 + config.regen_rate) ** steps, config.max_cell_halite)


def cell_reward(current_position, cell, config):
    distance_to_cell = manhattan_distance(current_position, cell.position, config)
    cell_halite = future_halite_in_cell(cell, distance_to_cell, config)

    collected_turns = 1
    collected_halite = config.collect_rate * cell_halite
    max_reward = collected_halite / (distance_to_cell + collected_turns)
    remaining_cell_halite = cell_halite - collected_halite

    min_cell_halite = 30
    # TODO: verify no bugs
    while remaining_cell_halite > min_cell_halite:
        collected_turns += 1
        collected_halite += config.collect_rate * remaining_cell_halite
        max_reward = max(max_reward, collected_halite / (distance_to_cell + collected_turns))
        remaining_cell_halite = cell_halite - collected_halite
    return max_reward


def best_cell_heuristic(current_position, cells, config):
    """
    Use heuristic to find the best cell to go to from the given list of cells
    :param current_position:
    :param cells: list of cells to check
    :param config: the env configuration
    :return: return best point by heuristic
    """
    return max(cells, key=lambda cell: cell_reward(current_position, cell, config))
