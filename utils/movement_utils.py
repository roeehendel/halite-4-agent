import numpy as np
from kaggle_environments.envs.halite.helpers import ShipAction

from utils.board_utils import euclidean_distance, get_movements_and_neighbors, manhattan_distance, SHIP_MOVEMENT_ACTIONS


# TODO: move by distance_fn

def radial_move(current_point, destination_position, config):
    """
    Get the ShipAction movement that gets you closest to the destination (in euclidean distance)
    :param current_point:
    :param destination_position:
    :param board_size:
    :return: ShipAction
    """

    if current_point == destination_position:
        return None

    neighbors = get_movements_and_neighbors(current_point, config)
    return min([(movement, manhattan_distance(neighbor, destination_position, config))
                for movement, neighbor in neighbors], key=lambda x: x[1])[0]


def keep_distance_move(current_point, entities_positions, config):
    """
    Get the ShipAction movement that gets you farthest from all given entities (in euclidean distance)
    :param current_point:
    :param entities_positions:
    :param board_size:
    :return:
    """

    neighbors = get_movements_and_neighbors(current_point, config)

    distances = [config.size ** 2] * 4

    for entity_position in entities_positions:
        distances = [min(distances[i], euclidean_distance(neighbors[i][1], entity_position, config)) for i in
                     range(len(SHIP_MOVEMENT_ACTIONS))]

    index = distances.index(max(distances))
    return SHIP_MOVEMENT_ACTIONS[index]
