from actors.ship_actor_container import ShipActorContainer
from actors.shipyard_actor_container import ShipyardActorContainer
from agents.base_agent import BaseAgent
from resources.convert_resource import ConvertResource

from resources.deposit_resource import DepositResource
from resources.mine_cell_resource import MineCellResource
from resources.occupy_cell_resource import OccupyCellResource
from resources.spawn_resource import SpawnResource


class Agent(BaseAgent):
    def __init__(self):
        super().__init__()
        # Actor containers
        self.ship_actor_container = ShipActorContainer()
        self.shipyard_actor_container = ShipyardActorContainer()

        # Resources
        self.resources = [SpawnResource, ConvertResource, MineCellResource, DepositResource, OccupyCellResource]

    def get_actions(self, board):
        # Update actors in containers (add new, update existing and remove dead)
        self.ship_actor_container.update(board)
        self.shipyard_actor_container.update(board)
        actors = self.ship_actor_container.actors + self.shipyard_actor_container.actors

        # Remove previous resources
        for actor in actors:
            actor.reset()
            actor.choose_mode()

        # Allocate resources
        for resource in self.resources:
            resource.allocate(board, actors)

        # Use resources
        for actor in actors:
            actor.use_resources()

        return board.current_player.next_actions
