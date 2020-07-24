import numpy as np
from kaggle_environments.envs.halite.helpers import ShipyardAction

from resources.action.action_resource import ActionResource


class SpawnActionResource(ActionResource):
    def use(self, actor):
        actor.entity.next_action = ShipyardAction.SPAWN

    @classmethod
    def instances(cls, actor_groups):
        return [SpawnActionResource()]

    @classmethod
    def score_matrix(cls, actor_groups, instances):
        return np.zeros((len(actor_groups), len(instances)))
