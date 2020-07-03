from utils.entity_utils import get_entity_by_id


class ActorContainer:
    """
    This class is responsible for maintaining and updating a list of actors
    """

    def __init__(self):
        self.actors = []
        self.board = None

    def _get_entity_list(self):
        raise NotImplementedError

    def _create_actor(self, entity):
        raise NotImplementedError

    def _update_actors(self):
        entity_list = self._get_entity_list()

        last_turn_ids = set(actor.id for actor in self.actors)
        current_turn_ids = set(entity.id for entity in entity_list)

        removed_ids = last_turn_ids - current_turn_ids
        remained_ids = current_turn_ids.intersection(last_turn_ids)
        added_ids = current_turn_ids - last_turn_ids

        # Remove removed entities
        self.actors = [actor for actor in self.actors if actor.id not in removed_ids]

        # Update remained entities
        for entity_id in remained_ids:
            actor = get_entity_by_id(self.actors, entity_id)
            entity = get_entity_by_id(entity_list, entity_id)
            actor.entity = entity

        # Add added entities
        for entity_id in added_ids:
            entity = get_entity_by_id(entity_list, entity_id)
            self.actors.append(self._create_actor(entity))

        # Update board for all actors
        for actor in self.actors:
            actor.board = self.board

    def update(self, board):
        self.board = board
        self._update_actors()
