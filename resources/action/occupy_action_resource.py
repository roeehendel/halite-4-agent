import numpy as np
from kaggle_environments.envs.halite.helpers import Ship

from actors.actor import EntityType
from resources.action.action_resource import ActionResource
from resources.actor_scored_resource import ActorScoredResource
from resources.tactic.go_to_resource import GoToResource
from utils.board_utils import diff_vector, point_to_ship_action, get_neighbors, get_neighbor_cells, euclidean_distance
from utils.entity_utils import CellList


class OccupyActionResource(ActorScoredResource, ActionResource):
    def __init__(self, cell):
        super().__init__()
        self.cell = cell

    def use(self, actor):
        if type(actor.entity) == Ship:
            direction = diff_vector(actor.position, self.cell.position)
            action = point_to_ship_action(direction)
            actor.entity.next_action = action

    @staticmethod
    def score(actor, instance):
        cell = instance.cell

        if actor.entity_type == EntityType.SHIPYARD:
            return 3000 if cell.position == actor.position else 0

        # if cell.position not in \
        #         get_neighbors(actor.position) + [actor.position]:
        #     return - np.inf

        if cell.ship is not None and not cell.ship.player.is_current_player \
                and cell.ship.halite <= actor.entity.halite:
            return - 2000

        neighbors = get_neighbor_cells(cell)
        if any([n.ship.halite <= actor.entity.halite for n in neighbors if
                (n.ship is not None and not n.ship.player.is_current_player)]):
            return - 1000  # better then going straight into an enemy (?)

        destination_position = list(filter(lambda r: isinstance(r, GoToResource), actor.resources))[0].cell.position

        return - euclidean_distance(cell.position, destination_position)

    @classmethod
    def actor_scores(cls, actor, instances):
        relevant_cells = get_neighbors(actor.position) + [actor.position]
        relevant_instances = list(filter(lambda x: x.cell.position in relevant_cells, instances))
        relevant_instance_scores = {instance: cls.score(actor, instance) for instance in relevant_instances}
        return [relevant_instance_scores[instance] if instance in relevant_instance_scores else - 999999
                for instance in instances]

    @classmethod
    def instances(cls, actor_groups):
        return [OccupyActionResource(cell) for cell in CellList.all()]

    @classmethod
    def repeats(cls, actor_groups, instances):
        return np.ones(len(instances), dtype=int)
