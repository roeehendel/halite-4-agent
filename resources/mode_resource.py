from enum import Enum, auto

from resources.resource import Resource


class EntityModes(Enum):
    # Ship
    MINE = auto()
    DEPOSIT = auto()
    ATTACK = auto()
    CONVERT = auto()
    # Shipyard
    SPAWN = auto()
    REST = auto()


class ModeResource(Resource):
    def __init__(self, entity_mode):
        super().__init__()
        self.entity_mode = entity_mode

    @classmethod
    def score_matrix(cls, actors):
        repeats = []

        resources = [ModeResource(entity_mode) for entity_mode in EntityModes]

        score_matrix, repeats, resources

    def assign_to_actor(cls, actor, resource):
        actor.mode = resource
