import random
from enum import Enum, auto
from random import choice

from kaggle_environments.envs.halite.helpers import ShipAction

from actors.actor import Actor
from utils.board_utils import cell_within_manhattan_distance, CellList, best_cell_heuristic, manhattan_distance
from utils.movement_utils import keep_distance_move, radial_move


class ShipActor(Actor):
    class FOVTypes(Enum):
        FLEE_FOV = auto()
        KEEP_DISTANCE_FOV = auto()
        SHIPYARD_FOV = auto()
        HALITE_COLLECTION_FOV = auto()

        @staticmethod
        def get_default():
            return {
                ShipActor.FOVTypes.FLEE_FOV: 2,
                ShipActor.FOVTypes.KEEP_DISTANCE_FOV: 2,
                ShipActor.FOVTypes.SHIPYARD_FOV: 12,
                ShipActor.FOVTypes.HALITE_COLLECTION_FOV: 5
            }

    # TODO: change epsilon to sensible value
    def __init__(self, entity, epsilon=0.1, fovs=None):
        """
        :param entity: the entity this actor represents
        :param epsilon: the probability for performing a random action
        :param fovs:
        """
        super().__init__(entity)
        if fovs is None:
            fovs = ShipActor.FOVTypes.get_default()
        self.epsilon = epsilon
        self.fovs = fovs

    def normal_mode(self, board):
        # TODO: remove magic number (replace with parameter) and magic string (replace with enum)
        if self.entity.halite >= 700:
            self.mode = 'DEPOSIT'

        if random.random() < self.epsilon:
            return choice(
                [ShipAction.NORTH, ShipAction.EAST, ShipAction.SOUTH, ShipAction.WEST, None]
            )

        all_entities = CellList(board.cells.values()).entity_list

        fovs_cells = {
            fov_type: CellList(cell_within_manhattan_distance(board,
                                                              self.entity.cell,
                                                              fov_size,
                                                              board.configuration))
            for fov_type, fov_size in self.fovs.items()
        }

        if fovs_cells[ShipActor.FOVTypes.SHIPYARD_FOV] \
                .entity_list \
                .amount(friendly_only=True, entity_types=['shipyard']) < 1:
            # Convert to shipyard
            return ShipAction.CONVERT
        elif fovs_cells[ShipActor.FOVTypes.KEEP_DISTANCE_FOV] \
                .entity_list \
                .amount(friendly_only=True, entity_types=['ship'], excluded_ids=[self.entity.id]) > 0 \
                or fovs_cells[ShipActor.FOVTypes.FLEE_FOV] \
                .entity_list \
                .amount(enemy_only=True, entity_types=['ship']) > 0:
            # Keep distance from friendly
            return keep_distance_move(self.entity.position,
                                      all_entities.filter(entity_types=['ship'],
                                                          excluded_ids=[self.entity.id]).positions,
                                      board.configuration)
        else:
            # Use heuristic to go to best cell to mine halite
            best_cell = best_cell_heuristic(self.entity.position,
                                            fovs_cells[ShipActor.FOVTypes.HALITE_COLLECTION_FOV],
                                            board.configuration)
            return radial_move(self.entity.position, best_cell.position, board.configuration)

    def deposit(self, board):
        # TODO: don't use normal mode like this
        if self.entity.halite == 0:
            self.mode = 'NORMAL'
            return self.normal_mode(board)
        all_entities = CellList(board.cells.values()).entity_list
        friendly_shipyards = all_entities.filter(friendly_only=True, entity_types=['shipyard'])
        if len(friendly_shipyards) < 1:
            return ShipAction.CONVERT
        nearest_shipyard = min(friendly_shipyards, key=lambda s: manhattan_distance(self.entity.position,
                                                                                    s.position,
                                                                                    board.configuration))
        return radial_move(self.entity.position, nearest_shipyard.position, board.configuration)

    def define_modes(self):
        modes = {
            'NORMAL': self.normal_mode,
            'DEPOSIT': self.deposit,
        }

        default_mode = 'NORMAL'

        return modes, default_mode
