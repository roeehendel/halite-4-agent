import math
from enum import Enum, auto

import numpy as np

from actors.actor import Actor
from resources.convert_resource import ConvertResource

from resources.deposit_resource import DepositResource
from resources.mine_cell_resource import MineCellResource
from resources.occupy_cell_resource import OccupyCellResource
from utils.entity_utils import EntityList, EntityType


class ShipActor(Actor):
    class Modes(Enum):
        GO_TO_MINE = auto()
        DEPOSIT = auto()
        CONVERT = auto()

    def __init__(self, entity):
        """
        :param entity: the entity this actor represents
        """
        super().__init__(entity)

    def initial_mode(self):
        return ShipActor.Modes.GO_TO_MINE

    def choose_mode(self):
        shipyard_count = EntityList.all_entities(self.board) \
            .count(friendly_only=True, entity_types=[EntityType.SHIPYARD])
        ship_count = EntityList.all_entities(self.board) \
            .count(friendly_only=True, entity_types=[EntityType.SHIP])

        if shipyard_count < max(1, (ship_count - 2) // 7 + 1) \
                or (self.board.step == 400 and self.entity.halite > self.board.configuration.convert_cost):
            self.mode = ShipActor.Modes.CONVERT

        elif self.entity.halite > 200 * math.exp(-self.board.step / 200):
            self.mode = ShipActor.Modes.DEPOSIT

        else:
            self.mode = ShipActor.Modes.GO_TO_MINE

    def _get_resource_requests(self, available_resources):
        resource_requests = []

        go_to_mine_rrs = [
            [MineCellResource, {}],
            [
                OccupyCellResource,
                {'destination_position': lambda: self.get_my_resource(MineCellResource).cell.position}
            ]
        ]

        deposit_rrs = [
            [DepositResource, {}],
            [
                OccupyCellResource,
                {
                    'destination_position': lambda: self.get_my_resource(DepositResource).shipyard.position
                    if self.get_my_resource(DepositResource) is not None else self.position
                }
            ]
        ]

        if self.mode == ShipActor.Modes.GO_TO_MINE:
            resource_requests = []
            # elif self.mode == 'MINE':
        #     resource_requests = [OccupyCellResource, {'destination_position': self.entity.position}]
        elif self.mode == ShipActor.Modes.DEPOSIT:
            resource_requests = deposit_rrs
        elif self.mode == ShipActor.Modes.CONVERT:
            # TODO: replace this with prioritized request groups
            if len(self._requested_resources) > len(self.resources):
                # resource_requests = deposit_rrs
                resource_requests = []
            else:
                resource_requests = [[ConvertResource, {}]]

        resource_requests += go_to_mine_rrs

        return resource_requests
