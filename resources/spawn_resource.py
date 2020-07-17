import random

from kaggle_environments.envs.halite.helpers import ShipAction, ShipyardAction

from resources.resource import Resource
from utils.board_utils import manhattan_distance
from utils.entity_utils import EntityList, EntityType


class SpawnResource(Resource):
    def __init__(self, board):
        super().__init__(board)

    def _resolve_collision(self):
        # TODO: replace with a better mechanism
        return random.choice(self.requested_by)

    def score(self, actor, **kwargs):
        return 0

    @classmethod
    def _resource_instances(cls, board):
        if board.current_player.halite >= board.configuration.spawn_cost:
            return [SpawnResource(board)]
        return []

    def use(self, actor):
        actor.entity.next_action = ShipyardAction.SPAWN
