import numpy as np
from kaggle_environments.envs.halite.helpers import ShipAction

from resources.action.action_resource import ActionResource


class ConvertActionResource(ActionResource):
    def use(self, actor):
        actor.entity.next_action = ShipAction.CONVERT

    @classmethod
    def instances(cls, actor_groups):
        return [ConvertActionResource()]

    @classmethod
    def score_matrix(cls, actor_groups, instances):
        return np.zeros((len(actor_groups), len(instances)))
