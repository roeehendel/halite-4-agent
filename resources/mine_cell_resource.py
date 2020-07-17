from resources.resource import Resource
from utils.board_utils import manhattan_distance, future_halite_in_cell, get_movements_and_neighbors, get_neighbors


class MineCellResource(Resource):
    def __init__(self, board, cell):
        super().__init__(board)
        self.cell = cell

    def score(self, actor, **kwargs):
        config = self.board.configuration
        distance_fn = kwargs.get('distance_fn', manhattan_distance)

        distance_to_cell = distance_fn(actor.position, self.cell.position, config)
        cell_halite = future_halite_in_cell(self.cell, distance_to_cell, config)

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

    def _resolve_collision(self):
        nearest_actor = min(self.requested_by, key=lambda actor: manhattan_distance(self.cell.position,
                                                                                    actor.position,
                                                                                    self.board.configuration))
        return nearest_actor

    @classmethod
    def _resource_instances(cls, board):
        return [MineCellResource(board, cell) for cell in board.cells.values()]
