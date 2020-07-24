import numpy as np
from kaggle_environments.envs.halite.helpers import Point

from resources.actor_scored_resource import ActorScoredResource
from resources.tactic.go_to_resource import GoToResource
from utils.board_utils import manhattan_distance
from utils.entity_utils import CellList
from utils.global_vars import GLOBALS


def show_matrix(m):
    np.set_printoptions(edgeitems=30, linewidth=100000, formatter=dict(float=lambda x: "%.3g" % x))
    print(np.flip(m.T, axis=0))


class MineGoToResource(ActorScoredResource, GoToResource):
    @classmethod
    def initialize_once(cls):
        # TODO: make faster
        board_size = GLOBALS['config'].size
        cls.manhattan_distances = np.array([manhattan_distance(Point(x1, y1), Point(x2, y2))
                                            for x1 in range(board_size)
                                            for y1 in range(board_size)
                                            for x2 in range(board_size)
                                            for y2 in range(board_size)
                                            ], dtype=int).reshape(board_size, board_size, board_size, board_size)

    @classmethod
    def initialize_turn(cls):
        config = GLOBALS['config']

        board_size = config.size
        max_distance = board_size
        cls.cells_halite = np.zeros((board_size, board_size, max_distance))
        for cell in CellList.all():
            position = cell.position
            x, y = position.x, position.y
            cls.cells_halite[x, y, :] = cell.halite

        growth_factor = (1 + config.regen_rate) ** np.arange(max_distance)

        cls.cells_halite = cls.cells_halite * growth_factor
        cls.cells_halite = np.clip(cls.cells_halite, 0, config.max_cell_halite)

    @classmethod
    def instances(cls, actor_groups):
        return [MineGoToResource(cell) for cell in cls.cells()]

    @classmethod
    def actor_scores(cls, actor, instances):
        board_size = GLOBALS['config'].size

        position = actor.position
        x, y = position.x, position.y

        distances_from_actor = cls.manhattan_distances[x, y]

        yy, xx = np.meshgrid(np.arange(board_size), np.arange(board_size))
        # TODO: understand why replacing xx and yy was needed
        cells_halite_on_arrival = cls.cells_halite[xx, yy, distances_from_actor]

        max_stay = 20
        discount_factor = 0.8
        collect_rate = GLOBALS['config'].collect_rate

        geometric = 1 - ((1 - collect_rate) ** np.arange(1, max_stay))

        cells_halite_collected = cells_halite_on_arrival[:, :, np.newaxis] * geometric

        turns_to_the_future = distances_from_actor[:, :, np.newaxis] + np.arange(1, max_stay)

        average_halite_collected_per_turn = cells_halite_collected / turns_to_the_future \
            # * discount_factor ** turns_to_the_future

        max_average_halite_collected_per_turn = average_halite_collected_per_turn.max(axis=2).astype(int)

        # show_matrix(cls.cells_halite[:, :, 0].astype(int))
        # show_matrix(cells_halite_on_arrival.astype(int))
        # show_matrix(distances_from_actor)
        # show_matrix(max_average_halite_collected_per_turn)

        return [
            max_average_halite_collected_per_turn[instance.cell.position.x, instance.cell.position.y]
            for instance in instances
        ]

    @classmethod
    def cells(cls):
        return CellList.all()

    # TODO: implement using numpy 4d tensor
    # @classmethod
    # def score_matrix(cls, actor_groups, instances):
    #     pass
