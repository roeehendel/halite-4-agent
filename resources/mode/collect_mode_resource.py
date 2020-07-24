import math
from enum import auto

from resources.actor_scored_resource import ActorScoredResource
from resources.mode.mode_resource import ModeResource, ModeType
from resources.tactic.deposit_go_to_resource import DepositGoToResource
from utils.entity_utils import ActorList
from utils.global_vars import GLOBALS


class CollectModeType(ModeType):
    MINE = auto()
    DEPOSIT = auto()


class CollectModeResource(ActorScoredResource, ModeResource):
    Type = CollectModeType

    def __init__(self, mode_type):
        super().__init__(mode_type)

    @classmethod
    def instances(cls, actor_groups):
        return [CollectModeResource(CollectModeType.MINE), CollectModeResource(CollectModeType.DEPOSIT)]

    @classmethod
    def repeats(cls, actor_groups, instances):
        return [len(actor_groups),
                len(ActorList.all().friendly.shipyards) * DepositGoToResource.MAX_DEPOSITS_PER_SHIPYARD]

    @classmethod
    def actor_scores(cls, actor, instances):
        # TODO: move magic number to config
        # if actor.entity.halite > 200:
        #     return [0, 1]
        if actor.entity.halite > 200 * math.exp(-GLOBALS['board'].step / 200):
            return [0, 1]
        return [1, 0]
