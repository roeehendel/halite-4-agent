import random

from kaggle_environments.envs.halite.helpers import Shipyard, Ship

from resources.resource import Resource
from resources.spawn_resource import SpawnResource
from utils.board_utils import point_to_ship_action, diff_vector, euclidean_distance, \
    get_neighbors, get_neighbor_cells


class OccupyCellResource(Resource):
    def __init__(self, board, cell):
        super().__init__(board)
        self.cell = cell
        self.destination_position = None

    def __getitem__(self, item):
        return self.cell.position[item]

    def score(self, actor, **kwargs):
        if 'destination_position' in kwargs:
            if self.cell.position not in \
                    get_neighbors(actor.position, self.board.configuration) + [actor.position]:
                return None

            if self.cell.ship is not None and not self.cell.ship.player.is_current_player \
                    and self.cell.ship.halite <= actor.entity.halite:
                return - 2000

            neighbors = get_neighbor_cells(self.cell, self.board)
            if any([n.ship.halite <= actor.entity.halite for n in neighbors if
                    (n.ship is not None and not n.ship.player.is_current_player)]):
                return - 1000  # better then going straight into an enemy (?)

            distance_fn = kwargs.get('distance_fn', euclidean_distance)
            self.destination_position = kwargs['destination_position']()
            return - distance_fn(self.cell.position, self.destination_position, self.board.configuration)
        else:
            cell_position = kwargs['cell_position']()
            return 0 if cell_position == self.cell.position else None

    def _resolve_collision(self):
        # TODO: replace with a better mechanism
        # print([type(actor.entity) for actor in self.requested_by])
        # TODO: this is terrible, replace it with a proper resource dependency management
        shipyard_requests = list(
            filter(lambda actor: type(actor.entity) == Shipyard and actor.get_my_resource(SpawnResource) is not None,
                   self.requested_by))

        if len(shipyard_requests) > 0:
            # print('awarded to', shipyard_requests[0])
            return shipyard_requests[0]

        return random.choice(self.requested_by)

    @classmethod
    def _resource_instances(cls, board):
        return [OccupyCellResource(board, cell) for cell in board.cells.values() if
                (cell.shipyard is None or cell.shipyard.player.is_current_player)]

    def use(self, actor):
        if type(actor.entity) == Ship:
            direction = diff_vector(actor.position, self.cell.position, self.board.configuration)
            action = point_to_ship_action(direction)
            actor.entity.next_action = action
            # print(self.allocated_to)
            # print('ship used', self.cell.position)
        # else:
        # print(self.allocated_to)
        # print('shipyard used', self.cell.position)
        return True
