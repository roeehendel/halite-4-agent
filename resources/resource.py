from abc import ABC, abstractmethod

import numpy as np
from scipy.optimize import linear_sum_assignment

from utils.entity_utils import ActorGroupList


def bipartite_match(score_matrix, repeats):
    repeated_idx = np.repeat(np.arange(score_matrix.shape[1]), repeats=repeats)
    repeated_score_matrix = np.repeat(score_matrix, repeats=repeats, axis=1)
    row_ind, col_ind = linear_sum_assignment(repeated_score_matrix, maximize=True)

    return repeated_idx[col_ind]


class Resource(ABC):
    def __init__(self):
        pass

    @classmethod
    def initialize_turn(cls):
        pass

    @classmethod
    def group_actors(cls, actors):
        return ActorGroupList([[a] for a in actors])

    @classmethod
    def assign_to_actor(cls, actor, resource):
        actor.resources.append(resource)

    @classmethod
    @abstractmethod
    def instances(cls, actor_groups):
        pass

    @classmethod
    def repeats(cls, actor_groups, instances):
        return np.ones(len(instances), dtype=int)

    @classmethod
    @abstractmethod
    def score_matrix(cls, actor_groups, instances):
        pass

    @classmethod
    def relevant_actors(cls, actor_groups):
        return actor_groups

    @classmethod
    def allocate(cls, actors):
        # Group actors
        actor_groups = cls.group_actors(actors)
        actor_groups = cls.relevant_actors(actor_groups)

        # Create instances, repeats and score matrix
        instances = cls.instances(actor_groups)
        repeats = cls.repeats(actor_groups, instances)
        score_matrix = cls.score_matrix(actor_groups, instances)

        # Bipartite matching
        matching = bipartite_match(score_matrix, repeats)

        # Allocate resources to actors
        for i, actor_group in enumerate(actor_groups):
            for actor in actor_group:
                cls.assign_to_actor(actor, instances[matching[i]])
