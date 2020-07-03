from resources.resource import Resource
from utils.board_utils import manhattan_distance
from utils.entity_utils import EntityList, EntityType


class DepositResource(Resource):
    def __init__(self, board, shipyard):
        super().__init__(board)
        self.shipyard = shipyard

    def _resolve_collision(self):
        pass

    def score(self, actor, **kwargs):
        return manhattan_distance(actor.position, self.shipyard.position, self.board.configuration)

    @classmethod
    def _get_resource_instances(cls, board):
        shipyards = EntityList.all_entities(board).filter(entity_types=[EntityType.SHIPYARD], friendly_only=True)
        return [DepositResource(board, shipyard) for shipyard in shipyards]
