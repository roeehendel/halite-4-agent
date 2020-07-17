from enum import Enum, auto

from actors.actor import Actor
from agents.base_agent import BaseAgent
from resources.action.action_resource import ActionResource
from resources.action.convert_action_resource import ConvertActionResource
from resources.action.ship_occupy_action_resource import ShipOccupyActionResource
from resources.action.shipyard_occupy_action_resource import ShipyardOccupyActionResource
from resources.action.spawn_action_resource import SpawnActionResource
from resources.mode_resource import ModeResource, EntityModes
from resources.strategic.attack_player_resource import AttackPlayerResource
from resources.tactic.attack_go_to_resource import AttackGoToResource
from resources.tactic.deposit_go_to_resource import DepositGoToResource
from resources.tactic.mine_go_to_resource import MineGoToResource
from resources.tactic.spawn_go_to_resource import SpawnGoToResource

from utils.global_vars import GLOBALS


class Agent(BaseAgent):
    RESOURCE_HIERARCHY = [
        [AttackPlayerResource],
        [MineGoToResource, DepositGoToResource, AttackGoToResource, SpawnGoToResource],
        [ShipOccupyActionResource, ShipyardOccupyActionResource, ConvertActionResource, SpawnActionResource]
    ]

    MODE_RESOURCES = {
        # Ship
        EntityModes.MINE: [MineGoToResource, ShipOccupyActionResource],
        EntityModes.DEPOSIT: [DepositGoToResource, ShipOccupyActionResource],
        EntityModes.ATTACK: [AttackPlayerResource, AttackGoToResource, ShipOccupyActionResource],

        EntityModes.CONVERT: [ConvertActionResource],

        # Shipyard
        EntityModes.SPAWN: [SpawnGoToResource, ShipyardOccupyActionResource, SpawnActionResource],
        EntityModes.REST: []
    }

    def __init__(self):
        super().__init__()
        self.actors = None

    def allocate_modes(self):
        ModeResource.allocate(self.actors)

    def allocate_resources(self):
        for resource_level in Agent.RESOURCE_HIERARCHY:
            for resource in resource_level:
                candidate_actors = list(
                    filter(lambda a: resource in Agent.MODE_RESOURCES[a.mode.entity_mode], self.actors)
                )
                resource.allocate(candidate_actors)

    def use_action_resources(self):
        for actor in self.actors:
            action_resources = list(filter(lambda r: isinstance(r, ActionResource), actor.resources))
            for resource in action_resources:
                resource.use()

    def get_actions(self, board):
        print('TURN:', board.step, end=None)
        GLOBALS['board'] = board
        GLOBALS['config'] = board.configuration

        ships = []  # TODO: find all friendly entities
        shipyards = []
        entities = ships + shipyards
        self.actors = [Actor(e) for e in entities]

        self.allocate_modes()

        self.allocate_resources()

        self.use_action_resources()

        return board.current_player.next_actions
