from utils.board_utils import euclidean_distance, get_movements_and_neighbors, manhattan_distance, SHIP_MOVEMENT_ACTIONS
from utils.global_vars import GLOBALS


# TODO: move by distance_fn

def radial_move(current_point, destination_position):
    """
    Get the ShipAction movement that gets you closest to the destination (in euclidean distance)
    :param current_point:
    :param destination_position:
    :return: ShipAction
    """

    if current_point == destination_position:
        return None

    neighbors = get_movements_and_neighbors(current_point)
    return min([(movement, manhattan_distance(neighbor, destination_position))
                for movement, neighbor in neighbors], key=lambda x: x[1])[0]


def keep_distance_move(current_point, entities_positions):
    """
    Get the ShipAction movement that gets you farthest from all given entities (in euclidean distance)
    :param current_point:
    :param entities_positions:
    :return:
    """

    neighbors = get_movements_and_neighbors(current_point)

    distances = [GLOBALS['config'].size ** 2] * 4

    for entity_position in entities_positions:
        distances = [min(distances[i], euclidean_distance(neighbors[i][1], entity_position)) for i in
                     range(len(SHIP_MOVEMENT_ACTIONS))]

    index = distances.index(max(distances))
    return SHIP_MOVEMENT_ACTIONS[index]
