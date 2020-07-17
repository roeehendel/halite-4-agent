import numpy as np
from scipy.optimize import linear_sum_assignment


def bipartite_match(score_matrix, repeats):
    repeated_idx = np.repeat(np.arange(score_matrix.shape[1]), repeats=repeats, axis=1)
    repeated_score_matrix = np.repeat(score_matrix, repeats=repeats, axis=1)
    row_ind, col_ind = linear_sum_assignment(repeated_score_matrix)

    return repeated_idx[col_ind]


class Resource:
    def __init__(self):
        pass

    @classmethod
    def score_matrix(cls, actors):
        raise NotImplementedError

    @classmethod
    def group_actors(cls, actors):
        return [[a] for a in actors]

    @classmethod
    def assign_to_actor(cls, actor, resource):
        actor.resources.append(resource)

    @classmethod
    def allocate(cls, actors):
        actor_groups = cls.group_actors(actors)
        # Create score matrix
        score_matrix, repeats, resources = cls.score_matrix(actor_groups)
        # Bipartite matching
        matching = bipartite_match(score_matrix, repeats)
        # Allocate resources to actors
        for i, actor_group in enumerate(actor_groups):
            for actor in actor_group:
                cls.assign_to_actor(actor, resources[matching[i]])
