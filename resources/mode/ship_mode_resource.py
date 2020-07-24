from enum import auto

from resources.actor_scored_resource import ActorScoredResource
from resources.mode.mode_resource import ModeResource, ModeType
from utils.board_utils import manhattan_distance
from utils.entity_utils import ActorList, EntityList
from utils.global_vars import GLOBALS


class ShipModeType(ModeType):
    COLLECT = auto()
    ATTACK = auto()
    CONVERT = auto()


def can_convert(ship):
    board = GLOBALS['board']
    config = GLOBALS['config']
    return ship.halite + board.current_player.halite >= config.spawn_cost


class ShipModeResource(ActorScoredResource, ModeResource):
    Type = ShipModeType

    def __init__(self, mode_type):
        super().__init__(mode_type)

    @classmethod
    def relevant_actors(cls, actor_groups):
        return actor_groups.ships

    @classmethod
    def instances(cls, actor_groups):
        return [ShipModeResource(entity_mode) for entity_mode in ShipModeType]

    @classmethod
    def repeats(cls, actor_groups, instances):
        shipyard_count = len(ActorList.all().friendly.shipyards)
        ship_count = len(ActorList.all().friendly.ships)
        board = GLOBALS['board']

        n_convert = 0
        if shipyard_count < max(1, (ship_count - 2) // 7 + 1) > 0 \
                and any([can_convert(ship) for ship in EntityList.all().friendly.ships]):
            n_convert = 1

        n_act = len(actor_groups) - n_convert
        # TODO: decide when to attack
        n_collect = n_act
        n_attack = 0
        return [n_collect, n_attack, n_convert]

    @classmethod
    def actor_scores(cls, actor, resources):

        convert_score = - 99999

        if can_convert(actor.entity):
            friendly_shipyard = ActorList.all().friendly.shipyards
            if len(friendly_shipyard) > 0:
                convert_score = min(
                    [manhattan_distance(actor.entity.position, shipyard.position)
                     for shipyard in friendly_shipyard]
                )
            else:
                convert_score = 1

        return [0, 0, convert_score]
