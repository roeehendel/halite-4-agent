from kaggle_environments.envs.halite.helpers import Board, ShipAction, ShipyardAction

from actors.ship_actor_container import ShipActorContainer
from actors.shipyard_actor_container import ShipyardActorContainer
from agents.base_agent import BaseAgent
from government.government import Government


class DistributedAgent(BaseAgent):
    def __init__(self):
        super().__init__()
        self.ship_actor_container = ShipActorContainer()
        self.shipyard_actor_container = ShipyardActorContainer()
        # self.government = Government()

        # Government-actors communication
        self.ship_flags = None
        self.shipyard_flags = None
        self.government_flags = None

    def get_actions(self, board):
        self.ship_flags = self.ship_actor_container.update(board, government_flags=self.government_flags)
        self.shipyard_flags = self.shipyard_actor_container.update(board, government_flags=self.government_flags)
        # self.government_flags = self.government.update(board,
        #                                                ship_flags=self.ship_flags,
        #                                                shipyard_flags=self.shipyard_flags)

        return board.current_player.next_actions
