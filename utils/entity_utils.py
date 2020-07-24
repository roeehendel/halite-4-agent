from abc import abstractmethod, ABC

from actors.actor import EntityType, Actor
from utils.global_vars import GLOBALS


def get_entity_by_id(entity_list, entity_id):
    return next(entity for entity in entity_list if entity.id == entity_id)


# Entity Filters

class PlayerFilter:
    def __init__(self, players):
        self.players = players

    def __call__(self, e):
        return e.player in self.players


class EntityTypeFilter:
    def __init__(self, entity_types):
        self.entity_types = entity_types

    def __call__(self, e):
        return EntityType.from_entity(e) in self.entity_types


# List Helpers

class FilterableEntityDataStructure(ABC):
    @abstractmethod
    def filter(self, predicate):
        pass

    @property
    def ships(self):
        return self.filter(EntityTypeFilter([EntityType.SHIP]))

    @property
    def shipyards(self):
        return self.filter(EntityTypeFilter([EntityType.SHIPYARD]))

    @property
    def friendly(self):
        return self.filter(lambda entity: entity.player.is_current_player)

    @property
    def enemy(self):
        return self.filter(lambda entity: not entity.player.is_current_player)


class EntityList(list, FilterableEntityDataStructure):
    def __init__(self, entities):
        super().__init__([entity for entity in entities])

    def filter(self, predicate):
        return EntityList(filter(predicate, self))

    @classmethod
    def all(cls):
        return CellList.all().entity_list


class EntityGroupList(list, FilterableEntityDataStructure):
    def __init__(self, entity_groups):
        super().__init__(entity_groups)

    def filter(self, predicate):
        return EntityGroupList([list(filter(predicate, entity_group)) for entity_group in self])


class ActorList(list, FilterableEntityDataStructure):
    _all = None

    def __init__(self, actors):
        super().__init__([item for item in actors])

    def filter(self, predicate):
        return ActorList(filter(lambda actor: predicate(actor.entity), self))

    @classmethod
    def all(cls):
        if cls._all is None:
            cls._all = ActorList([Actor(e) for e in EntityList.all()]).friendly
        return cls._all

    @classmethod
    def reset(cls):
        cls._all = None


class ActorGroupList(list, FilterableEntityDataStructure):
    def __init__(self, actor_groups):
        super().__init__(actor_groups)

    def filter(self, predicate):
        return ActorGroupList([list(filter(lambda actor: predicate(actor.entity), actor_group))
                               for actor_group in self])


# TODO: consider making filterable
class CellList(list):
    def __init__(self, cells):
        super().__init__(cells)

    @staticmethod
    def all():
        return CellList(GLOBALS['board'].cells.values())

    @property
    def entity_list(self):
        return EntityList(
            filter(lambda x: x is not None, [cell.ship for cell in self] + [cell.shipyard for cell in self])
        )
