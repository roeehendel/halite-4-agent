from kaggle_environments.envs.halite.helpers import ShipAction

from resources.resource import Resource


class ConvertResource(Resource):
    def __init__(self, board):
        super().__init__(board)

    def _resolve_collision(self):
        pass

    def score(self, actor, **kwargs):
        return 0

    @classmethod
    def _get_resource_instances(cls, board):
        return [ConvertResource(board)]

    def use(self, actor):
        actor.entity.next_action = ShipAction.CONVERT
