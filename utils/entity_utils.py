from enum import Enum, auto

from kaggle_environments.envs.halite.helpers import Ship, Shipyard

from utils.board_utils import manhattan_distance

from utils.global_vars import GLOBALS


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


def get_entity_by_id(entity_list, entity_id):
    return next(entity for entity in entity_list if entity.id == entity_id)


class EntityList(list):
    def __init__(self, entities):
        super().__init__(entities)

    @staticmethod
    def all_entities():
        return CellList(GLOBALS['board'].cells.values()).entity_list

    def nearest_entity_to(self, point, distance_fn=manhattan_distance):
        return min(self, key=lambda entity: distance_fn(entity.position, point))

    @property
    def positions(self):
        return [e.position for e in self]

    def filter(self, players=None, entity_types=(EntityType.SHIP, EntityType.SHIPYARD),
               friendly_only=False, enemy_only=False, excluded_ids=()):
        def predicate(e):
            # TODO: rewrite this as a loop
            return (players is None or e.player in players) and \
                   (EntityType.from_entity(e) in entity_types) and \
                   (not friendly_only or e.player.is_current_player) and \
                   (not enemy_only or not e.player.is_current_player) and \
                   (e.id not in excluded_ids)

        return EntityList(list(filter(lambda e: predicate(e), self)))

    def count(self, **kwargs):
        return len(self.filter(**kwargs))


class CellList(list):
    def __init__(self, cells):
        super().__init__(cells)

    @property
    def entity_list(self):
        return EntityList(
            filter(lambda x: x is not None, [cell.ship for cell in self] + [cell.shipyard for cell in self])
        )
