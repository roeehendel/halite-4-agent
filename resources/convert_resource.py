import random

from kaggle_environments.envs.halite.helpers import ShipAction

from resources.resource import Resource
from utils.board_utils import manhattan_distance
from utils.entity_utils import EntityList, EntityType


class ConvertResource(Resource):
    def __init__(self, board):
        super().__init__(board)

    def _resolve_collision(self):
        can_convert_actors = list(
            filter(
                lambda actor:
                actor.entity.halite + self.board.current_player.halite >= self.board.configuration.spawn_cost,
                self.requested_by
            )
        )

        if len(can_convert_actors) < 1:
            return None

        friendly_shipyards = EntityList.all_entities(self.board).filter(friendly_only=True,
                                                                        entity_types=[EntityType.SHIPYARD])

        if len(friendly_shipyards) == 0:
            return max(can_convert_actors, key=lambda actor: actor.entity.halite)

        chosen_actor = max(can_convert_actors, key=lambda actor: min(
            [manhattan_distance(actor.entity.position, shipyard.position, self.board.configuration)
             for shipyard in friendly_shipyards]
        ))

        return chosen_actor

    def score(self, actor, **kwargs):
        return 0

    @classmethod
    def _resource_instances(cls, board):
        return [ConvertResource(board)]

    def use(self, actor):
        actor.entity.next_action = ShipAction.CONVERT
