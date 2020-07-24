from resources.actor_scored_resource import ActorScoredResource
from resources.tactic.go_to_resource import GoToResource
from utils.board_utils import manhattan_distance
from utils.entity_utils import ActorList


class DepositGoToResource(ActorScoredResource, GoToResource):
    # TODO: move magic number to config
    MAX_DEPOSITS_PER_SHIPYARD = 5

    @classmethod
    def instances(cls, actor_groups):
        return [DepositGoToResource(cell) for cell in cls.cells()]

    @classmethod
    def cells(cls):
        return [a.entity.cell for a in
                ActorList.all().friendly.shipyards] * DepositGoToResource.MAX_DEPOSITS_PER_SHIPYARD

    @classmethod
    def actor_scores(cls, actor, instances):
        return [-manhattan_distance(instance.cell.position, actor.position) for instance in instances]
