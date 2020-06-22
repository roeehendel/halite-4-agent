from utils.entity_utils import get_entity_by_id


class ActorContainer():
    def __init__(self):
        self.actors = []
        self.board = None

    def get_entity_list(self):
        raise NotImplementedError

    def create_actor(self, entity):
        raise NotImplementedError

    def update_actors(self):
        entity_list = self.get_entity_list()

        last_turn_ids = set(actor.id for actor in self.actors)
        current_turn_ids = set(entity.id for entity in entity_list)

        removed_ids = last_turn_ids - current_turn_ids
        remained_ids = current_turn_ids.intersection(last_turn_ids)
        added_ids = current_turn_ids - last_turn_ids

        self.actors = [actor for actor in self.actors if actor.id not in removed_ids]  # Remove removed entities

        # Update remained entities
        for entity_id in remained_ids:
            actor = get_entity_by_id(self.actors, entity_id)
            entity = get_entity_by_id(entity_list, entity_id)
            actor.entity = entity

        # Add added entities
        for entity_id in added_ids:
            entity = get_entity_by_id(entity_list, entity_id)
            self.actors.append(self.create_actor(entity))

    def update(self, board, government_flags):
        self.board = board
        self.update_actors()

        flags = []

        for actor in self.actors:
            actor.choose_action(board)
            flags += actor.flags

        return flags
