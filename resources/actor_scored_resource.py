from abc import abstractmethod

import numpy as np

from resources.resource import Resource


class ActorScoredResource(Resource):
    @classmethod
    @abstractmethod
    def instances(cls, actor_groups):
        pass

    @classmethod
    @abstractmethod
    def actor_scores(cls, actor, instances):
        pass

    @classmethod
    def score_matrix(cls, actor_groups, instances):
        return np.array([cls.actor_scores(actor_group[0], instances) for actor_group in actor_groups])
