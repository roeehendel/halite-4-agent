from enum import Enum, auto

from kaggle_environments.envs.halite.helpers import ShipyardAction

from actors.actor import Actor
from resources.occupy_cell_resource import OccupyCellResource
from resources.spawn_resource import SpawnResource
from utils.entity_utils import EntityType, EntityList


class ShipyardActor(Actor):
    class Modes(Enum):
        REST = auto()
        SPAWN = auto()

    def __init__(self, entity):
        """
        :param entity: the entity this actor represents
        """
        super().__init__(entity)

    def initial_mode(self):
        return ShipyardActor.Modes.REST

    def choose_mode(self):
        if self.board.step < 370 and \
                EntityList.all_entities(self.board).count(friendly_only=True, entity_types=[EntityType.SHIP]) \
                < min(self.board.step // 10 + 10, 30 - self.board.step // 20):
            self.mode = ShipyardActor.Modes.SPAWN
        else:
            self.mode = ShipyardActor.Modes.REST

    def _get_resource_requests(self, available_resources):
        resource_requests = []

        if self.mode == ShipyardActor.Modes.REST:
            pass
        elif self.mode == ShipyardActor.Modes.SPAWN:
            resource_requests = [
                [SpawnResource, {}],
                [
                    OccupyCellResource,
                    {'cell_position': lambda: self.position}
                ]
            ]

        return resource_requests
