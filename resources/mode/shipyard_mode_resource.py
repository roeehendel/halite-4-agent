from enum import auto

from resources.actor_scored_resource import ActorScoredResource
from resources.mode.mode_resource import ModeResource, ModeType
from utils.entity_utils import EntityList
from utils.global_vars import GLOBALS


class ShipyardModeType(ModeType):
    SPAWN = auto()
    REST = auto()


class ShipyardModeResource(ActorScoredResource, ModeResource):
    Type = ShipyardModeType

    def __init__(self, mode_type):
        super().__init__(mode_type)

    @classmethod
    def relevant_actors(cls, actor_groups):
        return actor_groups.shipyards

    @classmethod
    def instances(cls, actor_groups):
        return [ShipyardModeResource(entity_mode) for entity_mode in ShipyardModeType]

    @classmethod
    def repeats(cls, actor_groups, instances):
        board = GLOBALS['board']
        config = GLOBALS['config']

        should_spawn = board.step < 370 \
                       and len(EntityList.all().friendly.ships) < min(board.step // 10 + 10, 30 - board.step // 20) \
                       and board.current_player.halite >= config.spawn_cost

        if should_spawn:
            return [1, len(actor_groups) - 1]
        else:
            return [0, len(actor_groups)]

    @classmethod
    def actor_scores(cls, actor, instances):
        return [1, 0]
