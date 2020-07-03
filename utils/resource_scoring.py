from utils.board_utils import manhattan_distance, future_halite_in_cell


# def occupy_cell_resource_score(occupy_cell_resource, destination_position, config, distance_fn=manhattan_distance):
#     return - distance_fn(occupy_cell_resource.cell.position, destination_position, config)

# def mine_cell_resource_score(mine_cell_resource, current_position, config):
#     cell = mine_cell_resource.cell
#
#     distance_to_cell = manhattan_distance(current_position, cell.position, config)
#     cell_halite = future_halite_in_cell(cell, distance_to_cell, config)
#
#     collected_turns = 1
#     collected_halite = config.collect_rate * cell_halite
#     max_reward = collected_halite / (distance_to_cell + collected_turns)
#     remaining_cell_halite = cell_halite - collected_halite
#
#     min_cell_halite = 30
#     # TODO: verify no bugs
#     while remaining_cell_halite > min_cell_halite:
#         collected_turns += 1
#         collected_halite += config.collect_rate * remaining_cell_halite
#         max_reward = max(max_reward, collected_halite / (distance_to_cell + collected_turns))
#         remaining_cell_halite = cell_halite - collected_halite
#     return max_reward
