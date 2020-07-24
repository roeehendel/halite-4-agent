from abc import abstractmethod
from enum import Enum

from resources.resource import Resource


class ModeType(Enum):
    pass


class ModeResource(Resource):
    Type = None

    def __init__(self, mode_type):
        super().__init__()
        self.mode_type = mode_type

    @classmethod
    @abstractmethod
    def instances(cls, actor_groups):
        pass

    @classmethod
    @abstractmethod
    def repeats(cls, actor_groups, instances):
        pass

    @classmethod
    @abstractmethod
    def score_matrix(cls, actor_groups, instances):
        pass

    @classmethod
    def assign_to_actor(cls, actor, resource):
        actor.modes.append(resource)
