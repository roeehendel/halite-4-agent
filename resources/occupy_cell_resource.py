import math
import random

from kaggle_environments.envs.halite.helpers import ShipAction

from resources.resource import Resource
from utils.board_utils import manhattan_distance, point_to_ship_action


class OccupyCellResource(Resource):
    def __init__(self, board, cell):
        super().__init__(board)
        self.cell = cell
        self.destination_position = None

    def score(self, actor, **kwargs):
        distance_fn = kwargs.get('distance_fn', manhattan_distance)
        self.destination_position = kwargs['destination_position']()

        if manhattan_distance(self.cell.position, actor.position, self.board.configuration) > 1:
            return - math.inf

        return - distance_fn(self.cell.position, self.destination_position, self.board.configuration)

    def _resolve_collision(self):
        return random.choice(self.requested_by)

    @classmethod
    def _get_resource_instances(cls, board):
        return [OccupyCellResource(board, cell) for cell in board.cells.values()]

    def use(self, actor):
        direction = (self.cell.position - actor.position)
        # print(self.cell.position, actor.position, (self.cell.position - actor.position), direction)
        action = point_to_ship_action(direction)
        actor.entity.next_action = action
