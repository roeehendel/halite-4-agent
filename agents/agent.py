import operator
import time
from functools import reduce

from actors.actor import EntityType
from agents.base_agent import BaseAgent
from resources.action.action_resource import ActionResource
from resources.action.convert_action_resource import ConvertActionResource
from resources.action.occupy_action_resource import OccupyActionResource
from resources.action.ship_occupy_action_resource import ShipOccupyActionResource
from resources.action.shipyard_occupy_action_resource import ShipyardOccupyActionResource
from resources.action.spawn_action_resource import SpawnActionResource
from resources.mode.attack_player_resource import AttackEnemyResource
from resources.mode.collect_mode_resource import CollectModeResource
from resources.mode.ship_mode_resource import ShipModeResource
from resources.mode.shipyard_mode_resource import ShipyardModeResource
from resources.tactic.attack_go_to_resource import AttackGoToResource
from resources.tactic.deposit_go_to_resource import DepositGoToResource
from resources.tactic.mine_go_to_resource import MineGoToResource
from utils.entity_utils import ActorList
from utils.global_vars import GLOBALS


def get_by_path(root, items):
    """Access a nested object in root by item sequence."""
    return reduce(operator.getitem, items, root)


class Agent(BaseAgent):
    MODE_RESOURCE_HIERARCHY = [
        [ShipModeResource, ShipyardModeResource],
        [CollectModeResource],
    ]

    TACTIC_RESOURCE_HIERARCHY = [
        [AttackEnemyResource],
        [MineGoToResource, DepositGoToResource, AttackGoToResource],
        [OccupyActionResource, ConvertActionResource, SpawnActionResource]
    ]

    SHIP_RESOURCES_TREE = {
        ShipModeResource.Type.COLLECT: {
            CollectModeResource.Type.MINE: [MineGoToResource, ShipOccupyActionResource],
            CollectModeResource.Type.DEPOSIT: [DepositGoToResource, ShipOccupyActionResource]
        },
        ShipModeResource.Type.ATTACK: [AttackEnemyResource, AttackGoToResource, ShipOccupyActionResource],
        ShipModeResource.Type.CONVERT: [ConvertActionResource],
    }

    SHIPYARD_RESOURCES_TREE = {
        ShipyardModeResource.Type.SPAWN: [ShipyardOccupyActionResource, SpawnActionResource],
        ShipyardModeResource.Type.REST: []
    }

    RESOURCE_TREE = {**SHIP_RESOURCES_TREE, **SHIPYARD_RESOURCES_TREE}

    def __init__(self):
        super().__init__()

    def allocate_modes(self):
        for resource_level in Agent.MODE_RESOURCE_HIERARCHY:
            for resource in resource_level:
                def is_candidate(a):
                    mode_subtree = get_by_path(Agent.RESOURCE_TREE, a.mode_types)
                    if not isinstance(mode_subtree, dict):
                        return False
                    if issubclass(resource, ShipModeResource) and a.entity_type != EntityType.SHIP:
                        return False
                    if issubclass(resource, ShipyardModeResource) and a.entity_type != EntityType.SHIPYARD:
                        return False
                    return any([isinstance(x, resource.Type) for x in list(mode_subtree.keys())])

                candidate_actors = list(filter(is_candidate, ActorList.all()))
                if len(candidate_actors) > 0:
                    resource.allocate(candidate_actors)

    def allocate_resources(self):
        for resource_level in Agent.TACTIC_RESOURCE_HIERARCHY:
            for resource in resource_level:
                start_time = time.time()
                candidate_actors = list(filter(
                    lambda a: any([issubclass(r, resource) for r in get_by_path(Agent.RESOURCE_TREE, a.mode_types)]),
                    ActorList.all())
                )
                if len(candidate_actors) > 0:
                    resource.initialize_turn()
                    resource.allocate(candidate_actors)
                # print(resource, time.time() - start_time)

    def use_action_resources(self):
        for actor in ActorList.all():
            action_resources = list(filter(lambda r: isinstance(r, ActionResource), actor.resources))
            for resource in action_resources:
                resource.use(actor)

    def get_actions(self, board):
        print('TURN (new):', board.step, end=None)
        GLOBALS['board'] = board
        GLOBALS['config'] = board.configuration

        # TODO: perform initializations in a more consistent way
        if board.step == 0:
            MineGoToResource.initialize_once()

        ActorList.reset()

        self.allocate_modes()

        self.allocate_resources()

        self.use_action_resources()

        return board.current_player.next_actions
