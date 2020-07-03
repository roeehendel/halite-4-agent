from enum import Enum, auto

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
        if self.entity.halite > 200:
            self.mode = ShipActor.Modes.DEPOSIT
        elif EntityList.all_entities(self.board).count(friendly_only=True, entity_types=[EntityType.SHIPYARD]) < 1:
            self.mode = ShipActor.Modes.CONVERT
        else:
            self.mode = ShipActor.Modes.GO_TO_MINE

    def _get_resource_requests(self, available_resources):
        resource_requests = []

        if self.mode == ShipActor.Modes.GO_TO_MINE:
            resource_requests = [
                [MineCellResource, {}],
                [
                    OccupyCellResource,
                    {'destination_position': lambda: self.get_my_resource(MineCellResource).cell.position}
                ]
            ]
        # elif self.mode == 'MINE':
        #     resource_requests = [OccupyCellResource, {'destination_position': self.entity.position}]
        elif self.mode == ShipActor.Modes.DEPOSIT:
            resource_requests = [
                [DepositResource, {}],
                [
                    OccupyCellResource,
                    {'destination_position': lambda: self.get_my_resource(DepositResource).shipyard.position}
                ]]
        elif self.mode == ShipActor.Modes.CONVERT:
            resource_requests = [[ConvertResource, {}]]

        return resource_requests
