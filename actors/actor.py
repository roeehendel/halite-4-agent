from enum import Enum, auto

from kaggle_environments.envs.halite.helpers import Ship, Shipyard


class EntityType(Enum):
    SHIP = auto()
    SHIPYARD = auto()

    def to_class_type(self):
        return (
            Ship if self == EntityType.SHIP else
            Shipyard
        )

    @staticmethod
    def from_class_type(class_type):
        return (
            EntityType.SHIP if class_type == Ship else
            EntityType.SHIPYARD
        )

    @staticmethod
    def from_entity(entity):
        return EntityType.from_class_type(type(entity))


class Actor:
    def __init__(self, entity):
        self.entity = entity
        self.modes = []
        self.resources = []

    @property
    def entity_type(self):
        return EntityType.from_entity(self.entity)

    @property
    def mode_types(self):
        return [mode.mode_type for mode in self.modes]

    @property
    def position(self):
        return self.entity.position
